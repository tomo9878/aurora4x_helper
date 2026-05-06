"""
Aurora 4x DB Reader
使い方: python aurora_reader.py [DBファイルのパス]
出力: aurora_dashboard.html / aurora_gamelog.txt
"""

import sqlite3
import datetime
import sys
import os
import argparse

# ==================== 多言語ラベル ====================

LABELS = {
    "ja": {
        "capital": "首都", "needs_maint": "要整備", "paused": "一時停止",
        "obsolete": "廃止", "support": "支援", "military": "軍用", "civilian": "民間",
        "geo_survey_badge": "地理調査", "grav_survey_badge": "重力調査",
        "in_transit": "艦上輸送中", "unassigned": "未配属", "ok": "正常",
        "all_clear": "全通過", "unexplored": "未通過", "non_combat": "非戦闘",
        "pop": "人口", "speed": "速度", "cost": "コスト", "crew": "乗員",
        "fuel": "燃料", "mag": "弾倉", "shield": "シールド",
        "active": "就役", "hulls": "隻", "no_equip": "装備なし", "slipways_unit": "基",
        "rp_left": "残", "rp_unit": "RP", "labs": "施設数",
        "building": "建造中", "shipyard_default": "造船所",
        "mineral_card": "Mineral Stockpile (首都)",
        "th_mineral": "鉱物", "th_stock": "在庫", "th_ship": "艦名",
        "th_class": "クラス", "th_fleet": "艦隊", "th_fuel": "燃料", "th_status": "状態",
        "th_name": "名称", "th_type": "種別", "th_slipways": "スリップウェイ",
        "th_maxcap": "最大容量", "th_system": "星系名", "th_discovered": "発見日",
        "th_grav": "重力探査", "th_geo": "地理探査", "th_jp": "JP通過",
        "th_minerals": "主要鉱物 Top3",
        "th_formation": "部隊名", "th_commander": "指揮官", "th_sysname": "星系",
        "th_location": "配備天体", "th_tonnage": "総重量", "th_police": "警察力",
        "th_morale": "士気/要塞",
        "th_count": "数", "th_weight": "重量", "th_armourwpn": "装甲/火力",
        "th_equip": "装備・能力", "units_unit": "体", "armour": "装甲", "wpn": "火力",
        "no_research": "研究プロジェクトなし", "no_tasks": "建造タスクなし",
        "no_ships": "艦船なし", "no_systems": "星系データなし",
        "no_formations": "部隊データなし",
        "show_obs": "廃止クラスを表示", "obs_label": "廃止クラス", "obs_unit": "件",
        "colony_candidates": "有望な入植候補 (コスト < 3.0)",
        "th_body": "天体名", "th_colony_cost": "入植コスト",
        "th_temp_c": "表面温度", "cost_exact": "実測", "cost_est": "概算",
        "no_candidates": "なし",
    },
    "en": {
        "capital": "Capital", "needs_maint": "Needs Maint.", "paused": "Paused",
        "obsolete": "Obsolete", "support": "Support", "military": "Military", "civilian": "Civilian",
        "geo_survey_badge": "Geo Survey", "grav_survey_badge": "Grav Survey",
        "in_transit": "In Transit", "unassigned": "Unassigned", "ok": "OK",
        "all_clear": "All Clear", "unexplored": "Unexplored", "non_combat": "Non-Combat",
        "pop": "Pop", "speed": "Speed", "cost": "Cost", "crew": "Crew",
        "fuel": "Fuel", "mag": "Mag", "shield": "Shield",
        "active": "Active", "hulls": "hulls", "no_equip": "No Equipment", "slipways_unit": "slipways",
        "rp_left": "Left", "rp_unit": "RP", "labs": "Labs",
        "building": "Building", "shipyard_default": "Shipyard",
        "mineral_card": "Mineral Stockpile (Capital)",
        "th_mineral": "Mineral", "th_stock": "Stock", "th_ship": "Ship",
        "th_class": "Class", "th_fleet": "Fleet", "th_fuel": "Fuel", "th_status": "Status",
        "th_name": "Name", "th_type": "Type", "th_slipways": "Slipways",
        "th_maxcap": "Max Capacity", "th_system": "System", "th_discovered": "Discovered",
        "th_grav": "Grav Survey", "th_geo": "Geo Survey", "th_jp": "JP Status",
        "th_minerals": "Top 3 Minerals",
        "th_formation": "Formation", "th_commander": "Commander", "th_sysname": "System",
        "th_location": "Location", "th_tonnage": "Tonnage", "th_police": "Police",
        "th_morale": "Morale/Fort",
        "th_count": "Count", "th_weight": "Weight", "th_armourwpn": "Armour/Wpn",
        "th_equip": "Equipment & Capabilities", "units_unit": "units", "armour": "Arm", "wpn": "Wpn",
        "no_research": "No research projects", "no_tasks": "No construction tasks",
        "no_ships": "No ships", "no_systems": "No system data",
        "no_formations": "No formation data",
        "show_obs": "Show Obsolete Classes", "obs_label": "Obsolete classes", "obs_unit": "",
        "colony_candidates": "Colony Candidates (Cost < 3.0)",
        "th_body": "Body", "th_colony_cost": "Col. Cost",
        "th_temp_c": "Surf. Temp", "cost_exact": "exact", "cost_est": "est.",
        "no_candidates": "None",
    },
}

_LANG = "ja"

def L(key):
    return LABELS[_LANG][key]

# ==================== DB接続 ====================

def get_db_path(db_arg=None):
    if db_arg:
        return db_arg
    default = os.path.join(os.path.dirname(os.path.abspath(__file__)), "AuroraDB.db")
    if os.path.exists(default):
        return default
    print("使い方: python aurora_reader.py [AuroraDB.dbのパス]")
    sys.exit(1)

def connect(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

BASE_DATE = datetime.datetime(2025, 1, 1)

def aurora_time(sec):
    if not sec:
        return "出発点"
    return (BASE_DATE + datetime.timedelta(seconds=float(sec))).strftime("%Y-%m-%d")

MINERAL_NAMES = {
    1: "Duranium", 2: "Neutronium", 3: "Corbomite", 4: "Tritanium",
    5: "Boronide", 6: "Mercassium", 7: "Vendarite", 8: "Sorium",
    9: "Uridium", 10: "Corundium", 11: "Gallicite"
}

# ==================== データ取得 ====================

def get_games(conn):
    cur = conn.cursor()
    cur.execute("SELECT GameID, GameName, GameTime FROM FCT_Game ORDER BY GameID DESC")
    return [dict(r) for r in cur.fetchall()]

def get_player_races(conn, game_id):
    cur = conn.cursor()
    cur.execute("SELECT RaceID, RaceName, WealthPoints, Research FROM FCT_Race WHERE GameID=? AND NPR=0 ORDER BY RaceID", (game_id,))
    return [dict(r) for r in cur.fetchall()]

def get_research(conn, game_id, race_id):
    cur = conn.cursor()
    cur.execute("""
        SELECT rp.TechID, ts.Name, rp.Facilities, rp.ResearchPointsRequired, rp.Pause
        FROM FCT_ResearchProject rp
        LEFT JOIN FCT_TechSystem ts ON rp.TechID = ts.TechSystemID
        WHERE rp.GameID=? AND rp.RaceID=?
        ORDER BY rp.ResearchPointsRequired
    """, (game_id, race_id))
    return [dict(r) for r in cur.fetchall()]

def get_fleets(conn, game_id, race_id):
    cur = conn.cursor()
    cur.execute("SELECT FleetID, FleetName FROM FCT_Fleet WHERE GameID=? AND RaceID=? ORDER BY FleetID", (game_id, race_id))
    return [dict(r) for r in cur.fetchall()]

def get_ships(conn, game_id, race_id):
    cur = conn.cursor()
    cur.execute("""
        SELECT s.ShipName, s.FleetID, s.Fuel, s.MaintenanceState, sc.ClassName
        FROM FCT_Ship s JOIN FCT_ShipClass sc ON s.ShipClassID = sc.ShipClassID
        WHERE s.GameID=? AND s.RaceID=? AND s.Destroyed=0 AND s.ShippingLineID=0
        ORDER BY s.ShipName
    """, (game_id, race_id))
    return [dict(r) for r in cur.fetchall()]

def get_shipyard_tasks(conn, game_id, race_id):
    cur = conn.cursor()
    cur.execute("""
        SELECT st.TotalBP, st.CompletedBP, st.Paused, st.UnitName, sy.ShipyardName
        FROM FCT_ShipyardTask st
        LEFT JOIN FCT_Shipyard sy ON st.ShipyardID = sy.ShipyardID
        WHERE st.GameID=? AND st.RaceID=?
    """, (game_id, race_id))
    return [dict(r) for r in cur.fetchall()]

def get_shipyards(conn, game_id, race_id):
    cur = conn.cursor()
    cur.execute("SELECT ShipyardID, ShipyardName, Slipways, Capacity, SYType FROM FCT_Shipyard WHERE GameID=? AND RaceID=? ORDER BY Capacity DESC", (game_id, race_id))
    return [dict(r) for r in cur.fetchall()]

def get_populations(conn, game_id, race_id):
    cur = conn.cursor()
    cur.execute("""
        SELECT PopulationID, PopName, Population, Capital,
               Duranium, Neutronium, Corbomite, Tritanium, Boronide,
               Mercassium, Vendarite, Sorium, Uridium, Corundium, Gallicite
        FROM FCT_Population WHERE GameID=? AND RaceID=? ORDER BY Population DESC
    """, (game_id, race_id))
    return [dict(r) for r in cur.fetchall()]


def load_mineral_snapshot(base_dir):
    import json
    path = os.path.join(base_dir, "aurora_mineral_snapshot.json")
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

def save_mineral_snapshot(base_dir, pops, game_time):
    import json
    data = {
        "game_time": game_time,
        "pops": {}
    }
    minerals = ["Duranium","Neutronium","Corbomite","Tritanium","Boronide",
                "Mercassium","Vendarite","Sorium","Uridium","Corundium","Gallicite"]
    for p in pops:
        data["pops"][p["PopName"]] = {m: p[m] or 0 for m in minerals}
    path = os.path.join(base_dir, "aurora_mineral_snapshot.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def calc_mineral_diff(pops, snapshot):
    if not snapshot:
        return {}
    minerals = ["Duranium","Neutronium","Corbomite","Tritanium","Boronide",
                "Mercassium","Vendarite","Sorium","Uridium","Corundium","Gallicite"]
    diff = {}
    for p in pops:
        name = p["PopName"]
        prev = snapshot.get("pops", {}).get(name)
        if not prev:
            continue
        diff[name] = {}
        for m in minerals:
            cur_val = p[m] or 0
            prv_val = prev.get(m, 0) or 0
            diff[name][m] = cur_val - prv_val
    return diff

def get_unexplored_jp(conn, game_id, race_id):
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) as cnt FROM FCT_RaceJumpPointSurvey WHERE GameID=? AND RaceID=? AND Explored=0", (game_id, race_id))
    row = cur.fetchone()
    return row["cnt"] if row else 0


# 基本部品として除外するCategoryID
BASIC_CATEGORIES = {
    1,   # Armour
    11,  # Bridge/Engineering/Crew/Fuel等の構造系
}
# エンジンカテゴリ
ENGINE_CATEGORIES = {7}

def get_ship_classes(conn, game_id, race_id):
    cur = conn.cursor()
    cur.execute("""
        SELECT ShipClassID, ClassName, Size, MaxSpeed, Cost, Crew,
               Commercial, Obsolete, TotalNumber, MagazineCapacity,
               GeoSurvey, GravSurvey, FuelCapacity, ShieldStrength,
               MilitaryEngines
        FROM FCT_ShipClass
        WHERE GameID=? AND RaceID=? AND AutomatedDesignID=0
        ORDER BY Obsolete, ShipClassID
    """, (game_id, race_id))
    classes = [dict(r) for r in cur.fetchall()]

    class_ids = [c["ShipClassID"] for c in classes]
    if not class_ids:
        return []
    ph = ",".join("?" * len(class_ids))

    # コンポーネント取得
    cur.execute(
        "SELECT cc.ClassID, cc.ComponentID, cc.NumComponent, ts.Name, ts.CategoryID "
        "FROM FCT_ClassComponent cc "
        "LEFT JOIN FCT_TechSystem ts ON cc.ComponentID=ts.TechSystemID "
        "WHERE cc.GameID=? AND cc.ClassID IN (" + ph + ") "
        "ORDER BY cc.ClassID, ts.CategoryID, cc.ChanceToHit",
        [game_id] + class_ids
    )
    comp_rows = cur.fetchall()

    comp_map = {}
    for r in comp_rows:
        cid = r["ClassID"]
        if cid not in comp_map:
            comp_map[cid] = []
        comp_map[cid].append(dict(r))

    for c in classes:
        cid = c["ShipClassID"]
        comps = comp_map.get(cid, [])
        # エンジン
        engines = [r for r in comps if r["CategoryID"] in ENGINE_CATEGORIES]
        # 特殊装備（基本部品・エンジン以外）
        specials = [r for r in comps if r["CategoryID"] not in BASIC_CATEGORIES and r["CategoryID"] not in ENGINE_CATEGORIES]
        c["engines"] = engines
        c["specials"] = specials
    return classes

def get_systems(conn, game_id, race_id):
    cur = conn.cursor()
    cur.execute("""
        SELECT SystemID, Name, SurveyDone, GeoSurveyDefaultDone, DiscoveredTime
        FROM FCT_RaceSysSurvey WHERE GameID=? AND RaceID=? ORDER BY DiscoveredTime
    """, (game_id, race_id))
    systems = [dict(r) for r in cur.fetchall()]
    sys_ids = [s["SystemID"] for s in systems]
    if not sys_ids:
        return []
    ph = ",".join("?" * len(sys_ids))

    cur.execute(
        "SELECT jp.SystemID, COUNT(*) as total_jp, SUM(CASE WHEN rjp.Explored=1 THEN 1 ELSE 0 END) as explored_jp "
        "FROM FCT_JumpPoint jp "
        "LEFT JOIN FCT_RaceJumpPointSurvey rjp ON jp.WarpPointID=rjp.WarpPointID AND rjp.GameID=? AND rjp.RaceID=? "
        "WHERE jp.GameID=? AND jp.SystemID IN (" + ph + ") GROUP BY jp.SystemID",
        [game_id, race_id, game_id] + sys_ids
    )
    jp_map = {r["SystemID"]: dict(r) for r in cur.fetchall()}

    cur.execute(
        "SELECT sb.SystemID, COUNT(DISTINCT sb.SystemBodyID) as total_bodies, COUNT(DISTINCT sbs.SystemBodyID) as geo_done "
        "FROM FCT_SystemBody sb "
        "LEFT JOIN FCT_SystemBodySurveys sbs ON sb.SystemBodyID=sbs.SystemBodyID AND sbs.GameID=? AND sbs.RaceID=? "
        "WHERE sb.GameID=? AND sb.SystemID IN (" + ph + ") GROUP BY sb.SystemID",
        [game_id, race_id, game_id] + sys_ids
    )
    geo_map = {r["SystemID"]: dict(r) for r in cur.fetchall()}

    cur.execute(
        "SELECT md.SystemID, md.MaterialID, SUM(md.Amount) as total "
        "FROM FCT_MineralDeposit md "
        "JOIN FCT_SystemBodySurveys sbs "
        "  ON md.SystemBodyID=sbs.SystemBodyID AND sbs.GameID=? AND sbs.RaceID=? "
        "WHERE md.GameID=? AND md.SystemID IN (" + ph + ") "
        "GROUP BY md.SystemID, md.MaterialID",
        [game_id, race_id, game_id] + sys_ids
    )
    mineral_map = {}
    for r in cur.fetchall():
        sid = r["SystemID"]
        if sid not in mineral_map:
            mineral_map[sid] = {}
        mineral_map[sid][r["MaterialID"]] = round(r["total"])

    for s in systems:
        sid = s["SystemID"]
        jp = jp_map.get(sid, {})
        s["total_jp"] = jp.get("total_jp", 0)
        s["explored_jp"] = jp.get("explored_jp", 0) or 0
        s["unexplored_jp"] = s["total_jp"] - s["explored_jp"]
        geo = geo_map.get(sid, {})
        s["total_bodies"] = geo.get("total_bodies", 0)
        s["geo_done"] = geo.get("geo_done", 0)
        s["minerals"] = mineral_map.get(sid, {})
    return systems

def calc_colony_cost_approx(temp, grav, press, gases, sp):
    """Approximate colony cost from physical parameters (not exact Aurora formula)."""
    temp_excess = max(0.0, abs(temp - sp["Temperature"]) - sp["TempDev"])
    grav_excess = max(0.0, abs(grav - sp["Gravity"]) - sp["GravDev"])

    breathe_id = sp["BreatheID"]
    breathe_atm = gases.get(breathe_id, {}).get("atm", 0.0)
    o2_min = max(0.0, sp["Oxygen"] - sp["OxyDev"])
    o2_max = sp["Oxygen"] + sp["OxyDev"]
    o2_ok = o2_min <= breathe_atm <= o2_max
    press_max = sp["PressMax"] or 10.0

    temp_cost = temp_excess * 0.01
    grav_cost = grav_excess * 23.0
    atmos_cost = 0.0
    if not o2_ok:
        atmos_cost = 2.0
    if press > press_max:
        atmos_cost += (press - press_max) * 1.0

    total = temp_cost + grav_cost + atmos_cost
    if total > 0.0:
        total = max(2.0, total)
    return round(total, 2)


def get_colony_candidates(conn, game_id, race_id):
    """
    Returns promising colonization candidates with colony cost < 3.0, grouped by system.
    Existing colonies use exact LastColonyCost; uninhabited geo-surveyed bodies use approx.
    """
    cur = conn.cursor()

    # Primary species for this race (from capital colony)
    cur.execute("""
        SELECT s.BreatheID, s.Oxygen, s.OxyDev, s.PressMax,
               s.Temperature, s.TempDev, s.Gravity, s.GravDev
        FROM FCT_Species s
        JOIN FCT_Population p ON p.SpeciesID = s.SpeciesID AND p.GameID = s.GameID
        WHERE p.GameID = ? AND p.RaceID = ? AND p.Capital = 1
        LIMIT 1
    """, (game_id, race_id))
    sp_row = cur.fetchone()
    if not sp_row:
        cur.execute("""
            SELECT DISTINCT s.BreatheID, s.Oxygen, s.OxyDev, s.PressMax,
                   s.Temperature, s.TempDev, s.Gravity, s.GravDev
            FROM FCT_Species s
            JOIN FCT_Population p ON p.SpeciesID = s.SpeciesID AND p.GameID = s.GameID
            WHERE p.GameID = ? AND p.RaceID = ?
            LIMIT 1
        """, (game_id, race_id))
        sp_row = cur.fetchone()
    if not sp_row:
        return []
    sp = dict(sp_row)

    # System name map
    cur.execute("SELECT SystemID, Name FROM FCT_RaceSysSurvey WHERE GameID=? AND RaceID=?", (game_id, race_id))
    sys_name_map = {r["SystemID"]: r["Name"] for r in cur.fetchall()}
    known_sys = list(sys_name_map.keys())
    if not known_sys:
        return []

    results = []

    # 1. Existing colonies with exact cost (cost > 0 and < 3, skip homeworld)
    cur.execute("""
        SELECT p.PopName, p.LastColonyCost, p.SystemBodyID, p.SystemID
        FROM FCT_Population p
        WHERE p.GameID=? AND p.RaceID=? AND p.LastColonyCost > 0.0 AND p.LastColonyCost < 3.0
    """, (game_id, race_id))
    for r in cur.fetchall():
        results.append({
            "system": sys_name_map.get(r["SystemID"], "?"),
            "system_id": r["SystemID"],
            "body": r["PopName"],
            "cost": r["LastColonyCost"],
            "temp_c": None,
            "grav": None,
            "exact": True,
        })

    # 2. Geo-surveyed uninhabited bodies
    ph = ",".join("?" * len(known_sys))
    cur.execute(f"""
        SELECT sb.SystemBodyID, sb.SystemID, sb.Name,
               sb.SurfaceTemp, sb.Gravity, sb.AtmosPress
        FROM FCT_SystemBody sb
        JOIN FCT_SystemBodySurveys sbs ON sb.SystemBodyID=sbs.SystemBodyID
            AND sbs.GameID=? AND sbs.RaceID=?
        LEFT JOIN FCT_Population p ON p.SystemBodyID=sb.SystemBodyID AND p.GameID=?
        WHERE sb.GameID=? AND sb.SystemID IN ({ph})
          AND p.SystemBodyID IS NULL
    """, [game_id, race_id, game_id, game_id] + known_sys)
    uninhabited = [dict(r) for r in cur.fetchall()]

    if uninhabited:
        body_ids = [b["SystemBodyID"] for b in uninhabited]
        ph2 = ",".join("?" * len(body_ids))
        cur.execute(f"""
            SELECT ag.SystemBodyID, ag.AtmosGasID, ag.GasAtm,
                   g.Dangerous, g.DangerousLevel
            FROM FCT_AtmosphericGas ag
            JOIN DIM_Gases g ON g.GasID=ag.AtmosGasID
            WHERE ag.GameID=? AND ag.SystemBodyID IN ({ph2})
        """, [game_id] + body_ids)
        gas_map = {}
        for r in cur.fetchall():
            bid = r["SystemBodyID"]
            if bid not in gas_map:
                gas_map[bid] = {}
            gas_map[bid][r["AtmosGasID"]] = {"atm": r["GasAtm"], "dangerous": r["Dangerous"]}

        for body in uninhabited:
            cost = calc_colony_cost_approx(
                body["SurfaceTemp"], body["Gravity"], body["AtmosPress"],
                gas_map.get(body["SystemBodyID"], {}), sp
            )
            if cost < 3.0:
                results.append({
                    "system": sys_name_map.get(body["SystemID"], "?"),
                    "system_id": body["SystemID"],
                    "body": body["Name"] or ("Body #" + str(body["SystemBodyID"])),
                    "cost": cost,
                    "temp_c": round(body["SurfaceTemp"] - 273.15, 1),
                    "grav": round(body["Gravity"], 2),
                    "exact": False,
                })

    results.sort(key=lambda x: (x["system"], x["cost"]))
    return results


def get_gamelog(conn, game_id, race_id, after_time=None, after_increment=None):
    cur = conn.cursor()
    if after_time is not None and after_increment is not None:
        cur.execute("""
            SELECT gl.Time, gl.IncrementID, gl.EventType, gl.MessageText, det.Description
            FROM FCT_GameLog gl
            LEFT JOIN DIM_EventType det ON gl.EventType = det.EventTypeID
            WHERE gl.GameID=? AND gl.RaceID=?
              AND (gl.Time > ? OR (gl.Time = ? AND gl.IncrementID > ?))
            ORDER BY gl.Time, gl.IncrementID
        """, (game_id, race_id, after_time, after_time, after_increment))
    else:
        cur.execute("""
            SELECT gl.Time, gl.IncrementID, gl.EventType, gl.MessageText, det.Description
            FROM FCT_GameLog gl
            LEFT JOIN DIM_EventType det ON gl.EventType = det.EventTypeID
            WHERE gl.GameID=? AND gl.RaceID=?
            ORDER BY gl.Time, gl.IncrementID
        """, (game_id, race_id))
    return [dict(r) for r in cur.fetchall()]

def get_ground_formations(conn, game_id, race_id):
    import math
    cur = conn.cursor()
    cur.execute("""
        SELECT
            f.FormationID, f.Name as FormationName, f.Abbreviation, f.Civilian,
            f.PopulationID, f.ShipID,
            p.PopName, p.SystemBodyID,
            ss.Name as SystemName,
            sb.Name as BodyName,
            c.Name as CommanderName
        FROM FCT_GroundUnitFormation f
        LEFT JOIN FCT_Population p ON f.PopulationID=p.PopulationID AND p.GameID=?
        LEFT JOIN FCT_RaceSysSurvey ss ON p.SystemID=ss.SystemID AND ss.GameID=? AND ss.RaceID=?
        LEFT JOIN FCT_SystemBody sb ON p.SystemBodyID=sb.SystemBodyID AND sb.GameID=?
        LEFT JOIN FCT_Commander c ON c.CommandID=f.FormationID AND c.GameID=? AND c.RaceID=?
            AND c.CommandType=5 AND c.Deceased=0
        WHERE f.GameID=? AND f.RaceID=?
        ORDER BY f.Civilian, f.FormationID
    """, (game_id, game_id, race_id, game_id, game_id, race_id, game_id, race_id))
    formations = [dict(r) for r in cur.fetchall()]

    # 各フォーメーションの構成ユニット詳細を取得
    fids = [f["FormationID"] for f in formations]
    if not fids:
        return formations
    ph = ",".join("?" * len(fids))
    cur.execute("""
        SELECT
            fe.FormationID, fe.Units, fe.Morale, fe.FortificationLevel,
            gu.GroundUnitClassID, gu.ClassName, gu.Size, gu.NonCombatClass,
            gu.ArmourStrengthModifier, gu.WeaponStrengthModifier,
            gu.HQCapacity, gu.ConstructionRating,
            bt.Name as BaseTypeName, bt.HitPoints,
            ca.ComponentName as CompA, cb.ComponentName as CompB,
            ca.Penetration as PenA, ca.Damage as DmgA, ca.Shots as ShotsA,
            cb.Penetration as PenB, cb.Damage as DmgB, cb.Shots as ShotsB,
            ca.AAWeapon as AAA, ca.BombardmentWeapon as BombA,
            cb.AAWeapon as AAB, cb.BombardmentWeapon as BombB
        FROM FCT_GroundUnitFormationElement fe
        JOIN FCT_GroundUnitClass gu ON fe.ClassID=gu.GroundUnitClassID AND gu.GameID=?
        LEFT JOIN DIM_GroundUnitBaseType bt ON gu.BaseType=bt.UnitBaseTypeID
        LEFT JOIN DIM_GroundComponentType ca ON gu.ComponentA=ca.ComponentTypeID
        LEFT JOIN DIM_GroundComponentType cb ON gu.ComponentB=cb.ComponentTypeID
        WHERE fe.GameID=? AND fe.FormationID IN (""" + ph + """)
        ORDER BY fe.FormationID, gu.NonCombatClass, gu.Size DESC
    """, [game_id, game_id] + fids)
    elem_rows = cur.fetchall()

    # ケイパビリティ取得
    cur.execute("""
        SELECT gc.GroundUnitClassID, cap.CapabilityName
        FROM FCT_GroundUnitCapability gc
        JOIN DIM_GroundUnitCapability cap ON gc.CapabilityID=cap.CapabilityID
        WHERE gc.GameID=? AND gc.CapabilityID != 0
    """, (game_id,))
    cap_map = {}
    for r in cur.fetchall():
        cap_map.setdefault(r["GroundUnitClassID"], []).append(r["CapabilityName"])

    # FormationIDをキーに要素を集約
    elem_map = {}
    for r in elem_rows:
        fid = r["FormationID"]
        if fid not in elem_map:
            elem_map[fid] = []
        e = dict(r)
        e["capabilities"] = cap_map.get(e["GroundUnitClassID"], [])
        e["police"] = math.sqrt(e["Size"]) / 100 * e["Units"]
        elem_map[fid].append(e)

    # フォーメーションにサマリー情報を付加
    for f in formations:
        elems = elem_map.get(f["FormationID"], [])
        f["elements"] = elems
        f["total_tonnage"] = sum(e["Units"] * e["Size"] for e in elems)
        f["total_units"] = sum(e["Units"] for e in elems)
        f["combat_units"] = sum(e["Units"] for e in elems if not e["NonCombatClass"])
        f["police_strength"] = math.floor(sum(e["police"] for e in elems))
        morale = elems[0]["Morale"] if elems else None
        f["morale"] = round(morale) if morale else "—"
        fortif = elems[0]["FortificationLevel"] if elems else None
        f["fortification"] = fortif if fortif is not None else "—"
    return formations

def load_last_log_pos(base_dir, game_id):
    """前回の最終ログ位置を読み込む (Time, IncrementID)。ゲームIDが変わったらリセット"""
    pos_path = os.path.join(base_dir, "aurora_log_pos.txt")
    if not os.path.exists(pos_path):
        return None, None
    try:
        with open(pos_path, "r", encoding="utf-8") as f:
            parts = f.read().strip().split(",")
            if int(parts[0]) != game_id:
                return None, None  # 別ゲームのデータなので初回扱い
            return float(parts[1]), int(parts[2])
    except Exception:
        return None, None

def save_last_log_pos(base_dir, game_id, logs):
    """最終ログ位置を保存"""
    if not logs:
        return
    last = logs[-1]
    pos_path = os.path.join(base_dir, "aurora_log_pos.txt")
    with open(pos_path, "w", encoding="utf-8") as f:
        f.write(str(game_id) + "," + str(last["Time"]) + "," + str(last["IncrementID"]))

# ==================== テキスト生成 ====================

def build_log_text(logs, race_name, game_name):
    lines = [
        "# Aurora 4x Game Log",
        "# Game: " + game_name,
        "# Race: " + race_name,
        "# Total events: " + str(len(logs)),
        "",
    ]
    prev_year = prev_date = None
    for row in logs:
        game_date = BASE_DATE + datetime.timedelta(seconds=float(row["Time"]))
        date_str = game_date.strftime("%Y-%m-%d")
        year_str = game_date.strftime("%Y")
        if year_str != prev_year:
            lines.append("\n=== " + year_str + " ===")
            prev_year = year_str
            prev_date = None
        if date_str != prev_date:
            lines.append("\n--- " + date_str + " ---")
            prev_date = date_str
        label = row["Description"] if row["Description"] else "Event" + str(row["EventType"])
        lines.append("[" + label + "] " + row["MessageText"])
    return "\n".join(lines)

# ==================== HTML生成 ====================

def pct(completed, total):
    if not total:
        return 0
    return min(100, round(completed / total * 100))

def _build_army_rows(formations):
    if not formations:
        return '<tr><td colspan="8" class="empty-note">' + L("no_formations") + '</td></tr>'

    COMP_ICON = {
        "Anti-Vehicle": "🔴", "Anti-Personnel": "🟡", "Anti-Aircraft": "🔵",
        "Bombardment": "💥", "Surface-to-Orbit": "🚀", "Headquarters": "⭐",
        "Logistics": "📦", "Construction": "🔧", "Geosurvey": "🔬",
        "Xenoarchaeology": "🏺", "Personal Weapons": "🔫",
    }

    def comp_icon(name):
        if not name:
            return ""
        for k, v in COMP_ICON.items():
            if k in name:
                return v
        return ""

    rows = ""
    for idx, f in enumerate(formations):
        fid = f["FormationID"]
        kind = '<span class="badge-com">' + L("civilian") + '</span>' if f["Civilian"] else '<span class="badge-mil">' + L("military") + '</span>'
        commander = f["CommanderName"] or '—'
        system = f["SystemName"] or "—"
        body = f["BodyName"] or f["PopName"] or "—"
        if f["ShipID"]:
            body = '<span class="badge-warn">' + L("in_transit") + '</span>'
        tonnage = f'{int(f["total_tonnage"]):,}t'
        police = str(f["police_strength"])
        morale = str(f["morale"])
        fortif = str(f["fortification"])

        rows += (
            '<tr class="army-row" onclick="toggleArmy(' + str(idx) + ')" style="cursor:pointer">'
            '<td class="army-name">▶ ' + (f["FormationName"] or "—") + '</td>'
            '<td style="text-align:center">' + kind + '</td>'
            '<td>' + commander + '</td>'
            '<td class="sys-name">' + system + '</td>'
            '<td>' + body + '</td>'
            '<td style="text-align:right;font-family:monospace">' + tonnage + '</td>'
            '<td style="text-align:right;font-family:monospace">' + police + '</td>'
            '<td style="text-align:center">' + morale + ' / <span style="color:#f39c12">' + fortif + '</span></td>'
            '</tr>'
        )

        elem_rows = ""
        for e in f["elements"]:
            caps = " ".join(
                '<span class="equip-tag special" style="font-size:9px">' + c + '</span>'
                for c in e["capabilities"]
            )
            comps = ""
            if e["CompA"]:
                icon = comp_icon(e["CompA"])
                stats = ""
                if e["ShotsA"] and e["ShotsA"] > 0:
                    stats = f' P{e["PenA"]}/D{e["DmgA"]}×{e["ShotsA"]}'
                comps += '<span class="equip-tag">' + icon + " " + e["CompA"] + stats + '</span> '
            if e["CompB"]:
                icon = comp_icon(e["CompB"])
                stats = ""
                if e["ShotsB"] and e["ShotsB"] > 0:
                    stats = f' P{e["PenB"]}/D{e["DmgB"]}×{e["ShotsB"]}'
                comps += '<span class="equip-tag">' + icon + " " + e["CompB"] + stats + '</span>'
            nc_badge = '<span style="color:var(--text2);font-size:10px"> [' + L("non_combat") + ']</span>' if e["NonCombatClass"] else ""
            elem_rows += (
                '<tr>'
                '<td style="color:var(--text2);font-size:11px;padding-left:12px">' + e["BaseTypeName"] + nc_badge + '</td>'
                '<td style="font-family:monospace;font-size:12px">' + e["ClassName"] + '</td>'
                '<td style="text-align:right;font-size:12px">' + str(e["Units"]) + ' ' + L("units_unit") + '</td>'
                '<td style="text-align:right;font-size:11px;color:var(--text2)">' + str(e["Size"]) + 't</td>'
                '<td style="font-size:11px;color:var(--text2)">' + L("armour") + ' ' + str(e["ArmourStrengthModifier"]) + ' / ' + L("wpn") + ' ' + str(e["WeaponStrengthModifier"]) + '</td>'
                '<td colspan="3" style="font-size:11px">' + comps + caps + '</td>'
                '</tr>'
            )

        rows += (
            '<tr id="army-detail-' + str(idx) + '" style="display:none">'
            '<td colspan="8" style="padding:0;background:var(--bg)">'
            '<table style="width:100%;margin:4px 0;border-collapse:collapse">'
            '<thead><tr style="background:var(--bg3)">'
            '<th style="font-size:10px;padding:4px 8px;text-align:left">' + L("th_type") + '</th>'
            '<th style="font-size:10px;padding:4px 8px;text-align:left">' + L("th_class") + '</th>'
            '<th style="font-size:10px;padding:4px 8px;text-align:right">' + L("th_count") + '</th>'
            '<th style="font-size:10px;padding:4px 8px;text-align:right">' + L("th_weight") + '</th>'
            '<th style="font-size:10px;padding:4px 8px">' + L("th_armourwpn") + '</th>'
            '<th colspan="3" style="font-size:10px;padding:4px 8px">' + L("th_equip") + '</th>'
            '</tr></thead>'
            '<tbody>' + elem_rows + '</tbody>'
            '</table>'
            '</td></tr>'
        )
    return rows

def build_html(game, race, research, fleets, ships, tasks, shipyards, pops, unexplored_jp, systems, ship_classes, ground_formations, snapshot=None, colony_candidates=None):
    game_name = game["GameName"]
    race_name = race["RaceName"]
    wealth = round(race["WealthPoints"])
    research_cap = race["Research"]
    generated_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    game_time_str = aurora_time(game["GameTime"])

    # --- 植民地 ---
    pop_cards = ""
    for p in pops:
        pop_m = round(p["Population"])
        badge = '<span class="badge-cap">' + L("capital") + '</span>' if p["Capital"] else ""
        pop_cards += (
            '<div class="pop-card">'
            '<div class="pop-name">' + p["PopName"] + " " + badge + '</div>'
            '<div class="pop-detail">' + L("pop") + ' ' + f'{pop_m:,}' + 'M</div>'
            '</div>'
        )

    # --- 鉱物 ---
    earth = next((p for p in pops if p["Capital"] == 1), pops[0] if pops else None)
    mineral_diff = calc_mineral_diff(pops, snapshot) if snapshot else {}
    earth_diff = mineral_diff.get(earth["PopName"], {}) if earth else {}
    mineral_rows = ""
    if earth:
        minerals = [
            ("Duranium", earth["Duranium"]), ("Neutronium", earth["Neutronium"]),
            ("Corbomite", earth["Corbomite"]), ("Tritanium", earth["Tritanium"]),
            ("Boronide", earth["Boronide"]), ("Mercassium", earth["Mercassium"]),
            ("Vendarite", earth["Vendarite"]), ("Sorium", earth["Sorium"]),
            ("Uridium", earth["Uridium"]), ("Corundium", earth["Corundium"]),
            ("Gallicite", earth["Gallicite"]),
        ]
        for name, val in minerals:
            v = round(val or 0)
            bar_w = min(100, int(v / 2000))
            warn = ' style="color:#e67e22;"' if v < 5000 else ''
            d = earth_diff.get(name, None)
            if d is None:
                diff_cell = '<td class="min-diff" style="color:var(--text2)">—</td>'
            elif d > 0:
                diff_cell = '<td class="min-diff" style="color:#2ecc71">+</td>'
            elif d < 0:
                diff_cell = '<td class="min-diff" style="color:#e74c3c">−</td>'
            else:
                diff_cell = '<td class="min-diff" style="color:var(--text2)">±0</td>'
            mineral_rows += (
                '<tr>'
                '<td class="min-label"' + warn + '>' + name + '</td>'
                '<td class="min-val"' + warn + '>' + f'{v:,}' + '</td>'
                + diff_cell +
                '<td class="min-bar"><div class="bar-track"><div class="bar-fill" style="width:' + str(bar_w) + '%"></div></div></td>'
                '</tr>'
            )

    # --- 研究 ---
    research_items = ""
    colors = ["#2ecc71","#3498db","#9b59b6","#e67e22","#e74c3c","#95a5a6","#1abc9c"]
    for i, r in enumerate(research):
        pts = round(r["ResearchPointsRequired"])
        name = r["Name"] or "Tech " + str(r["TechID"])
        fac = r["Facilities"]
        bar_w = max(5, 100 - min(100, int(pts / 100)))
        color = colors[i % len(colors)]
        research_items += (
            '<div class="research-item">'
            '<div class="research-header">'
            '<span class="research-name">' + name + '</span>'
            '<span class="research-pts">' + L("rp_left") + ' ' + f'{pts:,}' + ' ' + L("rp_unit") + ' &nbsp;|&nbsp; ' + L("labs") + ' ' + str(fac) + '</span>'
            '</div>'
            '<div class="bar-track"><div class="bar-fill" style="width:' + str(bar_w) + '%;background:' + color + '"></div></div>'
            '</div>'
        )
    if not research_items:
        research_items = '<div class="empty-note">' + L("no_research") + '</div>'

    # --- 造船タスク ---
    task_items = ""
    for t in tasks:
        p = pct(t["CompletedBP"], t["TotalBP"])
        name = t["UnitName"] or L("building")
        sy = t["ShipyardName"] or L("shipyard_default")
        paused = '<span class="badge-warn">' + L("paused") + '</span>' if t["Paused"] else ""
        task_items += (
            '<div class="task-item">'
            '<div class="task-header">'
            '<span class="task-name">' + name + " " + paused + '</span>'
            '<span class="task-pct">' + str(p) + '%</span>'
            '</div>'
            '<div class="task-sub">' + sy + '</div>'
            '<div class="bar-track"><div class="bar-fill" style="width:' + str(p) + '%;background:#3498db"></div></div>'
            '</div>'
        )
    if not task_items:
        task_items = '<div class="empty-note">' + L("no_tasks") + '</div>'

    # --- 造船所 ---
    sy_rows = ""
    for sy in shipyards:
        sy_type = L("civilian") if sy["SYType"] == 2 else L("military")
        sy_rows += (
            '<tr>'
            '<td>' + sy["ShipyardName"] + '</td>'
            '<td>' + sy_type + '</td>'
            '<td>' + str(int(sy["Slipways"])) + ' ' + L("slipways_unit") + '</td>'
            '<td>' + f'{int(sy["Capacity"]):,}' + ' t</td>'
            '</tr>'
        )

    # --- 艦船 ---
    fleet_map = {f["FleetID"]: f["FleetName"] for f in fleets}
    ship_rows = ""
    for s in ships:
        fleet_name = fleet_map.get(s["FleetID"], L("unassigned"))
        fuel = round(s["Fuel"])
        maint = s["MaintenanceState"]
        status = '<span class="badge-warn">' + L("needs_maint") + '</span>' if maint and maint > 0 else L("ok")
        ship_rows += (
            '<tr>'
            '<td>' + s["ShipName"] + '</td>'
            '<td>' + s["ClassName"] + '</td>'
            '<td>' + fleet_name + '</td>'
            '<td>' + f'{fuel:,}' + '</td>'
            '<td>' + status + '</td>'
            '</tr>'
        )
    if not ship_rows:
        ship_rows = '<tr><td colspan="5" class="empty-note">' + L("no_ships") + '</td></tr>'

    # --- 星系テーブル ---
    sys_rows = ""
    for s in systems:
        name = s["Name"]
        gravity = "✔" if s["SurveyDone"] else "—"
        geo_done = s["geo_done"]
        geo_total = s["total_bodies"]
        if geo_done >= geo_total and geo_total > 0:
            geo_str = "✔"
        else:
            geo_str = str(geo_done) + "/" + str(geo_total)
        jp_unex = s["unexplored_jp"]
        if not s["SurveyDone"]:
            jp_str = "—"
        elif jp_unex > 0:
            jp_str = '<span class="badge-warn">' + str(jp_unex) + ' ' + L("unexplored") + '</span>'
        else:
            jp_str = '<span style="color:#00ff9d">' + L("all_clear") + '</span>'
        mins = s["minerals"]
        top3 = sorted(mins.items(), key=lambda x: x[1], reverse=True)[:3]
        min_str = " / ".join(MINERAL_NAMES.get(mid, "?") + " " + f"{amt:,}" for mid, amt in top3) if top3 else "—"
        disc = aurora_time(s["DiscoveredTime"])
        sys_rows += (
            '<tr>'
            '<td class="sys-name">' + name + '</td>'
            '<td style="text-align:center">' + disc + '</td>'
            '<td style="text-align:center">' + gravity + '</td>'
            '<td style="text-align:center">' + geo_str + '</td>'
            '<td style="text-align:center">' + jp_str + '</td>'
            '<td class="sys-minerals">' + min_str + '</td>'
            '</tr>'
        )
    if not sys_rows:
        sys_rows = '<tr><td colspan="6" class="empty-note">' + L("no_systems") + '</td></tr>'

    # --- コロニー候補テーブル ---
    colony_rows = ""
    if colony_candidates:
        prev_sys = None
        for c in colony_candidates:
            if c["system"] != prev_sys:
                colspan = 5
                colony_rows += (
                    '<tr style="background:#0d1a0d">'
                    '<td colspan="' + str(colspan) + '" style="color:#00ff9d;font-weight:bold;padding:4px 8px">'
                    + c["system"] + '</td></tr>'
                )
                prev_sys = c["system"]
            cost_val = f'{c["cost"]:.2f}'
            cost_tag = L("cost_exact") if c["exact"] else L("cost_est")
            if c["cost"] <= 2.0:
                cost_color = "#00ff9d"
            elif c["cost"] <= 2.5:
                cost_color = "#f0c040"
            else:
                cost_color = "#e07060"
            temp_str = (str(c["temp_c"]) + "°C") if c["temp_c"] is not None else "—"
            grav_str = (str(c["grav"]) + "G") if c["grav"] is not None else "—"
            colony_rows += (
                '<tr>'
                '<td style="padding-left:20px">' + (c["body"] or "?") + '</td>'
                '<td style="text-align:center;color:' + cost_color + ';font-weight:bold">'
                + cost_val + '</td>'
                '<td style="text-align:center;font-size:11px;color:#888">(' + cost_tag + ')</td>'
                '<td style="text-align:center">' + temp_str + '</td>'
                '<td style="text-align:center">' + grav_str + '</td>'
                '</tr>'
            )
    if not colony_rows:
        colony_rows = '<tr><td colspan="5" class="empty-note">' + L("no_candidates") + '</td></tr>'

    # --- 設計書タブ ---
    WEAPON_CATS = {2, 3, 26, 28, 39, 40}
    SENSOR_CATS = {13, 14, 34}

    def equip_class(cat_id):
        if cat_id in WEAPON_CATS: return "weapon"
        if cat_id in SENSOR_CATS: return "sensor"
        return "special"

    design_cards_active = ""
    design_cards_obs = ""

    for cls in ship_classes:
        name = cls["ClassName"]
        size_hs = round(cls["Size"])
        speed = int(cls["MaxSpeed"])
        cost = round(cls["Cost"])
        crew = cls["Crew"]
        mag = int(cls["MagazineCapacity"] or 0)
        mil = cls["MilitaryEngines"]
        com = cls["Commercial"]
        obs = cls["Obsolete"]
        total = cls["TotalNumber"] or 0
        fuel = int(cls["FuelCapacity"] or 0)
        shield = round(cls["ShieldStrength"] or 0)
        geo = cls["GeoSurvey"]
        grav = cls["GravSurvey"]

        badges = ""
        if obs:
            badges += '<span class="design-badge badge-obs">' + L("obsolete") + '</span>'
        if mil and com:
            badges += '<span class="design-badge badge-sup">' + L("support") + '</span>'
        elif mil:
            badges += '<span class="design-badge badge-mil">' + L("military") + '</span>'
        elif com:
            badges += '<span class="design-badge badge-com">' + L("civilian") + '</span>'
        if geo:
            badges += '<span class="design-badge" style="color:#f39c12;border-color:#f39c12;background:#1a1000">' + L("geo_survey_badge") + '</span>'
        if grav:
            badges += '<span class="design-badge" style="color:#f39c12;border-color:#f39c12;background:#1a1000">' + L("grav_survey_badge") + '</span>'

        stats = (
            '<span><b>' + str(size_hs) + '</b> HS</span>'
            '<span>' + L("speed") + ' <b>' + f'{speed:,}' + '</b> km/s</span>'
            '<span>' + L("cost") + ' <b>' + f'{cost:,}' + '</b></span>'
            '<span>' + L("crew") + ' <b>' + str(crew) + '</b></span>'
            '<span>' + L("fuel") + ' <b>' + f'{fuel:,}' + '</b> L</span>'
        )
        if mag > 0:
            stats += '<span>' + L("mag") + ' <b>' + str(mag) + '</b></span>'
        if shield > 0:
            stats += '<span>' + L("shield") + ' <b>' + str(shield) + '</b></span>'
        if total > 0:
            stats += '<span>' + L("active") + ' <b>' + str(total) + '</b> ' + L("hulls") + '</span>'

        equip_tags = ""
        for e in cls["engines"]:
            n_raw = e["NumComponent"]
            n = int(n_raw) if n_raw == int(n_raw) else round(n_raw, 1)
            equip_tags += '<span class="equip-tag engine">×' + str(n) + ' ' + (e["Name"] or "Engine") + '</span>'

        for s in cls["specials"]:
            cat = s["CategoryID"] or 0
            ec = equip_class(cat)
            n_raw = s["NumComponent"]
            n = int(n_raw) if n_raw == int(n_raw) else round(n_raw, 1)
            equip_tags += '<span class="equip-tag ' + ec + '">×' + str(n) + ' ' + (s["Name"] or "?") + '</span>'

        if not equip_tags:
            equip_tags = '<span class="equip-tag">' + L("no_equip") + '</span>'

        card = (
            '<div class="design-card' + (' obsolete' if obs else '') + '">' 
            '<div class="design-header"><span class="design-name">' + name + '</span>' + badges + '</div>'
            '<div class="design-stats">' + stats + '</div>'
            '<div class="design-equip">' + equip_tags + '</div>'
            '</div>'
        )
        if obs:
            design_cards_obs += card
        else:
            design_cards_active += card

    # ==================== HTMLテンプレート ====================
    css = """
    :root {
      --bg: #0a0e1a; --bg2: #111828; --bg3: #1a2236;
      --accent: #00c8ff; --accent2: #00ff9d;
      --warn: #f39c12; --text: #cdd9f0; --text2: #7a93b8;
      --border: #1e3050; --card-radius: 8px;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background: var(--bg); color: var(--text); font-family: 'Noto Sans JP', sans-serif; font-size: 14px; line-height: 1.6; padding: 24px; }
    .mono { font-family: 'Share Tech Mono', monospace; }
    .header { border-bottom: 1px solid var(--border); padding-bottom: 16px; margin-bottom: 20px; display: flex; align-items: baseline; gap: 16px; flex-wrap: wrap; }
    .header h1 { font-family: 'Share Tech Mono', monospace; font-size: 22px; font-weight: 400; color: var(--accent); letter-spacing: 2px; }
    .header .meta { font-size: 12px; color: var(--text2); }
    .tab-bar { display: flex; gap: 2px; margin-bottom: 0; border-bottom: 1px solid var(--border); }
    .tab-btn { background: none; border: none; border-bottom: 2px solid transparent; color: var(--text2); font-size: 13px; padding: 8px 20px; cursor: pointer; font-family: 'Share Tech Mono', monospace; letter-spacing: 1px; margin-bottom: -1px; }
    .tab-btn.active { color: var(--accent); border-bottom-color: var(--accent); }
    .tab-panel { display: none; padding-top: 16px; }
    .tab-panel.active { display: block; }
    .stat-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 10px; margin-bottom: 24px; }
    .stat-card { background: var(--bg2); border: 1px solid var(--border); border-radius: var(--card-radius); padding: 12px 16px; }
    .stat-label { font-size: 11px; color: var(--text2); margin-bottom: 4px; letter-spacing: 1px; text-transform: uppercase; }
    .stat-value { font-family: 'Share Tech Mono', monospace; font-size: 22px; color: var(--accent); }
    .stat-value.warn { color: var(--warn); }
    .two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px; }
    @media (max-width: 700px) { .two-col { grid-template-columns: 1fr; } }
    .card { background: var(--bg2); border: 1px solid var(--border); border-radius: var(--card-radius); padding: 16px 20px; margin-bottom: 16px; }
    .card-title { font-family: 'Share Tech Mono', monospace; font-size: 13px; color: var(--accent); letter-spacing: 2px; text-transform: uppercase; margin-bottom: 14px; padding-bottom: 8px; border-bottom: 1px solid var(--border); }
    .bar-track { height: 4px; background: var(--bg3); border-radius: 2px; overflow: hidden; margin-top: 4px; }
    .bar-fill { height: 100%; background: var(--accent2); border-radius: 2px; }
    .research-item { margin-bottom: 12px; }
    .research-header { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 3px; }
    .research-name { font-size: 12px; color: var(--text); }
    .research-pts { font-size: 11px; color: var(--text2); white-space: nowrap; margin-left: 8px; }
    .task-item { margin-bottom: 12px; }
    .task-header { display: flex; justify-content: space-between; align-items: baseline; }
    .task-name { font-size: 12px; color: var(--text); }
    .task-pct { font-family: 'Share Tech Mono', monospace; font-size: 13px; color: var(--accent); }
    .task-sub { font-size: 11px; color: var(--text2); margin-bottom: 3px; }
    table { width: 100%; border-collapse: collapse; font-size: 12px; }
    th { color: var(--text2); font-weight: 500; text-align: left; padding: 4px 8px 6px; border-bottom: 1px solid var(--border); font-size: 11px; letter-spacing: 1px; text-transform: uppercase; }
    td { padding: 5px 8px; border-bottom: 1px solid var(--border); color: var(--text); }
    tr:last-child td { border-bottom: none; }
    tr:hover td { background: var(--bg3); }
    .min-label { width: 100px; color: var(--text2); }
    .min-val { font-family: 'Share Tech Mono', monospace; width: 90px; text-align: right; }
    .min-bar { width: 100%; padding-left: 8px; }
    .min-diff { font-family: 'Share Tech Mono', monospace; width: 36px; text-align: center; font-size: 14px; font-weight: bold; }
    .pop-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 8px; }
    .pop-card { background: var(--bg3); border: 1px solid var(--border); border-radius: 6px; padding: 10px 12px; }
    .pop-name { font-size: 13px; font-weight: 500; color: var(--text); margin-bottom: 2px; }
    .pop-detail { font-size: 11px; color: var(--text2); }
    .badge-cap { display: inline-block; font-size: 10px; background: #1a3a4a; color: var(--accent); border: 1px solid var(--accent); border-radius: 3px; padding: 1px 5px; margin-left: 4px; vertical-align: middle; }
    .badge-warn { display: inline-block; font-size: 10px; background: #3a2a0a; color: var(--warn); border: 1px solid var(--warn); border-radius: 3px; padding: 1px 5px; margin-left: 4px; vertical-align: middle; }
    .empty-note { color: var(--text2); font-size: 12px; padding: 8px 0; }
    .sys-name { font-family: 'Share Tech Mono', monospace; font-size: 12px; color: var(--accent); }
    .design-card { background: var(--bg2); border: 1px solid var(--border); border-radius: var(--card-radius); padding: 14px 18px; margin-bottom: 10px; }
    .design-card.obsolete { opacity: 0.5; }
    .design-header { display: flex; align-items: baseline; gap: 12px; flex-wrap: wrap; margin-bottom: 8px; }
    .design-name { font-family: 'Share Tech Mono', monospace; font-size: 14px; color: var(--accent); }
    .design-badge { font-size: 10px; padding: 2px 7px; border-radius: 3px; border: 1px solid; }
    .badge-mil { color: #e74c3c; border-color: #e74c3c; background: #2a0a0a; }
    .badge-com { color: #3498db; border-color: #3498db; background: #0a1a2a; }
    .badge-sup { color: #f39c12; border-color: #f39c12; background: #1a1000; }
    .badge-obs { color: #555; border-color: #555; background: #111; }
    .design-stats { display: flex; flex-wrap: wrap; gap: 16px; font-size: 12px; color: var(--text2); margin-bottom: 8px; }
    .design-stats span b { color: var(--text); }
    .design-equip { display: flex; flex-wrap: wrap; gap: 6px; }
    .equip-tag { font-size: 11px; background: var(--bg3); border: 1px solid var(--border); border-radius: 3px; padding: 2px 8px; color: var(--text2); }
    .equip-tag.weapon { border-color: #c0392b; color: #e74c3c; background: #1a0505; }
    .equip-tag.sensor { border-color: #2980b9; color: #5dade2; background: #050d1a; }
    .equip-tag.special { border-color: #8e44ad; color: #af7ac5; background: #0e0516; }
    .equip-tag.engine { border-color: #27ae60; color: #58d68d; background: #051a0a; }
    .designs-controls { margin-bottom: 14px; display: flex; gap: 10px; align-items: center; }
    .designs-controls label { font-size: 12px; color: var(--text2); display: flex; align-items: center; gap: 5px; cursor: pointer; }
    .sys-minerals { font-size: 11px; color: var(--text2); }
    .footer { margin-top: 32px; padding-top: 12px; border-top: 1px solid var(--border); font-size: 11px; color: var(--text2); text-align: right; }
    .army-name { font-family: 'Share Tech Mono', monospace; font-size: 13px; color: var(--accent); }
    .army-row:hover td { background: var(--bg3) !important; }
    """

    warn_class = " warn" if unexplored_jp > 5 else ""

    html_parts = [
        '<!DOCTYPE html>',
        '<html lang="' + _LANG + '">',
        '<head>',
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '<title>Aurora 4x — ' + race_name + ' Dashboard</title>',
        '<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Noto+Sans+JP:wght@400;500&display=swap" rel="stylesheet">',
        '<style>' + css + '</style>',
        '</head>',
        '<body>',

        '<div class="header">',
        '<h1>[ ' + race_name + ' ] EMPIRE DASHBOARD</h1>',
        '<span class="meta">GAME: ' + game_name + ' &nbsp;|&nbsp; DATE: ' + game_time_str + ' &nbsp;|&nbsp; GENERATED: ' + generated_at + '</span>',
        '</div>',

        '<div class="tab-bar">',
        '<button class="tab-btn active" onclick="showTab(\'main\',this)">EMPIRE</button>',
        '<button class="tab-btn" onclick="showTab(\'systems\',this)">SYSTEMS</button>',
        '<button class="tab-btn" onclick="showTab(\'army\',this)">ARMY</button>',
        '<button class="tab-btn" onclick="showTab(\'designs\',this)">DESIGNS</button>',
        '</div>',

        # === EMPIRE タブ ===
        '<div id="tab-main" class="tab-panel active">',

        '<div class="stat-grid">',
        '<div class="stat-card"><div class="stat-label">Wealth</div><div class="stat-value">' + f'{wealth:,}' + '</div></div>',
        '<div class="stat-card"><div class="stat-label">Research Cap</div><div class="stat-value">' + str(research_cap) + '</div></div>',
        '<div class="stat-card"><div class="stat-label">Colonies</div><div class="stat-value">' + str(len(pops)) + '</div></div>',
        # Unexplored JP非表示（重力調査前はネタバレになるため）
        '<div class="stat-card"><div class="stat-label">Active Ships</div><div class="stat-value">' + str(len(ships)) + '</div></div>',
        '<div class="stat-card"><div class="stat-label">Fleets</div><div class="stat-value">' + str(len(fleets)) + '</div></div>',
        '</div>',

        '<div class="two-col">',
        '<div class="card"><div class="card-title">Research Queue</div>' + research_items + '</div>',
        '<div>',
        '<div class="card"><div class="card-title">Shipyard Tasks</div>' + task_items + '</div>',
        '<div class="card"><div class="card-title">Colonies</div><div class="pop-grid">' + pop_cards + '</div></div>',
        '</div>',
        '</div>',

        '<div class="two-col">',
        '<div class="card"><div class="card-title">' + L("mineral_card") + '</div><table><thead><tr><th>' + L("th_mineral") + '</th><th>' + L("th_stock") + '</th><th></th></tr></thead><tbody>' + mineral_rows + '</tbody></table></div>',
        '<div class="card"><div class="card-title">Active Ships</div><table><thead><tr><th>' + L("th_ship") + '</th><th>' + L("th_class") + '</th><th>' + L("th_fleet") + '</th><th>' + L("th_fuel") + '</th><th>' + L("th_status") + '</th></tr></thead><tbody>' + ship_rows + '</tbody></table></div>',
        '</div>',

        '<div class="card"><div class="card-title">Shipyards</div><table><thead><tr><th>' + L("th_name") + '</th><th>' + L("th_type") + '</th><th>' + L("th_slipways") + '</th><th>' + L("th_maxcap") + '</th></tr></thead><tbody>' + sy_rows + '</tbody></table></div>',

        '</div>',  # /tab-main

        # === SYSTEMS タブ ===
        '<div id="tab-systems" class="tab-panel">',
        '<div class="card"><div class="card-title">Discovered Systems</div>',
        '<div style="overflow-x:auto">',
        '<table><thead><tr><th>' + L("th_system") + '</th><th>' + L("th_discovered") + '</th><th>' + L("th_grav") + '</th><th>' + L("th_geo") + '</th><th>' + L("th_jp") + '</th><th>' + L("th_minerals") + '</th></tr></thead>',
        '<tbody>' + sys_rows + '</tbody></table>',
        '</div></div>',
        '<div class="card"><div class="card-title">' + L("colony_candidates") + '</div>',
        '<div style="overflow-x:auto">',
        '<table><thead><tr>'
        '<th>' + L("th_body") + '</th>'
        '<th style="text-align:center">' + L("th_colony_cost") + '</th>'
        '<th></th>'
        '<th style="text-align:center">' + L("th_temp_c") + '</th>'
        '<th style="text-align:center">' + L("th_grav") + '</th>'
        '</tr></thead>',
        '<tbody>' + colony_rows + '</tbody></table>',
        '</div></div>',
        '</div>',  # /tab-systems

        # === ARMY タブ ===
        '<div id="tab-army" class="tab-panel">',
        '<div class="card"><div class="card-title">Ground Forces</div>',
        '<div style="overflow-x:auto">',
        '<table><thead><tr>'
        '<th>' + L("th_formation") + '</th><th>' + L("th_type") + '</th><th>' + L("th_commander") + '</th><th>' + L("th_sysname") + '</th><th>' + L("th_location") + '</th>'
        '<th style="text-align:right">' + L("th_tonnage") + '</th><th style="text-align:right">' + L("th_police") + '</th><th style="text-align:center">' + L("th_morale") + '</th>'
        '</tr></thead>',
        '<tbody>' + _build_army_rows(ground_formations) + '</tbody></table>',
        '</div>',
        '</div>',
        '</div>',  # /tab-army

        # === DESIGNS タブ ===
        '<div id="tab-designs" class="tab-panel">',
        '<div class="card">',
        '<div class="card-title">Ship Designs</div>',
        '<div class="designs-controls">',
        '<label><input type="checkbox" id="show-obs" onchange="toggleObs()"> ' + L("show_obs") + '</label>',
        '<span style="font-size:11px;color:var(--text2)" id="obs-count"></span>',
        '</div>',
        '<div id="designs-active">' + design_cards_active + '</div>',
        '<div id="designs-obs" style="display:none">' + design_cards_obs + '</div>',
        '</div>',
        '</div>',  # /tab-designs

        '<script>',
        'function showTab(id,btn){',
        'document.querySelectorAll(".tab-panel").forEach(p=>p.classList.remove("active"));',
        'document.querySelectorAll(".tab-btn").forEach(b=>b.classList.remove("active"));',
        'document.getElementById("tab-"+id).classList.add("active");',
        'btn.classList.add("active");',
        '}',
        'function toggleArmy(idx){',
        'var d=document.getElementById("army-detail-"+idx);',
        'var row=d.previousElementSibling;',
        'var open=d.style.display==="none";',
        'd.style.display=open?"table-row":"none";',
        'var cell=row.querySelector(".army-name");',
        'cell.textContent=cell.textContent.replace(open?"▶":"▼",open?"▼":"▶");',
        '}',
        'function toggleObs(){',
        'var show=document.getElementById("show-obs").checked;',
        'document.getElementById("designs-obs").style.display=show?"block":"none";',
        '}',
        '(function(){',
        'var n=document.getElementById("designs-obs").children.length;',
        'document.getElementById("obs-count").textContent="' + L("obs_label") + ' "+n+"' + L("obs_unit") + '";',
        '})();',
        '</script>',

        '<div class="footer">Aurora 4x Dashboard Generator &mdash; ' + generated_at + '</div>',
        '</body>',
        '</html>',
    ]

    return "\n".join(html_parts)

# ==================== メイン ====================

def main():
    global _LANG
    parser = argparse.ArgumentParser(description="Aurora 4x Dashboard Generator")
    parser.add_argument("--lang", choices=["ja", "en"], default="ja", help="Output language (default: ja)")
    parser.add_argument("db", nargs="?", default=None, help="Path to AuroraDB.db")
    args = parser.parse_args()
    _LANG = args.lang

    db_path = get_db_path(args.db)
    print("DB: " + db_path)

    conn = connect(db_path)
    games = get_games(conn)
    if not games:
        print("ゲームデータが見つかりませんでした。")
        return

    game = games[0]
    game_id = game["GameID"]
    print("ゲーム: " + game["GameName"] + " (ID:" + str(game_id) + ")")

    player_races = get_player_races(conn, game_id)
    if not player_races:
        print("プレイヤー帝国が見つかりませんでした。")
        return

    if len(player_races) == 1:
        race = player_races[0]
    else:
        print("\nプレイヤー帝国を選択してください:")
        for i, r in enumerate(player_races):
            print("  " + str(i+1) + ". " + r["RaceName"] + " (ID:" + str(r["RaceID"]) + ")")
        try:
            idx = int(input("番号を入力: ")) - 1
            race = player_races[idx]
        except (ValueError, IndexError):
            race = player_races[0]

    race_id = race["RaceID"]
    print("帝国: " + race["RaceName"] + " (ID:" + str(race_id) + ")")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    # EN run is HTML-only; state files (log pos, snapshot) are managed by the JA run
    is_primary = (_LANG == "ja")
    snapshot          = load_mineral_snapshot(base_dir) if is_primary else None
    systems           = get_systems(conn, game_id, race_id)
    ship_classes      = get_ship_classes(conn, game_id, race_id)
    research          = get_research(conn, game_id, race_id)
    fleets            = get_fleets(conn, game_id, race_id)
    ships             = get_ships(conn, game_id, race_id)
    tasks             = get_shipyard_tasks(conn, game_id, race_id)
    shipyards         = get_shipyards(conn, game_id, race_id)
    pops              = get_populations(conn, game_id, race_id)
    unexplored        = get_unexplored_jp(conn, game_id, race_id)
    ground            = get_ground_formations(conn, game_id, race_id)
    colony_candidates = get_colony_candidates(conn, game_id, race_id)

    # 前回の最終ログ位置を読み込み（JA実行のみ）
    if is_primary:
        last_time, last_inc = load_last_log_pos(base_dir, game_id)
        is_first = last_time is None

        # ロールバック検出: 保存済みの位置がDBの最新ログより未来なら位置をリセット
        if last_time is not None:
            _cur = conn.cursor()
            _cur.execute(
                "SELECT MAX(Time) as mt FROM FCT_GameLog WHERE GameID=? AND RaceID=?",
                (game_id, race_id)
            )
            _row = _cur.fetchone()
            if _row and _row["mt"] is not None and float(_row["mt"]) < last_time:
                print("[WARN] セーブのロールバックを検出しました。ログ位置をリセットします。")
                last_time, last_inc = None, None
                is_first = True

        logs = get_gamelog(conn, game_id, race_id, last_time, last_inc)
    conn.close()

    html_filename = "aurora_dashboard_en.html" if _LANG == "en" else "aurora_dashboard.html"
    html_path = os.path.join(base_dir, html_filename)
    log_path  = os.path.join(base_dir, "aurora_gamelog.txt")

    html = build_html(game, race, research, fleets, ships, tasks, shipyards, pops, unexplored, systems, ship_classes, ground, snapshot, colony_candidates)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("\n[OK] ダッシュボード: " + html_path)

    if not is_primary:
        return

    save_mineral_snapshot(base_dir, pops, game["GameTime"])

    diff_path = os.path.join(base_dir, "aurora_gamelog_diff.txt")

    if logs:
        log_text = build_log_text(logs, race["RaceName"], game["GameName"])

        # 全ログ累積（ニヤニヤ用）
        mode = "w" if is_first else "a"
        label = "全件" if is_first else "差分"
        with open(log_path, mode, encoding="utf-8") as f:
            if not is_first:
                f.write("\n\n")
            f.write(log_text)
        print("[OK] 全ログ:         " + log_path + " (" + label + " " + str(len(logs)) + "件追加)")

        # 差分のみ（AAR投げ用）
        with open(diff_path, "w", encoding="utf-8") as f:
            f.write(log_text)
        print("[OK] 差分ログ:       " + diff_path + " (" + str(len(logs)) + "件)")

        save_last_log_pos(base_dir, game_id, logs)
    else:
        print("[OK] ログ:           新規ログなし (前回以降の更新なし)")
        # 差分ファイルは空にしておく
        with open(diff_path, "w", encoding="utf-8") as f:
            f.write("# No new events since last run.")

    print("\n完了！ブラウザで aurora_dashboard.html を開いてください。")

if __name__ == "__main__":
    main()

"""
Aurora 4x Mineral Resource Viewer
使い方: python aurora_minerals.py [AuroraDB.dbのパス]
出力: aurora_minerals.html
"""

import sqlite3
import datetime
import sys
import os

MINERAL_NAMES = {
    1: "Duranium", 2: "Neutronium", 3: "Corbomite", 4: "Tritanium",
    5: "Boronide", 6: "Mercassium", 7: "Vendarite", 8: "Sorium",
    9: "Uridium", 10: "Corundium", 11: "Gallicite"
}

BASE_DATE = datetime.datetime(2025, 1, 1)

def get_db_path():
    if len(sys.argv) > 1:
        return sys.argv[1]
    default = os.path.join(os.path.dirname(os.path.abspath(__file__)), "AuroraDB.db")
    if os.path.exists(default):
        return default
    print("使い方: python aurora_minerals.py [AuroraDB.dbのパス]")
    sys.exit(1)

def get_latest_game(conn):
    cur = conn.cursor()
    cur.execute("SELECT GameID, GameName FROM FCT_Game ORDER BY GameID DESC LIMIT 1")
    return dict(cur.fetchone())

def get_player_race(conn, game_id):
    cur = conn.cursor()
    cur.execute("SELECT RaceID, RaceName FROM FCT_Race WHERE GameID=? AND NPR=0 ORDER BY RaceID LIMIT 1", (game_id,))
    return dict(cur.fetchone())

def get_mining_rate(conn, game_id, race_id):
    """完了済み技術からMining Production rateを取得"""
    cur = conn.cursor()
    cur.execute("""
        SELECT ts.Name, ts.AdditionalInfo
        FROM FCT_RaceTech rt
        JOIN FCT_TechSystem ts ON rt.TechID = ts.TechSystemID
        WHERE rt.GameID=? AND rt.RaceID=?
        AND ts.Name LIKE 'Mining Production%'
        ORDER BY ts.AdditionalInfo DESC
        LIMIT 1
    """, (game_id, race_id))
    row = cur.fetchone()
    if row:
        return int(row["AdditionalInfo"])
    return 5  # デフォルト

def get_orbital_mining_diameter(conn, game_id, race_id):
    """完了済み技術から最大軌道採掘直径を取得"""
    cur = conn.cursor()
    cur.execute("""
        SELECT ts.AdditionalInfo
        FROM FCT_RaceTech rt
        JOIN FCT_TechSystem ts ON rt.TechID = ts.TechSystemID
        WHERE rt.GameID=? AND rt.RaceID=?
        AND ts.Name LIKE 'Maximum Orbital Mining Diameter%'
        ORDER BY ts.AdditionalInfo DESC
        LIMIT 1
    """, (game_id, race_id))
    row = cur.fetchone()
    return int(row["AdditionalInfo"]) if row else 0

def get_mineral_data(conn, game_id, race_id):
    """調査済み天体の鉱物データを取得"""
    cur = conn.cursor()
    cur.execute("""
        SELECT
            sb.SystemBodyID,
            NULLIF(sb.Name,'') as BodyName,
            sb.BodyClass,
            sb.BodyTypeID,
            sb.Radius,
            sb.PlanetNumber,
            sb.OrbitNumber,
            sb.ParentBodyID,
            ss.Name as SystemName,
            md.MaterialID,
            md.Amount,
            md.Accessibility
        FROM FCT_MineralDeposit md
        JOIN FCT_SystemBody sb ON md.SystemBodyID=sb.SystemBodyID AND sb.GameID=?
        JOIN FCT_SystemBodySurveys sbs ON md.SystemBodyID=sbs.SystemBodyID
            AND sbs.GameID=? AND sbs.RaceID=?
        JOIN FCT_RaceSysSurvey ss ON md.SystemID=ss.SystemID
            AND ss.GameID=? AND ss.RaceID=?
        WHERE md.GameID=? AND md.Amount > 0
        ORDER BY ss.Name, sb.PlanetNumber, sb.OrbitNumber, md.MaterialID
    """, (game_id, game_id, race_id, game_id, race_id, game_id))
    rows = cur.fetchall()

    # 惑星番号→ローマ数字変換
    def to_roman(n):
        vals = [(1000,'M'),(900,'CM'),(500,'D'),(400,'CD'),(100,'C'),(90,'XC'),
                (50,'L'),(40,'XL'),(10,'X'),(9,'IX'),(5,'V'),(4,'IV'),(1,'I')]
        r = ''
        for v, s in vals:
            while n >= v:
                r += s; n -= v
        return r

    # 親天体のPlanetNumberを引くためのマップ
    parent_ids = set(r["ParentBodyID"] for r in rows if r["ParentBodyID"])
    parent_map = {}
    if parent_ids:
        ph = ",".join("?" * len(parent_ids))
        cur.execute(
            "SELECT SystemBodyID, Name, PlanetNumber FROM FCT_SystemBody WHERE SystemBodyID IN (" + ph + ")",
            list(parent_ids)
        )
        for p in cur.fetchall():
            parent_map[p["SystemBodyID"]] = p

    def make_body_name(r):
        if r["BodyName"]:
            return r["BodyName"]
        planet_num = r["PlanetNumber"] or 0
        orbit_num = r["OrbitNumber"] or 0
        body_class = r["BodyClass"]
        if body_class == 2:  # 衛星
            parent = parent_map.get(r["ParentBodyID"])
            parent_planet = parent["PlanetNumber"] if parent else planet_num
            return "Moon " + to_roman(parent_planet) + " " + str(orbit_num)
        elif body_class == 3:  # 小惑星
            return "Asteroid Belt " + to_roman(planet_num)
        else:
            return to_roman(planet_num) if planet_num else "(unnamed)"

    # 天体ごとに集約
    bodies = {}
    for r in rows:
        body_name = make_body_name(r)
        key = (r["SystemName"], body_name, r["SystemBodyID"])
        if key not in bodies:
            bodies[key] = {
            "minerals": {},
            "body_class": r["BodyClass"],
            "body_type": r["BodyTypeID"],
            "radius": r["Radius"] or 0,
        }
        bodies[key]["minerals"][r["MaterialID"]] = {
            "amount": r["Amount"],
            "accessibility": r["Accessibility"]
        }

    # リスト化
    result = []
    for (sys_name, body_name, body_id), data in bodies.items():
        result.append({
            "system": sys_name,
            "body": body_name,
            "body_class": data["body_class"],
            "body_type": data["body_type"],
            "radius": data["radius"],
            "minerals": data["minerals"]
        })
    return result

def build_html(game, race, bodies, mining_rate, orbital_diameter=0):
    generated_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    race_name = race["RaceName"]
    game_name = game["GameName"]

    # 天体行のHTML生成
    # 軌道採掘対象判定（小惑星:BodyClass=3, 彗星:BodyClass=5）
    ORBITAL_CLASSES = {3, 5}

    def can_orbital_mine(b):
        if b["body_class"] not in ORBITAL_CLASSES:
            return False
        diameter = b["radius"] * 2
        return orbital_diameter > 0 and diameter <= orbital_diameter

    def make_row(b):
        orbital = can_orbital_mine(b)
        orbital_cell = (
            '<td class="orbital-ok" title="軌道採掘可能 (直径' + str(b["radius"]*2) + 'km)">⛏</td>'
            if orbital else
            '<td class="orbital-no"></td>'
        )
        cells = ""
        total_weighted = 0
        for mid in range(1, 12):
            m = b["minerals"].get(mid)
            if m:
                amt = int(m["amount"])
                acc = m["accessibility"]
                # アクセシビリティで色分け
                if acc >= 0.8:
                    acc_color = "#2ecc71"
                elif acc >= 0.5:
                    acc_color = "#f39c12"
                else:
                    acc_color = "#e74c3c"
                total_weighted += amt * acc
                cells += (
                    '<td class="min-cell has-mineral">'
                    '<div class="min-amount">' + f'{amt:,}' + '</div>'
                    '<div class="min-acc" style="color:' + acc_color + '">' + str(acc) + '</div>'
                    '</td>'
                )
            else:
                cells += '<td class="min-cell">—</td>'

        return (
            '<tr>'
            '<td class="body-system">' + b["system"] + '</td>'
            '<td class="body-name">' + b["body"] + '</td>'
            + orbital_cell
            + cells +
            '</tr>'
        )

    rows_html = "".join(make_row(b) for b in bodies)

    # ヘッダー行
    header_cells = "".join(
        '<th class="min-header">' + MINERAL_NAMES[mid] + '</th>'
        for mid in range(1, 12)
    )

    css = """
    :root {
      --bg: #0a0e1a; --bg2: #111828; --bg3: #1a2236;
      --accent: #00c8ff; --accent2: #00ff9d;
      --text: #cdd9f0; --text2: #7a93b8;
      --border: #1e3050;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background: var(--bg); color: var(--text); font-family: 'Noto Sans JP', sans-serif; font-size: 13px; padding: 20px; }
    h1 { font-family: 'Share Tech Mono', monospace; font-size: 18px; color: var(--accent); letter-spacing: 2px; margin-bottom: 6px; }
    .meta { font-size: 11px; color: var(--text2); margin-bottom: 16px; }

    .controls { display: flex; gap: 12px; align-items: center; flex-wrap: wrap; margin-bottom: 14px; }
    .controls label { font-size: 12px; color: var(--text2); }
    .controls select, .controls input[type=number] {
      background: var(--bg2); border: 1px solid var(--border); color: var(--text);
      padding: 4px 8px; border-radius: 4px; font-size: 12px;
    }
    .controls input[type=number] { width: 80px; }
    .mine-result { font-size: 12px; color: var(--accent2); }

    .table-wrap { overflow-x: auto; }
    table { border-collapse: collapse; min-width: 100%; }
    th { background: var(--bg3); color: var(--text2); font-size: 11px; letter-spacing: 1px;
         padding: 6px 8px; border: 1px solid var(--border); text-align: center;
         white-space: nowrap; cursor: pointer; user-select: none; }
    th:hover { color: var(--accent); }
    th.sorted-asc::after { content: ' ▲'; color: var(--accent); }
    th.sorted-desc::after { content: ' ▼'; color: var(--accent); }
    td { padding: 5px 8px; border: 1px solid var(--border); vertical-align: top; }
    tr:hover td { background: var(--bg3); }

    .body-system { color: var(--text2); font-size: 11px; white-space: nowrap; }
    .body-name { font-family: 'Share Tech Mono', monospace; color: var(--accent); white-space: nowrap; }
    .min-cell { text-align: right; min-width: 90px; color: var(--text2); }
    .min-cell.has-mineral { color: var(--text); }
    .min-amount { font-size: 12px; }
    .min-acc { font-size: 10px; margin-top: 1px; }

    .orbital-ok { text-align: center; color: #00ff9d; font-size: 14px; }
    .orbital-no { text-align: center; color: var(--text2); }
    .footer { margin-top: 20px; font-size: 11px; color: var(--text2); text-align: right; }
    """

    mineral_names_js = str([MINERAL_NAMES[i] for i in range(1, 12)])

    js = """
    const MINERAL_NAMES = """ + mineral_names_js + """;

    function exportCSV() {
      const mineralCols = MINERAL_NAMES.length;
      // ヘッダー行
      const headers = ['System', 'Body', 'Orbital'];
      for (const m of MINERAL_NAMES) {
        headers.push(m + '_Amount');
        headers.push(m + '_Acc');
      }

      const csvRows = [headers.join(',')];

      // 表示中の行のみ
      Array.from(document.getElementById('tbody').querySelectorAll('tr')).forEach(row => {
        if (row.style.display === 'none') return;
        const cells = row.cells;
        const system = cells[0].textContent.trim();
        const body   = '"' + cells[1].textContent.trim().replace(/"/g, '""') + '"';
        const orbital = cells[2].textContent.trim() === '⛏' ? '1' : '0';
        const cols = [system, body, orbital];
        for (let ci = 3; ci < cells.length; ci++) {
          const amtEl = cells[ci].querySelector('.min-amount');
          const accEl = cells[ci].querySelector('.min-acc');
          if (amtEl) {
            cols.push(amtEl.textContent.replace(/,/g, ''));
            cols.push(accEl ? accEl.getAttribute('data-orig') || accEl.textContent.trim() : '');
          } else {
            cols.push(''); cols.push('');
          }
        }
        csvRows.push(cols.join(','));
      });

      const bom = '﻿';  // Excel用BOM
      const blob = new Blob([bom + csvRows.join('\r\n')], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      const sys = document.getElementById('system-filter').value || 'all';
      a.href = url;
      a.download = 'aurora_minerals_' + sys + '.csv';
      a.click();
      URL.revokeObjectURL(url);
    }

    const tbody = document.getElementById('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    let sortCol = -1, sortDir = 1;

    function sortTable(colIdx) {
      if (sortCol === colIdx) sortDir *= -1;
      else { sortCol = colIdx; sortDir = -1; }

      // ヘッダーの矢印更新
      document.querySelectorAll('th').forEach((th, i) => {
        th.classList.remove('sorted-asc','sorted-desc');
        if (i === colIdx) th.classList.add(sortDir === 1 ? 'sorted-asc' : 'sorted-desc');
      });

      rows.sort((a, b) => {
        const av = getCellVal(a, colIdx);
        const bv = getCellVal(b, colIdx);
        if (av === null && bv === null) return 0;
        if (av === null) return 1;
        if (bv === null) return -1;
        return (av - bv) * sortDir;
      });
      rows.forEach(r => tbody.appendChild(r));
    }

    function getCellVal(row, colIdx) {
      const cell = row.cells[colIdx];
      if (!cell) return null;
      if (colIdx <= 1) return cell.textContent.trim();
      const amtEl = cell.querySelector('.min-amount');
      if (!amtEl) return null;
      const v = parseFloat(amtEl.textContent.replace(/,/g, ''));
      return isNaN(v) ? null : v;
    }

    // ソートヘッダーにイベント追加
    document.querySelectorAll('th').forEach((th, i) => {
      th.addEventListener('click', () => sortTable(i));
    });

    // 元のアクセシビリティ値を保存
    document.querySelectorAll('.min-acc').forEach(el => {
      el.setAttribute('data-orig', el.textContent);
    });

    function filterSystem() {
      const sel = document.getElementById('system-filter').value;
      rows.forEach(row => {
        if (!sel || row.cells[0].textContent.trim() === sel) {
          row.style.display = '';
        } else {
          row.style.display = 'none';
        }
      });
    }

    function resetMining() {
      document.querySelectorAll('.min-acc').forEach(el => {
        el.textContent = el.getAttribute('data-orig');
        const v = parseFloat(el.textContent);
        if (v >= 0.8) el.style.color = '#2ecc71';
        else if (v >= 0.5) el.style.color = '#f39c12';
        else el.style.color = '#e74c3c';
      });
    }

    function calcMining() {
      const mines = parseInt(document.getElementById('mine-count').value) || 0;
      const rate = """ + str(mining_rate) + """;
      resetMining();
      rows.forEach(row => {
        for (let col = 2; col < row.cells.length; col++) {
          const accEl = row.cells[col]?.querySelector('.min-acc');
          if (!accEl) continue;
          const acc = parseFloat(accEl.getAttribute('data-orig'));
          if (isNaN(acc)) continue;
          const annual = Math.round(mines * rate * acc);
          accEl.textContent = annual.toLocaleString() + ' t/yr';
          accEl.style.color = annual > 0 ? '#00c8ff' : '#555';
        }
      });
    }
    """

    mineral_options = "".join(
        '<option value="' + str(mid) + '">' + MINERAL_NAMES[mid] + '</option>'
        for mid in range(1, 12)
    )

    systems = sorted(set(b["system"] for b in bodies))
    system_options = '<option value="">全星系</option>' + "".join(
        '<option value="' + s + '">' + s + '</option>'
        for s in systems
    )

    html = (
        '<!DOCTYPE html><html lang="ja"><head>'
        '<meta charset="UTF-8">'
        '<title>Aurora 4x Mineral Viewer</title>'
        '<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Noto+Sans+JP:wght@400;500&display=swap" rel="stylesheet">'
        '<style>' + css + '</style>'
        '</head><body>'
        '<h1>[ ' + race_name + ' ] MINERAL RESOURCES</h1>'
        '<div class="meta">GAME: ' + game_name + ' &nbsp;|&nbsp; Mining Rate: ' + str(mining_rate) + ' tons &nbsp;|&nbsp; Orbital Mining: ' + (str(orbital_diameter) + ' km diameter' if orbital_diameter else 'none') + ' &nbsp;|&nbsp; GENERATED: ' + generated_at + '</div>'
        '<div class="controls">'
        '<label>星系: <select id="system-filter" onchange="filterSystem()"><'+system_options+'</select></label>'
        '<label>自動鉱山 <input type="number" id="mine-count" value="10" min="1" max="9999"> 台</label>'
        '<button onclick="calcMining()" style="background:#1a3a4a;color:var(--accent);border:1px solid var(--accent);padding:4px 12px;border-radius:4px;cursor:pointer;font-size:12px;">全資源計算</button>'
        '<button onclick="resetMining()" style="background:#1a1a1a;color:var(--text2);border:1px solid var(--border);padding:4px 12px;border-radius:4px;cursor:pointer;font-size:12px;">リセット</button>'
        '<button onclick="exportCSV()" style="background:#1a2a1a;color:#00ff9d;border:1px solid #00ff9d;padding:4px 12px;border-radius:4px;cursor:pointer;font-size:12px;">CSV出力</button>'
        '<span class="mine-result">採掘レート: ' + str(mining_rate) + ' tons / 年</span>'
        '</div>'
        '<div class="table-wrap">'
        '<table>'
        '<thead><tr>'
        '<th>星系</th><th>天体名</th><th title="軌道採掘">⛏</th>'
        + header_cells +
        '</tr></thead>'
        '<tbody id="tbody">' + rows_html + '</tbody>'
        '</table></div>'
        '<div class="footer">Aurora 4x Mineral Viewer &mdash; ' + generated_at + '</div>'
        '<script>' + js + '</script>'
        '</body></html>'
    )
    return html

def main():
    db_path = get_db_path()
    print("DB: " + db_path)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    game = get_latest_game(conn)
    race = get_player_race(conn, game["GameID"])
    print("ゲーム: " + game["GameName"] + " / 帝国: " + race["RaceName"])

    mining_rate = get_mining_rate(conn, game["GameID"], race["RaceID"])
    print("採掘レート: " + str(mining_rate) + " tons/年")
    orbital_diameter = get_orbital_mining_diameter(conn, game["GameID"], race["RaceID"])
    print("軌道採掘最大直径: " + str(orbital_diameter) + " km")

    bodies = get_mineral_data(conn, game["GameID"], race["RaceID"])
    print("調査済み天体: " + str(len(bodies)) + " 件")
    conn.close()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(base_dir, "aurora_minerals.html")

    html = build_html(game, race, bodies, mining_rate, orbital_diameter)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    print("\n[OK] 出力: " + out_path)
    print("完了！ブラウザで aurora_minerals.html を開いてください。")

if __name__ == "__main__":
    main()

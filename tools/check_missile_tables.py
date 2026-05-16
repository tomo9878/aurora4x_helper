import sqlite3

DB = "AuroraDB.db"
conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# ミサイル関連テーブル一覧
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND (name LIKE '%Missile%' OR name LIKE '%Warhead%' OR name LIKE '%Ordnance%') ORDER BY name")
print("Missile-related tables:")
for r in cur.fetchall():
    print(f"  {r['name']}")

print()

# DIM_MissileEngine があれば内容確認
for tname in ['DIM_MissileEngineType', 'DIM_MissileEngine', 'FCT_MissileDesign', 'DIM_Warhead', 'DIM_MissileFuelType']:
    try:
        cur.execute(f"SELECT * FROM {tname} LIMIT 5")
        cols = [d[0] for d in cur.description]
        rows = cur.fetchall()
        print(f"=== {tname} (columns: {cols}) ===")
        for r in rows:
            print(f"  {dict(r)}")
    except Exception as e:
        print(f"  {tname}: {e}")
    print()

conn.close()

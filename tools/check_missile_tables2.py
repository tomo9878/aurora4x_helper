import sqlite3

DB = "AuroraDB.db"
conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# FCT_MissileType の構造確認
cur.execute("PRAGMA table_info(FCT_MissileType)")
cols = cur.fetchall()
print("FCT_MissileType columns:")
for c in cols:
    print(f"  {c['cid']:2d} {c['name']:35s} {c['type']}")

print()

# 実データ1件確認
cur.execute("SELECT * FROM FCT_MissileType LIMIT 2")
rows = cur.fetchall()
for r in rows:
    print("Sample FCT_MissileType row:")
    for k in r.keys():
        print(f"  {k:35s} = {r[k]}")
    print()

# DIM系テーブル全部確認
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'DIM_%' ORDER BY name")
dim_tables = [r['name'] for r in cur.fetchall()]
print("All DIM_ tables:", dim_tables[:30])

# Tech tables for missile engine
print()
for kw in ['Engine', 'Fuel', 'Warhead', 'Agility', 'ECM', 'Missile']:
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE ?", (f'%{kw}%',))
    found = [r['name'] for r in cur.fetchall()]
    if found:
        print(f"  '{kw}' tables: {found}")

conn.close()

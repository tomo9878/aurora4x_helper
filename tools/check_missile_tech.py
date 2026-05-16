import sqlite3

DB = "AuroraDB.db"
conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

cur.execute("SELECT GameID FROM FCT_Game ORDER BY GameID DESC LIMIT 1")
gid = cur.fetchone()["GameID"]
cur.execute("SELECT RaceID FROM FCT_Race WHERE GameID=? AND NPR=0", (gid,))
rid = cur.fetchone()["RaceID"]

cur.execute("SELECT TechID FROM FCT_RaceTech WHERE RaceID=?", (rid,))
researched = set(r["TechID"] for r in cur.fetchall())

def mark(tid): return "[R]" if tid in researched else "[ ]"

# Engine base type (TechTypeID=40)
print("=== Engine base tech (TechTypeID=40) ===")
cur.execute("SELECT TechSystemID, Name, AdditionalInfo FROM FCT_TechSystem WHERE TechTypeID=40 ORDER BY AdditionalInfo")
for r in cur.fetchall():
    print(f"  {mark(r['TechSystemID'])} {r['Name']:45s} EP/HS={r['AdditionalInfo']}")

print()

# Max Engine Power Modifier (TechTypeID=130)
print("=== Max Engine Power Modifier (TechTypeID=130) ===")
cur.execute("SELECT TechSystemID, Name, AdditionalInfo FROM FCT_TechSystem WHERE TechTypeID=130 ORDER BY AdditionalInfo")
for r in cur.fetchall():
    print(f"  {mark(r['TechSystemID'])} {r['Name']:45s} Max={r['AdditionalInfo']}")

print()

# Fuel Consumption (TechTypeID=65)
print("=== Fuel Consumption (TechTypeID=65) ===")
cur.execute("SELECT TechSystemID, Name, AdditionalInfo FROM FCT_TechSystem WHERE TechTypeID=65 ORDER BY AdditionalInfo")
for r in cur.fetchall():
    print(f"  {mark(r['TechSystemID'])} {r['Name']:55s} L/EPH={r['AdditionalInfo']}")

print()

# Warhead Strength (TechTypeID=12)
print("=== Warhead Strength (TechTypeID=12) ===")
cur.execute("SELECT TechSystemID, Name, AdditionalInfo FROM FCT_TechSystem WHERE TechTypeID=12 ORDER BY CAST(AdditionalInfo AS REAL)")
for r in cur.fetchall():
    print(f"  {mark(r['TechSystemID'])} {r['Name']:45s} x{r['AdditionalInfo']}")

print()

# ATG (TechSystemID 33-42)
print("=== Active Terminal Guidance ===")
cur.execute("SELECT TechSystemID, Name, AdditionalInfo FROM FCT_TechSystem WHERE TechSystemID IN (33,34,35,36,37,38,39,42) ORDER BY AdditionalInfo")
for r in cur.fetchall():
    print(f"  {mark(r['TechSystemID'])} [{r['TechSystemID']}] {r['Name']:45s} bonus={r['AdditionalInfo']}")

print()

# ECCM tech
print("=== Missile ECCM (search by name) ===")
cur.execute("SELECT TechSystemID, Name, AdditionalInfo FROM FCT_TechSystem WHERE Name LIKE '%ECCM%' ORDER BY AdditionalInfo LIMIT 15")
for r in cur.fetchall():
    print(f"  {mark(r['TechSystemID'])} {r['Name']:45s} level={r['AdditionalInfo']}")

conn.close()

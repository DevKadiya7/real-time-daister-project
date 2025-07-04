import sqlite3

conn = sqlite3.connect("../data/disaster.db")
cursor = conn.cursor()

# Insert one row
cursor.execute("""
INSERT INTO disasters (id, disaster_type, location, severity, time, source, url)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", (
    "quake_001", "earthquake", "Gujarat", 6.8, 1720092300, "NDMA", "https://example.com/quake_001"
))

conn.commit()
conn.close()
print("✅ Data inserted")

import sqlite3
import os

# Construct full path to the database file
db_path = os.path.join(os.path.dirname(__file__), "disaster.db")

# Check if DB exists
if not os.path.exists(db_path):
    print("❌ Database not found:", db_path)
else:
    # Connect using correct path
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Fetch and print all disaster events
    cursor.execute("SELECT * FROM disasters")
    rows = cursor.fetchall()

    print("✅ Disasters from NASA in Database:")
    for row in rows:
        print(row)

    conn.close()

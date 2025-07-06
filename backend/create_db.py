# backend/create_db.py
import sqlite3
import os

# Path to the DB (store in /data/)
db_path = os.path.join("data", "disaster.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Table 1: disasters
cursor.execute('''
CREATE TABLE IF NOT EXISTS disasters (
    id TEXT PRIMARY KEY,
    disaster_type TEXT,
    location TEXT,
    severity REAL,
    time INTEGER,
    source TEXT,
    url TEXT
)
''')

# Table 2: help_requests
cursor.execute('''
CREATE TABLE IF NOT EXISTS help_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    location TEXT,
    disaster_type TEXT,
    message TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

# Table 3: users
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
)
''')

conn.commit()
conn.close()
print("✅ All tables created successfully in disaster.db")

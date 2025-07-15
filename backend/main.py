from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import sqlite3
import os
import nasa_fetch_and_store

app = FastAPI()
DB_PATH = os.path.join(os.path.dirname(__file__), "../data/disaster.db")

class Disaster(BaseModel):
    id: str
    disaster_type: str
    location: str
    severity: float
    time: int
    source: str
    url: str

@app.post("/api/disasters")
def add_disaster(disaster: Disaster):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO disasters (id, disaster_type, location, severity, time, source, url)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            disaster.id,
            disaster.disaster_type,
            disaster.location,
            disaster.severity,
            disaster.time,
            disaster.source,
            disaster.url
        ))
        conn.commit()
        return {"message": "✅ Disaster added successfully!"}
    except sqlite3.IntegrityError:
        return {"error": f"Disaster with id '{disaster.id}' already exists."}
    finally:
        conn.close()

@app.get("/api/disasters")
def get_disasters():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM disasters")
        rows = cursor.fetchall()
        data = [dict(row) for row in rows]
        return JSONResponse(content=data)
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()
@app.post("/api/fetch-nasa")
def fetch_nasa_data():
    events = nasa_fetch_and_store.fetch_nasa_events()
    nasa_fetch_and_store.store_events(events)
    return {}  # returns nothing (silent response)


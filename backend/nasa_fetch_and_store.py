import requests
import sqlite3
import os
import time

# Set path to DB
DB_PATH = os.path.join(os.path.dirname(__file__), "../data/disaster.db")
NASA_API = "https://eonet.gsfc.nasa.gov/api/v3/events"

# Define India's lat/lon bounding box
INDIA_BOUNDS = {
    "min_lat": 6.5,
    "max_lat": 37.0,
    "min_lon": 68.0,
    "max_lon": 97.5
}

def is_within_india(lat, lon):
    return (INDIA_BOUNDS["min_lat"] <= lat <= INDIA_BOUNDS["max_lat"]) and \
           (INDIA_BOUNDS["min_lon"] <= lon <= INDIA_BOUNDS["max_lon"])

def fetch_nasa_events():
    try:
        response = requests.get(NASA_API, timeout=10)
        response.raise_for_status()
        return response.json().get("events", [])
    except Exception as e:
        print(f"❌ Error fetching data from NASA API: {e}")
        return []

def store_events(events):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    inserted_count = 0

    for event in events:
        try:
            # Get first geometry point
            geometry = event.get("geometry", [])
            if not geometry:
                continue

            coordinates = geometry[0].get("coordinates", [])
            if not isinstance(coordinates, list) or len(coordinates) < 2:
                continue

            lon, lat = coordinates[0], coordinates[1]

            # 🌍 Filter only events within India
            if not is_within_india(lat, lon):
                continue

            # Extract rest of the fields
            event_id = event.get("id", "")
            disaster_type = event["categories"][0]["title"] if event.get("categories") else "Unknown"
            location_str = f"{lat}, {lon}"
            severity = 1.0
            timestamp = int(time.time())
            source = "NASA EONET"
            url = event["sources"][0]["url"] if event.get("sources") else ""

            cursor.execute("""
                INSERT OR IGNORE INTO disasters (id, disaster_type, location, severity, time, source, url)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                event_id,
                disaster_type,
                location_str,
                severity,
                timestamp,
                source,
                url
            ))
            inserted_count += 1

        except Exception as e:
            print(f"⚠️ Error with event {event.get('id')}: {e}")

    conn.commit()
    conn.close()
    print(f"✅ Stored {inserted_count} events in India")

if __name__ == "__main__":
    events = fetch_nasa_events()
    store_events(events)

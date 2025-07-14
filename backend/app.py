
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
<<<<<<< HEAD
from functools import lru_cache
import nasa_fetch_and_store 

import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env
api_key = os.getenv("NEWS_API_KEY")
=======
import httpx
>>>>>>> 8a54c83dcab2d877b3f9a1e701a9a87c7ba9f808

app = FastAPI()

# Allow frontend (Streamlit or browser) to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific domain(s) in production
    allow_methods=["*"],
    allow_headers=["*"],
)
<<<<<<< HEAD
=======

# 👋 Root route
>>>>>>> 8a54c83dcab2d877b3f9a1e701a9a87c7ba9f808
@app.get("/")
async def root():
    return {"message": "Welcome to the Disaster News API. Use /api/disasters to get data."}

# 🌊 NewsAPI disaster news route
@app.get("/api/disasters")
async def get_disasters():
    try:
<<<<<<< HEAD
        # Replace with your own NewsAPI key

=======
        api_key = "69f48923e7254c158bda56b10f06b460"  # Replace with env var in production
>>>>>>> 8a54c83dcab2d877b3f9a1e701a9a87c7ba9f808
        url = f"https://newsapi.org/v2/everything?q=tsunami&sortBy=publishedAt&apiKey={api_key}"

        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url)
        response.raise_for_status()

        articles = response.json().get("articles", [])

        news_data = [
            {
                "title": a.get("title"),
                "description": a.get("description"),
                "url": a.get("url"),
                "image": a.get("urlToImage", "https://via.placeholder.com/150"),
            }
            for a in articles
        ]

        return JSONResponse(content=news_data)

    except Exception as e:
        print("❌ NewsAPI Error:", e)
        return JSONResponse(status_code=500, content={"error": str(e)})

# 🌍 EONET NASA Disaster API
@app.get("/api/nasa")
async def get_nasa_disasters():
    try:
        nasa_url = "https://eonet.gsfc.nasa.gov/api/v3/events?status=open"

        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(nasa_url)
        response.raise_for_status()

        events = response.json().get("events", [])

        data = [
            {
                "id": event["id"],
                "title": event["title"],
                "category": event["categories"][0]["title"] if event["categories"] else "Unknown",
                "date": event["geometry"][-1]["date"] if event["geometry"] else "N/A",
                "coordinates": event["geometry"][-1]["coordinates"] if event["geometry"] else [],
            }
            for event in events
        ]

        return JSONResponse(content=data)

    except Exception as e:
<<<<<<< HEAD
        return {"error": str(e)}
    
@app.get("/api/nasa-events")
async def get_nasa_events():
    data = cached_nasa_events()
    if isinstance(data, dict) and "error" in data:
        return JSONResponse(status_code=500, content=data)
    return JSONResponse(content=data)
@app.post("/api/fetch-nasa")
def fetch_nasa_data():
    events = nasa_fetch_and_store.fetch_nasa_events()
    nasa_fetch_and_store.store_events(events)
    return {}  # returns nothing (silent response)
=======
        print("❌ NASA API Error:", e)
        return JSONResponse(status_code=500, content={"error": str(e)})
>>>>>>> 8a54c83dcab2d877b3f9a1e701a9a87c7ba9f808

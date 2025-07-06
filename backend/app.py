from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from functools import lru_cache
import requests

app = FastAPI()

# Allow frontend (Streamlit or browser) to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific domain in production
    allow_methods=["*"],
    allow_headers=["*"],
)
#kanzariya
# 👋 Root route
@app.get("/")
async def root():
    return {"message": "Welcome to the Disaster News API. Use /api/disasters to get data."}

# 🌊 Tsunami or disaster news API route
@app.get("/api/disasters")
async def get_disasters():
    try:
        # Replace with your own NewsAPI key
        api_key = "69f48923e7254c158bda56b10f06b460"
        url = f"https://newsapi.org/v2/everything?q=tsunami&sortBy=publishedAt&apiKey={api_key}"

        response = requests.get(url, timeout=5)
        response.raise_for_status()
        articles = response.json().get("articles", [])

        news_data = [{
            "title": a.get("title"),
            "description": a.get("description"),
            "url": a.get("url"),
            "image": a.get("urlToImage", "https://via.placeholder.com/150")
        } for a in articles]

        return JSONResponse(content=news_data)

    except Exception as e:
        print("❌ ERROR:", e)
        return JSONResponse(status_code=500, content={"error": str(e)})
@lru_cache(maxsize=1)
def cached_nasa_events():
    try:
        url = "https://eonet.gsfc.nasa.gov/api/v3/events"
        response = requests.get(url, timeout=(3, 5))
        response.raise_for_status()
        events = response.json().get("events", [])[:10]
        return [{
            "title": e["title"],
            "category": e["categories"][0]["title"] if e.get("categories") else "N/A",
            "link": e["sources"][0]["url"] if e.get("sources") else None
        } for e in events]
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/api/nasa-events")
async def get_nasa_events():
    data = cached_nasa_events()
    if isinstance(data, dict) and "error" in data:
        return JSONResponse(status_code=500, content=data)
    return JSONResponse(content=data)
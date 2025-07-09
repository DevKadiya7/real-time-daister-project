from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx
import requests

app = FastAPI()

# Allow frontend (Streamlit or browser) to access API


app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],  # You can restrict this later
    allow_credentials=True,
    allow_origins=["*"],  # Replace with specific domain(s) in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# 👋 Root route
@app.get("/")
async def root():
    return {"message": "Welcome to the Disaster News API. Use /api/disasters to get data."}

# 🌊 NewsAPI disaster news route
@app.get("/api/disasters")
async def get_disasters():
    try:
        api_key = "69f48923e7254c158bda56b10f06b460"  # Replace with env var in production
        url = f"https://newsapi.org/v2/everything?q=tsunami&sortBy=publishedAt&apiKey={api_key}"

 
        response = requests.get(api_key, timeout=10)  # or even 30 if needed


        async with httpx.AsyncClient(timeout=15.0) as client:
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
        print("❌ NASA API Error:", e)
        return JSONResponse(status_code=500, content={"error": str(e)})

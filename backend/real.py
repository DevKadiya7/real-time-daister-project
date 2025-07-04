from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import pandas as pd

app = FastAPI()


# Allow frontend access (e.g., Streamlit, React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Load CSV data
df = pd.read_csv("../data/disaster_reports.csv")

@app.get('/')
def home():
    return {"message": "Welcome to the Disaster Reports API"}

@app.get('/api/reports')
def get_reports(
    state: Optional[str] = None,
    year: Optional[int] = None,
    report_type: Optional[str] = None
):
    filtered = df.copy()

    if state:
        filtered = filtered[filtered["State Name"].str.lower() == state.lower()]
    if year:
        filtered = filtered[filtered["Year"] == year]
    if report_type:
        filtered = filtered[filtered["Report Type"].str.lower() == report_type.lower()]

    return filtered.to_dict(orient="records")

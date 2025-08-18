# real-time-disaster-project
own project
# 🌍 Real-Time Disaster Information Dashboard

A web-based platform to aggregate and display real-time global disaster events using data from NASA EONET, weather APIs, and local authorities. Inspired by SACHET (NDMA), this project aims to enhance disaster awareness and support early warning systems for citizens, researchers, and authorities.

## 🚀 Features

- 🔥 Live disaster event tracking from NASA EONET
- 🌩️ Real-time weather alerts using external APIs (e.g., OpenWeatherMap)
- 📍 Interactive map with disaster markers
- 📰 Live news and alerts feed for natural disasters
- 📊 Streamlit-based interactive dashboard
- ⚡ FastAPI-powered backend API services

- ## 🛠️ Tech Stack

| Category         | Technologies |
|------------------|--------------|
| Frontend         | `Streamlit`, `Folium`, `HTML/CSS` |
| Backend          | `FastAPI`, `Python`, `httpx`, `SQLite` |
| APIs Used        | NASA EONET, NDMA, OpenWeatherMap |
| Visualization    | `Pandas`, `Plotly`, `Folium`, `Streamlit-Folium` |


## 🚀 Getting Started

### 🔧 Prerequisites

- Python 3.8+
- `pip`, `virtualenv` (recommended)
- Access to the following APIs:
  - [NASA EONET](https://eonet.gsfc.nasa.gov/)
  - [OpenWeatherMap](https://openweathermap.org/api)

### 📦 Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/real-time-disaster-dashboard.git
cd real-time-disaster-dashboard

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the backend (FastAPI)
cd backend
uvicorn main:app --reload

# 5. Run the frontend (Streamlit)
cd ../frontend
streamlit run app.py
💡 Environment variables like API keys can be placed in a .env file.

🤝 Contribution Guidelines
We welcome contributions of all kinds: code, design, documentation, bug reports, suggestions, etc.

🧭 How to Contribute
Fork this repository

Create a new branch: git checkout -b feature/your-feature

Commit your changes: git commit -m "Added something"

Push to your fork: git push origin feature/your-feature

Create a Pull Request


✨ Acknowledgements
NASA EONET API

OpenWeatherMap

NDMA

Streamlit

FastAPI

📢 Call for Contributions!
This project is open for submission under programs like GSoC, and hackathons. If you’re interested in contributing or collaborating, feel free to:

🐛 Open an issue

---

📧 Email:  kadiyadev07@gmail.com

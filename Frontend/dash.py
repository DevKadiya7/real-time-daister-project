import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="🌍 Real-Time Disaster Info", layout="wide")

st.markdown("""
    <style>
    #MainMenu, header, footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

page = st.radio("Navigation", ["🏠 Dashboard", "🗺️ Map", "📰 News", "📩 Help Request"],
                horizontal=True, label_visibility="collapsed")

API_URL = "http://localhost:8000/api/reports"

def fetch_reports(state=None, year=None, report_type=None):
    params = {}
    if state: params["state"] = state
    if year: params["year"] = year
    if report_type: params["report_type"] = report_type
    try:
        res = requests.get(API_URL, params=params)
        return res.json()
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return []

def display_news():
    data = fetch_reports()
    for item in data[:10]:  # limit to first 10
        with st.container():
            cols = st.columns([1, 3])
            cols[0].image(item.get("image", "https://via.placeholder.com/150"), width=150)
            with cols[1]:
                st.subheader(item.get("title", "No Title"))
                st.write(item.get("description", "No description available."))
                st.markdown(f"[🔗 Read more]({item.get('url', '#')})", unsafe_allow_html=True)
        st.markdown("---")

def display_map(data):
    if not data:
        st.warning("No data to display on the map.")
        return

    m = folium.Map(location=[20.5937, 78.9629], zoom_start=4)
    for item in data:
        lat = item.get("latitude")
        lon = item.get("longitude")
        if pd.notna(lat) and pd.notna(lon):
            popup = f"{item.get('title')}<br>{item.get('description')}"
            folium.Marker(location=[lat, lon], popup=popup).add_to(m)
    st_folium(m, width=700, height=450)

def main():
    if page == "🏠 Dashboard":
        st.header("📊 Disaster Report Dashboard")
        st.info("Use the Map and News tabs to view detailed info.")

    elif page == "🗺️ Map":
        st.sidebar.header("Filter Reports")
        state = st.sidebar.text_input("State")
        year = st.sidebar.number_input("Year", min_value=2000, max_value=2100, step=1)
        report_type = st.sidebar.selectbox("Report Type", ["", "Flood", "Fire", "Earthquake", "Other"])
        data = fetch_reports(state, year if year else None, report_type if report_type else None)
        st.subheader("🗺️ Disaster Map")
        display_map(data)

    elif page == "📰 News":
        st.header("📰 Latest Disaster News")
        display_news()

    elif page == "📩 Help Request":
        st.header("📩 Request Assistance")
        name = st.text_input("Name")
        location = st.text_input("Location")
        need = st.text_area("Your Need")
        if st.button("Submit"):
            st.success("✅ Your request has been recorded!")

if __name__ == "__main__":
    main()

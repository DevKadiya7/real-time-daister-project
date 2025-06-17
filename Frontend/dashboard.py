# frontend/dashboard.py
import streamlit as st
import requests

st.title("🌍 Real-Time Disaster Info Dashboard")

response = requests.get("http://localhost:5000/api/disasters")
data = response.json()

for item in data:
    st.subheader(item['title'])
    st.write(item['description'])
    st.markdown(f"[Read more]({item['url']})")

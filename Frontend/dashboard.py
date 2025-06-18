import streamlit as st
import requests

st.set_page_config(page_title="🌍 Real-Time Disaster Info", layout="wide")

st.markdown("## 🌍 Real-Time Disaster Information Dashboard")
st.markdown("Live updates from NewsAPI based on keywords like **disaster, earthquake, flood**")

# Call Flask backend
response = requests.get("http://localhost:5000/api/disasters")

if response.status_code == 200:
    data = response.json()

    # Loop through disaster items
    for item in data:
        with st.container():
            cols = st.columns([1, 3])
            # 🖼️ Image (if exists)
            if item.get("image"):
                cols[0].image(item["image"], width=150)
            else:
                cols[0].image("https://via.placeholder.com/150", caption="No Image", width=150)

            # 📝 Info
            with cols[1]:
                st.subheader(item["title"])
                st.write(item["description"] or "No description available.")
                with st.expander("🔍 Read More"):
                    st.write(item.get("content") or "Full content not available.")
                    st.markdown(f"🔗 [Original Source]({item['url']})", unsafe_allow_html=True)

            st.markdown("---")

else:
    st.error("❌ Failed to fetch data from backend. Please check Flask server.")


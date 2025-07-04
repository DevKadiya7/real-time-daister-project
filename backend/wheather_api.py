import requests
import pandas as pd
import streamlit as st
import altair as alt

st.title("🌤️ Real-Time Weather Forecast")

# Get city from user
city = st.text_input("Enter city", "Ahmedabad")

api_key = "your_verified_api_key_here"

if st.button("Get Live Forecast"):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        # Extract forecast
        forecast = pd.DataFrame([{
            'datetime': item['dt_txt'],
            'temperature': item['main']['temp'],
            'humidity': item['main']['humidity'],
        } for item in data['list']])

        # Convert datetime
        forecast['datetime'] = pd.to_datetime(forecast['datetime'])

        # Line chart for temperature
        line_chart = alt.Chart(forecast).mark_line(color="orange").encode(
            x='datetime:T',
            y='temperature:Q',
            tooltip=['datetime', 'temperature']
        ).properties(
            title=f"Temperature Forecast - {city}"
        )

        st.altair_chart(line_chart, use_container_width=True)
    else:
        st.error("API call failed: " + str(response.status_code))

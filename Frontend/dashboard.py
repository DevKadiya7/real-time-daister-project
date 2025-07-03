import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium
@st.cache_data(ttl=300)
def fetch_disaster_data():
    try:
        response = requests.get("http://localhost:5000/api/disasters", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"⚠️ API Error: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"❌ Could not fetch news: {e}")
        return []


st.set_page_config(page_title="🌍 Real-Time Disaster Info", layout="wide")
st.title("🌍 REAL-TIME-DISASTER-DASHBOARD")

#himanshi
# Global hide header/footer/menu
st.markdown("""
    <style>
    #MainMenu, header, footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Define tab navigation (using radio so we can detect page state)
page = st.radio("Navigation", ["🏠 Dashboard", "🗺️ Map", "📰 News", "📩 Help Request"],
                horizontal=True, label_visibility="collapsed")

# Hide sidebar if not on Map tab
if page != "🗺️ Map":
    st.markdown("""
        <style>
        section[data-testid="stSidebar"] {display: none !important;}
        [data-testid="collapsedControl"] {display: none !important;}
        </style>
    """, unsafe_allow_html=True)

# API display function
def display_API():
    data = fetch_disaster_data()
    if data:
        for item in data:
            with st.container():
                cols = st.columns([1, 3])
                cols[0].image(item.get("image") or "https://via.placeholder.com/150", width=150)
                with cols[1]:
                    st.subheader(item.get("title", "No Title"))
                    st.write(item.get("description", "No description available."))
                    st.markdown(f"[🔗 Read more]({item['url']})", unsafe_allow_html=True)
                st.markdown("---")
    else:
        st.error("❌ Failed to fetch data from backend.")

                  
# Map and metrics functions
APP_TITLE = 'Fraud and Identity Theft Report'
APP_SUB_TITLE = 'Source: Federal Trade Commission'

def display_fraud_facts(df, year, quarter, state_name, report_type, field_name, title, number_format='${:,}', is_meadian=False):
    df = df[(df['Year'] == year) & (df['Quarter'] == quarter) & (df['Report Type'] == report_type)]
    if state_name:
        df = df[df['State Name'] == state_name]
    df.drop_duplicates(inplace=True)
    total = df[field_name].sum()/len(df) if is_meadian and len(df) else df[field_name].sum()
    st.metric(title, number_format.format(round(total)))

def display_map(df, year, quarter):
    #update
    st.title(APP_TITLE)
    st.caption(APP_SUB_TITLE)
    df = df[(df['Year'] == year) & (df['Quarter'] == quarter)]
    my_map = folium.Map(location=[38, -96.5], zoom_start=4, scrollWheelZoom=False, tiles='CartoDB positron')
    choropleth = folium.Choropleth(
        geo_data='../data/us-state-boundaries.geojson',
        data=df,
        columns=('State Name', 'State Total Reports Quarter'),
        key_on='feature.properties.name',
        line_opacity=0.8,
        highlight=True
    )
    choropleth.geojson.add_to(my_map)
    df = df.set_index('State Name')

    for feature in choropleth.geojson.data['features']:
        state_name = feature['properties']['name']

        if state_name in df.index:
            state_pop = df.loc[state_name, 'State Pop']
            reports_per_100k = df.loc[state_name, 'Reports per 100K-F&O together']

            if isinstance(state_pop, pd.Series):
                state_pop = state_pop.iloc[0]
            if isinstance(reports_per_100k, pd.Series):
                reports_per_100k = reports_per_100k.iloc[0]

            population_str = f"Population: {state_pop:,}"
            per_100k_str = f"Reports/100K: {round(reports_per_100k):,}"
        else:
            population_str = "Population: N/A"
            per_100k_str = "Reports/100K: N/A"

        feature['properties']['population'] = population_str
        feature['properties']['per_100k'] = per_100k_str

    choropleth.geojson.add_child(folium.features.GeoJsonTooltip(['name', 'population', 'per_100k'], labels=False))
    st_map = st_folium(my_map, width=700, height=450)
    if 'last_active_drawing' in st_map and st_map['last_active_drawing']:
        return st_map['last_active_drawing']['properties']['name']
    return ""

# Main logic
def main():
    # Load data
    df_continental = pd.read_csv('../data/AxS-Continental_Full Data_data.csv')
    df_fraud = pd.read_csv('../data/AxS-Fraud Box_Full Data_data.csv')
    df_mead = pd.read_csv('../data/AxS-Median Box_Full Data_data.csv')
    df_loss = pd.read_csv('../data/AxS-Losses Box_Full Data_data.csv')

    if page == "🏠 Dashboard":
        st.header("🏠 Dashboard")
        st.write("This is the main dashboard with data overview.")

    elif page == "🗺️ Map":
        with st.container():
            st.header("🗺️ Real-Time Map")

        # Sidebar controls (only shown now)
        with st.sidebar:
            year_list = sorted(df_continental['Year'].unique())
            year = st.selectbox("Year", year_list, index=len(year_list)-1)
            quarter = st.radio("Quarter", [1, 2, 3, 4])
            state_list = [''] + sorted(df_continental['State Name'].unique())
            state_name = st.selectbox("State", state_list)
            report_type = st.radio("Report Type", ["Fraud", "Other"])

        st.subheader(f"{year} Q{quarter}")
        clicked_state = display_map(df_continental, year, quarter)
        final_state = clicked_state or state_name

        st.subheader(f'{final_state} {report_type} Facts')
        col1, col2, col3 = st.columns(3)
        with col1:
            display_fraud_facts(df_fraud, year, quarter, final_state, report_type, "State Fraud/Other Count", f'{report_type} Reports', number_format='{:,}')
        with col2:
            display_fraud_facts(df_mead, year, quarter, final_state, report_type, "Overall Median Losses Qtr", "Median Loss", is_meadian=True)
        with col3:
            display_fraud_facts(df_loss, year, quarter, final_state, report_type, "Total Losses", "Total Loss")

    elif page == "📰 News":
        placeholder = st.empty()
        with placeholder.container():
            st.header("📰 Disaster News")
        display_API()

    elif page == "📩 Help Request":
        st.header("📩 Help Request Form")
        name = st.text_input("Your Name")
        location = st.text_input("Your Location")
        need = st.text_area("What do you need?")
        if st.button("Submit Request"):
            st.success("✅ Your help request has been submitted!")

    st.markdown("<hr><p style='text-align:center;'>© 2025 Real-Time Disaster Dashboard | Developed by Himanshi Kanzariya</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()

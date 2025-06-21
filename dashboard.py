import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="🌍 Real-Time Disaster Info", layout="wide")

st.markdown("## 🌍 Real-Time Disaster Information Dashboard")
st.markdown("Live updates from NewsAPI based on keywords like disaster, earthquake, flood")

def display_API():
    # Call Flask backend
    response = requests.get("http://localhost:5000/api/disasters")

    if response.status_code == 200:
        data = response.json()

        # Loop through disaster items
        for item in data:
            with st.container():
                cols = st.columns([1, 3])
                # Image (if exists)
                if item.get("image"):
                    cols[0].image(item["image"], width=150)
                else:
                    cols[0].image("https://via.placeholder.com/150", caption="No Image", width=150)

                #  Info
                with cols[1]:
                    st.subheader(item["title"])
                    st.write(item["description"] or "No description available.")
                    st.markdown(f"[🔗 Read more]({item['url']})", unsafe_allow_html=True)

                st.markdown("---")

    else:
        st.error("❌ Failed to fetch data from backend. Please check Flask server.")


APP_TITLE = 'Fraud and Identity Theft Report'
APP_SUB_TITLE = 'Source: Federal Trade Commission'

def display_fraud_facts(df,year,quarter ,state_name,report_type, field_name, title, number_format='${:,}',is_meadian=False):
    
    df= df[(df['Year']== year)& (df['Quarter']==quarter)& (df['Report Type']==report_type)] 
    if state_name:
        df=df[df['State Name']==state_name]
    df.drop_duplicates(inplace=True)
    if is_meadian:
        total =df[field_name].sum()/len(df) if len(df) else 0
    else:
        total=df[field_name].sum() 
    st.metric(title, number_format.format(round(total)))

def display_map(df, year, quarter):
    # st.title(APP_TITLE)
    # st.caption(APP_SUB_TITLE)

    df= df[(df['Year']== year)& (df['Quarter']==quarter)] 

    my_map = folium.Map(location=[38, -96.5], zoom_start=4,scrollWheelZoom=False ,tiles='CartoDB positron')

    choropleth=folium.Choropleth(
        geo_data='../data/us-state-boundaries.geojson',
        data=df,
        columns=('State Name' ,'State Total Reports Quarter'),
        key_on='feature.properties.name',

        line_opacity=0.8,
        highlight=True
    )

    choropleth.geojson.add_to(my_map)



    df=df.set_index('State Name')
   

    for feature in choropleth.geojson.data['features']:
        state_name=feature['properties']['name']
        feature['properties']['population']='population: ' + str('{:,}'.format(df.loc[state_name ,'State Pop'][0]) if state_name in list(df.index) else 'N\A')
        feature['properties']['per_100k']='Reports/100K Population:'+str('{:,}'.format(round(df.loc[state_name ,'Reports per 100K-F&O together'][0])) if state_name in list(df.index) else 'N\A')
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['name', 'population','per_100k'], labs=False)
    )

    st_map = st_folium(my_map, width=700, height=450)
    state_name=''
    if st_map['last_active_drawing']:
        state_name =st.write(st_map['last_active_drawing']['properties']['name'])
    
    return state_name

def display_time_filters(df):

    year_list = list(df['Year'].unique())
    year_list.sort()
    year=st.sidebar.selectbox('Year', year_list,len(year_list)-1)
    quarter = st.sidebar.radio('Quarter',[1, 2, 3, 4])
    st.header(f'{year} Q{quarter}')
    return year, quarter

def display_state_filter(df, state_name):
    state_list=[''] + list(df['State Name'].unique())
    state_list.sort()
    state_index = state_list.index(state_name) if state_name and state_name in state_list else 0
    return st.sidebar.selectbox('State', state_list, state_index)

def display_report_type():
    report_types=['Fraud', 'Other']
    return st.sidebar.radio('Report Type', report_types)

def main():
    #Load data
    df_continental = pd.read_csv('../data/AxS-Continental_Full Data_data.csv')
    df_fraud       = pd.read_csv('../data/AxS-Fraud Box_Full Data_data.csv')
    df_mead        = pd.read_csv('../data/AxS-Median Box_Full Data_data.csv')
    df_loss        = pd.read_csv('../data/AxS-Losses Box_Full Data_data.csv')

    
    #display filters and map
    display_API()
    year , quarter =display_time_filters(df_continental)
    state_name = display_map( df_continental, year, quarter)
    state_name= display_state_filter(df_continental, state_name)
    report_type =display_report_type()
    

    #display matrics
    st.subheader(f' {state_name} {report_type} Facts ')
    col1, col2, col3= st.columns(3)
    with col1:
        display_fraud_facts(df_fraud,year,quarter ,state_name,report_type, "State Fraud/Other Count", f'#{report_type} of Report',number_format='{:,}')
    with col2: 
        display_fraud_facts(df_mead,year,quarter ,state_name,report_type, 'Overall Median Losses Qtr' , 'Meadian & Loss',is_meadian=True)
    with col3:
        display_fraud_facts(df_loss,year,quarter ,state_name,report_type, 'Total Losses' , 'Total & Loss')

if __name__ == "__main__":
    main()
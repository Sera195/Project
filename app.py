import requests
import streamlit as st
import pydeck as pdk
import pandas as pd
import folium
from streamlit_folium import st_folium

m = folium.Map(location=[39.949610, -75.150282], zoom_start=16)
st_data = st_folium(m, width=725)

data = pd.DataFrame({
    'lat': [37.76, 34.05],
    'lon': [-122.4, -118.25]
})
st.map(data)
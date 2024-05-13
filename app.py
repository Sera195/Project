import requests
import streamlit as st
import pydeck as pdk
import pandas as pd

data = pd.DataFrame({
    'lat': [37.76, 34.05],
    'lon': [-122.4, -118.25]
})
st.map(data)
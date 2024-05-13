import requests
import streamlit as st
import pydeck as pdk


st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=37.76,
        longitude=-122.4,
        zoom=11,
        pitch=50,
    ),
    layers=[layer],
    api_keys={'mapbox': 'your_mapbox_api_key', 'google_maps': 'auth_key'},
))
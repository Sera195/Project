pip install gmaps

import requests
import streamlit as st
import gmaps

st.write("HELLO, im asdlfkj")

headers = {
    "authorization": st.secrets["auth_key"],
    "content-type": "application/json"
}

def get_coordinates(place):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={place}&key={'auth_key'}"
    response = requests.get(url)
    #überprüfen ob code == 200 (Verbindung OK)
    if response.status_code == 200:
        data = response.json()
        if "results" in data and len(data["results"]) > 0:
            location = data["results"][0]["geometry"]["location"]
            return location["lat"], location["lng"]
    return None, None


st.display(print(data))
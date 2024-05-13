import streamlit as st
import googlemaps
import pydeck as pdk
import pandas as pd

# Funktion zum Abrufen der Verkehrsdaten von Google Maps API
def get_traffic_data(api_key):
    # Initialisiere Google Maps Client
    gmaps = googlemaps.Client(key=api_key)

    # Beispielabfrage für Verkehrsdaten (hier kannst du deine eigene Abfrage definieren)
    traffic_data = gmaps.places_nearby(location=(40.7128, -74.0060), radius=1000, type='bus_station')

    # Verarbeite die Daten und extrahiere relevante Informationen
    processed_data = []
    for place in traffic_data['results']:
        processed_data.append({
            'lat': place['geometry']['location']['lat'],
            'lon': place['geometry']['location']['lng'],
            'name': place['name']
        })

    return pd.DataFrame(processed_data)

# Hauptfunktion für die Streamlit-App
def main():
    # Setze den Titel der Streamlit-App
    st.title("Öffentlicher Verkehr Visualisierung")

    # Lese den API-Schlüssel aus Streamlit
    api_key = st.secrets["auth_key"]

    # Wenn ein API-Schlüssel vorhanden ist, rufe die Verkehrsdaten ab und visualisiere sie
    if api_key:
        # Rufe die Verkehrsdaten ab
        traffic_data = get_traffic_data(api_key)
        
        # Erstelle eine Pydeck-Karte
        map_layer = pdk.Layer(
            'ScatterplotLayer',
            data=traffic_data,
            get_position='[lon, lat]',
            get_radius=100,
            get_fill_color=[255, 0, 0],
            pickable=True,
            auto_highlight=True)

        view_state = pdk.ViewState(
            latitude=40.7128,
            longitude=-74.0060,
            zoom=11,
            bearing=0,
            pitch=45)

        # Render die Pydeck-Karte in Streamlit
        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=view_state,
            layers=[map_layer],
            tooltip={"text": "Public Transport Station"}))
    else:
        st.warning("Bitte geben Sie Ihren Google Maps API-Schlüssel ein.")

# Starte die Streamlit-App
if __name__ == "__main__":
    main()
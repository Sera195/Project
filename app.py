import streamlit as st
import googlemaps
import pydeck as pdk
import pandas as pd

# Funktion zum Abrufen der Zugroute von Google Maps API
def get_train_route(api_key, start_location, end_location):
    # Initialisiere Google Maps Client
    gmaps = googlemaps.Client(key=api_key)

    # Abfrage für die Zugroute
    train_route = gmaps.directions(start_location, end_location, mode="transit", transit_mode="rail")

    # Verarbeite die Daten und extrahiere relevante Informationen
    processed_data = []
    for step in train_route[0]['legs'][0]['steps']:
        if step['travel_mode'] == 'TRANSIT':
            departure_station = step['transit_details']['departure_stop']['name']
            arrival_station = step['transit_details']['arrival_stop']['name']
            line = step['transit_details'].get('line', {}).get('name', "Unknown")
            departure_time = step['transit_details']['departure_time']['text']
            arrival_time = step['transit_details']['arrival_time']['text']
            duration = step['duration']['text']
            processed_data.append({
                'departure_station': departure_station,
                'arrival_station': arrival_station,
                'line': line,
                'departure_time': departure_time,
                'arrival_time': arrival_time,
                'duration': duration
            })

    return pd.DataFrame(processed_data)

# Hauptfunktion für die Streamlit-App
def main():
    # Setze den Titel der Streamlit-App
    st.title("Zugroute Visualisierung")

    # Lese den API-Schlüssel aus Streamlit
    api_key = st.secrets["auth_key"]

    # Start- und Endpunkt für die Zugroute
    start_location = "Zürich HB, Schweiz"
    end_location = "Genève, Schweiz"

    # Wenn ein API-Schlüssel vorhanden ist, rufe die Zugroute ab und visualisiere sie
    if api_key:
        # Rufe die Zugroute ab
        train_route = get_train_route(api_key, start_location, end_location)
        
        # Zeige die Zugroute als Tabelle an
        st.write(train_route)
    else:
        st.warning("Bitte geben Sie Ihren Google Maps API-Schlüssel ein.")

# Starte die Streamlit-App
if __name__ == "__main__":
    main()

Copy code
import streamlit as st
import googlemaps
import requests
from datetime import datetime, timedelta
import pandas as pd

# Funktion zum Abrufen der Zugroute von Google Maps API
def get_train_route(api_key, start_location, end_location, departure_time):
    # Initialisiere Google Maps Client
    gmaps = googlemaps.Client(key=api_key)

    # Abfrage für die Zugroute mit Abfahrtszeit
    train_route = gmaps.directions(start_location, end_location, mode="transit", transit_mode="rail", departure_time=departure_time)

    # Verarbeite die Daten und extrahiere relevante Informationen
    processed_data = []
    route_coordinates = []
    for step in train_route[0]['legs'][0]['steps']:
        if step['travel_mode'] == 'TRANSIT':
            departure_station = step['transit_details']['departure_stop']['name']
            arrival_station = step['transit_details']['arrival_stop']['name']
            line = step['transit_details'].get('line', {}).get('name', "Unknown")
            departure_time = step['transit_details']['departure_time']['text']
            arrival_time = step['transit_details']['arrival_time']['text']
            duration = step['duration']['text']
            route_coordinates.append((step['start_location']['lat'], step['start_location']['lng']))
            route_coordinates.append((step['end_location']['lat'], step['end_location']['lng']))
            processed_data.append({
                'departure_station': departure_station,
                'arrival_station': arrival_station,
                'line': line,
                'departure_time': departure_time,
                'arrival_time': arrival_time,
                'duration': duration
            })

    return pd.DataFrame(processed_data), route_coordinates

# Funktion zum Abrufen der lokalen Zeit für einen Ort
def get_local_time(api_key, location):
    url = f"https://maps.googleapis.com/maps/api/timezone/json?location={location}&timestamp=0&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        raw_offset = data.get("rawOffset", 0)
        dst_offset = data.get("dstOffset", 0)
        local_time = datetime.utcnow() + timedelta(seconds=raw_offset + dst_offset)
        return local_time.strftime("%Y-%m-%dT%H:%M:%S")
    else:
        return None

# Hauptfunktion für die Streamlit-App
def main():
    # Setze den Titel der Streamlit-App
    st.title("Zugroute Visualisierung")

    # Lese den API-Schlüssel aus Streamlit
    api_key = st.secrets["auth_key"]

    # Startort eingeben
    start_location = st.text_input("Startort eingeben", "Zürich, Schweiz")

    # Zielort eingeben
    end_location = st.text_input("Zielort eingeben", "Genf, Schweiz")

    # Wenn ein API-Schlüssel vorhanden ist und Start- und Zielort gültig sind
    if api_key and start_location and end_location:
        # Rufe die lokale Abfahrtszeit für den Startort ab
        departure_time = get_local_time(api_key, start_location)

        # Wenn die Abfahrtszeit abgerufen werden konnte
        if departure_time:
            # Rufe die Zugroute und die Koordinaten ab
            train_route, route_coordinates = get_train_route(api_key, start_location, end_location, departure_time)
            
            # Zeige die Zugroute als Tabelle an
            st.subheader(f"Zugroute von {start_location} nach {end_location} (Abfahrt um {departure_time})")
            st.write(train_route)

            # Erstelle eine Google Maps-Karte für die Zugroute
            st.subheader(f"Zugroute von {start_location} nach {end_location} (Abfahrt um {departure_time}) auf Karte anzeigen")
            st.markdown(f'<iframe width="100%" height="500" src="https://www.google.com/maps/embed/v1/directions?key={api_key}&origin={start_location}&destination={end_location}&mode=transit&departure_time={departure_time}" allowfullscreen></iframe>', unsafe_allow_html=True)
        else:
            st.warning("Die lokale Abfahrtszeit konnte nicht abgerufen werden. Bitte überprüfen Sie Ihre Eingabe und versuchen Sie es erneut.")
    else:
        st.warning("Bitte geben Sie Ihren Google Maps API-Schlüssel, sowie einen gültigen Startort und Zielort ein.")

# Starte die Streamlit-App
if __name__ == "__main__":
    main()
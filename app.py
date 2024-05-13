import streamlit as st
import googlemaps
import pandas as pd
import requests

# Funktion zum Abrufen der Zugroute von Google Maps API
def get_train_route(api_key, start_location, end_location):
    # Initialisiere Google Maps Client
    gmaps = googlemaps.Client(key=api_key)

    # Abfrage für die Zugroute
    train_route = gmaps.directions(start_location, end_location, mode="transit", transit_mode="rail")

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

# Funktion zur Umwandlung von Ortsnamen in Koordinaten
def get_coordinates(place, api_key):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={place}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "results" in data and len(data["results"]) > 0:
            location = data["results"][0]["geometry"]["location"]
            return location["lat"], location["lng"]
    return None, None

# Hauptfunktion für die Streamlit-App
def main():
    # Setze den Titel der Streamlit-App
    st.title("Zugroute Visualisierung")

    # Lese den API-Schlüssel aus Streamlit
    api_key = st.secrets["auth_key"]

    # Startorte eingeben
    start_locations = st.text_input("Startorte eingeben (getrennt durch Kommas)", "Zürich HB, Schweiz; Bern, Schweiz; Basel, Schweiz")
    start_locations_list = [x.strip() for x in start_locations.split(';')]

    # Zielort eingeben
    end_location = st.text_input("Zielort eingeben", "Genève, Schweiz")

    # Farben für die Routen festlegen
    colors = ['blue', 'red', 'green', 'yellow', 'orange', 'purple', 'pink']

    # Wenn ein API-Schlüssel vorhanden ist und Start- und Zielort gültig sind
    if api_key and start_locations_list and end_location:
        for i, start_location in enumerate(start_locations_list):
            start_lat, start_lng = get_coordinates(start_location, api_key)
            end_lat, end_lng = get_coordinates(end_location, api_key)
            # Rufe die Zugroute und die Koordinaten ab
            train_route, route_coordinates = get_train_route(api_key, f"{start_lat},{start_lng}", f"{end_lat},{end_lng}")
            
            # Zeige die Zugroute als Tabelle an
            st.subheader(f"Zugroute von {start_location} nach {end_location}")
            st.write(train_route)

            # Erstelle eine Google Maps-Karte für die Zugroute
            st.subheader(f"Zugroute von {start_location} nach {end_location} auf Karte anzeigen")
            directions_layer = gmaps.directions_layer(
                start = (start_lat, start_lng),
                end = (end_lat, end_lng),
                travel_mode = "TRANSIT",
                stroke_color = colors[i % len(colors)],
                stroke_weight = 3.0,
                stroke_opacity = 1.0,
            )
            st.markdown(gmaps.figure_to_html(fig))
    else:
        st.warning("Bitte geben Sie Ihren Google Maps API-Schlüssel ein und stellen Sie sicher, dass die Start- und Zielorte gültig sind.")

# Starte die Streamlit-App
if __name__ == "__main__":
    main()
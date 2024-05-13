import streamlit as st
import googlemaps
import pandas as pd

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

# Hauptfunktion für die Streamlit-App
def main():
    # Setze den Titel der Streamlit-App
    st.title("Zugroute Visualisierung")

    # Lese den API-Schlüssel aus Streamlit
    api_key = st.secrets["auth_key"]

    # Verschiedene Startpunkte auswählen
    start_locations = st.multiselect("Startorte auswählen", ["Zürich HB, Schweiz", "Bern, Schweiz", "Basel, Schweiz"])

    # Zielort eingeben
    end_location = st.text_input("Zielort eingeben", "Genève, Schweiz")

    # Wenn ein API-Schlüssel vorhanden ist und mindestens ein Startpunkt ausgewählt wurde
    if api_key and start_locations and end_location:
        route_coordinates_all = []
        for start_location in start_locations:
            # Rufe die Zugroute und die Koordinaten ab
            train_route, route_coordinates = get_train_route(api_key, start_location, end_location)
            route_coordinates_all.extend(route_coordinates)

            # Zeige die Zugroute als Tabelle an
            st.subheader(f"Zugroute von {start_location} nach {end_location}")
            st.write(train_route)

        # Erstelle eine Google Maps-Karte für alle Routen
        st.subheader(f"Zugrouten auf Karte anzeigen")
        waypoints = '|'.join([f"{coord[0]},{coord[1]}" for coord in route_coordinates_all[1:-1]])
        url = f"https://www.google.com/maps/embed/v1/directions?key={api_key}&origin={start_locations[0]}&destination={end_location}&mode=transit"
        if waypoints:
            url += f"&waypoints={waypoints}"
        st.markdown(f'<iframe width="100%" height="500" src="{url}" allowfullscreen></iframe>', unsafe_allow_html=True)
    else:
        st.warning("Bitte geben Sie Ihren Google Maps API-Schlüssel ein und wählen Sie mindestens einen Startort sowie einen Zielort aus.")

# Starte die Streamlit-App
if __name__ == "__main__":
    main()
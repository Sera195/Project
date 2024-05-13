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
    route_coordinates = []
    for step in train_route[0]['legs'][0]['steps']:
        if step['travel_mode'] == 'TRANSIT':
            departure_station = step['transit_details']['departure_stop']['name']
            arrival_station = step['transit_details']['arrival_stop']['name']
            line = step['transit_details'].get('line', {}).get('name', "Unknown")
            departure_time = step['transit_details']['departure_time']['text']
            arrival_time = step['transit_details']['arrival_time']['text']
            duration = step['duration']['text']
            route_coordinates.append([step['start_location']['lat'], step['start_location']['lng']])
            route_coordinates.append([step['end_location']['lat'], step['end_location']['lng']])
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

    # Start- und Endpunkt für die Zugroute
    start_location = "Zürich HB, Schweiz"
    end_location = "Genève, Schweiz"

    # Wenn ein API-Schlüssel vorhanden ist, rufe die Zugroute ab
    if api_key:
        # Rufe die Zugroute und die Koordinaten ab
        train_route, route_coordinates = get_train_route(api_key, start_location, end_location)
        
        # Zeige die Zugroute als Tabelle an
        st.subheader("Zugroute als Tabelle")
        st.write(train_route)

        # Erstelle eine Pydeck-Karte für die Zugroute
        st.subheader("Zugroute auf Karte anzeigen")
        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(
                latitude=46.8182,
                longitude=8.2275,
                zoom=7,
                pitch=0,
                bearing=0
            ),
            layers=[
                pdk.Layer(
                    'PathLayer',
                    data=route_coordinates,
                    width_scale=8,
                    width_min_pixels=2,
                    get_color=[255, 0, 0],
                    pickable=True,
                    auto_highlight=True
                )
            ]
        ))
    else:
        st.warning("Bitte geben Sie Ihren Google Maps API-Schlüssel ein.")

# Starte die Streamlit-App
if __name__ == "__main__":
    main()
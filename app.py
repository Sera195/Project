import streamlit as st
import googlemaps
import pandas as pd
import requests

# Konfiguration der Karte mit Höhe und Breite und Hinterlegung in fig
gmaps.configure(api_key=API_KEY)
fig = gmaps.figure(layout = {"width": "1550px", "height": "600px"})

# Definiere Farben für verschiedene Routen
colors = [(0, 0, 255), (255, 0, 0), (0, 255, 0), (255, 255, 0), (255, 165, 0), (128, 0, 128), (255, 192, 203)]

# Durchlauf der verschiedenen Startpunkte mittels for Schleife
# Quelle: Angepasst aus ChatGPT
for i, origin in enumerate(origins):
    # Überprüfen ob der Standort eine Adresse ist 
    if ',' in origin:  # Bei der Adresse kann eine Postleitzahl hinzugefügt werden um Doppelungen zu vermeiden jedoch nicht zwingend notwendig 
        place, postal_code = origin.split(',', 1)
        start_latlng = get_coordinates(place.strip())  # Koordinaten werden abgerufen und geladen
        if start_latlng[0] is None or start_latlng[1] is None:
            #Falls Adresse falsch keine Koordinaten gefunden
            print(f"Ort nicht gefunden für {place}")
            continue
    # Falls keine Adresse direkt die Koordinaten des Ortenamens auslesen
    else:
        start_latlng = get_coordinates(origin.strip())  # Koordinaten des Startpunkts abrufen
        if start_latlng[0] is None or start_latlng[1] is None:
            # Falls Ort falsch keine Koordinaten gefunden
            print(f"Ort nicht gefunden für {origin}")
            continue

    # http Anfrage für Routes API zur Bestimmung der Route
    # Quelle: https://www.youtube.com/watch?v=yOXQAmYl0Aw&t=105s
    url_origin = f"https://maps.googleapis.com/maps/api/directions/json?origin={start_latlng[0]},{start_latlng[1]}&destination={destination}&key={API_KEY}"

    # Sende http get Anfrage
    response_origin = requests.get(url_origin)

    # Überprüfe, ob die Anfrage erfolgreich war (Status Code 200 -> OK)
    if response_origin.status_code == 200:
        # Extrahiere Daten aus der Antwort (im JSON-Format)
        data_origin = response_origin.json()

        # Überprüfen ob eine Route zwischen den Koordinaten gefunden werden kann
        # Quelle: Angepasst aus ChatGPT
        if "routes" in data_origin and len(data_origin["routes"]) > 0:
            # Eintrag der Startkoordinaten
            start_location_origin = (data_origin["routes"][0]["legs"][0]["start_location"]["lat"], data_origin["routes"][0]["legs"][0]["start_location"]["lng"],)
            # Eintrag der Endkoordinaten
            end_location_origin = (data_origin["routes"][0]["legs"][0]["end_location"]["lat"], data_origin["routes"][0]["legs"][0]["end_location"]["lng"],)

            # Farbe der Route festlegen
            # Quelle: https://stackoverflow.com/questions/18729180/understanding-the-modulus-operator
            color = colors[i % len(colors)]

            # Angaben welche Art der Route hier Transit -> ÖV, sowie die Darstellung der Route (Farbe, Breite sowie Deckkraft)
            # Quelle: https://developers.google.com/maps/documentation/routes
            # Quelle: https://www.youtube.com/watch?v=mXGyH8_FcMQ&t=5s
            transit_layer_origin = gmaps.directions_layer(
                start = start_location_origin,
                end = end_location_origin,
                travel_mode = "TRANSIT",
                stroke_color = color,
                stroke_weight = 3.0,
                stroke_opacity = 1.0,)

            fig.add_layer(transit_layer_origin)

# Zeige die Karte
st.write(fig)
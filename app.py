pip install streamlit-folium

import streamlit as st
def new_york():

    # Plot coordinates
    coordinates = (40.75, -74)
    _map = gmaps.figure(center=coordinates, zoom_level=12)

    # Render map in Streamlit
    snippet = embed.embed_snippet(views=_map)
    html = embed.html_template.format(title="", snippet=snippet)
    return components.html(html, height=500,width=500)

new_york()
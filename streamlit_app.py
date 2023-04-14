import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy import distance
import json
import time

def print_fancy_header(text, font_size=22, color="#ff5f27"):
    res = f'<span style="color:{color}; font-size: {font_size}px;">{text}</span>'
    st.markdown(res, unsafe_allow_html=True )


    
with st.form(key="user_inputs"):
    print_fancy_header(text='\nHere you can choose which city to process.',
                       font_size=24, color="#00FFFF")
    st.write("🗨 Wait for the map to load, then click on the desired city to select. Now click the 'Submit' button.")

    my_map = folium.Map(location=[39.8283, -98.5795], zoom_start=4)
    
    cities = {
        'Seattle': [47.6062, -122.3321],
        'New York City': [40.7128, -74.0060],
        'Los Angeles': [34.0522, -118.2437],
        'Chicago': [41.8781, -87.6298],
        'Houston': [29.7604, -95.3698]
    }


    # Add markers for each city
    for city, coord in cities.items():
        folium.CircleMarker(
            location=coord,
            popup=city
        ).add_to(my_map)

    my_map.add_child(folium.LatLngPopup())

    res_map = st_folium(my_map, height=300, width=600)

    try:
        new_lat, new_long = res_map["last_clicked"]["lat"], res_map["last_clicked"]["lng"]

        coordinates = {
            "lat": new_lat,
            "long": new_long,
        }

        # display selected points
        
        print_fancy_header(text=f"Latitude: {new_lat}", font_size=18, color="#52fa23")
        print_fancy_header(text=f"Longitude: {new_long}", font_size=18, color="#52fa23")
    
        # Calculate the distance between the clicked location and each city
        distances = {city: distance.distance(coord, (new_lat, new_long)).km for city, coord in cities.items()}

        # Find the city with the minimum distance and print its name
        nearest_city = min(distances, key=distances.get)
        st.write("The nearest city is:", nearest_city)

    except Exception as err:
        print(err)
        pass

    submit_button = st.form_submit_button(label='Submit')



import streamlit as st
import osmnx as ox
import networkx as nx
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Route Planner", page_icon="🌍")

st.title("🌍 Real Route Planner")

# Input
start_place = st.text_input("Enter Start Location")
end_place = st.text_input("Enter Destination")

if st.button("Find Route"):
    geolocator = Nominatim(user_agent="route_app")

    try:
        # Get coordinates
        start_location = geolocator.geocode(start_place)
        end_location = geolocator.geocode(end_place)

        if not start_location or not end_location:
            st.error("❌ Location not found!")
        else:
            start_coords = (start_location.latitude, start_location.longitude)
            end_coords = (end_location.latitude, end_location.longitude)

            # Create bounding box
            north = max(start_coords[0], end_coords[0])
            south = min(start_coords[0], end_coords[0])
            east = max(start_coords[1], end_coords[1])
            west = min(start_coords[1], end_coords[1])

            # Load graph
            G = ox.graph_from_bbox(north, south, east, west, network_type='drive')

            # Find nearest nodes
            start_node = ox.distance.nearest_nodes(G, start_coords[1], start_coords[0])
            end_node = ox.distance.nearest_nodes(G, end_coords[1], end_coords[0])

            # Shortest path
            route = nx.shortest_path(G, start_node, end_node, weight='length')

            # Distance (in km)
            route_length = nx.shortest_path_length(G, start_node, end_node, weight='length') / 1000

            st.success("✅ Route Found!")
            st.write(f"📏 Distance: {route_length:.2f} km")

            # Get coordinates for map
            route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]

            # Create map
            m = folium.Map(location=route_coords[0], zoom_start=6)

            # Draw route
            folium.PolyLine(route_coords, color="blue", weight=5).add_to(m)

            # Add markers
            folium.Marker(route_coords[0], tooltip="Start").add_to(m)
            folium.Marker(route_coords[-1], tooltip="End").add_to(m)

            # Display map
            st_folium(m, width=700, height=500)

    except Exception as e:
        st.error(f"❌ Error: {e}")

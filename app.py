import streamlit as st
import osmnx as ox
import networkx as nx
from geopy.geocoders import Nominatim

st.title("🌍 Real Route Planner")

# User input
start_place = st.text_input("Enter Start Location")
end_place = st.text_input("Enter Destination")

if st.button("Find Route"):
    geolocator = Nominatim(user_agent="route_app")

    try:
        # Convert to coordinates
        start_location = geolocator.geocode(start_place)
        end_location = geolocator.geocode(end_place)

        start_coords = (start_location.latitude, start_location.longitude)
        end_coords = (end_location.latitude, end_location.longitude)

        # Load map graph
        G = ox.graph_from_place(start_place, network_type='drive')

        # Get nearest nodes
        start_node = ox.distance.nearest_nodes(G, start_coords[1], start_coords[0])
        end_node = ox.distance.nearest_nodes(G, end_coords[1], end_coords[0])

        # Shortest path
        route = nx.shortest_path(G, start_node, end_node, weight='length')

        st.success("Route Found!")

        # Plot map
        fig, ax = ox.plot_graph_route(G, route, node_size=0)
        st.pyplot(fig)

    except Exception as e:
        st.error("Error: " + str(e))

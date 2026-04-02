import streamlit as st
import heapq

# Graph (real cities)
graph = {
    'Vijayawada': [('Guntur', 35), ('Hyderabad', 275)],
    'Guntur': [('Hyderabad', 270), ('Bangalore', 600)],
    'Hyderabad': [('Bangalore', 570), ('Chennai', 630)],
    'Bangalore': [('Chennai', 350)],
    'Chennai': []
}

def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    previous = {node: None for node in graph}

    distances[start] = 0
    pq = [(0, start)]

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        for neighbor, weight in graph[current_node]:
            new_distance = current_distance + weight

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current_node
                heapq.heappush(pq, (new_distance, neighbor))

    return distances, previous

def get_path(previous, target):
    path = []
    while target:
        path.append(target)
        target = previous[target]
    return path[::-1]

# UI
st.title("🚗 Route Planner")

start = st.selectbox("Select Start City", list(graph.keys()))
end = st.selectbox("Select Destination City", list(graph.keys()))

if st.button("Find Shortest Path"):
    distances, previous = dijkstra(graph, start)

    st.write("### Shortest Distance:", distances[end], "km")
    st.write("### Path:", " → ".join(get_path(previous, end)))

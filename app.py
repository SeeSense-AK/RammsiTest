import streamlit as st
import folium
import geopandas as gpd
from shapely.geometry import Point
from streamlit_folium import folium_static

# Load existing crash data (replace with your actual data path)
@st.cache_data
def load_data():
    df = gpd.read_file("crash_data.geojson")  # Load as GeoDataFrame
    return df

# Function to calculate risk reduction (simple placeholder logic)
def calculate_risk_change(intervention_type):
    if intervention_type == "Bike Lane":
        return -15  # Assume 15% risk reduction
    elif intervention_type == "Pedestrian Crossing":
        return -10  # Assume 10% reduction
    else:
        return 0  # No effect

# Load data
df = load_data()

# Streamlit UI
st.title("🚴 What-If Urban Planning Tool")

# Display crash heatmap
st.subheader("Crash Hotspots Map")
m = folium.Map(location=[df.geometry.y.mean(), df.geometry.x.mean()], zoom_start=12)
for _, row in df.iterrows():
    folium.CircleMarker(
        location=[row.geometry.y, row.geometry.x],
        radius=5,
        color="red",
        fill=True,
        fill_color="red",
        fill_opacity=0.6,
    ).add_to(m)

folium_static(m)

# User input for adding new infrastructure
st.subheader("Add New Infrastructure")
lat = st.number_input("Latitude", value=df.geometry.y.mean(), format="%.6f")
lon = st.number_input("Longitude", value=df.geometry.x.mean(), format="%.6f")
intervention = st.selectbox("Select Infrastructure Type", ["Bike Lane", "Pedestrian Crossing"])

if st.button("Simulate Impact"):
    risk_change = calculate_risk_change(intervention)
    st.success(f"Estimated risk reduction: {risk_change}% at ({lat}, {lon})")

    # Add marker to map
    folium.Marker(
        location=[lat, lon],
        popup=f"{intervention} - Risk ↓ {risk_change}%",
        icon=folium.Icon(color="green"),
    ).add_to(m)

    folium_static(m)

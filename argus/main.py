import streamlit as st
from utils.fetch_firms import fetch_firms_data
from utils.visualize import visualize_anomalies
from utils.zone_manager import load_all_zones

st.title("ARGUS - Autonomous Recon Grid for Unusual Signatures")

# Load all zones
zones = load_all_zones("zones")
zone_names = [z["name"] for z in zones]

selected_name = st.sidebar.selectbox("📍 Select a monitoring zone", zone_names)
selected_zone = next(z["data"] for z in zones if z["name"] == selected_name)

st.subheader(f"Monitoring Zone: {selected_name}")
firms_data = fetch_firms_data(selected_zone)

# Display raw data
if not firms_data.empty and "latitude" in firms_data.columns and "longitude" in firms_data.columns:
    st.write("### FIRMS Heat Anomalies", firms_data.head(10))
    visualize_anomalies(firms_data, selected_zone)
else:
    st.warning("⚠️ No valid FIRMS data found for this zone. Try a different area or broader time window.")

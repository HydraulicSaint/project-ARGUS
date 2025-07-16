
import streamlit as st
import os
import json
from scanner.live_ping import scan_tiles
from datetime import datetime

st.set_page_config(page_title="ARGUS Recon Console", layout="wide")

st.title("🛰️ ARGUS Recon Console")
st.markdown("Autonomous Recon Grid for Unusual Signatures")

# Sidebar settings
st.sidebar.header("🛠️ Scan Settings")
tile_size = st.sidebar.slider("Tile Size (degrees)", min_value=1, max_value=10, value=5)
scan_delay = st.sidebar.slider("Delay Between Tiles (sec)", min_value=0.0, max_value=5.0, value=1.5)
scan_days = st.sidebar.slider("How many days back to scan?", min_value=1, max_value=7, value=3)
optimize = st.sidebar.checkbox("🌍 Exclude open ocean & polar zones", value=True)

# Zone selection
zone_files = [f for f in os.listdir("zones") if f.endswith(".json")]
zone_choice = st.sidebar.selectbox("Zone", ["Custom"] + zone_files)

if zone_choice != "Custom":
    with open(os.path.join("zones", zone_choice), "r", encoding="utf-8") as f:
        z = json.load(f)
    lat_range = (z["lat_min"], z["lat_max"])
    lon_range = (z["lon_min"], z["lon_max"])
else:
    default_lat = (-60, 60) if optimize else (-90, 90)
    default_lon = (-170, 170) if optimize else (-180, 180)
    lat_min = st.sidebar.number_input("Lat Min", value=float(default_lat[0]), format="%.2f")
    lat_max = st.sidebar.number_input("Lat Max", value=float(default_lat[1]), format="%.2f")
    lon_min = st.sidebar.number_input("Lon Min", value=float(default_lon[0]), format="%.2f")
    lon_max = st.sidebar.number_input("Lon Max", value=float(default_lon[1]), format="%.2f")
    lat_range = (lat_min, lat_max)
    lon_range = (lon_min, lon_max)

if st.sidebar.button("🚀 Launch ARGUS Scan"):
    with st.spinner("Scanning..."):
        scan_tiles(step=tile_size, delay=scan_delay, days=scan_days,
                   lat_range=lat_range, lon_range=lon_range)
    st.success("Scan complete. Grid map updated!")

# Display the latest grid map
map_path = "output/grid_map.html"
if os.path.exists(map_path):
    st.subheader("🌍 Thermal Scan Map")
    with open(map_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    st.components.v1.html(html_content, height=700)
else:
    st.warning("Map not generated yet. Run a scan to create the first grid map.")

# Optional: footer or logs
st.caption(f"Last refreshed: {datetime.utcnow().isoformat()} UTC")

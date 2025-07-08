import folium
from streamlit_folium import st_folium
import pandas as pd  # Needed for pd.isna()


def visualize_anomalies(df, zone):
    if df.empty:
        print("⚠️ DataFrame is empty — skipping map.")
        return

    if "latitude" not in df.columns or "longitude" not in df.columns:
        print("❌ Missing 'latitude' or 'longitude' columns — cannot visualize.")
        return

    lat_center = (zone["lat_min"] + zone["lat_max"]) / 2
    lon_center = (zone["lon_min"] + zone["lon_max"]) / 2

    m = folium.Map(location=[lat_center, lon_center], zoom_start=6, control_scale=True)

    for _, row in df.iterrows():
        lat = row.get("latitude")
        lon = row.get("longitude")

        if pd.isna(lat) or pd.isna(lon):
            continue

        popup_text = f"🔥 Brightness: {row.get('bright_ti4', '?')}<br>Confidence: {row.get('confidence', '?')}<br>Date: {row.get('acq_date', '?')}"
        folium.CircleMarker(
            location=[lat, lon],
            radius=6,
            popup=popup_text,
            color="red",
            fill=True,
            fill_opacity=0.7
        ).add_to(m)

    st_folium(m, width=700, height=500)

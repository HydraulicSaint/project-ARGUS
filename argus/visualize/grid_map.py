import folium
from folium.plugins import HeatMap
from typing import List, Dict
import os
from argus.scanner.coarse_grid import generate_grid

def build_map(scan_log: List[Dict], output="output/grid_map.html"):
    """Builds a 2D grid map with color-coded tiles and a heatmap layer."""

    # Create map centered at 0,0
    m = folium.Map(location=[0, 0], zoom_start=2, tiles="cartodb positron")

    heat_points = []
    for tile in scan_log:
        bounds = [
            [tile["lat_min"], tile["lon_min"]],
            [tile["lat_max"], tile["lon_max"]]
        ]
        name = tile["name"]
        hits = tile.get("hits", 0)
        timestamp = tile.get("timestamp", "N/A")
        status = tile.get("status", "unknown")

        color = {
            "clear": "green",
            "heat": "red",
            "unknown": "gray"
        }.get(status, "blue")

        tooltip = f"{name}<br>{status.upper()}<br>Hits: {hits}<br>Last Scan: {timestamp}"

        folium.Rectangle(
            bounds=bounds,
            color=color,
            fill=True,
            fill_opacity=0.4,
            tooltip=tooltip
        ).add_to(m)

        if status == "heat":
            heat_points.append([
                (tile["lat_min"] + tile["lat_max"]) / 2,
                (tile["lon_min"] + tile["lon_max"]) / 2,
                hits
            ])

    if heat_points:
        HeatMap(heat_points, radius=15, blur=10).add_to(m)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output), exist_ok=True)
    m.save(output)

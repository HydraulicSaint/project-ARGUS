import os
from typing import List, Dict
import plotly.graph_objects as go


def build_globe(scan_log: List[Dict], output: str = "output/globe_map.html") -> None:
    """Build an orthographic globe map from scan log data."""

    fig = go.Figure()

    for tile in scan_log:
        color = {
            "clear": "green",
            "heat": "red",
            "unknown": "gray",
        }.get(tile.get("status", "unknown"), "blue")

        lats = [
            tile["lat_min"],
            tile["lat_min"],
            tile["lat_max"],
            tile["lat_max"],
            tile["lat_min"],
        ]
        lons = [
            tile["lon_min"],
            tile["lon_max"],
            tile["lon_max"],
            tile["lon_min"],
            tile["lon_min"],
        ]

        hover = (
            f"{tile['name']}<br>{tile.get('status', 'UNKNOWN').upper()}"
            f"<br>Hits: {tile.get('hits', 0)}"
            f"<br>Last Scan: {tile.get('timestamp', 'N/A')}"
        )

        fig.add_trace(
            go.Scattergeo(
                lon=lons,
                lat=lats,
                mode="lines",
                line=dict(width=1, color=color),
                fill="toself",
                fillcolor=color,
                opacity=0.3,
                hoverinfo="text",
                text=hover,
                name=tile["name"],
            )
        )

    fig.update_geos(
        projection_type="orthographic",
        showcountries=True,
        landcolor="rgb(229, 229, 229)",
        showocean=True,
        oceancolor="rgb(0, 169, 231)",
    )
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), showlegend=False)

    os.makedirs(os.path.dirname(output), exist_ok=True)
    fig.write_html(output)

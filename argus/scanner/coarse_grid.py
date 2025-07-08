# scanner/coarse_grid.py

def generate_grid(step=5, lat_range=(-60, 60), lon_range=(-170, 170)):
    """Generates a grid of tiles covering the Earth in latitude/longitude steps."""
    tiles = []

    for lat in range(lat_range[0], lat_range[1], step):
        for lon in range(lon_range[0], lon_range[1], step):
            tiles.append({
                "name": f"tile_{lat}_{lon}",
                "lat_min": lat,
                "lat_max": lat + step,
                "lon_min": lon,
                "lon_max": lon + step
            })

    return tiles

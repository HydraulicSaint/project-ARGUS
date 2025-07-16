import json
import os


def write_zone(name, lat_min, lat_max, lon_min, lon_max, directory="zones"):
    """Save a zone definition to a JSON file and return the file path."""
    os.makedirs(directory, exist_ok=True)
    zone = {
        "name": name,
        "lat_min": lat_min,
        "lat_max": lat_max,
        "lon_min": lon_min,
        "lon_max": lon_max,
    }
    path = os.path.join(directory, f"{name.lower().replace(' ', '_')}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(zone, f, indent=4)
    return path

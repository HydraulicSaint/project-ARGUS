import os
import json

def load_all_zones(directory="zones"):
    zone_files = [f for f in os.listdir(directory) if f.endswith(".json")]
    zones = []

    for filename in zone_files:
        with open(os.path.join(directory, filename)) as f:
            data = json.load(f)
            zones.append({
                "name": data.get("name", filename),
                "data": data
            })

    return zones

# scanner/live_ping.py

import time
import requests
from config import MAP_KEY
from scanner.coarse_grid import generate_grid
from datetime import datetime, timezone
from visualize.grid_map import build_map  # NEW: for visual integration

def scan_tiles(step=5, delay=1.5, days=3, source="VIIRS_SNPP_NRT",  lat_range=(-90, 90), lon_range=(-180, 180)):
    tiles = generate_grid(step=step)
    scan_log = []

    print(f"🔍 Starting live scan with {len(tiles)} tiles...\n")

    for tile in tiles:
        bbox = f"{tile['lon_min']},{tile['lat_min']},{tile['lon_max']},{tile['lat_max']}"
        url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{MAP_KEY}/{source}/{bbox}/{days}"

        try:
            response = requests.get(url)
            now = datetime.now(timezone.utc).isoformat()

            if response.status_code == 200:
                lines = response.text.splitlines()
                if len(lines) > 1:
                    hit_count = len(lines) - 1
                    print(f"🔥 {tile['name']} → {hit_count} detections")
                    scan_log.append({
                        **tile,
                        "status": "heat",
                        "hits": hit_count,
                        "timestamp": now
                    })
                        
                else:
                    print(f"✅ Clear: {tile['name']}")
                    scan_log.append({
                        **tile,
                        "status": "clear",
                        "hits": 0,
                        "timestamp": now
                    })
                    # 🧠 Visual feedback every 5 tiles
                if len(scan_log) % 5 == 0:
                    build_map(scan_log, output="output/grid_map.html")
                    print(f"🗺️ Map updated at {len(scan_log)} tiles scanned.")

            else:
                print(f"⚠️ API error {response.status_code} for {tile['name']}")

        except Exception as e:
            print(f"⚠️ Error scanning {tile['name']}: {e}")

        time.sleep(delay)

    # 🔁 After scanning all tiles: generate visual map
    print("🗺️ Generating map...")
    build_map(scan_log, output="output/grid_map.html")
    print("✅ Map written to output/grid_map.html")

# ✅ MAIN TRIGGER
if __name__ == "__main__":
    scan_tiles()

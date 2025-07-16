# scanner/live_ping.py

import time
import requests
import logging
from config import MAP_KEY
from scanner.coarse_grid import generate_grid
from datetime import datetime, timezone
from visualize.grid_map import build_map  # NEW: for visual integration

logger = logging.getLogger(__name__)

def scan_tiles(step=5, delay=1.5, days=3, source="VIIRS_SNPP_NRT",  lat_range=(-90, 90), lon_range=(-180, 180)):
    tiles = generate_grid(step=step, lat_range=lat_range, lon_range=lon_range)
    scan_log = []

    logger.info("Starting live scan with %d tiles", len(tiles))

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
                    logger.info("%s - %d detections", tile['name'], hit_count)
                    scan_log.append({
                        **tile,
                        "status": "heat",
                        "hits": hit_count,
                        "timestamp": now
                    })
                        
                else:
                    logger.debug("Clear: %s", tile['name'])
                    scan_log.append({
                        **tile,
                        "status": "clear",
                        "hits": 0,
                        "timestamp": now
                    })
                    # 🧠 Visual feedback every 5 tiles
                if len(scan_log) % 5 == 0:
                    build_map(scan_log, output="output/grid_map.html")
                    logger.debug("Map updated at %d tiles scanned", len(scan_log))

            else:
                logger.warning("API error %s for %s", response.status_code, tile['name'])

        except Exception as e:
            logger.error("Error scanning %s: %s", tile['name'], e)

        time.sleep(delay)

    # 🔁 After scanning all tiles: generate visual map
    logger.info("Generating map...")
    build_map(scan_log, output="output/grid_map.html")
    logger.info("Map written to output/grid_map.html")

# ✅ MAIN TRIGGER
if __name__ == "__main__":
    scan_tiles()

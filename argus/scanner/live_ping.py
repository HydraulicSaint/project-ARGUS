# scanner/live_ping.py

import time
import requests
import logging
from config import MAP_KEY
from argus.scanner.coarse_grid import generate_grid
from datetime import datetime, timezone
from argus.visualize.grid_map import build_map
from argus.visualize.globe_map import build_globe

logger = logging.getLogger(__name__)

def scan_tiles(step=5, delay=1.5, days=3, source="VIIRS_SNPP_NRT",
               lat_range=(-90, 90), lon_range=(-180, 180),
               progress_callback=None, globe=False):
    """Scan tiles for FIRMS detections and update the grid map.

    Parameters
    ----------
    step : int
        Grid spacing in degrees.
    delay : float
        Delay in seconds between tile queries.
    days : int
        How many days back to fetch FIRMS data.
    source : str
        FIRMS product identifier.
    lat_range : tuple
        Latitude range to scan.
    lon_range : tuple
        Longitude range to scan.
    progress_callback : callable, optional
        Function called with ``(done, total)`` after each tile is processed.
    globe : bool, optional
        If True, also generate a globe map in ``output/globe_map.html``.
    """

    tiles = generate_grid(step=step, lat_range=lat_range, lon_range=lon_range)
    total_tiles = len(tiles)
    scan_log = []

    logger.info("Starting live scan with %d tiles", total_tiles)

    for idx, tile in enumerate(tiles, start=1):
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
                    if globe:
                        build_globe(scan_log, output="output/globe_map.html")
                    logger.debug("Map updated at %d tiles scanned", len(scan_log))
                    if progress_callback:
                        progress_callback(idx, total_tiles)

            else:
                logger.warning("API error %s for %s", response.status_code, tile['name'])

        except Exception as e:
            logger.error("Error scanning %s: %s", tile['name'], e)

        if progress_callback and len(scan_log) % 5 != 0:
            progress_callback(idx, total_tiles)

        time.sleep(delay)

    # 🔁 After scanning all tiles: generate visual map
    logger.info("Generating map...")
    build_map(scan_log, output="output/grid_map.html")
    if globe:
        build_globe(scan_log, output="output/globe_map.html")
    logger.info("Map written to output/grid_map.html")
    if progress_callback:
        progress_callback(total_tiles, total_tiles)

# ✅ MAIN TRIGGER
if __name__ == "__main__":
    scan_tiles()

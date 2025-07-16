import pandas as pd
import requests
import logging
from io import StringIO
from config import MAP_KEY

logger = logging.getLogger(__name__)

def fetch_firms_data(zone):
    # Construct bounding box string for API
    south = zone["lat_min"]
    north = zone["lat_max"]
    west = zone["lon_min"]
    east = zone["lon_max"]
    bbox = f"{west},{south},{east},{north}"

    # Choose source and day range
    source = "VIIRS_SNPP_NRT"
    day_range = 7

    url = (
        f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/"
        f"{MAP_KEY}/{source}/{bbox}/{day_range}"
    )

    try:
        logger.info("Requesting FIRMS data from %s", url)

        response = requests.get(url)
        response.raise_for_status()

        with open("data/latest_firms_pull.csv", "w", encoding="utf-8") as f:
            f.write(response.text)

        df = pd.read_csv(StringIO(response.text))
        df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

        logger.info("FIRMS data pulled successfully")
        logger.debug("Columns: %s", df.columns.tolist())


        return df
    except Exception as e:
        logger.error("Error fetching FIRMS data: %s", e)
        return pd.DataFrame()

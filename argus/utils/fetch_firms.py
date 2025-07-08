import pandas as pd
import requests
from io import StringIO
from config import MAP_KEY

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
        print("🌐 Requesting FIRMS data from:")
        print(url)

        response = requests.get(url)
        response.raise_for_status()

        with open("data/latest_firms_pull.csv", "w", encoding="utf-8") as f:
            f.write(response.text)

        df = pd.read_csv(StringIO(response.text))
        df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

        print("\n✅ FIRMS data pulled successfully")
        print("Columns:", df.columns.tolist())
        print(df.head(3).to_string())


        return df
    except Exception as e:
        print("🚫 Error fetching FIRMS data:", e)
        return pd.DataFrame()

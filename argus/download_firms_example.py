from .config import MAP_KEY
import requests
import os

# === CONFIG ===
source = "VIIRS_SNPP_NRT"
day_range = 7

# Bounding box for testing (Australia fire zone — usually has data)
lat_min = -36.5
lat_max = -35.5
lon_min = 148.5
lon_max = 149.5

# Construct bounding box string for API
bbox = f"{lon_min},{lat_min},{lon_max},{lat_max}"
url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{MAP_KEY}/{source}/{bbox}/{day_range}"

# Output location
os.makedirs("data", exist_ok=True)
output_file = "data/firms_raw_output.csv"

print(f"🔄 Downloading FIRMS data from:\n{url}")

try:
    response = requests.get(url)
    response.raise_for_status()

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(response.text)

    print(f"✅ Data saved to: {output_file}")
except Exception as e:
    print("❌ Error downloading FIRMS data:", e)

import os
import urllib.request
import logging

NASA_API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")
logger = logging.getLogger(__name__)


def fetch_satellite_image(lat, lon, *, dim=0.1, date=None, output="data/satellite.png"):
    """Download a satellite image for the given coordinates.

    Parameters
    ----------
    lat, lon : float
        Center point of the desired image.
    dim : float, optional
        Width and height of the image in degrees.
    date : str, optional
        Date string (YYYY-MM-DD). If omitted, the most recent image is used.
    output : str, optional
        Path where the image file will be written.

    Returns
    -------
    str
        The path to the saved image file.
    """
    params = f"lat={lat}&lon={lon}&dim={dim}&api_key={NASA_API_KEY}"
    if date:
        params += f"&date={date}"
    url = f"https://api.nasa.gov/planetary/earth/imagery?{params}"
    logger.info("Fetching satellite image from %s", url)
    with urllib.request.urlopen(url) as resp:
        data = resp.read()
    os.makedirs(os.path.dirname(output), exist_ok=True)
    with open(output, "wb") as f:
        f.write(data)
    return output


def classify_thermal_anomaly(image_path, *, threshold=50000):
    """Very basic classification based on file size.

    The function returns ``"hot spot"`` if the file size exceeds ``threshold``
    bytes, otherwise ``"no anomaly"``. This placeholder approach avoids heavy
    dependencies while providing a simple example pipeline.
    """
    size = os.path.getsize(image_path)
    return "hot spot" if size > threshold else "no anomaly"

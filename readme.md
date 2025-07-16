# ARGUS

**Autonomous Recon Grid for Unusual Signatures**

ARGUS scans the NASA FIRMS (Fire Information for Resource Management System) API for recent thermal anomalies. It walks a configurable latitude/longitude grid, logs detections, and builds an interactive map showing the results. A Streamlit app provides a simple interface to trigger scans and view the generated map.

## Requirements

- Python 3.x
- The Python packages listed in [`argus/requirements.txt`](argus/requirements.txt)
- A valid FIRMS "Map Key" API token

## Getting Started

1. Install the dependencies:

   ```bash
   pip install -r argus/requirements.txt
   ```

2. Provide your own FIRMS API token. Edit `argus/config.py` and replace the value of `MAP_KEY` with your token. Do not commit private keys to source control.

3. Launch the Streamlit console:

   ```bash
   streamlit run argus/app.py
   ```

   Choose your grid settings and start a scan. Results are written to `output/grid_map.html`.

You can also run `python argus/scanner/live_ping.py` to perform a scan without the Streamlit UI.

## Project Structure

- `argus/scanner/` – core scanning logic for iterating grid tiles
- `argus/visualize/` – utilities for rendering Folium maps
- `argus/utils/` – helpers for fetching FIRMS data and managing zones
- `argus/zones/` – sample monitoring zones in JSON format

## License and API Keys

This repository is provided for educational reference. Review the license in [`LICENSE`](LICENSE) for usage restrictions. A valid FIRMS API key is required to obtain data and must be supplied by the user.

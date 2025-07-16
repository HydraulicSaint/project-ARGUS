# ARGUS

Autonomous Recon Grid for Unusual Signatures.

This project scans NASA FIRMS data for thermal anomalies and visualizes the results.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Provide your FIRMS API key in `argus/config.py` or a `.env` file.

## Usage

Run the Streamlit interface:

```bash
streamlit run argus/app.py
```

Scan results will be saved to `output/grid_map.html`.

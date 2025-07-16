# ARGUS

Autonomous Recon Grid for Unusual Signatures.

This project scans NASA FIRMS data for thermal anomalies and visualizes the results.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a `.env` file with your FIRMS API key:
   ```
   FIRMS_API_KEY=YOUR_KEY_HERE
   ```

## Usage

Run the Streamlit interface:

```bash
streamlit run argus/app.py
```

Scan results will be saved to `output/grid_map.html`.

## Testing

Run unit tests with `pytest`:

```bash
pytest
```

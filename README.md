# SlopeX — SIH Internal Hackathon MVP

## What this demonstrates
A location-specific landslide risk monitoring dashboard for the North-East Region (NER):
- Interactive NER map
- Risk classification: LOW / MODERATE / HIGH
- Explainable risk score
- Simulator for rainfall, intensity, slope, elevation, soil, land cover, drainage and historical events
- Monitoring summary table
- Flask backend API

## Run on Windows
1. Install Python 3.10+.
2. Open this folder in VS Code terminal.
3. Run:
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   python app.py
4. Open http://127.0.0.1:5000

## Demo flow
1. Open the dashboard.
2. Show the NER risk map.
3. Select a location / explain the factors.
4. Set rainfall to ~280 mm, intensity ~55 mm/h, slope ~40°, drainage Poor.
5. Click CALCULATE RISK.
6. Explain that the current engine is an interpretable weighted baseline and is designed to be replaced by a trained Random Forest/XGBoost model using real geospatial/time-series data.
7. Show the monitoring table.

## Important
The current location conditions are synthetic demo data. Do not claim they are live IMD/ISRO observations.
For a production version, integrate verified rainfall, DEM/slope, soil, land-cover, drainage and historical landslide datasets and validate the model spatially and temporally.

## Pitch line
"SlopeX converts environmental and terrain signals into an actionable, location-specific landslide risk score so authorities can monitor vulnerable zones and trigger early-warning workflows before conditions become critical."

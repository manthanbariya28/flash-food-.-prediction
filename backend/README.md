# Backend Module

Owner: TBD

## Goal
Serve the ML model's flood risk predictions to the frontend via a simple API.

## Suggested first steps
1. Use FastAPI (or Flask) — create `main.py` with a `/flood-risk` GET endpoint
   that returns a list of regions with their risk scores (matches the shape
   in `src/services/api.js` MOCK_DATA on the frontend).
2. Import the ML module's `predict.py` to generate real scores instead of
   hardcoded values.
3. Add `/data/*` routes if the frontend needs raw data (rainfall, river level)
   for charts.

## Expected response shape (contract with frontend)
```json
[
  { "id": 1, "name": "Region A", "lat": 29.39, "lng": 79.45, "riskScore": 82, "rainfallMm": 120 }
]
```

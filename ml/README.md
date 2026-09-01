# ML Module

Owner: ML lead (you)

## Goal
Take fused features (rainfall intensity, slope, soil saturation, river level
trend) and output a flood risk score (0-100) or risk class per region.

## Suggested first steps
1. Put a sample/synthetic dataset in `ml/data/` (csv) with columns like:
   `region_id, rainfall_mm_3h, rainfall_mm_24h, slope_deg, soil_moisture,
   river_level_m, land_use_type, flood_occurred (label)`
2. Start with a baseline: Random Forest / XGBoost classifier or regressor —
   fast to train, explainable, good enough for a hackathon demo.
3. Export the trained model (`joblib`/`pickle`) into `ml/model/` so the
   backend can load it.
4. Write a small `predict.py` that backend/API can call or import.

## Files to create here
- `train.py` — training script
- `predict.py` — inference function used by backend
- `data/` — datasets (raw + processed)
- `model/` — saved trained model file

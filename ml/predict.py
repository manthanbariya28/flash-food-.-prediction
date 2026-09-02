"""
predict.py — Inference module for the flood risk model.

Backend team: import `predict_risk()` from this file and call it with a
dict of raw feature values. It returns a risk score (0-100) and a flood
flag, matching the frontend's expected API shape.

Example:
    from predict import predict_risk

    result = predict_risk({
        "rainfall_mm_3h": 45.0,
        "rainfall_mm_24h": 120.0,
        "slope_deg": 22.0,
        "soil_moisture": 0.55,
        "river_level_m": 3.2,
        "land_use_type": "Urban",
    })
    # -> {"riskScore": 78.4, "floodLikely": True}
"""

import os
import joblib
import pandas as pd

MODEL_DIR = os.path.join(os.path.dirname(__file__), "model")

_model = None
_land_use_encoder = None
_threshold = None


def _load_artifacts():
    global _model, _land_use_encoder, _threshold
    if _model is None:
        _model = joblib.load(os.path.join(MODEL_DIR, "flood_rf_model.joblib"))
        _land_use_encoder = joblib.load(os.path.join(MODEL_DIR, "land_use_encoder.joblib"))
        _threshold = joblib.load(os.path.join(MODEL_DIR, "decision_threshold.joblib"))


def predict_risk(features: dict) -> dict:
    """
    features: dict with keys
        rainfall_mm_3h, rainfall_mm_24h, slope_deg, soil_moisture,
        river_level_m, land_use_type (one of: Agriculture, Urban, Barren, Forest)

    Returns: {"riskScore": float (0-100), "floodLikely": bool}
    """
    _load_artifacts()

    land_use_encoded = _land_use_encoder.transform([features["land_use_type"]])[0]

    row = pd.DataFrame([{
        "rainfall_mm_3h": features["rainfall_mm_3h"],
        "rainfall_mm_24h": features["rainfall_mm_24h"],
        "slope_deg": features["slope_deg"],
        "soil_moisture": features["soil_moisture"],
        "river_level_m": features["river_level_m"],
        "land_use_encoded": land_use_encoded,
    }])

    probability = _model.predict_proba(row)[0, 1]  # probability of flood_occurred=1
    risk_score = round(float(probability) * 100, 1)
    flood_likely = bool(probability >= _threshold)

    return {"riskScore": risk_score, "floodLikely": flood_likely}


def predict_batch(rows: list) -> list:
    """Same as predict_risk but for a list of feature dicts — used when
    scoring multiple regions at once for the dashboard."""
    return [predict_risk(r) for r in rows]


if __name__ == "__main__":
    # Quick manual test
    sample = {
        "rainfall_mm_3h": 60.0,
        "rainfall_mm_24h": 150.0,
        "slope_deg": 28.0,
        "soil_moisture": 0.68,
        "river_level_m": 4.5,
        "land_use_type": "Urban",
    }
    print(predict_risk(sample))

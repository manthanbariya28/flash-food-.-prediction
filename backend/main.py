from fastapi import FastAPI
from ml.predict import predict_risk
from backend.alerts.notifier import send_alert

app = FastAPI(title="Flood Risk Prediction API")


@app.get("/")
def home():
    return {"message": "Flood Risk API is running"}


@app.get("/flood-risk")
def flood_risk():
    regions = [
        {
            "id": 1,
            "name": "Region A",
            "lat": 29.39,
            "lng": 79.45,
            "rainfallMm": 120.0,
            "features": {
                "rainfall_mm_3h": 45.0,
                "rainfall_mm_24h": 120.0,
                "slope_deg": 22.0,
                "soil_moisture": 0.55,
                "river_level_m": 3.2,
                "land_use_type": "Urban"
            }
        }
    ]

    results = []

    for region in regions:
        prediction = predict_risk(region["features"])
        

    if prediction["riskScore"] >= 70:
        send_alert(
            region["name"],
            prediction["riskScore"]
        )

    results.append({
        "id": region["id"],
        "name": region["name"],
        "lat": region["lat"],
        "lng": region["lng"],
        "riskScore": prediction["riskScore"],
        "rainfallMm": region["rainfallMm"]
    })

    return results

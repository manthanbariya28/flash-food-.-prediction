from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ml.predict import predict_risk
from backend.alerts.notifier import send_alert

app = FastAPI(title="Flood Risk Prediction API")

# Allow the React frontend (running on a different port) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for hackathon demo; restrict this in production
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Flood Risk API is running"}


@app.get("/flood-risk")
def flood_risk():
    regions = [
        {
            "id": 1, "name": "Region A - Nainital", "lat": 29.39, "lng": 79.45,
            "rainfallMm": 120.0,
            "features": {
                "rainfall_mm_3h": 45.0, "rainfall_mm_24h": 120.0,
                "slope_deg": 22.0, "soil_moisture": 0.55,
                "river_level_m": 3.2, "land_use_type": "Urban",
            },
        },
        {
            "id": 2, "name": "Region B - Shimla", "lat": 31.10, "lng": 77.17,
            "rainfallMm": 60.0,
            "features": {
                "rainfall_mm_3h": 20.0, "rainfall_mm_24h": 60.0,
                "slope_deg": 18.0, "soil_moisture": 0.4,
                "river_level_m": 2.0, "land_use_type": "Forest",
            },
        },
        {
            "id": 3, "name": "Region C - Gangtok", "lat": 27.33, "lng": 88.60,
            "rainfallMm": 290.0,
            "features": {
                "rainfall_mm_3h": 160.0, "rainfall_mm_24h": 290.0,
                "slope_deg": 28.0, "soil_moisture": 0.88,
                "river_level_m": 6.4, "land_use_type": "Urban",
            },
        },
    ]

    results = []
    for region in regions:
        prediction = predict_risk(region["features"])

        if prediction["riskScore"] >= 70:
            send_alert(region["name"], prediction["riskScore"])

        results.append({
            "id": region["id"],
            "name": region["name"],
            "lat": region["lat"],
            "lng": region["lng"],
            "riskScore": prediction["riskScore"],
            "rainfallMm": region["rainfallMm"],
        })

    return results

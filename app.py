from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np
from datetime import datetime

model = joblib.load("models/aqi_model.pkl")
city_encoder = joblib.load("models/city_encoder.pkl")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AQIData(BaseModel):
    date: str
    city: str
    pm25: float
    pm10: float
    no2: float
    co: float
    temp: float
    humidity: float
    retail_mobility: float
    workplace_mobility: float
    transit_mobility: float


def aqi_category(aqi):
    if aqi <= 50: return "Good 🟢"
    elif aqi <= 100: return "Satisfactory 🟡"
    elif aqi <= 200: return "Moderate 🟠"
    elif aqi <= 300: return "Poor 🔴"
    elif aqi <= 400: return "Very Poor 🟣"
    else: return "Severe ⚫"


@app.get("/")
def home():
    return {"message": "AQI Prediction API Running 🚀"}


@app.post("/predict")
def predict(data: AQIData):
    try:
        # safe city encoding
        try:
            city_encoded = city_encoder.transform([data.city])[0]
        except:
            return {"error": f"City '{data.city}' not in training data"}

        dt = datetime.fromisoformat(data.date)

        features = [
            city_encoded,
            data.pm25,
            data.pm10,
            data.no2,
            data.co,
            data.temp,
            data.humidity,
            data.retail_mobility,
            data.workplace_mobility,
            data.transit_mobility,
            dt.year,
            dt.month,
            dt.day,
            dt.hour
        ]

        prediction = model.predict(np.array([features]))[0]

        return {
            "predicted_aqi": float(prediction),
            "category": aqi_category(prediction)
        }

    except Exception as e:
        return {"error": str(e)}

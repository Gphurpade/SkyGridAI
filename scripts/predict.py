"""
predict.py

Reusable prediction module for SkyGridAI.
"""

import joblib
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RAIN_MODEL_PATH = BASE_DIR / "models" / "rainfall_model.pkl"
MAX_MODEL_PATH = BASE_DIR / "models" / "max_temp_model.pkl"
MIN_MODEL_PATH = BASE_DIR / "models" / "min_temp_model.pkl"

rain_model = None
max_model = None
min_model = None


def _load_models():
    global rain_model, max_model, min_model

    if rain_model is not None and max_model is not None and min_model is not None:
        return

    missing = [
        path.name for path in [RAIN_MODEL_PATH, MAX_MODEL_PATH, MIN_MODEL_PATH]
        if not path.exists()
    ]

    if missing:
        raise RuntimeError(
            "The required trained model files are missing: " + ", ".join(missing)
        )

    rain_model = joblib.load(RAIN_MODEL_PATH)
    max_model = joblib.load(MAX_MODEL_PATH)
    min_model = joblib.load(MIN_MODEL_PATH)


def predict_all(day, latitude, longitude, max_temp_input, min_temp_input):
    """
    Predict rainfall, maximum temperature and minimum temperature.

    Parameters
    ----------
    day : int
    latitude : float
    longitude : float
    max_temp_input : float
    min_temp_input : float

    Returns
    -------
    dict
    """

    _load_models()

    rain_features = pd.DataFrame([{
        "Day": day,
        "Latitude": latitude,
        "Longitude": longitude,
        "MaxTemp": max_temp_input,
        "MinTemp": min_temp_input
    }])

    predicted_rainfall = rain_model.predict(rain_features)[0]

    temp_features = pd.DataFrame([{
        "Day": day,
        "Latitude": latitude,
        "Longitude": longitude,
        "Rainfall": predicted_rainfall
    }])

    predicted_max = max_model.predict(temp_features)[0]
    predicted_min = min_model.predict(temp_features)[0]

    return {
        "rainfall": float(predicted_rainfall),
        "max_temperature": float(predicted_max),
        "min_temperature": float(predicted_min)
    }


if __name__ == "__main__":

    print("SkyGridAI Prediction Module\n")

    day = int(input("Day (1-365): "))
    latitude = float(input("Latitude: "))
    longitude = float(input("Longitude: "))
    max_temp = float(input("Maximum Temperature (°C): "))
    min_temp = float(input("Minimum Temperature (°C): "))

    result = predict_all(
        day,
        latitude,
        longitude,
        max_temp,
        min_temp
    )

    print("\nPrediction Result")
    print("-----------------------------")
    print(f"Rainfall : {result['rainfall']:.2f} mm")
    print(f"Max Temp : {result['max_temperature']:.2f} °C")
    print(f"Min Temp : {result['min_temperature']:.2f} °C")
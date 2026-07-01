"""
predict.py - Optimized for Hugging Face Hub (Using .pkl files)
"""
import streamlit as st
import joblib
import pandas as pd
from huggingface_hub import hf_hub_download

# CONFIGURATION: Replace these with your actual Hugging Face repo details
# Example: "johndoe/skygrid-models"
REPO_ID = "your-username/skygrid-models" 

@st.cache_resource
def get_model(filename):
    """
    Downloads model from Hugging Face Hub and caches it in memory.
    This avoids local storage issues.
    """
    try:
        model_path = hf_hub_download(repo_id=REPO_ID, filename=filename)
        return joblib.load(model_path)
    except Exception as e:
        st.error(f"Error loading model {filename} from Hub: {e}")
        return None

def predict_all(day, latitude, longitude, max_temp_input, min_temp_input):
    """
    Predicts weather metrics using models fetched from Hugging Face.
    """
    # Changed from .joblib to .pkl here:
    rain_model = get_model("rainfall_model.pkl")
    max_model = get_model("max_temp_model.pkl")
    min_model = get_model("min_temp_model.pkl")

    if None in [rain_model, max_model, min_model]:
        return {"rainfall": 0.0, "max_temperature": 0.0, "min_temperature": 0.0}

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

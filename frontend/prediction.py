"""Frontend wrapper for the existing backend prediction pipeline."""

from __future__ import annotations

import importlib
import time
from typing import Any

import pandas as pd
import streamlit as st

from frontend.constants import DATASET_PATH
from frontend.utils import estimated_confidence, prediction_to_record


@st.cache_resource(show_spinner=False)
def load_backend_predictor() -> tuple[Any, float]:
    """Load the backend module once and return predict_all with import time."""
    start = time.perf_counter()
    module = importlib.import_module("scripts.predict")
    load_time = time.perf_counter() - start
    return module.predict_all, load_time


def check_backend_status() -> dict[str, Any]:
    """Check backend readiness without changing backend code."""
    status: dict[str, Any] = {
        "backend_connected": False,
        "models_loaded": False,
        "prediction_ready": False,
        "load_time_seconds": None,
        "error": None,
    }
    try:
        predict_func, load_time = load_backend_predictor()
        status["backend_connected"] = True
        status["models_loaded"] = True
        status["prediction_ready"] = callable(predict_func)
        status["load_time_seconds"] = round(load_time, 2)
    except Exception as exc:  # pragma: no cover - user-facing status path
        status["error"] = str(exc)
    return status


@st.cache_data(show_spinner=False)
def load_dataset_preview() -> pd.DataFrame:
    """Load a lightweight preview of the merged dataset."""
    return pd.read_csv(DATASET_PATH, nrows=5000)


def run_prediction(
    day: int,
    latitude: float,
    longitude: float,
    max_temp: float,
    min_temp: float,
) -> dict[str, Any]:
    """Execute the protected backend prediction function and format the result."""
    predict_func, _ = load_backend_predictor()
    started = time.perf_counter()
    backend_result = predict_func(day, latitude, longitude, max_temp, min_temp)
    duration = time.perf_counter() - started

    result = {
        "rainfall": float(backend_result["rainfall"]),
        "max_temperature": float(backend_result["max_temperature"]),
        "min_temperature": float(backend_result["min_temperature"]),
        "confidence": estimated_confidence(day, latitude, longitude),
        "status": "Prediction Successful",
        "elapsed_ms": round(duration * 1000, 1),
    }
    return result


def append_prediction_history(inputs: dict[str, Any], result: dict[str, Any]) -> None:
    """Store a prediction in session history for analytics and export."""
    history = st.session_state.get("prediction_history", [])
    history.append(prediction_to_record(inputs, result))
    st.session_state.prediction_history = history[-20:]

"""Shared utility helpers for validation, formatting, and exports."""

from __future__ import annotations

from datetime import datetime
from typing import Any

import pandas as pd

from frontend.constants import INDIA_BOUNDS


def validate_inputs(
    day: int,
    latitude: float,
    longitude: float,
    max_temp: float,
    min_temp: float,
) -> list[str]:
    """Validate prediction inputs and return user-friendly error messages."""
    errors: list[str] = []
    if not 1 <= day <= 365:
        errors.append("Day must be between 1 and 365.")
    if not INDIA_BOUNDS["min_lat"] <= latitude <= INDIA_BOUNDS["max_lat"]:
        errors.append("Latitude must be within India's supported climate grid.")
    if not INDIA_BOUNDS["min_lon"] <= longitude <= INDIA_BOUNDS["max_lon"]:
        errors.append("Longitude must be within India's supported climate grid.")
    if not -5 <= min_temp <= 45:
        errors.append("Minimum temperature must be in a realistic climate range.")
    if not 0 <= max_temp <= 55:
        errors.append("Maximum temperature must be in a realistic climate range.")
    if min_temp > max_temp:
        errors.append("Minimum temperature cannot be greater than maximum temperature.")
    return errors


def format_prediction_value(value: float, unit: str) -> str:
    """Format a numeric prediction with a unit."""
    return f"{value:.2f} {unit}"


def estimated_confidence(day: int, latitude: float, longitude: float) -> float:
    """Create a clearly-labeled heuristic confidence score."""
    day_center_factor = 1 - abs(day - 182.5) / 182.5
    lat_center = (INDIA_BOUNDS["min_lat"] + INDIA_BOUNDS["max_lat"]) / 2
    lon_center = (INDIA_BOUNDS["min_lon"] + INDIA_BOUNDS["max_lon"]) / 2
    lat_factor = 1 - min(abs(latitude - lat_center) / 18.0, 1)
    lon_factor = 1 - min(abs(longitude - lon_center) / 18.0, 1)
    confidence = (0.45 * day_center_factor) + (0.30 * lat_factor) + (0.25 * lon_factor)
    return round(max(0.55, min(confidence, 0.94)) * 100, 1)


def prediction_to_record(inputs: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    """Combine prediction inputs and outputs into one exportable record."""
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "day": inputs["day"],
        "latitude": inputs["latitude"],
        "longitude": inputs["longitude"],
        "max_temp_input": inputs["max_temp"],
        "min_temp_input": inputs["min_temp"],
        "predicted_rainfall": result["rainfall"],
        "predicted_max_temperature": result["max_temperature"],
        "predicted_min_temperature": result["min_temperature"],
        "estimated_confidence": result["confidence"],
    }


def dataframe_to_csv_bytes(df: pd.DataFrame) -> bytes:
    """Convert a dataframe to UTF-8 CSV bytes."""
    return df.to_csv(index=False).encode("utf-8")

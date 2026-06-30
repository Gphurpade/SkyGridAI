"""Simulation utilities for a clearly-labeled 7-day scenario forecast."""

from __future__ import annotations

import pandas as pd


def build_simulated_forecast(day: int, result: dict[str, float]) -> pd.DataFrame:
    """Create a 7-day simulation derived from one prediction result."""
    rows = []
    for offset in range(7):
        rainfall_factor = 1 + ((offset - 3) * 0.04)
        warming = (offset - 3) * 0.35
        rows.append(
            {
                "Day": min(day + offset, 365),
                "Simulated Rainfall (mm)": round(max(result["rainfall"] * rainfall_factor, 0), 2),
                "Simulated Max Temp (°C)": round(result["max_temperature"] + warming, 2),
                "Simulated Min Temp (°C)": round(result["min_temperature"] + (warming * 0.8), 2),
            }
        )
    return pd.DataFrame(rows)

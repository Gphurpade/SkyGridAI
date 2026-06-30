"""Centralized configuration for the SkyGridAI frontend."""

from __future__ import annotations

from pathlib import Path

APP_NAME = "SkyGridAI"
TAGLINE = "AI Powered Climate Digital Twin"
VERSION = "1.0.0"
HACKATHON_NAME = "Artificial Intelligence for Climate Intelligence"
DESCRIPTION = (
    "Predicting rainfall and temperature using Artificial Intelligence "
    "and IMD climate datasets."
)

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "frontend" / "assets"
OUTPUT_DIR = BASE_DIR / "output"
HEATMAP_DIR = OUTPUT_DIR / "heatmaps"
DATASET_PATH = OUTPUT_DIR / "csv" / "merged_all_days.csv"
LOGO_PATH = ASSETS_DIR / "skygrid_logo_symbol.png"
WORDMARK_PATH = ASSETS_DIR / "skygrid_logo_wordmark.png"

INDIA_BOUNDS = {
    "min_lat": 6.0,
    "max_lat": 38.8,
    "min_lon": 66.0,
    "max_lon": 100.5,
}
INDIA_CENTER = {"lat": 22.9734, "lon": 78.6569}

DEFAULT_INPUTS = {
    "day": 120,
    "latitude": 19.0760,
    "longitude": 72.8777,
    "max_temp": 32.0,
    "min_temp": 25.0,
}

SAMPLE_CITIES = {
    "Mumbai": {"lat": 19.0760, "lon": 72.8777, "day": 180, "max_temp": 31.0, "min_temp": 26.0},
    "Delhi": {"lat": 28.6139, "lon": 77.2090, "day": 150, "max_temp": 38.0, "min_temp": 28.0},
    "Chennai": {"lat": 13.0827, "lon": 80.2707, "day": 220, "max_temp": 34.0, "min_temp": 27.0},
    "Bengaluru": {"lat": 12.9716, "lon": 77.5946, "day": 200, "max_temp": 28.0, "min_temp": 21.0},
    "Kolkata": {"lat": 22.5726, "lon": 88.3639, "day": 210, "max_temp": 33.0, "min_temp": 27.0},
    "Nagpur": {"lat": 21.1458, "lon": 79.0882, "day": 170, "max_temp": 36.0, "min_temp": 27.0},
    "Pune": {"lat": 18.5204, "lon": 73.8567, "day": 190, "max_temp": 30.0, "min_temp": 23.0},
}

NAV_ITEMS = [
    "Dashboard",
    "Prediction",
    "India Map",
    "Analytics",
    "Heatmaps",
    "Forecast",
    "AI Models",
    "Dataset",
    "Settings",
    "About",
]

HEATMAP_FILES = {
    "Rainfall Heatmap": HEATMAP_DIR / "day1_heatmap_v2.png",
    "Rainfall Heatmap (Alt)": HEATMAP_DIR / "day1_heatmap.png",
    "Max Temperature Heatmap": HEATMAP_DIR / "max_temp_day1.png",
    "Min Temperature Heatmap": HEATMAP_DIR / "min_temp_day1.png",
}

THEMES = {
    "light": {
        "background": "#f4f8fb",
        "surface": "rgba(255, 255, 255, 0.88)",
        "surface_strong": "#ffffff",
        "text": "#0b1f3a",
        "muted": "#54657d",
        "border": "rgba(11, 31, 58, 0.09)",
        "primary": "#0c4ea3",
        "secondary": "#1187d8",
        "accent": "#1ca874",
        "warning": "#f97316",
        "danger": "#dc2626",
        "hero_a": "#deefff",
        "hero_b": "#e7fcf5",
    },
    "dark": {
        "background": "#081321",
        "surface": "rgba(11, 24, 42, 0.84)",
        "surface_strong": "#0c1b31",
        "text": "#e5eef8",
        "muted": "#97aec6",
        "border": "rgba(148, 163, 184, 0.14)",
        "primary": "#2c7be5",
        "secondary": "#19b9da",
        "accent": "#27c486",
        "warning": "#fb923c",
        "danger": "#f87171",
        "hero_a": "#0d2a57",
        "hero_b": "#0c3a3d",
    },
}

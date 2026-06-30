"""Reusable card renderers for metrics and information sections."""

from __future__ import annotations

import streamlit as st

from frontend.utils import format_prediction_value


def render_prediction_cards(result: dict | None) -> None:
    """Render the three primary prediction cards."""
    st.markdown('<div class="section-title">AI Prediction Cards</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-copy">Live values returned by the existing backend models.</div>',
        unsafe_allow_html=True,
    )
    cols = st.columns(3)
    cards = [
        ("Rainfall", "Predicted rainfall for the selected conditions", "mm", "metric-gradient-rain", "🌧", "Rainfall layer ready"),
        ("Maximum Temperature", "Predicted daytime temperature", "°C", "metric-gradient-max", "☀", "Daytime thermal intensity"),
        ("Minimum Temperature", "Predicted nighttime temperature", "°C", "metric-gradient-min", "❄", "Nighttime cooling pattern"),
    ]
    values = [
        result["rainfall"] if result else None,
        result["max_temperature"] if result else None,
        result["min_temperature"] if result else None,
    ]

    for col, (title, desc, unit, class_name, icon, mini), value in zip(cols, cards, values):
        display_value = "No prediction yet" if value is None else format_prediction_value(value, unit)
        col.markdown(
            f"""
            <div class="app-card metric-card {class_name}">
                <div class="metric-row">
                    <div class="metric-label">{title}</div>
                    <div class="metric-icon">{icon}</div>
                </div>
                <div class="metric-value">{display_value}</div>
                <div class="metric-desc">{desc}</div>
                <div class="metric-mini" style="margin-top:0.85rem;">{mini}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_status_cards(status: dict) -> None:
    """Render small backend status indicators."""
    cols = st.columns(3)
    items = [
        ("Backend Status", "Connected" if status.get("backend_connected") else "Offline", "Live Python backend bridge"),
        ("Model Status", "Loaded Successfully" if status.get("models_loaded") else "Unavailable", "Random forest models available"),
        ("Prediction API", "Ready" if status.get("prediction_ready") else "Not Ready", "Protected predict_all() endpoint"),
    ]
    for col, (label, value, description) in zip(cols, items):
        col.markdown(
            f"""
            <div class="app-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value" style="font-size:1.65rem;">{value}</div>
                <div class="metric-desc">{description}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_info_grid(items: list[dict[str, str]], columns: int = 3) -> None:
    """Render a reusable information card grid."""
    cols = st.columns(columns)
    for index, item in enumerate(items):
        cols[index % columns].markdown(
            f"""
            <div class="app-card">
                <div class="metric-label">{item["title"]}</div>
                <div class="metric-value" style="font-size:1.35rem;">{item["value"]}</div>
                <div class="metric-desc">{item["description"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

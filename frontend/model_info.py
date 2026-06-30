"""Model and backend architecture presentation."""

from __future__ import annotations

import streamlit as st

from frontend.cards import render_info_grid


def render_model_info(status: dict) -> None:
    """Render model architecture and backend readiness details."""
    items = [
        {
            "title": "Rainfall Model",
            "value": "Random Forest Regressor",
            "description": "Consumes Day, Latitude, Longitude, MaxTemp, and MinTemp.",
        },
        {
            "title": "Temperature Models",
            "value": "Random Forest Regressors",
            "description": "Consume Day, Latitude, Longitude, and predicted Rainfall.",
        },
        {
            "title": "Prediction Pipeline",
            "value": "predict_all()",
            "description": "Frontend calls the existing backend exactly once through one cached wrapper.",
        },
    ]
    st.markdown('<div class="section-title">AI Models & Pipeline</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-copy">A concise view of the current machine learning architecture already implemented in the backend.</div>',
        unsafe_allow_html=True,
    )
    render_info_grid(items)

    if status.get("backend_connected"):
        st.success(
            "Backend Connected | Models Loaded | "
            f"Initial load time: {status.get('load_time_seconds', 'n/a')} seconds"
        )
    else:
        st.error(f"Backend unavailable: {status.get('error', 'Unknown error')}")

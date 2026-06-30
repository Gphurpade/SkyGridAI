"""Theme and session configuration helpers."""

from __future__ import annotations

import streamlit as st

from frontend.constants import DEFAULT_INPUTS, THEMES


def initialize_session() -> None:
    """Initialize persistent session state for the app."""
    st.session_state.setdefault("theme_mode", "light")
    st.session_state.setdefault("selected_page", "Dashboard")
    st.session_state.setdefault("prediction_result", None)
    st.session_state.setdefault("prediction_history", [])
    st.session_state.setdefault("forecast_rows", [])
    st.session_state.setdefault("backend_status", {})
    st.session_state.setdefault("map_click", None)
    st.session_state.setdefault("selected_city", "Mumbai")
    st.session_state.setdefault("input_day", DEFAULT_INPUTS["day"])
    st.session_state.setdefault("input_latitude", DEFAULT_INPUTS["latitude"])
    st.session_state.setdefault("input_longitude", DEFAULT_INPUTS["longitude"])
    st.session_state.setdefault("input_max_temp", DEFAULT_INPUTS["max_temp"])
    st.session_state.setdefault("input_min_temp", DEFAULT_INPUTS["min_temp"])


def get_theme() -> dict[str, str]:
    """Return the active theme tokens."""
    return THEMES[st.session_state.get("theme_mode", "light")]


def toggle_theme() -> None:
    """Toggle light and dark mode."""
    st.session_state.theme_mode = (
        "dark" if st.session_state.get("theme_mode") == "light" else "light"
    )

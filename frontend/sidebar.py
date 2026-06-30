"""Sidebar layout and navigation for SkyGridAI."""

from __future__ import annotations

import base64

import streamlit as st

from frontend.constants import APP_NAME, HACKATHON_NAME, LOGO_PATH, NAV_ITEMS, TAGLINE, VERSION
from frontend.theme import toggle_theme


def render_sidebar(status: dict) -> str:
    """Render sidebar navigation and project status."""
    with st.sidebar:
        logo_markup = ""
        if LOGO_PATH.exists():
            logo_data = base64.b64encode(LOGO_PATH.read_bytes()).decode("utf-8")
            logo_markup = f'<img src="data:image/png;base64,{logo_data}" alt="SkyGridAI logo" />'

        st.markdown(
            f"""
            <div class="sidebar-brand">
                <div class="sidebar-brand-row">
                    {logo_markup}
                    <div>
                        <div class="sidebar-title">{APP_NAME}</div>
                        <div class="sidebar-subtitle">{TAGLINE}</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.caption(f"Version {VERSION}")

        if st.button("Toggle Light / Dark"):
            toggle_theme()
            st.rerun()

        st.markdown('<div class="sidebar-section-label">Navigation</div>', unsafe_allow_html=True)
        selected = st.radio(
            "Go to section",
            NAV_ITEMS,
            index=NAV_ITEMS.index(st.session_state.get("selected_page", "Dashboard")),
            label_visibility="collapsed",
        )
        st.session_state.selected_page = selected

        st.markdown('<div class="sidebar-section-label">Platform Status</div>', unsafe_allow_html=True)
        status_rows = [
            ("Backend", "Connected" if status.get("backend_connected") else "Offline"),
            ("Models", "Loaded Successfully" if status.get("models_loaded") else "Unavailable"),
            ("Prediction API", "Ready" if status.get("prediction_ready") else "Pending"),
        ]
        for label, value in status_rows:
            st.markdown(
                f"""
                <div class="sidebar-stat">
                    <div class="metric-label">{label}</div>
                    <div class="metric-desc" style="font-size:0.95rem; color:var(--text); font-weight:700;">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown('<div class="sidebar-section-label">Project</div>', unsafe_allow_html=True)
        st.write(HACKATHON_NAME)
        st.write("Dataset Source: India Meteorological Department")
        st.write("Theme: Session-persistent light/dark mode")
        return selected

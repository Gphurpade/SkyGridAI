"""Footer renderer for the Streamlit app."""

from __future__ import annotations

import streamlit as st

from frontend.constants import APP_NAME, HACKATHON_NAME, TAGLINE, VERSION


def render_footer() -> None:
    """Render the shared application footer."""
    st.markdown(
        f"""
        <div class="app-card footer-wrap">
            <div class="footer-grid">
                <div>
                    <div class="metric-label">{APP_NAME}</div>
                    <div class="metric-value" style="font-size:1.45rem; margin-top:0.25rem;">{TAGLINE}</div>
                    <div class="small-note">{HACKATHON_NAME} | Version {VERSION}</div>
                </div>
                <div class="footer-meta">
                    <span class="status-pill pill-ok">IMD Dataset</span>
                    <span class="status-pill pill-ok">Python</span>
                    <span class="status-pill pill-ok">Streamlit</span>
                    <span class="status-pill pill-warn">GitHub Placeholder</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

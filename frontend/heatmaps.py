"""Heatmap display helpers using existing backend-generated images."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from frontend.constants import HEATMAP_FILES


def render_heatmaps() -> None:
    """Render available heatmap assets from the output folder."""
    st.markdown('<div class="section-title">Heatmap Visualizations</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-copy">These visualizations are loaded from the existing backend output folder.</div>',
        unsafe_allow_html=True,
    )
    labels = [label for label, path in HEATMAP_FILES.items() if Path(path).exists()]
    if not labels:
        st.error("No heatmap assets were found in output/heatmaps.")
        return

    selected = st.selectbox("Heatmap Layer", labels, key="heatmap_selector")
    image_path = HEATMAP_FILES[selected]
    current_index = labels.index(selected)
    control_cols = st.columns([1, 1, 1.2])
    if control_cols[0].button("Previous Layer", disabled=current_index == 0):
        st.session_state.heatmap_selector = labels[current_index - 1]
        st.rerun()
    if control_cols[1].button("Next Layer", disabled=current_index == len(labels) - 1):
        st.session_state.heatmap_selector = labels[current_index + 1]
        st.rerun()
    control_cols[2].download_button(
        "Download Heatmap",
        data=Path(image_path).read_bytes(),
        file_name=Path(image_path).name,
        mime="image/png",
    )
    st.markdown('<div class="app-card heatmap-card">', unsafe_allow_html=True)
    st.image(str(image_path), use_container_width=True, caption=selected)
    st.markdown("</div>", unsafe_allow_html=True)

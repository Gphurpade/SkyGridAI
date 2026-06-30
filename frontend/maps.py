"""Interactive India map components."""

from __future__ import annotations

import folium
import streamlit as st
from folium.plugins import Fullscreen
from streamlit_folium import st_folium

from frontend.constants import INDIA_BOUNDS, INDIA_CENTER


def render_india_map(latitude: float, longitude: float) -> tuple[float | None, float | None]:
    """Render a Folium map and return clicked coordinates when available."""
    st.markdown('<div class="section-title">Interactive India Map</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-copy">Click on the map to update latitude and longitude with a reliable Streamlit and Folium workflow.</div>',
        unsafe_allow_html=True,
    )

    fmap = folium.Map(
        location=[latitude or INDIA_CENTER["lat"], longitude or INDIA_CENTER["lon"]],
        zoom_start=4.7,
        tiles="CartoDB positron",
        control_scale=True,
    )
    Fullscreen(position="topright").add_to(fmap)
    fmap.fit_bounds(
        [
            [INDIA_BOUNDS["min_lat"], INDIA_BOUNDS["min_lon"]],
            [INDIA_BOUNDS["max_lat"], INDIA_BOUNDS["max_lon"]],
        ]
    )
    folium.CircleMarker(
        [latitude, longitude],
        radius=12,
        weight=2,
        color="#0c4ea3",
        fill=True,
        fill_color="#11b5d8",
        fill_opacity=0.9,
        tooltip=f"Selected location: {latitude:.3f}, {longitude:.3f}",
    ).add_to(fmap)

    map_data = st_folium(fmap, width=None, height=520, returned_objects=["last_clicked"])
    clicked = map_data.get("last_clicked") if map_data else None
    if clicked:
        return clicked["lat"], clicked["lng"]
    return None, None

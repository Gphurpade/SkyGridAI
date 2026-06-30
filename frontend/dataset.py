"""Dataset metadata and preview sections."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from frontend.cards import render_info_grid


def render_dataset_section(dataset: pd.DataFrame) -> None:
    """Render dataset information cards and a preview table."""
    info_items = [
        {
            "title": "Dataset Source",
            "value": "IMD",
            "description": "India Meteorological Department climate grids used by the backend pipeline.",
        },
        {
            "title": "Coverage",
            "value": "365 Days",
            "description": "Merged all-day dataset produced by the protected backend merge pipeline.",
        },
        {
            "title": "Variables",
            "value": "Rainfall, MaxTemp, MinTemp",
            "description": "Inputs and targets preserved exactly as the backend models expect them.",
        },
    ]
    st.markdown('<div class="section-title">Dataset Intelligence</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-copy">Structured metadata for the historical climate grids currently driving predictions.</div>',
        unsafe_allow_html=True,
    )
    render_info_grid(info_items)

    summary = [
        {"title": "Rows Previewed", "value": f"{len(dataset):,}", "description": "Lightweight sample loaded for dashboard analytics."},
        {"title": "Latitude Range", "value": f"{dataset['Latitude'].min():.2f} to {dataset['Latitude'].max():.2f}", "description": "Spatial extent covered in the merged climate grid."},
        {"title": "Longitude Range", "value": f"{dataset['Longitude'].min():.2f} to {dataset['Longitude'].max():.2f}", "description": "Longitude extent in the merged dataset sample."},
        {"title": "Grid Resolution", "value": "0.25° / 1.0°", "description": "Rainfall and temperature grids are preserved from the backend mapping process."},
        {"title": "Training Samples", "value": "Merged Multi-Day", "description": "Served from the generated all-day merged CSV without changing the training pipeline."},
        {"title": "Update Year", "value": "2025", "description": "Current source files in the repository are the 2025 climate grids."},
    ]
    render_info_grid(summary)
    st.dataframe(dataset.head(25), use_container_width=True, hide_index=True)

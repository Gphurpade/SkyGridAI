"""Plotly charts for SkyGridAI analytics."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots


def _axis_style() -> dict:
    """Return axis styling based on the active theme."""
    dark = st.session_state.get("theme_mode") == "dark"
    return {
        "showgrid": True,
        "gridcolor": "rgba(148, 163, 184, 0.16)" if dark else "rgba(11, 31, 58, 0.08)",
        "zeroline": False,
        "color": "#dbe7f5" if dark else "#17304e",
    }


def _layout_base(height: int, title: str) -> dict:
    """Return a consistent layout block for Plotly charts."""
    dark = st.session_state.get("theme_mode") == "dark"
    return {
        "title": title,
        "height": height,
        "margin": dict(l=20, r=20, t=56, b=20),
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {"color": "#dbe7f5" if dark else "#17304e"},
        "legend": {
            "bgcolor": "rgba(0,0,0,0)",
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "x": 0,
        },
    }


def create_gauge_chart(title: str, value: float, min_value: float, max_value: float, color: str) -> go.Figure:
    """Create a compact gauge indicator."""
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            title={"text": title},
            gauge={
                "axis": {"range": [min_value, max_value]},
                "bar": {"color": color},
                "bgcolor": "rgba(0,0,0,0)",
                "steps": [
                    {"range": [min_value, (min_value + max_value) / 2], "color": "rgba(148, 163, 184, 0.18)"},
                    {"range": [(min_value + max_value) / 2, max_value], "color": "rgba(56, 189, 248, 0.16)"},
                ],
            },
        )
    )
    fig.update_layout(**_layout_base(250, title))
    return fig


def create_prediction_comparison(result: dict) -> go.Figure:
    """Create a bar comparison chart for the current prediction."""
    fig = go.Figure()
    fig.add_bar(
        x=["Rainfall", "Max Temp", "Min Temp"],
        y=[result["rainfall"], result["max_temperature"], result["min_temperature"]],
        marker_color=["#0ea5e9", "#f97316", "#06b6d4"],
        text=[f'{result["rainfall"]:.2f}', f'{result["max_temperature"]:.2f}', f'{result["min_temperature"]:.2f}'],
        textposition="auto",
    )
    fig.update_layout(**_layout_base(330, "Prediction Summary"), yaxis_title="Predicted Value")
    fig.update_yaxes(**_axis_style())
    return fig


def create_history_chart(history_df: pd.DataFrame) -> go.Figure:
    """Create a multi-series timeline for recent predictions."""
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(
            x=history_df["timestamp"],
            y=history_df["predicted_rainfall"],
            mode="lines+markers",
            name="Rainfall (mm)",
            line=dict(color="#0ea5e9", width=3),
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=history_df["timestamp"],
            y=history_df["predicted_max_temperature"],
            mode="lines+markers",
            name="Max Temp (°C)",
            line=dict(color="#f97316", width=3),
        ),
        secondary_y=True,
    )
    fig.add_trace(
        go.Scatter(
            x=history_df["timestamp"],
            y=history_df["predicted_min_temperature"],
            mode="lines+markers",
            name="Min Temp (°C)",
            line=dict(color="#06b6d4", width=3),
        ),
        secondary_y=True,
    )
    fig.update_layout(**_layout_base(360, "Prediction Timeline"))
    fig.update_xaxes(**_axis_style())
    fig.update_yaxes(title_text="Rainfall (mm)", secondary_y=False, **_axis_style())
    fig.update_yaxes(title_text="Temperature (°C)", secondary_y=True, **_axis_style())
    return fig


def create_distribution_chart(dataset: pd.DataFrame) -> go.Figure:
    """Create a three-panel distribution overview from historical data."""
    fig = go.Figure()
    fig.add_histogram(x=dataset["Rainfall"], nbinsx=40, name="Rainfall", opacity=0.7, marker_color="#0ea5e9")
    fig.add_histogram(x=dataset["MaxTemp"], nbinsx=40, name="Max Temp", opacity=0.6, marker_color="#f97316")
    fig.add_histogram(x=dataset["MinTemp"], nbinsx=40, name="Min Temp", opacity=0.6, marker_color="#06b6d4")
    fig.update_layout(**_layout_base(360, "Historical Distribution Snapshot"), barmode="overlay")
    fig.update_xaxes(**_axis_style())
    fig.update_yaxes(**_axis_style())
    return fig

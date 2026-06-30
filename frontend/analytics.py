"""Higher-level analytics sections built from prediction results and history."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from frontend.charts import (
    create_distribution_chart,
    create_gauge_chart,
    create_history_chart,
    create_prediction_comparison,
)


def render_analytics(result: dict | None, history: list[dict], dataset: pd.DataFrame) -> None:
    """Render analytics blocks and charts."""
    st.markdown('<div class="section-title">Charts & Analytics</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-copy">Interactive analytics update after each backend prediction.</div>',
        unsafe_allow_html=True,
    )

    if not result:
        st.info("No prediction yet. Run a scenario to unlock analytics, gauges, and forecast simulation.")
        return

    gauge_cols = st.columns(3)
    gauge_cols[0].plotly_chart(create_gauge_chart("Rainfall Gauge", result["rainfall"], 0, 300, "#0ea5e9"), use_container_width=True)
    gauge_cols[1].plotly_chart(create_gauge_chart("Max Temperature", result["max_temperature"], 0, 50, "#f97316"), use_container_width=True)
    gauge_cols[2].plotly_chart(create_gauge_chart("Min Temperature", result["min_temperature"], -5, 40, "#06b6d4"), use_container_width=True)

    chart_cols = st.columns([1.2, 1])
    chart_cols[0].plotly_chart(create_prediction_comparison(result), use_container_width=True)
    chart_cols[1].plotly_chart(create_distribution_chart(dataset), use_container_width=True)

    if history:
        history_df = pd.DataFrame(history)
        st.plotly_chart(create_history_chart(history_df), use_container_width=True)

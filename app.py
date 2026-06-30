"""Main Streamlit application for the SkyGridAI frontend."""

from __future__ import annotations

import base64

import pandas as pd
import streamlit as st

from frontend.analytics import render_analytics
from frontend.cards import render_prediction_cards, render_status_cards
from frontend.constants import (
    APP_NAME,
    DEFAULT_INPUTS,
    DESCRIPTION,
    LOGO_PATH,
    SAMPLE_CITIES,
    TAGLINE,
    WORDMARK_PATH,
)
from frontend.dataset import render_dataset_section
from frontend.footer import render_footer
from frontend.forecast import build_simulated_forecast
from frontend.heatmaps import render_heatmaps
from frontend.maps import render_india_map
from frontend.model_info import render_model_info
from frontend.prediction import (
    append_prediction_history,
    check_backend_status,
    load_dataset_preview,
    run_prediction,
)
from frontend.sidebar import render_sidebar
from frontend.styles import inject_styles
from frontend.theme import get_theme, initialize_session
from frontend.utils import dataframe_to_csv_bytes, validate_inputs


st.set_page_config(
    page_title=APP_NAME,
    page_icon="🌦",
    layout="wide",
    initial_sidebar_state="expanded",
)

initialize_session()
theme = get_theme()
inject_styles(theme)

status = check_backend_status()
st.session_state.backend_status = status
selected_page = render_sidebar(status)
dataset_preview = load_dataset_preview()


def set_sample_inputs(city_name: str) -> None:
    """Apply a sample city's inputs to session state."""
    city = SAMPLE_CITIES[city_name]
    st.session_state.input_day = city["day"]
    st.session_state.input_latitude = city["lat"]
    st.session_state.input_longitude = city["lon"]
    st.session_state.input_max_temp = city["max_temp"]
    st.session_state.input_min_temp = city["min_temp"]


def reset_dashboard() -> None:
    """Reset inputs and outputs to the default state."""
    st.session_state.prediction_result = None
    st.session_state.forecast_rows = []
    st.session_state.map_click = None
    st.session_state.input_day = DEFAULT_INPUTS["day"]
    st.session_state.input_latitude = DEFAULT_INPUTS["latitude"]
    st.session_state.input_longitude = DEFAULT_INPUTS["longitude"]
    st.session_state.input_max_temp = DEFAULT_INPUTS["max_temp"]
    st.session_state.input_min_temp = DEFAULT_INPUTS["min_temp"]


def clear_results() -> None:
    """Clear results while preserving user inputs."""
    st.session_state.prediction_result = None
    st.session_state.forecast_rows = []


def render_hero() -> None:
    """Render the main hero section."""
    symbol_markup = ""
    wordmark_markup = ""
    if LOGO_PATH.exists():
        logo_data = base64.b64encode(LOGO_PATH.read_bytes()).decode("utf-8")
        symbol_markup = (
            f'<div class="hero-logo"><img src="data:image/png;base64,{logo_data}" '
            f'alt="SkyGridAI symbol" style="width:100%;height:100%;display:block;object-fit:cover;" /></div>'
        )
    if WORDMARK_PATH.exists():
        wordmark_data = base64.b64encode(WORDMARK_PATH.read_bytes()).decode("utf-8")
        wordmark_markup = (
            f'<img class="hero-wordmark" src="data:image/png;base64,{wordmark_data}" '
            f'alt="SkyGridAI wordmark" />'
        )

    title_block = wordmark_markup if wordmark_markup else f'<div class="hero-title">{APP_NAME}</div>'
    st.markdown(
        f"""
        <div class="hero-panel">
            <div class="hero-grid">
                <div>
                    <div class="hero-brand">
                        {symbol_markup}
                        <div>
                            <div class="hero-kicker">AI Climate Intelligence Platform</div>
                            {title_block}
                            <div class="hero-title" style="font-size:clamp(1.05rem, 1.7vw, 1.35rem); font-weight:700; margin-top:0.85rem;">{TAGLINE}</div>
                        </div>
                    </div>
                    <div class="hero-subtitle" style="margin-top:1rem;">{DESCRIPTION}</div>
                    <div style="margin-top: 1rem;">
                        <span class="status-pill pill-ok">Model Loaded</span>
                        <span class="status-pill pill-ok">Data Source IMD</span>
                        <span class="status-pill pill-warn">Forecast = Simulation</span>
                    </div>
                </div>
                <div class="hero-stats">
                    <div class="hero-stat-card">
                        <div class="hero-stat-label">Prediction Engine</div>
                        <div class="hero-stat-value">Random Forest Climate Stack</div>
                    </div>
                    <div class="hero-stat-card">
                        <div class="hero-stat-label">Backend Readiness</div>
                        <div class="hero-stat-value">{'Connected' if status.get('prediction_ready') else 'Pending'}</div>
                    </div>
                    <div class="hero-stat-card">
                        <div class="hero-stat-label">Last Updated</div>
                        <div class="hero-stat-value">Using current repo outputs and models</div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_prediction_panel() -> None:
    """Render the main input form, backend prediction call, and exports."""
    left, right = st.columns([1, 1.15], gap="large")
    with left:
        st.markdown('<div class="app-card section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Prediction Studio</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-copy">Use manual inputs, sample city presets, or map clicks to generate backend predictions.</div>',
            unsafe_allow_html=True,
        )
        selected_city = st.selectbox("Sample Indian city", list(SAMPLE_CITIES.keys()), key="city_selector")
        action_cols = st.columns(3)
        if action_cols[0].button("Use Sample Data"):
            set_sample_inputs(selected_city)
            st.success(f"Loaded sample scenario for {selected_city}.")
        if action_cols[1].button("Reset Inputs"):
            reset_dashboard()
            st.success("Inputs and dashboard state were reset.")
        if action_cols[2].button("Clear Results"):
            clear_results()
            st.info("Prediction outputs cleared.")

        st.session_state.input_day = st.slider(
            "Day",
            min_value=1,
            max_value=365,
            value=int(st.session_state.input_day),
            help="Select a day between 1 and 365.",
        )
        temp_cols = st.columns(2)
        st.session_state.input_latitude = temp_cols[0].number_input(
            "Latitude",
            value=float(st.session_state.input_latitude),
            step=0.1,
            format="%.4f",
            help="Latitude within India's climate grid.",
        )
        st.session_state.input_longitude = temp_cols[1].number_input(
            "Longitude",
            value=float(st.session_state.input_longitude),
            step=0.1,
            format="%.4f",
            help="Longitude within India's climate grid.",
        )
        st.session_state.input_max_temp = temp_cols[0].number_input(
            "Maximum Temperature",
            value=float(st.session_state.input_max_temp),
            step=0.5,
            format="%.2f",
            help="Maximum daily temperature in degrees Celsius.",
        )
        st.session_state.input_min_temp = temp_cols[1].number_input(
            "Minimum Temperature",
            value=float(st.session_state.input_min_temp),
            step=0.5,
            format="%.2f",
            help="Minimum daily temperature in degrees Celsius.",
        )

        errors = validate_inputs(
            st.session_state.input_day,
            st.session_state.input_latitude,
            st.session_state.input_longitude,
            st.session_state.input_max_temp,
            st.session_state.input_min_temp,
        )
        if errors:
            for error in errors:
                st.warning(error)

        if st.button("Run AI Prediction", type="primary", disabled=bool(errors) or not status.get("prediction_ready")):
            with st.spinner("Prediction in progress... loading backend models and running inference."):
                result = run_prediction(
                    st.session_state.input_day,
                    st.session_state.input_latitude,
                    st.session_state.input_longitude,
                    st.session_state.input_max_temp,
                    st.session_state.input_min_temp,
                )
            st.session_state.prediction_result = result
            st.session_state.forecast_rows = build_simulated_forecast(st.session_state.input_day, result).to_dict("records")
            append_prediction_history(
                {
                    "day": st.session_state.input_day,
                    "latitude": st.session_state.input_latitude,
                    "longitude": st.session_state.input_longitude,
                    "max_temp": st.session_state.input_max_temp,
                    "min_temp": st.session_state.input_min_temp,
                },
                result,
            )
            st.success("Prediction successful. Cards, analytics, and forecast have been updated.")

        result = st.session_state.prediction_result
        if result:
            summary_df = pd.DataFrame(st.session_state.prediction_history)
            st.download_button(
                "Export Prediction CSV",
                data=dataframe_to_csv_bytes(summary_df),
                file_name="skygridai_predictions.csv",
                mime="text/csv",
            )
            st.caption(
                f"Estimated confidence: {result['confidence']}% | "
                f"Backend inference time: {result['elapsed_ms']} ms"
            )
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="app-card map-card">', unsafe_allow_html=True)
        clicked_lat, clicked_lon = render_india_map(
            st.session_state.input_latitude,
            st.session_state.input_longitude,
        )
        if clicked_lat is not None and clicked_lon is not None:
            st.session_state.input_latitude = round(clicked_lat, 4)
            st.session_state.input_longitude = round(clicked_lon, 4)
            st.success("Map click captured. Latitude and longitude fields were updated.")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


def render_forecast_section() -> None:
    """Render the simulated forecast section."""
    st.markdown('<div class="section-title">Forecast & Simulation</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-copy">This 7-day view is a simulation derived from the single-scenario backend prediction. It is not a true backend forecast model.</div>',
        unsafe_allow_html=True,
    )
    if not st.session_state.forecast_rows:
        st.info("Run a prediction to generate the 7-day simulation.")
        return
    forecast_df = pd.DataFrame(st.session_state.forecast_rows)
    search = st.text_input("Search forecast day", placeholder="Type a day number like 121")
    if search.strip():
        forecast_df = forecast_df[forecast_df["Day"].astype(str).str.contains(search.strip(), na=False)]
    toolbar_cols = st.columns([1.2, 1])
    toolbar_cols[0].markdown(
        '<div class="small-note">Simulation data grid derived from one backend scenario.</div>',
        unsafe_allow_html=True,
    )
    toolbar_cols[1].download_button(
        "Download Forecast CSV",
        data=dataframe_to_csv_bytes(forecast_df),
        file_name="skygridai_forecast_simulation.csv",
        mime="text/csv",
    )
    st.dataframe(forecast_df, use_container_width=True, hide_index=True)
    st.line_chart(
        forecast_df.set_index("Day")[
            ["Simulated Rainfall (mm)", "Simulated Max Temp (°C)", "Simulated Min Temp (°C)"]
        ],
        use_container_width=True,
    )


def render_dashboard() -> None:
    """Render the primary all-in-one dashboard page."""
    render_hero()
    st.write("")
    render_status_cards(status)
    st.write("")
    render_prediction_panel()
    st.write("")
    render_prediction_cards(st.session_state.prediction_result)
    st.write("")
    render_analytics(
        st.session_state.prediction_result,
        st.session_state.prediction_history,
        dataset_preview,
    )
    st.write("")
    render_heatmaps()
    st.write("")
    render_forecast_section()
    st.write("")
    render_dataset_section(dataset_preview)
    st.write("")
    render_model_info(status)


def render_about() -> None:
    """Render the about page."""
    st.markdown('<div class="section-title">About SkyGridAI</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-copy">SkyGridAI is a climate intelligence prototype that turns an existing machine learning backend into a judge-ready decision dashboard.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="app-card">
            <p><strong>Objective:</strong> Transform historical IMD climate grids into an AI-assisted digital twin for rainfall and temperature scenario analysis.</p>
            <p><strong>Backend Architecture:</strong> Protected Python scripts parse GRD files, merge climate variables, and serve predictions through <code>predict_all()</code>.</p>
            <p><strong>Frontend Architecture:</strong> Streamlit + Plotly + Folium, organized into reusable modules with one cached backend wrapper.</p>
            <p><strong>Technology Stack:</strong> Python, Streamlit, Plotly, Folium, streamlit-folium, Pandas, NumPy, Joblib.</p>
            <p><strong>Team Section:</strong> Ready for your final team names, GitHub link, and project credits.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


if selected_page == "Dashboard":
    render_dashboard()
elif selected_page == "Prediction":
    render_prediction_panel()
    render_prediction_cards(st.session_state.prediction_result)
elif selected_page == "India Map":
    clicked_lat, clicked_lon = render_india_map(
        st.session_state.input_latitude,
        st.session_state.input_longitude,
    )
    if clicked_lat is not None and clicked_lon is not None:
        st.session_state.input_latitude = round(clicked_lat, 4)
        st.session_state.input_longitude = round(clicked_lon, 4)
        st.success("Map click captured. Coordinates updated.")
        st.rerun()
elif selected_page == "Analytics":
    render_analytics(st.session_state.prediction_result, st.session_state.prediction_history, dataset_preview)
elif selected_page == "Heatmaps":
    render_heatmaps()
elif selected_page == "Forecast":
    render_forecast_section()
elif selected_page == "AI Models":
    render_model_info(status)
elif selected_page == "Dataset":
    render_dataset_section(dataset_preview)
elif selected_page == "Settings":
    st.markdown('<div class="section-title">Settings</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-copy">Theme is session-persistent. Use the sidebar toggle to switch between light and dark mode. Reset and clear controls are available in the prediction panel.</div>',
        unsafe_allow_html=True,
    )
    st.info("Settings are intentionally minimal to keep the frontend reliable and fully Python-based.")
elif selected_page == "About":
    render_about()

st.write("")
render_footer()

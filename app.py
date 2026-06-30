import sys
from pathlib import Path

# Ensure the app can find packages from both the workspace venv and the SkyGrid env.
BASE_DIR = Path(__file__).resolve().parent
site_packages_candidates = [
    BASE_DIR / ".venv" / "Lib" / "site-packages",
    BASE_DIR / ".venv" / "lib" / f"python{sys.version_info.major}.{sys.version_info.minor}" / "site-packages",
    BASE_DIR / "skygrid" / "Lib" / "site-packages",
    BASE_DIR / "skygrid" / "lib" / f"python{sys.version_info.major}.{sys.version_info.minor}" / "site-packages",
]
module_search_paths = [BASE_DIR / "scripts"]

for package_path in site_packages_candidates:
    if package_path.exists():
        sys.path.insert(0, str(package_path))

for module_path in module_search_paths:
    if module_path.exists():
        sys.path.insert(0, str(module_path))

# ==========================================================
# Original Imports Continue Below
# ==========================================================

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium

# Import your existing modules
import parser as imd_parser
import predict as imd_predict

st.set_page_config(layout="wide", page_title="SkyGridAI - Digital Twin of India")

st.title(" SkyGridAI")
st.markdown("Get insights into India's weather patterns with our interactive map visualizer and predictive simulator. Explore historical data or simulate future scenarios based on your inputs.")

# ==========================================================
# Global Sidebar Configuration
# ==========================================================
st.sidebar.header("Control Panel")
selected_day = st.sidebar.slider("Select Day of Year (1-365)", min_value=1, max_value=365, value=150)
app_mode = st.sidebar.radio("Navigate Application Mode", ["Historical Grid Viewer", "What-If Simulator"])

# Cache file reading to keep the UI highly responsive
@st.cache_data
def get_cached_grids():
    try:
        rain = imd_parser.load_rainfall()
        max_t = imd_parser.load_max_temperature()
        min_t = imd_parser.load_min_temperature()
        return rain, max_t, min_t, True
    except Exception as e:
        return None, None, None, False

rain_grid, max_grid, min_grid, data_available = get_cached_grids()

# ==========================================================
# Mode 1: Historical Grid Viewer
# ==========================================================
if app_mode == "Historical Grid Viewer":
    if not data_available:
        st.error("⚠️ Unable to automatically read the .GRD files. Ensure data is correctly placed in `../data/`.")
    else:
        st.subheader(f" Historical Grid Layer: Day {selected_day}")
        
        metric = st.selectbox("Choose Weather Parameter", ["Rainfall (mm)", "Max Temperature (°C)", "Min Temperature (°C)"])
        
        if "Rainfall" in metric:
            grid_slice = rain_grid[selected_day - 1]
            lats, lons = imd_parser.rainfall_coordinates()
            color_theme = "Blues"
            label = "Rainfall (mm)"
        elif "Max" in metric:
            grid_slice = max_grid[selected_day - 1]
            lats, lons = imd_parser.temperature_coordinates()
            color_theme = "YlOrRd"
            label = "Max Temp (°C)"
        else:
            grid_slice = min_grid[selected_day - 1]
            lats, lons = imd_parser.temperature_coordinates()
            color_theme = "Thermal"
            label = "Min Temp (°C)"
            
        lon_mesh, lat_mesh = np.meshgrid(lons, lats)
        
        map_df = pd.DataFrame({
            'Latitude': lat_mesh.flatten(),
            'Longitude': lon_mesh.flatten(),
            label: grid_slice.flatten()
        }).dropna()
        
        fig = px.scatter_mapbox(
            map_df,
            lat='Latitude',
            lon='Longitude',
            color=label,
            color_continuous_scale=color_theme,
            size_max=8,
            zoom=4,
            center={"lat": 22.9734, "lon": 78.6568},
            mapbox_style="carto-positron",
            opacity=0.7,
            title=f"IMD Spatial Layout for India — {metric}"
        )
        fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, height=650)
        st.plotly_chart(fig, use_container_width=True)

# ==========================================================
# Mode 2: What-If Predictive Simulator (Clickable Map & Bounds Enforced)
# ==========================================================
else:
    st.subheader("Climate Scenario Playground")
    st.markdown("Click inside the highlighted region on the map to set your target location, then shift baseline parameters to observe impacts.")
    
    # Define exact IMD Grid Boundary coordinates for Indian Subcontinent
    IND_MIN_LAT, IND_MAX_LAT = 6.5, 38.75
    IND_MIN_LON, IND_MAX_LON = 66.5, 100.25

    # Initialize session state for coordinates so they persist between interactions
    if "target_lat" not in st.session_state:
        st.session_state.target_lat = 18.52  # Default Pune
    if "target_lon" not in st.session_state:
        st.session_state.target_lon = 73.85
        
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.markdown("###  Interactive Location Selector")
        
        # Enforce max map viewing bounds to prevent camera from drifting completely away from India
        m = folium.Map(
            location=[22.9734, 78.6568], 
            zoom_start=4,
            max_bounds=True,
            min_lat=IND_MIN_LAT - 2,
            max_lat=IND_MAX_LAT + 2,
            min_lon=IND_MIN_LON - 2,
            max_lon=IND_MAX_LON + 2
        )
        
        # Requirement 1: Highlight Allowed Workspace Region
        folium.Rectangle(
            bounds=[[IND_MIN_LAT, IND_MIN_LON], [IND_MAX_LAT, IND_MAX_LON]],
            color="#2E86C1",
            weight=2,
            fill=True,
            fill_color="#AED6F1",
            fill_opacity=0.15
        ).add_to(m)
        
        # Requirement 2: Highlight Selected Location explicitly
        folium.Marker(
            [st.session_state.target_lat, st.session_state.target_lon], 
            tooltip="Selected Coordinate Target",
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(m)
        
        folium.Circle(
            location=[st.session_state.target_lat, st.session_state.target_lon],
            radius=60000,  # 60km dynamic target highlight ring
            color="#E74C3C",
            fill=True,
            fill_color="#F1948A",
            fill_opacity=0.3
        ).add_to(m)
        
        map_data = st_folium(m, height=450, width=500)
        
        # Catch click events and evaluate parameters
        if map_data and map_data.get("last_clicked"):
            clicked_lat = map_data["last_clicked"]["lat"]
            clicked_lng = map_data["last_clicked"]["lng"]
            
            # Check if this click is unique compared to current state
            if clicked_lat != st.session_state.target_lat or clicked_lng != st.session_state.target_lon:
                # Requirement 3: Spatial filter restriction wall
                if IND_MIN_LAT <= clicked_lat <= IND_MAX_LAT and IND_MIN_LON <= clicked_lng <= IND_MAX_LON:
                    st.session_state.target_lat = clicked_lat
                    st.session_state.target_lon = clicked_lng
                    st.rerun()
                else:
                    st.error(f"⚠️ Selection Blocked! Coordinates (`{clicked_lat:.2f}N, {clicked_lng:.2f}E`) fall outside the allowable India grid region.")

    with col2:
        st.markdown(f"**Current Valid Target Point:** `{st.session_state.target_lat:.3f} N, {st.session_state.target_lon:.3f} E`")
        
        st.markdown("###  Base Settings")
        base_max = st.slider("Base Max Temperature (°C)", 15.0, 50.0, 33.0)
        base_min = st.slider("Base Min Temperature (°C)", 5.0, 35.0, 22.0)
        
        st.markdown("###  Stress Tests")
        anomaly = st.slider("Forced Hot/Cold Anomaly Shift (°C)", -5.0, 5.0, 0.0, step=0.5)
        
        adjusted_max = base_max + anomaly
        adjusted_min = base_min + anomaly
        
    st.divider()
        
    try:
        # 1. Run the Baseline Prediction (Without Anomaly)
        res_baseline = imd_predict.predict_all(
            day=selected_day,
            latitude=st.session_state.target_lat,
            longitude=st.session_state.target_lon,
            max_temp_input=base_max,
            min_temp_input=base_min
        )

        # 2. Run the Adjusted Prediction (With Anomaly)
        res_adjusted = imd_predict.predict_all(
            day=selected_day,
            latitude=st.session_state.target_lat,
            longitude=st.session_state.target_lon,
            max_temp_input=adjusted_max,
            min_temp_input=adjusted_min
        )

        # Calculate Impacts (Deltas)
        impact_rain = res_adjusted['rainfall'] - res_baseline['rainfall']
        impact_max_t = res_adjusted['max_temperature'] - res_baseline['max_temperature']
        impact_min_t = res_adjusted['min_temperature'] - res_baseline['min_temperature']
        
        st.markdown("###  Scenario Impact Dashboard")
        st.markdown(f"Comparing Baseline vs. a **{anomaly:+.1f} °C** shift in base temperatures.")

        # Display Metrics with Deltas highlighting the impact
        m1, m2, m3 = st.columns(3)
        m1.metric(
            label="Predicted Rainfall Impact", 
            value=f"{res_adjusted['rainfall']:.2f} mm", 
            delta=f"{impact_rain:+.2f} mm"
        )
        m2.metric(
            label="Downstream Max Temp Impact", 
            value=f"{res_adjusted['max_temperature']:.2f} °C", 
            delta=f"{impact_max_t:+.2f} °C",
            delta_color="inverse" 
        )
        m3.metric(
            label="Downstream Min Temp Impact", 
            value=f"{res_adjusted['min_temperature']:.2f} °C", 
            delta=f"{impact_min_t:+.2f} °C",
            delta_color="inverse"
        )

        # Render comparison bar chart
        chart_data = pd.DataFrame({
            "Scenario": ["Baseline", "Stressed", "Baseline", "Stressed", "Baseline", "Stressed"],
            "Parameter": ["Rainfall", "Rainfall", "Max Temp", "Max Temp", "Min Temp", "Min Temp"],
            "Value": [
                res_baseline['rainfall'], res_adjusted['rainfall'],
                res_baseline['max_temperature'], res_adjusted['max_temperature'],
                res_baseline['min_temperature'], res_adjusted['min_temperature']
            ]
        })

        fig_compare = px.bar(
            chart_data, 
            x="Parameter", 
            y="Value", 
            color="Scenario", 
            barmode="group",
            title="Baseline vs. Stressed Scenario Comparison",
            color_discrete_sequence=["#1f77b4", "#d62728"]
        )
        fig_compare.update_layout(height=350, margin={"r":0,"t":40,"l":0,"b":0})
        st.plotly_chart(fig_compare, use_container_width=True)
        
    except Exception as e:
        st.info(f" Please ensure your trained `.pkl` models exist within the `../models/` directory to utilize this predictive playground. Context: {e}")
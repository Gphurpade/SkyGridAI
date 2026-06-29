"""
parser.py

Reusable parser for IMD GRD datasets.
"""

from pathlib import Path
import numpy as np

# ==========================================================
# File Paths
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

RAINFALL_FILE = BASE_DIR / "data" / "Rainfall_ind2025_rfp25.grd"
MAXTEMP_FILE = BASE_DIR / "data" / "Maxtemp_MaxT_2025.GRD"
MINTEMP_FILE = BASE_DIR / "data" / "Mintemp_MinT_2025.GRD"


# ==========================================================
# Rainfall Parser
# ==========================================================

def read_rainfall(file_path):
    DAYS = 365
    LAT = 129
    LON = 135
    MISSING_VALUE = -999.0

    file_path = Path(file_path)

    data = np.fromfile(file_path, dtype=np.float32)

    expected = DAYS * LAT * LON

    if len(data) != expected:
        raise ValueError(
            f"Expected {expected} values but found {len(data)}"
        )

    rainfall = data.reshape(DAYS, LAT, LON)

    rainfall = np.where(
        rainfall == MISSING_VALUE,
        np.nan,
        rainfall
    )

    return rainfall


# ==========================================================
# Temperature Parser
# ==========================================================

def read_temperature(file_path):

    DAYS = 365
    ROWS = 31
    COLS = 31
    MISSING_VALUE = 99.9

    file_path = Path(file_path)

    data = np.fromfile(file_path, dtype=np.float32)

    expected = DAYS * ROWS * COLS

    if len(data) != expected:
        raise ValueError(
            f"Expected {expected} values but found {len(data)}"
        )

    temperature = data.reshape(DAYS, ROWS, COLS)

    temperature = np.where(
        temperature == MISSING_VALUE,
        np.nan,
        temperature
    )

    return temperature


# ==========================================================
# Wrapper Functions
# ==========================================================

def load_rainfall():
    return read_rainfall(RAINFALL_FILE)


def load_max_temperature():
    return read_temperature(MAXTEMP_FILE)


def load_min_temperature():
    return read_temperature(MINTEMP_FILE)


# ==========================================================
# Rainfall Coordinates
# ==========================================================

def rainfall_coordinates():

    latitudes = np.arange(6.5, 38.75, 0.25)
    longitudes = np.arange(66.5, 100.25, 0.25)

    return latitudes, longitudes


# ==========================================================
# Temperature Coordinates
# ==========================================================

def temperature_coordinates():

    latitudes = np.arange(7.5, 38.5, 1.0)
    longitudes = np.arange(67.5, 98.5, 1.0)

    return latitudes, longitudes


# ==========================================================
# Nearest Temperature Grid
# ==========================================================

def nearest_temperature_index(lat, lon):

    temp_lat, temp_lon = temperature_coordinates()

    row = np.abs(temp_lat - lat).argmin()
    col = np.abs(temp_lon - lon).argmin()

    return row, col


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    print("Loading datasets...\n")

    rainfall = load_rainfall()
    max_temp = load_max_temperature()
    min_temp = load_min_temperature()

    print("Rainfall Shape :", rainfall.shape)
    print("Max Temp Shape :", max_temp.shape)
    print("Min Temp Shape :", min_temp.shape)

    print("\nParser Working Successfully!")
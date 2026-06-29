from pathlib import Path
import numpy as np
import pandas as pd

# ======================================================
# IMD Rainfall Dataset Specifications (Official)
# ======================================================

DAYS = 365
LONGITUDE_POINTS = 135
LATITUDE_POINTS = 129

START_LONGITUDE = 66.5
START_LATITUDE = 6.5

GRID_SIZE = 0.25

# ======================================================
# Read Binary File
# ======================================================

file_path = Path("../data/Rainfall_ind2025_rfp25.grd")

print("Reading IMD Rainfall Dataset...\n")

data = np.fromfile(file_path, dtype=np.float32)

print(f"Total Values : {len(data)}")

expected = DAYS * LATITUDE_POINTS * LONGITUDE_POINTS

print(f"Expected Values : {expected}")

if len(data) != expected:
    print("❌ Dataset size mismatch!")
    exit()

print("✅ Dataset size verified.\n")

# ======================================================
# Official IMD Layout
# ======================================================

daily_data = data.reshape(
    DAYS,
    LATITUDE_POINTS,
    LONGITUDE_POINTS
)

print("Dataset Shape :", daily_data.shape)

# ======================================================
# Day 1
# ======================================================

day1 = daily_data[0]

print("Day 1 Shape :", day1.shape)

# ======================================================
# Replace Missing Values
# ======================================================

day1 = np.where(day1 == -999, np.nan, day1)

# ======================================================
# Latitude & Longitude
# ======================================================

latitudes = np.arange(
    START_LATITUDE,
    START_LATITUDE + LATITUDE_POINTS * GRID_SIZE,
    GRID_SIZE
)

longitudes = np.arange(
    START_LONGITUDE,
    START_LONGITUDE + LONGITUDE_POINTS * GRID_SIZE,
    GRID_SIZE
)

# ======================================================
# Create CSV
# ======================================================

rows = []

for lat_index in range(LATITUDE_POINTS):

    for lon_index in range(LONGITUDE_POINTS):

        rows.append([
            latitudes[lat_index],
            longitudes[lon_index],
            day1[lat_index][lon_index]
        ])

df = pd.DataFrame(
    rows,
    columns=[
        "Latitude",
        "Longitude",
        "Rainfall"
    ]
)

# ======================================================
# Save CSV
# ======================================================

output_csv = Path("../output/day1_rainfall_v2.csv")

df.to_csv(output_csv, index=False)

print("\nCSV Saved Successfully!")

print(output_csv.resolve())

# ======================================================
# Statistics
# ======================================================

print("\nRainfall Statistics")

print(df["Rainfall"].describe())
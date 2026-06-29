"""
merge_data.py

Merge Rainfall + Maximum Temperature + Minimum Temperature
for Day 1 using nearest-neighbor mapping.
"""

from pathlib import Path
import pandas as pd

from parser import (
    read_rainfall,
    read_temperature,
    rainfall_coordinates,
    nearest_temperature_index,
)

# ==========================================================
# Read Datasets
# ==========================================================

print("Loading datasets...")

rainfall = read_rainfall("../data/Rainfall_ind2025_rfp25.grd")
max_temp = read_temperature("../data/Maxtemp_MaxT_2025.GRD")
min_temp = read_temperature("../data/Mintemp_MinT_2025.GRD")

print("Datasets Loaded Successfully!\n")

# ==========================================================
# Day to Process
# ==========================================================

DAY = 0  # Day 1

rain_day = rainfall[DAY]
max_day = max_temp[DAY]
min_day = min_temp[DAY]

# ==========================================================
# Coordinates
# ==========================================================

rain_latitudes, rain_longitudes = rainfall_coordinates()

# ==========================================================
# Merge
# ==========================================================

rows = []

print("Merging Day 1 Data...")

for lat_index, lat in enumerate(rain_latitudes):

    for lon_index, lon in enumerate(rain_longitudes):

        rainfall_value = rain_day[lat_index, lon_index]

        temp_row, temp_col = nearest_temperature_index(lat, lon)

        max_temperature = max_day[temp_row, temp_col]
        min_temperature = min_day[temp_row, temp_col]

        rows.append({
            "Latitude": lat,
            "Longitude": lon,
            "Rainfall": rainfall_value,
            "MaxTemp": max_temperature,
            "MinTemp": min_temperature
        })

# ==========================================================
# DataFrame
# ==========================================================

merged_df = pd.DataFrame(rows)

print("\nMerged Dataset Created!")

print("\nShape:")
print(merged_df.shape)

print("\nFirst 10 Rows:")
print(merged_df.head(10))

print("\nMissing Values:")
print(merged_df.isna().sum())

# ==========================================================
# Save CSV
# ==========================================================

output_path = Path("../output/day1_merged.csv")

merged_df.to_csv(output_path, index=False)

print("\nCSV Saved Successfully!")

print(output_path.resolve())
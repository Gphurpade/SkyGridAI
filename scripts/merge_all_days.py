"""
merge_all_days.py

Creates one merged CSV for all 365 days.
"""

from pathlib import Path
import numpy as np
import pandas as pd

from parser import (
    load_rainfall,
    load_max_temperature,
    load_min_temperature,
)

from mapping import mapping

# ==========================================================
# Load Datasets
# ==========================================================

print("Loading datasets...\n")

rainfall = load_rainfall()
max_temp = load_max_temperature()
min_temp = load_min_temperature()

print("Datasets Loaded Successfully!\n")

# ==========================================================
# Coordinates
# ==========================================================

rain_lat = np.arange(6.5, 38.75, 0.25)
rain_lon = np.arange(66.5, 100.25, 0.25)

# ==========================================================
# Output File
# ==========================================================

output_folder = Path("../output/csv")
output_folder.mkdir(parents=True, exist_ok=True)

output_file = output_folder / "merged_all_days.csv"

# Delete old file if it exists
if output_file.exists():
    output_file.unlink()

first_write = True

total_rows = 0

# ==========================================================
# Process All Days
# ==========================================================

for day in range(365):

    print(f"Processing Day {day + 1}/365")

    rows = []

    rain_day = rainfall[day]
    max_day = max_temp[day]
    min_day = min_temp[day]

    for i in range(129):

        for j in range(135):

            rain_value = rain_day[i, j]

            temp_i, temp_j = mapping[(i, j)]

            max_value = max_day[temp_i, temp_j]
            min_value = min_day[temp_i, temp_j]

            # Skip invalid cells
            if (
                np.isnan(rain_value)
                or np.isnan(max_value)
                or np.isnan(min_value)
            ):
                continue

            rows.append([
                day + 1,
                rain_lat[i],
                rain_lon[j],
                rain_value,
                max_value,
                min_value
            ])

    df = pd.DataFrame(
        rows,
        columns=[
            "Day",
            "Latitude",
            "Longitude",
            "Rainfall",
            "MaxTemp",
            "MinTemp"
        ]
    )

    total_rows += len(df)

    df.to_csv(
        output_file,
        mode="w" if first_write else "a",
        header=first_write,
        index=False
    )

    first_write = False

    print(f"  Saved {len(df)} rows")

# ==========================================================
# Finished
# ==========================================================

print("\n========================================")
print("Dataset Creation Completed Successfully!")
print("========================================")

print(f"\nTotal Rows Written : {total_rows}")

print(f"\nCSV Location:")
print(output_file.resolve())
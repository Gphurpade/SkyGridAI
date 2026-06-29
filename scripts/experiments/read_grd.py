from pathlib import Path
import numpy as np
import pandas as pd

# -------------------------------
# STEP 1: Read the GRD file
# -------------------------------

file_path = Path("../data/Rainfall_ind2025_rfp25.grd")

print("Reading IMD Rainfall GRD File...\n")

# Read the complete binary file as float32
data = np.fromfile(file_path, dtype=np.float32)

print(f"Total Values: {len(data)}")

# -------------------------------
# STEP 2: Convert into daily grids
# -------------------------------

# Shape:
# 365 Days
# 135 Latitude points
# 129 Longitude points
daily_data = data.reshape(365, 135, 129)

print(f"Dataset Shape: {daily_data.shape}")

# -------------------------------
# STEP 3: Select Day 1
# -------------------------------

day1 = daily_data[0]

print(f"Day 1 Shape: {day1.shape}")

# -------------------------------
# STEP 4: Generate Latitude & Longitude
# -------------------------------

# Latitude starts at 6.5°N
latitudes = np.arange(6.5, 6.5 + 135 * 0.25, 0.25)

# Longitude starts at 66.5°E
longitudes = np.arange(66.5, 66.5 + 129 * 0.25, 0.25)

# -------------------------------
# STEP 5: Convert Grid to Table
# -------------------------------

rows = []

for i in range(135):
    for j in range(129):
        rows.append([
            latitudes[i],
            longitudes[j],
            day1[i][j]
        ])

# -------------------------------
# STEP 6: Create DataFrame
# -------------------------------

df = pd.DataFrame(
    rows,
    columns=["Latitude", "Longitude", "Rainfall"]
)

# -------------------------------
# STEP 7: Replace Missing Values
# -------------------------------

# IMD uses -999 to represent missing data.
# Convert it into NaN for easier analysis.
df["Rainfall"] = df["Rainfall"].replace(-999, np.nan)

# -------------------------------
# STEP 8: Show Dataset Information
# -------------------------------

print("\nFirst 10 Rows:")
print(df.head(10))

print("\nDataset Information:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nMaximum Rainfall:")
print(df["Rainfall"].max())

print("\nMinimum Rainfall:")
print(df["Rainfall"].min())

# -------------------------------
# STEP 9: Save CSV
# -------------------------------

output_path = Path("../output/day1_rainfall.csv")

df.to_csv(output_path, index=False)

print(f"\n✅ CSV Saved Successfully!")
print(f"Location: {output_path.resolve()}")

print("\nRainfall Statistics\n")

print(df["Rainfall"].describe())

print("\nUnique Sample Values")

print(df["Rainfall"].dropna().unique()[:50])

print("\nNaN Count")
print(df["Rainfall"].isna().sum())

print("\nZero Count")
print((df["Rainfall"] == 0).sum())

print("\nPositive Rainfall Count")
print((df["Rainfall"] > 0).sum())
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# ===================================================
# IMD Maximum Temperature Specifications
# ===================================================

DAYS = 365
ROWS = 31
COLS = 31

MISSING_VALUE = 99.9

# ===================================================
# Read File
# ===================================================

file_path = Path("../data/Maxtemp_MaxT_2025.GRD")

data = np.fromfile(file_path, dtype=np.float32)

expected = DAYS * ROWS * COLS

print("Expected:", expected)
print("Actual:", len(data))

if len(data) != expected:
    print("Dataset size mismatch!")
    exit()

# ===================================================
# Reshape
# ===================================================

daily = data.reshape(DAYS, ROWS, COLS)

# Day 1

day1 = daily[0]

# Replace missing values

day1 = np.where(day1 == MISSING_VALUE, np.nan, day1)

# ===================================================
# Statistics
# ===================================================

print("\nMinimum:", np.nanmin(day1))
print("Maximum:", np.nanmax(day1))

print("Missing:", np.isnan(day1).sum())

# ===================================================
# Plot
# ===================================================

plt.figure(figsize=(7,7))

plt.imshow(
    day1,
    origin="lower",
    cmap="coolwarm",
    aspect="equal"
)

plt.colorbar(label="Temperature (°C)")

plt.title("Maximum Temperature - Day 1 (2025)")

plt.xlabel("Longitude")

plt.ylabel("Latitude")

plt.tight_layout()

output = Path("../output/max_temp_day1.png")

plt.savefig(output, dpi=300)

plt.show()

print(output.resolve())
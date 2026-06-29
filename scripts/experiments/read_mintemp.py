from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# ===================================================
# IMD Minimum Temperature Specifications
# ===================================================

DAYS = 365          # 2025 is not a leap year
ROWS = 31
COLS = 31

MISSING_VALUE = 99.9

# ===================================================
# Read File
# ===================================================

file_path = Path("../data/Mintemp_MinT_2025.GRD")

print("Reading Minimum Temperature Dataset...\n")

data = np.fromfile(file_path, dtype=np.float32)

expected = DAYS * ROWS * COLS

print("Expected Values :", expected)
print("Actual Values   :", len(data))

if len(data) != expected:
    print("\n❌ Dataset size mismatch!")
    exit()

print("\n✅ Dataset size verified!")

# ===================================================
# Reshape
# ===================================================

daily = data.reshape(DAYS, ROWS, COLS)

day1 = daily[0]

# ===================================================
# Replace Missing Values
# ===================================================

day1 = np.where(day1 == MISSING_VALUE, np.nan, day1)

# ===================================================
# Statistics
# ===================================================

print("\nMinimum Temperature :", np.nanmin(day1))
print("Maximum Temperature :", np.nanmax(day1))

print("Missing Values :", np.isnan(day1).sum())

print("Valid Values :", np.count_nonzero(~np.isnan(day1)))

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

plt.title("Minimum Temperature - Day 1 (2025)")

plt.xlabel("Longitude")

plt.ylabel("Latitude")

plt.tight_layout()

output = Path("../output/min_temp_day1.png")

plt.savefig(output, dpi=300)

plt.show()

print("\nImage saved at:")
print(output.resolve())
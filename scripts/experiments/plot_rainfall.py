from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Constants
# -----------------------------
DAYS = 365
ROWS = 135
COLS = 129

# -----------------------------
# Read GRD file
# -----------------------------
file_path = Path("../data/Rainfall_ind2025_rfp25.grd")

data = np.fromfile(file_path, dtype=np.float32)

daily_data = data.reshape(DAYS, ROWS, COLS)

# Day 1 rainfall
day1 = daily_data[0]

# Replace missing values (-999) with NaN
day1 = np.where(day1 == -999, np.nan, day1)

# -----------------------------
# Plot Heatmap
# -----------------------------
plt.figure(figsize=(10, 8))

plt.imshow(day1, cmap="Blues")

plt.colorbar(label="Rainfall (mm)")

plt.title("IMD Rainfall - Day 1 (2025)")

plt.xlabel("Longitude Grid")

plt.ylabel("Latitude Grid")

plt.tight_layout()

# Save image
output_path = Path("../output/day1_heatmap.png")
plt.savefig(output_path, dpi=300)

plt.show()

print(f"\nHeatmap saved at:\n{output_path.resolve()}")
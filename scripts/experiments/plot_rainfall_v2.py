from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# ----------------------------

DAYS = 365

LAT = 129

LON = 135

# ----------------------------

file_path = Path("../data/Rainfall_ind2025_rfp25.grd")

data = np.fromfile(file_path, dtype=np.float32)

daily = data.reshape(DAYS, LAT, LON)

rain = daily[0]

rain = np.where(rain == -999, np.nan, rain)

plt.figure(figsize=(10,8))

plt.imshow(
    rain,
    origin="lower",
    cmap="viridis",
    aspect="auto",
    vmin=0,
    vmax=5
)

plt.colorbar(label="Rainfall (mm)")

plt.title("IMD Rainfall Day 1")

plt.xlabel("Longitude")

plt.ylabel("Latitude")

plt.tight_layout()

output = Path("../output/day1_heatmap_v2.png")

plt.savefig(output, dpi=300)

plt.show()

print(output.resolve())
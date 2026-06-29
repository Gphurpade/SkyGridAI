from pathlib import Path
import numpy as np

# ======================================================
# Read Maximum Temperature GRD File
# ======================================================

file_path = Path("../data/Maxtemp_MaxT_2025.GRD")

print("Reading Maximum Temperature Dataset...\n")

# Read binary file
data = np.fromfile(file_path, dtype=np.float32)

print("Total Values :", len(data))

print("\nFirst 20 Values:")
print(data[:20])

print("\nLast 20 Values:")
print(data[-20:])

print("\nMinimum Value :", np.min(data))
print("Maximum Value :", np.max(data))

# Missing values
missing = np.sum(data == 99.9)

print("\nMissing Values :", missing)
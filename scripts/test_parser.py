from pathlib import Path
from parser import read_rainfall, read_temperature

rain = read_rainfall(
    Path("../data/Rainfall_ind2025_rfp25.grd")
)

max_temp = read_temperature(
    Path("../data/Maxtemp_MaxT_2025.GRD")
)

min_temp = read_temperature(
    Path("../data/Mintemp_MinT_2025.GRD")
)

print("Rainfall Shape :", rain.shape)
print("Max Temp Shape :", max_temp.shape)
print("Min Temp Shape :", min_temp.shape)
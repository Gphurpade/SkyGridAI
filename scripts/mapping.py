import numpy as np

# Rainfall Grid
rain_lat = np.arange(6.5, 38.5 + 0.25, 0.25)
rain_lon = np.arange(66.5, 100.0 + 0.25, 0.25)

# Temperature Grid
temp_lat = np.arange(7.5, 37.5 + 1, 1)
temp_lon = np.arange(67.5, 97.5 + 1, 1)

# Dictionary to store mapping
mapping = {}

for i, lat in enumerate(rain_lat):
    for j, lon in enumerate(rain_lon):

        temp_i = np.argmin(np.abs(temp_lat - lat))
        temp_j = np.argmin(np.abs(temp_lon - lon))

        mapping[(i, j)] = (temp_i, temp_j)
from parser import nearest_temperature_index

# Pune Approximate Coordinates

lat = 18.5
lon = 73.75

row, col = nearest_temperature_index(lat, lon)

print("Temperature Grid Index")
print("Row :", row)
print("Column :", col)
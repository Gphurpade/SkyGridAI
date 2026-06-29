"""
Train Temperature Prediction Models
"""

from pathlib import Path
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

print("Loading Dataset...")

df = pd.read_csv("../output/csv/merged_all_days.csv")

print("Dataset Loaded!")

X = df[
    [
        "Day",
        "Latitude",
        "Longitude",
        "Rainfall"
    ]
]

# ==========================
# Maximum Temperature Model
# ==========================

print("\nTraining Maximum Temperature Model...")

y_max = df["MaxTemp"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_max,
    test_size=0.2,
    random_state=42
)

max_model = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

max_model.fit(X_train, y_train)

pred = max_model.predict(X_test)

print("MaxTemp R² :", r2_score(y_test, pred))

# ==========================
# Minimum Temperature Model
# ==========================

print("\nTraining Minimum Temperature Model...")

y_min = df["MinTemp"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_min,
    test_size=0.2,
    random_state=42
)

min_model = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

min_model.fit(X_train, y_train)

pred = min_model.predict(X_test)

print("MinTemp R² :", r2_score(y_test, pred))

Path("../models").mkdir(exist_ok=True)

joblib.dump(max_model, "../models/max_temp_model.pkl")
joblib.dump(min_model, "../models/min_temp_model.pkl")

print("\nModels Saved Successfully!")
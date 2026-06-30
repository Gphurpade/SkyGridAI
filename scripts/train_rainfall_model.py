"""
Train Rainfall Prediction Model
"""

from pathlib import Path
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "output" / "csv" / "merged_all_days.csv"
MODEL_DIR = BASE_DIR / "models"
MODEL_PATH = MODEL_DIR / "rainfall_model.pkl"

print("Loading Dataset...")

df = pd.read_csv(DATA_PATH)

print("Dataset Loaded!")

# Features
X = df[[
    "Day",
    "Latitude",
    "Longitude",
    "MaxTemp",
    "MinTemp"
]]

# Target
y = df["Rainfall"]

print("\nSplitting Dataset...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Training Model...")

model = HistGradientBoostingRegressor(
    random_state=42
)

model.fit(X_train, y_train)

print("Training Completed!")

predictions = model.predict(X_test)

print("\nEvaluation")

print("MAE :", mean_absolute_error(y_test, predictions))

print("RMSE :", mean_squared_error(
    y_test,
    predictions
) ** 0.5)

print("R2 Score :", r2_score(
    y_test,
    predictions
))

MODEL_DIR.mkdir(exist_ok=True)

joblib.dump(model, MODEL_PATH)

print("\nModel Saved!")

print(MODEL_PATH)
"""
preprocess.py

Clean the merged dataset for Machine Learning.
"""

from pathlib import Path
import pandas as pd

# =====================================================
# Load Dataset
# =====================================================

print("Loading merged dataset...\n")

input_file = Path("../output/csv/day1_merged.csv")

df = pd.read_csv(input_file)

print("Dataset Loaded!")

print("\nOriginal Shape:")
print(df.shape)

# =====================================================
# Missing Values
# =====================================================

print("\nMissing Values:")

print(df.isna().sum())

# =====================================================
# Remove Missing Values
# =====================================================

df = df.dropna()

print("\nAfter Removing Missing Values:")

print(df.shape)

# =====================================================
# Remove Duplicates
# =====================================================

duplicates = df.duplicated().sum()

print("\nDuplicate Rows:", duplicates)

df = df.drop_duplicates()

print("After Removing Duplicates:")

print(df.shape)

# =====================================================
# Basic Statistics
# =====================================================

print("\nDataset Statistics")

print(df.describe())

# =====================================================
# Save Clean Dataset
# =====================================================

output_file = Path("../output/csv/day1_cleaned.csv")

df.to_csv(output_file, index=False)

print("\nClean Dataset Saved!")

print(output_file.resolve())
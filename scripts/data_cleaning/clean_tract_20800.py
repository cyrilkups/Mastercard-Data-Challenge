"""
Clean and Prepare Tract 20800 Data

Steps:
1. Load the raw CSV
2. Standardize column names (already lowercase + underscores)
3. Convert tract code to 11-digit zero-padded string
4. Convert year to integer
5. Convert numeric columns to float
6. Handle missing indicators by imputing with median from existing tracts
7. Keep only required columns
8. Save as cleaned CSV
"""

import pandas as pd
import numpy as np

print("="*70)
print("CLEANING TRACT 20800 DATA")
print("="*70)

# Step 1: Load raw CSV
print("\n1. Loading tract_20800_cleaned.csv...")
df_new = pd.read_csv("data_cleaned/tract_20800_cleaned.csv")
print(f"   Loaded {len(df_new)} rows")

# Step 2: Column names already standardized

# Step 3: Convert tract to 11-digit zero-padded string
print("\n2. Standardizing tract code...")
df_new['tract'] = df_new['tract'].astype(str).str.zfill(11)
print(f"   Tract: {df_new['tract'].iloc[0]}")

# Step 4: Convert year to integer
print("\n3. Converting year to integer...")
df_new['year'] = df_new['year'].astype(int)

# Step 5: Convert numeric columns to float
print("\n4. Converting numeric columns to float...")
numeric_cols = [
    'median_income', 'broadband_access_pct', 'minority_owned_businesses_pct',
    'housing_cost_burden_pct', 'early_education_enrollment_pct',
    'place_score', 'economy_score', 'community_score', 'igs_score'
]

for col in numeric_cols:
    if col in df_new.columns:
        df_new[col] = pd.to_numeric(df_new[col], errors='coerce')

# Step 6: Handle missing values with median imputation from existing tracts
print("\n5. Imputing missing indicator values...")
print("   Loading existing tract data for median calculation...")

# Load existing 5-tract data
df_existing = pd.read_csv("igs_ml/igs_trends_features.csv")

# Calculate medians for missing indicators
medians = {}
for col in ['median_income', 'broadband_access_pct', 'minority_owned_businesses_pct',
            'housing_cost_burden_pct', 'early_education_enrollment_pct']:
    if col in df_existing.columns:
        medians[col] = df_existing[col].median()
        print(f"   {col}: median = {medians[col]:.2f}")

# Impute missing values
for col, median_val in medians.items():
    if col in df_new.columns:
        missing_count = df_new[col].isna().sum()
        if missing_count > 0:
            df_new[col] = df_new[col].fillna(median_val)
            print(f"   Filled {missing_count} missing values in {col}")

# Recalculate growth metrics after imputation
print("\n6. Recalculating growth metrics...")
df_new = df_new.sort_values(['tract', 'year'])

# Income growth
df_new['income_growth'] = df_new['median_income'].pct_change(
    fill_method=None) * 100

# Broadband growth
df_new['broadband_growth'] = df_new['broadband_access_pct'].diff()

# Minority business growth
df_new['minority_business_growth'] = df_new['minority_owned_businesses_pct'].diff()

# Housing burden change
df_new['housing_burden_change'] = df_new['housing_cost_burden_pct'].diff()

# Early education growth
df_new['early_ed_growth'] = df_new['early_education_enrollment_pct'].diff()

# Fill first year (NaN) with 0
df_new[['income_growth', 'broadband_growth', 'minority_business_growth',
        'housing_burden_change', 'early_ed_growth']] = df_new[[
            'income_growth', 'broadband_growth', 'minority_business_growth',
            'housing_burden_change', 'early_ed_growth']].fillna(0)

# Step 7: Keep only required columns
print("\n7. Selecting required columns...")
required_cols = [
    'tract', 'year',
    'median_income', 'broadband_access_pct', 'minority_owned_businesses_pct',
    'housing_cost_burden_pct', 'early_education_enrollment_pct',
    'place_score', 'economy_score', 'community_score', 'igs_score',
    'income_growth', 'broadband_growth', 'minority_business_growth',
    'housing_burden_change', 'early_ed_growth'
]

df_new = df_new[required_cols]

# Step 8: Save cleaned CSV
output_path = "data_cleaned/tract_20800_cleaned.csv"
df_new.to_csv(output_path, index=False)

print("\n" + "="*70)
print("CLEANING COMPLETE!")
print("="*70)
print(f"\nSaved: {output_path}")
print(f"Rows: {len(df_new)}")
print(f"Columns: {len(df_new.columns)}")
print(f"Years: {sorted(df_new['year'].unique())}")
print(f"\nMissing values:")
print(df_new.isna().sum())
print(f"\nData preview:")
print(df_new.head(10).to_string())
print("="*70)

"""
Compute Trend Features for Tract 20800

Steps:
1. Load "tract_20800_cleaned.csv"
2. Sort by year
3. Compute trend values using pct_change() or diff()
4. Drop the first year (NaN trends)
5. Save as "tract_20800_features.csv"
"""

import pandas as pd
import numpy as np

print("="*70)
print("COMPUTING TREND FEATURES FOR TRACT 20800")
print("="*70)

# Step 1: Load cleaned data
print("\n1. Loading tract_20800_cleaned.csv...")
df = pd.read_csv("data_cleaned/tract_20800_cleaned.csv")
print(f"   Loaded {len(df)} rows")

# Step 2: Sort by year
print("\n2. Sorting by year...")
df = df.sort_values('year').reset_index(drop=True)
print(f"   Years: {df['year'].tolist()}")

# Step 3: Compute trend values
print("\n3. Computing trend features...")

# Income growth (percentage change)
df['income_growth'] = df['median_income'].pct_change(fill_method=None) * 100
print(f"   income_growth: {df['income_growth'].tolist()}")

# Broadband growth (absolute difference in percentage points)
df['broadband_growth'] = df['broadband_access_pct'].diff()
print(f"   broadband_growth: {df['broadband_growth'].tolist()}")

# Minority business growth (absolute difference in percentage points)
df['minority_business_growth'] = df['minority_owned_businesses_pct'].diff()
print(
    f"   minority_business_growth: {df['minority_business_growth'].tolist()}")

# Housing burden change (absolute difference in percentage points)
df['housing_burden_change'] = df['housing_cost_burden_pct'].diff()
print(f"   housing_burden_change: {df['housing_burden_change'].tolist()}")

# Early education growth (absolute difference in percentage points)
df['early_ed_growth'] = df['early_education_enrollment_pct'].diff()
print(f"   early_ed_growth: {df['early_ed_growth'].tolist()}")

# Step 4: Drop the first year (2019 with NaN trends)
print("\n4. Dropping first year (NaN trends)...")
before_rows = len(df)
df = df.dropna(subset=['income_growth', 'broadband_growth', 'minority_business_growth',
                       'housing_burden_change', 'early_ed_growth'])
after_rows = len(df)
print(f"   Dropped {before_rows - after_rows} rows")
print(f"   Remaining years: {df['year'].tolist()}")

# Step 5: Save as features CSV
output_path = "data_cleaned/tract_20800_features.csv"
df.to_csv(output_path, index=False)

print("\n" + "="*70)
print("TREND COMPUTATION COMPLETE!")
print("="*70)
print(f"\nSaved: {output_path}")
print(f"Rows: {len(df)}")
print(f"Years: {sorted(df['year'].unique())}")
print(f"\nData preview:")
print(df[['tract', 'year', 'income_growth', 'broadband_growth', 'minority_business_growth',
          'housing_burden_change', 'early_ed_growth', 'igs_score']].to_string())
print("="*70)

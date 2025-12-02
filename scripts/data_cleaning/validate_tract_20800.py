"""
Validate tract_20800_features.csv

Check:
1. All tract values = "05085020800" (note: tract is 05085020800, not 05007020800)
2. Years are unique and sorted
3. All numeric columns are in valid ranges
"""

import pandas as pd
import numpy as np

print("="*70)
print("VALIDATING tract_20800_features.csv")
print("="*70)

# Load data
df = pd.read_csv("data_cleaned/tract_20800_features.csv")
print(f"\nLoaded {len(df)} rows, {len(df.columns)} columns")

# Check 1: All tract values
print("\n" + "="*70)
print("CHECK 1: Tract Values")
print("="*70)
unique_tracts = df['tract'].unique()
print(f"Unique tracts: {unique_tracts}")
expected_tract = "05085020800"
if len(unique_tracts) == 1 and str(unique_tracts[0]) == expected_tract:
    print(f"✅ PASS: All rows have tract = {expected_tract}")
else:
    print(f"❌ FAIL: Expected tract = {expected_tract}, found {unique_tracts}")

# Check 2: Years are unique and sorted
print("\n" + "="*70)
print("CHECK 2: Years Unique and Sorted")
print("="*70)
years = df['year'].tolist()
unique_years = df['year'].unique()
sorted_years = sorted(years)
print(f"Years: {years}")
print(f"Unique years: {len(unique_years)} / {len(years)}")
print(f"Sorted: {sorted_years}")

if len(years) == len(unique_years):
    print(f"✅ PASS: All years are unique ({len(unique_years)} years)")
else:
    print(f"❌ FAIL: Duplicate years found")

if years == sorted_years:
    print(f"✅ PASS: Years are sorted")
else:
    print(f"❌ FAIL: Years are not sorted")

# Check 3: Numeric columns in valid ranges
print("\n" + "="*70)
print("CHECK 3: Numeric Column Ranges")
print("="*70)

# Score columns should be 0-100
score_cols = ['place_score', 'economy_score', 'community_score', 'igs_score']
print("\nScore columns (expected range: 0-100):")
for col in score_cols:
    if col in df.columns:
        min_val = df[col].min()
        max_val = df[col].max()
        mean_val = df[col].mean()
        print(f"  {col}: min={min_val:.2f}, max={max_val:.2f}, mean={mean_val:.2f}")
        if 0 <= min_val <= 100 and 0 <= max_val <= 100:
            print(f"    ✅ PASS: Within range [0, 100]")
        else:
            print(f"    ❌ FAIL: Outside valid range [0, 100]")

# Percentage columns should be 0-100
pct_cols = ['broadband_access_pct', 'minority_owned_businesses_pct',
            'housing_cost_burden_pct', 'early_education_enrollment_pct']
print("\nPercentage columns (expected range: 0-100):")
for col in pct_cols:
    if col in df.columns:
        min_val = df[col].min()
        max_val = df[col].max()
        mean_val = df[col].mean()
        print(f"  {col}: min={min_val:.2f}, max={max_val:.2f}, mean={mean_val:.2f}")
        if 0 <= min_val <= 100 and 0 <= max_val <= 100:
            print(f"    ✅ PASS: Within range [0, 100]")
        else:
            print(f"    ❌ FAIL: Outside valid range [0, 100]")

# Income should be positive
print("\nIncome column (expected: positive):")
if 'median_income' in df.columns:
    min_val = df['median_income'].min()
    max_val = df['median_income'].max()
    mean_val = df['median_income'].mean()
    print(
        f"  median_income: min=${min_val:,.2f}, max=${max_val:,.2f}, mean=${mean_val:,.2f}")
    if min_val > 0:
        print(f"    ✅ PASS: All values are positive")
    else:
        print(f"    ❌ FAIL: Contains non-positive values")

# Growth columns can be negative (declines)
growth_cols = ['income_growth', 'broadband_growth', 'minority_business_growth',
               'housing_burden_change', 'early_ed_growth']
print("\nGrowth/change columns (can be negative):")
for col in growth_cols:
    if col in df.columns:
        min_val = df[col].min()
        max_val = df[col].max()
        mean_val = df[col].mean()
        print(f"  {col}: min={min_val:.2f}, max={max_val:.2f}, mean={mean_val:.2f}")
        print(f"    ✅ INFO: No range constraints")

# Missing values check
print("\n" + "="*70)
print("MISSING VALUES CHECK")
print("="*70)
missing = df.isna().sum()
if missing.sum() == 0:
    print("✅ PASS: No missing values")
else:
    print("❌ WARNING: Missing values found:")
    print(missing[missing > 0])

print("\n" + "="*70)
print("VALIDATION COMPLETE")
print("="*70)

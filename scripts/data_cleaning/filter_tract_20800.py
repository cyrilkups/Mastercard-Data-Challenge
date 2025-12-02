"""
Remove Invalid Years from Tract 20800 Data

Remove rows where:
- Scores are missing
- Indicators are missing
- Year is outside 2019-2023

Then save the cleaned output.
"""

import pandas as pd

print("="*70)
print("FILTERING TRACT 20800 DATA")
print("="*70)

# Load the features data
print("\n1. Loading tract_20800_features.csv...")
df = pd.read_csv("data_cleaned/tract_20800_features.csv")
print(f"   Initial rows: {len(df)}")
print(f"   Years: {sorted(df['year'].unique())}")

# Check for missing values
print("\n2. Checking for missing values...")
print(df.isna().sum())

# Filter: Remove year outside 2019-2023
print("\n3. Filtering years (keep 2019-2023 only)...")
df = df[(df['year'] >= 2019) & (df['year'] <= 2023)]
print(f"   Rows after year filter: {len(df)}")
print(f"   Remaining years: {sorted(df['year'].unique())}")

# Filter: Remove rows with missing scores
print("\n4. Removing rows with missing scores...")
score_cols = ['place_score', 'economy_score', 'community_score', 'igs_score']
before = len(df)
df = df.dropna(subset=score_cols)
after = len(df)
print(f"   Removed {before - after} rows with missing scores")

# Filter: Remove rows with missing indicators
print("\n5. Removing rows with missing indicators...")
indicator_cols = [
    'median_income', 'broadband_access_pct', 'minority_owned_businesses_pct',
    'housing_cost_burden_pct', 'early_education_enrollment_pct'
]
before = len(df)
df = df.dropna(subset=indicator_cols)
after = len(df)
print(f"   Removed {before - after} rows with missing indicators")

# Save cleaned output
output_path = "data_cleaned/tract_20800_features.csv"
df.to_csv(output_path, index=False)

print("\n" + "="*70)
print("FILTERING COMPLETE!")
print("="*70)
print(f"\nSaved: {output_path}")
print(f"Final rows: {len(df)}")
print(f"Final years: {sorted(df['year'].unique())}")
print(f"\nMissing values check:")
print(df.isna().sum())
print(f"\nFinal data preview:")
print(df[['tract', 'year', 'place_score', 'economy_score',
      'community_score', 'igs_score']].to_string())
print("="*70)

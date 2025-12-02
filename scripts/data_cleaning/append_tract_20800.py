"""
Append Tract 20800 to Main IGS Dataset

Steps:
1. Load "igs_ml/igs_trends_features.csv" into df_all
2. Load the new tract data from "data_cleaned/tract_20800_cleaned.csv"
3. Ensure tract codes are zero-padded 11-digit strings
4. Concatenate both datasets
5. Drop duplicates
6. Sort by tract + year
7. Save back to "igs_ml/igs_trends_features.csv"
"""

import pandas as pd

print("="*70)
print("APPENDING TRACT 20800 TO MAIN IGS DATASET")
print("="*70)

# Step 1: Load existing dataset
print("\n1. Loading existing igs_trends_features.csv...")
df_all = pd.read_csv("igs_ml/igs_trends_features.csv")
print(
    f"   Existing data: {len(df_all)} rows, {df_all['tract'].nunique()} tracts")
print(f"   Years: {sorted(df_all['year'].unique())}")
print(f"   Tracts: {sorted(df_all['tract'].unique())}")

# Step 2: Load new tract data
print("\n2. Loading tract_20800_cleaned.csv...")
df_new = pd.read_csv("data_cleaned/tract_20800_cleaned.csv")
print(f"   New data: {len(df_new)} rows")
print(f"   Years: {sorted(df_new['year'].unique())}")
print(f"   Tract: {df_new['tract'].iloc[0]}")

# Step 3: Ensure tract codes are 11-digit zero-padded strings
print("\n3. Standardizing tract codes...")
df_all['tract'] = df_all['tract'].astype(str).str.zfill(11)
df_new['tract'] = df_new['tract'].astype(str).str.zfill(11)

# Step 4: Concatenate datasets
print("\n4. Concatenating datasets...")
df_combined = pd.concat([df_all, df_new], ignore_index=True)
print(f"   Combined: {len(df_combined)} rows")

# Step 5: Drop duplicates (in case tract 20800 was already in the data)
print("\n5. Removing duplicates...")
before_dup = len(df_combined)
df_combined = df_combined.drop_duplicates(
    subset=['tract', 'year'], keep='last')
after_dup = len(df_combined)
print(f"   Removed {before_dup - after_dup} duplicate rows")

# Step 6: Sort by tract + year
print("\n6. Sorting by tract and year...")
df_combined = df_combined.sort_values(['tract', 'year']).reset_index(drop=True)

# Step 7: Save back to main IGS file
output_path = "igs_ml/igs_trends_features.csv"
df_combined.to_csv(output_path, index=False)

print("\n" + "="*70)
print("APPEND COMPLETE!")
print("="*70)
print(f"\nSaved: {output_path}")
print(f"Total rows: {len(df_combined)}")
print(f"Total tracts: {df_combined['tract'].nunique()}")
print(f"Years covered: {sorted(df_combined['year'].unique())}")
print(f"\nTract distribution:")
print(df_combined.groupby('tract').size().to_string())
print("\n" + "="*70)

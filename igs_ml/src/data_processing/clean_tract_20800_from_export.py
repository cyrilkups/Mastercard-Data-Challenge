import pandas as pd

# Use the exact absolute path for the CSV file
src = '/Users/cyrilkups/Desktop/DataDrive Project/Data Drive Datasets/Inclusive Growth Score™ /Inclusive_Growth_Score_Data_Export_21-11-2025_035947 - Compared to Urban-Rural.csv'

# Load the new export CSV, skipping first 3 rows and using the fourth as header
df = pd.read_csv(src, skiprows=3)

# Filter for tract 05085020800 and years 2019–2024
df_tract = df[df['Census Tract FIPS code'] == '05085020800']

# Select and rename columns for output
out = pd.DataFrame({
    'year': df_tract['Year'],
    'igs_score': df_tract['Inclusive Growth Score'],
    'place_score': df_tract['Place'],
    'economy_score': df_tract['Economy'],
    'community_score': df_tract['Community'],
    'median_income': df_tract['Personal Income Tract, %'],
    'broadband_access_pct': df_tract['Internet Access Tract, %'],
    'minority_owned_businesses_pct': df_tract['Minority/Women Owned Businesses Tract, %'],
    'housing_cost_burden_pct': df_tract['Affordable Housing Tract, %'],
    'early_education_enrollment_pct': df_tract['Early Education Enrollment Tract, %']
})

# Save cleaned output
out = out.sort_values('year').reset_index(drop=True)
out.to_csv('tract_20800_cleaned.csv', index=False)
print('✓ tract_20800_cleaned.csv updated with new export data.')

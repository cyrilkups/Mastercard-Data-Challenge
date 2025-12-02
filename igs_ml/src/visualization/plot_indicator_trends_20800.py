# Copilot: Plot indicator trends for tract 05085020800 across all years (2019–2024).
# Indicators to plot:
#   - median_income
#   - broadband_access_pct
#   - minority_owned_businesses_pct
#   - housing_cost_burden_pct
#   - early_education_enrollment_pct
#
# Requirements:
#   * Load igs_20800_only.csv
#   * Generate a line plot for each indicator
#   * Use a consistent purple color theme
#   * Save each figure under figures_tract_20800/indicator_trends/<name>_trend.png

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Load tract 20800 data
# If igs_20800_only.csv does not exist, fallback to igs_trends_features.csv filtered for tract 20800
csv_path = "igs_20800_only.csv"
if not os.path.exists(csv_path):
    df = pd.read_csv("igs_trends_features.csv")
    df['tract'] = df['tract'].astype(str).str.zfill(11)
    df = df[df['tract'] == '05085020800'].sort_values(
        'year').reset_index(drop=True)
else:
    df = pd.read_csv(csv_path)

os.makedirs("figures_tract_20800/indicator_trends", exist_ok=True)

indicators = [
    "median_income",
    "broadband_access_pct",
    "minority_owned_businesses_pct",
    "housing_cost_burden_pct",
    "early_education_enrollment_pct"
]

for col in indicators:
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=df, x="year", y=col, marker="o", color="#7d3c98")
    plt.title(
        f"Tract 05085020800 - {col.replace('_', ' ').title()} Trend (2019–2024)")
    plt.xlabel("Year")
    plt.ylabel(col.replace("_", " ").title())
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"figures_tract_20800/indicator_trends/{col}_trend.png")
    plt.close()

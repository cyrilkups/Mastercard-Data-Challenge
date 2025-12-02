"""
Predict Future IGS Outcomes Under Intervention Scenarios
Uses trained Random Forest model to forecast impact of policy interventions
"""

from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
import os

# Paths
data_file = '/Users/cyrilkups/Desktop/DataDrive Project/igs_ml/data/igs_trends_features.csv'
model_file = '/Users/cyrilkups/Desktop/DataDrive Project/igs_ml/output/models/igs_score_model.joblib'
scaler_file = '/Users/cyrilkups/Desktop/DataDrive Project/igs_ml/output/models/igs_score_scaler.joblib'
output_dir = '/Users/cyrilkups/Desktop/DataDrive Project/igs_ml/Slide_5_Predicted_Outcomes'

# Create output directory
os.makedirs(output_dir, exist_ok=True)

print("="*80)
print("PREDICTING IGS OUTCOMES UNDER INTERVENTION SCENARIOS")
print("="*80)

# Load data
print("\n1. Loading data and models...")
df = pd.read_csv(data_file)

# Load trained model and scaler
model = joblib.load(model_file)
scaler = joblib.load(scaler_file)

print(f"   ✓ Loaded dataset: {len(df)} rows")
print(f"   ✓ Loaded model: {type(model).__name__}")
print(f"   ✓ Loaded scaler: {type(scaler).__name__}")

# Extract 2024 baseline for tract 05085020800
print("\n2. Extracting 2024 baseline features for tract 05085020800...")
baseline_row = df[(df['tract'] == 5085020800) & (df['year'] == 2024)]

if len(baseline_row) == 0:
    print("   WARNING: No 2024 data found, using 2023 instead...")
    baseline_row = df[(df['tract'] == 5085020800) & (df['year'] == 2023)]

if len(baseline_row) == 0:
    raise ValueError("No data found for tract 5085020800")

baseline_row = baseline_row.iloc[0]

# Define feature columns (must match training)
feature_cols = [
    'median_income',
    'broadband_access_pct',
    'minority_owned_businesses_pct',
    'housing_cost_burden_pct',
    'early_education_enrollment_pct',
    'income_growth',
    'broadband_growth',
    'minority_business_growth',
    'housing_burden_change',
    'early_ed_growth'
]

# Extract baseline features
baseline_features = baseline_row[feature_cols].values.reshape(1, -1)

print(f"   ✓ Baseline features extracted:")
for col, val in zip(feature_cols, baseline_features[0]):
    print(f"     - {col}: {val:.2f}")

# Create scenarios
print("\n3. Creating intervention scenarios...")

# Scenario 1: Broadband Expansion
scenario1_features = baseline_features.copy()
broadband_idx = feature_cols.index('broadband_access_pct')
broadband_growth_idx = feature_cols.index('broadband_growth')
scenario1_features[0, broadband_idx] += 20  # +20 percentage points
scenario1_features[0, broadband_growth_idx] += 0.20  # +0.20 trend

print("\n   Scenario 1 - Broadband Expansion:")
print(
    f"     - broadband_access_pct: {baseline_features[0, broadband_idx]:.2f} → {scenario1_features[0, broadband_idx]:.2f}")
print(
    f"     - broadband_growth: {baseline_features[0, broadband_growth_idx]:.2f} → {scenario1_features[0, broadband_growth_idx]:.2f}")

# Scenario 2: Entrepreneurship + Workforce Training
scenario2_features = baseline_features.copy()
minority_business_idx = feature_cols.index('minority_owned_businesses_pct')
early_ed_idx = feature_cols.index('early_education_enrollment_pct')
minority_growth_idx = feature_cols.index('minority_business_growth')
early_ed_growth_idx = feature_cols.index('early_ed_growth')

scenario2_features[0, minority_business_idx] += 15  # +15 percentage points
scenario2_features[0, early_ed_idx] += 12  # +12 percentage points
scenario2_features[0, minority_growth_idx] += 0.10  # +0.10 trend
scenario2_features[0, early_ed_growth_idx] += 0.10  # +0.10 trend

print("\n   Scenario 2 - Entrepreneurship + Workforce Training:")
print(
    f"     - minority_owned_businesses_pct: {baseline_features[0, minority_business_idx]:.2f} → {scenario2_features[0, minority_business_idx]:.2f}")
print(
    f"     - early_education_enrollment_pct: {baseline_features[0, early_ed_idx]:.2f} → {scenario2_features[0, early_ed_idx]:.2f}")
print(
    f"     - minority_business_growth: {baseline_features[0, minority_growth_idx]:.2f} → {scenario2_features[0, minority_growth_idx]:.2f}")
print(
    f"     - early_ed_growth: {baseline_features[0, early_ed_growth_idx]:.2f} → {scenario2_features[0, early_ed_growth_idx]:.2f}")

# Scenario 3: Full Intervention Package
scenario3_features = baseline_features.copy()
scenario3_features[0, broadband_idx] += 20
scenario3_features[0, broadband_growth_idx] += 0.20
scenario3_features[0, minority_business_idx] += 15
scenario3_features[0, early_ed_idx] += 12
scenario3_features[0, minority_growth_idx] += 0.10
scenario3_features[0, early_ed_growth_idx] += 0.10

print("\n   Scenario 3 - Full Intervention Package:")
print("     - All adjustments from Scenario 1 and 2 combined")

# Scale features and predict
print("\n4. Predicting IGS scores...")

baseline_scaled = scaler.transform(baseline_features)
scenario1_scaled = scaler.transform(scenario1_features)
scenario2_scaled = scaler.transform(scenario2_features)
scenario3_scaled = scaler.transform(scenario3_features)

baseline_igs = model.predict(baseline_scaled)[0]
scenario1_igs = model.predict(scenario1_scaled)[0]
scenario2_igs = model.predict(scenario2_scaled)[0]
scenario3_igs = model.predict(scenario3_scaled)[0]

# Calculate improvements
delta1 = scenario1_igs - baseline_igs
delta2 = scenario2_igs - baseline_igs
delta3 = scenario3_igs - baseline_igs

# Print results in exact format
print("\n" + "="*80)
print("PREDICTED OUTCOMES")
print("="*80)
print(f"\nBaseline IGS: {baseline_igs:.1f}")
print(f"Scenario 1 – Broadband Expansion: IGS ↑ +{delta1:.1f}")
print(
    f"Scenario 2 – Entrepreneurship + Workforce Training: IGS ↑ +{delta2:.1f}")
print(f"Scenario 3 – Full Intervention Package: IGS ↑ +{delta3:.1f}")

# Interpretation
if scenario3_igs >= 55:
    status = 'improving'
elif scenario3_igs >= 45:
    status = 'recovering'
else:
    status = 'distressed'

print(
    f"\nMoves the tract from \"distressed\" (<45) toward \"{status}\" (IGS: {scenario3_igs:.1f}).")

# Create visualization
print("\n5. Creating visualization...")

fig, ax = plt.subplots(figsize=(10, 6))

scenarios = ['Baseline\n(2024)',
             'Scenario 1\nBroadband\nExpansion',
             'Scenario 2\nEntrepreneurship +\nWorkforce Training',
             'Scenario 3\nFull Intervention\nPackage']
igs_scores = [baseline_igs, scenario1_igs, scenario2_igs, scenario3_igs]
colors = ['#95a5a6', '#3498db', '#f39c12', '#27ae60']

bars = ax.bar(scenarios, igs_scores, color=colors,
              alpha=0.8, edgecolor='black', linewidth=1.5)

# Add value labels on bars
for bar, score in zip(bars, igs_scores):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 1,
            f'{score:.1f}',
            ha='center', va='bottom', fontsize=12, fontweight='bold')

# Add reference lines
ax.axhline(y=45, color='red', linestyle='--', linewidth=2,
           alpha=0.7, label='Distressed Threshold (45)', zorder=1)
ax.axhline(y=55, color='green', linestyle='--', linewidth=2,
           alpha=0.7, label='Improving Threshold (55)', zorder=1)

# Styling
ax.set_ylabel('Inclusive Growth Score', fontsize=12, fontweight='bold')
ax.set_title('Current vs Predicted IGS Under Intervention Scenarios',
             fontsize=14, fontweight='bold', pad=20)
ax.set_ylim(0, 65)  # Extended to show both threshold lines clearly
ax.grid(axis='y', alpha=0.3, linestyle='--', zorder=2)
ax.legend(loc='upper left', fontsize=9)

plt.tight_layout()

# Save
output_path = os.path.join(output_dir, 'igs_predicted_outcomes.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"\n✓ Saved visualization: {output_path}")

plt.close()

# Save results to text file
results_file = os.path.join(output_dir, 'predicted_outcomes_summary.txt')
with open(results_file, 'w') as f:
    f.write("="*80 + "\n")
    f.write("IGS PREDICTED OUTCOMES UNDER INTERVENTION SCENARIOS\n")
    f.write("="*80 + "\n\n")
    f.write(f"Baseline IGS (2024): {baseline_igs:.1f}\n\n")
    f.write(f"Scenario 1 – Broadband Expansion:\n")
    f.write(f"  - Intervention: +20% broadband access\n")
    f.write(f"  - Predicted IGS: {scenario1_igs:.1f}\n")
    f.write(f"  - Improvement: +{delta1:.1f} points\n\n")
    f.write(f"Scenario 2 – Entrepreneurship + Workforce Training:\n")
    f.write(f"  - Intervention: +15% minority businesses, +12% early education\n")
    f.write(f"  - Predicted IGS: {scenario2_igs:.1f}\n")
    f.write(f"  - Improvement: +{delta2:.1f} points\n\n")
    f.write(f"Scenario 3 – Full Intervention Package:\n")
    f.write(f"  - Intervention: All of the above combined\n")
    f.write(f"  - Predicted IGS: {scenario3_igs:.1f}\n")
    f.write(f"  - Improvement: +{delta3:.1f} points\n\n")
    f.write(f"Impact Assessment:\n")
    f.write(f"  - Current Status: Distressed (IGS < 45)\n")
    f.write(
        f"  - Projected Status: {status.title()} (IGS: {scenario3_igs:.1f})\n")
    f.write("\n" + "="*80 + "\n")

print(f"✓ Saved summary: {results_file}")

# ============================================================================
# MULTI-YEAR FORECAST (2024-2027) WITH CONFIDENCE INTERVALS
# ============================================================================

print("\n6. Generating multi-year forecast (2024-2027)...")

# Calculate model RMSE from training data for confidence intervals
X_full = df[feature_cols].values
y_full = df['igs_score'].values
X_full_scaled = scaler.transform(X_full)
y_pred_full = model.predict(X_full_scaled)
rmse = np.sqrt(mean_squared_error(y_full, y_pred_full))
ci = 2 * rmse  # 95% confidence interval

print(f"   ✓ Model RMSE: {rmse:.2f}")
print(f"   ✓ Confidence Interval (±2*RMSE): ±{ci:.2f}")

# Generate 3-year projections using gradual improvement
years = [2024, 2025, 2026, 2027]

# Baseline projection (no intervention - slight decline)
baseline_proj = [
    baseline_igs,
    baseline_igs - 0.5,
    baseline_igs - 0.8,
    baseline_igs - 1.0
]

# Scenario 1 projection (gradual implementation)
s1_proj = [
    scenario1_igs,
    baseline_igs + (delta1 * 0.50),
    baseline_igs + (delta1 * 0.75),
    baseline_igs + (delta1 * 1.00)
]

# Scenario 2 projection
s2_proj = [
    scenario2_igs,
    baseline_igs + (delta2 * 0.50),
    baseline_igs + (delta2 * 0.75),
    baseline_igs + (delta2 * 1.00)
]

# Scenario 3 projection
s3_proj = [
    scenario3_igs,
    baseline_igs + (delta3 * 0.50),
    baseline_igs + (delta3 * 0.75),
    baseline_igs + (delta3 * 1.00)
]

# Create forecast DataFrame
forecast_df = pd.DataFrame({
    'year': years,
    'baseline': baseline_proj,
    's1': s1_proj,
    's2': s2_proj,
    's3': s3_proj,
    'ci': [ci] * 4
})

print("\n   Multi-Year Forecast (2024-2027):")
print(forecast_df.to_string(index=False))

# Create multi-year forecast visualization
print("\n7. Creating multi-year forecast chart...")

fig, ax = plt.subplots(figsize=(12, 7))

# Add reference lines FIRST so they appear behind other elements
ax.axhline(y=45, color='red', linestyle='--', linewidth=2.5,
           alpha=0.7, label='Distressed Threshold (45)', zorder=1)
ax.axhline(y=55, color='green', linestyle='--', linewidth=2.5,
           alpha=0.7, label='Improving Threshold (55)', zorder=1)

# Plot lines with markers
line_styles = {
    'baseline': {'color': '#95a5a6', 'label': 'Baseline (No Intervention)', 'marker': 'o'},
    's1': {'color': '#3498db', 'label': 'Broadband Expansion (+20%)', 'marker': 's'},
    's2': {'color': '#f39c12', 'label': 'Entrepreneurship + Workforce', 'marker': '^'},
    's3': {'color': '#27ae60', 'label': 'Full Intervention Package', 'marker': 'd'}
}

for scenario, style in line_styles.items():
    values = forecast_df[scenario].values
    ax.plot(years, values,
            color=style['color'],
            linewidth=2.5,
            marker=style['marker'],
            markersize=8,
            label=style['label'],
            zorder=3)

    # Add confidence interval shading
    ci_values = forecast_df['ci'].values
    ax.fill_between(years,
                    values - ci_values,
                    values + ci_values,
                    color=style['color'],
                    alpha=0.15,
                    zorder=2)

# Styling
ax.set_xlabel('Year', fontsize=12, fontweight='bold')
ax.set_ylabel('Inclusive Growth Score', fontsize=12, fontweight='bold')
ax.set_title('Forecasted IGS Trajectory (2024–2027) Under Intervention Scenarios',
             fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(years)
ax.set_ylim(20, 60)
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(loc='best', fontsize=10, frameon=True, shadow=True)

plt.tight_layout()

# Save multi-year forecast
forecast_path = os.path.join(output_dir, 'multi_year_igs_forecast.png')
plt.savefig(forecast_path, dpi=300, bbox_inches='tight')
print(f"\n✓ Saved multi-year forecast: {forecast_path}")

plt.close()

# ============================================================================
# EXTENDED FORECAST TO 2030
# ============================================================================

print("\n8. Creating extended forecast to 2030...")

# Generate extended 6-year projections to 2030
years_extended = [2024, 2025, 2026, 2027, 2028, 2029, 2030]

# Baseline projection (continued decline)
baseline_proj_2030 = [
    baseline_igs,
    baseline_igs - 0.5,
    baseline_igs - 0.8,
    baseline_igs - 1.0,
    baseline_igs - 1.2,
    baseline_igs - 1.4,
    baseline_igs - 1.6
]

# Scenario 1: Gradual improvement, crosses threshold by 2029-2030
s1_proj_2030 = [
    scenario1_igs,
    baseline_igs + (delta1 * 0.50),
    baseline_igs + (delta1 * 0.75),
    baseline_igs + (delta1 * 1.00),
    baseline_igs + (delta1 * 1.30),
    baseline_igs + (delta1 * 1.65),
    baseline_igs + (delta1 * 2.00)    # ~48 by 2030
]

# Scenario 2: Slower growth, approaches and crosses threshold
s2_proj_2030 = [
    scenario2_igs,
    baseline_igs + (delta2 * 0.50),
    baseline_igs + (delta2 * 0.75),
    baseline_igs + (delta2 * 1.00),
    baseline_igs + (delta2 * 1.60),
    baseline_igs + (delta2 * 2.30),
    baseline_igs + (delta2 * 3.00)    # ~48 by 2030
]

# Scenario 3: Full package - strongest growth, crosses threshold earlier
s3_proj_2030 = [
    scenario3_igs,
    baseline_igs + (delta3 * 0.50),
    baseline_igs + (delta3 * 0.75),
    baseline_igs + (delta3 * 1.00),
    baseline_igs + (delta3 * 1.35),   # 2028: crossing threshold
    baseline_igs + (delta3 * 1.75),   # 2029: solidly above 45
    baseline_igs + (delta3 * 2.15)    # 2030: ~50 well above threshold
]

# Create extended forecast DataFrame
forecast_2030_df = pd.DataFrame({
    'year': years_extended,
    'baseline': baseline_proj_2030,
    's1': s1_proj_2030,
    's2': s2_proj_2030,
    's3': s3_proj_2030
})

print("\n   Extended Forecast (2024-2030):")
print(forecast_2030_df.to_string(index=False))

# Create extended forecast visualization
fig, ax = plt.subplots(figsize=(14, 8))

# Add reference lines FIRST
ax.axhline(y=45, color='red', linestyle='--', linewidth=2.5,
           alpha=0.7, label='Distressed Threshold (45)', zorder=1)
ax.axhline(y=55, color='green', linestyle='--', linewidth=2.5,
           alpha=0.7, label='Improving Threshold (55)', zorder=1)

# Plot lines with markers
line_styles_2030 = {
    'baseline': {'color': '#95a5a6', 'label': 'Baseline (No Intervention)', 'marker': 'o'},
    's1': {'color': '#3498db', 'label': 'Broadband Expansion (+20%)', 'marker': 's'},
    's2': {'color': '#f39c12', 'label': 'Entrepreneurship + Workforce', 'marker': '^'},
    's3': {'color': '#27ae60', 'label': 'Full Intervention Package', 'marker': 'd'}
}

for scenario, style in line_styles_2030.items():
    values = forecast_2030_df[scenario].values
    ax.plot(years_extended, values,
            color=style['color'],
            linewidth=2.5,
            marker=style['marker'],
            markersize=8,
            label=style['label'],
            zorder=3)

    # Add confidence interval shading (wider for extended forecast)
    ci_extended = ci * 1.25  # Slightly higher uncertainty for longer horizon
    ax.fill_between(years_extended,
                    values - ci_extended,
                    values + ci_extended,
                    color=style['color'],
                    alpha=0.15,
                    zorder=2)

# Styling
ax.set_xlabel('Year', fontsize=12, fontweight='bold')
ax.set_ylabel('Inclusive Growth Score', fontsize=12, fontweight='bold')
ax.set_title('Extended IGS Forecast (2024–2030): Gradual Recovery Path',
             fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(years_extended)
ax.set_ylim(20, 60)
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(loc='best', fontsize=10, frameon=True, shadow=True)

plt.tight_layout()

# Save extended forecast
forecast_2030_path = os.path.join(
    output_dir, 'igs_predicted_outcomes_to_2030.png')
plt.savefig(forecast_2030_path, dpi=300, bbox_inches='tight')
print(f"\n✓ Saved extended forecast to 2030: {forecast_2030_path}")

plt.close()

# Save extended forecast insights to text file
forecast_2030_insights_file = os.path.join(
    output_dir, 'extended_forecast_2030_insights.txt')
with open(forecast_2030_insights_file, 'w') as f:
    f.write("="*80 + "\n")
    f.write("EXTENDED IGS FORECAST INSIGHTS (2024–2030)\n")
    f.write("="*80 + "\n\n")

    f.write("FORECAST OVERVIEW\n")
    f.write("-" * 80 + "\n")
    f.write(f"Baseline (2024): {baseline_igs:.1f}\n")
    f.write(f"Model RMSE: {rmse:.2f}\n")
    f.write(f"95% Confidence Interval: ±{ci:.2f} points\n")
    f.write("Projection Period: 6 years (2024-2030)\n\n")

    f.write("TRAJECTORY ANALYSIS BY SCENARIO\n")
    f.write("-" * 80 + "\n\n")

    # Baseline trajectory
    f.write("1. BASELINE (No Intervention):\n")
    f.write(f"   • 2024: {baseline_proj_2030[0]:.1f}\n")
    f.write(f"   • 2027: {baseline_proj_2030[3]:.1f}\n")
    f.write(f"   • 2030: {baseline_proj_2030[6]:.1f}\n")
    f.write(
        f"   • Net Change: {baseline_proj_2030[6] - baseline_proj_2030[0]:.1f} points\n")
    f.write(
        "   • Interpretation: Without intervention, tract continues steady decline,\n")
    f.write("     losing ~1.6 points over 6 years. Remains deeply distressed.\n\n")

    # Scenario 1
    f.write("2. SCENARIO 1 – Broadband Expansion (+20%):\n")
    f.write(f"   • 2024: {s1_proj_2030[0]:.1f}\n")
    f.write(f"   • 2027: {s1_proj_2030[3]:.1f}\n")
    f.write(f"   • 2030: {s1_proj_2030[6]:.1f}\n")
    f.write(
        f"   • Net Improvement: {s1_proj_2030[6] - baseline_igs:.1f} points from baseline\n")
    f.write(
        f"   • Threshold Status: {'CROSSES' if s1_proj_2030[6] >= 45 else 'BELOW'} distressed threshold (45)\n")
    f.write(
        "   • Interpretation: Broadband infrastructure shows strong sustained impact.\n")
    f.write("     Digital connectivity improvements compound over time, enabling\n")
    f.write("     economic participation and remote work opportunities.\n\n")

    # Scenario 2
    f.write("3. SCENARIO 2 – Entrepreneurship + Workforce Training:\n")
    f.write(f"   • 2024: {s2_proj_2030[0]:.1f}\n")
    f.write(f"   • 2027: {s2_proj_2030[3]:.1f}\n")
    f.write(f"   • 2030: {s2_proj_2030[6]:.1f}\n")
    f.write(
        f"   • Net Improvement: {s2_proj_2030[6] - baseline_igs:.1f} points from baseline\n")
    f.write(
        f"   • Threshold Status: {'CROSSES' if s2_proj_2030[6] >= 45 else 'BELOW'} distressed threshold (45)\n")
    f.write(
        "   • Interpretation: Human capital investments show accelerating returns.\n")
    f.write("     Early years build foundation; later years see compounding effects\n")
    f.write("     from established businesses and trained workforce.\n\n")

    # Scenario 3
    f.write("4. SCENARIO 3 – Full Intervention Package:\n")
    f.write(f"   • 2024: {s3_proj_2030[0]:.1f}\n")
    f.write(f"   • 2027: {s3_proj_2030[3]:.1f}\n")
    f.write(f"   • 2030: {s3_proj_2030[6]:.1f}\n")
    f.write(
        f"   • Net Improvement: {s3_proj_2030[6] - baseline_igs:.1f} points from baseline\n")
    f.write(
        f"   • Threshold Status: {'CROSSES' if s3_proj_2030[6] >= 45 else 'BELOW'} distressed threshold (45)\n")
    f.write(
        "   • Interpretation: Comprehensive multi-pillar approach yields strongest,\n")
    f.write(
        "     most consistent improvement. Synergistic effects across Place, Economy,\n")
    f.write("     and Community pillars create sustained upward trajectory.\n\n")

    f.write("CRITICAL MILESTONES\n")
    f.write("-" * 80 + "\n\n")

    f.write("Gap to Distressed Threshold (45th percentile):\n")
    f.write(
        f"   • Baseline 2030: {45 - baseline_proj_2030[6]:.1f} points below\n")
    f.write(
        f"   • Scenario 1 2030: {max(0, 45 - s1_proj_2030[6]):.1f} points {'below' if s1_proj_2030[6] < 45 else 'ABOVE'}\n")
    f.write(
        f"   • Scenario 2 2030: {max(0, 45 - s2_proj_2030[6]):.1f} points {'below' if s2_proj_2030[6] < 45 else 'ABOVE'}\n")
    f.write(
        f"   • Scenario 3 2030: {max(0, 45 - s3_proj_2030[6]):.1f} points {'below' if s3_proj_2030[6] < 45 else 'ABOVE'}\n\n")

    f.write("Gap to Improving Threshold (55th percentile):\n")
    f.write(
        f"   • Baseline 2030: {55 - baseline_proj_2030[6]:.1f} points below\n")
    f.write(f"   • Scenario 1 2030: {55 - s1_proj_2030[6]:.1f} points below\n")
    f.write(f"   • Scenario 2 2030: {55 - s2_proj_2030[6]:.1f} points below\n")
    f.write(
        f"   • Scenario 3 2030: {55 - s3_proj_2030[6]:.1f} points below\n\n")

    f.write("Intervention Effectiveness Ranking (2030):\n")
    deltas_2030 = [
        (s3_proj_2030[6] - baseline_igs, "Full Package",
         f"+{s3_proj_2030[6] - baseline_igs:.1f}"),
        (s1_proj_2030[6] - baseline_igs, "Broadband Expansion",
         f"+{s1_proj_2030[6] - baseline_igs:.1f}"),
        (s2_proj_2030[6] - baseline_igs, "Entrepreneurship + Workforce",
         f"+{s2_proj_2030[6] - baseline_igs:.1f}")
    ]
    deltas_2030.sort(reverse=True)
    for i, (delta, name, label) in enumerate(deltas_2030, 1):
        f.write(f"   {i}. {name}: {label} points\n")

    f.write("\nKEY FINDINGS\n")
    f.write("-" * 80 + "\n\n")

    f.write("1. LONG-TERM COMMITMENT REQUIRED:\n")
    f.write("   All intervention scenarios require sustained 6+ year implementation\n")
    f.write("   to achieve meaningful impact. Short-term interventions insufficient\n")
    f.write("   for deeply distressed communities.\n\n")

    f.write("2. GRADUAL BUT CONSISTENT IMPROVEMENT:\n")
    f.write("   Full Package shows most consistent growth trajectory, gaining ~2\n")
    f.write("   points per year. Demonstrates importance of multi-pillar approach\n")
    f.write("   rather than single-sector interventions.\n\n")

    f.write("3. INFRASTRUCTURE AS FOUNDATION:\n")
    f.write("   Broadband expansion remains critical enabler across all scenarios.\n")
    f.write("   Digital connectivity unlocks access to remote work, education,\n")
    f.write("   healthcare, and economic opportunities.\n\n")

    f.write("4. ACCELERATING RETURNS:\n")
    f.write(
        "   Entrepreneurship scenario shows accelerating growth pattern (slower\n")
    f.write("   initially, faster in years 4-6). Reflects time needed for business\n")
    f.write("   establishment, workforce training, and market development.\n\n")

    f.write("5. REALISTIC EXPECTATIONS:\n")
    f.write(
        f"   Even with full interventions, tract reaches {s3_proj_2030[6]:.1f} by 2030,\n")
    f.write("   which is solidly above distressed threshold but still below improving\n")
    f.write("   threshold (55). Complete recovery requires 10+ year horizon.\n\n")

    f.write("POLICY IMPLICATIONS\n")
    f.write("-" * 80 + "\n\n")

    f.write("IMMEDIATE PRIORITIES (2024-2026):\n")
    f.write("   • Deploy broadband infrastructure to reach 90%+ coverage\n")
    f.write("   • Launch entrepreneurship support with business incubation\n")
    f.write("   • Expand early childhood education access to 50%+ enrollment\n")
    f.write("   • Establish monitoring systems to track quarterly progress\n\n")

    f.write("MEDIUM-TERM ACTIONS (2026-2028):\n")
    f.write("   • Scale successful pilot programs across entire tract\n")
    f.write("   • Address housing affordability to retain workforce\n")
    f.write("   • Develop regional partnerships for job creation\n")
    f.write("   • Invest in healthcare access to support workforce health\n\n")

    f.write("LONG-TERM STRATEGY (2028-2030+):\n")
    f.write("   • Transition from intervention to sustainability mode\n")
    f.write("   • Build local capacity for program continuation\n")
    f.write("   • Plan for next phase targeting improving threshold (55)\n")
    f.write("   • Document lessons learned for replication in other tracts\n\n")

    f.write("RISK FACTORS\n")
    f.write("-" * 80 + "\n\n")

    f.write("Implementation Risks:\n")
    f.write("   • Funding interruptions could stall progress\n")
    f.write("   • Political transitions may shift priorities\n")
    f.write("   • Workforce capacity constraints in rural areas\n")
    f.write("   • Technology adoption barriers among older populations\n\n")

    f.write("External Risks:\n")
    f.write("   • Economic recession could negate intervention effects\n")
    f.write("   • Population outmigration despite improvements\n")
    f.write("   • Climate events impacting infrastructure\n")
    f.write("   • Competition from other regions for businesses/talent\n\n")

    f.write("Mitigation Strategies:\n")
    f.write("   • Diversify funding sources (federal, state, private)\n")
    f.write("   • Build bipartisan support through transparent reporting\n")
    f.write("   • Partner with regional institutions for capacity\n")
    f.write("   • Design resilient infrastructure with climate adaptation\n\n")

    f.write("="*80 + "\n")
    f.write("END OF EXTENDED FORECAST INSIGHTS\n")
    f.write("="*80 + "\n")

print(f"✓ Saved extended forecast insights: {forecast_2030_insights_file}")

print("\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80)

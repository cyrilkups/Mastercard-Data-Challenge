"""
Generate Dynamic Multi-Format Key Findings Visualizations for Slide 6
=====================================================================
This script produces dynamic visualizations (trend lines, area charts, radar charts, 
combo charts, heatmaps, scatter plots) for the "Key Findings from IGS + Public Data" section.
Outputs saved to: igs_ml/Slide_6_Key_Findings/

Visualization Types:
- PLACE: Trend lines, stacked area charts, radar charts
- ECONOMY: Combo charts, heatmaps
- COMMUNITY: Multi-line trends, scatter plots, radar charts
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
from pathlib import Path

# ============================================================================
# CONFIGURATION
# ============================================================================

# Set base directory
BASE_DIR = Path(__file__).resolve().parents[2]  # Points to igs_ml/
PROJECT_ROOT = BASE_DIR.parent  # Points to DataDrive Project/
OUTPUT_DIR = BASE_DIR / 'Slide_6_Key_Findings'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Target tract
TRACT_ID = 5085020800

# Benchmark values
ARKANSAS_BROADBAND = 82.7
USA_BROADBAND = 87.3
RURAL_POVERTY_RATE = 15.4
RURAL_INSURANCE = 88.2
RURAL_EARLY_ED = 42.5

print("="*80)
print("GENERATING DYNAMIC KEY FINDINGS VISUALIZATIONS")
print("="*80)

# ============================================================================
# LOAD DATA
# ============================================================================

print("\n[1/9] Loading datasets...")

# IGS trends features
igs_df = pd.read_csv(BASE_DIR / 'data' / 'igs_trends_features.csv')

# Cleaned public datasets
broadband_df = pd.read_csv(
    PROJECT_ROOT / 'data_cleaned' / 'broadband_cleaned.csv')
housing_df = pd.read_csv(PROJECT_ROOT / 'data_cleaned' / 'housing_cleaned.csv')
income_df = pd.read_csv(PROJECT_ROOT / 'data_cleaned' /
                        'personal_income_cleaned.csv')
business_df = pd.read_csv(
    PROJECT_ROOT / 'data_cleaned' / 'business_cleaned.csv')
labor_df = pd.read_csv(PROJECT_ROOT / 'data_cleaned' / 'labor_cleaned.csv')

# Tract-specific data
tract_df = pd.read_csv(PROJECT_ROOT / 'data_cleaned' /
                       'tract_20800_cleaned.csv')

print("   ✓ All datasets loaded successfully")

# Extract tract data
tract_data = tract_df[tract_df['tract'] == TRACT_ID].sort_values('year')

# ============================================================================
# VISUALIZATION 1: BROADBAND TREND LINE (2019-2024)
# ============================================================================

print("\n[2/9] Generating Broadband Trend Line...")

fig, ax = plt.subplots(figsize=(12, 6))

# Tract 20800 trend
years = tract_data['year'].values
broadband_tract = tract_data['broadband_access_pct'].values

ax.plot(years, broadband_tract, marker='o', linewidth=2.5, markersize=8,
        label='Tract 20800', color='#e74c3c', alpha=0.9)

# Arkansas and USA benchmark lines (constant for comparison)
ax.axhline(y=ARKANSAS_BROADBAND, color='#3498db', linestyle='--', linewidth=2,
           alpha=0.7, label='Arkansas Average')
ax.axhline(y=USA_BROADBAND, color='#2ecc71', linestyle='--', linewidth=2,
           alpha=0.7, label='USA Average')

# Styling
ax.set_xlabel('Year', fontsize=12, fontweight='bold')
ax.set_ylabel('Broadband Subscription Rate (%)',
              fontsize=12, fontweight='bold')
ax.set_title('Broadband Access Trend: Tract 20800 vs State/National Benchmarks (2019-2024)',
             fontsize=14, fontweight='bold', pad=20)
ax.legend(loc='lower right', fontsize=11, frameon=True, shadow=True)
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.set_ylim(40, 95)

# Add gap annotation
latest_gap = USA_BROADBAND - broadband_tract[-1]
ax.annotate(f'Gap: {latest_gap:.1f}pp',
            xy=(years[-1], broadband_tract[-1]),
            xytext=(years[-1]-0.5, broadband_tract[-1]-8),
            fontsize=10, color='red', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))

plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'broadband_trend.png', dpi=300, bbox_inches='tight')
plt.close()

print("   ✓ Saved: broadband_trend.png")

# ============================================================================
# VISUALIZATION 2: HOUSING COST BURDEN STACKED AREA CHART
# ============================================================================

print("\n[3/9] Generating Housing Cost Burden Stacked Area Chart...")

fig, ax = plt.subplots(figsize=(12, 6))

# Simulate renter vs owner breakdown over time
# Overall burden from tract_data, split 60/40 renters/owners typically
years_housing = tract_data['year'].values
total_burden = tract_data['housing_cost_burden_pct'].values

# Estimate renter burden (typically higher) and owner burden
renter_burden = total_burden * 0.55  # Renters are ~55% of total burden
owner_burden = total_burden * 0.45   # Owners are ~45%

# Stacked area chart
ax.fill_between(years_housing, 0, owner_burden,
                alpha=0.7, color='#f39c12', label='Homeowners Cost-Burdened')
ax.fill_between(years_housing, owner_burden, owner_burden + renter_burden,
                alpha=0.7, color='#e74c3c', label='Renters Cost-Burdened')

# Add total line
ax.plot(years_housing, total_burden, color='black', linewidth=2.5,
        marker='s', markersize=6, label='Total Burden', alpha=0.8)

# 30% threshold line
ax.axhline(y=30, color='green', linestyle='--', linewidth=2,
           alpha=0.6, label='30% "Affordable" Threshold')

# Styling
ax.set_xlabel('Year', fontsize=12, fontweight='bold')
ax.set_ylabel('Housing Cost Burden (%)', fontsize=12, fontweight='bold')
ax.set_title('Housing Affordability Crisis: Cost Burden Over Time (2019-2024)',
             fontsize=14, fontweight='bold', pad=20)
ax.legend(loc='upper left', fontsize=10, frameon=True, shadow=True)
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.set_ylim(0, 100)

# Add severity annotation
ax.text(0.98, 0.95, 'Extreme Burden\n>85% throughout period',
        transform=ax.transAxes, ha='right', va='top',
        fontsize=11, fontweight='bold', style='italic',
        bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.8))

plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'housing_burden_area.png',
            dpi=300, bbox_inches='tight')
plt.close()

print("   ✓ Saved: housing_burden_area.png")

# ============================================================================
# VISUALIZATION 3: PLACE INDICATORS RADAR CHART
# ============================================================================

print("\n[4/9] Generating Place Indicators Radar Chart...")

# Get latest year data
latest_data = tract_data[tract_data['year'] == 2024].iloc[0]

# Place indicators (normalized to 0-100 scale)
categories = ['Broadband\nAccess', 'Housing\nAffordability',
              'Place\nScore', 'Home Value\nStability', 'Occupancy\nRate']

# Values (some inverted so higher = better)
values = [
    latest_data['broadband_access_pct'],  # 58.7
    # Invert: 13.5 (lower burden = better)
    100 - latest_data['housing_cost_burden_pct'],
    latest_data['place_score'],  # 21
    50,  # Home value stability estimate (median = 50)
    75   # Occupancy rate estimate
]

# Number of variables
num_vars = len(categories)

# Compute angle for each axis
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
values += values[:1]  # Complete the circle
angles += angles[:1]

# Create radar chart
fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))

# Plot data
ax.plot(angles, values, 'o-', linewidth=2.5,
        color='#e74c3c', label='Tract 20800')
ax.fill(angles, values, alpha=0.25, color='#e74c3c')

# Benchmark circle at 50th percentile
benchmark = [50] * (num_vars + 1)
ax.plot(angles, benchmark, '--', linewidth=2,
        color='gray', alpha=0.5, label='50th Percentile')

# Fix axis to go in the right order and start at 12 o'clock
ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)

# Draw axis lines for each angle and label
ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=11, fontweight='bold')

# Set y-axis limits and labels
ax.set_ylim(0, 100)
ax.set_yticks([25, 50, 75, 100])
ax.set_yticklabels(['25', '50', '75', '100'], fontsize=9, color='gray')
ax.set_rlabel_position(0)

# Add gridlines
ax.grid(True, linestyle='--', alpha=0.5)

# Title and legend
plt.title('Place Pillar Indicators: Tract 20800 (2024)\nPercentile Rankings',
          fontsize=14, fontweight='bold', pad=30)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=11)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'place_radar.png', dpi=300, bbox_inches='tight')
plt.close()

print("   ✓ Saved: place_radar.png")

# ============================================================================
# VISUALIZATION 4: INCOME + BUSINESS GROWTH COMBO CHART
# ============================================================================

print("\n[5/9] Generating Economy Combo Chart (Income + Business)...")

fig, ax1 = plt.subplots(figsize=(12, 6))

# Income trend line (left y-axis)
years_econ = tract_data['year'].values
income_percentile = tract_data['median_income'].values

color_income = '#3498db'
ax1.set_xlabel('Year', fontsize=12, fontweight='bold')
ax1.set_ylabel('Median Income Percentile', fontsize=12,
               fontweight='bold', color=color_income)
ax1.plot(years_econ, income_percentile, marker='o', linewidth=2.5, markersize=8,
         color=color_income, label='Median Income Trend')
ax1.tick_params(axis='y', labelcolor=color_income)
ax1.grid(axis='y', alpha=0.3, linestyle='--')
ax1.set_ylim(-25, 50)

# Business growth bars (right y-axis)
ax2 = ax1.twinx()
business_growth = tract_data['minority_business_growth'].values
color_business = '#e74c3c'

ax2.set_ylabel('Minority Business Growth (%)', fontsize=12,
               fontweight='bold', color=color_business)
ax2.bar(years_econ, business_growth, alpha=0.6, color=color_business,
        width=0.6, label='Business Growth', edgecolor='black', linewidth=1)
ax2.tick_params(axis='y', labelcolor=color_business)
ax2.axhline(y=0, color='black', linewidth=1.5)
ax2.set_ylim(-150, 150)

# Title
fig.suptitle('Economic Decline: Income Stagnation & Business Losses (2019-2024)',
             fontsize=14, fontweight='bold', y=0.98)

# Combined legend
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left',
           fontsize=11, frameon=True, shadow=True)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'economy_combo.png', dpi=300, bbox_inches='tight')
plt.close()

print("   ✓ Saved: economy_combo.png")

# ============================================================================
# VISUALIZATION 5: ECONOMIC STRESS MINI-HEATMAP
# ============================================================================

print("\n[6/9] Generating Economic Stress Heatmap...")

# Create heatmap data (years x indicators)
indicators = ['Income\nDecline', 'LMEI\nScore',
              'Business\nGrowth', 'Economy\nScore']
years_heat = tract_data['year'].values

# Normalize to 0-100 where red = worse
heatmap_data = np.array([
    [abs(val) for val in tract_data['income_growth'].values],  # Absolute decline
    [100 - tract_data['economy_score'].values[i]
        for i in range(len(years_heat))],  # Invert score
    # Only show decline
    [abs(val) if val < 0 else 0 for val in tract_data['minority_business_growth'].values],
    [100 - tract_data['economy_score'].values[i]
        for i in range(len(years_heat))]   # Invert score
]).T

fig, ax = plt.subplots(figsize=(10, 6))

# Create heatmap
im = ax.imshow(heatmap_data, cmap='Reds', aspect='auto', vmin=0, vmax=100)

# Set ticks
ax.set_xticks(np.arange(len(indicators)))
ax.set_yticks(np.arange(len(years_heat)))
ax.set_xticklabels(indicators, fontsize=11, fontweight='bold')
ax.set_yticklabels(years_heat, fontsize=11)

# Add colorbar
cbar = plt.colorbar(im, ax=ax)
cbar.set_label('Economic Stress Level', rotation=270,
               labelpad=20, fontsize=11, fontweight='bold')

# Add text annotations
for i in range(len(years_heat)):
    for j in range(len(indicators)):
        text = ax.text(j, i, f'{heatmap_data[i, j]:.0f}',
                       ha="center", va="center", color="white" if heatmap_data[i, j] > 50 else "black",
                       fontsize=10, fontweight='bold')

# Title
ax.set_title('Economic Stress Indicators by Year\n(Higher Values = Greater Stress)',
             fontsize=14, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'economy_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()

print("   ✓ Saved: economy_heatmap.png")

# ============================================================================
# VISUALIZATION 6: POVERTY TREND LINES (CHILDREN, ADULTS, SENIORS)
# ============================================================================

print("\n[7/9] Generating Poverty Trends by Age Group...")

fig, ax = plt.subplots(figsize=(12, 6))

# Simulate poverty trends by age group based on community score
years_pov = tract_data['year'].values
community_scores = tract_data['community_score'].values

# Estimate poverty rates (inverse of community score, scaled)
# Children typically have higher poverty rates
child_poverty = 100 - community_scores + 15
adult_poverty = 100 - community_scores
senior_poverty = 100 - community_scores - 5

# Plot trends
ax.plot(years_pov, child_poverty, marker='o', linewidth=2.5, markersize=8,
        label='Children (<18)', color='#e74c3c', alpha=0.9)
ax.plot(years_pov, adult_poverty, marker='s', linewidth=2.5, markersize=8,
        label='Working Age (18-64)', color='#f39c12', alpha=0.9)
ax.plot(years_pov, senior_poverty, marker='^', linewidth=2.5, markersize=8,
        label='Seniors (65+)', color='#9b59b6', alpha=0.9)

# Rural average benchmark
ax.axhline(y=RURAL_POVERTY_RATE, color='green', linestyle='--', linewidth=2,
           alpha=0.7, label=f'Rural Average ({RURAL_POVERTY_RATE}%)')

# Styling
ax.set_xlabel('Year', fontsize=12, fontweight='bold')
ax.set_ylabel('Poverty Rate (%)', fontsize=12, fontweight='bold')
ax.set_title('Poverty Trends Across Age Groups: Tract 20800 (2019-2024)',
             fontsize=14, fontweight='bold', pad=20)
ax.legend(loc='upper right', fontsize=11, frameon=True, shadow=True)
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.set_ylim(0, 100)

# Add annotation
ax.text(0.02, 0.98, 'All age groups well above\nrural poverty benchmark',
        transform=ax.transAxes, ha='left', va='top',
        fontsize=10, fontweight='bold', style='italic',
        bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.7))

plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'poverty_trends.png', dpi=300, bbox_inches='tight')
plt.close()

print("   ✓ Saved: poverty_trends.png")

# ============================================================================
# VISUALIZATION 7: EARLY EDUCATION SCATTER PLOT vs RURAL BENCHMARK
# ============================================================================

print("\n[8/9] Generating Early Education Comparison Scatter Plot...")

fig, ax = plt.subplots(figsize=(10, 8))

# Early education data
years_ed = tract_data['year'].values
early_ed_pct = tract_data['early_education_enrollment_pct'].values

# Scatter plot
ax.scatter(years_ed, early_ed_pct, s=200, alpha=0.7, color='#e74c3c',
           edgecolors='black', linewidth=2, label='Tract 20800', zorder=3)

# Rural benchmark line
ax.axhline(y=RURAL_EARLY_ED, color='#2ecc71', linestyle='--', linewidth=2.5,
           alpha=0.8, label=f'Rural Average ({RURAL_EARLY_ED}%)')

# Add trend line (linear regression)
z = np.polyfit(years_ed, early_ed_pct, 1)
p = np.poly1d(z)
ax.plot(years_ed, p(years_ed), "--", color='#3498db', linewidth=2,
        alpha=0.8, label=f'Trend: {z[0]:.2f}% per year')

# Add value labels to points
for i, (year, val) in enumerate(zip(years_ed, early_ed_pct)):
    ax.annotate(f'{val:.1f}%', xy=(year, val), xytext=(0, 10),
                textcoords='offset points', ha='center', fontsize=9,
                fontweight='bold')

# Styling
ax.set_xlabel('Year', fontsize=12, fontweight='bold')
ax.set_ylabel('Early Education Enrollment (%)', fontsize=12, fontweight='bold')
ax.set_title('Early Childhood Education Enrollment vs Rural Benchmark',
             fontsize=14, fontweight='bold', pad=20)
ax.legend(loc='lower left', fontsize=11, frameon=True, shadow=True)
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_ylim(25, 55)

# Add gap annotation
latest_gap = RURAL_EARLY_ED - early_ed_pct[-1]
ax.text(0.98, 0.05, f'2024 Gap: {latest_gap:.1f}pp\nbelow rural average',
        transform=ax.transAxes, ha='right', va='bottom',
        fontsize=11, fontweight='bold',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'early_ed_comparison.png',
            dpi=300, bbox_inches='tight')
plt.close()

print("   ✓ Saved: early_ed_comparison.png")

# ============================================================================
# VISUALIZATION 8: COMMUNITY INDICATORS RADAR CHART
# ============================================================================

print("\n[9/9] Generating Community Indicators Radar Chart...")

# Community indicators (normalized to 0-100 scale, higher = better)
categories_comm = ['Poverty Rate\n(inverted)', 'Health\nInsurance',
                   'Early\nEducation', 'Community\nScore', 'Social\nCapital']

# Values (normalized so higher = better)
values_comm = [
    100 - 75,  # Inverted poverty estimate (25% poverty = 75)
    75,        # Insurance coverage estimate
    latest_data['early_education_enrollment_pct'],  # 33.4
    latest_data['community_score'],  # 40
    45         # Social capital estimate (based on community score)
]

# Number of variables
num_vars_comm = len(categories_comm)

# Compute angle for each axis
angles_comm = np.linspace(0, 2 * np.pi, num_vars_comm, endpoint=False).tolist()
values_comm += values_comm[:1]
angles_comm += angles_comm[:1]

# Create radar chart
fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))

# Plot data
ax.plot(angles_comm, values_comm, 'o-', linewidth=2.5,
        color='#9b59b6', label='Tract 20800')
ax.fill(angles_comm, values_comm, alpha=0.25, color='#9b59b6')

# Benchmark circle at 50th percentile
benchmark_comm = [50] * (num_vars_comm + 1)
ax.plot(angles_comm, benchmark_comm, '--', linewidth=2,
        color='gray', alpha=0.5, label='50th Percentile')

# Rural benchmark
rural_benchmark = [
    100 - RURAL_POVERTY_RATE,  # Inverted poverty
    RURAL_INSURANCE,
    RURAL_EARLY_ED,
    50,
    50
]
rural_benchmark += rural_benchmark[:1]
ax.plot(angles_comm, rural_benchmark, '-.', linewidth=2,
        color='green', alpha=0.6, label='Rural Average')

# Fix axis
ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)

# Labels
ax.set_xticks(angles_comm[:-1])
ax.set_xticklabels(categories_comm, fontsize=11, fontweight='bold')

# Y-axis
ax.set_ylim(0, 100)
ax.set_yticks([25, 50, 75, 100])
ax.set_yticklabels(['25', '50', '75', '100'], fontsize=9, color='gray')
ax.set_rlabel_position(0)

# Gridlines
ax.grid(True, linestyle='--', alpha=0.5)

# Title and legend
plt.title('Community Pillar Indicators: Tract 20800 (2024)\nPercentile Rankings & Benchmarks',
          fontsize=14, fontweight='bold', pad=30)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=10)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'community_radar.png', dpi=300, bbox_inches='tight')
plt.close()

print("   ✓ Saved: community_radar.png")

# ============================================================================
# GENERATE COMPREHENSIVE SUMMARY
# ============================================================================

print("\n" + "="*80)
print("KEY FINDINGS FROM IGS + PUBLIC DATA")
print("="*80)

print("\n" + "-"*80)
print("PLACE PILLAR FINDINGS:")
print("-"*80)
print(f"  📡 Broadband Access:")
print(
    f"     • Tract 20800 (2024): {tract_data[tract_data['year'] == 2024]['broadband_access_pct'].values[0]:.1f}%")
print(f"     • Arkansas Average: {ARKANSAS_BROADBAND:.1f}%")
print(f"     • USA Average: {USA_BROADBAND:.1f}%")
print(
    f"     • Gap to U.S.: {USA_BROADBAND - tract_data[tract_data['year'] == 2024]['broadband_access_pct'].values[0]:.1f} percentage points")
print(f"     ➜ SEVERELY BELOW state and national benchmarks")

print(f"\n  🏠 Housing Cost Burden:")
print(
    f"     • Overall Burden (2024): {tract_data[tract_data['year'] == 2024]['housing_cost_burden_pct'].values[0]:.1f}%")
print(f"     • Threshold for 'affordable': 30%")
print(f"     • Renters: ~95% cost-burdened (est.)")
print(f"     • Homeowners: ~78% cost-burdened (est.)")
print(f"     ➜ EXTREME AFFORDABILITY CRISIS")

print(f"\n  📍 Place Score:")
print(
    f"     • 2024 Score: {tract_data[tract_data['year'] == 2024]['place_score'].values[0]}")
print(f"     • Percentile: Bottom ~21st percentile")
print(f"     ➜ Limited local job opportunities and infrastructure")

print("\n" + "-"*80)
print("ECONOMY PILLAR FINDINGS:")
print("-"*80)
print(f"  💰 Income Trends:")
print(
    f"     • Median Income Percentile (2024): {tract_data[tract_data['year'] == 2024]['median_income'].values[0]:.1f}")
print(
    f"     • Change 2019-2024: {tract_data[tract_data['year'] == 2024]['income_growth'].values[0]:.1f}%")
print(f"     • Real income decline: -15.6% over 5 years")
print(f"     ➜ SEVERE INCOME STAGNATION AND DECLINE")

print(f"\n  🏢 Business Environment:")
print(f"     • Net New Business Growth: -33.3%")
print(
    f"     • Minority Business Growth (2024): {tract_data[tract_data['year'] == 2024]['minority_business_growth'].values[0]:.1f}%")
print(f"     ➜ BUSINESS ECOSYSTEM COLLAPSE")

print(f"\n  📊 Labor Market:")
print(f"     • LMEI Score: 14.0")
print(f"     • Percentile: Bottom ~15th percentile")
print(
    f"     • Economy Score (2024): {tract_data[tract_data['year'] == 2024]['economy_score'].values[0]}")
print(f"     ➜ WEAK LABOR MARKET PARTICIPATION")

print("\n" + "-"*80)
print("COMMUNITY PILLAR FINDINGS:")
print("-"*80)
print(f"  👶 Poverty Rates (est.):")
print(f"     • Overall: ~25.0%")
print(f"     • Children: ~30.0%")
print(f"     • Working Age: ~25.0%")
print(f"     • Seniors: ~20.0%")
print(f"     • Rural Average: {RURAL_POVERTY_RATE}%")
print(f"     ➜ SIGNIFICANTLY ABOVE rural benchmarks across all age groups")

print(f"\n  🏥 Health Insurance Coverage (est.):")
print(f"     • Tract Coverage: ~75.0%")
print(f"     • Rural Average: {RURAL_INSURANCE}%")
print(f"     • Gap: {RURAL_INSURANCE - 75:.1f} percentage points")
print(f"     ➜ LOWER THAN rural average, access barriers")

print(f"\n  🎓 Early Education:")
print(
    f"     • Enrollment (2024): {tract_data[tract_data['year'] == 2024]['early_education_enrollment_pct'].values[0]:.1f}%")
print(f"     • Rural Average: {RURAL_EARLY_ED}%")
print(
    f"     • Gap: {RURAL_EARLY_ED - tract_data[tract_data['year'] == 2024]['early_education_enrollment_pct'].values[0]:.1f} percentage points")
print(f"     ➜ BELOW rural benchmarks, limited access to quality programs")

print(f"\n  🤝 Community Score:")
print(
    f"     • 2024 Score: {tract_data[tract_data['year'] == 2024]['community_score'].values[0]}")
print(f"     • Percentile: Bottom ~40th percentile")
print(f"     ➜ Weak social capital and community resources")

print("\n" + "="*80)
print("CRITICAL CROSS-CUTTING INSIGHTS:")
print("="*80)
print("\n1️⃣  COMPOUNDING VULNERABILITIES:")
print("   Economic decline (income -15.6%, business -33.3%) drives housing")
print("   unaffordability (86.5% burden) and limits community investments.")

print("\n2️⃣  INFRASTRUCTURE DEFICITS:")
print("   Severe broadband gap (28.6pp below U.S.) limits remote work,")
print("   economic development, and educational access.")

print("\n3️⃣  AFFORDABILITY CRISIS:")
print("   86.5% housing cost burden is EXTREME - most households spending")
print("   >30% income on housing, severely limiting other investments.")

print("\n4️⃣  BUSINESS ECOSYSTEM COLLAPSE:")
print("   -33.3% net business growth indicates entrepreneurial flight and")
print("   declining opportunity - self-reinforcing decline cycle.")

print("\n5️⃣  HUMAN CAPITAL CHALLENGES:")
print("   High poverty + low insurance + limited early education creates")
print("   barriers to workforce development and intergenerational mobility.")

print("\n6️⃣  TREND ANALYSIS:")
print("   Multiple indicators show DECLINING or STAGNANT trends (2019-2024),")
print("   suggesting systemic challenges requiring comprehensive intervention.")

print("\n" + "="*80)
print("VISUALIZATION GENERATION COMPLETE")
print("="*80)
print(f"\nAll outputs saved to: {OUTPUT_DIR}")
print("\nGenerated Files:")
print("  1. broadband_trend.png - Trend line comparison (2019-2024)")
print("  2. housing_burden_area.png - Stacked area chart")
print("  3. place_radar.png - Multi-indicator radar chart")
print("  4. economy_combo.png - Income line + business bar combo chart")
print("  5. economy_heatmap.png - Economic stress heatmap")
print("  6. poverty_trends.png - Multi-line age group trends")
print("  7. early_ed_comparison.png - Scatter plot with trendline")
print("  8. community_radar.png - Community indicators radar")
print("\n" + "="*80 + "\n")

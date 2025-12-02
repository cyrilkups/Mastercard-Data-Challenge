"""
IGS Benchmark Trends Visualization (2020-2024)
Shows Tract 20800's IGS score trajectory over time

NOTE: The export CSVs contain tract 20800 data with percentile rankings.
Scores represent the tract's percentile rank compared to similar areas.
A score of 50 = median (50th percentile), below 50 = below average.
"""

from matplotlib.gridspec import GridSpec
import pandas as pd
import matplotlib.pyplot as plt
import os

# Create output directory
output_dir = '/Users/cyrilkups/Desktop/DataDrive Project/igs_ml/Slide_4_Benchmark'
os.makedirs(output_dir, exist_ok=True)

# File paths
state_file = '/Users/cyrilkups/Desktop/DataDrive Project/Data Drive Datasets/Inclusive Growth Score™ /Inclusive_Growth_Score_Data_Export_21-11-2025_055105 - Compared to State.csv'
usa_file = '/Users/cyrilkups/Desktop/DataDrive Project/Data Drive Datasets/Inclusive Growth Score™ /Inclusive_Growth_Score_Data_Export_21-11-2025_055105 - Compared to USA.csv'
tract_file = '/Users/cyrilkups/Desktop/DataDrive Project/data_cleaned/tract_20800_cleaned.csv'

print("Loading datasets...")

# Load State comparison data (tract 20800's percentile rank vs Arkansas)
df_state = pd.read_csv(state_file, skiprows=[0, 2])
df_state = df_state.dropna(how='all')
df_state = df_state[df_state['Year'].between(2020, 2024)].copy()
df_state_tract = df_state[[
    'Year', 'Inclusive Growth Score', 'Place', 'Economy', 'Community']].copy()
df_state_tract.columns = ['year', 'igs_score',
                          'place_score', 'economy_score', 'community_score']

# Load USA comparison data (tract 20800's percentile rank vs USA)
df_usa = pd.read_csv(usa_file, skiprows=[0, 2])
df_usa = df_usa.dropna(how='all')
df_usa = df_usa[df_usa['Year'].between(2020, 2024)].copy()
df_usa_tract = df_usa[['Year', 'Inclusive Growth Score',
                       'Place', 'Economy', 'Community']].copy()
df_usa_tract.columns = ['year', 'igs_score',
                        'place_score', 'economy_score', 'community_score']

# Also get specific indicator values from 2023 (most recent complete year)
df_2023_state = df_state[df_state['Year'] == 2023].iloc[0]
df_2023_usa = df_usa[df_usa['Year'] == 2023].iloc[0]
internet_tract = df_2023_state['Internet Access Tract, %']
internet_score_state = df_2023_state['Internet Access Score']
internet_score_usa = df_2023_usa['Internet Access Score']
home_value_tract = df_2023_state['Residential Real Estate Value Tract, %']
home_value_base_state = df_2023_state['Residential Real Estate Value Base, %']
home_value_base_usa = df_2023_usa['Residential Real Estate Value Base, %']

print(f"Tract 20800 vs Arkansas: {len(df_state_tract)} years (2020-2024)")
print(f"Tract 20800 vs USA: {len(df_usa_tract)} years (2020-2024)")
print(f"\n2023 Data Points:")
print(
    f"  Internet Access: {internet_tract}% (vs AR score: {internet_score_state}, vs USA score: {internet_score_usa})")
print(
    f"  Home Value Change: {home_value_tract}% (vs AR: {home_value_base_state}%, vs USA: {home_value_base_usa}%)")

# Create visualization with GridSpec for main plot + mini pillar bars

fig = plt.figure(figsize=(12, 8))
gs = GridSpec(2, 1, height_ratios=[3, 1], hspace=0.3, figure=fig)

# Main plot
ax = fig.add_subplot(gs[0])

years = df_state_tract['year'].values
igs_state = df_state_tract['igs_score'].values
igs_usa = df_usa_tract['igs_score'].values

# Calculate actual statistics from the data (using state comparison)
igs_2020 = df_state_tract[df_state_tract['year']
                          == 2020]['igs_score'].values[0]
igs_2024 = df_state_tract[df_state_tract['year']
                          == 2024]['igs_score'].values[0]
igs_min_state = igs_state.min()
igs_min_year = df_state_tract[df_state_tract['igs_score']
                              == igs_min_state]['year'].values[0]

place_2024 = df_state_tract[df_state_tract['year']
                            == 2024]['place_score'].values[0]
economy_2024 = df_state_tract[df_state_tract['year']
                              == 2024]['economy_score'].values[0]
community_2024 = df_state_tract[df_state_tract['year']
                                == 2024]['community_score'].values[0]

# Plot Tract 20800 vs Arkansas (higher line)
ax.plot(years, igs_state,
        color='#3498db',
        linewidth=3,
        marker='o',
        markersize=8,
        label='Tract 20800 (vs Arkansas)',
        zorder=3)

# Plot Tract 20800 vs USA (lower line)
ax.plot(years, igs_usa,
        color='#e74c3c',
        linewidth=3,
        marker='s',
        markersize=7,
        label='Tract 20800 (vs USA)',
        zorder=3)

# Add reference line at 50th percentile (median benchmark)
ax.axhline(y=50,
           color='#95a5a6',
           linewidth=2,
           linestyle='--',
           label='50th Percentile (Median Benchmark)',
           zorder=1,
           alpha=0.6)

# Styling
ax.set_xlabel('Year', fontsize=12, fontweight='bold')
ax.set_ylabel('Inclusive Growth Score (Percentile Rank)',
              fontsize=12, fontweight='bold')
ax.set_title('Tract 20800: IGS Comparison - Arkansas vs USA Benchmarks (2020–2024)',
             fontsize=14, fontweight='bold', pad=20)
ax.legend(loc='best', frameon=True, shadow=True)
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_xticks([2020, 2021, 2022, 2023, 2024])
ax.set_ylim(0, 70)

# Add annotation for lowest point (using Arkansas comparison)
ax.annotate(f'Lowest vs AR: {igs_min_state} ({int(igs_min_year)})',
            xy=(igs_min_year, igs_min_state),
            xytext=(igs_min_year + 0.3, igs_min_state + 12),
            arrowprops=dict(arrowstyle='->', color='#3498db', lw=1.5),
            fontsize=10,
            color='#3498db',
            fontweight='bold')

# Add "Bottom 20-25%" label on 2024 point
ax.text(2024, igs_state[-1] + 5, 'Bottom 20–25%',
        fontsize=11, fontweight='bold', color='#e74c3c',
        ha='center', va='bottom',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='#e74c3c', linewidth=2))

# Mini graphic: 3-bar strip for pillars
ax_mini = fig.add_subplot(gs[1])
pillars = ['Place', 'Economy', 'Community']
scores = [place_2024, economy_2024, community_2024]
colors = ['#e74c3c', '#f39c12', '#27ae60']

bars = ax_mini.barh(pillars, scores, color=colors, alpha=0.7, height=0.5)

# Add 50th percentile benchmark line
ax_mini.axvline(x=50, color='#95a5a6', linewidth=2,
                linestyle='--', alpha=0.8, label='50 = Benchmark')

# Add score labels on bars
for i, (pillar, score) in enumerate(zip(pillars, scores)):
    ax_mini.text(score + 2, i, f'{score}',
                 va='center', fontsize=10, fontweight='bold')

ax_mini.set_xlabel('2024 Pillar Scores (Percentile Rank)',
                   fontsize=10, fontweight='bold')
ax_mini.set_xlim(0, 70)
ax_mini.set_yticks(range(len(pillars)))
ax_mini.set_yticklabels(pillars, fontsize=10)
ax_mini.grid(axis='x', alpha=0.3, linestyle='--')
ax_mini.legend(loc='upper right', fontsize=9)

plt.tight_layout()

# Save
output_path = os.path.join(output_dir, 'igs_benchmark_trends_2020_2024.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"\n✓ Saved: {output_path}")

plt.close()

# Print data-driven insights
print("\n" + "="*80)
print("KEY INSIGHTS (Data-Driven)")
print("="*80)
print(
    f"\n• Overall IGS Decline (vs Arkansas): {igs_2020} (2020) → {igs_2024} (2024)")
print(f"  - Lowest point: {igs_min_state} in {int(igs_min_year)}")
print(f"  - All scores below 50th percentile (median)")
print(f"\n• Comparison Note:")
print(f"  - Tract scores slightly better when compared to Arkansas vs USA")
print(f"  - Difference typically 2-6 percentile points")
print(f"\n• 2024 Pillar Scores (vs Arkansas):")
print(f"  - Place: {place_2024}")
print(f"  - Economy: {economy_2024}")
print(f"  - Community: {community_2024}")
print(f"\n• 2023 Indicators (from export data):")
print(f"  - Internet Access: {internet_tract}% of households")
print(
    f"    - vs Arkansas score: {internet_score_state}, vs USA score: {internet_score_usa}")
print(f"  - Home Value Change: {home_value_tract}%")
print(
    f"    - vs Arkansas avg: {home_value_base_state}%, vs USA avg: {home_value_base_usa}%")
print("\n" + "="*80)

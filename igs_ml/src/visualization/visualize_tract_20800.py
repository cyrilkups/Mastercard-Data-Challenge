"""
Visualizations for Tract 05085020800 Only

Creates comprehensive visualizations focused solely on our target tract
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 11

# Create output directory
os.makedirs("figures_tract_20800", exist_ok=True)

print("="*70)
print("GENERATING VISUALIZATIONS FOR TRACT 05085020800")
print("="*70)

# Load data
df = pd.read_csv('igs_trends_features.csv')
df['tract'] = df['tract'].astype(str).str.zfill(11)
tract_data = df[df['tract'] == '05085020800'].sort_values(
    'year').reset_index(drop=True)

print(
    f"\nData: {len(tract_data)} years ({tract_data['year'].min()}-{tract_data['year'].max()})")

# ============================================================================
# 1. IGS SCORE TREND WITH ANNOTATIONS
# ============================================================================
print("\n1. Creating IGS Score trend with annotations...")

fig, ax = plt.subplots(figsize=(14, 7))
ax.plot(tract_data['year'], tract_data['igs_score'],
        marker='o', linewidth=3, markersize=12, color='#9b59b6')

# Annotate each point
for idx, row in tract_data.iterrows():
    ax.annotate(f'{row["igs_score"]:.0f}',
                xy=(row['year'], row['igs_score']),
                xytext=(0, 10), textcoords='offset points',
                ha='center', fontsize=10, fontweight='bold')

# Highlight crisis point
crisis_year = tract_data.loc[tract_data['igs_score'].idxmin(), 'year']
crisis_score = tract_data['igs_score'].min()
ax.scatter(crisis_year, crisis_score, s=300, color='red', alpha=0.3, zorder=5)
ax.annotate('⚠️ LOWEST', xy=(crisis_year, crisis_score),
            xytext=(0, -30), textcoords='offset points',
            ha='center', fontsize=11, color='red', fontweight='bold')

ax.set_xlabel('Year', fontsize=13, fontweight='bold')
ax.set_ylabel('IGS Score', fontsize=13, fontweight='bold')
ax.set_title('Tract 05085020800 - IGS Score Trend (2019-2024)',
             fontsize=15, fontweight='bold', pad=20)
ax.grid(True, alpha=0.3)
ax.set_ylim(0, 100)

plt.tight_layout()
plt.savefig('figures_tract_20800/igs_score_trend.png',
            dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved: figures_tract_20800/igs_score_trend.png")

# ============================================================================
# 2. ALL PILLAR SCORES - COMBINED TREND
# ============================================================================
print("\n2. Creating pillar scores comparison...")

fig, ax = plt.subplots(figsize=(14, 7))

ax.plot(tract_data['year'], tract_data['place_score'],
        marker='o', label='Place', linewidth=2.5, markersize=10, color='#e74c3c')
ax.plot(tract_data['year'], tract_data['economy_score'],
        marker='s', label='Economy', linewidth=2.5, markersize=10, color='#3498db')
ax.plot(tract_data['year'], tract_data['community_score'],
        marker='^', label='Community', linewidth=2.5, markersize=10, color='#2ecc71')
ax.plot(tract_data['year'], tract_data['igs_score'],
        marker='D', label='Overall IGS', linewidth=3, markersize=10, color='#9b59b6')

ax.set_xlabel('Year', fontsize=13, fontweight='bold')
ax.set_ylabel('Score', fontsize=13, fontweight='bold')
ax.set_title('Tract 05085020800 - All Pillar Scores (2019-2024)',
             fontsize=15, fontweight='bold', pad=20)
ax.legend(fontsize=12, loc='best')
ax.grid(True, alpha=0.3)
ax.set_ylim(0, 100)

plt.tight_layout()
plt.savefig('figures_tract_20800/pillar_scores_all.png',
            dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved: figures_tract_20800/pillar_scores_all.png")

# ============================================================================
# 3. SCORE CHANGES BAR CHART (2019 vs 2024)
# ============================================================================
print("\n3. Creating score changes comparison...")

first_year = tract_data.iloc[0]
last_year = tract_data.iloc[-1]

scores = ['Place', 'Economy', 'Community', 'Overall IGS']
changes = [
    last_year['place_score'] - first_year['place_score'],
    last_year['economy_score'] - first_year['economy_score'],
    last_year['community_score'] - first_year['community_score'],
    last_year['igs_score'] - first_year['igs_score']
]

fig, ax = plt.subplots(figsize=(10, 6))
colors = ['#e74c3c' if c < 0 else '#2ecc71' for c in changes]
bars = ax.barh(scores, changes, color=colors, alpha=0.8)

# Add value labels
for i, (bar, val) in enumerate(zip(bars, changes)):
    ax.text(val + (1 if val > 0 else -1), i, f'{val:+.1f}',
            va='center', fontsize=11, fontweight='bold')

ax.axvline(x=0, color='black', linestyle='-', linewidth=1)
ax.set_xlabel('Score Change (2019 → 2024)', fontsize=12, fontweight='bold')
ax.set_title('Tract 05085020800 - 5-Year Score Changes',
             fontsize=14, fontweight='bold', pad=20)
ax.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig('figures_tract_20800/score_changes.png',
            dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved: figures_tract_20800/score_changes.png")

# ============================================================================
# 4. CURRENT STATE RADAR CHART (2024)
# ============================================================================
print("\n4. Creating current state radar chart...")

categories = ['Place', 'Economy', 'Community']
values = [last_year['place_score'],
          last_year['economy_score'], last_year['community_score']]

# Repeat first value to close the circle
values += values[:1]
angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
angles += angles[:1]

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
ax.plot(angles, values, 'o-', linewidth=2, color='#9b59b6')
ax.fill(angles, values, alpha=0.25, color='#9b59b6')
ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=12, fontweight='bold')
ax.set_ylim(0, 100)
ax.set_yticks([25, 50, 75, 100])
ax.set_title('Tract 05085020800 - Current Pillar Scores (2024)',
             fontsize=14, fontweight='bold', pad=30)
ax.grid(True)

plt.tight_layout()
plt.savefig('figures_tract_20800/current_state_radar.png',
            dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved: figures_tract_20800/current_state_radar.png")

# ============================================================================
# 5. YEAR-OVER-YEAR CHANGES HEATMAP
# ============================================================================
print("\n5. Creating year-over-year changes heatmap...")

# Calculate year-over-year changes
yoy_changes = pd.DataFrame({
    'Place': tract_data['place_score'].diff(),
    'Economy': tract_data['economy_score'].diff(),
    'Community': tract_data['community_score'].diff(),
    'Overall IGS': tract_data['igs_score'].diff()
})
yoy_changes['Year'] = tract_data['year'].astype(str)
yoy_changes = yoy_changes.dropna()
yoy_changes = yoy_changes.set_index('Year').T

fig, ax = plt.subplots(figsize=(10, 5))
sns.heatmap(yoy_changes, annot=True, fmt='.1f', cmap='RdYlGn', center=0,
            cbar_kws={'label': 'Score Change'}, linewidths=0.5, ax=ax)
ax.set_xlabel('Year', fontsize=12, fontweight='bold')
ax.set_ylabel('Score Type', fontsize=12, fontweight='bold')
ax.set_title('Tract 05085020800 - Year-over-Year Score Changes',
             fontsize=14, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('figures_tract_20800/yoy_changes_heatmap.png',
            dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved: figures_tract_20800/yoy_changes_heatmap.png")

# ============================================================================
# 6. KEY INDICATORS CURRENT STATE
# ============================================================================
print("\n6. Creating key indicators snapshot...")

indicators = {
    'Median\nIncome': f'${last_year["median_income"]:,.0f}',
    'Broadband\nAccess': f'{last_year["broadband_access_pct"]:.1f}%',
    'Minority\nBusinesses': f'{last_year["minority_owned_businesses_pct"]:.1f}%',
    'Housing\nCost Burden': f'{last_year["housing_cost_burden_pct"]:.1f}%',
    'Early Ed\nEnrollment': f'{last_year["early_education_enrollment_pct"]:.1f}%'
}

fig, ax = plt.subplots(figsize=(14, 6))
x_pos = np.arange(len(indicators))
colors_ind = ['#3498db', '#2ecc71', '#9b59b6', '#e74c3c', '#f39c12']

bars = ax.bar(x_pos, [1]*len(indicators),
              color=colors_ind, alpha=0.3, width=0.8)
ax.set_ylim(0, 1.5)
ax.set_xticks(x_pos)
ax.set_xticklabels(indicators.keys(), fontsize=11, fontweight='bold')
ax.set_title('Tract 05085020800 - Key Indicators (2024)',
             fontsize=15, fontweight='bold', pad=20)
ax.axis('off')

# Add values as text
for i, (key, val) in enumerate(indicators.items()):
    ax.text(i, 0.5, val, ha='center', va='center',
            fontsize=16, fontweight='bold', color=colors_ind[i])

plt.tight_layout()
plt.savefig('figures_tract_20800/key_indicators.png',
            dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved: figures_tract_20800/key_indicators.png")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*70)
print("VISUALIZATION COMPLETE!")
print("="*70)
print(f"\nAll figures saved to: figures_tract_20800/")
print(f"\nGenerated visualizations:")
print(f"  1. igs_score_trend.png - IGS trend with crisis point")
print(f"  2. pillar_scores_all.png - All pillar scores comparison")
print(f"  3. score_changes.png - 5-year changes bar chart")
print(f"  4. current_state_radar.png - 2024 pillar scores radar")
print(f"  5. yoy_changes_heatmap.png - Year-over-year changes")
print(f"  6. key_indicators.png - Current indicators snapshot")

print(f"  7. indicator_trends.png - Indicator trends (income, broadband, minority business, housing burden, early ed) 2019–2024")
print(f"\nTotal: 7 high-resolution PNG files (300 DPI)")
print("="*70)

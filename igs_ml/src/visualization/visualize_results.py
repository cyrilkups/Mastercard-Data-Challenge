"""
IGS ML Model Visualization Script

Generates comprehensive visualizations for:
- Temporal trends (2020-2023)
- Pillar scores evolution
- Feature correlations
- Model feature importance
- Intervention impact analysis
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
from pathlib import Path

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

# Create output directory
os.makedirs("figures", exist_ok=True)

# Load main dataset
print("Loading igs_trends_features.csv...")
df = pd.read_csv("igs_trends_features.csv")
df = df.sort_values(["tract", "year"])
print(f"Loaded {len(df)} rows, {len(df.columns)} columns")
print(f"Years: {sorted(df['year'].unique())}")
print(f"Tracts: {sorted(df['tract'].unique())}\n")

# ============================================================================
# 1. TREND LINE CHARTS - Key Indicators (2020-2023)
# ============================================================================
print("Creating indicator trend charts...")

indicators = [
    ('median_income', 'Median Income ($)', 'viridis'),
    ('broadband_access_pct', 'Broadband Access (%)', 'Blues'),
    ('minority_owned_businesses_pct', 'Minority-Owned Businesses (%)', 'Greens'),
    ('housing_cost_burden_pct', 'Housing Cost Burden (%)', 'Oranges'),
    ('early_education_enrollment_pct', 'Early Education Enrollment (%)', 'Purples')
]

for col, title, palette in indicators:
    fig, ax = plt.subplots(figsize=(10, 6))

    for tract in sorted(df['tract'].unique()):
        tract_data = df[df['tract'] == tract]
        ax.plot(tract_data['year'], tract_data[col],
                marker='o', label=f'Tract {tract}', linewidth=2)

    ax.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax.set_ylabel(title, fontsize=12, fontweight='bold')
    ax.set_title(f'{title} Trends by Tract (2020-2023)',
                 fontsize=14, fontweight='bold', pad=20)
    ax.legend(title='Census Tract', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'figures/trend_{col}.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  ✓ Saved: figures/trend_{col}.png")

# ============================================================================
# 2. PILLAR SCORES TRENDS
# ============================================================================
print("\nCreating pillar score trend charts...")

pillar_scores = [
    ('place_score', 'Place Score', '#e74c3c'),
    ('economy_score', 'Economy Score', '#3498db'),
    ('community_score', 'Community Score', '#2ecc71'),
    ('igs_score', 'Overall IGS Score', '#9b59b6')
]

# Individual pillar charts
for col, title, color in pillar_scores:
    fig, ax = plt.subplots(figsize=(10, 6))

    for tract in sorted(df['tract'].unique()):
        tract_data = df[df['tract'] == tract]
        ax.plot(tract_data['year'], tract_data[col],
                marker='o', label=f'Tract {tract}', linewidth=2.5)

    ax.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax.set_ylabel(title, fontsize=12, fontweight='bold')
    ax.set_title(f'{title} Evolution by Tract (2020-2023)',
                 fontsize=14, fontweight='bold', pad=20)
    ax.legend(title='Census Tract', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'figures/trend_{col}.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  ✓ Saved: figures/trend_{col}.png")

# Combined pillar scores chart
fig, ax = plt.subplots(figsize=(12, 7))
avg_scores = df.groupby('year')[['place_score', 'economy_score',
                                 'community_score', 'igs_score']].mean()

ax.plot(avg_scores.index, avg_scores['place_score'],
        marker='o', label='Place Score', linewidth=3, color='#e74c3c')
ax.plot(avg_scores.index, avg_scores['economy_score'],
        marker='s', label='Economy Score', linewidth=3, color='#3498db')
ax.plot(avg_scores.index, avg_scores['community_score'],
        marker='^', label='Community Score', linewidth=3, color='#2ecc71')
ax.plot(avg_scores.index, avg_scores['igs_score'],
        marker='D', label='Overall IGS Score', linewidth=3, color='#9b59b6')

ax.set_xlabel('Year', fontsize=12, fontweight='bold')
ax.set_ylabel('Score', fontsize=12, fontweight='bold')
ax.set_title('Average Pillar Scores Across All Tracts (2020-2023)',
             fontsize=14, fontweight='bold', pad=20)
ax.legend(fontsize=11, loc='best')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('figures/pillar_scores_combined.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"  ✓ Saved: figures/pillar_scores_combined.png")

# ============================================================================
# 3. CORRELATION HEATMAP
# ============================================================================
print("\nCreating correlation heatmap...")

# Select numerical columns (exclude tract and year)
numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
numeric_cols = [col for col in numeric_cols if col not in ['tract', 'year']]

correlation_matrix = df[numeric_cols].corr()

fig, ax = plt.subplots(figsize=(14, 12))
sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm',
            center=0, square=True, linewidths=0.5, cbar_kws={"shrink": 0.8},
            ax=ax)
ax.set_title('Feature Correlation Heatmap',
             fontsize=16, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('figures/correlation_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"  ✓ Saved: figures/correlation_heatmap.png")

# ============================================================================
# 4. SCATTERPLOTS - Key Relationships
# ============================================================================
print("\nCreating scatterplots...")

scatterplots = [
    ('broadband_access_pct', 'economy_score', 'Broadband Access vs Economy Score'),
    ('median_income', 'community_score', 'Median Income vs Community Score'),
    ('housing_cost_burden_pct', 'igs_score', 'Housing Cost Burden vs IGS Score')
]

for x_col, y_col, title in scatterplots:
    fig, ax = plt.subplots(figsize=(10, 6))

    # Color by tract
    for tract in sorted(df['tract'].unique()):
        tract_data = df[df['tract'] == tract]
        ax.scatter(tract_data[x_col], tract_data[y_col],
                   label=f'Tract {tract}', s=100, alpha=0.7)

    # Add regression line
    z = np.polyfit(df[x_col].dropna(), df[y_col].dropna(), 1)
    p = np.poly1d(z)
    ax.plot(df[x_col].sort_values(), p(df[x_col].sort_values()),
            "r--", alpha=0.8, linewidth=2, label='Trend Line')

    ax.set_xlabel(x_col.replace('_', ' ').title(),
                  fontsize=12, fontweight='bold')
    ax.set_ylabel(y_col.replace('_', ' ').title(),
                  fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.legend(title='Census Tract', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    safe_title = title.lower().replace(' ', '_').replace('vs', 'vs')
    plt.savefig(f'figures/scatter_{safe_title}.png',
                dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  ✓ Saved: figures/scatter_{safe_title}.png")

# ============================================================================
# 5. FEATURE IMPORTANCE BAR CHARTS
# ============================================================================
print("\nCreating feature importance charts...")

models_dir = Path("models")
if models_dir.exists():
    importance_files = [
        ('place_score_feature_importance.csv', 'Place Score Model', '#e74c3c'),
        ('economy_score_feature_importance.csv', 'Economy Score Model', '#3498db'),
        ('community_score_feature_importance.csv',
         'Community Score Model', '#2ecc71'),
        ('igs_score_feature_importance.csv', 'IGS Score Model', '#9b59b6')
    ]

    for filename, title, color in importance_files:
        filepath = models_dir / filename
        if filepath.exists():
            importance_df = pd.read_csv(filepath)

            # Plot top 10 features
            top_features = importance_df.head(10)

            fig, ax = plt.subplots(figsize=(10, 6))
            bars = ax.barh(range(len(top_features)), top_features['importance'],
                           color=color, alpha=0.8)
            ax.set_yticks(range(len(top_features)))
            ax.set_yticklabels(top_features['feature'])
            ax.set_xlabel('Importance Score', fontsize=12, fontweight='bold')
            ax.set_title(f'Top 10 Features - {title}',
                         fontsize=14, fontweight='bold', pad=20)
            ax.invert_yaxis()
            ax.grid(True, alpha=0.3, axis='x')

            # Add value labels
            for i, (bar, val) in enumerate(zip(bars, top_features['importance'])):
                ax.text(val, i, f' {val:.4f}', va='center', fontsize=9)

            plt.tight_layout()
            safe_name = filename.replace('.csv', '')
            plt.savefig(f'figures/{safe_name}.png',
                        dpi=300, bbox_inches='tight')
            plt.close()
            print(f"  ✓ Saved: figures/{safe_name}.png")
        else:
            print(f"  ⚠ Not found: {filepath}")
else:
    print("  ⚠ models/ directory not found")

# ============================================================================
# 6. INTERVENTION COMPARISON
# ============================================================================
print("\nCreating intervention comparison chart...")

intervention_file = models_dir / "intervention_comparison.csv"
if intervention_file.exists():
    intervention_df = pd.read_csv(intervention_file)

    # Create comparison chart for different intervention scenarios
    fig, ax = plt.subplots(figsize=(14, 7))

    scenarios = intervention_df['Scenario']
    x = range(len(scenarios))
    width = 0.2

    # Plot all four scores as grouped bars
    bars1 = ax.bar([i - 1.5*width for i in x], intervention_df['place_score'],
                   width, label='Place Score', color='#e74c3c', alpha=0.8)
    bars2 = ax.bar([i - 0.5*width for i in x], intervention_df['economy_score'],
                   width, label='Economy Score', color='#3498db', alpha=0.8)
    bars3 = ax.bar([i + 0.5*width for i in x], intervention_df['community_score'],
                   width, label='Community Score', color='#2ecc71', alpha=0.8)
    bars4 = ax.bar([i + 1.5*width for i in x], intervention_df['igs_score'],
                   width, label='IGS Score', color='#9b59b6', alpha=0.8)

    ax.set_xlabel('Intervention Scenario', fontsize=12, fontweight='bold')
    ax.set_ylabel('Score', fontsize=12, fontweight='bold')
    ax.set_title('Impact of Different Intervention Strategies on Pillar Scores',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(scenarios, rotation=15, ha='right')
    ax.legend(fontsize=11, loc='lower left')
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig('figures/intervention_comparison.png',
                dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  ✓ Saved: figures/intervention_comparison.png")

    # Create delta comparison chart
    fig, ax = plt.subplots(figsize=(14, 7))

    # Plot score changes (deltas) - exclude baseline row
    delta_df = intervention_df.iloc[1:]  # Skip baseline
    scenarios_delta = delta_df['Scenario']
    x_delta = range(len(scenarios_delta))

    bars1 = ax.bar([i - 1.5*width for i in x_delta], delta_df['place_score_delta'],
                   width, label='Place Score Δ', color='#e74c3c', alpha=0.8)
    bars2 = ax.bar([i - 0.5*width for i in x_delta], delta_df['economy_score_delta'],
                   width, label='Economy Score Δ', color='#3498db', alpha=0.8)
    bars3 = ax.bar([i + 0.5*width for i in x_delta], delta_df['community_score_delta'],
                   width, label='Community Score Δ', color='#2ecc71', alpha=0.8)
    bars4 = ax.bar([i + 1.5*width for i in x_delta], delta_df['igs_score_delta'],
                   width, label='IGS Score Δ', color='#9b59b6', alpha=0.8)

    ax.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)
    ax.set_xlabel('Intervention Scenario', fontsize=12, fontweight='bold')
    ax.set_ylabel('Change in Score (Δ)', fontsize=12, fontweight='bold')
    ax.set_title('Score Changes from Baseline by Intervention Strategy',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x_delta)
    ax.set_xticklabels(scenarios_delta, rotation=15, ha='right')
    ax.legend(fontsize=11, loc='best')
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig('figures/intervention_delta_comparison.png',
                dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  ✓ Saved: figures/intervention_delta_comparison.png")

    plt.tight_layout()
    plt.savefig('figures/intervention_comparison.png',
                dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  ✓ Saved: figures/intervention_comparison.png")
else:
    print(f"  ⚠ Not found: {intervention_file}")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*70)
print("VISUALIZATION COMPLETE!")
print("="*70)
print(f"\nAll figures saved to: figures/")
print(f"\nGenerated visualizations:")
print(f"  - 5 indicator trend charts")
print(f"  - 4 pillar score trend charts")
print(f"  - 1 combined pillar scores chart")
print(f"  - 1 correlation heatmap")
print(f"  - 3 scatterplots")
print(f"  - 4 feature importance charts")
print(f"  - 1 intervention comparison chart")
print(f"\nTotal: ~19 high-resolution PNG files (300 DPI)")
print("="*70)

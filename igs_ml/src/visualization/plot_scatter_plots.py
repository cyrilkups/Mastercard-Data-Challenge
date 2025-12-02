"""
Using the FULL dataset (all tracts), generate the following scatter plots:

1. median_income vs community_score
2. housing_cost_burden_pct vs igs_score
3. broadband_access_pct vs economy_score

Instructions:
• Load `igs_ml/igs_trends_features.csv`
• Remove rows with missing values
• Use sns.regplot with purple markers (#8e44ad)
• Add clear titles and axis labels
• Save to `igs_ml/figures/` as:
    scatter_median_income_vs_community_score.png
    scatter_housing_cost_burden_vs_igs_score.png
    scatter_broadband_access_vs_economy_score.png
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 11

# Create output directory
os.makedirs("figures", exist_ok=True)

# Purple color
purple = '#8e44ad'

print("="*70)
print("GENERATING SCATTER PLOTS")
print("="*70)

# Load the full dataset
csv_file = 'igs_trends_features.csv'
print(f"\nLoading data from {csv_file}...")
df = pd.read_csv(csv_file)
print(f"Loaded {len(df)} rows, {len(df.columns)} columns")

# Remove rows with missing values
df_clean = df.dropna()
print(f"After removing missing values: {len(df_clean)} rows")

# Define scatter plots to generate
scatter_plots = [
    {
        'x': 'median_income',
        'y': 'community_score',
        'x_label': 'Median Income (%)',
        'y_label': 'Community Score',
        'title': 'Median Income vs Community Score',
        'filename': 'scatter_median_income_vs_community_score.png'
    },
    {
        'x': 'housing_cost_burden_pct',
        'y': 'igs_score',
        'x_label': 'Housing Cost Burden (%)',
        'y_label': 'IGS Score',
        'title': 'Housing Cost Burden vs IGS Score',
        'filename': 'scatter_housing_cost_burden_vs_igs_score.png'
    },
    {
        'x': 'broadband_access_pct',
        'y': 'economy_score',
        'x_label': 'Broadband Access (%)',
        'y_label': 'Economy Score',
        'title': 'Broadband Access vs Economy Score',
        'filename': 'scatter_broadband_access_vs_economy_score.png'
    }
]

# Generate each scatter plot
for i, plot_config in enumerate(scatter_plots, 1):
    print(f"\n{i}. Generating {plot_config['title']}...")

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create scatter plot with regression line
    sns.regplot(data=df_clean,
                x=plot_config['x'],
                y=plot_config['y'],
                scatter_kws={'color': purple, 'alpha': 0.6, 's': 80},
                line_kws={'color': purple, 'linewidth': 2},
                ax=ax)

    # Set labels and title
    ax.set_xlabel(plot_config['x_label'], fontsize=13, fontweight='bold')
    ax.set_ylabel(plot_config['y_label'], fontsize=13, fontweight='bold')
    ax.set_title(plot_config['title'], fontsize=15, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    # Save figure
    output_file = f"figures/{plot_config['filename']}"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"  ✓ Saved: {output_file}")

print("\n" + "="*70)
print("SCATTER PLOTS COMPLETE!")
print("="*70)
print(f"\nAll figures saved to: figures/")
print(f"Total: {len(scatter_plots)} high-resolution PNG files (300 DPI)")
print("="*70)

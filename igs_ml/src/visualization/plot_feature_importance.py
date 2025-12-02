"""
Load feature importance CSVs for all four models and generate horizontal
bar charts.

Files (from models/ directory):
  - place_score_feature_importance.csv
  - economy_score_feature_importance.csv
  - community_score_feature_importance.csv
  - igs_score_feature_importance.csv

Requirements:
  * Load each CSV
  * Create a horizontal bar chart
  * Use a clean purple color palette
  * Save under figures/feature_importance/<model>.png
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

# Define models and their display names
models = {
    'place_score': 'Place Score Model',
    'economy_score': 'Economy Score Model',
    'community_score': 'Community Score Model',
    'igs_score': 'IGS Score Model'
}

# Purple color
purple = '#8e44ad'

print("="*70)
print("GENERATING FEATURE IMPORTANCE VISUALIZATIONS")
print("="*70)

for i, (model_name, display_name) in enumerate(models.items()):
    csv_file = f'models/{model_name}_feature_importance.csv'

    # Check if file exists
    if not os.path.exists(csv_file):
        print(f"\n⚠ Skipping {display_name}: {csv_file} not found")
        continue

    # Load feature importance data
    df = pd.read_csv(csv_file)

    # Sort by importance (descending)
    df = df.sort_values('importance', ascending=True)

    # Create horizontal bar chart
    fig, ax = plt.subplots(figsize=(10, 7))

    bars = ax.barh(df['feature'], df['importance'],
                   color=purple, alpha=0.85)

    # Add value labels
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.01, bar.get_y() + bar.get_height()/2,
                f'{width:.3f}',
                ha='left', va='center', fontsize=10, fontweight='bold')

    ax.set_xlabel('Feature Importance', fontsize=13, fontweight='bold')
    ax.set_ylabel('Feature', fontsize=13, fontweight='bold')
    ax.set_title(f'Feature Importance – {display_name}',
                 fontsize=15, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, axis='x')

    plt.tight_layout()

    # Save figure
    output_file = f'figures/{model_name}_feature_importance.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"\n✓ {display_name}")
    print(f"  - Loaded: {csv_file}")
    print(f"  - Saved: {output_file}")
    print(f"  - Features: {len(df)}")

print("\n" + "="*70)
print("FEATURE IMPORTANCE VISUALIZATION COMPLETE!")
print("="*70)
print(f"\nAll figures saved to: figures/")
print(f"Total: {len(models)} high-resolution PNG files (300 DPI)")
print("="*70)

"""
Generate a correlation heatmap using the FULL dataset in 
`igs_ml/igs_trends_features.csv`.

Instructions:
• Load the CSV
• Only keep numeric columns (drop tract_code, county_name, etc.)
• Compute df.corr()
• Use seaborn.heatmap with annotated cells
• Color palette: "RdYlGn"
• Title: "Correlation Heatmap – IGS Model Features"
• Save to: `igs_ml/figures/correlation_heatmap.png`
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style
sns.set_style("white")
plt.rcParams['figure.figsize'] = (14, 12)
plt.rcParams['font.size'] = 10

# Create output directory
os.makedirs("figures", exist_ok=True)

print("="*70)
print("GENERATING CORRELATION HEATMAP")
print("="*70)

# Load the full dataset
csv_file = 'igs_trends_features.csv'
print(f"\nLoading data from {csv_file}...")
df = pd.read_csv(csv_file)
print(f"Loaded {len(df)} rows, {len(df.columns)} columns")

# Select only numeric columns
numeric_df = df.select_dtypes(include=['float64', 'int64'])
print(f"\nNumeric columns: {len(numeric_df.columns)}")
print(f"Columns: {list(numeric_df.columns)}")

# Compute correlation matrix
print("\nComputing correlation matrix...")
corr_matrix = numeric_df.corr()

# Create heatmap
print("Creating heatmap...")
fig, ax = plt.subplots(figsize=(14, 12))

sns.heatmap(corr_matrix,
            annot=True,
            fmt='.2f',
            cmap='RdYlGn',
            center=0,
            square=True,
            linewidths=0.5,
            cbar_kws={"shrink": 0.8},
            ax=ax)

ax.set_title('Correlation Heatmap – IGS Model Features',
             fontsize=16, fontweight='bold', pad=20)

plt.tight_layout()

# Save figure
output_file = 'figures/correlation_heatmap.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight')
plt.close()

print(f"\n✓ Heatmap saved to: {output_file}")
print(f"  - Matrix size: {corr_matrix.shape[0]} x {corr_matrix.shape[1]}")
print(f"  - Resolution: 300 DPI")

print("\n" + "="*70)
print("CORRELATION HEATMAP COMPLETE!")
print("="*70)

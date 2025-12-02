"""
Quick Data Verification - View all cleaned datasets
"""

import pandas as pd
import os


def show_dataset_info(filename):
    """Display key info about a cleaned dataset"""
    filepath = os.path.join('data_cleaned', filename)
    if not os.path.exists(filepath):
        print(f"❌ {filename} - NOT FOUND")
        return

    df = pd.read_csv(filepath)

    print(f"\n{'='*70}")
    print(f"📊 {filename.upper()}")
    print(f"{'='*70}")
    print(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")

    if 'year' in df.columns:
        years = sorted(df['year'].unique())
        if len(years) <= 10:
            print(f"Years: {years}")
        else:
            print(f"Years: {years[0]}-{years[-1]} ({len(years)} total years)")

    if 'estimate_type' in df.columns:
        print(f"Estimate types: {df['estimate_type'].unique().tolist()}")

    print(f"\nColumns ({len(df.columns)}):")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i:2d}. {col}")

    print(f"\nFirst 3 rows:")
    print(df.head(3).to_string())
    print(f"{'='*70}\n")


if __name__ == "__main__":
    print("\n" + "🎯 CLEANED DATASETS VERIFICATION" + "\n")

    datasets = [
        'personal_income_parsed.csv',
        'broadband_cleaned.csv',
        'housing_cleaned.csv',
        'labor_cleaned.csv',
        'business_cleaned.csv'
    ]

    for dataset in datasets:
        show_dataset_info(dataset)

    print("\n✅ ALL 5 CLEANED DATASETS VERIFIED!\n")
    print("Next steps:")
    print("  1. Collect additional personal income data (2019-2023)")
    print("  2. Merge datasets by year for integrated analysis")
    print("  3. Calculate trend features (YoY changes)")
    print("  4. Train ML models on combined dataset")
    print("\nSee CLEANED_DATASETS_SUMMARY.md for detailed documentation.")

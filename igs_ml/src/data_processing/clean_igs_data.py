"""
Data Cleaning Script for IGS (Inclusive Growth Score) Analysis

This script processes census tract data across multiple years to:
1. Clean and standardize tract identifiers and years
2. Calculate year-over-year trend features for key metrics
3. Prepare data for machine learning models

Expected input: CSV with columns including:
- tract, year, median_income, broadband_access_pct, minority_owned_businesses_pct,
  housing_cost_burden_pct, early_education_enrollment_pct, 
  place_score, economy_score, community_score, igs_score
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path


def load_raw_data(file_path):
    """
    Load raw census data from CSV file.

    Parameters:
    -----------
    file_path : str
        Path to the raw data CSV file

    Returns:
    --------
    pd.DataFrame
        Loaded raw data
    """
    print(f"Loading data from {file_path}...")
    df = pd.read_csv(file_path)
    print(f"Loaded {len(df)} rows")
    return df


def clean_tract_year(df):
    """
    Clean and standardize tract and year columns.

    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe with 'tract' and 'year' columns

    Returns:
    --------
    pd.DataFrame
        DataFrame with cleaned tract (zero-padded string) and year (integer)
    """
    print("Cleaning tract and year columns...")

    # Ensure tract is zero-padded string (11 digits: 2 state + 3 county + 6 tract)
    df['tract'] = df['tract'].astype(str).str.zfill(11)

    # Ensure year is integer
    df['year'] = df['year'].astype(int)

    # Sort by tract and year for trend calculations
    df = df.sort_values(['tract', 'year']).reset_index(drop=True)

    print(f"Data spans {df['year'].min()} to {df['year'].max()}")
    print(f"Number of unique tracts: {df['tract'].nunique()}")

    return df


def calculate_trend_features(df):
    """
    Calculate year-over-year trend features for each tract.

    Computes percentage/percentage point changes from previous year for:
    - median_income (% change)
    - broadband_access_pct (percentage point change)
    - minority_owned_businesses_pct (percentage point change)
    - housing_cost_burden_pct (percentage point change)
    - early_education_enrollment_pct (percentage point change)

    Parameters:
    -----------
    df : pd.DataFrame
        Cleaned data sorted by tract and year

    Returns:
    --------
    pd.DataFrame
        DataFrame with trend features added
    """
    print("Calculating trend features...")

    # Group by tract to calculate within-tract changes
    df_sorted = df.sort_values(['tract', 'year']).copy()

    # Calculate income growth (percentage change)
    df_sorted['income_growth'] = df_sorted.groupby(
        'tract')['median_income'].pct_change() * 100

    # Calculate percentage point changes for other metrics
    df_sorted['broadband_growth'] = df_sorted.groupby(
        'tract')['broadband_access_pct'].diff()
    df_sorted['minority_business_growth'] = df_sorted.groupby(
        'tract')['minority_owned_businesses_pct'].diff()
    df_sorted['housing_burden_change'] = df_sorted.groupby(
        'tract')['housing_cost_burden_pct'].diff()
    df_sorted['early_ed_growth'] = df_sorted.groupby(
        'tract')['early_education_enrollment_pct'].diff()

    # Display summary statistics
    print("\nTrend feature summary:")
    trend_cols = ['income_growth', 'broadband_growth', 'minority_business_growth',
                  'housing_burden_change', 'early_ed_growth']
    print(df_sorted[trend_cols].describe())

    return df_sorted


def remove_first_year_per_tract(df):
    """
    Remove the first year observation for each tract (where trend values are NaN).

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with trend features

    Returns:
    --------
    pd.DataFrame
        DataFrame with first year per tract removed
    """
    print("\nRemoving first year per tract (NaN trend values)...")
    initial_rows = len(df)

    # Group by tract and drop the first observation (index 0 in each group)
    df_filtered = df.groupby('tract').apply(
        lambda x: x.iloc[1:] if len(x) > 1 else x).reset_index(drop=True)

    removed_rows = initial_rows - len(df_filtered)
    print(f"Removed {removed_rows} rows (first year per tract)")
    print(f"Remaining rows: {len(df_filtered)}")

    return df_filtered


def save_cleaned_data(df, output_path):
    """
    Save cleaned data with trend features to CSV.

    Parameters:
    -----------
    df : pd.DataFrame
        Cleaned data with trend features
    output_path : str
        Path to save the output CSV file
    """
    # Create output directory if it doesn't exist
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save to CSV
    df.to_csv(output_path, index=False)
    print(f"\nCleaned data saved to: {output_path}")
    print(f"Final dataset shape: {df.shape}")
    print(f"\nColumns in output:")
    print(df.columns.tolist())


def generate_sample_data():
    """
    Generate sample data for demonstration purposes.
    This can be replaced with actual data loading logic.

    Returns:
    --------
    pd.DataFrame
        Sample dataset with IGS metrics
    """
    print("Generating sample data for demonstration...")

    np.random.seed(42)

    # Create sample tracts (Arkansas census tracts)
    tracts = ['05085020100', '05085020200',
              '05085020300', '05085020400', '05085020500']
    years = [2019, 2020, 2021, 2022, 2023]

    data = []
    for tract in tracts:
        base_income = np.random.randint(35000, 75000)
        base_broadband = np.random.uniform(60, 85)
        base_minority_biz = np.random.uniform(5, 15)
        base_housing_burden = np.random.uniform(25, 40)
        base_early_ed = np.random.uniform(40, 70)

        for i, year in enumerate(years):
            # Add some trend and noise
            income_trend = np.random.uniform(-0.02, 0.05)
            broadband_trend = np.random.uniform(-2, 5)

            data.append({
                'tract': tract,
                'year': year,
                'median_income': base_income * (1 + income_trend * i) + np.random.randint(-2000, 2000),
                'broadband_access_pct': min(100, base_broadband + broadband_trend * i + np.random.uniform(-3, 3)),
                'minority_owned_businesses_pct': base_minority_biz + np.random.uniform(-1, 2) * i,
                'housing_cost_burden_pct': base_housing_burden + np.random.uniform(-2, 2) * i,
                'early_education_enrollment_pct': base_early_ed + np.random.uniform(-3, 4) * i,
                'place_score': np.random.uniform(40, 85),
                'economy_score': np.random.uniform(35, 80),
                'community_score': np.random.uniform(45, 90),
                'igs_score': np.random.uniform(50, 85)
            })

    return pd.DataFrame(data)


def main():
    """
    Main execution function to clean IGS data and create trend features.
    """
    print("="*60)
    print("IGS Data Cleaning and Trend Feature Engineering")
    print("="*60 + "\n")

    # Define paths
    # TODO: Replace this with actual path to your combined IGS data CSV
    # raw_data_path = "Data Drive Datasets/combined_igs_data.csv"

    output_path = "data_cleaned/igs_trends_features.csv"

    # For demonstration, generate sample data
    # TODO: Replace this with: df = load_raw_data(raw_data_path)
    df = generate_sample_data()

    # Step 1: Clean tract and year columns
    df = clean_tract_year(df)

    # Step 2: Calculate trend features
    df = calculate_trend_features(df)

    # Step 3: Remove first year per tract (NaN trend values)
    df = remove_first_year_per_tract(df)

    # Step 4: Save cleaned data
    save_cleaned_data(df, output_path)

    print("\n" + "="*60)
    print("Data cleaning complete!")
    print("="*60)

    # Display sample of final data
    print("\nSample of cleaned data with trend features:")
    print(df.head(10))

    return df


if __name__ == "__main__":
    df_cleaned = main()

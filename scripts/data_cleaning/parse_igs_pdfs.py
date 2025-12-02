"""
Parse IGS PDF Reports to Extract Tract-Level Data

Extracts scores and indicators from official Inclusive Growth Score™ PDFs
for tract 05085020800 (2019-2024)
"""

import pdfplumber
import pandas as pd
import re
from pathlib import Path


def extract_igs_from_pdf(pdf_path):
    """
    Extract IGS data from a single PDF report

    Returns:
    --------
    dict with tract, year, and all IGS metrics
    """
    print(f"\nProcessing: {pdf_path.name}")

    # Extract year from filename
    year_match = re.search(r'\((\d{4})\)', pdf_path.name)
    year = int(year_match.group(1)) if year_match else None

    # Extract tract from filename
    tract_match = re.search(r'(\d{11})', pdf_path.name)
    tract = tract_match.group(1) if tract_match else None

    data = {
        'tract': tract,
        'year': year
    }

    # Open PDF and extract text
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            full_text += page.extract_text() + "\n"

    print(f"  Extracted text length: {len(full_text)} characters")

    # Extract scores using regex patterns
    # PDFs have format: "PILLAR AVERAGE INCLUSION GROWTH 2023 SCORE"
    # Followed by: "Inclusive Growth Score 36 21 28"
    # Where the numbers are: AVERAGE INCLUSION GROWTH
    # We want the last number (2023 SCORE column)

    # IGS Score - extract the 2023 SCORE column (third number)
    igs_match = re.search(
        r'Inclusive Growth Score\s+(\d+)\s+(\d+)\s+(\d+)', full_text)
    data['igs_score'] = float(igs_match.group(3)) if igs_match else None

    # Place Score - extract the 2023 SCORE column (third number)
    place_match = re.search(r'Place\s+(\d+)\s+(\d+)\s+(\d+)', full_text)
    data['place_score'] = float(place_match.group(3)) if place_match else None

    # Economy Score - extract the 2023 SCORE column (third number)
    economy_match = re.search(r'Economy\s+(\d+)\s+(\d+)\s+(\d+)', full_text)
    data['economy_score'] = float(
        economy_match.group(3)) if economy_match else None

    # Community Score - extract the 2023 SCORE column (third number)
    community_match = re.search(
        r'Community\s+(\d+)\s+(\d+)\s+(\d+)', full_text)
    data['community_score'] = float(
        community_match.group(3)) if community_match else None

    # Indicators - look for Median Income
    income_match = re.search(
        r'Median Income.*?\$\s*(\d+,?\d*)', full_text, re.IGNORECASE)
    if income_match:
        data['median_income'] = float(income_match.group(1).replace(',', ''))
    else:
        data['median_income'] = None

    # For other indicators, we don't have enough info in PDFs
    # Set to None - they'll be filled from other sources later if needed
    data['broadband_access_pct'] = None
    data['minority_owned_businesses_pct'] = None
    data['housing_cost_burden_pct'] = None
    data['early_education_enrollment_pct'] = None

    print(
        f"  Extracted scores: IGS={data['igs_score']}, Place={data['place_score']}, Economy={data['economy_score']}, Community={data['community_score']}")

    return data


def parse_all_igs_pdfs(igs_dir):
    """
    Parse all IGS PDFs for tract 20800

    Returns:
    --------
    DataFrame with all years of data
    """
    igs_path = Path(igs_dir)
    pdf_files = sorted(igs_path.glob("*.pdf"))

    print(f"Found {len(pdf_files)} PDF files")

    all_data = []
    for pdf_file in pdf_files:
        try:
            data = extract_igs_from_pdf(pdf_file)
            all_data.append(data)
        except Exception as e:
            print(f"  ⚠ Error processing {pdf_file.name}: {e}")

    # Create DataFrame
    df = pd.DataFrame(all_data)

    # Ensure tract is 11-digit string
    df['tract'] = df['tract'].astype(str).str.zfill(11)

    # Sort by year
    df = df.sort_values('year')

    return df


def calculate_growth_metrics(df):
    """
    Calculate year-over-year growth for each indicator

    Matches the structure of existing igs_trends_features.csv
    """
    df = df.sort_values(['tract', 'year'])

    # Initialize growth columns with 0 (safer than calculating from None values)
    df['income_growth'] = 0.0
    df['broadband_growth'] = 0.0
    df['minority_business_growth'] = 0.0
    df['housing_burden_change'] = 0.0
    df['early_ed_growth'] = 0.0

    # Calculate growth for each tract (only if data exists)
    for tract in df['tract'].unique():
        tract_mask = df['tract'] == tract
        tract_df = df[tract_mask].copy()

        # Income growth - only if we have median_income data
        if tract_df['median_income'].notna().sum() > 1:
            df.loc[tract_mask, 'income_growth'] = tract_df['median_income'].pct_change(
                fill_method=None) * 100

        # For other indicators that are None, keep growth at 0
        # They can be calculated later if indicator data is added

    # Fill NaN in growth columns with 0
    df[['income_growth', 'broadband_growth', 'minority_business_growth',
        'housing_burden_change', 'early_ed_growth']] = df[[
            'income_growth', 'broadband_growth', 'minority_business_growth',
            'housing_burden_change', 'early_ed_growth']].fillna(0)

    return df


if __name__ == "__main__":
    print("="*70)
    print("IGS PDF PARSER - Tract 05085020800")
    print("="*70)

    # Path to IGS PDFs
    igs_dir = "Data Drive Datasets/Inclusive Growth Score™ (IGS) "

    # Parse PDFs
    df = parse_all_igs_pdfs(igs_dir)

    # Calculate growth metrics
    df = calculate_growth_metrics(df)

    # Reorder columns to match existing format
    column_order = [
        'tract', 'year',
        'place_score', 'economy_score', 'community_score', 'igs_score',
        'median_income', 'broadband_access_pct', 'minority_owned_businesses_pct',
        'housing_cost_burden_pct', 'early_education_enrollment_pct',
        'income_growth', 'broadband_growth', 'minority_business_growth',
        'housing_burden_change', 'early_ed_growth'
    ]

    # Keep only columns that exist
    existing_cols = [col for col in column_order if col in df.columns]
    df = df[existing_cols]

    # Save to CSV
    output_path = "data_cleaned/tract_20800_cleaned.csv"
    df.to_csv(output_path, index=False)

    print("\n" + "="*70)
    print("EXTRACTION COMPLETE")
    print("="*70)
    print(f"\nSaved: {output_path}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print(f"Years: {sorted(df['year'].unique())}")
    print(f"\nData preview:")
    print(df.to_string())
    print("\n" + "="*70)

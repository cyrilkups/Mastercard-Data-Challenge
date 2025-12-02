"""
Personal Income Data Parser for Multi-Year ACS Data

This script parses and consolidates Personal Income data from
multiple years (2019-2024) of ACS 5-year and 1-year estimates.

It extracts key metrics and combines them into a clean dataset
ready for ML model training.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import re
from typing import List, Dict, Tuple


class PersonalIncomeParser:
    """Parse and consolidate multi-year Personal Income ACS data."""

    def __init__(self, data_dir='Data Drive Datasets/Data That Back IGS (Problem)/Community Pillar/Personal Income'):
        self.data_dir = Path(data_dir)
        self.parsed_data = []

    def extract_year_and_type(self, filename: str) -> Tuple[int, str]:
        """
        Extract year and estimate type from filename.

        Examples:
        - ACSST5Y2023.S1901-*.csv -> (2023, '5-year')
        - ACSST1Y2024.S1901-*.csv -> (2024, '1-year')
        """
        match = re.search(r'ACSST(5Y|1Y)(\d{4})', filename)
        if match:
            estimate_type = '5-year' if match.group(1) == '5Y' else '1-year'
            year = int(match.group(2))
            return year, estimate_type
        return None, None

    def extract_table_code(self, filename: str) -> str:
        """Extract table code (S1901 or S2001) from filename."""
        match = re.search(r'(S\d{4})', filename)
        return match.group(1) if match else None

    def parse_s1901_household_income(self, filepath: Path, year: int,
                                     estimate_type: str) -> Dict:
        """
        Parse S1901 - Household/Family Income data.

        Extracts:
        - Median household income
        - Mean household income
        - Median family income
        - Income distribution percentages
        """
        df = pd.read_csv(filepath)

        # Extract county name from column headers
        county_cols = [
            col for col in df.columns if 'Households!!Estimate' in col]
        if county_cols:
            county_name = county_cols[0].split('!!')[0]
        else:
            county_name = 'Unknown'

        result = {
            'year': year,
            'estimate_type': estimate_type,
            'table': 'S1901',
            'county': county_name,
            'source_file': filepath.name
        }

        # Extract median and mean values
        for idx, row in df.iterrows():
            label = str(row['Label (Grouping)']).strip()

            if 'Median income (dollars)' in label:
                # Extract household median
                hh_col = [
                    c for c in df.columns if 'Households!!Estimate' in c][0]
                result['median_household_income'] = self._clean_value(
                    row[hh_col])

                # Extract family median
                fam_col = [
                    c for c in df.columns if 'Families!!Estimate' in c][0]
                result['median_family_income'] = self._clean_value(
                    row[fam_col])

            elif 'Mean income (dollars)' in label:
                hh_col = [
                    c for c in df.columns if 'Households!!Estimate' in c][0]
                result['mean_household_income'] = self._clean_value(
                    row[hh_col])

        return result

    def parse_s2001_earnings(self, filepath: Path, year: int,
                             estimate_type: str) -> Dict:
        """
        Parse S2001 - Earnings data.

        Extracts:
        - Median earnings (overall)
        - Median earnings by gender
        - Median earnings for full-time workers
        """
        df = pd.read_csv(filepath)

        # Extract county name
        county_cols = [col for col in df.columns if 'Total!!Estimate' in col]
        if county_cols:
            county_name = county_cols[0].split('!!')[0]
        else:
            county_name = 'Unknown'

        result = {
            'year': year,
            'estimate_type': estimate_type,
            'table': 'S2001',
            'county': county_name,
            'source_file': filepath.name
        }

        for idx, row in df.iterrows():
            label = str(row['Label (Grouping)']).strip()

            # Overall median earnings
            if label == 'Median earnings (dollars)':
                total_col = [
                    c for c in df.columns if 'Total!!Estimate' in c][0]
                result['median_earnings'] = self._clean_value(row[total_col])

                # Gender breakdown
                male_col = [c for c in df.columns if 'Male!!Estimate' in c][0]
                result['median_earnings_male'] = self._clean_value(
                    row[male_col])

                female_col = [
                    c for c in df.columns if 'Female!!Estimate' in c][0]
                result['median_earnings_female'] = self._clean_value(
                    row[female_col])

            # Full-time worker earnings
            elif 'full-time, year-round workers with earnings' in label.lower() and 'Median' in label:
                total_col = [
                    c for c in df.columns if 'Total!!Estimate' in c][0]
                result['median_earnings_fulltime'] = self._clean_value(
                    row[total_col])

        return result

    def _clean_value(self, value) -> float:
        """Clean and convert string values to float."""
        if pd.isna(value) or value == 'N' or value == '(X)':
            return np.nan

        # Remove commas and convert to float
        value_str = str(value).replace(',', '').replace('$', '').strip()
        try:
            return float(value_str)
        except ValueError:
            return np.nan

    def parse_all_files(self) -> pd.DataFrame:
        """
        Parse all Personal Income CSV files in the directory.

        Returns:
        --------
        pd.DataFrame
            Consolidated data from all files
        """
        print("="*60)
        print("PARSING PERSONAL INCOME DATA")
        print("="*60 + "\n")

        csv_files = list(self.data_dir.glob('*.csv'))
        print(f"Found {len(csv_files)} CSV files\n")

        for filepath in sorted(csv_files):
            year, estimate_type = self.extract_year_and_type(filepath.name)
            table_code = self.extract_table_code(filepath.name)

            if not year or not table_code:
                print(f"⚠ Skipping {filepath.name} - couldn't parse filename")
                continue

            print(f"Processing: {filepath.name}")
            print(
                f"  Year: {year}, Type: {estimate_type}, Table: {table_code}")

            try:
                if table_code == 'S1901':
                    data = self.parse_s1901_household_income(
                        filepath, year, estimate_type)
                elif table_code == 'S2001':
                    data = self.parse_s2001_earnings(
                        filepath, year, estimate_type)
                else:
                    print(f"  ⚠ Unknown table code: {table_code}")
                    continue

                self.parsed_data.append(data)
                print(f"  ✓ Parsed successfully")

            except Exception as e:
                print(f"  ✗ Error: {str(e)}")

            print()

        # Convert to DataFrame
        df = pd.DataFrame(self.parsed_data)

        print("="*60)
        print("PARSING COMPLETE")
        print("="*60)
        print(f"\nTotal records parsed: {len(df)}")
        print(f"Years covered: {sorted(df['year'].unique())}")
        print(f"Tables: {sorted(df['table'].unique())}")
        print(f"Estimate types: {sorted(df['estimate_type'].unique())}")

        return df

    def merge_income_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Merge S1901 and S2001 data by year and estimate type.

        Creates a consolidated dataset with all income metrics.
        """
        # Separate tables
        s1901 = df[df['table'] == 'S1901'].copy()
        s2001 = df[df['table'] == 'S2001'].copy()

        # Merge on year and estimate_type
        merged = pd.merge(
            s1901,
            s2001,
            on=['year', 'estimate_type', 'county'],
            how='outer',
            suffixes=('_s1901', '_s2001')
        )

        # Clean up columns
        merged['table'] = 'S1901+S2001'
        merged['source_files'] = merged.apply(
            lambda x: f"{x.get('source_file_s1901', '')} | {x.get('source_file_s2001', '')}",
            axis=1
        )

        # Drop redundant columns
        cols_to_drop = [
            c for c in merged.columns if c.endswith(('_s1901', '_s2001'))]
        merged = merged.drop(columns=cols_to_drop)

        return merged

    def calculate_derived_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate additional metrics from the parsed data.

        Examples:
        - Gender earnings gap
        - Income-to-earnings ratio
        """
        df = df.copy()

        # Gender earnings gap (as percentage)
        if 'median_earnings_male' in df.columns and 'median_earnings_female' in df.columns:
            df['gender_earnings_gap_pct'] = (
                (df['median_earnings_male'] - df['median_earnings_female']) /
                df['median_earnings_male'] * 100
            )

        # Household income to earnings ratio
        if 'median_household_income' in df.columns and 'median_earnings' in df.columns:
            df['household_to_earnings_ratio'] = (
                df['median_household_income'] / df['median_earnings']
            )

        return df

    def save_parsed_data(self, df: pd.DataFrame, output_path='data_cleaned/personal_income_parsed.csv'):
        """Save parsed data to CSV."""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        df.to_csv(output_file, index=False)
        print(f"\n✓ Parsed data saved to: {output_file}")
        print(f"  Shape: {df.shape}")
        print(f"  Columns: {list(df.columns)}")


def main():
    """Main execution function."""
    parser = PersonalIncomeParser()

    # Parse all files
    df = parser.parse_all_files()

    if len(df) == 0:
        print("\n⚠ No data parsed. Please add ACS CSV files to the Personal Income folder.")
        print("   See DATA_COLLECTION_GUIDE.py for instructions.")
        return

    # Merge tables
    print("\n" + "="*60)
    print("MERGING DATA")
    print("="*60)
    merged_df = parser.merge_income_data(df)
    print(
        f"\n✓ Merged {len(df)} records into {len(merged_df)} combined records")

    # Calculate derived metrics
    print("\n" + "="*60)
    print("CALCULATING DERIVED METRICS")
    print("="*60)
    final_df = parser.calculate_derived_metrics(merged_df)

    if 'gender_earnings_gap_pct' in final_df.columns:
        print(f"\n✓ Gender earnings gap:")
        print(f"  Mean: {final_df['gender_earnings_gap_pct'].mean():.2f}%")
        print(
            f"  Range: {final_df['gender_earnings_gap_pct'].min():.2f}% - {final_df['gender_earnings_gap_pct'].max():.2f}%")

    # Save results
    parser.save_parsed_data(final_df)

    # Display summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print("\nSample data:")
    print(final_df.head().to_string())

    return final_df


if __name__ == "__main__":
    df = main()

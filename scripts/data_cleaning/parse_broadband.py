"""
Parse Broadband Access Data (ACS Tables B28008 and S2801)
Extracts computer ownership and internet subscription metrics for Lonoke County, Arkansas
"""

import pandas as pd
import glob
import os
from pathlib import Path


class BroadbandParser:
    def __init__(self, data_dir="Data Drive Datasets/Data That Back IGS (Problem)/Place Pillar Data/Severely Limited Broadband Access_"):
        self.data_dir = data_dir
        self.b28008_dir = os.path.join(
            data_dir, "B28008 - Presence of a Computer and Type of Internet Subscription in Household")
        self.s2801_dir = os.path.join(
            data_dir, "S2801 Types of Computers and Internet Subscriptions")

    def parse_b28008_file(self, filepath):
        """Parse B28008 table - Computer and Internet Subscription in Household"""
        try:
            # Read Excel file (skip metadata rows)
            df = pd.read_excel(filepath, header=1)

            # Extract year and estimate type from filename
            filename = os.path.basename(filepath)
            parts = filename.split('.')
            estimate_info = parts[0]  # e.g., "ACSDT1Y2024" or "ACSDT5Y2023"

            if '1Y' in estimate_info:
                estimate_type = '1-year'
                year = int(estimate_info.split('1Y')[1])
            else:
                estimate_type = '5-year'
                year = int(estimate_info.split('5Y')[1])

            # Filter for Lonoke County
            if 'Geographic Area Name' in df.columns or 'Label (Grouping)' in df.columns:
                geo_col = 'Geographic Area Name' if 'Geographic Area Name' in df.columns else 'Label (Grouping)'
                lonoke_data = df[df[geo_col].str.contains(
                    'Lonoke County', na=False)]

                if lonoke_data.empty:
                    # Try the first data row if no Lonoke County found
                    lonoke_data = df.iloc[[0]]
            else:
                # Just use first row if can't identify geography
                lonoke_data = df.iloc[[0]]

            # Extract key columns (B28008 structure)
            # Total households, with computer, with broadband, no internet
            result = {
                'year': year,
                'estimate_type': estimate_type,
                'source_table': 'B28008',
                'county': 'Lonoke County, Arkansas'
            }

            # Look for total households and internet subscription columns
            for col in df.columns:
                col_lower = str(col).lower()
                if 'total' in col_lower and 'estimate' in col_lower:
                    result['total_households'] = lonoke_data[col].values[0]
                elif 'broadband' in col_lower and 'estimate' in col_lower:
                    result['households_with_broadband'] = lonoke_data[col].values[0]
                elif 'without' in col_lower and 'internet' in col_lower and 'estimate' in col_lower:
                    result['households_no_internet'] = lonoke_data[col].values[0]
                elif 'computer' in col_lower and 'estimate' in col_lower:
                    if 'households_with_computer' not in result:
                        result['households_with_computer'] = lonoke_data[col].values[0]

            return result

        except Exception as e:
            print(f"Error parsing {filepath}: {e}")
            return None

    def parse_s2801_file(self, filepath):
        """Parse S2801 table - Types of Computers and Internet Subscriptions"""
        try:
            # Read Excel file (skip metadata rows)
            df = pd.read_excel(filepath, header=1)

            # Extract year and estimate type from filename
            filename = os.path.basename(filepath)
            parts = filename.split('.')
            estimate_info = parts[0]

            if '1Y' in estimate_info:
                estimate_type = '1-year'
                year = int(estimate_info.split('1Y')[1])
            else:
                estimate_type = '5-year'
                year = int(estimate_info.split('5Y')[1])

            # Filter for Lonoke County
            if 'Geographic Area Name' in df.columns or 'Label (Grouping)' in df.columns:
                geo_col = 'Geographic Area Name' if 'Geographic Area Name' in df.columns else 'Label (Grouping)'
                lonoke_data = df[df[geo_col].str.contains(
                    'Lonoke County', na=False)]

                if lonoke_data.empty:
                    lonoke_data = df.iloc[[0]]
            else:
                lonoke_data = df.iloc[[0]]

            result = {
                'year': year,
                'estimate_type': estimate_type,
                'source_table': 'S2801',
                'county': 'Lonoke County, Arkansas'
            }

            # Extract broadband subscription percentages
            for col in df.columns:
                col_lower = str(col).lower()
                if 'broadband' in col_lower and 'percent' in col_lower:
                    result['broadband_pct'] = lonoke_data[col].values[0]
                elif 'desktop' in col_lower and 'percent' in col_lower:
                    result['desktop_computer_pct'] = lonoke_data[col].values[0]
                elif 'laptop' in col_lower and 'percent' in col_lower:
                    result['laptop_computer_pct'] = lonoke_data[col].values[0]
                elif 'smartphone' in col_lower and 'percent' in col_lower:
                    result['smartphone_pct'] = lonoke_data[col].values[0]
                elif 'tablet' in col_lower and 'percent' in col_lower:
                    result['tablet_pct'] = lonoke_data[col].values[0]

            return result

        except Exception as e:
            print(f"Error parsing {filepath}: {e}")
            return None

    def parse_all_files(self):
        """Parse all broadband data files and combine"""
        all_data = []

        # Parse B28008 files
        b28008_files = glob.glob(os.path.join(self.b28008_dir, "*.xlsx"))
        print(f"Found {len(b28008_files)} B28008 files")
        for filepath in sorted(b28008_files):
            print(f"Parsing {os.path.basename(filepath)}...")
            result = self.parse_b28008_file(filepath)
            if result:
                all_data.append(result)

        # Parse S2801 files
        s2801_files = glob.glob(os.path.join(self.s2801_dir, "*.xlsx"))
        print(f"Found {len(s2801_files)} S2801 files")
        for filepath in sorted(s2801_files):
            print(f"Parsing {os.path.basename(filepath)}...")
            result = self.parse_s2801_file(filepath)
            if result:
                all_data.append(result)

        # Convert to DataFrame
        df = pd.DataFrame(all_data)

        # Merge B28008 and S2801 data by year and estimate type
        if not df.empty:
            df = self.merge_broadband_data(df)
            df = self.calculate_derived_metrics(df)

        return df

    def merge_broadband_data(self, df):
        """Merge B28008 and S2801 data by year and estimate type"""
        b28008_df = df[df['source_table'] == 'B28008'].copy()
        s2801_df = df[df['source_table'] == 'S2801'].copy()

        # Merge on year and estimate_type
        merged = pd.merge(
            b28008_df,
            s2801_df,
            on=['year', 'estimate_type', 'county'],
            how='outer',
            suffixes=('_b28008', '_s2801')
        )

        # Clean up source_table column
        merged['source_tables'] = 'B28008+S2801'
        merged = merged.drop(
            columns=['source_table_b28008', 'source_table_s2801'], errors='ignore')

        return merged

    def calculate_derived_metrics(self, df):
        """Calculate additional broadband metrics"""
        # Broadband access rate
        if 'total_households' in df.columns and 'households_with_broadband' in df.columns:
            df['broadband_access_rate'] = (
                pd.to_numeric(df['households_with_broadband'], errors='coerce') /
                pd.to_numeric(df['total_households'], errors='coerce') * 100
            )

        # No internet rate
        if 'total_households' in df.columns and 'households_no_internet' in df.columns:
            df['no_internet_rate'] = (
                pd.to_numeric(df['households_no_internet'], errors='coerce') /
                pd.to_numeric(df['total_households'], errors='coerce') * 100
            )

        # Computer ownership rate
        if 'total_households' in df.columns and 'households_with_computer' in df.columns:
            df['computer_ownership_rate'] = (
                pd.to_numeric(df['households_with_computer'], errors='coerce') /
                pd.to_numeric(df['total_households'], errors='coerce') * 100
            )

        # Sort by year and estimate type
        df = df.sort_values(['year', 'estimate_type']).reset_index(drop=True)

        return df

    def save_to_csv(self, df, output_path="data_cleaned/broadband_cleaned.csv"):
        """Save parsed data to CSV"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"\n✓ Saved to {output_path}")
        print(f"  Shape: {df.shape}")
        print(f"  Years: {sorted(df['year'].unique().tolist())}")
        print(
            f"  Estimate types: {sorted(df['estimate_type'].unique().tolist())}")


if __name__ == "__main__":
    parser = BroadbandParser()
    df = parser.parse_all_files()

    if not df.empty:
        print("\n" + "="*60)
        print("BROADBAND DATA SUMMARY")
        print("="*60)
        print(df.head(10))
        print("\nColumns:", df.columns.tolist())

        parser.save_to_csv(df)
    else:
        print("No data parsed. Check file paths and formats.")

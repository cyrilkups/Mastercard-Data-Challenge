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
            # Read Excel file with proper header
            df = pd.read_excel(filepath, header=0)

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

            # Find the Estimate column (contains 'Estimate' in name)
            estimate_col = [
                col for col in df.columns if 'Estimate' in str(col)][0]

            result = {
                'year': year,
                'estimate_type': estimate_type,
                'source_table': 'B28008',
                'county': 'Lonoke County, Arkansas'
            }

            # Extract values by matching label text
            for idx, row in df.iterrows():
                label = str(row.iloc[0]).strip().replace(
                    '\xa0', '').replace(' ', '').lower()
                value = row[estimate_col]

                if label == 'total:':
                    result['total_households'] = value
                elif 'hasacomputer:' in label and label.count(':') == 1:
                    result['households_with_computer'] = value
                elif 'broadbandsubscription:' in label:
                    result['households_with_broadband'] = value
                elif 'withoutinternetsubscription' in label:
                    result['households_no_internet'] = value

            return result

        except Exception as e:
            print(f"Error parsing {filepath}: {e}")
            return None

    def parse_s2801_file(self, filepath):
        """Parse S2801 table - Types of Computers and Internet Subscriptions"""
        try:
            # Read Excel file
            df = pd.read_excel(filepath, header=0)

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

            # Find columns with 'Percent' in them
            percent_col = None
            for col in df.columns:
                if 'Percent' in str(col) and 'Estimate' in str(col):
                    percent_col = col
                    break

            result = {
                'year': year,
                'estimate_type': estimate_type,
                'source_table': 'S2801',
                'county': 'Lonoke County, Arkansas'
            }

            if percent_col:
                # Extract percentages from first data row
                for idx, row in df.iterrows():
                    label = str(row.iloc[0]).strip().replace(
                        '\xa0', '').lower()

                    if 'broadband' in label and percent_col:
                        result['broadband_pct'] = row[percent_col]
                        break

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
        print("\nSample data:")
        print(df[['year', 'estimate_type', 'total_households',
              'households_with_broadband', 'broadband_access_rate']].head())

        parser.save_to_csv(df)
    else:
        print("No data parsed. Check file paths and formats.")

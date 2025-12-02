"""
Parse Housing Data (ACS Tables B25002 and S2501)
Extracts occupancy status and housing characteristics for Lonoke County, Arkansas
"""

import pandas as pd
import glob
import os
from pathlib import Path


class HousingParser:
    def __init__(self, data_dir="Data Drive Datasets/Data That Back IGS (Problem)/Place Pillar Data/Housing Market Decline & Out-Migration"):
        self.data_dir = data_dir
        self.b25002_dir = os.path.join(data_dir, "B25002 – Occupancy Status")
        self.s2501_dir = os.path.join(
            data_dir, "S2501 – Occupancy Characteristics")

    def parse_b25002_file(self, filepath):
        """Parse B25002 table - Occupancy Status"""
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
                'source_table': 'B25002',
                'county': 'Lonoke County, Arkansas'
            }

            # Extract housing unit counts
            for col in df.columns:
                col_lower = str(col).lower()
                if 'total' in col_lower and 'estimate' in col_lower:
                    result['total_housing_units'] = lonoke_data[col].values[0]
                elif 'occupied' in col_lower and 'estimate' in col_lower and 'vacant' not in col_lower:
                    result['occupied_units'] = lonoke_data[col].values[0]
                elif 'vacant' in col_lower and 'estimate' in col_lower:
                    result['vacant_units'] = lonoke_data[col].values[0]

            return result

        except Exception as e:
            print(f"Error parsing {filepath}: {e}")
            return None

    def parse_s2501_file(self, filepath):
        """Parse S2501 table - Occupancy Characteristics"""
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
                'source_table': 'S2501',
                'county': 'Lonoke County, Arkansas'
            }

            # Extract key housing metrics
            for col in df.columns:
                col_lower = str(col).lower()
                # Owner-occupied
                if 'owner' in col_lower and 'occupied' in col_lower:
                    if 'percent' in col_lower:
                        result['owner_occupied_pct'] = lonoke_data[col].values[0]
                    elif 'estimate' in col_lower and 'owner_occupied_units' not in result:
                        result['owner_occupied_units'] = lonoke_data[col].values[0]
                # Renter-occupied
                elif 'renter' in col_lower and 'occupied' in col_lower:
                    if 'percent' in col_lower:
                        result['renter_occupied_pct'] = lonoke_data[col].values[0]
                    elif 'estimate' in col_lower and 'renter_occupied_units' not in result:
                        result['renter_occupied_units'] = lonoke_data[col].values[0]
                # Vacancy rate
                elif 'vacancy' in col_lower and ('rate' in col_lower or 'percent' in col_lower):
                    result['vacancy_rate'] = lonoke_data[col].values[0]
                # Median value
                elif 'median' in col_lower and 'value' in col_lower and 'estimate' in col_lower:
                    result['median_home_value'] = lonoke_data[col].values[0]
                # Median rent
                elif 'median' in col_lower and ('rent' in col_lower or 'gross rent' in col_lower) and 'estimate' in col_lower:
                    result['median_gross_rent'] = lonoke_data[col].values[0]

            return result

        except Exception as e:
            print(f"Error parsing {filepath}: {e}")
            return None

    def parse_all_files(self):
        """Parse all housing data files and combine"""
        all_data = []

        # Parse B25002 files
        b25002_files = glob.glob(os.path.join(self.b25002_dir, "*.xlsx"))
        print(f"Found {len(b25002_files)} B25002 files")
        for filepath in sorted(b25002_files):
            print(f"Parsing {os.path.basename(filepath)}...")
            result = self.parse_b25002_file(filepath)
            if result:
                all_data.append(result)

        # Parse S2501 files
        s2501_files = glob.glob(os.path.join(self.s2501_dir, "*.xlsx"))
        print(f"Found {len(s2501_files)} S2501 files")
        for filepath in sorted(s2501_files):
            print(f"Parsing {os.path.basename(filepath)}...")
            result = self.parse_s2501_file(filepath)
            if result:
                all_data.append(result)

        # Convert to DataFrame
        df = pd.DataFrame(all_data)

        # Merge and calculate metrics
        if not df.empty:
            df = self.merge_housing_data(df)
            df = self.calculate_derived_metrics(df)

        return df

    def merge_housing_data(self, df):
        """Merge B25002 and S2501 data by year and estimate type"""
        b25002_df = df[df['source_table'] == 'B25002'].copy()
        s2501_df = df[df['source_table'] == 'S2501'].copy()

        # Merge on year and estimate_type
        merged = pd.merge(
            b25002_df,
            s2501_df,
            on=['year', 'estimate_type', 'county'],
            how='outer',
            suffixes=('_b25002', '_s2501')
        )

        # Clean up source_table column
        merged['source_tables'] = 'B25002+S2501'
        merged = merged.drop(
            columns=['source_table_b25002', 'source_table_s2501'], errors='ignore')

        return merged

    def calculate_derived_metrics(self, df):
        """Calculate additional housing metrics"""
        # Occupancy rate
        if 'total_housing_units' in df.columns and 'occupied_units' in df.columns:
            df['occupancy_rate'] = (
                pd.to_numeric(df['occupied_units'], errors='coerce') /
                pd.to_numeric(df['total_housing_units'], errors='coerce') * 100
            )

        # Vacancy rate (if not already present from S2501)
        if 'total_housing_units' in df.columns and 'vacant_units' in df.columns and 'vacancy_rate' not in df.columns:
            df['vacancy_rate_calculated'] = (
                pd.to_numeric(df['vacant_units'], errors='coerce') /
                pd.to_numeric(df['total_housing_units'], errors='coerce') * 100
            )

        # Homeownership rate
        if 'occupied_units' in df.columns and 'owner_occupied_units' in df.columns:
            df['homeownership_rate'] = (
                pd.to_numeric(df['owner_occupied_units'], errors='coerce') /
                pd.to_numeric(df['occupied_units'], errors='coerce') * 100
            )

        # Rent-to-value ratio (affordability indicator)
        if 'median_gross_rent' in df.columns and 'median_home_value' in df.columns:
            df['monthly_rent_to_home_value_ratio'] = (
                pd.to_numeric(df['median_gross_rent'], errors='coerce') /
                pd.to_numeric(df['median_home_value'], errors='coerce') * 100
            )

        # Sort by year and estimate type
        df = df.sort_values(['year', 'estimate_type']).reset_index(drop=True)

        return df

    def save_to_csv(self, df, output_path="data_cleaned/housing_cleaned.csv"):
        """Save parsed data to CSV"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"\n✓ Saved to {output_path}")
        print(f"  Shape: {df.shape}")
        print(f"  Years: {sorted(df['year'].unique().tolist())}")
        print(
            f"  Estimate types: {sorted(df['estimate_type'].unique().tolist())}")


if __name__ == "__main__":
    parser = HousingParser()
    df = parser.parse_all_files()

    if not df.empty:
        print("\n" + "="*60)
        print("HOUSING DATA SUMMARY")
        print("="*60)
        print(df.head(10))
        print("\nColumns:", df.columns.tolist())

        parser.save_to_csv(df)
    else:
        print("No data parsed. Check file paths and formats.")

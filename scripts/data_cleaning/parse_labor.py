"""
Parse Labor Market Data (Business Dynamics Statistics - BDSTIMESERIES)
Extracts job creation, firm dynamics, and establishment data for Lonoke County, Arkansas
"""

import pandas as pd
import glob
import os
from pathlib import Path


class LaborParser:
    def __init__(self, data_dir="Data Drive Datasets/Data That Back IGS (Problem)/Economic Pillar Data"):
        self.data_dir = data_dir
        self.lmei_dir = os.path.join(
            data_dir, "Labor Market Engagement Index (LMEI)")
        self.unemployment_dir = os.path.join(
            data_dir, "Local Area Unemployment Statistics")

    def parse_bds_file(self, filepath):
        """Parse Business Dynamics Statistics CSV files"""
        try:
            # Read CSV file
            df = pd.read_csv(filepath)

            # Filter for Lonoke County
            if 'Geographic Area Name (NAME)' in df.columns:
                lonoke_data = df[df['Geographic Area Name (NAME)'].str.contains(
                    'Lonoke County', na=False)]
            elif 'NAME' in df.columns:
                lonoke_data = df[df['NAME'].str.contains(
                    'Lonoke County', na=False)]
            else:
                print(f"Warning: No geography column found in {filepath}")
                return None

            if lonoke_data.empty:
                print(f"Warning: No Lonoke County data in {filepath}")
                return None

            # Select relevant columns
            filename = os.path.basename(filepath)

            # Standardize column names
            column_mapping = {
                'Year (time)': 'year',
                'time': 'year',
                'Geographic Area Name (NAME)': 'county',
                'NAME': 'county',
                'Number of firms (FIRM)': 'num_firms',
                'FIRM': 'num_firms',
                'Number of establishments (ESTAB)': 'num_establishments',
                'ESTAB': 'num_establishments',
                'Number of employees (EMP)': 'num_employees',
                'EMP': 'num_employees',
                'Number of establishments born during the last 12 months (ESTABS_ENTRY)': 'establishments_born',
                'ESTABS_ENTRY': 'establishments_born',
                'Rate of establishments born during the last 12 months (ESTABS_ENTRY_RATE)': 'establishment_birth_rate',
                'ESTABS_ENTRY_RATE': 'establishment_birth_rate',
                'Number of establishments exited during the last 12 months (ESTABS_EXIT)': 'establishments_exited',
                'ESTABS_EXIT': 'establishments_exited',
                'Rate of establishments exited during the last 12 months (ESTABS_EXIT_RATE)': 'establishment_exit_rate',
                'ESTABS_EXIT_RATE': 'establishment_exit_rate',
                'Number of jobs created from expanding and opening establishments during the last 12 months (JOB_CREATION)': 'jobs_created',
                'JOB_CREATION': 'jobs_created',
                'Rate of jobs created from expanding and opening establishments during the last 12 months (JOB_CREATION_RATE)': 'job_creation_rate',
                'JOB_CREATION_RATE': 'job_creation_rate',
                'Number of jobs lost from contracting and closing establishments during the last 12 months (JOB_DESTRUCTION)': 'jobs_destroyed',
                'JOB_DESTRUCTION': 'jobs_destroyed',
                'Rate of jobs lost from contracting and closing establishments during the last 12 months (JOB_DESTRUCTION_RATE)': 'job_destruction_rate',
                'JOB_DESTRUCTION_RATE': 'job_destruction_rate',
                'Number of net jobs created from expanding/contracting and opening/closing establishments during the last 12 months (NET_JOB_CREATION)': 'net_jobs_created',
                'NET_JOB_CREATION': 'net_jobs_created',
                'Rate of net jobs created from expanding/contracting and opening/closing establishments during the last 12 months (NET_JOB_CREATION_RATE)': 'net_job_creation_rate',
                'NET_JOB_CREATION_RATE': 'net_job_creation_rate',
                'Rate of reallocation during the last 12 months (REALLOCATION_RATE)': 'reallocation_rate',
                'REALLOCATION_RATE': 'reallocation_rate',
                'Number of firms that exited during the last 12 months (FIRMDEATH_FIRMS)': 'firms_exited',
                'FIRMDEATH_FIRMS': 'firms_exited',
                'Number of employees associated with firm deaths during the last 12 months (FIRMDEATH_EMP)': 'employees_from_firm_deaths',
                'FIRMDEATH_EMP': 'employees_from_firm_deaths'
            }

            # Rename columns that exist
            lonoke_data = lonoke_data.rename(columns=column_mapping)

            # Add source file identifier
            if 'BDSEAGE' in filename:
                lonoke_data['source_file'] = 'BDSEAGE'
            elif 'BDSGEO' in filename:
                lonoke_data['source_file'] = 'BDSGEO'
            else:
                lonoke_data['source_file'] = filename

            return lonoke_data

        except Exception as e:
            print(f"Error parsing {filepath}: {e}")
            return None

    def parse_unemployment_file(self, filepath):
        """Parse Local Area Unemployment Statistics Excel file"""
        try:
            # Read Excel file
            df = pd.read_excel(filepath, header=0)

            # Look for relevant columns
            result_data = []

            # Try to identify year, area, unemployment rate columns
            for idx, row in df.iterrows():
                # Skip header rows
                if pd.isna(row.iloc[0]):
                    continue

                result = {}

                # Extract year (usually in first column or in area name)
                for col in df.columns:
                    col_lower = str(col).lower()
                    if 'year' in col_lower:
                        result['year'] = row[col]
                    elif 'area' in col_lower or 'county' in col_lower:
                        if 'Lonoke' in str(row[col]):
                            result['county'] = row[col]
                    elif 'unemployment' in col_lower and 'rate' in col_lower:
                        result['unemployment_rate'] = row[col]
                    elif 'labor' in col_lower and 'force' in col_lower:
                        result['labor_force'] = row[col]
                    elif 'employed' in col_lower:
                        result['employed'] = row[col]
                    elif 'unemployed' in col_lower:
                        result['unemployed'] = row[col]

                if result and 'county' in result:
                    result['source_file'] = 'unemployment_stats'
                    result_data.append(result)

            if result_data:
                return pd.DataFrame(result_data)
            else:
                return None

        except Exception as e:
            print(f"Error parsing {filepath}: {e}")
            return None

    def parse_all_files(self):
        """Parse all labor market data files"""
        all_data = []

        # Parse BDS files (LMEI directory)
        bds_files = glob.glob(os.path.join(self.lmei_dir, "*.csv"))
        print(f"Found {len(bds_files)} BDS files")
        for filepath in sorted(bds_files):
            print(f"Parsing {os.path.basename(filepath)}...")
            result = self.parse_bds_file(filepath)
            if result is not None and not result.empty:
                all_data.append(result)

        # Parse unemployment files
        unemployment_files = glob.glob(
            os.path.join(self.unemployment_dir, "*.xlsx"))
        print(f"Found {len(unemployment_files)} unemployment files")
        for filepath in sorted(unemployment_files):
            print(f"Parsing {os.path.basename(filepath)}...")
            result = self.parse_unemployment_file(filepath)
            if result is not None and not result.empty:
                all_data.append(result)

        # Combine all DataFrames
        if all_data:
            df = pd.concat(all_data, ignore_index=True)
            df = self.calculate_derived_metrics(df)
            return df
        else:
            return pd.DataFrame()

    def calculate_derived_metrics(self, df):
        """Calculate additional labor market metrics"""
        # Job churn rate (total job creation + destruction)
        if 'jobs_created' in df.columns and 'jobs_destroyed' in df.columns:
            df['job_churn'] = (
                pd.to_numeric(df['jobs_created'], errors='coerce') +
                pd.to_numeric(df['jobs_destroyed'], errors='coerce')
            )

        # Net establishment change
        if 'establishments_born' in df.columns and 'establishments_exited' in df.columns:
            df['net_establishments_change'] = (
                pd.to_numeric(df['establishments_born'], errors='coerce') -
                pd.to_numeric(df['establishments_exited'], errors='coerce')
            )

        # Employees per firm
        if 'num_employees' in df.columns and 'num_firms' in df.columns:
            df['employees_per_firm'] = (
                pd.to_numeric(df['num_employees'], errors='coerce') /
                pd.to_numeric(df['num_firms'], errors='coerce')
            )

        # Establishments per firm
        if 'num_establishments' in df.columns and 'num_firms' in df.columns:
            df['establishments_per_firm'] = (
                pd.to_numeric(df['num_establishments'], errors='coerce') /
                pd.to_numeric(df['num_firms'], errors='coerce')
            )

        # Employment rate (if unemployment data available)
        if 'labor_force' in df.columns and 'employed' in df.columns:
            df['employment_rate'] = (
                pd.to_numeric(df['employed'], errors='coerce') /
                pd.to_numeric(df['labor_force'], errors='coerce') * 100
            )

        # Sort by year
        if 'year' in df.columns:
            df = df.sort_values('year').reset_index(drop=True)

        return df

    def save_to_csv(self, df, output_path="data_cleaned/labor_cleaned.csv"):
        """Save parsed data to CSV"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"\n✓ Saved to {output_path}")
        print(f"  Shape: {df.shape}")
        if 'year' in df.columns:
            years = df['year'].dropna().unique()
            print(
                f"  Years: {sorted([int(y) for y in years if str(y).isdigit()])}")
        print(f"  Source files: {df['source_file'].unique().tolist()}")


if __name__ == "__main__":
    parser = LaborParser()
    df = parser.parse_all_files()

    if not df.empty:
        print("\n" + "="*60)
        print("LABOR MARKET DATA SUMMARY")
        print("="*60)
        print(df.head(10))
        print("\nColumns:", df.columns.tolist())

        parser.save_to_csv(df)
    else:
        print("No data parsed. Check file paths and formats.")

"""
Parse Business Dynamics Data (Annual Business Survey and County Business Patterns)
Extracts business counts, revenue, employment, and payroll data for Lonoke County, Arkansas
"""

import pandas as pd
import glob
import os
from pathlib import Path


class BusinessParser:
    def __init__(self, data_dir="Data Drive Datasets/Data That Back IGS (Problem)/Economic Pillar Data/Decline in Local Businesses"):
        self.data_dir = data_dir

    def parse_abs_file(self, filepath):
        """Parse Annual Business Survey (ABSNESD) CSV file"""
        try:
            # Read CSV file
            df = pd.read_csv(filepath)

            # Filter for Lonoke County and total for all sectors
            lonoke_data = df[
                (df['Geographic Area Name (NAME)'].str.contains('Lonoke County', na=False)) &
                # Total for all sectors
                (df['2022 NAICS code (NAICS2022)'] == '00') &
                (df['Meaning of Sex code (SEX_LABEL)'] == 'Total') &
                (df['Meaning of Ethnicity code (ETH_GROUP_LABEL)'] == 'Total') &
                (df['Meaning of Race code (RACE_GROUP_LABEL)'] == 'Total') &
                (df['Meaning of Veteran code (VET_GROUP_LABEL)'] == 'Total')
            ].copy()

            if lonoke_data.empty:
                print(f"Warning: No Lonoke County data in {filepath}")
                return None

            # Extract key metrics
            result = {
                'year': lonoke_data['Year (YEAR)'].values[0],
                'county': lonoke_data['Geographic Area Name (NAME)'].values[0],
                'source_table': 'ABS',
                'total_firms': lonoke_data['Total number of employer and nonemployer firms (FIRMALL)'].values[0],
                'employer_firms': lonoke_data['Number of employer firms (FIRMPDEMP)'].values[0],
                'nonemployer_firms': lonoke_data['Number of nonemployer firms (FIRMNOPD)'].values[0],
                'total_revenue_thousands': lonoke_data['Total sales, value of shipments, or revenue of employer and nonemployer firms ($1,000) (RCPALL)'].values[0],
                'employer_revenue_thousands': lonoke_data['Sales, value of shipments, or revenue of employer firms ($1,000) (RCPPDEMP)'].values[0],
                'nonemployer_revenue_thousands': lonoke_data['Sales, value of shipments, or revenue of nonemployer firms ($1,000) (RCPNOPD)'].values[0],
                'num_employees': lonoke_data['Number of employees (EMP)'].values[0],
                'annual_payroll_thousands': lonoke_data['Annual payroll ($1,000) (PAYANN)'].values[0]
            }

            return result

        except Exception as e:
            print(f"Error parsing {filepath}: {e}")
            return None

    def parse_cbp_file(self, filepath):
        """Parse County Business Patterns (CBP) CSV file"""
        try:
            # Read CSV file
            df = pd.read_csv(filepath)

            # Filter for Lonoke County and total for all sectors
            lonoke_data = df[
                (df['Geographic Area Name (NAME)'].str.contains('Lonoke County', na=False)) &
                # Total for all sectors
                (df['2022 NAICS Code (NAICS2022)'] == '00')
            ].copy()

            if lonoke_data.empty:
                print(f"Warning: No Lonoke County data in {filepath}")
                return None

            # Extract key metrics
            result = {
                'year': lonoke_data['Year (YEAR)'].values[0] if 'Year (YEAR)' in lonoke_data.columns else 2023,
                'county': lonoke_data['Geographic Area Name (NAME)'].values[0],
                'source_table': 'CBP',
                'num_establishments': lonoke_data['Number of establishments (ESTAB)'].values[0] if 'Number of establishments (ESTAB)' in lonoke_data.columns else None,
                'num_employees_cbp': lonoke_data['Number of employees during pay period including March 12 (EMP)'].values[0] if 'Number of employees during pay period including March 12 (EMP)' in lonoke_data.columns else None,
                'annual_payroll_thousands_cbp': lonoke_data['Annual payroll ($1,000) (PAYANN)'].values[0] if 'Annual payroll ($1,000) (PAYANN)' in lonoke_data.columns else None,
                'first_quarter_payroll_thousands': lonoke_data['First-quarter payroll ($1,000) (AP)'].values[0] if 'First-quarter payroll ($1,000) (AP)' in lonoke_data.columns else None
            }

            return result

        except Exception as e:
            print(f"Error parsing {filepath}: {e}")
            return None

    def parse_all_files(self):
        """Parse all business data files"""
        all_data = []

        # Parse ABS files
        abs_files = glob.glob(os.path.join(self.data_dir, "ABSNESD*.csv"))
        print(f"Found {len(abs_files)} ABS files")
        for filepath in sorted(abs_files):
            print(f"Parsing {os.path.basename(filepath)}...")
            result = self.parse_abs_file(filepath)
            if result:
                all_data.append(result)

        # Parse CBP files
        cbp_files = glob.glob(os.path.join(self.data_dir, "CBP*.csv"))
        print(f"Found {len(cbp_files)} CBP files")
        for filepath in sorted(cbp_files):
            print(f"Parsing {os.path.basename(filepath)}...")
            result = self.parse_cbp_file(filepath)
            if result:
                all_data.append(result)

        # Convert to DataFrame
        df = pd.DataFrame(all_data)

        # Merge and calculate metrics
        if not df.empty:
            df = self.merge_business_data(df)
            df = self.calculate_derived_metrics(df)

        return df

    def merge_business_data(self, df):
        """Merge ABS and CBP data by year"""
        abs_df = df[df['source_table'] == 'ABS'].copy()
        cbp_df = df[df['source_table'] == 'CBP'].copy()

        if abs_df.empty and cbp_df.empty:
            return df
        elif abs_df.empty:
            return cbp_df
        elif cbp_df.empty:
            return abs_df

        # Merge on year and county
        merged = pd.merge(
            abs_df,
            cbp_df,
            on=['year', 'county'],
            how='outer',
            suffixes=('_abs', '_cbp')
        )

        # Clean up source_table column
        merged['source_tables'] = 'ABS+CBP'
        merged = merged.drop(
            columns=['source_table_abs', 'source_table_cbp'], errors='ignore')

        return merged

    def calculate_derived_metrics(self, df):
        """Calculate additional business metrics"""
        # Revenue per firm
        if 'total_revenue_thousands' in df.columns and 'total_firms' in df.columns:
            df['revenue_per_firm_thousands'] = (
                pd.to_numeric(df['total_revenue_thousands'], errors='coerce') /
                pd.to_numeric(df['total_firms'], errors='coerce')
            )

        # Revenue per employee
        if 'employer_revenue_thousands' in df.columns and 'num_employees' in df.columns:
            df['revenue_per_employee_thousands'] = (
                pd.to_numeric(df['employer_revenue_thousands'], errors='coerce') /
                pd.to_numeric(df['num_employees'], errors='coerce')
            )

        # Average payroll per employee
        if 'annual_payroll_thousands' in df.columns and 'num_employees' in df.columns:
            df['payroll_per_employee_thousands'] = (
                pd.to_numeric(df['annual_payroll_thousands'], errors='coerce') /
                pd.to_numeric(df['num_employees'], errors='coerce')
            )

        # Employer firm ratio
        if 'employer_firms' in df.columns and 'total_firms' in df.columns:
            df['employer_firm_ratio'] = (
                pd.to_numeric(df['employer_firms'], errors='coerce') /
                pd.to_numeric(df['total_firms'], errors='coerce') * 100
            )

        # Nonemployer firm ratio
        if 'nonemployer_firms' in df.columns and 'total_firms' in df.columns:
            df['nonemployer_firm_ratio'] = (
                pd.to_numeric(df['nonemployer_firms'], errors='coerce') /
                pd.to_numeric(df['total_firms'], errors='coerce') * 100
            )

        # Revenue concentration (employer vs total)
        if 'employer_revenue_thousands' in df.columns and 'total_revenue_thousands' in df.columns:
            df['employer_revenue_share'] = (
                pd.to_numeric(df['employer_revenue_thousands'], errors='coerce') /
                pd.to_numeric(df['total_revenue_thousands'],
                              errors='coerce') * 100
            )

        # Employees per establishment (from CBP data)
        if 'num_employees_cbp' in df.columns and 'num_establishments' in df.columns:
            df['employees_per_establishment'] = (
                pd.to_numeric(df['num_employees_cbp'], errors='coerce') /
                pd.to_numeric(df['num_establishments'], errors='coerce')
            )

        # Sort by year
        if 'year' in df.columns:
            df = df.sort_values('year').reset_index(drop=True)

        return df

    def save_to_csv(self, df, output_path="data_cleaned/business_cleaned.csv"):
        """Save parsed data to CSV"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"\n✓ Saved to {output_path}")
        print(f"  Shape: {df.shape}")
        if 'year' in df.columns:
            print(f"  Years: {sorted(df['year'].unique().tolist())}")
        if 'source_tables' in df.columns:
            print(f"  Source tables: {df['source_tables'].unique().tolist()}")
        elif 'source_table' in df.columns:
            print(f"  Source tables: {df['source_table'].unique().tolist()}")


if __name__ == "__main__":
    parser = BusinessParser()
    df = parser.parse_all_files()

    if not df.empty:
        print("\n" + "="*60)
        print("BUSINESS DATA SUMMARY")
        print("="*60)
        print(df.head(10))
        print("\nColumns:", df.columns.tolist())

        parser.save_to_csv(df)
    else:
        print("No data parsed. Check file paths and formats.")

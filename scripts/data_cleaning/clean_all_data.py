"""
Master Data Cleaning Script - Create all cleaned datasets
Generates: broadband_cleaned.csv, housing_cleaned.csv, labor_cleaned.csv, business_cleaned.csv
"""

import pandas as pd
import glob
import os
import numpy as np


def clean_label(label):
    """Clean label text by removing non-breaking spaces and extra whitespace"""
    return str(label).strip().replace('\xa0', '').replace(' ', '').lower()


def extract_year_and_estimate(filename):
    """Extract year and estimate type from ACS filename"""
    parts = filename.split('.')
    estimate_info = parts[0]

    if '1Y' in estimate_info:
        estimate_type = '1-year'
        year = int(estimate_info.split('1Y')[1])
    else:
        estimate_type = '5-year'
        year = int(estimate_info.split('5Y')[1])

    return year, estimate_type

#############################################################################
# BROADBAND DATA
#############################################################################


def parse_broadband_data():
    """Parse broadband access data from B28008 and S2801 tables"""
    print("\n" + "="*70)
    print("PARSING BROADBAND DATA")
    print("="*70)

    base_dir = "Data Drive Datasets/Data That Back IGS (Problem)/Place Pillar Data/Severely Limited Broadband Access_"
    all_data = []

    # Parse B28008 files
    b28008_dir = os.path.join(
        base_dir, "B28008 - Presence of a Computer and Type of Internet Subscription in Household")
    b28008_files = glob.glob(os.path.join(b28008_dir, "*.xlsx"))

    for filepath in sorted(b28008_files):
        try:
            df = pd.read_excel(filepath, header=0)
            year, estimate_type = extract_year_and_estimate(
                os.path.basename(filepath))

            estimate_col = [
                col for col in df.columns if 'Estimate' in str(col)][0]

            result = {
                'year': year,
                'estimate_type': estimate_type,
                'county': 'Lonoke County, Arkansas'
            }

            for idx, row in df.iterrows():
                label = clean_label(row.iloc[0])
                value = row[estimate_col]

                if label == 'total:':
                    result['total_households'] = value
                elif 'hasacomputer:' in label and label.count(':') == 1:
                    result['households_with_computer'] = value
                elif 'broadbandsubscription:' in label and 'witha' in label:
                    result['households_with_broadband'] = value
                elif 'withoutinternetsubscription' in label:
                    result['households_no_internet'] = value

            all_data.append(result)
            print(f"  ✓ {os.path.basename(filepath)}")
        except Exception as e:
            print(f"  ✗ {os.path.basename(filepath)}: {e}")

    df = pd.DataFrame(all_data)

    # Calculate derived metrics
    df['broadband_access_pct'] = (
        df['households_with_broadband'] / df['total_households'] * 100).round(2)
    df['no_internet_pct'] = (
        df['households_no_internet'] / df['total_households'] * 100).round(2)
    df['computer_ownership_pct'] = (
        df['households_with_computer'] / df['total_households'] * 100).round(2)

    df = df.sort_values(['year', 'estimate_type']).reset_index(drop=True)

    return df

#############################################################################
# HOUSING DATA
#############################################################################


def parse_housing_data():
    """Parse housing data from B25002 and S2501 tables"""
    print("\n" + "="*70)
    print("PARSING HOUSING DATA")
    print("="*70)

    base_dir = "Data Drive Datasets/Data That Back IGS (Problem)/Place Pillar Data/Housing Market Decline & Out-Migration"
    all_data = []

    # Parse B25002 files (Occupancy Status)
    b25002_dir = os.path.join(base_dir, "B25002 – Occupancy Status")
    b25002_files = glob.glob(os.path.join(b25002_dir, "*.xlsx"))

    for filepath in sorted(b25002_files):
        try:
            df = pd.read_excel(filepath, header=0)
            year, estimate_type = extract_year_and_estimate(
                os.path.basename(filepath))

            estimate_col = [
                col for col in df.columns if 'Estimate' in str(col)][0]

            result = {
                'year': year,
                'estimate_type': estimate_type,
                'county': 'Lonoke County, Arkansas',
                'source': 'B25002'
            }

            for idx, row in df.iterrows():
                label = clean_label(row.iloc[0])
                value = row[estimate_col]

                if label == 'total:':
                    result['total_housing_units'] = value
                elif label == 'occupied':
                    result['occupied_units'] = value
                elif label == 'vacant':
                    result['vacant_units'] = value

            all_data.append(result)
            print(f"  ✓ {os.path.basename(filepath)}")
        except Exception as e:
            print(f"  ✗ {os.path.basename(filepath)}: {e}")

    # Parse S2501 files (Occupancy Characteristics)
    s2501_dir = os.path.join(base_dir, "S2501 – Occupancy Characteristics")
    s2501_files = glob.glob(os.path.join(s2501_dir, "*.xlsx"))

    for filepath in sorted(s2501_files):
        try:
            df = pd.read_excel(filepath, header=0)
            year, estimate_type = extract_year_and_estimate(
                os.path.basename(filepath))

            estimate_col = [
                col for col in df.columns if 'Estimate' in str(col)][0]

            result = {
                'year': year,
                'estimate_type': estimate_type,
                'county': 'Lonoke County, Arkansas',
                'source': 'S2501'
            }

            for idx, row in df.iterrows():
                label = clean_label(row.iloc[0])
                value = row[estimate_col]

                if 'occupiedhousingunits' == label:
                    result['total_occupied'] = value
                elif 'owner-occupied' == label or 'owneroccupied' == label:
                    result['owner_occupied_units'] = value
                elif 'renter-occupied' == label or 'renteroccupied' == label:
                    result['renter_occupied_units'] = value
                elif 'medianvalue(dollars)' in label or 'median(dollars)' in label:
                    result['median_home_value'] = value
                elif 'mediangrossrent' in label:
                    result['median_gross_rent'] = value
                elif 'vacancyrate' in label:
                    result['vacancy_rate'] = value

            all_data.append(result)
            print(f"  ✓ {os.path.basename(filepath)}")
        except Exception as e:
            print(f"  ✗ {os.path.basename(filepath)}: {e}")

    # Merge B25002 and S2501 data
    df = pd.DataFrame(all_data)

    # Group by year and estimate_type, consolidating data
    grouped = df.groupby(
        ['year', 'estimate_type', 'county']).first().reset_index()

    # Calculate derived metrics
    if 'total_housing_units' in grouped.columns and 'occupied_units' in grouped.columns:
        grouped['occupancy_rate'] = (
            grouped['occupied_units'] / grouped['total_housing_units'] * 100).round(2)
    if 'total_housing_units' in grouped.columns and 'vacant_units' in grouped.columns:
        grouped['vacancy_pct'] = (
            grouped['vacant_units'] / grouped['total_housing_units'] * 100).round(2)
    if 'occupied_units' in grouped.columns and 'owner_occupied_units' in grouped.columns:
        grouped['homeownership_rate'] = (
            grouped['owner_occupied_units'] / grouped['occupied_units'] * 100).round(2)

    grouped = grouped.sort_values(
        ['year', 'estimate_type']).reset_index(drop=True)
    grouped = grouped.drop(columns=['source'], errors='ignore')

    return grouped

#############################################################################
# LABOR MARKET DATA
#############################################################################


def parse_labor_data():
    """Parse labor market data from Business Dynamics Statistics"""
    print("\n" + "="*70)
    print("PARSING LABOR MARKET DATA")
    print("="*70)

    base_dir = "Data Drive Datasets/Data That Back IGS (Problem)/Economic Pillar Data/Labor Market Engagement Index (LMEI)"

    # Parse BDS files
    bds_files = glob.glob(os.path.join(base_dir, "*.csv"))
    all_data = []

    for filepath in sorted(bds_files):
        try:
            df = pd.read_csv(filepath)

            # Filter for Lonoke County and Total for all sectors
            lonoke_data = df[
                (df['Geographic Area Name (NAME)'].str.contains('Lonoke County', na=False)) &
                (df['2017 NAICS Code (NAICS)'] == '00')
            ].copy()

            if lonoke_data.empty:
                continue

            # Rename columns
            lonoke_data = lonoke_data.rename(columns={
                'Year (time)': 'year',
                'Geographic Area Name (NAME)': 'county',
                'Number of firms (FIRM)': 'num_firms',
                'Number of establishments (ESTAB)': 'num_establishments',
                'Number of employees (EMP)': 'num_employees',
                'Number of establishments born during the last 12 months (ESTABS_ENTRY)': 'establishments_born',
                'Number of establishments exited during the last 12 months (ESTABS_EXIT)': 'establishments_exited',
                'Number of jobs created from expanding and opening establishments during the last 12 months (JOB_CREATION)': 'jobs_created',
                'Number of jobs lost from contracting and closing establishments during the last 12 months (JOB_DESTRUCTION)': 'jobs_destroyed',
                'Number of net jobs created from expanding/contracting and opening/closing establishments during the last 12 months (NET_JOB_CREATION)': 'net_jobs_created',
                'Rate of net jobs created from expanding/contracting and opening/closing establishments during the last 12 months (NET_JOB_CREATION_RATE)': 'net_job_creation_rate'
            })

            # Select key columns
            key_cols = ['year', 'county', 'num_firms', 'num_establishments', 'num_employees',
                        'establishments_born', 'establishments_exited', 'jobs_created',
                        'jobs_destroyed', 'net_jobs_created', 'net_job_creation_rate']
            available_cols = [
                col for col in key_cols if col in lonoke_data.columns]

            all_data.append(lonoke_data[available_cols])
            print(f"  ✓ {os.path.basename(filepath)}: {len(lonoke_data)} rows")
        except Exception as e:
            print(f"  ✗ {os.path.basename(filepath)}: {e}")

    if all_data:
        df = pd.concat(all_data, ignore_index=True)

        # Convert numeric columns to proper types
        numeric_cols = ['num_firms', 'num_establishments', 'num_employees',
                        'establishments_born', 'establishments_exited',
                        'jobs_created', 'jobs_destroyed', 'net_jobs_created']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Calculate derived metrics
        df['employees_per_firm'] = (
            df['num_employees'] / df['num_firms']).round(2)
        df['net_establishment_change'] = df['establishments_born'] - \
            df['establishments_exited']
        df['job_churn'] = df['jobs_created'] + df['jobs_destroyed']

        df = df.sort_values('year').reset_index(drop=True)
        return df
    else:
        return pd.DataFrame()

#############################################################################
# BUSINESS DATA
#############################################################################


def parse_business_data():
    """Parse business data from Annual Business Survey"""
    print("\n" + "="*70)
    print("PARSING BUSINESS DATA")
    print("="*70)

    base_dir = "Data Drive Datasets/Data That Back IGS (Problem)/Economic Pillar Data/Decline in Local Businesses"

    # Parse ABS files
    abs_files = glob.glob(os.path.join(base_dir, "ABSNESD*.csv"))
    all_data = []

    for filepath in sorted(abs_files):
        try:
            df = pd.read_csv(filepath)

            # Filter for Lonoke County, all sectors, total demographics
            lonoke_data = df[
                (df['Geographic Area Name (NAME)'].str.contains('Lonoke County', na=False)) &
                (df['2022 NAICS code (NAICS2022)'] == '00') &
                (df['Meaning of Sex code (SEX_LABEL)'] == 'Total') &
                (df['Meaning of Ethnicity code (ETH_GROUP_LABEL)'] == 'Total')
            ].copy()

            if lonoke_data.empty:
                continue

            result = {
                'year': int(lonoke_data['Year (YEAR)'].values[0]),
                'county': lonoke_data['Geographic Area Name (NAME)'].values[0],
                'total_firms': pd.to_numeric(lonoke_data['Total number of employer and nonemployer firms (FIRMALL)'].values[0].replace(',', ''), errors='coerce'),
                'employer_firms': pd.to_numeric(lonoke_data['Number of employer firms (FIRMPDEMP)'].values[0].replace(',', '') if pd.notna(lonoke_data['Number of employer firms (FIRMPDEMP)'].values[0]) else 0, errors='coerce'),
                'nonemployer_firms': pd.to_numeric(lonoke_data['Number of nonemployer firms (FIRMNOPD)'].values[0].replace(',', '') if pd.notna(lonoke_data['Number of nonemployer firms (FIRMNOPD)'].values[0]) else 0, errors='coerce'),
                'total_revenue_thousands': pd.to_numeric(lonoke_data['Total sales, value of shipments, or revenue of employer and nonemployer firms ($1,000) (RCPALL)'].values[0].replace(',', ''), errors='coerce'),
                'num_employees': pd.to_numeric(lonoke_data['Number of employees (EMP)'].values[0].replace(',', '') if pd.notna(lonoke_data['Number of employees (EMP)'].values[0]) else 0, errors='coerce'),
                'annual_payroll_thousands': pd.to_numeric(lonoke_data['Annual payroll ($1,000) (PAYANN)'].values[0].replace(',', '') if pd.notna(lonoke_data['Annual payroll ($1,000) (PAYANN)'].values[0]) else 0, errors='coerce')
            }

            all_data.append(result)
            print(f"  ✓ {os.path.basename(filepath)}")
        except Exception as e:
            print(f"  ✗ {os.path.basename(filepath)}: {e}")

    if all_data:
        df = pd.DataFrame(all_data)

        # Calculate derived metrics
        df['employer_firm_pct'] = (
            df['employer_firms'] / df['total_firms'] * 100).round(2)
        df['revenue_per_firm'] = (
            df['total_revenue_thousands'] / df['total_firms']).round(2)
        df['revenue_per_employee'] = (
            df['total_revenue_thousands'] / df['num_employees']).round(2)
        df['payroll_per_employee'] = (
            df['annual_payroll_thousands'] / df['num_employees']).round(2)

        df = df.sort_values('year').reset_index(drop=True)
        return df
    else:
        return pd.DataFrame()

#############################################################################
# MAIN EXECUTION
#############################################################################


if __name__ == "__main__":
    os.makedirs("data_cleaned", exist_ok=True)

    # Parse all datasets
    broadband_df = parse_broadband_data()
    housing_df = parse_housing_data()
    labor_df = parse_labor_data()
    business_df = parse_business_data()

    # Save all datasets
    print("\n" + "="*70)
    print("SAVING CLEANED DATASETS")
    print("="*70)

    if not broadband_df.empty:
        broadband_df.to_csv("data_cleaned/broadband_cleaned.csv", index=False)
        print(
            f"✓ broadband_cleaned.csv: {broadband_df.shape[0]} rows, {broadband_df.shape[1]} columns")
        print(f"  Years: {sorted(broadband_df['year'].unique())}")

    if not housing_df.empty:
        housing_df.to_csv("data_cleaned/housing_cleaned.csv", index=False)
        print(
            f"✓ housing_cleaned.csv: {housing_df.shape[0]} rows, {housing_df.shape[1]} columns")
        print(f"  Years: {sorted(housing_df['year'].unique())}")

    if not labor_df.empty:
        labor_df.to_csv("data_cleaned/labor_cleaned.csv", index=False)
        print(
            f"✓ labor_cleaned.csv: {labor_df.shape[0]} rows, {labor_df.shape[1]} columns")
        print(
            f"  Years: {sorted(labor_df['year'].unique())[:10]}... (showing first 10)")

    if not business_df.empty:
        business_df.to_csv("data_cleaned/business_cleaned.csv", index=False)
        print(
            f"✓ business_cleaned.csv: {business_df.shape[0]} rows, {business_df.shape[1]} columns")
        print(f"  Years: {sorted(business_df['year'].unique())}")

    print("\n" + "="*70)
    print("ALL DATASETS CLEANED AND SAVED!")
    print("="*70)
    print("\nCleaned files in data_cleaned/ directory:")
    print("  - personal_income_parsed.csv (already exists)")
    print("  - broadband_cleaned.csv")
    print("  - housing_cleaned.csv")
    print("  - labor_cleaned.csv")
    print("  - business_cleaned.csv")

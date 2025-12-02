import pandas as pd
from pathlib import Path

BASE = Path(
    '/Users/cyrilkups/Desktop/DataDrive Project/Data Drive Datasets/Data That Back Solution')
OUT = Path('/Users/cyrilkups/Desktop/DataDrive Project/igs_plus_more_data/integrated_county_solutions.csv')


def clean_numeric(value):
    """Clean Census Bureau numeric values: remove commas, handle suppressed cells"""
    if pd.isna(value):
        return pd.NA
    s = str(value).strip()
    if s in ['S', 'N', 'X', 'D', '']:
        return pd.NA
    return float(s.replace(',', ''))


def read_beltrami_abs():
    """Read ABS NESD 2023 files for Beltrami"""
    bel = BASE / 'Beltrami County'
    results = []
    for fn in bel.glob('ABSNESD2023.*.csv'):
        try:
            df = pd.read_csv(fn)
            # Get total row (NAICS 00, Sex=Total, Ethnicity=Total, Race=Total, Veteran=Total)
            total = df[
                (df.get('2022 NAICS code (NAICS2022)', '') == '00') &
                (df.get('Meaning of Sex code (SEX_LABEL)', '') == 'Total') &
                (df.get('Meaning of Ethnicity code (ETH_GROUP_LABEL)', '') == 'Total') &
                (df.get('Meaning of Race code (RACE_GROUP_LABEL)', '') == 'Total') &
                (df.get('Meaning of Veteran code (VET_GROUP_LABEL)', '') == 'Total')
            ]
            if total.empty:
                continue
            row = total.iloc[0]
            results.append({
                'county': 'Beltrami County',
                'year': 2023,
                'total_firms': clean_numeric(row.get('Total number of employer and nonemployer firms (FIRMALL)')),
                'employer_firms': clean_numeric(row.get('Number of employer firms (FIRMPDEMP)')),
                'nonemployer_firms': clean_numeric(row.get('Number of nonemployer firms (FIRMNOPD)')),
                'total_revenue_k': clean_numeric(row.get('Total sales, value of shipments, or revenue of employer and nonemployer firms ($1,000) (RCPALL)')),
                'employer_revenue_k': clean_numeric(row.get('Sales, value of shipments, or revenue of employer firms ($1,000) (RCPPDEMP)')),
                'nonemployer_revenue_k_abs': clean_numeric(row.get('Sales, value of shipments, or revenue of nonemployer firms ($1,000) (RCPNOPD)')),
                'num_employees': clean_numeric(row.get('Number of employees (EMP)')),
                'annual_payroll': clean_numeric(row.get('Annual payroll ($1,000) (PAYANN)')),
            })
        except Exception as e:
            print(f'Warning ABS {fn.name}: {e}')
    return pd.DataFrame(results)


def read_beltrami_cbp():
    """Read CBP 2020/2023 files for Beltrami"""
    bel = BASE / 'Beltrami County'
    results = []
    for fn in bel.glob('CBP*.csv'):
        try:
            df = pd.read_csv(fn)
            # Get total row (NAICS 00, All establishments)
            total = df[
                (df.get('2017 NAICS code (NAICS2017)', '') == '00') &
                (df.get('Meaning of Employment size of establishments code (EMPSZES_LABEL)',
                 '') == 'All establishments')
            ]
            if total.empty:
                continue
            row = total.iloc[0]
            year_val = row.get('Year (YEAR)')
            results.append({
                'county': 'Beltrami County',
                'year': int(year_val) if year_val else pd.NA,
                'num_establishments': clean_numeric(row.get('Number of establishments (ESTAB)')),
                'num_employees': clean_numeric(row.get('Number of employees (EMP)')),
                'annual_payroll': clean_numeric(row.get('Annual payroll ($1,000) (PAYANN)')),
                'payroll_q1': clean_numeric(row.get('First-quarter payroll ($1,000) (PAYQTR1)')),
            })
        except Exception as e:
            print(f'Warning CBP {fn.name}: {e}')
    return pd.DataFrame(results)


def read_beltrami_nonemp():
    """Read NONEMP 2020 files for Beltrami"""
    bel = BASE / 'Beltrami County'
    results = []
    for fn in bel.glob('NONEMP*.csv'):
        try:
            df = pd.read_csv(fn)
            # Get total row (NAICS 00)
            total = df[df.get('2017 NAICS code (NAICS2017)', '') == '00']
            if total.empty:
                continue
            row = total.iloc[0]
            year_val = row.get('Year (YEAR)')
            results.append({
                'county': 'Beltrami County',
                'year': int(year_val) if year_val else pd.NA,
                'nonemployers': clean_numeric(row.get('Number of nonemployer establishments (NESTAB)')),
                'nonemployer_revenue_k': clean_numeric(row.get('Nonemployer sales, value of shipments, or revenue ($1,000) (NRCPTOT)')),
            })
        except Exception as e:
            print(f'Warning NONEMP {fn.name}: {e}')
    return pd.DataFrame(results)


def read_igs_from_excel(path: Path, county_name: str):
    """Read IGS Excel export"""
    try:
        # Row 1 contains column names
        xl = pd.read_excel(path, sheet_name=0, header=1)
    except Exception as e:
        print(f'Warning reading {path.name}: {e}')
        return pd.DataFrame()

    # Find columns heuristically
    cols_lower = {c.lower(): c for c in xl.columns if isinstance(c, str)}
    year_col = next((c for k, c in cols_lower.items() if 'year' in k), None)
    igs_col = next((c for k, c in cols_lower.items()
                   if 'inclusive growth score' in k), None)
    place_col = next((c for k, c in cols_lower.items() if k ==
                     'place' or 'place score' in k), None)
    economy_col = next((c for k, c in cols_lower.items()
                       if k == 'economy' or 'economy score' in k), None)
    community_col = next((c for k, c in cols_lower.items()
                         if k == 'community' or 'community score' in k), None)

    if not year_col or not igs_col:
        print(f'Warning: Could not find Year/IGS columns in {path.name}')
        print(f'Available columns: {list(xl.columns[:10])}')
        return pd.DataFrame()

    use_cols = [year_col, igs_col]
    rename_map = {year_col: 'year', igs_col: 'igs_score'}
    if place_col:
        use_cols.append(place_col)
        rename_map[place_col] = 'place_score'
    if economy_col:
        use_cols.append(economy_col)
        rename_map[economy_col] = 'economy_score'
    if community_col:
        use_cols.append(community_col)
        rename_map[community_col] = 'community_score'

    df = xl[use_cols].copy()
    df = df.rename(columns=rename_map)
    df['county'] = county_name
    # Drop rows with missing year or IGS
    df = df.dropna(subset=['year', 'igs_score'])
    return df


def main():
    frames = []

    # Beltrami: merge ABS, CBP, NONEMP on county+year
    abs_df = read_beltrami_abs()
    cbp_df = read_beltrami_cbp()
    nonemp_df = read_beltrami_nonemp()

    bel_frames = [df for df in [abs_df, cbp_df, nonemp_df] if not df.empty]
    if bel_frames:
        bel_combined = bel_frames[0]
        for df in bel_frames[1:]:
            bel_combined = bel_combined.merge(
                df, on=['county', 'year'], how='outer', suffixes=('', '_dup'))
            # Drop duplicate columns (keep first)
            bel_combined = bel_combined.loc[:, ~
                                            bel_combined.columns.str.endswith('_dup')]
        frames.append(bel_combined)
        print(
            f'Beltrami: {len(bel_combined)} rows, columns: {list(bel_combined.columns)}')

    # Chaffee County IGS
    chaffee_path = BASE / 'Chaffee County, Colorado' / \
        'Inclusive_Growth_Score_Data_Export_02-12-2025_030333 - Compared to USA.xlsx'
    chaffee = read_igs_from_excel(chaffee_path, 'Chaffee County, Colorado')
    if not chaffee.empty:
        frames.append(chaffee)
        print(f'Chaffee: {len(chaffee)} rows')

    # Fulton County IGS
    fulton_path = BASE / 'Fulton County' / \
        'Inclusive_Growth_Score_Data_Export_02-12-2025_030333 - Compared to USA (1).xlsx'
    fulton = read_igs_from_excel(fulton_path, 'Fulton County')
    if not fulton.empty:
        frames.append(fulton)
        print(f'Fulton: {len(fulton)} rows')

    if not frames:
        print('No solution datasets found.')
        return

    # Concatenate all counties
    combined = pd.concat(frames, ignore_index=True)
    combined['year'] = pd.to_numeric(combined['year'], errors='coerce')
    combined = combined.dropna(subset=['year'])

    # Deduplicate: keep first row for each county+year
    combined = combined.groupby(['county', 'year'], as_index=False).first()
    combined = combined.sort_values(['county', 'year']).reset_index(drop=True)

    combined.to_csv(OUT, index=False)
    print(f'\n✓ Wrote {len(combined)} rows to {OUT}')
    print(f'Columns: {list(combined.columns)}')
    print(f'\nSample data:\n{combined.head(10)}')


if __name__ == '__main__':
    main()

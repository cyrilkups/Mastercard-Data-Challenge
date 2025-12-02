"""
Data Collection Guide for Personal Income (2019-2024)

This guide helps you collect comprehensive Personal Income data from 
the U.S. Census Bureau's American Community Survey (ACS).

DATASETS NEEDED:
================

For Personal Income (Tables S1901 and S2001), collect:
- Years: 2019, 2020, 2021, 2022, 2023, 2024
- Estimates: Both 5-year AND 1-year (where available)

Table S1901: Income in the Past 12 Months (Household/Family Income)
Table S2001: Earnings in the Past 12 Months

NAMING CONVENTION:
==================
Files should follow this pattern:
- 5-year: ACSST5Y{YEAR}.S1901-{timestamp}.csv
- 1-year: ACSST1Y{YEAR}.S1901-{timestamp}.csv

Example:
- ACSST5Y2023.S1901-2025-11-20T230710.csv
- ACSST1Y2024.S1901-2025-11-20T230710.csv

WHERE TO GET THE DATA:
======================

1. Visit: https://data.census.gov/
2. Search for table codes: "S1901" or "S2001"
3. Select:
   - Geography: Lonoke County, Arkansas (or your target counties)
   - Year: 2019-2024
   - Dataset: Choose between:
     * ACS 5-Year Estimates (available for all years)
     * ACS 1-Year Estimates (only for larger populations)
4. Download as CSV

CURRENT STATUS:
===============

✓ S1901 - 2024 (1-year)
✓ S2001 - 2024 (1-year)

NEEDED FILES:
=============

Personal Income - Household/Family (S1901):
[ ] ACSST5Y2019.S1901-*.csv
[ ] ACSST5Y2020.S1901-*.csv
[ ] ACSST5Y2021.S1901-*.csv
[ ] ACSST5Y2022.S1901-*.csv
[ ] ACSST5Y2023.S1901-*.csv
[ ] ACSST1Y2023.S1901-*.csv (if available)
[ ] ACSST1Y2022.S1901-*.csv (if available)
[ ] ACSST1Y2021.S1901-*.csv (if available)
[ ] ACSST1Y2020.S1901-*.csv (if available)
[ ] ACSST1Y2019.S1901-*.csv (if available)

Personal Income - Earnings (S2001):
[ ] ACSST5Y2019.S2001-*.csv
[ ] ACSST5Y2020.S2001-*.csv
[ ] ACSST5Y2021.S2001-*.csv
[ ] ACSST5Y2022.S2001-*.csv
[ ] ACSST5Y2023.S2001-*.csv
[ ] ACSST1Y2023.S2001-*.csv (if available)
[ ] ACSST1Y2022.S2001-*.csv (if available)
[ ] ACSST1Y2021.S2001-*.csv (if available)
[ ] ACSST1Y2020.S2001-*.csv (if available)
[ ] ACSST1Y2019.S2001-*.csv (if available)

NOTES:
======
- 1-year estimates are only available for areas with population ≥65,000
- 5-year estimates are more reliable for smaller areas
- If Lonoke County doesn't qualify for 1-year, use 5-year estimates
- Having both provides redundancy and validation

After downloading, place files in:
Data Drive Datasets/Data That Back IGS (Problem)/Community Pillar/Personal Income/
"""

print(__doc__)

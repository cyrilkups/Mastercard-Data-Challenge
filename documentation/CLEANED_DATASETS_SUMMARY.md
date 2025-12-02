# Cleaned Datasets Summary

## ✅ All Cleaned Datasets Created Successfully!

Located in: `data_cleaned/` directory

---

## 1. **personal_income_parsed.csv** (Already existed)

- **Rows**: 1
- **Years**: 2024
- **Estimate Types**: 1-year
- **Source Tables**: S1901 (Household/Family Income), S2001 (Earnings)
- **Key Metrics**:
  - Median household income
  - Median family income
  - Median earnings (total, male, female)
  - Gender earnings gap
  - Full-time worker earnings

**Note**: Need to collect 2019-2023 data for stronger model (see PERSONAL_INCOME_INTEGRATION_PLAN.md)

---

## 2. **broadband_cleaned.csv** ✅

- **Rows**: 7
- **Years**: 2019-2024
- **Estimate Types**: 1-year and 5-year
- **Source Tables**: B28008 (Computer and Internet Subscription), S2801 (Types of Internet)

### Key Metrics:

| Metric                      | Description                             |
| --------------------------- | --------------------------------------- |
| `total_households`          | Total households in Lonoke County       |
| `households_with_computer`  | Households with a computer              |
| `households_with_broadband` | Households with broadband internet      |
| `households_no_internet`    | Households without internet             |
| `broadband_access_pct`      | % of households with broadband (91-95%) |
| `no_internet_pct`           | % without internet (1.8-6.8%)           |
| `computer_ownership_pct`    | % with computer (93-97%)                |

### Sample Data (2023, 1-year):

- Total households: 75,721
- Broadband access: 95.48%
- No internet: 1.76%
- Computer ownership: 97.23%

---

## 3. **housing_cleaned.csv** ✅

- **Rows**: 7
- **Years**: 2019-2024
- **Estimate Types**: 1-year and 5-year
- **Source Tables**: B25002 (Occupancy Status), S2501 (Occupancy Characteristics)

### Key Metrics:

| Metric                  | Description                                 |
| ----------------------- | ------------------------------------------- |
| `total_housing_units`   | Total housing units in county               |
| `occupied_units`        | Occupied housing units                      |
| `vacant_units`          | Vacant housing units                        |
| `total_occupied`        | Total occupied (from S2501)                 |
| `occupancy_rate`        | % of units that are occupied (86-94%)       |
| `vacancy_pct`           | % of units that are vacant (5.8-13.5%)      |
| `owner_occupied_units`  | Owner-occupied units                        |
| `renter_occupied_units` | Renter-occupied units                       |
| `homeownership_rate`    | % of occupied units that are owner-occupied |
| `median_home_value`     | Median value of owner-occupied homes        |
| `median_gross_rent`     | Median monthly rent                         |

### Sample Data (2023, 1-year):

- Total housing units: 31,176
- Occupied: 29,388 (94.24%)
- Vacant: 1,788 (5.76%)

---

## 4. **labor_cleaned.csv** ✅

- **Rows**: 322
- **Years**: 1978-2023 (46 years!)
- **Source**: Business Dynamics Statistics (BDSTIMESERIES)

### Key Metrics:

| Metric                     | Description                            |
| -------------------------- | -------------------------------------- |
| `num_firms`                | Number of firms                        |
| `num_establishments`       | Number of establishments               |
| `num_employees`            | Number of employees                    |
| `establishments_born`      | New establishments (last 12 months)    |
| `establishments_exited`    | Closed establishments (last 12 months) |
| `jobs_created`             | Jobs created (expanding + opening)     |
| `jobs_destroyed`           | Jobs lost (contracting + closing)      |
| `net_jobs_created`         | Net job creation                       |
| `net_job_creation_rate`    | Net job creation rate (%)              |
| `employees_per_firm`       | Average employees per firm             |
| `net_establishment_change` | Net establishment births - deaths      |
| `job_churn`                | Total job creation + destruction       |

### Data Coverage:

- **Historical data**: 1978-2023 (comprehensive labor market dynamics)
- **Multiple industry breakdowns**: Available by NAICS code
- **Establishment age data**: Available from BDSEAGE file

---

## 5. **business_cleaned.csv** ✅

- **Rows**: 1
- **Years**: 2023
- **Source**: Annual Business Survey (ABS) - ABSNESD

### Key Metrics:

| Metric                     | Description                        | 2023 Value    |
| -------------------------- | ---------------------------------- | ------------- |
| `total_firms`              | Total employer + nonemployer firms | 6,791         |
| `employer_firms`           | Firms with employees               | 1,291 (19.0%) |
| `nonemployer_firms`        | Sole proprietors (no employees)    | 5,500 (81.0%) |
| `total_revenue_thousands`  | Total revenue ($1,000s)            | $3,707,643K   |
| `num_employees`            | Total employees                    | 14,045        |
| `annual_payroll_thousands` | Annual payroll ($1,000s)           | $528,858K     |
| `employer_firm_pct`        | % of firms with employees          | 19.01%        |
| `revenue_per_firm`         | Average revenue per firm ($1,000s) | $545.96K      |
| `revenue_per_employee`     | Revenue per employee ($1,000s)     | $263.98K      |
| `payroll_per_employee`     | Payroll per employee ($1,000s)     | $37.65K       |

### Insights:

- **81% of firms are nonemployers** (sole proprietors, gig workers)
- **Average firm employs ~11 people** (14,045 / 1,291 employers)
- **Average payroll: $37,650/employee/year**

---

## Data Quality Summary

### ✅ Complete Datasets

1. **labor_cleaned.csv**: 46 years (1978-2023), 322 observations
2. **broadband_cleaned.csv**: 6 years (2019-2024), dual estimates
3. **housing_cleaned.csv**: 6 years (2019-2024), dual estimates

### ⚠️ Limited Coverage

4. **business_cleaned.csv**: Only 2023 (need historical data)
5. **personal_income_parsed.csv**: Only 2024 (need 2019-2023)

---

## Next Steps for Model Enhancement

### Priority 1: Expand Personal Income Data

- Collect S1901 and S2001 for years 2019-2023
- Both 5-year and 1-year estimates
- See: `PERSONAL_INCOME_INTEGRATION_PLAN.md`
- **Impact**: 300-600% increase in training observations

### Priority 2: Collect Historical Business Data

- Find Annual Business Survey data for earlier years
- Ideally 2017-2023 to match other datasets
- **Impact**: Enable business trend analysis

### Priority 3: Data Integration

- Merge all cleaned datasets by year
- Create master dataset with all features
- Handle different estimate types (1-year vs 5-year)
- Calculate year-over-year trends

### Priority 4: Feature Engineering

- Broadband adoption rate trends
- Housing market cooling indicators (vacancy increases)
- Labor market dynamism (job churn, establishment turnover)
- Business concentration metrics
- Income inequality measures

---

## Usage Examples

### Load and explore broadband data:

```python
import pandas as pd

# Load broadband data
broadband = pd.read_csv('data_cleaned/broadband_cleaned.csv')

# Filter for 1-year estimates only
broadband_1y = broadband[broadband['estimate_type'] == '1-year']

# Calculate broadband growth
broadband_1y = broadband_1y.sort_values('year')
broadband_1y['broadband_growth'] = broadband_1y['broadband_access_pct'].pct_change() * 100
print(broadband_1y[['year', 'broadband_access_pct', 'broadband_growth']])
```

### Merge datasets by year:

```python
# Load all datasets
broadband = pd.read_csv('data_cleaned/broadband_cleaned.csv')
housing = pd.read_csv('data_cleaned/housing_cleaned.csv')
business = pd.read_csv('data_cleaned/business_cleaned.csv')

# Filter for 1-year estimates and merge
broadband_1y = broadband[broadband['estimate_type'] == '1-year']
housing_1y = housing[housing['estimate_type'] == '1-year']

# Merge on year
merged = pd.merge(broadband_1y, housing_1y, on=['year', 'county'],
                  suffixes=('_broadband', '_housing'))
merged = pd.merge(merged, business, on=['year', 'county'], how='left')

print(f"Merged dataset shape: {merged.shape}")
```

---

## File Locations

All cleaned datasets are in: `/Users/cyrilkups/Desktop/DataDrive Project/data_cleaned/`

```
data_cleaned/
├── personal_income_parsed.csv    (1 row, 2024 only)
├── broadband_cleaned.csv          (7 rows, 2019-2024)
├── housing_cleaned.csv            (7 rows, 2019-2024)
├── labor_cleaned.csv              (322 rows, 1978-2023)
└── business_cleaned.csv           (1 row, 2023 only)
```

---

## Scripts Used

Parsing scripts in project root:

- `clean_all_data.py` - Master cleaning script (run this!)
- `parse_personal_income.py` - Personal income parser
- `parse_broadband.py` / `parse_broadband_v2.py` - Broadband parsers
- `parse_housing.py` - Housing parser
- `parse_labor.py` - Labor market parser
- `parse_business.py` - Business dynamics parser

---

**Status**: ✅ **5 out of 5 cleaned datasets created!**

Run `python clean_all_data.py` to regenerate all cleaned datasets at any time.

# Personal Income Data Integration Plan (2019-2024)

## 📋 Current Status

### ✅ What You Have Now:

- **2024 Personal Income data** (1-year estimates only)
  - S1901: Household/Family Income
  - S2001: Earnings

### 🎯 What You Need:

Complete **multi-year dataset (2019-2024)** with both:

- **5-year estimates** (more stable, available for all areas)
- **1-year estimates** (more current, only for larger populations)

## 📊 Data Collection Checklist

### Step 1: Download Missing Data

Visit **https://data.census.gov/** and download these files:

#### S1901 - Household/Family Income (2019-2023)

```
Priority: HIGH (need both 5-year and 1-year if available)

□ ACSST5Y2019.S1901  (5-year estimate for 2019)
□ ACSST5Y2020.S1901  (5-year estimate for 2020)
□ ACSST5Y2021.S1901  (5-year estimate for 2021)
□ ACSST5Y2022.S1901  (5-year estimate for 2022)
□ ACSST5Y2023.S1901  (5-year estimate for 2023)

Optional (if Lonoke County qualifies):
□ ACSST1Y2019.S1901  (1-year estimate for 2019)
□ ACSST1Y2020.S1901  (1-year estimate for 2020)
□ ACSST1Y2021.S1901  (1-year estimate for 2021)
□ ACSST1Y2022.S1901  (1-year estimate for 2022)
□ ACSST1Y2023.S1901  (1-year estimate for 2023)
```

#### S2001 - Earnings (2019-2023)

```
Priority: HIGH (need both 5-year and 1-year if available)

□ ACSST5Y2019.S2001  (5-year estimate for 2019)
□ ACSST5Y2020.S2001  (5-year estimate for 2020)
□ ACSST5Y2021.S2001  (5-year estimate for 2021)
□ ACSST5Y2022.S2001  (5-year estimate for 2022)
□ ACSST5Y2023.S2001  (5-year estimate for 2023)

Optional (if Lonoke County qualifies):
□ ACSST1Y2019.S2001  (1-year estimate for 2019)
□ ACSST1Y2020.S2001  (1-year estimate for 2020)
□ ACSST1Y2021.S2001  (1-year estimate for 2021)
□ ACSST1Y2022.S2001  (1-year estimate for 2022)
□ ACSST1Y2023.S2001  (1-year estimate for 2023)
```

### Step 2: How to Download from Census Bureau

1. **Go to**: https://data.census.gov/
2. **Search**: Enter "S1901" or "S2001" in the search box
3. **Filter**:
   - Geography: Select "Lonoke County, Arkansas"
   - Years: Select one year at a time (2019, 2020, etc.)
   - Surveys: Choose "ACS 5-Year Estimates" or "ACS 1-Year Estimates"
4. **Download**: Click "Download" button and save as CSV
5. **Save to**: `Data Drive Datasets/Data That Back IGS (Problem)/Community Pillar/Personal Income/`

## 🔧 Processing the Data

### After Downloading All Files:

Run the parser to consolidate all years:

```bash
python parse_personal_income.py
```

This will:

1. ✓ Parse all CSV files (2019-2024)
2. ✓ Extract key income metrics
3. ✓ Merge S1901 and S2001 data
4. ✓ Calculate derived metrics (gender gap, ratios)
5. ✓ Save to: `data_cleaned/personal_income_parsed.csv`

## 📈 Why Multi-Year Data Makes Models Stronger

### Benefits:

1. **More Training Data**

   - Current: 1 year (2024 only) = ~20 observations
   - With 2019-2024: 6 years × 2 estimate types = ~60-120 observations
   - **300-600% increase in training data!**

2. **Temporal Patterns**

   - Capture income trends over time
   - COVID-19 impact (2020-2021)
   - Economic recovery patterns
   - Long-term growth trajectories

3. **Model Robustness**

   - Better generalization
   - Reduced overfitting
   - More reliable predictions
   - Cross-validation becomes meaningful

4. **Dual Estimates Validation**
   - 5-year: Smoother, more stable
   - 1-year: More responsive to recent changes
   - Compare both for data quality checks

## 🎯 Key Metrics to Extract

From the parsed data, you'll get:

### From S1901 (Household Income):

- `median_household_income` - Core income metric
- `mean_household_income` - Average (affected by outliers)
- `median_family_income` - Family-specific income

### From S2001 (Earnings):

- `median_earnings` - Individual earnings
- `median_earnings_male` - Male workers
- `median_earnings_female` - Female workers
- `median_earnings_fulltime` - Full-time workers

### Derived Metrics:

- `gender_earnings_gap_pct` - Male-female earnings disparity
- `household_to_earnings_ratio` - Household vs individual income

## 🔄 Next Steps After Collection

1. **Download the missing files** (see checklist above)
2. **Run parser**: `python parse_personal_income.py`
3. **Verify output**: Check `data_cleaned/personal_income_parsed.csv`
4. **Integrate with IGS data**: Merge with existing cleaned dataset
5. **Retrain models** with enhanced feature set

## 💡 Integration with Existing Models

Once you have the parsed data, you can:

1. **Add as new features** to `clean_igs_data.py`
2. **Include in model training** (`train_ml_model.py`)
3. **Test interventions** with income-based scenarios (`simulate_intervention.py`)

### Example New Features:

- Income growth rates (year-over-year)
- Gender income gap trends
- Education-earnings relationships
- Full-time vs part-time earnings ratios

## 📞 Need Help?

If you encounter issues:

- Check file naming follows: `ACSST[5Y|1Y][YEAR].S[1901|2001]-*.csv`
- Ensure files are in the Personal Income folder
- Run `python DATA_COLLECTION_GUIDE.py` for detailed instructions
- Check the parser output for errors

---

**Ready to start?** Begin with downloading the 5-year estimates for 2019-2023 (S1901 and S2001).
These are guaranteed to be available for all counties!

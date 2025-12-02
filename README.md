# IGS (Inclusive Growth Score) ML Model Project

## Overview

This project builds machine learning models to predict Inclusive Growth Scores (IGS) for census tracts in Arkansas. It includes comprehensive data cleaning pipelines, ML model training, policy simulations, and visualizations.

---

## Recent Updates (Dec 2025)

### Augmented Model Development ⭐

- **BREAKTHROUGH:** Integrated solution county data (Beltrami MN, Chaffee CO, Fulton GA)
- **Training Data:** Expanded from 26 samples (1 county) to 38 samples (4 counties)
- **Model Performance:**
  - IGS: R² = 0.73 (vs 0.55 original, **+32% improvement**)
  - Economy: R² = 0.44 (vs 0.05 original, **+780% improvement**)
  - Place: R² = 0.57, Community: R² = 0.05
- **Evidence-Based Predictions:** Backed by counties that achieved real improvements:
  - Chaffee County: IGS 37 → 42 (+13.5%, 2020-2021)
  - Fulton County: IGS 37 → 42 (+13.5%, 2020-2021)
  - Beltrami County: Employment +231% (2020-2023)

### 2030 Forecast & Intervention Scenarios

- **Baseline (2024):** 27.0 IGS (distressed status)
- **Without Intervention:** Declines to 25.2 by 2030
- **With Combined Intervention Package:** Reaches 45.7 by 2030
  - **CROSSES distressed threshold (45)** for first time
  - Housing affordability (-10% burden): +16.1 points
  - Early education (+12% enrollment): +18.8 points
  - Business support (+15% minority businesses): +17.1 points
  - **Combined synergy:** +20.5 points total

### Presentation Materials (Slide 5)

- **4 Visualizations Created:**
  - Immediate intervention impacts (bar chart)
  - Multi-pillar predictions (2×2 breakdown)
  - 6-year forecast to 2030 (threshold crossing highlighted)
  - 4-year forecast to 2027 (short-term view)
- **Evidence Documentation:** Full analysis with compounding effects and policy implications

### Key Findings

- **Lonoke County Trends (2019-2024):**
  - IGS declined from 40 to 27 (-32.5%)
  - Median income: 36.9% → -15.6% (severe decline)
  - Broadband access: 44.1% → 58.7% (improving but insufficient)
  - Early education: 50% → 33.4% (declining)
- **Threshold Crossing Achievement:** Combined intervention reaches 45.7 by 2030 (0.7 above distressed threshold)
- **Next Goal:** Improving threshold (55) requires additional 9.3 points by 2035

---

## Project Structure

```
DataDrive Project/
│
├── README.md                       # This file - main project overview
├── CLEANUP_SUMMARY.md              # Directory cleanup documentation
│
├── data_cleaned/                   # Cleaned datasets ready for analysis
│   ├── igs_trends_features.csv     # Tract-level IGS features (26 rows, 6 tracts)
│   ├── tract_20800_cleaned.csv     # Lonoke County tract data
│   ├── broadband_cleaned.csv       # County-level broadband (2019-2024)
│   ├── housing_cleaned.csv         # County-level housing (2019-2024)
│   ├── labor_cleaned.csv           # County-level labor market (1978-2023)
│   ├── business_cleaned.csv        # County-level business (2023)
│   └── personal_income_cleaned.csv # County-level income (2024)
│
├── igs_plus_more_data/             # ⭐ AUGMENTED MODELS (Best Performance)
│   ├── train_augmented_model.py    # Current model training script
│   ├── integrate_solutions_data.py # Data integration script
│   ├── integrated_igs_county_data.csv # 38 samples from 4 counties
│   ├── integrated_county_solutions.csv # Solution county data
│   ├── AUGMENTED_MODEL_SUMMARY.md  # Comprehensive documentation
│   └── models_augmented/           # Trained models (R²=0.73)
│       ├── *_model.joblib          # Random Forest models (4)
│       ├── *_scaler.joblib         # Feature scalers (4)
│       ├── *_feature_importance.csv # Feature rankings (4)
│       ├── lonoke_intervention_predictions.csv # ⭐ Intervention scenarios
│       ├── model_comparison_summary.csv
│       └── training_report.txt
│
├── igs_ml/                         # Original tract-level ML models
│   ├── README.md                   # ML models overview
│   ├── data/
│   │   └── igs_trends_features.csv # Main dataset (26 rows)
│   ├── src/                        # Source code
│   │   ├── data_processing/        # Data cleaning scripts
│   │   ├── modeling/               # ML training & prediction
│   │   ├── visualization/          # Chart generation
│   │   └── analysis/               # Analysis & simulation tools
│   ├── output/
│   │   ├── models/                 # Original trained models
│   │   ├── figures/                # Global visualizations
│   │   └── Important Findings/     # Core findings (01-04, 08 only)
│   ├── Slide_4_Benchmark/          # Benchmark analysis
│   ├── Slide_5_Predicted_Outcomes/ # ⭐ CURRENT PRESENTATION
│   │   ├── igs_predicted_outcomes.png # Immediate gains bar chart
│   │   ├── multi_pillar_predictions.png # 2×2 pillar breakdown
│   │   ├── igs_predicted_outcomes_to_2030.png # 6-year forecast
│   │   ├── multi_year_igs_forecast.png # 4-year forecast
│   │   ├── predicted_outcomes_summary.txt
│   │   └── extended_forecast_2030_insights.txt
│   └── Slide_6_Key_Findings/       # Key findings summary
│
├── scripts/                        # Data processing scripts
│   ├── data_cleaning/              # Parse raw Census/ACS data
│   └── data_verification/          # Data quality checks
│
├── documentation/                  # Project documentation
│   ├── CLEANED_DATASETS_SUMMARY.md
│   ├── DATA_COLLECTION_GUIDE.md
│   └── PERSONAL_INCOME_INTEGRATION_PLAN.md
│
├── nextjs-dashboard/               # Web dashboard (separate app)
│
└── Data Drive Datasets/            # Raw source data
```

---

## ML Model Performance

**Best Model:** Augmented (Solution Counties Integrated)  
**Location:** `igs_plus_more_data/models_augmented/`  
**Dataset:** 38 samples (4 counties: Lonoke AR, Beltrami MN, Chaffee CO, Fulton GA)

| Model               | Train R² | Test R² | Improvement vs Original | Key Features                       |
| ------------------- | -------- | ------- | ----------------------- | ---------------------------------- |
| **IGS Score**       | 0.92     | 0.73    | +32% (0.55 → 0.73)      | housing_cost_burden, median_income |
| **Place Score**     | 0.86     | 0.57    | -14% (0.66 → 0.57)      | early_ed_growth, housing_burden    |
| **Economy Score**   | 0.86     | 0.44    | +780% (0.05 → 0.44)     | median_income, minority_businesses |
| **Community Score** | 0.79     | 0.05    | -79% (0.24 → 0.05)      | income_growth, broadband_access    |

**Original Model Performance** (for comparison):  
**Location:** `igs_ml/output/models/`  
**Dataset:** 26 samples (1 county: Lonoke AR only)

---

## 2030 Intervention Scenarios

**Source:** Augmented model predictions  
**File:** `igs_plus_more_data/models_augmented/lonoke_intervention_predictions.csv`

**Baseline (2024):** 27.0 IGS → **25.2 by 2030** (without intervention)

| Intervention                           | 2024 Immediate | 2030 Projected | Gain from Baseline |
| -------------------------------------- | -------------- | -------------- | ------------------ |
| Housing Affordability (-10% burden)    | 37.3 (+10.3)   | 41.3           | +16.1              |
| Early Education (+12% enrollment)      | 37.3 (+10.3)   | 44.0           | +18.8 (highest)    |
| Business Support (+15% minority firms) | 37.5 (+10.5)   | 42.3           | +17.1              |
| **Combined Package (All Three)**       | **37.5**       | **45.7**       | **+20.5**          |
| **Threshold Crossing Status**          |                | **✓ CROSSES**  | **0.7 above (45)** |

**Evidence Base:**

- Chaffee County, CO: IGS improved 37 → 42 in 1 year (2020-2021)
- Fulton County, GA: IGS improved 37 → 42 in 1 year (2020-2021)
- Beltrami County, MN: Employment grew +231% (2020-2023, 10,735 jobs, $492M payroll)

---

## Available Scripts & Tools

### Augmented Model (Current Best)

```bash
cd igs_plus_more_data

# Train augmented models with solution county data
python train_augmented_model.py

# Integrate solution county data
python integrate_solutions_data.py
```

### Data Cleaning

```bash
cd scripts/data_cleaning

# Master cleaning script for all datasets
python clean_all_data.py

# Extract tract 20800 from official IGS export
python clean_tract_20800_from_export.py
```

### ML Training & Prediction (Original Models)

```bash
cd igs_ml/src/modeling

# Train original Random Forest models
python train_ml_model.py

# Make predictions
python predict_scores.py
```

### Analysis & Simulation

```bash
cd igs_ml/src/analysis

# Policy intervention simulation
python simulate_intervention.py

# Detailed tract 20800 analysis
python analyze_tract_20800.py
```

### Visualization

```bash
cd igs_ml/src/visualization

# Generate all visualizations
python visualize_results.py
python visualize_tract_20800.py

# Specific charts
python plot_feature_importance.py
python plot_correlation_heatmap.py
python plot_scatter_plots.py
python plot_indicator_trends_20800.py
```

---

## Key Findings (Lonoke County Tract 20800)

### Score Trends (2019–2024)

- **IGS Score:** 40 → 27 (-32.5% decline)
- **Place Score:** 34 → 21 (-38.2% decline)
- **Economy Score:** 30 → 20 (-33.3% decline)
- **Community Score:** 54 → 40 (-25.9% decline)

### Indicator Trends

- **Median Income:** 36.9% → -15.6% (severe 52.5 point decline)
- **Broadband Access:** 44.1% → 58.7% (+14.6pp improvement, but still 28.6pp below U.S.)
- **Minority Businesses:** -40% → 8.3% (recovery from negative)
- **Housing Cost Burden:** 91% → 86.5% (slight improvement, still extreme)
- **Early Education:** 50% → 33.4% (-16.6pp decline)

### Crisis Period

- **2020–2021:** Sharpest declines across all scores
- **2021:** Lowest IGS score recorded (21 points)
- **2024:** Remains in distressed status (27, threshold is 45)

### 2030 Projections (Evidence-Based)

**Without Intervention:**

- IGS continues declining to 25.2 (-1.8 from 2024)
- Remains severely distressed

**With Combined Intervention Package:**

- IGS improves to 45.7 (+18.7 from 2024)
- **CROSSES distressed threshold (45) by 0.7 points**
- Pathway to improving status (55) visible by 2035
- Evidence: Based on actual improvements in Chaffee, Fulton, and Beltrami counties

---

## Usage

### Training Augmented Models (Recommended)

```bash
cd igs_plus_more_data
python train_augmented_model.py
```

**Output:** 4 models saved to `models_augmented/` with R²=0.73 for IGS

### Generating Presentation Materials

```bash
# View Slide 5 predictions (already generated)
open igs_ml/Slide_5_Predicted_Outcomes/igs_predicted_outcomes_to_2030.png
open igs_ml/Slide_5_Predicted_Outcomes/multi_pillar_predictions.png

# Read analysis
cat igs_ml/Slide_5_Predicted_Outcomes/extended_forecast_2030_insights.txt
```

### Running Policy Simulations (Original)

```bash
cd igs_ml/src/analysis
python simulate_intervention.py
```

### Generating Visualizations

```bash
cd igs_ml/src/visualization

# All visualizations
python visualize_results.py
python visualize_tract_20800.py

# Specific charts
python plot_feature_importance.py
python plot_correlation_heatmap.py
python plot_scatter_plots.py
python plot_indicator_trends_20800.py
```

### Analysis

```bash
cd igs_ml/src/analysis
python analyze_tract_20800.py  # Detailed statistical analysis
```

---

## Next Steps

### Immediate Actions

- **Present Slide 5 Materials:** Use visualizations in `igs_ml/Slide_5_Predicted_Outcomes/`
- **Policy Planning:** Review intervention scenarios and select priorities
- **Stakeholder Engagement:** Share evidence-based projections with decision makers

### Model Improvements

- **Expand Training Data:** Add more solution counties that improved IGS
- **Refine Interventions:** Test specific policy combinations and timelines
- **Temporal Validation:** Monitor actual 2025-2026 outcomes vs predictions

### Data Collection

- **Update 2025 Data:** Incorporate latest IGS scores when available
- **Solution County Tracking:** Monitor Chaffee, Fulton, Beltrami progress
- **Intervention Monitoring:** Track actual policy implementations

### Dashboard Development

- **Interactive Tool:** Build web dashboard for real-time scenario testing
- **Stakeholder Portal:** Enable policymakers to explore interventions
- **Progress Tracking:** Visualize actual vs predicted outcomes over time

---

## Documentation

- **Augmented Model:** `igs_plus_more_data/AUGMENTED_MODEL_SUMMARY.md`
- **Cleanup Log:** `CLEANUP_SUMMARY.md`
- **Data Dictionary:** `documentation/CLEANED_DATASETS_SUMMARY.md`
- **Data Sources:** `documentation/DATA_COLLECTION_GUIDE.md`
- **Presentation Materials:** `igs_ml/Slide_5_Predicted_Outcomes/`

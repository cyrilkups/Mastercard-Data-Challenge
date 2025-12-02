# IGS ML - Tract-Level Prediction Models

This directory contains ML models for predicting Inclusive Growth Scores (IGS) at the census tract level.

**⭐ CURRENT BEST MODELS:** See `../igs_plus_more_data/models_augmented/` for improved models trained on solution county data (R²=0.73 vs 0.55)

**This directory contains:**

- Original baseline models (26 samples, Lonoke County only)
- Presentation materials (Slide 4, 5, 6)
- Analysis visualizations and source code

## 📁 Directory Structure

```
igs_ml/
├── README.md                       # This file
├── data/                           # Input data
│   └── igs_trends_features.csv     # Main dataset (26 rows, 6 tracts × 2019-2024)
├── src/                            # Source code
│   ├── data_processing/            # Data cleaning scripts
│   │   ├── clean_igs_data.py
│   │   └── clean_tract_20800_from_export.py
│   ├── modeling/                   # ML training & prediction
│   │   ├── train_ml_model.py
│   │   └── predict_scores.py
│   ├── visualization/              # Chart generation
│   │   ├── plot_feature_importance.py
│   │   ├── plot_correlation_heatmap.py
│   │   ├── plot_scatter_plots.py
│   │   ├── plot_indicator_trends_20800.py
│   │   ├── visualize_results.py
│   │   └── visualize_tract_20800.py
│   └── analysis/                   # Analysis & simulation tools
│       ├── analyze_tract_20800.py
│       ├── simulate_policy_intervention.py
│       └── simulate_intervention.py
└── output/                         # All generated outputs
    ├── models/                     # Trained models & artifacts
    ├── figures/                    # Global visualizations
    └── figures_tract_20800/        # Tract 20800 focused charts
```

## 🚀 Quick Start

### 1. Train ML Models

```bash
python src/modeling/train_ml_model.py
```

Trains 4 Random Forest models (Place, Economy, Community, IGS scores) and saves to `output/models/`

### 2. Generate Visualizations

**Global Analysis:**

```bash
python src/visualization/visualize_results.py
```

Creates feature importance, correlation heatmap, scatter plots → `output/figures/`

**Tract 20800 Focus:**

```bash
python src/visualization/visualize_tract_20800.py
```

Creates 6 charts showing tract 20800 trends → `output/figures_tract_20800/`

**Individual Indicator Trends:**

```bash
python src/visualization/plot_indicator_trends_20800.py
```

Creates 5 individual indicator trend charts → `output/figures_tract_20800/indicator_trends/`

### 3. Run Policy Simulation

```bash
python src/analysis/simulate_policy_intervention.py
```

Tests intervention scenarios and generates comparison charts → `output/figures_tract_20800/`

## 📊 Models

### Augmented Models (⭐ Recommended)

**Location:** `../igs_plus_more_data/models_augmented/`
**Training Data:** 38 samples (4 counties: Lonoke AR, Beltrami MN, Chaffee CO, Fulton GA)

| Model               | Test R² | Improvement | Key Features                       |
| ------------------- | ------- | ----------- | ---------------------------------- |
| **igs_score**       | 0.73    | +32%        | All 18 features (inc. lagged)      |
| **place_score**     | 0.57    | -14%        | Housing burden, broadband access   |
| **economy_score**   | 0.44    | +780%       | Median income, minority businesses |
| **community_score** | 0.05    | -79%        | Early education, median income     |

**Key File:** `lonoke_intervention_predictions.csv` - Contains all intervention scenarios

### Original Models (Baseline)

**Location:** `output/models/`
**Training Data:** 26 samples (1 county: Lonoke AR only)

| Model               | Test R² | Key Features                       |
| ------------------- | ------- | ---------------------------------- |
| **place_score**     | 0.66    | Housing burden, broadband access   |
| **igs_score**       | 0.55    | Housing burden, median income      |
| **community_score** | 0.24    | Income growth, broadband access    |
| **economy_score**   | 0.05    | Median income, minority businesses |

## 📈 Dataset

- **Source:** Official IGS export CSV (Inclusive_Growth_Score_Data_Export_21-11-2025_035947)
- **Rows:** 26 (6 tracts × 2019–2024, except 2024 limited to 2 tracts)
- **Features (10):** median_income, broadband_access, minority_businesses, housing_burden, early_education + 5 trend features
- **Targets (4):** place_score, economy_score, community_score, igs_score

## 🎯 Key Features

- **4 Random Forest Models:** Trained with 100 estimators, max depth 10
- **10 Features:** Level indicators + year-over-year trend features
- **Policy Simulation:** Test intervention scenarios with projected impact
- **Comprehensive Visualizations:** 20+ charts including:
  - Feature importance (4 models)
  - Correlation heatmap (16×16)
  - Scatter plots (3)
  - Tract 20800 trends (6 main + 5 individual indicators)
  - Policy intervention comparisons (2)

## 📋 Usage Examples

### Data Processing

```bash
# Clean main dataset
python src/data_processing/clean_igs_data.py

# Extract tract 20800 from official export
python src/data_processing/clean_tract_20800_from_export.py
```

### Making Predictions

```bash
python src/modeling/predict_scores.py
```

### Analysis

```bash
# Statistical analysis of tract 20800
python src/analysis/analyze_tract_20800.py
```

## 📌 Key Findings

### Lonoke County Tract 20800 (2019-2024)

- **IGS decline:** 40 → 27 (-32.5%)
- **Drivers of decline:**
  - Median income: 36.9% → -15.6% (52.5 point drop)
  - Broadband access: 44.1% → 58.7% (improving but 28.6pp below U.S.)
  - Minority businesses: -40% → 8.3% (recovering)
  - Early education: 50% → 33.4% (-16.6pp decline)
  - Housing burden: 91% → 86.5% (slight improvement, still extreme)

### 2030 Projections (Augmented Model)

**Baseline (no intervention):** 25.2 (-1.8 from 2024)

**With Intervention Package:**

- Housing affordability: 41.3 (+16.1 from baseline)
- Early education: 44.0 (+18.8 from baseline, highest single)
- Business support: 42.3 (+17.1 from baseline)
- **Combined: 45.7 (+20.5 from baseline)** ✓ CROSSES THRESHOLD (45)

**Evidence:**

- Chaffee County, CO: IGS 37 → 42 (+13.5%, 2020-2021)
- Fulton County, GA: IGS 37 → 42 (+13.5%, 2020-2021)
- Beltrami County, MN: Employment +231% (2020-2023)

## 🔗 Documentation

- **Main Project Overview:** `/Users/cyrilkups/Desktop/DataDrive Project/README.md`
- **Augmented Model Details:** `../igs_plus_more_data/AUGMENTED_MODEL_SUMMARY.md`
- **Presentation Materials:** `Slide_5_Predicted_Outcomes/` (current, evidence-based)
- **Cleanup Log:** `../CLEANUP_SUMMARY.md`

## 🛠️ Technical Stack

- Python 3.13.5
- pandas, numpy, scikit-learn, joblib
- matplotlib, seaborn
- Random Forest Regressor (n_estimators=100, max_depth=10)

# DataDrive Project - Directory Structure

## Root Level
```
DataDrive Project/
├── README.md                           # Main project overview
├── .venv/                              # Python virtual environment
├── data_cleaned/                       # All cleaned datasets
├── scripts/                            # Data processing scripts
├── documentation/                      # Project documentation
├── igs_ml/                             # Tract-level ML models (RECOMMENDED)
├── igs_plus_more_data/                 # Combined tract+county ML (EXPERIMENTAL)
└── Data Drive Datasets/                # Raw source data
```

## Detailed Structure

### data_cleaned/
```
data_cleaned/
├── broadband_cleaned.csv               # County broadband (2019-2024)
├── housing_cleaned.csv                 # County housing (2019-2024)
├── labor_cleaned.csv                   # County labor market (1978-2023)
├── business_cleaned.csv                # County business (2023)
├── personal_income_cleaned.csv         # County income (2024)
└── igs_trends_features.csv             # Tract-level IGS features
```

### scripts/
```
scripts/
├── data_cleaning/
│   ├── clean_all_data.py               # Master cleaning script
│   ├── parse_broadband.py              # Parse ACS B28008/S2801
│   ├── parse_broadband_v2.py           # Improved broadband parser
│   ├── parse_housing.py                # Parse ACS B25002/S2501
│   ├── parse_labor.py                  # Parse BDS time series
│   ├── parse_business.py               # Parse ABS NESD
│   └── parse_personal_income.py        # Parse income data
└── data_verification/
    └── verify_cleaned_data.py          # Validate cleaned data
```

### documentation/
```
documentation/
├── CLEANED_DATASETS_SUMMARY.md         # Data dictionary & sources
├── PERSONAL_INCOME_INTEGRATION_PLAN.md # Income data collection plan
└── DATA_COLLECTION_GUIDE.md            # Guide to data sources
```

### igs_ml/ ⭐ RECOMMENDED
```
igs_ml/
├── README.md                           # Model documentation
├── clean_igs_data.py                   # Feature engineering
├── train_ml_model.py                   # Train 4 RF models
├── predict_scores.py                   # Make predictions
├── simulate_intervention.py            # Policy simulations
├── igs_trends_features.csv             # Training data (20 obs)
└── models/
    ├── place_score_model.joblib
    ├── place_score_scaler.joblib
    ├── place_score_feature_importance.csv
    ├── economy_score_model.joblib
    ├── economy_score_scaler.joblib
    ├── economy_score_feature_importance.csv
    ├── community_score_model.joblib
    ├── community_score_scaler.joblib
    ├── community_score_feature_importance.csv
    ├── igs_score_model.joblib
    ├── igs_score_scaler.joblib
    ├── igs_score_feature_importance.csv
    ├── model_comparison_summary.csv
    ├── training_report.txt
    └── intervention_comparison.csv
```

### igs_plus_more_data/ (EXPERIMENTAL)
```
igs_plus_more_data/
├── README.md                           # Combined model docs
├── integrate_data.py                   # Merge county + tract data
├── train_combined_model.py             # Train enriched models
├── integrated_igs_county_data.csv      # Combined dataset (20×38)
└── models_combined/
    ├── place_score_model.joblib
    ├── place_score_scaler.joblib
    ├── place_score_feature_importance.csv
    ├── economy_score_model.joblib
    ├── economy_score_scaler.joblib
    ├── economy_score_feature_importance.csv
    ├── community_score_model.joblib
    ├── community_score_scaler.joblib
    ├── community_score_feature_importance.csv
    ├── igs_score_model.joblib
    ├── igs_score_scaler.joblib
    ├── igs_score_feature_importance.csv
    ├── model_comparison_summary.csv
    └── training_report.txt
```

### Data Drive Datasets/ (Raw source data)
```
Data Drive Datasets/
├── Data That Back IGS (Problem)/
│   ├── Community Pillar/
│   ├── Economic Pillar Data/
│   └── Place Pillar Data/
├── Data That Back Why (Causes)/
│   ├── Community Pillar/
│   ├── Economic Pillar/
│   └── Place Pillar/
├── Data That Back Solution/
│   ├── Community Pillar/
│   ├── Economic Pillar/
│   └── Place Pillar/
└── Federal Financial Institutions Examination Council/
```

## Key Files by Purpose

### Data Cleaning
- **Master script:** `scripts/data_cleaning/clean_all_data.py`
- **Verification:** `scripts/data_verification/verify_cleaned_data.py`

### Machine Learning (Recommended)
- **Train:** `igs_ml/train_ml_model.py`
- **Predict:** `igs_ml/predict_scores.py`
- **Simulate:** `igs_ml/simulate_intervention.py`

### Documentation
- **Project overview:** `README.md`
- **Data dictionary:** `documentation/CLEANED_DATASETS_SUMMARY.md`
- **Model details:** `igs_ml/README.md`

## Changes from Original Structure

### Removed
- ❌ Duplicate files in root (train_ml_model.py, predict_scores.py, etc.)
- ❌ Duplicate `models/` directory in root
- ❌ Empty `ml_models/` directory
- ❌ Scattered parser scripts in root

### Added
- ✅ `scripts/` folder with organized subfolders
- ✅ `documentation/` folder for all docs
- ✅ Cleaner root directory (only README + folders)

### Preserved
- ✅ All cleaned datasets in `data_cleaned/`
- ✅ Both ML approaches in separate folders
- ✅ All trained models and artifacts
- ✅ All raw source data

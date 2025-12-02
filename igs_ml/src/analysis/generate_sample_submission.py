"""
Generate Sample_submission.csv
================================
Creates a combined submission file with predictions for both training and test sets.

Output format:
tract,year,set_type,igs_score_actual,igs_score_predicted,place_score_predicted,economy_score_predicted,community_score_predicted

Where:
- set_type: 'train' or 'test'
- Training set: 2020-2023 data (used for model training)
- Test set: 2019 and 2024 data (held-out for testing)
"""

from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import pandas as pd
import numpy as np
import joblib
from pathlib import Path

# ============================================================================
# CONFIGURATION
# ============================================================================

BASE_DIR = Path(__file__).resolve().parents[2]
PROJECT_ROOT = BASE_DIR.parent
OUTPUT_DIR = BASE_DIR / 'output'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("="*80)
print("GENERATING SAMPLE SUBMISSION FILE")
print("="*80)

# ============================================================================
# LOAD DATA AND MODELS
# ============================================================================

print("\n[1/4] Loading data and models...")

# Load data
data_path = BASE_DIR / 'data' / 'igs_trends_features.csv'
df = pd.read_csv(data_path)

# Load models and scalers
models_dir = BASE_DIR / 'output' / 'models'
igs_model = joblib.load(models_dir / 'igs_score_model.joblib')
igs_scaler = joblib.load(models_dir / 'igs_score_scaler.joblib')

place_model = joblib.load(models_dir / 'place_score_model.joblib')
place_scaler = joblib.load(models_dir / 'place_score_scaler.joblib')

economy_model = joblib.load(models_dir / 'economy_score_model.joblib')
economy_scaler = joblib.load(models_dir / 'economy_score_scaler.joblib')

community_model = joblib.load(models_dir / 'community_score_model.joblib')
community_scaler = joblib.load(models_dir / 'community_score_scaler.joblib')

print(f"   ✓ Loaded {len(df)} rows of data")
print(f"   ✓ Loaded 4 models (IGS, Place, Economy, Community)")

# ============================================================================
# PREPARE FEATURES
# ============================================================================

print("\n[2/4] Preparing features...")

# Feature columns for each model
feature_cols = [
    'median_income', 'broadband_access_pct', 'minority_owned_businesses_pct',
    'housing_cost_burden_pct', 'early_education_enrollment_pct',
    'income_growth', 'broadband_growth', 'minority_business_growth',
    'housing_burden_change', 'early_ed_growth'
]

# Extract features
X = df[feature_cols].values

# Target columns
y_igs = df['igs_score'].values
y_place = df['place_score'].values
y_economy = df['economy_score'].values
y_community = df['community_score'].values

print(f"   ✓ Using {len(feature_cols)} features")

# ============================================================================
# SPLIT TRAIN/TEST SETS
# ============================================================================

print("\n[3/4] Splitting train/test sets...")

# Define train/test split
# Training: 2020-2023 (most data)
# Test: 2019 and 2024 (held-out years)
train_mask = df['year'].isin([2020, 2021, 2022, 2023])
test_mask = df['year'].isin([2019, 2024])

X_train = X[train_mask]
X_test = X[test_mask]

train_indices = df[train_mask].index
test_indices = df[test_mask].index

print(f"   ✓ Training set: {len(X_train)} rows (years 2020-2023)")
print(f"   ✓ Test set: {len(X_test)} rows (years 2019, 2024)")

# ============================================================================
# GENERATE PREDICTIONS
# ============================================================================

print("\n[4/4] Generating predictions...")

# Scale features
X_train_scaled = igs_scaler.transform(X_train)
X_test_scaled = igs_scaler.transform(X_test)

X_train_scaled_place = place_scaler.transform(X_train)
X_test_scaled_place = place_scaler.transform(X_test)

X_train_scaled_economy = economy_scaler.transform(X_train)
X_test_scaled_economy = economy_scaler.transform(X_test)

X_train_scaled_community = community_scaler.transform(X_train)
X_test_scaled_community = community_scaler.transform(X_test)

# Generate predictions for training set
igs_pred_train = igs_model.predict(X_train_scaled)
place_pred_train = place_model.predict(X_train_scaled_place)
economy_pred_train = economy_model.predict(X_train_scaled_economy)
community_pred_train = community_model.predict(X_train_scaled_community)

# Generate predictions for test set
igs_pred_test = igs_model.predict(X_test_scaled)
place_pred_test = place_model.predict(X_test_scaled_place)
economy_pred_test = economy_model.predict(X_test_scaled_economy)
community_pred_test = community_model.predict(X_test_scaled_community)

print(f"   ✓ Generated predictions for all sets")

# ============================================================================
# CREATE SUBMISSION DATAFRAME
# ============================================================================

print("\n[5/5] Creating submission file...")

# Training set dataframe
train_df = pd.DataFrame({
    'tract': df.loc[train_indices, 'tract'].values,
    'year': df.loc[train_indices, 'year'].values,
    'set_type': 'train',
    'igs_score_actual': y_igs[train_mask],
    'igs_score_predicted': igs_pred_train,
    'place_score_actual': y_place[train_mask],
    'place_score_predicted': place_pred_train,
    'economy_score_actual': y_economy[train_mask],
    'economy_score_predicted': economy_pred_train,
    'community_score_actual': y_community[train_mask],
    'community_score_predicted': community_pred_train,
    'igs_residual': y_igs[train_mask] - igs_pred_train,
    'place_residual': y_place[train_mask] - place_pred_train,
    'economy_residual': y_economy[train_mask] - economy_pred_train,
    'community_residual': y_community[train_mask] - community_pred_train
})

# Test set dataframe
test_df = pd.DataFrame({
    'tract': df.loc[test_indices, 'tract'].values,
    'year': df.loc[test_indices, 'year'].values,
    'set_type': 'test',
    'igs_score_actual': y_igs[test_mask],
    'igs_score_predicted': igs_pred_test,
    'place_score_actual': y_place[test_mask],
    'place_score_predicted': place_pred_test,
    'economy_score_actual': y_economy[test_mask],
    'economy_score_predicted': economy_pred_test,
    'community_score_actual': y_community[test_mask],
    'community_score_predicted': community_pred_test,
    'igs_residual': y_igs[test_mask] - igs_pred_test,
    'place_residual': y_place[test_mask] - place_pred_test,
    'economy_residual': y_economy[test_mask] - economy_pred_test,
    'community_residual': y_community[test_mask] - community_pred_test
})

# Combine train and test
submission_df = pd.concat([train_df, test_df], ignore_index=True)

# Sort by tract and year
submission_df = submission_df.sort_values(
    ['tract', 'year']).reset_index(drop=True)

# Round predictions to 2 decimal places
pred_cols = [
    col for col in submission_df.columns if 'predicted' in col or 'residual' in col]
for col in pred_cols:
    submission_df[col] = submission_df[col].round(2)

# ============================================================================
# SAVE SUBMISSION FILE
# ============================================================================

output_path = OUTPUT_DIR / 'Sample_submission.csv'
submission_df.to_csv(output_path, index=False)

print(f"   ✓ Saved: {output_path}")

# ============================================================================
# GENERATE SUMMARY STATISTICS
# ============================================================================

print("\n" + "="*80)
print("SUBMISSION FILE SUMMARY")
print("="*80)

print("\nData Distribution:")
print(f"  Total rows: {len(submission_df)}")
print(
    f"  Training rows: {len(train_df)} ({len(train_df)/len(submission_df)*100:.1f}%)")
print(
    f"  Test rows: {len(test_df)} ({len(test_df)/len(submission_df)*100:.1f}%)")

print("\nYear Distribution:")
year_counts = submission_df.groupby(['year', 'set_type']).size()
for (year, set_type), count in year_counts.items():
    print(f"  {year} ({set_type}): {count} rows")

print("\nTract Coverage:")
tract_counts = submission_df['tract'].value_counts().sort_index()
for tract, count in tract_counts.items():
    print(f"  Tract {tract}: {count} rows")

print("\n" + "-"*80)
print("PREDICTION ACCURACY (TRAINING SET)")
print("-"*80)

# Calculate metrics for training set

train_metrics = train_df.copy()

igs_rmse_train = np.sqrt(mean_squared_error(train_metrics['igs_score_actual'],
                                            train_metrics['igs_score_predicted']))
igs_mae_train = mean_absolute_error(train_metrics['igs_score_actual'],
                                    train_metrics['igs_score_predicted'])
igs_r2_train = r2_score(train_metrics['igs_score_actual'],
                        train_metrics['igs_score_predicted'])

print(f"\nIGS Score:")
print(f"  RMSE: {igs_rmse_train:.2f}")
print(f"  MAE: {igs_mae_train:.2f}")
print(f"  R²: {igs_r2_train:.3f}")

place_rmse_train = np.sqrt(mean_squared_error(train_metrics['place_score_actual'],
                                              train_metrics['place_score_predicted']))
place_r2_train = r2_score(train_metrics['place_score_actual'],
                          train_metrics['place_score_predicted'])

print(f"\nPlace Score:")
print(f"  RMSE: {place_rmse_train:.2f}")
print(f"  R²: {place_r2_train:.3f}")

economy_rmse_train = np.sqrt(mean_squared_error(train_metrics['economy_score_actual'],
                                                train_metrics['economy_score_predicted']))
economy_r2_train = r2_score(train_metrics['economy_score_actual'],
                            train_metrics['economy_score_predicted'])

print(f"\nEconomy Score:")
print(f"  RMSE: {economy_rmse_train:.2f}")
print(f"  R²: {economy_r2_train:.3f}")

community_rmse_train = np.sqrt(mean_squared_error(train_metrics['community_score_actual'],
                                                  train_metrics['community_score_predicted']))
community_r2_train = r2_score(train_metrics['community_score_actual'],
                              train_metrics['community_score_predicted'])

print(f"\nCommunity Score:")
print(f"  RMSE: {community_rmse_train:.2f}")
print(f"  R²: {community_r2_train:.3f}")

print("\n" + "-"*80)
print("PREDICTION ACCURACY (TEST SET)")
print("-"*80)

test_metrics = test_df.copy()

igs_rmse_test = np.sqrt(mean_squared_error(test_metrics['igs_score_actual'],
                                           test_metrics['igs_score_predicted']))
igs_mae_test = mean_absolute_error(test_metrics['igs_score_actual'],
                                   test_metrics['igs_score_predicted'])
igs_r2_test = r2_score(test_metrics['igs_score_actual'],
                       test_metrics['igs_score_predicted'])

print(f"\nIGS Score:")
print(f"  RMSE: {igs_rmse_test:.2f}")
print(f"  MAE: {igs_mae_test:.2f}")
print(f"  R²: {igs_r2_test:.3f}")

place_rmse_test = np.sqrt(mean_squared_error(test_metrics['place_score_actual'],
                                             test_metrics['place_score_predicted']))
place_r2_test = r2_score(test_metrics['place_score_actual'],
                         test_metrics['place_score_predicted'])

print(f"\nPlace Score:")
print(f"  RMSE: {place_rmse_test:.2f}")
print(f"  R²: {place_r2_test:.3f}")

economy_rmse_test = np.sqrt(mean_squared_error(test_metrics['economy_score_actual'],
                                               test_metrics['economy_score_predicted']))
economy_r2_test = r2_score(test_metrics['economy_score_actual'],
                           test_metrics['economy_score_predicted'])

print(f"\nEconomy Score:")
print(f"  RMSE: {economy_rmse_test:.2f}")
print(f"  R²: {economy_r2_test:.3f}")

community_rmse_test = np.sqrt(mean_squared_error(test_metrics['community_score_actual'],
                                                 test_metrics['community_score_predicted']))
community_r2_test = r2_score(test_metrics['community_score_actual'],
                             test_metrics['community_score_predicted'])

print(f"\nCommunity Score:")
print(f"  RMSE: {community_rmse_test:.2f}")
print(f"  R²: {community_r2_test:.3f}")

print("\n" + "="*80)
print("SAMPLE PREDICTIONS (FIRST 10 ROWS)")
print("="*80)
print(submission_df.head(10).to_string(index=False))

print("\n" + "="*80)
print("FILE GENERATION COMPLETE")
print("="*80)
print(f"\nOutput file: {output_path}")
print(f"Total rows: {len(submission_df)}")
print(f"Columns: {len(submission_df.columns)}")
print("\n" + "="*80 + "\n")

"""
Train Augmented ML Models Using Solution Counties

Combines Lonoke County data with solution counties (Beltrami, Chaffee, Fulton)
to learn intervention effects and predict improved outcomes for Lonoke.

Data Sources:
- Lonoke: Tract-level IGS trends (6 tracts, 2019-2024)
- Beltrami: Business/employment metrics (2020, 2023)
- Chaffee: IGS pillar scores (2020-2024)
- Fulton: IGS pillar scores (2020-2024)

Strategy:
- Use solution counties to learn relationships between business metrics and IGS scores
- Apply learned patterns to predict Lonoke improvements under interventions
"""

import pandas as pd
import numpy as np
from pathlib import Path
import joblib

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import warnings
warnings.filterwarnings('ignore')


def load_lonoke_data():
    """Load Lonoke County tract-level IGS data"""
    path = Path(
        '/Users/cyrilkups/Desktop/DataDrive Project/igs_ml/data/igs_trends_features.csv')
    df = pd.read_csv(path)
    df['county'] = 'Lonoke County, AR'
    df['data_source'] = 'lonoke'
    print(f"Loaded Lonoke: {len(df)} rows (2019-2024)")
    return df


def load_solution_counties():
    """Load solution counties data"""
    path = Path(
        '/Users/cyrilkups/Desktop/DataDrive Project/igs_plus_more_data/integrated_county_solutions.csv')
    df = pd.read_csv(path)
    df['data_source'] = 'solution'
    print(f"Loaded solution counties: {len(df)} rows")
    print(f"  Counties: {df['county'].unique()}")
    return df


def prepare_combined_dataset():
    """
    Combine Lonoke and solution counties into unified dataset

    Returns unified DataFrame with aligned features
    """
    lonoke = load_lonoke_data()
    solutions = load_solution_counties()

    # Align columns: create common feature set
    # Core IGS features (available in both)
    common_features = ['year', 'county', 'data_source']

    # IGS scores (targets)
    target_cols = ['igs_score', 'place_score',
                   'economy_score', 'community_score']

    # Lonoke features (tract-level)
    lonoke_features = [
        'median_income',
        'broadband_access_pct',
        'minority_owned_businesses_pct',
        'housing_cost_burden_pct',
        'early_education_enrollment_pct',
        'income_growth',
        'broadband_growth',
        'minority_business_growth',
        'housing_burden_change',
        'early_ed_growth'
    ]

    # Solution county features (county-level business metrics)
    solution_features = [
        'num_establishments',
        'num_employees',
        'annual_payroll',
        'total_firms',
        'employer_firms',
        'nonemployer_firms'
    ]

    # Create unified dataset
    lonoke_df = lonoke[common_features + target_cols + lonoke_features].copy()
    solutions_df = solutions[common_features +
                             target_cols + solution_features].copy()

    # Combine
    combined = pd.concat([lonoke_df, solutions_df], ignore_index=True)

    print(f"\nCombined dataset:")
    print(f"  Total rows: {len(combined)}")
    print(
        f"  Lonoke rows: {len(combined[combined['data_source'] == 'lonoke'])}")
    print(
        f"  Solution rows: {len(combined[combined['data_source'] == 'solution'])}")
    print(f"  Years: {sorted(combined['year'].unique())}")

    return combined


def engineer_features(df):
    """
    Engineer additional features and prepare final feature matrix

    Creates:
    - Lagged features (previous year values)
    - Year-over-year changes
    - Composite indicators
    """
    df = df.sort_values(['county', 'year']).reset_index(drop=True)

    # Create lagged features (previous year)
    for col in ['igs_score', 'place_score', 'economy_score', 'community_score']:
        if col in df.columns:
            df[f'{col}_lag1'] = df.groupby('county')[col].shift(1)
            df[f'{col}_change'] = df[col] - df[f'{col}_lag1']

    # Business efficiency metrics
    if 'num_employees' in df.columns and 'num_establishments' in df.columns:
        df['employees_per_establishment'] = df['num_employees'] / \
            df['num_establishments']
    if 'annual_payroll' in df.columns and 'num_employees' in df.columns:
        df['payroll_per_employee'] = df['annual_payroll'] / df['num_employees']

    return df


def prepare_training_data(df, target_name):
    """
    Prepare X, y for model training

    Focuses on rows with non-null target values
    Handles missing features appropriately
    """
    # Filter to rows with target
    df_train = df[df[target_name].notna()].copy()

    # Define feature categories
    feature_candidates = [
        # Lonoke tract features
        'median_income',
        'broadband_access_pct',
        'minority_owned_businesses_pct',
        'housing_cost_burden_pct',
        'early_education_enrollment_pct',
        'income_growth',
        'broadband_growth',
        'minority_business_growth',
        'housing_burden_change',
        'early_ed_growth',
        # Solution county business features
        'num_establishments',
        'num_employees',
        'annual_payroll',
        'total_firms',
        'employer_firms',
        'nonemployer_firms',
        'employees_per_establishment',
        'payroll_per_employee',
        # Lagged scores
        'igs_score_lag1',
        'place_score_lag1',
        'economy_score_lag1',
        'community_score_lag1',
        # Changes
        'igs_score_change',
        'place_score_change',
        'economy_score_change',
        'community_score_change'
    ]

    # Keep only features that exist and have sufficient data
    available_features = []
    for feat in feature_candidates:
        if feat in df_train.columns:
            non_null_pct = df_train[feat].notna().sum() / len(df_train)
            if non_null_pct > 0.3:  # Keep if >30% non-null
                available_features.append(feat)

    # Prepare X (features) and y (target)
    X = df_train[available_features].copy()
    y = df_train[target_name].copy()

    # Fill remaining missing values with median
    for col in X.columns:
        X[col] = X[col].fillna(X[col].median())

    print(f"\nTraining data for {target_name}:")
    print(f"  Samples: {len(X)}")
    print(f"  Features: {len(available_features)}")
    print(f"  Feature list: {available_features}")

    return X, y, available_features


def train_augmented_model(X, y, target_name, random_state=42):
    """
    Train Random Forest model on combined dataset

    Uses both Lonoke and solution county data to learn
    intervention patterns
    """
    print(f"\n{'='*70}")
    print(f"TRAINING AUGMENTED MODEL FOR: {target_name.upper()}")
    print(f"{'='*70}")

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=random_state
    )

    print(f"Train size: {len(X_train)}, Test size: {len(X_test)}")

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train Random Forest
    model = RandomForestRegressor(
        n_estimators=150,
        max_depth=8,
        min_samples_split=3,
        min_samples_leaf=2,
        random_state=random_state,
        n_jobs=-1
    )

    model.fit(X_train_scaled, y_train)

    # Predictions
    y_train_pred = model.predict(X_train_scaled)
    y_test_pred = model.predict(X_test_scaled)

    # Evaluate
    train_r2 = r2_score(y_train, y_train_pred)
    test_r2 = r2_score(y_test, y_test_pred)
    test_mae = mean_absolute_error(y_test, y_test_pred)
    test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))

    # Cross-validation
    cv_scores = cross_val_score(
        model, X_train_scaled, y_train, cv=min(5, len(X_train)), scoring='r2'
    )

    print(f"\nPerformance Metrics:")
    print(f"  Train R²: {train_r2:.4f}")
    print(f"  Test R²: {test_r2:.4f}")
    print(f"  Test MAE: {test_mae:.4f}")
    print(f"  Test RMSE: {test_rmse:.4f}")
    print(f"  CV R²: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)

    print(f"\nTop 10 Important Features:")
    for idx, row in feature_importance.head(10).iterrows():
        print(f"  {row['feature']}: {row['importance']:.4f}")

    return {
        'model': model,
        'scaler': scaler,
        'train_r2': train_r2,
        'test_r2': test_r2,
        'test_mae': test_mae,
        'test_rmse': test_rmse,
        'cv_scores': cv_scores,
        'feature_importance': feature_importance,
        'feature_names': list(X.columns)
    }


def save_augmented_models(results, target_name, output_dir='models_augmented'):
    """Save trained model artifacts"""
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Save model and scaler
    joblib.dump(results['model'], f"{output_dir}/{target_name}_model.joblib")
    joblib.dump(results['scaler'], f"{output_dir}/{target_name}_scaler.joblib")

    # Save feature importance
    results['feature_importance'].to_csv(
        f"{output_dir}/{target_name}_feature_importance.csv", index=False
    )

    print(f"✓ Saved model artifacts to {output_dir}/")


def predict_lonoke_interventions(combined_df, trained_models):
    """
    Predict Lonoke County outcomes under intervention scenarios

    Simulates:
    1. Housing affordability program (reduce housing burden by 10%)
    2. Early education expansion (increase enrollment by 12%)
    3. Small business support (increase minority businesses by 15%)
    """
    print(f"\n{'='*70}")
    print("PREDICTING LONOKE INTERVENTIONS")
    print(f"{'='*70}")

    # Get Lonoke 2024 baseline
    lonoke_2024 = combined_df[
        (combined_df['data_source'] == 'lonoke') &
        (combined_df['year'] == 2024)
    ].copy()

    if lonoke_2024.empty:
        print("No Lonoke 2024 data found, using latest available year")
        lonoke_latest = combined_df[combined_df['data_source'] == 'lonoke']
        latest_year = lonoke_latest['year'].max()
        lonoke_2024 = lonoke_latest[lonoke_latest['year']
                                    == latest_year].copy()

    # Average across tracts for county-level baseline
    baseline = lonoke_2024.mean(numeric_only=True)

    print(f"\nBaseline Lonoke County (2024):")
    print(f"  IGS Score: {baseline.get('igs_score', 'N/A'):.2f}")
    print(
        f"  Housing Burden: {baseline.get('housing_cost_burden_pct', 'N/A'):.2f}%")
    print(
        f"  Early Education: {baseline.get('early_education_enrollment_pct', 'N/A'):.2f}%")
    print(
        f"  Minority Businesses: {baseline.get('minority_owned_businesses_pct', 'N/A'):.2f}%")

    # Intervention scenarios
    scenarios = {
        'Housing Affordability': {
            # -10%
            'housing_cost_burden_pct': baseline.get('housing_cost_burden_pct', 0) * 0.9,
            'description': 'Reduce housing cost burden by 10%'
        },
        'Early Education': {
            # +12%
            'early_education_enrollment_pct': baseline.get('early_education_enrollment_pct', 0) * 1.12,
            'description': 'Increase early education enrollment by 12%'
        },
        'Business Support': {
            # +15%
            'minority_owned_businesses_pct': baseline.get('minority_owned_businesses_pct', 0) * 1.15,
            'description': 'Increase minority-owned businesses by 15%'
        },
        'Combined': {
            'housing_cost_burden_pct': baseline.get('housing_cost_burden_pct', 0) * 0.9,
            'early_education_enrollment_pct': baseline.get('early_education_enrollment_pct', 0) * 1.12,
            'minority_owned_businesses_pct': baseline.get('minority_owned_businesses_pct', 0) * 1.15,
            'description': 'All three interventions combined'
        }
    }

    results = []
    for scenario_name, changes in scenarios.items():
        if scenario_name == 'Combined':
            continue  # Process last

        # Create scenario data
        scenario_data = baseline.copy()
        for key, val in changes.items():
            if key != 'description':
                scenario_data[key] = val

        # Predict using trained models
        predictions = {'scenario': scenario_name}
        for target in ['igs_score', 'place_score', 'economy_score', 'community_score']:
            if target in trained_models:
                model_info = trained_models[target]
                features = model_info['feature_names']

                # Prepare feature vector
                X_scenario = pd.DataFrame([scenario_data[features]]).fillna(
                    pd.Series({f: scenario_data.get(f, 0) for f in features})
                )
                X_scenario = X_scenario.fillna(X_scenario.median())

                # Scale and predict
                X_scaled = model_info['scaler'].transform(X_scenario)
                pred = model_info['model'].predict(X_scaled)[0]

                predictions[target] = pred
                predictions[f'{target}_gain'] = pred - baseline.get(target, 0)

        results.append(predictions)

    # Combined scenario
    scenario_data = baseline.copy()
    for key, val in scenarios['Combined'].items():
        if key != 'description':
            scenario_data[key] = val

    predictions = {'scenario': 'Combined'}
    for target in ['igs_score', 'place_score', 'economy_score', 'community_score']:
        if target in trained_models:
            model_info = trained_models[target]
            features = model_info['feature_names']
            X_scenario = pd.DataFrame([scenario_data[features]]).fillna(
                pd.Series({f: scenario_data.get(f, 0) for f in features})
            )
            X_scenario = X_scenario.fillna(X_scenario.median())
            X_scaled = model_info['scaler'].transform(X_scenario)
            pred = model_info['model'].predict(X_scaled)[0]
            predictions[target] = pred
            predictions[f'{target}_gain'] = pred - baseline.get(target, 0)
    results.append(predictions)

    results_df = pd.DataFrame(results)
    results_df.to_csv(
        'models_augmented/lonoke_intervention_predictions.csv', index=False)

    print(f"\n{'='*70}")
    print("INTERVENTION PREDICTIONS")
    print(f"{'='*70}")
    print(results_df.to_string(index=False))

    return results_df


if __name__ == "__main__":
    print("="*70)
    print("AUGMENTED MODEL TRAINING - SOLUTION COUNTIES + LONOKE")
    print("="*70)

    # Load and combine datasets
    combined_df = prepare_combined_dataset()

    # Engineer features
    combined_df = engineer_features(combined_df)

    # Train models for each target
    targets = ['igs_score', 'place_score', 'economy_score', 'community_score']
    trained_models = {}

    for target in targets:
        X, y, feature_names = prepare_training_data(combined_df, target)

        if len(X) < 10:
            print(f"\nSkipping {target}: insufficient data ({len(X)} samples)")
            continue

        results = train_augmented_model(X, y, target)
        results['feature_names'] = feature_names
        trained_models[target] = results

        save_augmented_models(results, target)

    # Predict Lonoke interventions
    if trained_models:
        predictions = predict_lonoke_interventions(combined_df, trained_models)

    print("\n" + "="*70)
    print("AUGMENTED TRAINING COMPLETE!")
    print("="*70)
    print("\nOutputs saved to: models_augmented/")
    print("  - {target}_model.joblib")
    print("  - {target}_scaler.joblib")
    print("  - {target}_feature_importance.csv")
    print("  - lonoke_intervention_predictions.csv")

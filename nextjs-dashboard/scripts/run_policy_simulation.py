#!/usr/bin/env python3
"""
Run ML-powered policy simulation for Lonoke County
Loads trained Random Forest models and predicts intervention impacts
"""

import sys
import json
import numpy as np
import pandas as pd
from pathlib import Path
import joblib
import warnings
warnings.filterwarnings('ignore')


def main():
    # Parse command line arguments
    if len(sys.argv) != 4:
        print(json.dumps(
            {"error": "Usage: run_policy_simulation.py <housing_reduction> <education_increase> <business_increase>"}))
        sys.exit(1)

    housing_reduction = float(sys.argv[1])
    education_increase = float(sys.argv[2])
    business_increase = float(sys.argv[3])

    # Load trained models
    models_dir = Path(
        '/Users/cyrilkups/Desktop/DataDrive Project/igs_plus_more_data/models_augmented')

    try:
        igs_model = joblib.load(models_dir / 'igs_score_model.joblib')
        igs_scaler = joblib.load(models_dir / 'igs_score_scaler.joblib')
        place_model = joblib.load(models_dir / 'place_score_model.joblib')
        place_scaler = joblib.load(models_dir / 'place_score_scaler.joblib')
        economy_model = joblib.load(models_dir / 'economy_score_model.joblib')
        economy_scaler = joblib.load(
            models_dir / 'economy_score_scaler.joblib')
        community_model = joblib.load(
            models_dir / 'community_score_model.joblib')
        community_scaler = joblib.load(
            models_dir / 'community_score_scaler.joblib')
    except Exception as e:
        print(json.dumps({"error": f"Failed to load models: {str(e)}"}))
        sys.exit(1)

    # Baseline 2024 values for Lonoke County (Tract 20800)
    baseline = {
        'year': 2024,
        'median_income': 36500,
        'broadband_access_pct': 58.7,
        'minority_owned_businesses_pct': 8.3,
        'housing_cost_burden_pct': 86.5,
        'early_education_enrollment_pct': 33.4,
        'income_growth': -3.1,
        'broadband_growth': 2.9,
        'minority_business_growth': 0.0,
        'housing_burden_change': 0.0,
        'early_ed_growth': -3.3,
        'igs_score': 27.0,
        'place_score': 21.0,
        'economy_score': 20.0,
        'community_score': 40.0
    }

    # Create intervention scenario
    intervention = baseline.copy()
    intervention['housing_cost_burden_pct'] = max(
        0, baseline['housing_cost_burden_pct'] - housing_reduction)
    intervention['early_education_enrollment_pct'] = min(
        100, baseline['early_education_enrollment_pct'] + education_increase)
    intervention['minority_owned_businesses_pct'] = min(
        100, baseline['minority_owned_businesses_pct'] + business_increase)

    # Calculate changes
    intervention['housing_burden_change'] = intervention['housing_cost_burden_pct'] - \
        baseline['housing_cost_burden_pct']
    intervention['early_ed_growth'] = ((intervention['early_education_enrollment_pct'] - baseline['early_education_enrollment_pct']) /
                                       baseline['early_education_enrollment_pct'] * 100) if baseline['early_education_enrollment_pct'] > 0 else 0
    intervention['minority_business_growth'] = ((intervention['minority_owned_businesses_pct'] - baseline['minority_owned_businesses_pct']) /
                                                baseline['minority_owned_businesses_pct'] * 100) if baseline['minority_owned_businesses_pct'] > 0 else 0

    # Feature columns (18 features used in training)
    feature_cols = [
        'median_income', 'broadband_access_pct', 'minority_owned_businesses_pct',
        'housing_cost_burden_pct', 'early_education_enrollment_pct',
        'income_growth', 'broadband_growth', 'minority_business_growth',
        'housing_burden_change', 'early_ed_growth',
        'igs_score_lag1', 'place_score_lag1', 'economy_score_lag1', 'community_score_lag1',
        'igs_score_change', 'place_score_change', 'economy_score_change', 'community_score_change'
    ]

    # Add lagged and change features
    for score_type in ['igs_score', 'place_score', 'economy_score', 'community_score']:
        baseline[f'{score_type}_lag1'] = baseline[score_type]
        baseline[f'{score_type}_change'] = 0
        intervention[f'{score_type}_lag1'] = baseline[score_type]
        intervention[f'{score_type}_change'] = 0

    # Predict baseline
    X_baseline = pd.DataFrame([baseline])[feature_cols].fillna(0)
    X_baseline_scaled = igs_scaler.transform(X_baseline)

    baseline_pred = {
        'igs_score': float(igs_model.predict(X_baseline_scaled)[0]),
        'place_score': float(place_model.predict(place_scaler.transform(X_baseline))[0]),
        'economy_score': float(economy_model.predict(economy_scaler.transform(X_baseline))[0]),
        'community_score': float(community_model.predict(community_scaler.transform(X_baseline))[0])
    }

    # Predict intervention
    X_intervention = pd.DataFrame([intervention])[feature_cols].fillna(0)
    X_intervention_scaled = igs_scaler.transform(X_intervention)

    intervention_pred = {
        'igs_score': float(igs_model.predict(X_intervention_scaled)[0]),
        'place_score': float(place_model.predict(place_scaler.transform(X_intervention))[0]),
        'economy_score': float(economy_model.predict(economy_scaler.transform(X_intervention))[0]),
        'community_score': float(community_model.predict(community_scaler.transform(X_intervention))[0])
    }

    # Calculate impacts
    impacts = {
        'igs_score': intervention_pred['igs_score'] - baseline_pred['igs_score'],
        'place_score': intervention_pred['place_score'] - baseline_pred['place_score'],
        'economy_score': intervention_pred['economy_score'] - baseline_pred['economy_score'],
        'community_score': intervention_pred['community_score'] - baseline_pred['community_score']
    }

    # Project to 2030 (linear progression)
    projection_years = [2024, 2025, 2026, 2027, 2028, 2029, 2030]
    projection_data = []

    for i, year in enumerate(projection_years):
        progress = i / (len(projection_years) - 1)
        projection_data.append({
            'year': str(year),
            # Continuing decline trend (-0.3 per year)
            'baseline': round(27.0 - (0.3 * i), 2),
            'intervention': round(27.0 + (impacts['igs_score'] * progress), 2)
        })

    # Prepare result
    result = {
        'baseline': baseline_pred,
        'intervention': intervention_pred,
        'impacts': impacts,
        'projection': projection_data,
        'scenario': {
            'housing_burden': intervention['housing_cost_burden_pct'],
            'early_education': intervention['early_education_enrollment_pct'],
            'minority_business': intervention['minority_owned_businesses_pct']
        }
    }

    print(json.dumps(result))


if __name__ == '__main__':
    main()

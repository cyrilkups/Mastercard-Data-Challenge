"""
Model Prediction Script for IGS Score Prediction

This script demonstrates how to:
1. Load saved models and scalers
2. Make predictions on new data
3. Load feature importance for interpretation

Use this script to make predictions after training models with train_ml_model.py
"""

import pandas as pd
import numpy as np
import joblib
from pathlib import Path


def load_model_artifacts(target_name, models_dir='models'):
    """
    Load trained model, scaler, and feature importance for a target.

    Parameters:
    -----------
    target_name : str
        Name of target variable (e.g., 'place_score', 'economy_score')
    models_dir : str
        Directory containing saved models

    Returns:
    --------
    dict
        Dictionary containing model, scaler, and feature importance
    """
    models_path = Path(models_dir)

    # Load model
    model_file = models_path / f'{target_name}_model.joblib'
    model = joblib.load(model_file)
    print(f"✓ Loaded model: {model_file}")

    # Load scaler
    scaler_file = models_path / f'{target_name}_scaler.joblib'
    scaler = joblib.load(scaler_file)
    print(f"✓ Loaded scaler: {scaler_file}")

    # Load feature importance
    importance_file = models_path / f'{target_name}_feature_importance.csv'
    feature_importance = pd.read_csv(importance_file)
    print(f"✓ Loaded feature importance: {importance_file}")

    return {
        'model': model,
        'scaler': scaler,
        'feature_importance': feature_importance
    }


def prepare_prediction_features(df):
    """
    Prepare features for prediction (same as training).

    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe with required columns

    Returns:
    --------
    pd.DataFrame
        Feature matrix ready for prediction
    """
    required_features = [
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

    # Check if all required features are present
    missing_features = set(required_features) - set(df.columns)
    if missing_features:
        raise ValueError(f"Missing required features: {missing_features}")

    return df[required_features].copy()


def predict_score(data, target_name, models_dir='models'):
    """
    Make predictions for a specific target using saved model.

    Parameters:
    -----------
    data : pd.DataFrame
        Input data with required features
    target_name : str
        Target to predict ('place_score', 'economy_score', 'community_score', 'igs_score')
    models_dir : str
        Directory containing saved models

    Returns:
    --------
    np.ndarray
        Predicted values
    """
    # Load model artifacts
    artifacts = load_model_artifacts(target_name, models_dir)
    model = artifacts['model']
    scaler = artifacts['scaler']

    # Prepare features
    X = prepare_prediction_features(data)

    # Scale features
    X_scaled = scaler.transform(X)

    # Make predictions
    predictions = model.predict(X_scaled)

    print(f"\n✓ Generated {len(predictions)} predictions for {target_name}")

    return predictions


def predict_all_scores(data, models_dir='models'):
    """
    Make predictions for all four targets.

    Parameters:
    -----------
    data : pd.DataFrame
        Input data with required features
    models_dir : str
        Directory containing saved models

    Returns:
    --------
    pd.DataFrame
        DataFrame with predictions for all targets
    """
    targets = ['place_score', 'economy_score', 'community_score', 'igs_score']

    print("="*60)
    print("PREDICTING ALL IGS SCORES")
    print("="*60 + "\n")

    predictions_df = data.copy()

    for target in targets:
        print(f"\nPredicting {target}...")
        predictions = predict_score(data, target, models_dir)
        predictions_df[f'predicted_{target}'] = predictions

    print("\n" + "="*60)
    print("PREDICTIONS COMPLETE")
    print("="*60)

    return predictions_df


def display_feature_importance(target_name, models_dir='models', top_n=10):
    """
    Display feature importance for a specific model.

    Parameters:
    -----------
    target_name : str
        Target variable name
    models_dir : str
        Directory containing saved models
    top_n : int
        Number of top features to display
    """
    importance_file = Path(models_dir) / \
        f'{target_name}_feature_importance.csv'
    feature_importance = pd.read_csv(importance_file)

    print(f"\n{'='*60}")
    print(f"Feature Importance for {target_name}")
    print(f"{'='*60}\n")
    print(feature_importance.head(top_n).to_string(index=False))

    return feature_importance


def main():
    """
    Example usage of prediction functions.
    """
    print("="*60)
    print("IGS MODEL PREDICTION - EXAMPLE")
    print("="*60 + "\n")

    # Load test data
    print("Loading test data...")
    data_path = "data_cleaned/igs_trends_features.csv"
    df = pd.read_csv(data_path)

    # Select a few rows for demonstration
    test_data = df.head(5)[['tract', 'year',
                            'median_income',
                            'broadband_access_pct',
                            'minority_owned_businesses_pct',
                            'housing_cost_burden_pct',
                            'early_education_enrollment_pct',
                            'income_growth',
                            'broadband_growth',
                            'minority_business_growth',
                            'housing_burden_change',
                            'early_ed_growth']].copy()

    print(f"Selected {len(test_data)} samples for prediction\n")

    # Make predictions for all targets
    predictions = predict_all_scores(test_data)

    # Display results
    print("\n" + "="*60)
    print("PREDICTION RESULTS")
    print("="*60 + "\n")

    result_cols = ['tract', 'year',
                   'predicted_place_score', 'predicted_economy_score',
                   'predicted_community_score', 'predicted_igs_score']

    print(predictions[result_cols].to_string(index=False))

    # Show feature importance for IGS score
    display_feature_importance('igs_score', top_n=10)

    print("\n" + "="*60)
    print("EXAMPLE COMPLETE")
    print("="*60)
    print("\nTo use these models on your own data:")
    print("1. Prepare data with the required 10 features")
    print("2. Call predict_score() or predict_all_scores()")
    print("3. Models automatically scale features and make predictions")

    return predictions


if __name__ == "__main__":
    predictions = main()

"""
ML Model Training Script for IGS (Inclusive Growth Score) Prediction

This script trains Random Forest models to predict:
- place_score
- economy_score
- community_score
- igs_score

Uses level indicators and trend features with proper scaling and model persistence.
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


def load_cleaned_data(file_path):
    """Load the cleaned IGS data with trend features."""
    print(f"Loading cleaned data from {file_path}...")
    df = pd.read_csv(file_path)
    print(f"Loaded {len(df)} rows, {len(df.columns)} columns")
    print(f"\nData date range: {df['year'].min()} - {df['year'].max()}")
    print(f"Number of unique tracts: {df['tract'].nunique()}")
    return df


def prepare_features(df):
    """
    Prepare feature matrix with level and trend indicators.

    Parameters:
    -----------
    df : pd.DataFrame
        Cleaned data with trend features

    Returns:
    --------
    X : pd.DataFrame
        Feature matrix with level and trend indicators
    feature_names : list
        Names of features used
    """
    print("\nPreparing features...")

    # Define feature sets
    level_features = [
        'median_income',
        'broadband_access_pct',
        'minority_owned_businesses_pct',
        'housing_cost_burden_pct',
        'early_education_enrollment_pct'
    ]

    trend_features = [
        'income_growth',
        'broadband_growth',
        'minority_business_growth',
        'housing_burden_change',
        'early_ed_growth'
    ]

    # Combine all features
    all_features = level_features + trend_features

    # Create feature matrix
    X = df[all_features].copy()

    print(f"Feature matrix shape: {X.shape}")
    print(f"\nFeatures used:")
    print("  Level indicators:")
    for feat in level_features:
        print(f"    - {feat}")
    print("  Trend indicators:")
    for feat in trend_features:
        print(f"    - {feat}")

    return X, all_features


def train_model_for_target(X_train, X_test, y_train, y_test, target_name,
                           scaler, feature_names, model_params=None):
    """
    Train a Random Forest model for a specific target variable.

    Parameters:
    -----------
    X_train, X_test : pd.DataFrame
        Training and test features
    y_train, y_test : pd.Series
        Training and test target values
    target_name : str
        Name of the target variable
    scaler : StandardScaler
        Fitted scaler (already fitted on X_train)
    feature_names : list
        Names of features
    model_params : dict
        Random Forest parameters (optional)

    Returns:
    --------
    dict
        Dictionary containing model, metrics, and predictions
    """
    print(f"\n{'='*60}")
    print(f"Training Random Forest for: {target_name}")
    print(f"{'='*60}")

    # Default model parameters
    if model_params is None:
        model_params = {
            'n_estimators': 100,
            'max_depth': 10,
            'min_samples_split': 5,
            'min_samples_leaf': 2,
            'random_state': 42,
            'n_jobs': -1
        }

    # Scale features
    X_train_scaled = scaler.transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train model
    print(f"Training with parameters: {model_params}")
    model = RandomForestRegressor(**model_params)
    model.fit(X_train_scaled, y_train)

    # Make predictions
    y_train_pred = model.predict(X_train_scaled)
    y_test_pred = model.predict(X_test_scaled)

    # Calculate metrics
    train_r2 = r2_score(y_train, y_train_pred)
    test_r2 = r2_score(y_test, y_test_pred)
    train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
    test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
    train_mae = mean_absolute_error(y_train, y_train_pred)
    test_mae = mean_absolute_error(y_test, y_test_pred)

    # Cross-validation (on training data)
    print("Running 5-fold cross-validation...")
    cv_scores = cross_val_score(
        RandomForestRegressor(**model_params),
        X_train_scaled,
        y_train,
        cv=min(5, len(X_train)),  # Use fewer folds if dataset is small
        scoring='r2',
        n_jobs=-1
    )
    cv_mean = cv_scores.mean()
    cv_std = cv_scores.std()

    # Print results
    print(f"\n{'─'*60}")
    print(f"Results for {target_name}:")
    print(f"{'─'*60}")
    print(f"  Train R²:     {train_r2:.4f}")
    print(f"  Train MAE:    {train_mae:.4f}")
    print(f"  Train RMSE:   {train_rmse:.4f}")
    print(f"  ──────────────────────────")
    print(f"  Test R²:      {test_r2:.4f}")
    print(f"  Test MAE:     {test_mae:.4f}")
    print(f"  Test RMSE:    {test_rmse:.4f}")
    print(f"  ──────────────────────────")
    print(f"  CV R² (mean): {cv_mean:.4f} ± {cv_std:.4f}")

    # Feature importance
    feature_importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)

    print(f"\nTop 5 Most Important Features:")
    for idx, row in feature_importance_df.head(5).iterrows():
        print(f"  {row['feature']:<35} {row['importance']:.4f}")

    return {
        'model': model,
        'train_r2': train_r2,
        'test_r2': test_r2,
        'train_mae': train_mae,
        'test_mae': test_mae,
        'train_rmse': train_rmse,
        'test_rmse': test_rmse,
        'cv_r2_mean': cv_mean,
        'cv_r2_std': cv_std,
        'feature_importance': feature_importance_df,
        'predictions': y_test_pred
    }


def save_model_artifacts(model, scaler, feature_importance_df, target_name, output_dir='models'):
    """
    Save model, scaler, and feature importance to disk.

    Parameters:
    -----------
    model : RandomForestRegressor
        Trained model
    scaler : StandardScaler
        Fitted scaler
    feature_importance_df : pd.DataFrame
        Feature importance dataframe
    target_name : str
        Name of target variable
    output_dir : str
        Directory to save artifacts
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Save model
    model_file = output_path / f'{target_name}_model.joblib'
    joblib.dump(model, model_file)
    print(f"  ✓ Model saved: {model_file}")

    # Save scaler
    scaler_file = output_path / f'{target_name}_scaler.joblib'
    joblib.dump(scaler, scaler_file)
    print(f"  ✓ Scaler saved: {scaler_file}")

    # Save feature importance
    importance_file = output_path / f'{target_name}_feature_importance.csv'
    feature_importance_df.to_csv(importance_file, index=False)
    print(f"  ✓ Feature importance saved: {importance_file}")


def create_summary_report(all_results, output_dir='models'):
    """
    Create a summary report comparing all models.

    Parameters:
    -----------
    all_results : dict
        Dictionary of results for all target variables
    output_dir : str
        Directory to save report
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Create comparison dataframe
    comparison_data = []
    for target_name, results in all_results.items():
        comparison_data.append({
            'Target': target_name,
            'Test R²': results['test_r2'],
            'Test MAE': results['test_mae'],
            'Test RMSE': results['test_rmse'],
            'Train R²': results['train_r2'],
            'CV R² (mean)': results['cv_r2_mean'],
            'CV R² (std)': results['cv_r2_std']
        })

    comparison_df = pd.DataFrame(comparison_data)
    comparison_df = comparison_df.sort_values('Test R²', ascending=False)

    # Save comparison table
    comparison_file = output_path / 'model_comparison_summary.csv'
    comparison_df.to_csv(comparison_file, index=False)

    # Print summary
    print(f"\n{'='*60}")
    print("MODEL COMPARISON SUMMARY")
    print(f"{'='*60}\n")
    print(comparison_df.to_string(index=False))
    print(f"\n✓ Summary saved to: {comparison_file}")

    # Save detailed report
    report_file = output_path / 'training_report.txt'
    with open(report_file, 'w') as f:
        f.write("IGS SCORE PREDICTION - TRAINING REPORT\n")
        f.write("="*60 + "\n\n")
        f.write(
            f"Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write("MODELS TRAINED\n")
        f.write("-"*60 + "\n")
        for target_name in all_results.keys():
            f.write(f"  • {target_name}\n")

        f.write("\n\nMODEL PERFORMANCE COMPARISON\n")
        f.write("-"*60 + "\n")
        f.write(comparison_df.to_string(index=False))
        f.write("\n\n")

        f.write("DETAILED RESULTS BY TARGET\n")
        f.write("="*60 + "\n\n")

        for target_name, results in all_results.items():
            f.write(f"{target_name.upper()}\n")
            f.write("-"*60 + "\n")
            f.write(f"Test R²:     {results['test_r2']:.4f}\n")
            f.write(f"Test MAE:    {results['test_mae']:.4f}\n")
            f.write(f"Test RMSE:   {results['test_rmse']:.4f}\n")
            f.write(f"Train R²:    {results['train_r2']:.4f}\n")
            f.write(f"CV R² Mean:  {results['cv_r2_mean']:.4f}\n")
            f.write(f"CV R² Std:   {results['cv_r2_std']:.4f}\n")
            f.write(f"\nTop 5 Features:\n")
            for idx, row in results['feature_importance'].head(5).iterrows():
                f.write(
                    f"  {idx+1}. {row['feature']:<35} {row['importance']:.4f}\n")
            f.write("\n")

    print(f"✓ Detailed report saved to: {report_file}")

    return comparison_df


def main():
    """
    Main execution function for multi-target ML model training.
    """
    print("="*60)
    print("IGS MULTI-TARGET PREDICTION - ML MODEL TRAINING")
    print("="*60 + "\n")

    # Step 1: Load cleaned data
    data_path = "igs_trends_features.csv"
    df = load_cleaned_data(data_path)

    # Step 2: Prepare features
    X, feature_names = prepare_features(df)

    # Define target variables
    targets = ['place_score', 'economy_score', 'community_score', 'igs_score']

    print(f"\nTarget variables to predict: {targets}")

    # Step 3: Split data (same split for all targets)
    print(f"\nSplitting data (80% train, 20% test)...")
    X_train, X_test = train_test_split(X, test_size=0.2, random_state=42)

    print(f"  Training samples: {len(X_train)}")
    print(f"  Test samples: {len(X_test)}")

    # Step 4: Fit scaler on training data
    print(f"\nFitting StandardScaler on training data...")
    scaler = StandardScaler()
    scaler.fit(X_train)
    print(f"  ✓ Scaler fitted")

    # Step 5: Train models for each target
    all_results = {}

    for target_name in targets:
        y = df[target_name]
        y_train, y_test = train_test_split(y, test_size=0.2, random_state=42)

        # Train model
        results = train_model_for_target(
            X_train, X_test, y_train, y_test,
            target_name, scaler, feature_names
        )

        all_results[target_name] = results

        # Step 7: Save model artifacts
        print(f"\nSaving artifacts for {target_name}...")
        save_model_artifacts(
            results['model'],
            scaler,
            results['feature_importance'],
            target_name
        )

    # Step 8: Create summary report
    comparison_df = create_summary_report(all_results)

    print("\n" + "="*60)
    print("TRAINING COMPLETE!")
    print("="*60)
    print(f"\n✓ All models saved to 'models/' directory")
    print(f"✓ Each model includes:")
    print(f"  - Trained Random Forest model (.joblib)")
    print(f"  - Feature scaler (.joblib)")
    print(f"  - Feature importance (.csv)")
    print(f"\n✓ Summary reports generated:")
    print(f"  - model_comparison_summary.csv")
    print(f"  - training_report.txt")

    return all_results, comparison_df


if __name__ == "__main__":
    all_results, comparison_df = main()

"""
Policy Intervention Simulation Tool for IGS Score Prediction

This tool simulates the impact of policy interventions on IGS scores by:
1. Loading trained models and scalers
2. Extracting baseline features for a specific tract and year
3. Applying intervention adjustments to selected features
4. Predicting scores before and after intervention
5. Calculating the impact (delta) for each score

Use this to test "what-if" scenarios for policy decisions.
"""

import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from typing import Dict, Optional


class InterventionSimulator:
    """Simulates policy interventions and their impact on IGS scores."""

    def __init__(self, models_dir='models', data_path='data_cleaned/igs_trends_features.csv'):
        """
        Initialize the simulator with models and data.

        Parameters:
        -----------
        models_dir : str
            Directory containing trained models and scalers
        data_path : str
            Path to cleaned dataset
        """
        self.models_dir = Path(models_dir)
        self.data_path = data_path
        self.targets = ['place_score', 'economy_score',
                        'community_score', 'igs_score']
        self.models = {}
        self.scalers = {}
        self.data = None

        # Feature names
        self.features = [
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

        self._load_models()
        self._load_data()

    def _load_models(self):
        """Load all trained models and scalers."""
        print("Loading models and scalers...")
        for target in self.targets:
            model_file = self.models_dir / f'{target}_model.joblib'
            scaler_file = self.models_dir / f'{target}_scaler.joblib'

            self.models[target] = joblib.load(model_file)
            self.scalers[target] = joblib.load(scaler_file)
            print(f"  ✓ Loaded {target} model and scaler")

    def _load_data(self):
        """Load the cleaned dataset."""
        print(f"\nLoading data from {self.data_path}...")
        self.data = pd.read_csv(self.data_path)
        print(f"  ✓ Loaded {len(self.data)} rows")
        print(
            f"  ✓ Years: {self.data['year'].min()} - {self.data['year'].max()}")
        print(f"  ✓ Tracts: {self.data['tract'].nunique()}")

    def get_baseline_features(self, tract: str, year: int) -> Optional[pd.DataFrame]:
        """
        Extract baseline features for a specific tract and year.

        Parameters:
        -----------
        tract : str
            Census tract ID (can be with or without leading zeros)
        year : int
            Year

        Returns:
        --------
        pd.DataFrame or None
            Feature row if found, None otherwise
        """
        # Try to match tract as-is, or as integer, or zero-padded
        tract_variations = [
            str(tract),
            str(tract).zfill(11),
            int(str(tract).replace('-', '')
                ) if str(tract).replace('-', '').isdigit() else None
        ]

        baseline = None
        for tract_variant in tract_variations:
            if tract_variant is None:
                continue
            mask = (self.data['tract'].astype(str) == str(
                tract_variant)) & (self.data['year'] == year)
            baseline = self.data[mask]
            if len(baseline) > 0:
                break

        if baseline is None or len(baseline) == 0:
            print(f"⚠ Warning: No data found for tract {tract} in year {year}")
            print(f"  Available tracts: {sorted(self.data['tract'].unique())}")
            return None

        return baseline[self.features].copy()

    def apply_intervention(self, baseline_features: pd.DataFrame,
                           deltas: Dict[str, float]) -> pd.DataFrame:
        """
        Apply intervention adjustments to baseline features.

        Parameters:
        -----------
        baseline_features : pd.DataFrame
            Baseline feature values
        deltas : dict
            Dictionary of feature adjustments as relative percentages
            Example: {"broadband_access_pct": 0.20} means +20%

        Returns:
        --------
        pd.DataFrame
            Adjusted features after intervention
        """
        adjusted = baseline_features.copy()

        for feature, pct_change in deltas.items():
            if feature not in self.features:
                print(
                    f"⚠ Warning: '{feature}' is not a valid feature. Skipping.")
                continue

            if feature in adjusted.columns:
                original_value = adjusted[feature].iloc[0]
                new_value = original_value * (1 + pct_change)
                adjusted[feature] = new_value

                print(f"  {feature}:")
                print(f"    Original: {original_value:.2f}")
                print(f"    Adjustment: {pct_change:+.1%}")
                print(f"    New value: {new_value:.2f}")

        return adjusted

    def predict_scores(self, features: pd.DataFrame) -> Dict[str, float]:
        """
        Predict all four scores for given features.

        Parameters:
        -----------
        features : pd.DataFrame
            Feature values

        Returns:
        --------
        dict
            Predictions for each target score
        """
        predictions = {}

        for target in self.targets:
            # Scale features
            X_scaled = self.scalers[target].transform(features)

            # Predict
            pred = self.models[target].predict(X_scaled)[0]
            predictions[target] = pred

        return predictions

    def simulate_intervention(self, tract: str, year: int,
                              deltas: Dict[str, float]) -> Dict:
        """
        Simulate a policy intervention and calculate its impact.

        Parameters:
        -----------
        tract : str
            Census tract ID
        year : int
            Year
        deltas : dict
            Feature adjustments as relative percentages
            Example: {
                "broadband_access_pct": 0.20,  # +20%
                "housing_cost_burden_pct": -0.10,  # -10%
                "minority_owned_businesses_pct": 0.15,  # +15%
                "early_education_enrollment_pct": 0.12  # +12%
            }

        Returns:
        --------
        dict
            Results containing:
            - tract: Census tract ID
            - year: Year
            - interventions: Applied adjustments
            - baseline: Baseline scores
            - after_intervention: Scores after intervention
            - impact: Change in scores (after - baseline)
        """
        print("="*60)
        print("POLICY INTERVENTION SIMULATION")
        print("="*60)

        print(f"\nTract: {tract}")
        print(f"Year: {year}")

        # Get baseline features
        print("\n--- Extracting Baseline Features ---")
        baseline_features = self.get_baseline_features(tract, year)

        if baseline_features is None:
            return None

        # Predict baseline scores
        print("\n--- Baseline Predictions ---")
        baseline_scores = self.predict_scores(baseline_features)
        for target, score in baseline_scores.items():
            print(f"  {target}: {score:.2f}")

        # Apply intervention
        print("\n--- Applying Intervention ---")
        adjusted_features = self.apply_intervention(baseline_features, deltas)

        # Predict scores after intervention
        print("\n--- Predictions After Intervention ---")
        after_scores = self.predict_scores(adjusted_features)
        for target, score in after_scores.items():
            print(f"  {target}: {score:.2f}")

        # Calculate impact
        print("\n--- Impact Analysis ---")
        impact = {}
        for target in self.targets:
            delta = after_scores[target] - baseline_scores[target]
            impact[target] = delta
            direction = "↑" if delta > 0 else "↓" if delta < 0 else "→"
            print(f"  {target}: {delta:+.2f} {direction}")

        # Prepare results
        results = {
            'tract': tract,
            'year': year,
            'interventions': deltas,
            'baseline': baseline_scores,
            'after_intervention': after_scores,
            'impact': impact
        }

        print("\n" + "="*60)
        print("SIMULATION COMPLETE")
        print("="*60)

        return results

    def compare_interventions(self, tract: str, year: int,
                              intervention_scenarios: Dict[str, Dict[str, float]]) -> pd.DataFrame:
        """
        Compare multiple intervention scenarios side-by-side.

        Parameters:
        -----------
        tract : str
            Census tract ID
        year : int
            Year
        intervention_scenarios : dict
            Dictionary of named scenarios
            Example: {
                "Scenario A": {"broadband_access_pct": 0.20},
                "Scenario B": {"housing_cost_burden_pct": -0.15}
            }

        Returns:
        --------
        pd.DataFrame
            Comparison table of all scenarios
        """
        print("\n" + "="*60)
        print("COMPARING MULTIPLE INTERVENTION SCENARIOS")
        print("="*60)

        comparison_data = []

        # Get baseline
        baseline_features = self.get_baseline_features(tract, year)
        if baseline_features is None:
            return None

        baseline_scores = self.predict_scores(baseline_features)

        # Add baseline to comparison
        baseline_row = {'Scenario': 'Baseline (No Intervention)'}
        for target in self.targets:
            baseline_row[target] = baseline_scores[target]
        comparison_data.append(baseline_row)

        # Run each scenario
        for scenario_name, deltas in intervention_scenarios.items():
            print(f"\n--- {scenario_name} ---")
            adjusted = self.apply_intervention(
                baseline_features.copy(), deltas)
            scores = self.predict_scores(adjusted)

            row = {'Scenario': scenario_name}
            for target in self.targets:
                row[target] = scores[target]
                delta = scores[target] - baseline_scores[target]
                row[f'{target}_delta'] = delta

            comparison_data.append(row)

        comparison_df = pd.DataFrame(comparison_data)

        print("\n" + "="*60)
        print("SCENARIO COMPARISON")
        print("="*60 + "\n")
        print(comparison_df.to_string(index=False))

        return comparison_df


def main():
    """Example usage of the intervention simulator."""

    # Initialize simulator
    simulator = InterventionSimulator()

    print("\n" + "="*60)
    print("EXAMPLE 1: Single Intervention")
    print("="*60)

    # Example 1: Single intervention
    intervention_deltas = {
        "broadband_access_pct": 0.20,  # +20% broadband access
        "housing_cost_burden_pct": -0.10,  # -10% housing burden
        "minority_owned_businesses_pct": 0.15,  # +15% minority businesses
        "early_education_enrollment_pct": 0.12  # +12% early education
    }

    results = simulator.simulate_intervention(
        tract='5085020100',
        year=2023,
        deltas=intervention_deltas
    )

    if results:
        print("\n📊 Summary:")
        print(f"  Tract: {results['tract']}")
        print(f"  Year: {results['year']}")
        print(f"\n  Biggest Impact: ", end="")
        max_impact_target = max(
            results['impact'], key=lambda k: abs(results['impact'][k]))
        print(
            f"{max_impact_target} ({results['impact'][max_impact_target]:+.2f})")

    print("\n" + "="*60)
    print("EXAMPLE 2: Comparing Multiple Scenarios")
    print("="*60)

    # Example 2: Compare scenarios
    scenarios = {
        "Focus on Broadband": {
            "broadband_access_pct": 0.25
        },
        "Education Investment": {
            "early_education_enrollment_pct": 0.20
        },
        "Housing Affordability": {
            "housing_cost_burden_pct": -0.15
        },
        "Comprehensive Package": {
            "broadband_access_pct": 0.15,
            "housing_cost_burden_pct": -0.10,
            "early_education_enrollment_pct": 0.10,
            "minority_owned_businesses_pct": 0.12
        }
    }

    comparison = simulator.compare_interventions(
        tract='5085020100',
        year=2023,
        intervention_scenarios=scenarios
    )

    if comparison is not None:
        # Save comparison
        output_path = Path('models') / 'intervention_comparison.csv'
        comparison.to_csv(output_path, index=False)
        print(f"\n✓ Comparison saved to: {output_path}")


if __name__ == "__main__":
    main()

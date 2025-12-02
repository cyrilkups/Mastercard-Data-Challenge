import { NextResponse } from 'next/server';
import { exec } from 'child_process';
import { promisify } from 'util';

const execPromise = promisify(exec);

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const reportType = searchParams.get('type') || 'comprehensive';
    const dateRange = searchParams.get('dateRange') || 'all-time';

    // Python script to fetch real data
    const pythonScript = `
import pandas as pd
import json
import numpy as np
from pathlib import Path

# Load Lonoke County data
data_path = Path('/Users/cyrilkups/Desktop/DataDrive Project/igs_ml/data/igs_trends_features.csv')
df = pd.read_csv(data_path)

# Filter by date range
if '${dateRange}' == 'last-year':
    df = df[df['year'] >= 2024]
elif '${dateRange}' == 'last-quarter':
    df = df[df['year'] == 2024]
elif '${dateRange}' == 'all-time':
    pass  # Use all data

# Aggregate by year (average across tracts)
yearly = df.groupby('year').agg({
    'igs_score': 'mean',
    'place_score': 'mean',
    'economy_score': 'mean',
    'community_score': 'mean',
    'median_income': 'mean',
    'broadband_access_pct': 'mean',
    'housing_cost_burden_pct': 'mean',
    'early_education_enrollment_pct': 'mean',
    'minority_owned_businesses_pct': 'mean',
    'income_growth': 'mean',
    'broadband_growth': 'mean',
    'housing_burden_change': 'mean',
    'early_ed_growth': 'mean',
    'minority_business_growth': 'mean'
}).reset_index()

# Get latest year data
latest_year = yearly['year'].max()
latest = yearly[yearly['year'] == latest_year].iloc[0]
previous = yearly[yearly['year'] == latest_year - 1].iloc[0] if len(yearly) > 1 else latest

# Calculate changes
igs_change = ((latest['igs_score'] - previous['igs_score']) / previous['igs_score'] * 100) if previous['igs_score'] != 0 else 0
place_change = ((latest['place_score'] - previous['place_score']) / previous['place_score'] * 100) if previous['place_score'] != 0 else 0
economy_change = ((latest['economy_score'] - previous['economy_score']) / previous['economy_score'] * 100) if previous['economy_score'] != 0 else 0
community_change = ((latest['community_score'] - previous['community_score']) / previous['community_score'] * 100) if previous['community_score'] != 0 else 0

# Build comprehensive report
if '${reportType}' == 'comprehensive':
    # Load feature importance
    try:
        feature_importance_path = Path('/Users/cyrilkups/Desktop/DataDrive Project/igs_plus_more_data/models_augmented/igs_score_feature_importance.csv')
        feature_imp = pd.read_csv(feature_importance_path).head(10)
        top_features = feature_imp.to_dict('records')
    except:
        top_features = []
    
    result = {
        'metadata': {
            'title': 'Lonoke County IGS Comprehensive Report',
            'generated_date': pd.Timestamp.now().isoformat(),
            'date_range': '${dateRange}',
            'county': 'Lonoke County, Arkansas',
            'tracts': int(df['tract'].nunique()),
            'years_covered': f"{int(yearly['year'].min())}-{int(yearly['year'].max())}",
            'total_observations': int(len(df))
        },
        'executive_summary': {
            'current_igs': float(latest['igs_score']),
            'previous_igs': float(previous['igs_score']),
            'igs_change_pct': float(igs_change),
            'current_place': float(latest['place_score']),
            'place_change_pct': float(place_change),
            'current_economy': float(latest['economy_score']),
            'economy_change_pct': float(economy_change),
            'current_community': float(latest['community_score']),
            'community_change_pct': float(community_change),
            'status': 'Declining' if igs_change < 0 else 'Improving'
        },
        'historical_data': yearly[['year', 'igs_score', 'place_score', 'economy_score', 'community_score']].to_dict('records'),
        'detailed_indicators': {
            'economic': {
                'median_income': float(latest['median_income']),
                'income_growth': float(latest['income_growth']),
                'minority_business_pct': float(latest['minority_owned_businesses_pct']),
                'minority_business_growth': float(latest['minority_business_growth'])
            },
            'infrastructure': {
                'broadband_access': float(latest['broadband_access_pct']),
                'broadband_growth': float(latest['broadband_growth']),
                'housing_burden': float(latest['housing_cost_burden_pct']),
                'housing_burden_change': float(latest['housing_burden_change'])
            },
            'community': {
                'early_education': float(latest['early_education_enrollment_pct']),
                'early_ed_growth': float(latest['early_ed_growth'])
            }
        },
        'ml_model_info': {
            'model_type': 'Random Forest Regressor',
            'r2_score': 0.73,
            'training_samples': 36,
            'features_used': 18,
            'top_features': top_features,
            'solution_counties': ['Beltrami County, MN', 'Chaffee County, CO', 'Fulton County, GA']
        },
        'trends_analysis': {
            'igs_trend': 'Declining' if igs_change < 0 else 'Improving',
            'annual_change': float(igs_change),
            'five_year_change': float(((latest['igs_score'] - yearly['igs_score'].iloc[0]) / yearly['igs_score'].iloc[0] * 100) if len(yearly) > 4 else 0)
        }
    }
    
elif '${reportType}' == 'summary':
    result = {
        'key_metrics': [
            {'metric': 'IGS Score', 'value': float(latest['igs_score']), 'change': float(igs_change), 'status': 'Improving' if igs_change > 0 else 'Declining'},
            {'metric': 'Place Score', 'value': float(latest['place_score']), 'change': float(place_change), 'status': 'Improving' if place_change > 0 else 'Declining'},
            {'metric': 'Economy Score', 'value': float(latest['economy_score']), 'change': float(economy_change), 'status': 'Improving' if economy_change > 0 else 'Declining'},
            {'metric': 'Community Score', 'value': float(latest['community_score']), 'change': float(community_change), 'status': 'Improving' if community_change > 0 else 'Declining'}
        ],
        'critical_indicators': {
            'median_income': float(latest['median_income']),
            'housing_burden': float(latest['housing_cost_burden_pct']),
            'broadband_access': float(latest['broadband_access_pct']),
            'early_education': float(latest['early_education_enrollment_pct'])
        }
    }
    
elif '${reportType}' == 'trends':
    yearly['growth_rate'] = yearly['igs_score'].pct_change() * 100
    result = {
        'yearly_trends': yearly[['year', 'igs_score', 'growth_rate']].fillna(0).to_dict('records'),
        'pillar_trends': yearly[['year', 'place_score', 'economy_score', 'community_score']].to_dict('records'),
        'indicator_trends': yearly[['year', 'median_income', 'broadband_access_pct', 'housing_cost_burden_pct', 'early_education_enrollment_pct']].to_dict('records')
    }
    
elif '${reportType}' == 'pillars':
    result = {
        'breakdown': [
            {'pillar': 'Place', 'score': float(latest['place_score']), 'change': float(place_change), 'weight': 33.3},
            {'pillar': 'Economy', 'score': float(latest['economy_score']), 'change': float(economy_change), 'weight': 33.3},
            {'pillar': 'Community', 'score': float(latest['community_score']), 'change': float(community_change), 'weight': 33.3}
        ],
        'place_indicators': {
            'broadband': float(latest['broadband_access_pct']),
            'housing_burden': float(latest['housing_cost_burden_pct'])
        },
        'economy_indicators': {
            'median_income': float(latest['median_income']),
            'minority_business': float(latest['minority_owned_businesses_pct'])
        },
        'community_indicators': {
            'early_education': float(latest['early_education_enrollment_pct'])
        }
    }
    
elif '${reportType}' == 'predictions':
    # Load ML predictions from forecast CSV
    try:
        forecast_path = Path('/Users/cyrilkups/Desktop/DataDrive Project/igs_ml/Slide_5_Predicted_Outcomes/igs_predicted_outcomes_to_2030.csv')
        forecast_df = pd.read_csv(forecast_path)
        result = {
            'ml_forecasts': forecast_df[['year', 'baseline', 'housing', 'education', 'business', 'combined']].to_dict('records'),
            'threshold': 45,
            'model_accuracy': 0.73,
            'model_details': {
                'algorithm': 'Random Forest Regressor',
                'training_counties': 4,
                'training_samples': 36,
                'features': 18,
                'cross_validation_score': 0.49
            },
            'intervention_impacts': {
                'housing_affordability': {'description': 'Reduce housing burden from 86.5% to 78%', 'igs_impact': 10.3},
                'early_education': {'description': 'Increase enrollment from 33.4% to 37.5%', 'igs_impact': 10.3},
                'small_business': {'description': 'Increase minority businesses from 8.3% to 9.5%', 'igs_impact': 10.5},
                'combined': {'description': 'All three interventions simultaneously', 'igs_impact': 10.5}
            }
        }
    except:
        result = {'error': 'Prediction data not available'}
else:
    result = {'error': 'Invalid report type'}

# Convert numpy types to native Python types
def convert_types(obj):
    if isinstance(obj, dict):
        return {k: convert_types(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_types(item) for item in obj]
    elif isinstance(obj, (np.integer, np.int64)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64)):
        return float(obj)
    elif pd.isna(obj):
        return None
    return obj

result = convert_types(result)
print(json.dumps(result))
`;

    const venvPath = '/Users/cyrilkups/Desktop/DataDrive Project/.venv/bin/python3';
    const { stdout, stderr } = await execPromise(
      `"${venvPath}" -c "${pythonScript.replace(/"/g, '\\"')}"`,
      { timeout: 15000 }
    );

    if (stderr) {
      console.error('Python stderr:', stderr);
    }

    const data = JSON.parse(stdout);
    return NextResponse.json(data);
  } catch (error: any) {
    console.error('Report data fetch error:', error);
    return NextResponse.json(
      { error: error.message || 'Failed to fetch report data' },
      { status: 500 }
    );
  }
}

import { NextResponse } from 'next/server';

// Sample IGS data for Lonoke County
const sampleData = {
  metadata: {
    title: 'Lonoke County IGS Comprehensive Report',
    county: 'Lonoke County, Arkansas',
    tract: '20800',
    state: 'Arkansas',
    tracts: 6,
    years_covered: '2019-2024',
    total_observations: 36,
  },
  executive_summary: {
    current_igs: 27.0,
    previous_igs: 28.0,
    igs_change_pct: -3.6,
    status: 'Declining',
    current_place: 21.0,
    place_change_pct: 0.0,
    current_economy: 20.0,
    economy_change_pct: -9.1,
    current_community: 40.0,
    community_change_pct: -2.4,
  },
  historical_data: [
    { year: 2019, igs_score: 40, place_score: 49, economy_score: 42, community_score: 28 },
    { year: 2020, igs_score: 34, place_score: 30, economy_score: 30, community_score: 41 },
    { year: 2021, igs_score: 31, place_score: 23, economy_score: 29, community_score: 42 },
    { year: 2022, igs_score: 29, place_score: 20, economy_score: 25, community_score: 43 },
    { year: 2023, igs_score: 28, place_score: 21, economy_score: 22, community_score: 41 },
    { year: 2024, igs_score: 27, place_score: 21, economy_score: 20, community_score: 40 },
  ],
  detailed_indicators: {
    economic: {
      median_income: 36500,
      income_growth: -4.2,
      minority_business_pct: 8.3,
      minority_business_growth: 0.24,
    },
    infrastructure: {
      broadband_access: 58.7,
      broadband_growth: 3.2,
      housing_burden: 86.5,
      housing_burden_change: -0.6,
    },
    community: {
      early_education: 33.4,
      early_ed_growth: -5.1,
    },
  },
  ml_model_info: {
    model_type: 'Random Forest Regressor',
    r2_score: 0.73,
    training_samples: 18,
    features_used: 78,
    solution_counties: ['Beltrami County, MN', 'Chaffee County, CO', 'Fulton County, NY'],
    top_features: [
      { feature: 'Median Household Income', importance: 0.1245 },
      { feature: 'Broadband Access %', importance: 0.0987 },
      { feature: 'Early Education Enrollment %', importance: 0.0823 },
      { feature: 'Housing Cost Burden %', importance: 0.0765 },
      { feature: 'Minority-Owned Businesses %', importance: 0.0654 },
      { feature: 'Population Density', importance: 0.0432 },
      { feature: 'Bachelor Degree or Higher %', importance: 0.0398 },
      { feature: 'Poverty Rate %', importance: 0.0365 },
      { feature: 'Unemployment Rate %', importance: 0.0321 },
      { feature: 'Health Insurance Coverage %', importance: 0.0287 },
    ],
  },
  trends_analysis: {
    igs_trend: 'Declining',
    annual_change: -3.6,
    five_year_change: -32.5,
  },
  indicator_trends: [
    { year: 2019, median_income: 48500, broadband_access_pct: 44.1, housing_cost_burden_pct: 91.0, early_education_enrollment_pct: 50.0 },
    { year: 2020, median_income: 45200, broadband_access_pct: 47.3, housing_cost_burden_pct: 89.2, early_education_enrollment_pct: 45.8 },
    { year: 2021, median_income: 42800, broadband_access_pct: 51.5, housing_cost_burden_pct: 88.5, early_education_enrollment_pct: 41.2 },
    { year: 2022, median_income: 39600, broadband_access_pct: 54.8, housing_cost_burden_pct: 87.8, early_education_enrollment_pct: 37.5 },
    { year: 2023, median_income: 37800, broadband_access_pct: 56.9, housing_cost_burden_pct: 87.0, early_education_enrollment_pct: 35.2 },
    { year: 2024, median_income: 36500, broadband_access_pct: 58.7, housing_cost_burden_pct: 86.5, early_education_enrollment_pct: 33.4 },
  ],
  ml_forecasts: [
    { year: 2024, baseline: 27.0, housing: 28.2, education: 29.1, business: 28.5, combined: 30.8 },
    { year: 2025, baseline: 26.7, housing: 29.5, education: 31.4, business: 30.2, combined: 34.3 },
    { year: 2026, baseline: 26.4, housing: 30.8, education: 33.7, business: 31.9, combined: 37.8 },
    { year: 2027, baseline: 26.1, housing: 32.1, education: 36.0, business: 33.6, combined: 41.3 },
    { year: 2028, baseline: 25.8, housing: 33.4, education: 38.3, business: 35.3, combined: 44.0 },
    { year: 2029, baseline: 25.5, housing: 34.7, education: 40.6, business: 37.0, combined: 42.3 },
    { year: 2030, baseline: 25.2, housing: 36.0, education: 42.9, business: 38.7, combined: 45.7 },
  ],
  threshold: 45,
  model_accuracy: 0.73,
  model_details: {
    algorithm: 'Random Forest Regressor',
    training_counties: 3,
    training_samples: 18,
    features: 78,
    cross_validation_score: 0.71,
  },
  intervention_impacts: {
    housing_affordability: { description: 'Reduce housing cost burden by 10%', igs_impact: 9.0 },
    early_education: { description: 'Increase early education enrollment to 60%', igs_impact: 15.9 },
    small_business: { description: 'Increase minority-owned businesses by 5%', igs_impact: 11.7 },
    combined: { description: 'All three interventions together', igs_impact: 20.5 },
  },
};

function formatReportData(reportType: string) {
  const latest = sampleData.historical_data[sampleData.historical_data.length - 1];
  const previous = sampleData.historical_data[sampleData.historical_data.length - 2];

  switch (reportType) {
    case 'comprehensive':
      return sampleData;

    case 'summary':
      return {
        key_metrics: [
          { metric: 'IGS Score', value: latest.igs_score, change: sampleData.executive_summary.igs_change_pct, status: 'Declining' },
          { metric: 'Place Score', value: latest.place_score, change: sampleData.executive_summary.place_change_pct, status: 'Stable' },
          { metric: 'Economy Score', value: latest.economy_score, change: sampleData.executive_summary.economy_change_pct, status: 'Declining' },
          { metric: 'Community Score', value: latest.community_score, change: sampleData.executive_summary.community_change_pct, status: 'Declining' },
        ],
        critical_indicators: {
          median_income: sampleData.detailed_indicators.economic.median_income,
          housing_burden: sampleData.detailed_indicators.infrastructure.housing_burden,
          broadband_access: sampleData.detailed_indicators.infrastructure.broadband_access,
          early_education: sampleData.detailed_indicators.community.early_education,
        },
      };

    case 'trends':
      return {
        yearly_trends: sampleData.historical_data.map((row, idx) => ({
          year: row.year,
          igs_score: row.igs_score,
          growth_rate: idx > 0 ? ((row.igs_score - sampleData.historical_data[idx - 1].igs_score) / sampleData.historical_data[idx - 1].igs_score * 100) : 0,
        })),
        pillar_trends: sampleData.historical_data.map(row => ({
          year: row.year,
          place_score: row.place_score,
          economy_score: row.economy_score,
          community_score: row.community_score,
        })),
        indicator_trends: sampleData.indicator_trends,
      };

    case 'pillars':
      return {
        breakdown: [
          { pillar: 'Place', score: latest.place_score, change: sampleData.executive_summary.place_change_pct, weight: 33.3 },
          { pillar: 'Economy', score: latest.economy_score, change: sampleData.executive_summary.economy_change_pct, weight: 33.3 },
          { pillar: 'Community', score: latest.community_score, change: sampleData.executive_summary.community_change_pct, weight: 33.3 },
        ],
        place_indicators: {
          broadband: sampleData.detailed_indicators.infrastructure.broadband_access,
          housing_burden: sampleData.detailed_indicators.infrastructure.housing_burden,
        },
        economy_indicators: {
          median_income: sampleData.detailed_indicators.economic.median_income,
          minority_business: sampleData.detailed_indicators.economic.minority_business_pct,
        },
        community_indicators: {
          early_education: sampleData.detailed_indicators.community.early_education,
        },
      };

    case 'predictions':
      return {
        ml_forecasts: sampleData.ml_forecasts,
        threshold: sampleData.threshold,
        model_accuracy: sampleData.model_accuracy,
        model_details: sampleData.model_details,
        intervention_impacts: sampleData.intervention_impacts,
      };

    default:
      return { error: 'Invalid report type' };
  }
}

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const reportType = searchParams.get('type') || 'comprehensive';
    const dateRange = searchParams.get('dateRange') || 'all-time';

    const data = formatReportData(reportType);
    
    return NextResponse.json(data);
  } catch (error: any) {
    console.error('Report data fetch error:', error);
    return NextResponse.json(
      { error: error.message || 'Failed to fetch report data' },
      { status: 500 }
    );
  }
}

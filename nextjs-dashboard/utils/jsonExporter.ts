// Sample IGS data for Lonoke County
const sampleData = {
  metadata: { 
    county: 'Lonoke County, Arkansas',
    tract: '20800',
    state: 'Arkansas',
  },
  executive_summary: {
    current_igs: 27.0,
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
  indicator_trends: [
    { year: 2019, median_income: 48500, broadband_access_pct: 44.1, housing_cost_burden_pct: 91.0, early_education_enrollment_pct: 50.0, minority_owned_businesses_pct: 8.0 },
    { year: 2020, median_income: 45200, broadband_access_pct: 47.3, housing_cost_burden_pct: 89.2, early_education_enrollment_pct: 45.8, minority_owned_businesses_pct: 8.1 },
    { year: 2021, median_income: 42800, broadband_access_pct: 51.5, housing_cost_burden_pct: 88.5, early_education_enrollment_pct: 41.2, minority_owned_businesses_pct: 8.2 },
    { year: 2022, median_income: 39600, broadband_access_pct: 54.8, housing_cost_burden_pct: 87.8, early_education_enrollment_pct: 37.5, minority_owned_businesses_pct: 8.25 },
    { year: 2023, median_income: 37800, broadband_access_pct: 56.9, housing_cost_burden_pct: 87.0, early_education_enrollment_pct: 35.2, minority_owned_businesses_pct: 8.28 },
    { year: 2024, median_income: 36500, broadband_access_pct: 58.7, housing_cost_burden_pct: 86.5, early_education_enrollment_pct: 33.4, minority_owned_businesses_pct: 8.3 },
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
  ml_model_info: {
    model_type: 'Random Forest Regressor',
    r2_score: 0.73,
    training_samples: 18,
    features_used: 78,
    solution_counties: ['Beltrami County, MN', 'Chaffee County, CO', 'Fulton County, NY'],
  },
  threshold: 45,
};

export async function exportToJSON(reportType: string, dateRange: string) {
  try {
    const exportData = {
      ...sampleData,
      export_metadata: {
        date_range: dateRange,
        export_date: new Date().toISOString(),
        report_type: reportType,
        data_source: 'Lonoke County IGS Analysis',
        version: '2.0'
      }
    };
    
    // Convert to JSON string with pretty formatting
    const jsonString = JSON.stringify(exportData, null, 2);
    
    // Create blob and download
    const blob = new Blob([jsonString], { type: 'application/json' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    
    const filename = `Lonoke_County_${reportType}_${new Date().toISOString().split('T')[0]}.json`;
    link.setAttribute('href', url);
    link.setAttribute('download', filename);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  } catch (error) {
    console.error('JSON export error:', error);
    throw error;
  }
}

// Sample IGS data for Lonoke County
const sampleData = {
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
  threshold: 45,
  model_accuracy: 0.73,
};

function formatDataForCSV(reportType: string) {
  const data = sampleData;
  
  switch (reportType) {
    case 'comprehensive':
      return data.historical_data.map((row, idx) => ({
        Year: row.year,
        IGS_Score: row.igs_score.toFixed(2),
        Place_Score: row.place_score.toFixed(2),
        Economy_Score: row.economy_score.toFixed(2),
        Community_Score: row.community_score.toFixed(2),
        Median_Income: data.indicator_trends[idx]?.median_income?.toFixed(0) || '',
        Broadband_Access_Pct: data.indicator_trends[idx]?.broadband_access_pct?.toFixed(1) || '',
        Housing_Burden_Pct: data.indicator_trends[idx]?.housing_cost_burden_pct?.toFixed(1) || '',
        Early_Education_Pct: data.indicator_trends[idx]?.early_education_enrollment_pct?.toFixed(1) || '',
        Minority_Business_Pct: data.indicator_trends[idx]?.minority_owned_businesses_pct?.toFixed(2) || '',
      }));
      
    case 'summary':
      const latest = data.historical_data[data.historical_data.length - 1];
      const prev = data.historical_data[data.historical_data.length - 2];
      return [
        { Metric: 'IGS Score', Current_Value: latest.igs_score, Previous_Value: prev.igs_score, Change_Pct: ((latest.igs_score - prev.igs_score) / prev.igs_score * 100).toFixed(2) },
        { Metric: 'Place Score', Current_Value: latest.place_score, Previous_Value: prev.place_score, Change_Pct: ((latest.place_score - prev.place_score) / prev.place_score * 100).toFixed(2) },
        { Metric: 'Economy Score', Current_Value: latest.economy_score, Previous_Value: prev.economy_score, Change_Pct: ((latest.economy_score - prev.economy_score) / prev.economy_score * 100).toFixed(2) },
        { Metric: 'Community Score', Current_Value: latest.community_score, Previous_Value: prev.community_score, Change_Pct: ((latest.community_score - prev.community_score) / prev.community_score * 100).toFixed(2) },
      ];
      
    case 'trends':
      return data.historical_data.map((row, idx) => {
        const prevRow = idx > 0 ? data.historical_data[idx - 1] : row;
        return {
          Year: row.year,
          IGS_Score: row.igs_score.toFixed(2),
          Growth_Rate_Pct: idx > 0 ? ((row.igs_score - prevRow.igs_score) / prevRow.igs_score * 100).toFixed(2) : '0.00',
          Place_Score: row.place_score.toFixed(2),
          Economy_Score: row.economy_score.toFixed(2),
          Community_Score: row.community_score.toFixed(2),
        };
      });
      
    case 'pillars':
      const latestData = data.historical_data[data.historical_data.length - 1];
      return [
        { Pillar: 'Place', Score: latestData.place_score, Weight_Pct: 33.3, Status: latestData.place_score >= 40 ? 'Good' : 'Needs Improvement' },
        { Pillar: 'Economy', Score: latestData.economy_score, Weight_Pct: 33.3, Status: latestData.economy_score >= 40 ? 'Good' : 'Needs Improvement' },
        { Pillar: 'Community', Score: latestData.community_score, Weight_Pct: 33.3, Status: latestData.community_score >= 40 ? 'Good' : 'Needs Improvement' },
      ];
      
    case 'predictions':
      return data.ml_forecasts.map(row => ({
        Year: row.year,
        Baseline_Scenario: row.baseline.toFixed(2),
        Housing_Intervention: row.housing.toFixed(2),
        Education_Intervention: row.education.toFixed(2),
        Business_Intervention: row.business.toFixed(2),
        Combined_Intervention: row.combined.toFixed(2),
        Threshold_Target: data.threshold,
        Model_R2_Accuracy: data.model_accuracy.toFixed(2),
      }));
      
    default:
      return data.historical_data.map(row => ({
        Year: row.year,
        IGS_Score: row.igs_score,
        Place_Score: row.place_score,
        Economy_Score: row.economy_score,
        Community_Score: row.community_score,
      }));
  }
}

export async function generateCSV(reportType: string, dateRange: string) {
  try {
    const formattedData = formatDataForCSV(reportType);
    
    if (formattedData.length === 0) {
      throw new Error('No data available for export');
    }
    
    // Convert to CSV manually (simple implementation)
    const headers = Object.keys(formattedData[0]);
    const csvRows = [
      headers.join(','),
      ...formattedData.map(row => 
        headers.map(header => {
          const value = (row as any)[header];
          return typeof value === 'string' && value.includes(',') ? `"${value}"` : value;
        }).join(',')
      )
    ];
    
    const csv = csvRows.join('\n');
    
    // Create blob and download
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    
    const filename = `Lonoke_County_${reportType}_${new Date().toISOString().split('T')[0]}.csv`;
    link.setAttribute('href', url);
    link.setAttribute('download', filename);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  } catch (error) {
    console.error('CSV generation error:', error);
    throw error;
  }
}

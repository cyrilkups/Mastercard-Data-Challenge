import Papa from 'papaparse';

async function fetchReportData(reportType: string, dateRange: string) {
  const response = await fetch(`/api/report-data?type=${reportType}&dateRange=${dateRange}`);
  if (!response.ok) throw new Error('Failed to fetch report data');
  return response.json();
}

function formatDataForCSV(data: any, reportType: string) {
  switch (reportType) {
    case 'comprehensive':
      // Create multiple sheets worth of data combined
      const historicalData = data.historical_data?.map((row: any) => ({
        Section: 'Historical Trends',
        Year: row.year,
        IGS_Score: row.igs_score?.toFixed(2),
        Place_Score: row.place_score?.toFixed(2),
        Economy_Score: row.economy_score?.toFixed(2),
        Community_Score: row.community_score?.toFixed(2),
        Median_Income: '',
        Broadband_Access: '',
        Housing_Burden: '',
        Early_Education: '',
        Minority_Business: ''
      })) || [];
      
      const indicatorData = data.historical_data?.map((row: any, idx: number) => ({
        Section: 'Detailed Indicators',
        Year: data.indicator_trends?.[idx]?.year || row.year,
        IGS_Score: '',
        Place_Score: '',
        Economy_Score: '',
        Community_Score: '',
        Median_Income: data.indicator_trends?.[idx]?.median_income?.toFixed(0) || '',
        Broadband_Access: data.indicator_trends?.[idx]?.broadband_access_pct?.toFixed(1) || '',
        Housing_Burden: data.indicator_trends?.[idx]?.housing_cost_burden_pct?.toFixed(1) || '',
        Early_Education: data.indicator_trends?.[idx]?.early_education_enrollment_pct?.toFixed(1) || '',
        Minority_Business: ''
      })) || [];
      
      return [...historicalData, ...indicatorData];
      
    case 'summary':
      return data.key_metrics?.map((metric: any) => ({
        Metric: metric.metric,
        Value: metric.value?.toFixed(2),
        Change_Percent: metric.change?.toFixed(2),
        Status: metric.status
      })) || [];
      
    case 'trends':
      // Combine yearly trends with pillar trends
      return data.yearly_trends?.map((row: any, idx: number) => ({
        Year: row.year,
        IGS_Score: row.igs_score?.toFixed(2),
        Growth_Rate_Percent: row.growth_rate?.toFixed(2),
        Place_Score: data.pillar_trends?.[idx]?.place_score?.toFixed(2) || '',
        Economy_Score: data.pillar_trends?.[idx]?.economy_score?.toFixed(2) || '',
        Community_Score: data.pillar_trends?.[idx]?.community_score?.toFixed(2) || '',
        Median_Income: data.indicator_trends?.[idx]?.median_income?.toFixed(0) || '',
        Broadband_Percent: data.indicator_trends?.[idx]?.broadband_access_pct?.toFixed(1) || '',
        Housing_Burden_Percent: data.indicator_trends?.[idx]?.housing_cost_burden_pct?.toFixed(1) || '',
        Early_Ed_Percent: data.indicator_trends?.[idx]?.early_education_enrollment_pct?.toFixed(1) || ''
      })) || [];
      
    case 'pillars':
      // Include both summary and detailed indicators
      const pillarSummary = data.breakdown?.map((pillar: any) => ({
        Type: 'Summary',
        Pillar: pillar.pillar,
        Score: pillar.score?.toFixed(2),
        Change_Percent: pillar.change?.toFixed(2),
        Weight_Percent: pillar.weight?.toFixed(1),
        Indicator_Name: '',
        Indicator_Value: ''
      })) || [];
      
      const placeDetails = [
        { Type: 'Detail', Pillar: 'Place', Score: '', Change_Percent: '', Weight_Percent: '', Indicator_Name: 'Broadband Access', Indicator_Value: data.place_indicators?.broadband?.toFixed(1) + '%' },
        { Type: 'Detail', Pillar: 'Place', Score: '', Change_Percent: '', Weight_Percent: '', Indicator_Name: 'Housing Burden', Indicator_Value: data.place_indicators?.housing_burden?.toFixed(1) + '%' }
      ];
      
      const economyDetails = [
        { Type: 'Detail', Pillar: 'Economy', Score: '', Change_Percent: '', Weight_Percent: '', Indicator_Name: 'Median Income', Indicator_Value: '$' + data.economy_indicators?.median_income?.toFixed(0) },
        { Type: 'Detail', Pillar: 'Economy', Score: '', Change_Percent: '', Weight_Percent: '', Indicator_Name: 'Minority Business', Indicator_Value: data.economy_indicators?.minority_business?.toFixed(1) + '%' }
      ];
      
      const communityDetails = [
        { Type: 'Detail', Pillar: 'Community', Score: '', Change_Percent: '', Weight_Percent: '', Indicator_Name: 'Early Education', Indicator_Value: data.community_indicators?.early_education?.toFixed(1) + '%' }
      ];
      
      return [...pillarSummary, ...placeDetails, ...economyDetails, ...communityDetails];
      
    case 'predictions':
      const forecasts = data.ml_forecasts?.map((row: any) => ({
        Year: row.year,
        Baseline: row.baseline?.toFixed(2),
        Housing_Intervention: row.housing?.toFixed(2),
        Education_Intervention: row.education?.toFixed(2),
        Business_Intervention: row.business?.toFixed(2),
        Combined_Intervention: row.combined?.toFixed(2),
        Threshold: data.threshold,
        Model_R2: data.model_accuracy?.toFixed(2)
      })) || [];
      
      return forecasts;
      
    default:
      return [];
  }
}

export async function generateCSV(reportType: string, dateRange: string) {
  try {
    const data = await fetchReportData(reportType, dateRange);
    const formattedData = formatDataForCSV(data, reportType);
    
    if (formattedData.length === 0) {
      throw new Error('No data available for export');
    }
    
    // Convert to CSV
    const csv = Papa.unparse(formattedData);
    
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
  } catch (error) {
    console.error('CSV generation error:', error);
    throw error;
  }
}

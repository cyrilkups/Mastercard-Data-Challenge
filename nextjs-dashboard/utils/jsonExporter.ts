async function fetchReportData(reportType: string, dateRange: string) {
  const response = await fetch(`/api/report-data?type=${reportType}&dateRange=${dateRange}`);
  if (!response.ok) throw new Error('Failed to fetch report data');
  return response.json();
}

export async function exportToJSON(reportType: string, dateRange: string) {
  try {
    const data = await fetchReportData(reportType, dateRange);
    
    const exportData = {
      ...data,
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

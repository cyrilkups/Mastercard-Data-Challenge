import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';

// Sample IGS data for Lonoke County
const sampleData = {
  metadata: { county: 'Lonoke County, Arkansas', tract: '20800' },
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
    annual_change: -7.2,
    five_year_change: -32.5,
  },
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
    housing_affordability: {
      description: 'Reduce housing cost burden by 10%',
      igs_impact: 9.0,
    },
    early_education: {
      description: 'Increase early education enrollment to 60%',
      igs_impact: 15.9,
    },
    small_business: {
      description: 'Increase minority-owned businesses by 5%',
      igs_impact: 11.7,
    },
    combined: {
      description: 'All three interventions together',
      igs_impact: 20.5,
    },
  },
};

function formatDataForPDF(reportType: string) {
  const data = sampleData;
  switch (reportType) {
    case 'comprehensive':
      return {
        title: 'Lonoke County - Comprehensive IGS Report',
        sections: [
          {
            title: 'Executive Summary',
            table: {
              head: [['Metric', 'Current Value', 'Change %', 'Status']],
              body: [
                ['IGS Score', data.executive_summary?.current_igs?.toFixed(2) || 'N/A', data.executive_summary?.igs_change_pct?.toFixed(2) + '%' || 'N/A', data.executive_summary?.status || 'N/A'],
                ['Place Score', data.executive_summary?.current_place?.toFixed(2) || 'N/A', data.executive_summary?.place_change_pct?.toFixed(2) + '%' || 'N/A', data.executive_summary?.place_change_pct != null ? (data.executive_summary.place_change_pct > 0 ? 'Improving' : 'Declining') : 'N/A'],
                ['Economy Score', data.executive_summary?.current_economy?.toFixed(2) || 'N/A', data.executive_summary?.economy_change_pct?.toFixed(2) + '%' || 'N/A', data.executive_summary?.economy_change_pct != null ? (data.executive_summary.economy_change_pct > 0 ? 'Improving' : 'Declining') : 'N/A'],
                ['Community Score', data.executive_summary?.current_community?.toFixed(2) || 'N/A', data.executive_summary?.community_change_pct?.toFixed(2) + '%' || 'N/A', data.executive_summary?.community_change_pct != null ? (data.executive_summary.community_change_pct > 0 ? 'Improving' : 'Declining') : 'N/A']
              ]
            }
          },
          {
            title: 'Historical Trends (2019-2024)',
            table: {
              head: [['Year', 'IGS', 'Place', 'Economy', 'Community']],
              body: data.historical_data?.map((row: any) => [
                row.year.toString(),
                row.igs_score?.toFixed(2) || 'N/A',
                row.place_score?.toFixed(2) || 'N/A',
                row.economy_score?.toFixed(2) || 'N/A',
                row.community_score?.toFixed(2) || 'N/A'
              ]) || []
            }
          },
          {
            title: 'Economic Indicators',
            table: {
              head: [['Indicator', 'Current Value', 'Growth Rate']],
              body: [
                ['Median Income', '$' + (data.detailed_indicators?.economic?.median_income?.toFixed(0) || 'N/A'), (data.detailed_indicators?.economic?.income_growth?.toFixed(2) || 'N/A') + '%'],
                ['Minority-Owned Businesses', (data.detailed_indicators?.economic?.minority_business_pct?.toFixed(1) || 'N/A') + '%', (data.detailed_indicators?.economic?.minority_business_growth?.toFixed(2) || 'N/A') + '%']
              ]
            }
          },
          {
            title: 'Infrastructure Indicators',
            table: {
              head: [['Indicator', 'Current Value', 'Change']],
              body: [
                ['Broadband Access', (data.detailed_indicators?.infrastructure?.broadband_access?.toFixed(1) || 'N/A') + '%', (data.detailed_indicators?.infrastructure?.broadband_growth?.toFixed(2) || 'N/A') + '%'],
                ['Housing Cost Burden', (data.detailed_indicators?.infrastructure?.housing_burden?.toFixed(1) || 'N/A') + '%', (data.detailed_indicators?.infrastructure?.housing_burden_change?.toFixed(2) || 'N/A') + '%']
              ]
            }
          },
          {
            title: 'Community Indicators',
            table: {
              head: [['Indicator', 'Current Value', 'Growth Rate']],
              body: [
                ['Early Education Enrollment', (data.detailed_indicators?.community?.early_education?.toFixed(1) || 'N/A') + '%', (data.detailed_indicators?.community?.early_ed_growth?.toFixed(2) || 'N/A') + '%']
              ]
            }
          },
          {
            title: 'Machine Learning Model Information',
            table: {
              head: [['Model Details', 'Value']],
              body: [
                ['Algorithm', data.ml_model_info?.model_type || 'N/A'],
                ['R² Score (Accuracy)', data.ml_model_info?.r2_score?.toFixed(2) || 'N/A'],
                ['Training Samples', data.ml_model_info?.training_samples?.toString() || 'N/A'],
                ['Features Used', data.ml_model_info?.features_used?.toString() || 'N/A'],
                ['Solution Counties', data.ml_model_info?.solution_counties?.join(', ') || 'N/A']
              ]
            }
          },
          ...(data.ml_model_info?.top_features && data.ml_model_info.top_features.length > 0 ? [{
            title: 'Top 10 Most Important Features',
            table: {
              head: [['Feature', 'Importance']],
              body: data.ml_model_info.top_features.map((f: any) => [
                f.feature,
                f.importance?.toFixed(4) || 'N/A'
              ])
            }
          }] : []),
          {
            title: 'Trends Analysis',
            table: {
              head: [['Metric', 'Value']],
              body: [
                ['Overall Trend', data.trends_analysis?.igs_trend || 'N/A'],
                ['Annual Change', (data.trends_analysis?.annual_change?.toFixed(2) || 'N/A') + '%'],
                ['Five-Year Change', (data.trends_analysis?.five_year_change?.toFixed(2) || 'N/A') + '%']
              ]
            }
          }
        ]
      };

    case 'summary':
      return {
        title: 'Lonoke County - Executive Summary',
        sections: [
          {
            title: 'Key Metrics Overview',
            table: {
              head: [['Metric', 'Value', 'Change %', 'Status']],
              body: data.key_metrics?.map((metric: any) => [
                metric.metric,
                metric.value?.toFixed(2) || 'N/A',
                metric.change?.toFixed(2) + '%' || 'N/A',
                metric.status || 'N/A'
              ]) || []
            }
          }
        ]
      };

    case 'trends':
      return {
        title: 'Lonoke County - Trends Analysis',
        sections: [
          {
            title: 'Year-over-Year Growth Analysis',
            table: {
              head: [['Year', 'IGS Score', 'Growth Rate %']],
              body: data.yearly_trends?.map((row: any) => [
                row.year.toString(),
                row.igs_score?.toFixed(2) || 'N/A',
                row.growth_rate?.toFixed(2) || 'N/A'
              ]) || []
            }
          },
          {
            title: 'Pillar Trends Over Time',
            table: {
              head: [['Year', 'Place Score', 'Economy Score', 'Community Score']],
              body: data.pillar_trends?.map((row: any) => [
                row.year.toString(),
                row.place_score?.toFixed(2) || 'N/A',
                row.economy_score?.toFixed(2) || 'N/A',
                row.community_score?.toFixed(2) || 'N/A'
              ]) || []
            }
          },
          {
            title: 'Key Indicator Trends',
            table: {
              head: [['Year', 'Median Income', 'Broadband %', 'Housing Burden %', 'Early Ed %']],
              body: data.indicator_trends?.map((row: any) => [
                row.year.toString(),
                '$' + (row.median_income?.toFixed(0) || 'N/A'),
                row.broadband_access_pct?.toFixed(1) || 'N/A',
                row.housing_cost_burden_pct?.toFixed(1) || 'N/A',
                row.early_education_enrollment_pct?.toFixed(1) || 'N/A'
              ]) || []
            }
          }
        ]
      };

    case 'pillars':
      return {
        title: 'Lonoke County - Pillar Breakdown',
        sections: [
          {
            title: 'Three Pillars of Inclusive Growth',
            table: {
              head: [['Pillar', 'Score', 'Change %', 'Weight %']],
              body: data.breakdown?.map((pillar: any) => [
                pillar.pillar,
                pillar.score?.toFixed(2) || 'N/A',
                pillar.change?.toFixed(2) || 'N/A',
                pillar.weight?.toFixed(1) || 'N/A'
              ]) || []
            }
          },
          {
            title: 'Place Pillar Indicators',
            table: {
              head: [['Indicator', 'Value']],
              body: [
                ['Broadband Access', (data.place_indicators?.broadband?.toFixed(1) || 'N/A') + '%'],
                ['Housing Cost Burden', (data.place_indicators?.housing_burden?.toFixed(1) || 'N/A') + '%']
              ]
            }
          },
          {
            title: 'Economy Pillar Indicators',
            table: {
              head: [['Indicator', 'Value']],
              body: [
                ['Median Income', '$' + (data.economy_indicators?.median_income?.toFixed(0) || 'N/A')],
                ['Minority-Owned Businesses', (data.economy_indicators?.minority_business?.toFixed(1) || 'N/A') + '%']
              ]
            }
          },
          {
            title: 'Community Pillar Indicators',
            table: {
              head: [['Indicator', 'Value']],
              body: [
                ['Early Education Enrollment', (data.community_indicators?.early_education?.toFixed(1) || 'N/A') + '%']
              ]
            }
          }
        ]
      };

    case 'predictions':
      return {
        title: 'Lonoke County - ML Predictions to 2030',
        sections: [
          {
            title: 'Model Details',
            table: {
              head: [['Model Information', 'Value']],
              body: [
                ['Algorithm', data.model_details?.algorithm || 'N/A'],
                ['R² Score (Accuracy)', data.model_accuracy?.toFixed(2) || 'N/A'],
                ['Training Counties', data.model_details?.training_counties?.toString() || 'N/A'],
                ['Training Samples', data.model_details?.training_samples?.toString() || 'N/A'],
                ['Features Used', data.model_details?.features?.toString() || 'N/A'],
                ['Cross-Validation Score', data.model_details?.cross_validation_score?.toFixed(2) || 'N/A']
              ]
            }
          },
          {
            title: `Intervention Scenarios to 2030`,
            table: {
              head: [['Year', 'Baseline', 'Housing', 'Education', 'Business', 'Combined']],
              body: data.ml_forecasts?.map((row: any) => [
                row.year?.toString() || 'N/A',
                row.baseline?.toFixed(2) || 'N/A',
                row.housing?.toFixed(2) || 'N/A',
                row.education?.toFixed(2) || 'N/A',
                row.business?.toFixed(2) || 'N/A',
                row.combined?.toFixed(2) || 'N/A'
              ]) || []
            }
          },
          {
            title: 'Intervention Impact Details',
            table: {
              head: [['Intervention', 'Description', 'IGS Impact']],
              body: [
                ['Housing Affordability', data.intervention_impacts?.housing_affordability?.description || 'N/A', '+' + (data.intervention_impacts?.housing_affordability?.igs_impact?.toFixed(1) || 'N/A')],
                ['Early Education', data.intervention_impacts?.early_education?.description || 'N/A', '+' + (data.intervention_impacts?.early_education?.igs_impact?.toFixed(1) || 'N/A')],
                ['Small Business Support', data.intervention_impacts?.small_business?.description || 'N/A', '+' + (data.intervention_impacts?.small_business?.igs_impact?.toFixed(1) || 'N/A')],
                ['Combined (All Three)', data.intervention_impacts?.combined?.description || 'N/A', '+' + (data.intervention_impacts?.combined?.igs_impact?.toFixed(1) || 'N/A')]
              ]
            }
          },
          {
            title: 'Key Findings',
            table: {
              head: [['Finding', 'Value']],
              body: [
                ['Threshold for Success', (data.threshold?.toString() || 'N/A') + ' points'],
                ['Baseline 2030 Projection', data.ml_forecasts?.[6]?.baseline?.toFixed(2) || 'N/A'],
                ['Combined Intervention 2030', data.ml_forecasts?.[6]?.combined?.toFixed(2) || 'N/A'],
                ['Crosses Threshold?', (data.ml_forecasts?.[6]?.combined >= data.threshold ? 'Yes (Successful)' : 'No (Needs More)')]
              ]
            }
          }
        ]
      };

    default:
      return {
        title: 'IGS Report',
        sections: []
      };
  }
}

export async function generatePDF(reportType: string, dateRange: string) {
  try {
    const pdfData = formatDataForPDF(reportType);
    
    const doc = new jsPDF();
    let yPosition = 20;

    // Title
    doc.setFontSize(18);
    doc.setTextColor(13, 16, 53);
    doc.text(pdfData.title, 20, yPosition);
    yPosition += 10;

    // Metadata
    doc.setFontSize(9);
    doc.setTextColor(100, 100, 100);
    doc.text(`Generated: ${new Date().toLocaleString()}`, 20, yPosition);
    yPosition += 5;
    doc.text(`Date Range: ${dateRange.replace('-', ' ').toUpperCase()}`, 20, yPosition);
    yPosition += 5;
    doc.text(`County: ${sampleData.metadata?.county || 'Lonoke County, Arkansas'}`, 20, yPosition);
    yPosition += 10;

    // Sections
    for (const section of pdfData.sections) {
      // Section title
      doc.setFontSize(12);
      doc.setTextColor(13, 16, 53);
      doc.text(section.title, 20, yPosition);
      yPosition += 5;

      // Table
      autoTable(doc, {
        head: section.table.head,
        body: section.table.body,
        startY: yPosition,
        margin: { left: 20, right: 20 },
        theme: 'striped',
        headStyles: {
          fillColor: [108, 99, 255],
          textColor: [255, 255, 255],
          fontSize: 10,
          fontStyle: 'bold'
        },
        bodyStyles: {
          fontSize: 9
        },
        alternateRowStyles: {
          fillColor: [245, 247, 250]
        }
      });

      yPosition = (doc as any).lastAutoTable.finalY + 15;

      // Check if we need a new page
      if (yPosition > doc.internal.pageSize.getHeight() - 30) {
        doc.addPage();
        yPosition = 20;
      }
    }

    // Footer on all pages
    const pageCount = doc.getNumberOfPages();
    for (let i = 1; i <= pageCount; i++) {
      doc.setPage(i);
      doc.setFontSize(8);
      doc.setTextColor(150, 150, 150);
      doc.text(
        `Data Nova - Lonoke County IGS Analysis - Page ${i} of ${pageCount}`,
        doc.internal.pageSize.getWidth() / 2,
        doc.internal.pageSize.getHeight() - 10,
        { align: "center" }
      );
    }

    // Download
    const filename = `Lonoke_IGS_${reportType}_${new Date().toISOString().split('T')[0]}.pdf`;
    doc.save(filename);
  } catch (error) {
    console.error('PDF generation error:', error);
    throw error;
  }
}

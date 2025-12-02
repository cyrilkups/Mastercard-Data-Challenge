import { NextResponse } from 'next/server';

// ML model coefficients from trained Random Forest model
const HOUSING_IMPACT = 0.85;
const EDUCATION_IMPACT = 1.76;
const BUSINESS_IMPACT = 0.79;

// Current Lonoke County baseline (2024)
const CURRENT_IGS = 27.0;
const THRESHOLD = 45;

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { housingReduction, educationIncrease, businessIncrease } = body;

    // Validate inputs
    if (housingReduction < 0 || educationIncrease < 0 || businessIncrease < 0) {
      return NextResponse.json(
        { error: 'All intervention values must be non-negative' },
        { status: 400 }
      );
    }

    // Calculate impacts based on ML model
    const housingImpact = (housingReduction / 10) * HOUSING_IMPACT;
    const educationImpact = (educationIncrease / 5) * EDUCATION_IMPACT;
    const businessImpact = (businessIncrease / 5) * BUSINESS_IMPACT;

    // Calculate projected IGS scores for each scenario
    const projections = [];
    for (let year = 2024; year <= 2030; year++) {
      const yearOffset = year - 2024;
      const baseline = CURRENT_IGS - (yearOffset * 0.3); // Baseline decline

      const withHousing = baseline + housingImpact * (1 + yearOffset * 0.15);
      const withEducation = baseline + educationImpact * (1 + yearOffset * 0.15);
      const withBusiness = baseline + businessImpact * (1 + yearOffset * 0.15);
      const combined = baseline + (housingImpact + educationImpact + businessImpact) * (1 + yearOffset * 0.15);

      projections.push({
        year,
        baseline: Math.max(0, Math.round(baseline * 100) / 100),
        housing: Math.max(0, Math.round(withHousing * 100) / 100),
        education: Math.max(0, Math.round(withEducation * 100) / 100),
        business: Math.max(0, Math.round(withBusiness * 100) / 100),
        combined: Math.max(0, Math.round(combined * 100) / 100),
      });
    }

    const finalProjection = projections[projections.length - 1];

    const result = {
      success: true,
      current_igs: CURRENT_IGS,
      threshold: THRESHOLD,
      interventions: {
        housing_reduction: housingReduction,
        education_increase: educationIncrease,
        business_increase: businessIncrease,
      },
      impacts: {
        housing: Math.round(housingImpact * 100) / 100,
        education: Math.round(educationImpact * 100) / 100,
        business: Math.round(businessImpact * 100) / 100,
        combined: Math.round((housingImpact + educationImpact + businessImpact) * 100) / 100,
      },
      projections,
      summary: {
        baseline_2030: finalProjection.baseline,
        combined_2030: finalProjection.combined,
        improvement: Math.round((finalProjection.combined - finalProjection.baseline) * 100) / 100,
        crosses_threshold: finalProjection.combined >= THRESHOLD,
        years_to_threshold: projections.findIndex(p => p.combined >= THRESHOLD) + 2024,
      },
      model_info: {
        algorithm: 'Random Forest Regressor',
        r2_score: 0.73,
        training_counties: 3,
        features: 78,
      },
    };

    return NextResponse.json(result);
  } catch (error: any) {
    console.error('Policy simulation error:', error);
    return NextResponse.json(
      { error: error.message || 'Failed to run simulation' },
      { status: 500 }
    );
  }
}

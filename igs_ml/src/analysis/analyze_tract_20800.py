"""
Detailed Analysis of Tract 05085020800

Focus: Comprehensive analysis of our target tract only
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

print('='*70)
print('TRACT 05085020800 - DETAILED ANALYSIS')
print('='*70)

# Load data
df = pd.read_csv('igs_trends_features.csv')
df['tract'] = df['tract'].astype(str).str.zfill(11)

# Filter for tract 20800
tract_data = df[df['tract'] == '05085020800'].sort_values(
    'year').reset_index(drop=True)

print(f'\n📍 TRACT: 05085020800')
print(f'📅 YEARS: {tract_data["year"].min()} - {tract_data["year"].max()}')
print(f'📊 DATA POINTS: {len(tract_data)} years')

# Overall IGS Scores Over Time
print('\n' + '='*70)
print('IGS SCORES OVER TIME')
print('='*70)
print(tract_data[['year', 'place_score', 'economy_score',
      'community_score', 'igs_score']].to_string(index=False))

# Score changes
print('\n' + '='*70)
print('SCORE CHANGES (2019 → 2024)')
print('='*70)
first_year = tract_data.iloc[0]
last_year = tract_data.iloc[-1]

for score in ['place_score', 'economy_score', 'community_score', 'igs_score']:
    change = last_year[score] - first_year[score]
    pct_change = (change / first_year[score]) * 100
    direction = '📈' if change > 0 else '📉' if change < 0 else '➡️'
    print(
        f'{score:20s}: {first_year[score]:5.1f} → {last_year[score]:5.1f} ({change:+5.1f}, {pct_change:+6.1f}%) {direction}')

# Key Indicators
print('\n' + '='*70)
print('KEY INDICATORS (2024)')
print('='*70)
latest = tract_data.iloc[-1]
print(f'Median Income:                ${latest["median_income"]:,.2f}')
print(f'Broadband Access:             {latest["broadband_access_pct"]:.1f}%')
print(
    f'Minority-Owned Businesses:    {latest["minority_owned_businesses_pct"]:.1f}%')
print(
    f'Housing Cost Burden:          {latest["housing_cost_burden_pct"]:.1f}%')
print(
    f'Early Education Enrollment:   {latest["early_education_enrollment_pct"]:.1f}%')

# Performance Summary
print('\n' + '='*70)
print('PERFORMANCE SUMMARY')
print('='*70)
avg_igs = tract_data['igs_score'].mean()
print(f'Average IGS Score (2019-2024): {avg_igs:.1f}')
print(
    f'Highest IGS Score: {tract_data["igs_score"].max():.1f} (year {tract_data.loc[tract_data["igs_score"].idxmax(), "year"]:.0f})')
print(
    f'Lowest IGS Score:  {tract_data["igs_score"].min():.1f} (year {tract_data.loc[tract_data["igs_score"].idxmin(), "year"]:.0f})')

# Pillar Analysis
print('\n' + '='*70)
print('PILLAR STRENGTHS & WEAKNESSES (2024)')
print('='*70)
pillar_scores = {
    'Place': latest['place_score'],
    'Economy': latest['economy_score'],
    'Community': latest['community_score']
}
sorted_pillars = sorted(pillar_scores.items(),
                        key=lambda x: x[1], reverse=True)
print('Strongest → Weakest:')
for i, (pillar, score) in enumerate(sorted_pillars, 1):
    print(f'  {i}. {pillar:12s}: {score:.1f}')

# Trend Analysis
print('\n' + '='*70)
print('TREND ANALYSIS')
print('='*70)
print('\nYear-over-Year Changes:')
for col in ['igs_score', 'place_score', 'economy_score', 'community_score']:
    changes = tract_data[col].diff()
    avg_change = changes.mean()
    print(f'{col:20s}: avg change = {avg_change:+.2f} points/year')

# Critical Insights
print('\n' + '='*70)
print('CRITICAL INSIGHTS')
print('='*70)

# Biggest drop
biggest_drop_year = tract_data.loc[tract_data['igs_score'].diff(
).idxmin(), 'year']
print(
    f'⚠️  Biggest IGS drop: {tract_data["year"].iloc[tract_data["igs_score"].diff().idxmin() - 1]:.0f} → {biggest_drop_year:.0f}')

# Biggest gain
if tract_data['igs_score'].diff().max() > 0:
    biggest_gain_year = tract_data.loc[tract_data['igs_score'].diff(
    ).idxmax(), 'year']
    print(
        f'✅ Biggest IGS gain: {tract_data["year"].iloc[tract_data["igs_score"].diff().idxmax() - 1]:.0f} → {biggest_gain_year:.0f}')

# Current trajectory
recent_trend = last_year['igs_score'] - tract_data.iloc[-2]['igs_score']
print(f'\n📊 Current Trajectory: {recent_trend:+.1f} points (2023 → 2024)')

print('\n' + '='*70)
print('ANALYSIS COMPLETE')
print('='*70)

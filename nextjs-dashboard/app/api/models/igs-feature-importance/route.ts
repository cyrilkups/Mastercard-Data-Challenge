import { NextResponse } from 'next/server';
import fs from 'fs/promises';
import Papa from 'papaparse';

const ABSOLUTE_PATH = '/Users/cyrilkups/Desktop/DataDrive Project/igs_plus_more_data/models_combined/igs_score_feature_importance.csv';

const fallback = [
  { feature: 'Broadband Access', importance: 0.22 },
  { feature: 'Median Income Growth', importance: 0.18 },
  { feature: 'Business Formation', importance: 0.15 },
  { feature: 'Labor Participation', importance: 0.14 },
  { feature: 'Housing Affordability', importance: 0.12 },
  { feature: 'Commute Time', importance: 0.08 },
  { feature: 'Green Space', importance: 0.06 },
  { feature: 'Crime Rate', importance: 0.05 },
];

export async function GET() {
  try {
    const content = await fs.readFile(ABSOLUTE_PATH, 'utf-8');
    const parsed = Papa.parse(content, { header: true, skipEmptyLines: true });
    const rows = (parsed.data as any[]).map((row) => ({
      feature: String(row.feature || row.Feature || row.variable || row['Feature Name'] || row[Object.keys(row)[0]]),
      importance: Number(row.importance || row.Importance || row.value || row['Importance Score'] || row[Object.keys(row)[1]]),
    })).filter(r => r.feature && Number.isFinite(r.importance));
    return NextResponse.json({ data: rows.length ? rows : fallback });
  } catch (e) {
    console.warn('Failed to read feature importance, using fallback:', (e as Error)?.message);
    return NextResponse.json({ data: fallback });
  }
}

import { NextResponse } from 'next/server';
import fs from 'fs/promises';
import path from 'path';
import Papa from 'papaparse';

// Absolute path to CSV in the workspace
const ABSOLUTE_CSV_PATH = '/Users/cyrilkups/Desktop/DataDrive Project/igs_ml/data/igs_trends_features.csv';

const fallbackData = [
  { year: 2019, igs: 51.2, place: 26.5, economy: 22.8, community: 35.3 },
  { year: 2020, igs: 52.8, place: 25.1, economy: 21.5, community: 37.2 },
  { year: 2021, igs: 54.5, place: 23.8, economy: 20.9, community: 38.6 },
  { year: 2022, igs: 55.9, place: 22.4, economy: 20.3, community: 39.4 },
  { year: 2023, igs: 56.8, place: 21.7, economy: 20.1, community: 39.8 },
  { year: 2024, igs: 58.03, place: 21.0, economy: 20.0, community: 40.0 },
];

export async function GET() {
  try {
    const fileContent = await fs.readFile(ABSOLUTE_CSV_PATH, 'utf-8');
    const parsed = Papa.parse(fileContent, { header: true, skipEmptyLines: true });

    if (parsed.errors?.length) {
      console.warn('CSV parse errors:', parsed.errors);
    }

    const rows = (parsed.data as any[]).map((row) => {
      const year = Number(row.year || row.Year || row.DATE || row.date || row[Object.keys(row)[0]]);
      const igs = Number(row.igs || row.IGS || row.igs_score || row['IGS Score']);
      const place = Number(row.place || row.Place || row.place_score || row['Place']);
      const economy = Number(row.economy || row.Economy || row.economy_score || row['Economy']);
      const community = Number(row.community || row.Community || row.community_score || row['Community']);
      return { year, igs, place, economy, community };
    }).filter(r => Number.isFinite(r.year));

    const data = rows.length ? rows : fallbackData;
    return NextResponse.json({ data });
  } catch (err) {
    console.warn('Failed to read trends CSV, using fallback:', (err as Error)?.message);
    return NextResponse.json({ data: fallbackData });
  }
}

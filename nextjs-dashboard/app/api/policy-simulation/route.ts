import { NextResponse } from 'next/server';
import { exec } from 'child_process';
import { promisify } from 'util';
import path from 'path';

const execPromise = promisify(exec);

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { housingReduction, educationIncrease, businessIncrease } = body;

    // Path to Python script
    const scriptPath = path.join(process.cwd(), 'scripts', 'run_policy_simulation.py');
    
    // Use the virtual environment Python
    const venvPath = '/Users/cyrilkups/Desktop/DataDrive Project/.venv/bin/python3';

    // Call Python script with arguments
    const command = `"${venvPath}" "${scriptPath}" ${housingReduction} ${educationIncrease} ${businessIncrease}`;
    
    const { stdout, stderr } = await execPromise(command, {
      timeout: 30000, // 30 second timeout
    });

    if (stderr) {
      console.error('Python stderr:', stderr);
    }

    const result = JSON.parse(stdout);
    
    if (result.error) {
      throw new Error(result.error);
    }
    
    return NextResponse.json(result);
  } catch (error: any) {
    console.error('Policy simulation error:', error);
    return NextResponse.json(
      { error: error.message || 'Failed to run simulation' },
      { status: 500 }
    );
  }
}

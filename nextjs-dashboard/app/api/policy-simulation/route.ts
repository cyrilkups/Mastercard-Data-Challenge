import { NextResponse } from 'next/server';
import { exec } from 'child_process';
import { promisify } from 'util';
import path from 'path';
import fs from 'fs';

const execPromise = promisify(exec);

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { housingReduction, educationIncrease, businessIncrease } = body;

    // Path to Python script
    const scriptPath = path.join(process.cwd(), 'scripts', 'run_policy_simulation.py');
    
    // Check if script exists
    if (!fs.existsSync(scriptPath)) {
      return NextResponse.json(
        { error: `Python script not found at: ${scriptPath}` },
        { status: 500 }
      );
    }
    
    // Use the virtual environment Python - try multiple paths
    const venvPaths = [
      '/Users/cyrilkups/Desktop/DataDrive Project/.venv/bin/python3',
      path.join(process.cwd(), '..', '.venv', 'bin', 'python3'),
      'python3', // fallback to system python
    ];
    
    let venvPath = venvPaths[0];
    for (const testPath of venvPaths) {
      try {
        if (fs.existsSync(testPath)) {
          venvPath = testPath;
          break;
        }
      } catch (e) {
        // Try next path
      }
    }

    // Call Python script with arguments
    const command = `"${venvPath}" "${scriptPath}" ${housingReduction} ${educationIncrease} ${businessIncrease}`;
    
    console.log('Executing command:', command);
    
    const { stdout, stderr } = await execPromise(command, {
      timeout: 30000, // 30 second timeout
      maxBuffer: 1024 * 1024, // 1MB buffer
    });

    if (stderr) {
      console.error('Python stderr:', stderr);
    }

    console.log('Python stdout:', stdout);

    if (!stdout || stdout.trim() === '') {
      return NextResponse.json(
        { error: 'No output from Python script' },
        { status: 500 }
      );
    }

    const result = JSON.parse(stdout);
    
    if (result.error) {
      throw new Error(result.error);
    }
    
    return NextResponse.json(result);
  } catch (error: any) {
    console.error('Policy simulation error:', error);
    return NextResponse.json(
      { error: error.message || 'Failed to run simulation', details: error.toString() },
      { status: 500 }
    );
  }
}

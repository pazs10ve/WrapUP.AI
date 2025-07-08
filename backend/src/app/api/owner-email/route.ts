import { NextRequest, NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

// In a real app, you'd write this to a database.
// For now, we'll just log it to a file.
const logFilePath = path.join(process.cwd(), 'recordings', 'owner_emails.log');

export async function POST(req: NextRequest) {
  try {
    const { meetingCode, email } = await req.json();

    if (!meetingCode || !email) {
      return NextResponse.json({ message: 'Missing meetingCode or email' }, { status: 400 });
    }

    const logMessage = `Timestamp: ${new Date().toISOString()}, Meeting Code: ${meetingCode}, Owner Email: ${email}\n`;

    // Ensure directory exists
    fs.mkdirSync(path.dirname(logFilePath), { recursive: true });
    // Append to log file
    fs.appendFileSync(logFilePath, logMessage);

    console.log(`Received owner email for ${meetingCode}: ${email}`);

    return NextResponse.json({ message: 'Owner email received' }, { status: 200 });
  } catch (error) {
    console.error('Error in /api/owner-email:', error);
    const errorMessage = error instanceof Error ? error.message : 'An unknown error occurred';
    return NextResponse.json({ message: 'Failed to process request', error: errorMessage }, { status: 500 });
  }
}

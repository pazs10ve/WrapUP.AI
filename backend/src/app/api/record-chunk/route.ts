import { NextRequest, NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

// Ensure recordings dir exists once per cold start
const recordingsDir = path.join(process.cwd(), 'recordings');
if (!fs.existsSync(recordingsDir)) {
  fs.mkdirSync(recordingsDir, { recursive: true });
}

export async function POST(req: NextRequest) {
  const meetCode = req.headers.get('x-meet-code') || new Date().toISOString().replace(/[:.]/g, '-');
  const filePath = path.join(recordingsDir, `${meetCode}.webm`);

  // Read the raw binary body
  const chunk = Buffer.from(await req.arrayBuffer());
  fs.appendFileSync(filePath, chunk);

  return NextResponse.json({ ok: true });
}

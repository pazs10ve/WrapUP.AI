import { NextRequest, NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';
import axios from 'axios';
import FormData from 'form-data';

const recordingsDir = path.join(process.cwd(), 'recordings');
const fastApiUrl = process.env.NEXT_PUBLIC_FASTAPI_URL || 'http://localhost:8001/process-meeting/';

export async function POST(req: NextRequest) {
  console.log('--- Received request to /api/record-finish ---');
  try {
    const { meetingCode, meetLink, ownerEmail } = await req.json();
    console.log(`[record-finish] Received data: meetingCode=${meetingCode}, meetLink=${meetLink}, ownerEmail=${ownerEmail}`);

    if (!meetingCode || !meetLink || !ownerEmail) {
      console.error('[record-finish] Missing required fields');
      return NextResponse.json({ message: 'Missing required fields' }, { status: 400 });
    }

    const filePath = path.join(recordingsDir, `${meetingCode}.webm`);
    console.log(`[record-finish] Looking for recording at: ${filePath}`);
    if (!fs.existsSync(filePath)) {
      console.error('[record-finish] Recording file not found');
      return NextResponse.json({ message: 'Recording file not found' }, { status: 404 });
    }

    // Build multipart form to send to FastAPI
    const form = new FormData();
    form.append('meet_link', meetLink);
    form.append('user_email', ownerEmail);
    form.append('audio_file', fs.createReadStream(filePath), `${meetingCode}.webm`);
    console.log('[record-finish] FormData created, preparing to call FastAPI.');
    console.log(`Forwarding request to FastAPI at ${fastApiUrl}`);

    const response = await axios.post(fastApiUrl, form, {
      headers: {
        ...form.getHeaders(),
      },
    });
    console.log(`[record-finish] FastAPI response status: ${response.status}`);

    const data = response.data;
    console.log('[record-finish] Successfully processed by FastAPI:', data);
    return NextResponse.json({ message: 'Meeting processed', data });
  } catch (err) {
    if (axios.isAxiosError(err)) {
      console.error('Full Axios error in /api/record-finish:', err);
      return NextResponse.json({ message: 'Internal error', error: err.message, code: err.code }, { status: 500 });
    } else {
      const errorMessage = err instanceof Error ? err.message : 'An unknown error occurred';
      console.error('Generic error in /api/record-finish:', errorMessage);
      return NextResponse.json({ message: 'Internal error', error: errorMessage }, { status: 500 });
    }
  }
}

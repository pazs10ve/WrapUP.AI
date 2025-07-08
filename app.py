import os
import logging
import uvicorn
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from datetime import datetime
import database as db
from transcribe import transcribe_audio
from summarize import generate_summary
from send_email import send_summary_email

# Create uploads and summaries directories if they don't exist
os.makedirs("uploads", exist_ok=True)
os.makedirs("summaries", exist_ok=True)
os.makedirs("transcripts", exist_ok=True)

app = FastAPI()

@app.post("/process-meeting/")
async def process_meeting(
    meet_link: str = Form(...),
    user_email: str = Form(...),
    audio_file: UploadFile = File(...)
):
    print('--- Received request to /process-meeting/ ---')
    print(f'[process-meeting] Received data: meet_link={meet_link}, user_email={user_email}, filename={audio_file.filename}')
    """
    This endpoint processes a recorded meeting audio file.
    It transcribes the audio, generates a summary, sends it via email,
    and logs the meeting details in the database.
    """
    start_time = datetime.now()

    # 1. Save the uploaded audio file
    file_location = f"uploads/{audio_file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(audio_file.file.read())
    print(f'[process-meeting] Audio file saved to: {file_location}')

    # 2. Add initial meeting record to the database
    meeting_id = db.add_meeting(meet_link, user_email, start_time)
    print(f'[process-meeting] Added initial meeting record with ID: {meeting_id}')

    try:
        # 3. Transcribe the audio
        transcript_text, transcript_file_path = transcribe_audio(file_location)
        if transcript_file_path and not transcript_text:
            logging.warning("[process-meeting] Transcription completed but no text was returned (likely silence).")
            # Decide how to handle this case. For now, we'll call it a success and generate an empty summary.
            transcript_text = "(No speech detected in audio)"
        elif not transcript_file_path:
            logging.error("[process-meeting] An error occurred: 500: Transcription failed.")
            raise HTTPException(status_code=500, detail="Transcription failed.")

        # 4. Generate the summary
        summary_text, summary_file_path = generate_summary(transcript_text, meet_link)
        if not summary_text:
            raise HTTPException(status_code=500, detail="Summarization failed.")

        # 5. Send the summary email
        send_summary_email(user_email, summary_text, summary_file_path)

        # 6. Update the meeting record in the database
        end_time = datetime.now()
        db.update_meeting(meeting_id, end_time, summary_file_path, transcript_file_path)
        print({
            "message": "Meeting processed successfully!",
            "meeting_id": meeting_id,
            "summary_file": summary_file_path,
            "transcript_file": transcript_file_path
        })

        return {
            "message": "Meeting processed successfully!",
            "meeting_id": meeting_id,
            "summary_file": summary_file_path,
            "transcript_file": transcript_file_path
        }

    except Exception as e:
        print(f'[process-meeting] An error occurred: {e}')
        # Log the error and update the meeting status if something goes wrong
        end_time = datetime.now()
        db.update_meeting(meeting_id, end_time, "ERROR", str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/meetings/")
async def get_meetings():
    """Retrieves all meetings from the database."""
    meetings = db.get_all_meetings()
    return meetings

@app.get("/meetings/{meeting_id}")
async def get_meeting(meeting_id: int):
    """Retrieves a specific meeting by its ID."""
    meeting = db.get_meeting(meeting_id)
    if meeting is None:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return meeting

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)

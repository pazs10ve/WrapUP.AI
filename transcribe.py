import assemblyai as aai
from dotenv import load_dotenv
import os
import logging
from pydub import AudioSegment

load_dotenv()

# Ensure the transcripts directory exists
os.makedirs("transcripts", exist_ok=True)

def transcribe_audio(audio_file_path):
    """
    Processes an audio file by speeding it up, compressing it,
    and then transcribing it using AssemblyAI.

    Args:
        audio_file_path (str): The path to the audio file.

    Returns:
        tuple: A tuple containing the transcript text (str) and the path to the transcript file (str).
    """
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")
    aai.settings.api_key = api_key

    # Process audio
    audio = AudioSegment.from_file(audio_file_path)
    sped_up_audio = audio.speedup(playback_speed=1.4)
    temp_audio_path = "temp_processed_audio.mp3"
    sped_up_audio.export(temp_audio_path, format="mp3", bitrate="64k")

    # Transcribe
    config = aai.TranscriptionConfig(speech_model=aai.SpeechModel.best)
    transcriber = aai.Transcriber(config=config)
    transcript = transcriber.transcribe(temp_audio_path)
    print(transcript.text)

    # Clean up temp file
    os.remove(temp_audio_path)

    if transcript.status == aai.TranscriptStatus.error:
        logging.error(f"Transcription failed with error: {transcript.error}")
        return None, None

    if transcript.status != aai.TranscriptStatus.completed:
        logging.warning(f"Transcription for {audio_file_path} did not complete. Status: {transcript.status}")
        return None, None

    transcript_text = transcript.text
    if not transcript_text:
        logging.warning(f"Transcription for {audio_file_path} completed but returned empty text. Full transcript object: {transcript}")
        return None, None

    # Save transcript to a file
    base_filename = os.path.basename(audio_file_path)
    transcript_filename = f"transcript_{os.path.splitext(base_filename)[0]}.txt"
    transcript_file_path = os.path.join("transcripts", transcript_filename)

    with open(transcript_file_path, "w") as f:
        f.write(transcript.text)

    print(transcript.text, transcript_file_path)
    return transcript.text, transcript_file_path

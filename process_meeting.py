import os
import argparse
from transcribe import Transcribe
from summarize import Summarizer
from send_email import EmailSender

def main(audio_file, recipient_email):
    """
    Main function to run the full WrapUp.AI pipeline.
    """
    print("--- Starting WrapUp.AI Pipeline ---")

    # 1. Transcription
    try:
        print("\nStep 1: Transcribing audio file...")
        transcriber = Transcribe()
        transcript = transcriber.transcribe(audio_file)
        transcript_text = transcript.text
        print("Transcription complete.")
    except Exception as e:
        print(f"Error during transcription: {e}")
        return

    # 2. Summarization
    try:
        print("\nStep 2: Generating summary...")
        summarizer = Summarizer()
        summary_text = summarizer.summarize(transcript_text)
        print("Summary generation complete.")
    except Exception as e:
        print(f"Error during summarization: {e}")
        return

    # 3. Send Email
    try:
        print("\nStep 3: Sending email...")
        email_sender = EmailSender()
        subject = f"Meeting Summary for {os.path.basename(audio_file)}"
        message = email_sender.create_message('me', recipient_email, subject, summary_text)
        email_sender.send_message('me', message)
        print(f"Email sent successfully to {recipient_email}.")
    except Exception as e:
        print(f"Error sending email: {e}")
        return

    print("\n--- WrapUp.AI Pipeline Finished ---")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the full WrapUp.AI pipeline.")
    parser.add_argument("audio_file", type=str, help="The path to the audio file to process.")
    parser.add_argument("recipient_email", type=str, help="The email address to send the summary to.")
    args = parser.parse_args()

    if not os.path.exists(args.audio_file):
        print(f"Error: Audio file not found at '{args.audio_file}'")
    else:
        main(args.audio_file, args.recipient_email)

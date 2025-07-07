import assemblyai as aai
from dotenv import load_dotenv
import os
from pydub import AudioSegment

load_dotenv()


class Transcribe:
    def __init__(self):
        self.api_key = os.getenv("ASSEMBLYAI_API_KEY")
        if not self.api_key:
            raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")
        aai.settings.api_key = self.api_key

    def transcribe(self, audio_file):
        """
        Processes an audio file by speeding it up, compressing it,
        and then transcribing it using AssemblyAI.
        """

        audio = AudioSegment.from_file(audio_file)

        sped_up_audio = audio.speedup(playback_speed=1.4)

        temp_audio_path = "temp_processed_audio.mp3"
        sped_up_audio.export(temp_audio_path, format="mp3", bitrate="64k")

        config = aai.TranscriptionConfig(speech_model=aai.SpeechModel.best)
        transcriber = aai.Transcriber(config=config)
        transcript = transcriber.transcribe(temp_audio_path)

        os.remove(temp_audio_path)

        if transcript.status == aai.TranscriptStatus.error:
            raise RuntimeError(f"Transcription failed: {transcript.error}")
        
        return transcript


if __name__ == "__main__":
    audio_file = "audio.mp3"
    transcriber = Transcribe()
    transcript = transcriber.transcribe(audio_file)
    output_file = "transcript.txt"
    with open(output_file, "w") as f:
        f.write(transcript.text)
    print(f"\nTranscription saved to {output_file}")
    print("\n--- Transcription Text ---")
    print(transcript.text)
    print("--------------------------\n")

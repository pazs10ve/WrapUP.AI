from google import genai
from dotenv import load_dotenv
import os
import argparse

load_dotenv()

class Summarizer:
    """
    A class to handle meeting transcript summarization using the Gemini API.
    """
    def __init__(self):
        """
        Initializes the Summarizer by configuring the Gemini API key.
        """
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set.")
        self.client = genai.Client(api_key=self.api_key)

    def summarize(self, transcript_text):
        """
        Generates a structured summary from the transcript text.

        Args:
            transcript_text (str): The full text of the meeting transcript.

        Returns:
            str: The generated summary from the model.
        """
        prompt = f"""
        As an expert meeting analyst, your task is to provide a clear and concise summary of the following meeting transcript.

        Please structure your output in three distinct sections:
        1.  **Executive Summary:** A brief, high-level overview of the meeting's purpose and key outcomes (2-3 sentences).
        2.  **Key Discussion Points:** A bulleted list of the most important topics, decisions, and insights discussed.
        3.  **Action Items:** A numbered list of all tasks assigned, including who is responsible and any mentioned deadlines.

        If any of these sections are not applicable (e.g., no action items were discussed), state "None."

        Here is the transcript:
        ---
        {transcript_text}
        ---
        """

        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash", 
                contents=prompt
            )
            return response.text
        except Exception as e:
            raise RuntimeError(f"Failed to generate summary with Gemini: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Summarize a meeting transcript.")
    parser.add_argument(
        "transcript_file", 
        type=str, 
        help="The path to the text file containing the meeting transcript."
    )
    args = parser.parse_args()

    if not os.path.exists(args.transcript_file):
        print(f"Error: Transcript file not found at '{args.transcript_file}'")
    else:
        try:
            with open(args.transcript_file, 'r', encoding='utf-8') as f:
                transcript = f.read()
            
            summarizer = Summarizer()
            summary = summarizer.summarize(transcript)

            with open("summary.txt", "w") as f:
                f.write(summary)
   

        except (ValueError, RuntimeError) as e:
            print(f"An error occurred: {e}")

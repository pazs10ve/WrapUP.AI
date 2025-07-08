import os
from google import genai
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Ensure the summaries directory exists
os.makedirs("summaries", exist_ok=True)

def generate_summary(transcript_text, meet_link):
    """
    Generates a structured summary from the transcript text using the Gemini API.

    Args:
        transcript_text (str): The full text of the meeting transcript.
        meet_link (str): The link to the Google Meet session.

    Returns:
        tuple: A tuple containing the summary text (str) and the path to the summary file (str).
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")
    client = genai.Client(api_key=api_key)

    prompt = f"""
    As an expert meeting analyst, your task is to provide a clear and concise summary of the following meeting transcript.
    The meeting was held at the following link: {meet_link}

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
        response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
        summary_text = response.text
        print(summary_text)
    except Exception as e:
        raise RuntimeError(f"Failed to generate summary with Gemini: {e}")

    if not summary_text:
        return None, None

    # Save summary to a file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_filename = f"summary_{timestamp}.txt"
    summary_file_path = os.path.join("summaries", summary_filename)

    with open(summary_file_path, "w") as f:
        f.write(summary_text)

    return summary_text, summary_file_path

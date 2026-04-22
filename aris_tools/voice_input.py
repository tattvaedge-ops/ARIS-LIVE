import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def speech_to_text(file_path):

    try:
        with open(file_path, "rb") as audio_file:

            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )

        text = transcript.text.strip()

        if not text:
            return ""

        return text

    except Exception as e:
        print("❌ Speech-to-Text Error:", str(e))
        return ""
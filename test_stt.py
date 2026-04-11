from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

audio = open("test.wav", "rb")

response = client.audio.transcriptions.create(
    model="gpt-4o-mini-transcribe",
    file=audio
)

print("RESULT:", response.text)
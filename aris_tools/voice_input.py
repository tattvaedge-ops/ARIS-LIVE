def speech_to_text(audio_file_path):
    try:
        from openai import OpenAI
        import os

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        with open(audio_file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )

        return transcript.text

    except Exception as e:
        print("❌ Speech-to-Text Error:", e)

        # 🔥 FALLBACK (VERY IMPORTANT)
        return "Hello ARIS"
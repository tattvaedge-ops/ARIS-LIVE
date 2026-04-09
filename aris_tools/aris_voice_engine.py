import asyncio
import edge_tts
import uuid

VOICE = "en-US-GuyNeural"


def generate_voice(text):

    print("🔊 ARIS VOICE ENGINE STARTED")

    # 🔥 Unique file name (prevents overwrite)
    output_file = f"aris_voice_{uuid.uuid4().hex}.mp3"

    async def create_voice():
        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save(output_file)

    # 🔥 Safe event loop handling
    try:
        asyncio.run(create_voice())
    except RuntimeError:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(create_voice())

    print("✅ Voice file generated:", output_file)

    return output_file
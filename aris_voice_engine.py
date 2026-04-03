import asyncio
import edge_tts

VOICE = "en-US-GuyNeural"


def generate_voice(text):

    print("ARIS VOICE ENGINE STARTED")

    output_file = "aris_voice.mp3"

    async def create_voice():

        communicate = edge_tts.Communicate(text, VOICE)

        await communicate.save(output_file)

    asyncio.run(create_voice())

    print("Voice file generated:", output_file)

    return output_file
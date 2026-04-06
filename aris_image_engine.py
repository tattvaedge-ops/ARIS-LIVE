# ===== ARIS IMAGE ENGINE (FINAL WORKING VERSION) =====

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("❌ OPENAI_API_KEY NOT FOUND")

print("Image Engine Initialized")

client = OpenAI(api_key=api_key)


def generate_image(prompt):

    try:
        response = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024"
        )

        image_base64 = response.data[0].b64_json

        image_url = f"data:image/png;base64,{image_base64}"

        return image_url

    except Exception as e:
        print("IMAGE ERROR:", str(e))
        return None
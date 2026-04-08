# ===== ARIS IMAGE ENGINE (FIXED VERSION) =====

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

        # ✅ Extract base64 image
        image_base64 = response.data[0].b64_json

        # ✅ Convert to usable URL (base64)
        image_url = f"data:image/png;base64,{image_base64}"

        # ✅ RETURN DICT (IMPORTANT FIX)
        return {
            "url": image_url,
            "prompt": prompt
        }

    except Exception as e:
        print("IMAGE ERROR:", str(e))
        return f"❌ Image generation error: {str(e)}"
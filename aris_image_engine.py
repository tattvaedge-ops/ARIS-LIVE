# ===== ARIS IMAGE ENGINE (FINAL WORKING VERSION) =====

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Debug (optional - remove later)
api_key = os.getenv("OPENAI_API_KEY")
print("API KEY LOADED:", api_key[:10] if api_key else "NOT FOUND")

# Initialize client
client = OpenAI(api_key=api_key)


def generate_image(prompt):
    try:
        response = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024"
        )

        image_url = response.data[0].url

        return {
            "success": True,
            "url": image_url
        }

    except Exception as e:
        print("❌ IMAGE ERROR:", str(e))
        return {
            "success": False,
            "error": str(e)
        }
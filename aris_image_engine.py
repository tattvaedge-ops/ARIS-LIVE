# ===== ARIS IMAGE ENGINE (FINAL WORKING VERSION) =====

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Debug (optional - remove later)
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("❌ OPENAI_API_KEY NOT FOUND")

print("Image Engine Initialized")

# Initialize client
client = OpenAI(api_key=api_key)


def generate_image(prompt):
    return "❌ OLD IMAGE ENGINE DISABLED"

    try:
        # TEMP TEST (skip API)
        return f"✅ Image generated successfully for: {prompt}"

    except Exception as e:
        print("IMAGE ERROR:", str(e))
        return "❌ Image generation failed"
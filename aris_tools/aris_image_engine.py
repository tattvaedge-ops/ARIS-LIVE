# ===== ARIS IMAGE ENGINE (FINAL PRODUCTION SAFE) =====

import os
import requests
import base64
from dotenv import load_dotenv
from openai import OpenAI

# ===============================
# LOAD ENV
# ===============================
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ OPENAI_API_KEY NOT FOUND")

STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")

client = OpenAI(api_key=api_key)

print("🔥 ARIS Image Engine Initialized")


# ===============================
# PROMPT ENHANCER
# ===============================
def enhance_prompt(user_prompt):
    return f"""
Ultra realistic, cinematic, highly detailed,
professional lighting, volumetric light,
sharp focus, masterpiece quality,
{user_prompt}
"""


# ===============================
# OPENAI IMAGE ENGINE
# ===============================
def generate_openai_image(prompt):

    enhanced = enhance_prompt(prompt)

    try:
        print("🚀 Sending image request to OpenAI...")

        response = client.images.generate(
            model="gpt-image-1",
            prompt=enhanced,
            size="1024x1024"
        )

        print("✅ OpenAI image response received")

        image_base64 = response.data[0].b64_json
        image_url = f"data:image/png;base64,{image_base64}"

        return {
            "type": "openai",
            "url": image_url,
            "prompt": enhanced
        }

    except Exception as e:
        print("❌ OpenAI Image Error:", str(e))

        return {
            "type": "error",
            "message": "OpenAI image failed"
        }


# ===============================
# STABILITY FALLBACK ENGINE
# ===============================
def generate_stability_image(prompt):

    if not STABILITY_API_KEY:
        return {
            "type": "error",
            "message": "STABILITY_API_KEY missing"
        }

    enhanced = enhance_prompt(prompt)

    try:
        print("🚀 Sending image request to Stability...")

        response = requests.post(
            "https://api.stability.ai/v2beta/stable-image/generate/core",
            headers={
                "Authorization": f"Bearer {STABILITY_API_KEY}",
                "Accept": "application/json"
            },
            json={
                "prompt": enhanced,
                "output_format": "png"
            },
            timeout=20
        )

        if response.status_code != 200:
            print("❌ Stability API Error:", response.text)

            return {
                "type": "error",
                "message": "Stability failed"
            }

        result = response.json()

        image_base64 = result["image"]
        image_url = f"data:image/png;base64,{image_base64}"

        print("✅ Stability image response received")

        return {
            "type": "stability",
            "url": image_url,
            "prompt": enhanced
        }

    except Exception as e:
        print("❌ Stability Error:", str(e))

        return {
            "type": "error",
            "message": "Stability failed"
        }


# ===============================
# MAIN ROUTER
# ===============================
def generate_image(prompt, mode="normal"):

    try:
        print("🖼️ IMAGE GENERATION STARTED")

        if mode == "cinematic":
            return generate_stability_image(prompt)

        result = generate_openai_image(prompt)

        if result["type"] == "error":
            print("⚠️ Falling back to Stability...")
            return generate_stability_image(prompt)

        return result

    except Exception as e:
        print("❌ IMAGE ENGINE FATAL:", str(e))

        return {
            "type": "error",
            "message": "Image generation failed completely"
        }
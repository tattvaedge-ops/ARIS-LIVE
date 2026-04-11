# ===== ARIS IMAGE ENGINE (PRODUCTION SAFE VERSION) =====

import os
from dotenv import load_dotenv
from openai import OpenAI
import requests
import base64

# Load env
load_dotenv()

# OpenAI Setup
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ OPENAI_API_KEY NOT FOUND")

client = OpenAI(api_key=api_key)

# Stability Setup
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")

print("🔥 ARIS Image Engine Initialized (Production Mode)")


# ===============================
# 🔥 PROMPT ENHANCER
# ===============================
def enhance_prompt(user_prompt):
    return f"""
Ultra realistic, cinematic, highly detailed, professional lighting,
volumetric lighting, depth of field, sharp focus,
{user_prompt}
"""


# ===============================
# 🟢 OPENAI IMAGE (OPTIMIZED)
# ===============================
def generate_openai_image(prompt):

    enhanced = enhance_prompt(prompt)

    try:
        response = client.images.generate(
            model="gpt-image-1",
            prompt=enhanced,
            size=size="1024x1024"   # 🔥 IMPORTANT: reduced size (prevents crash)
        )

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
            "message": "OpenAI image failed (timeout or billing issue)"
        }


# ===============================
# 🔥 STABILITY IMAGE (FAST + SAFE)
# ===============================
def generate_stability_image(prompt):

    if not STABILITY_API_KEY:
        return {
            "type": "error",
            "message": "STABILITY_API_KEY NOT FOUND"
        }

    enhanced = enhance_prompt(prompt)

    url = "https://api.stability.ai/v2beta/stable-image/generate/core"

    headers = {
        "Authorization": f"Bearer {STABILITY_API_KEY}",
        "Accept": "application/json"
    }

    data = {
        "prompt": enhanced,
        "output_format": "png"
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=15)

        if response.status_code != 200:
            return {
                "type": "error",
                "message": f"Stability Error: {response.text}"
            }

        result = response.json()
        image_base64 = result["image"]

        image_bytes = base64.b64decode(image_base64)

        file_path = "stability_output.png"

        with open(file_path, "wb") as f:
            f.write(image_bytes)

        return {
            "type": "stability",
            "file": file_path,
            "prompt": enhanced
        }

    except Exception as e:
        print("❌ Stability Error:", str(e))

        return {
            "type": "error",
            "message": "Stability image failed"
        }


# ===============================
# 🎯 MAIN FUNCTION (SMART ROUTING)
# ===============================
def generate_image(prompt, mode="normal"):

    try:
        # 🔥 Prefer Stability in production (faster + safer)
        if mode == "cinematic":
            return generate_stability_image(prompt)

        # 🔁 fallback system
        result = generate_openai_image(prompt)

        if result.get("type") == "error":
            print("⚠️ Falling back to Stability AI...")
            return generate_stability_image(prompt)

        return result

    except Exception as e:
        print("❌ IMAGE ENGINE ERROR:", str(e))

        return {
            "type": "error",
            "message": "Image generation failed completely"
        }
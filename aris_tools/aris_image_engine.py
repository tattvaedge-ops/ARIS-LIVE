# ===== ARIS IMAGE ENGINE (FINAL PRO VERSION) =====

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

print("🔥 ARIS Image Engine Initialized")


# ===============================
# 🔥 PROMPT ENHANCER (WOW FACTOR)
# ===============================
def enhance_prompt(user_prompt):
    return f"""
Ultra realistic, cinematic, highly detailed, 8K resolution,
professional lighting, volumetric lighting, depth of field,
sharp focus, realistic textures,
{user_prompt}
"""


# ===============================
# 🟢 OPENAI IMAGE (FAST MODE)
# ===============================
def generate_openai_image(prompt):

    enhanced = enhance_prompt(prompt)

    response = client.images.generate(
        model="gpt-image-1",
        prompt=enhanced,
        size="1024x1024"
    )

    image_base64 = response.data[0].b64_json
    image_url = f"data:image/png;base64,{image_base64}"

    return {
        "type": "openai",
        "url": image_url,
        "prompt": enhanced
    }


# ===============================
# 🔥 STABILITY IMAGE (CINEMATIC)
# ===============================
def generate_stability_image(prompt):

    if not STABILITY_API_KEY:
        return "❌ STABILITY_API_KEY NOT FOUND"

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

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        return f"❌ Stability Error: {response.text}"

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


# ===============================
# 🎯 MAIN FUNCTION (ARIS ENTRY)
# ===============================
def generate_image(prompt, mode="normal"):

    try:
        if mode == "cinematic":
            return generate_stability_image(prompt)

        return generate_openai_image(prompt)

    except Exception as e:
        print("IMAGE ERROR:", str(e))
        return f"❌ Image generation error: {str(e)}"
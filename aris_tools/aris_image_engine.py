# ===== ARIS IMAGE ENGINE (FINAL PRODUCTION SAFE) =====

import os
import requests
from dotenv import load_dotenv
from openai import OpenAI
import aris_engines.aris_prompt_engine as prompt_engine

smart_prompt = prompt_engine.smart_prompt


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
# SMART IMAGE SIZE ENGINE
# ===============================
def choose_image_size(prompt):

    p = prompt.lower()

    if any(word in p for word in [
        "solar system", "timeline", "classroom",
        "landscape", "office", "city", "group"
    ]):
        return "1536x1024"

    if any(word in p for word in [
        "portrait", "leader", "person",
        "ambedkar", "face", "hero"
    ]):
        return "1024x1536"

    return "1024x1024"


# ===============================
# OPENAI IMAGE ENGINE
# ===============================
def generate_openai_image(prompt):

    enhanced = enhance_prompt(prompt)
    size = choose_image_size(prompt)

    try:
        print("🚀 Sending image request to OpenAI...")
        print("🖼️ SIZE:", size)

        response = client.images.generate(
            model="gpt-image-1",
            prompt=enhanced,
            size=size
        )

        image_base64 = response.data[0].b64_json
        image_url = f"data:image/png;base64,{image_base64}"

        print("✅ OpenAI image created")

        return {
            "success": True,
            "engine": "openai",
            "url": image_url,
            "prompt": enhanced
        }

    except Exception as e:
        print("❌ OpenAI Image Error:", str(e))

        return {
            "success": False,
            "message": "OpenAI image failed"
        }


# ===============================
# STABILITY FALLBACK
# ===============================
def generate_stability_image(prompt):

    if not STABILITY_API_KEY:
        return {
            "success": False,
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
            files={
                "prompt": (None, enhanced),
                "output_format": (None, "png")
            },
            timeout=25
        )

        if response.status_code != 200:
            print("❌ Stability API Error:", response.text)

            return {
                "success": False,
                "message": "Stability failed"
            }

        result = response.json()

        image_base64 = result["image"]
        image_url = f"data:image/png;base64,{image_base64}"

        print("✅ Stability image created")

        return {
            "success": True,
            "engine": "stability",
            "url": image_url,
            "prompt": enhanced
        }

    except Exception as e:
        print("❌ Stability Error:", str(e))

        return {
            "success": False,
            "message": "Stability failed"
        }


# ===============================
# MAIN ROUTER
# ===============================
def generate_image(prompt, mode="normal"):

    try:
        prompt = smart_prompt(prompt, mode, "image")

        print("🔥 SMART PROMPT:", prompt)
        print("🖼️ IMAGE GENERATION STARTED")

        result = generate_openai_image(prompt)

        if not result.get("success"):
            print("⚠️ Falling back to Stability...")
            result = generate_stability_image(prompt)

        return result

    except Exception as e:
        print("❌ IMAGE ENGINE FATAL:", str(e))

        return {
            "success": False,
            "message": "Image generation failed completely"
        }
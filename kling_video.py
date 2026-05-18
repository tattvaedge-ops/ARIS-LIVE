# C:\AGENTIC AI- ARIS\kling_video.py

import os
import requests


# ==========================================
# KLING API CREDENTIALS
# ==========================================
KLING_ACCESS_KEY = os.getenv("KLING_ACCESS_KEY", "").strip()
KLING_SECRET_KEY = os.getenv("KLING_SECRET_KEY", "").strip()


# ==========================================
# KLING VIDEO GENERATION
# ==========================================
def generate_kling_video(prompt):
    """
    Generate a video using Kling AI.

    Args:
        prompt (str): Text prompt describing the video.

    Returns:
        dict: Parsed JSON response from Kling API.
    """

    # --------------------------------------
    # VALIDATION
    # --------------------------------------
    prompt = str(prompt).strip()

    if not prompt:
        raise Exception("Video prompt is empty.")

    if not KLING_ACCESS_KEY:
        raise Exception("KLING_ACCESS_KEY is missing.")

    # --------------------------------------
    # API ENDPOINT
    # --------------------------------------
    url = "https://api.klingai.com/v1/videos"

    # --------------------------------------
    # HEADERS
    # --------------------------------------
    headers = {
        "Authorization": f"Bearer {KLING_ACCESS_KEY}",
        "Content-Type": "application/json",
    }

    # --------------------------------------
    # PAYLOAD
    # --------------------------------------
    payload = {
        "model_name": "kling-v1",
        "mode": "std",
        "duration": 5,
        "aspect_ratio": "16:9",
        "input": {
            "prompt": prompt
        }
    }

    # --------------------------------------
    # DEBUG LOGS
    # --------------------------------------
    print("KLING URL:", url)
    print("KLING PAYLOAD:", payload)

    # --------------------------------------
    # API REQUEST
    # --------------------------------------
    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=120,
    )

    # --------------------------------------
    # DEBUG RESPONSE
    # --------------------------------------
    print("KLING STATUS:", response.status_code)
    print("KLING RESPONSE:", response.text)

    # --------------------------------------
    # ERROR HANDLING
    # --------------------------------------
    if response.status_code not in [200, 201]:
        raise Exception(response.text)

    # --------------------------------------
    # PARSE JSON
    # --------------------------------------
    try:
        return response.json()
    except Exception:
        return {
            "success": True,
            "raw_response": response.text
        }
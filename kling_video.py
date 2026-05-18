import os
import requests


KLING_ACCESS_KEY = os.getenv("KLING_ACCESS_KEY", "").strip()
KLING_SECRET_KEY = os.getenv("KLING_SECRET_KEY", "").strip()


def generate_kling_video(prompt):
    if not KLING_ACCESS_KEY or not KLING_SECRET_KEY:
        raise Exception("Kling API keys are missing.")

    # TODO: Replace with official Kling API endpoint
    url = "https://api.klingai.com/v1/videos"

    headers = {
        "Authorization": f"Bearer {KLING_ACCESS_KEY}",
        "Content-Type": "application/json", 
    }

    payload = {
        "model_name": "kling-v1",
        "mode": "std",
        "duration": 5,
        "aspect_ratio": "16:9",
        "input": {
            "prompt": prompt
        }    
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=120,
    )

    if response.status_code not in [200, 201]:
        print("KLING STATUS:", response.status_code)
        print("KLING RESPONSE:", response.text)
        raise Exception(response.text)

    return response.json()

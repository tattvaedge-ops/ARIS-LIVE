import os
import requests

REPLICATE_API_KEY = os.getenv("REPLICATE_API_KEY")

def generate_ai_video(prompt):
    try:
        url = "https://api.replicate.com/v1/predictions"

        headers = {
            "Authorization": f"Token {REPLICATE_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "version": "PLACEHOLDER_MODEL",
            "input": {
                "prompt": prompt
            }
        }

        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        return {
            "type": "video",
            "status": "processing",
            "prediction_id": result.get("id"),
            "message": "🎬 ARIS is generating cinematic video..."
        }

    except Exception as e:
        return {
            "type": "video",
            "status": "error",
            "message": str(e)
        }
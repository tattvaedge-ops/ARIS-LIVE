import requests
import base64
import os

# Cloud GPU endpoint
VIDEO_GPU_URL = "https://your-ngrok-url/generate_video"

video_counter = 0


def generate_video_clip(prompt):

    global video_counter

    print("ARIS VIDEO DIFFUSION REQUEST")
    print("Prompt:", prompt)

    try:

        payload = {
            "prompt": prompt,
            "duration": 4
        }

        response = requests.post(VIDEO_GPU_URL, json=payload)

        if response.status_code != 200:
            print("VIDEO GPU ERROR:", response.text)
            return None

        result = response.json()

        if "video" not in result:
            print("VIDEO RESPONSE ERROR:", result)
            return None

        video_base64 = result["video"]

        video_bytes = base64.b64decode(video_base64)

        video_counter += 1

        filename = f"scene_video_{video_counter}.mp4"

        with open(filename, "wb") as f:
            f.write(video_bytes)

        print("VIDEO CLIP GENERATED:", filename)

        return filename

    except Exception as e:

        print("VIDEO GENERATION ERROR:", e)

        return None
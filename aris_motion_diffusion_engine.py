import requests
import os

# Example endpoint (replace later with real video diffusion API)
VIDEO_DIFFUSION_URL = "http://127.0.0.1:6000/generate_video"

video_counter = 0


def generate_motion_video(prompt):

    global video_counter

    print("ARIS MOTION DIFFUSION ENGINE")
    print("Prompt:", prompt)

    try:

        payload = {
            "prompt": prompt,
            "seconds": 3
        }

        response = requests.post(VIDEO_DIFFUSION_URL, json=payload)

        if response.status_code != 200:

            print("VIDEO DIFFUSION ERROR:", response.text)

            return None

        video_bytes = response.content

        video_counter += 1

        filename = f"scene_motion_{video_counter}.mp4"

        with open(filename, "wb") as f:
            f.write(video_bytes)

        print("Motion video generated:", filename)

        return filename

    except Exception as e:

        print("MOTION DIFFUSION ERROR:", e)

        return None
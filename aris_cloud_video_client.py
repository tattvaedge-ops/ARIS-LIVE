import requests
import base64
import os

OUTPUT_DIR = "ARIS_OUTPUT"


def generate_cloud_video(prompt, scene_id):

    print("\n==============================")
    print("ARIS CLOUD VIDEO REQUEST")
    print("Prompt:", prompt)
    print("==============================\n")

    try:

        url = "https://chaim-mentholated-alfredia.ngrok-free.dev/generate_video"

        payload = {
            "prompt": prompt
        }

        response = requests.post(url, json=payload)

        if response.status_code != 200:
            print("Cloud video generation failed")
            return None

        data = response.json()

        video_base64 = data["video"]

        video_bytes = base64.b64decode(video_base64)

        os.makedirs(OUTPUT_DIR, exist_ok=True)

        video_path = os.path.join(OUTPUT_DIR, f"scene_ai_{scene_id}.mp4")

        with open(video_path, "wb") as f:
            f.write(video_bytes)

        print("AI VIDEO GENERATED:", video_path)

        return video_path

    except Exception as e:

        print("Cloud video error:", str(e))

        return None
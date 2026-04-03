import requests
import base64
import os

OUTPUT_FOLDER = "ARIS_OUTPUT"


def generate_cloud_image(prompt, scene_id):

    print("\n==============================")
    print("ARIS CLOUD GPU IMAGE REQUEST")
    print("Prompt:", prompt)
    print("==============================\n")

    try:

        url = "https://chaim-mentholated-alfredia.ngrok-free.dev/generate_image"

        payload = {
            "prompt": prompt
        }

        response = requests.post(url, json=payload)

        if response.status_code != 200:

            print("Cloud GPU request failed")

            return None

        data = response.json()

        image_base64 = data["image"]

        image_bytes = base64.b64decode(image_base64)

        os.makedirs(OUTPUT_FOLDER, exist_ok=True)

        image_path = os.path.join(OUTPUT_FOLDER, f"image_scene_{scene_id}.png")

        with open(image_path, "wb") as f:
            f.write(image_bytes)

        print("IMAGE GENERATED FROM CLOUD GPU")

        print("Saved to:", image_path)

        return image_path

    except Exception as e:

        print("Cloud GPU error:", str(e))

        return None
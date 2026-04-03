import requests

API_URL = "https://chaim-mentholated-alfredia.ngrok-free.dev/"

def generate_image(prompt):

    payload = {
        "data": [prompt]
    }

    response = requests.post(API_URL, json=payload)

    result = response.json()

    image_url = result["data"][0]

    image = requests.get(image_url).content

    file_path = "generated_images/scene.png"

    with open(file_path, "wb") as f:
        f.write(image)

    return file_path
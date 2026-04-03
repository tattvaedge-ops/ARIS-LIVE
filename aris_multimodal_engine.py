import ollama


def analyze_image(image_description):

    prompt = f"""
You are a visual analysis AI.

Analyze this image description:

{image_description}

Return:

MAIN_OBJECT
KEY_ELEMENTS
CONCEPT
EDUCATIONAL_USE
"""

    response = ollama.chat(
        model="phi3:mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]


def analyze_video(video_description):

    prompt = f"""
You are a video analysis AI.

Analyze the following video description:

{video_description}

Return:

MAIN_SCENE
KEY_ACTION
CONCEPT
LEARNING_POINTS
"""

    response = ollama.chat(
        model="phi3:mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]
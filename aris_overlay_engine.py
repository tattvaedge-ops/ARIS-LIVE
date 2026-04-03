import ollama


def generate_overlays(topic):

    prompt = f"""
You are an educational video designer.

Topic: {topic}

Generate educational overlay elements.

Return in this format:

LABELS:
ARROWS:
HIGHLIGHTS:
CAPTION:

Rules:
Short phrases only.
Do not explain.
"""

    response = ollama.chat(
        model="phi3:mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]
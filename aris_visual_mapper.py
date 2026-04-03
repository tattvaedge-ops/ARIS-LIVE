import ollama


def map_visual_elements(topic, base_prompt):

    prompt = f"""
You are an XR educational visual designer.

Topic:
{topic}

Scene description:
{base_prompt}

Improve this scene by adding educational visual elements.

Add:
- labels
- arrows
- highlights
- diagrams
- explanatory markers

Rules:
Make it suitable for educational visualization.
Do not write explanation.
Return only the improved visual prompt.
"""

    response = ollama.chat(
        model="phi3:mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"].strip()
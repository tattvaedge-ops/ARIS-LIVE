import ollama


def enhance_visual_prompt(topic, base_prompt):

    prompt = f"""
You are an XR educational visual designer.

Topic: {topic}

Base visual idea:
{base_prompt}

Convert this into a high quality cinematic XR visualization prompt.

Rules:
- educational visualization
- highly detailed
- cinematic lighting
- clear concept illustration
- immersive environment
- suitable for AI image generation

Return only the improved prompt.
"""

    response = ollama.chat(
        model="phi3:mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"].strip()
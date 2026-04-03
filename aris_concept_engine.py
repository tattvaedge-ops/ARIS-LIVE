import ollama


def generate_concept_structure(topic):

    prompt = f"""
You are an expert educational instructor.

Explain the concept of: {topic}

Return the explanation using this structure:

DEFINITION
CORE_MECHANISM
REAL_WORLD_EXAMPLE
KEY_INSIGHT
COMMON_MISCONCEPTION
CONCLUSION

Rules:
Keep explanations clear and concise.
Focus on conceptual understanding.
Do not include extra commentary.
"""

    response = ollama.chat(
        model="phi3:mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]
import ollama


def plan_task(user_input):

    prompt = f"""
You are the central AI agent of ARIS.

User request:
{user_input}

Decide which ARIS systems should run.

Available systems:

VIDEO_CREATION
IMAGE_CREATION
RESEARCH
MULTIMODAL_ANALYSIS
GENERAL_CHAT

Return ONLY one task type.
"""

    response = ollama.chat(
        model="phi3:mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"].strip()
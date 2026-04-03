import ollama


def generate_story_arc(topic):

    prompt = f"""
You are a cinematic educational storyteller.

Create a 6-scene story arc to explain the concept: {topic}

Return in this format:

SCENE 1:
TYPE: Hook
DESCRIPTION:

SCENE 2:
TYPE: Curiosity
DESCRIPTION:

SCENE 3:
TYPE: Explanation
DESCRIPTION:

SCENE 4:
TYPE: Visualization
DESCRIPTION:

SCENE 5:
TYPE: Real World Example
DESCRIPTION:

SCENE 6:
TYPE: Final Insight
DESCRIPTION:

Rules:
Scenes must build understanding step-by-step.
Use visual storytelling.
Avoid long explanations.
"""

    response = ollama.chat(
        model="phi3:mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]
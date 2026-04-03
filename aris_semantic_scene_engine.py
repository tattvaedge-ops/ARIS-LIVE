try:
    import ollama
except:
    ollama = None


def generate_semantic_scenes(topic):

    prompt = f"""
You are a cinematic educational video director.

Create 6 visual scenes to explain the concept: {topic}

Return ONLY in this format:

SCENE 1:
TYPE:
VISUAL:
CAMERA:

SCENE 2:
TYPE:
VISUAL:
CAMERA:

SCENE 3:
TYPE:
VISUAL:
CAMERA:

SCENE 4:
TYPE:
VISUAL:
CAMERA:

SCENE 5:
TYPE:
VISUAL:
CAMERA:

SCENE 6:
TYPE:
VISUAL:
CAMERA:

Rules:
• Each scene must visually explain the concept
• Avoid abstract descriptions
• Prefer diagrams, demonstrations, or real situations
• Keep scenes cinematic
"""

    # =========================
    # LOCAL MODE (OLLAMA)
    # =========================
    if ollama:
        try:
            response = ollama.chat(
                model="phi3:mini",
                messages=[{"role": "user", "content": prompt}]
            )

            return response["message"]["content"]

        except Exception as e:
            print("Ollama error:", str(e))
            return "⚠️ Semantic scene generation failed"

    # =========================
    # CLOUD MODE (RENDER)
    # =========================
    else:
        return "⚠️ Semantic scene generation not available in cloud mode"
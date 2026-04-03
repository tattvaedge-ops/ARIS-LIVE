try:
    import ollama
except:
    ollama = None


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

    if ollama:
        try:
            response = ollama.chat(
                model="phi3:mini",
                messages=[{"role": "user", "content": prompt}]
            )

            return response["message"]["content"].strip()

        except Exception as e:
            print("Ollama error:", str(e))
            return "GENERAL_CHAT"

    else:
        # Cloud fallback (no ollama)
        return "GENERAL_CHAT"
# ===== ARIS CREATION AGENT (IMAGE + CREATIVE ENGINE) =====

from aris_brain import ask_ai
from aris_tools.aris_image_engine import generate_image


def creation_agent(user_input):

    text = user_input.lower()

    # =============================
    # IMAGE GENERATION
    # =============================
    if "image" in text or "picture" in text or "generate image" in text:

        print("ARIS IMAGE GENERATION TRIGGERED")

        result = generate_image(user_input)

        if result["success"]:
            return f"""
🖼️ ARIS IMAGE GENERATED

Prompt:
{user_input}

🔗 Image URL:
{result['url']}
"""
        else:
            return f"""
❌ IMAGE GENERATION FAILED

Error:
{result['error']}
"""

    # =============================
    # VIDEO CREATION (COMING NEXT)
    # =============================
    if "video" in text or "generate video" in text or "create video" in text:

        print("VIDEO REQUEST DETECTED")

        return """
🎬 ARIS VIDEO CREATION

Video generation is being activated.

Soon ARIS will generate:
• cinematic scenes
• AI visuals
• motion sequences
• final rendered video

(Feature unlocking next...)
"""

    # =============================
    # GENERAL CREATIVE RESPONSE
    # =============================
    prompt = f"""
You are ARIS Creator Agent.

Your role is to generate high-quality creative outputs.

Capabilities:
- content creation
- scripts
- explanations
- structured outputs
- creative ideas

User request:
{user_input}

Provide a powerful and useful response.
"""

    return ask_ai(prompt)
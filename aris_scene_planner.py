try:
    import ollama
except:
    ollama = None

import re

from aris_cinematic_story_engine import generate_story_arc
from aris_semantic_scene_engine import generate_semantic_scenes
from aris_image_engine import generate_image


def generate_scenes(topic):

    print("SCENE PLANNER STARTED")

    # Step 1: cinematic story
    story = generate_story_arc(topic)
    print("CINEMATIC STORY ARC READY")

    # Step 2: semantic structure
    semantic = generate_semantic_scenes(topic)
    print("SEMANTIC SCENES READY")

    prompt = f"""
You are an educational video director.

Topic:
{topic}

Story Arc:
{story}

Concept Structure:
{semantic}

Create a final scene plan for a 60 second educational video.

Return EXACT format:

SCENE 1
VISUAL:
NARRATION:

SCENE 2
VISUAL:
NARRATION:

SCENE 3
VISUAL:
NARRATION:

SCENE 4
VISUAL:
NARRATION:

SCENE 5
VISUAL:
NARRATION:

SCENE 6
VISUAL:
NARRATION:

Rules:
• narration = 1 short sentence
• visuals must be cinematic
• educational clarity
"""

    # =========================
    # OLLAMA (LOCAL MODE)
    # =========================
    if ollama:
        try:
            response = ollama.chat(
                model="phi3:mini",
                messages=[{"role": "user", "content": prompt}]
            )

            scene_script = response["message"]["content"]

        except Exception as e:
            print("Ollama error:", str(e))
            return "⚠️ Scene generation failed"

    # =========================
    # CLOUD FALLBACK
    # =========================
    else:
        return "⚠️ Scene planning not available in cloud mode"

    print("\nSCENE SCRIPT GENERATED\n")
    print(scene_script)

    # =========================
    # Extract VISUAL prompts
    # =========================
    visual_prompts = re.findall(r"VISUAL:\s*(.*)", scene_script)

    scenes = []

    for i, visual in enumerate(visual_prompts, start=1):

        print(f"\nGENERATING IMAGE FOR SCENE {i}")

        image_path = generate_image(visual)

        scene_data = {
            "scene_id": i,
            "visual_prompt": visual,
            "image_path": image_path
        }

        scenes.append(scene_data)

    print("\nALL SCENE IMAGES GENERATED\n")

    return scenes
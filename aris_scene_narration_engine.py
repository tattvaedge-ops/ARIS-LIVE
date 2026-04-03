import re


def extract_scene_narrations(scene_text):

    narrations = []

    lines = scene_text.split("\n")

    for line in lines:

        if "NARRATION:" in line:

            narration = line.replace("NARRATION:", "").strip()

            if narration:
                narrations.append(narration)

    return narrations



def match_narration_to_scenes(image_files, narrations):

    scene_data = []

    total = min(len(image_files), len(narrations))

    for i in range(total):

        scene = {
            "image": image_files[i],
            "narration": narrations[i]
        }

        scene_data.append(scene)

    return scene_data
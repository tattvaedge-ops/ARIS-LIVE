import random


VISUAL_STYLES = [

    "cinematic 3D scientific visualization",
    "high-detail educational documentary style",
    "professional science animation",
    "cinematic educational infographic",
    "high-quality scientific illustration"

]


CAMERA_STYLES = [

    "dramatic lighting",
    "soft studio lighting",
    "high contrast lighting",
    "cinematic depth of field"

]


COLOR_THEMES = [

    "blue scientific color palette",
    "dark space cinematic palette",
    "clean educational white palette"

]


def select_visual_style():

    style = random.choice(VISUAL_STYLES)
    camera = random.choice(CAMERA_STYLES)
    color = random.choice(COLOR_THEMES)

    visual_profile = {

        "style": style,
        "camera": camera,
        "color": color

    }

    return visual_profile



def apply_visual_consistency(prompt, visual_profile):

    style = visual_profile["style"]
    camera = visual_profile["camera"]
    color = visual_profile["color"]

    final_prompt = f"""
{prompt},

{style},
{camera},
{color},
high detail,
professional educational rendering
"""

    return final_prompt
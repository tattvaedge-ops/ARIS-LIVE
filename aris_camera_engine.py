import random


CAMERA_SHOTS = [

    "wide cinematic shot",
    "medium shot",
    "close-up shot",
    "macro detail shot",
    "overhead top view",
    "side profile shot",
    "tracking shot",
    "dramatic angle shot"

]


CAMERA_LENSES = [

    "50mm cinematic lens",
    "35mm documentary lens",
    "macro photography lens",
    "wide angle lens"

]


CAMERA_MOVEMENTS = [

    "steady camera",
    "slow tracking camera",
    "cinematic handheld camera",
    "smooth gimbal camera"

]


def generate_camera_plan(total_scenes):

    camera_plan = []

    for i in range(total_scenes):

        shot = random.choice(CAMERA_SHOTS)

        lens = random.choice(CAMERA_LENSES)

        movement = random.choice(CAMERA_MOVEMENTS)

        camera = {

            "shot": shot,
            "lens": lens,
            "movement": movement

        }

        camera_plan.append(camera)

    return camera_plan



def apply_camera_style(prompt, camera):

    shot = camera["shot"]
    lens = camera["lens"]
    movement = camera["movement"]

    enhanced_prompt = f"""
{prompt},

{shot},
{lens},
{movement},
cinematic composition,
professional film framing
"""

    return enhanced_prompt
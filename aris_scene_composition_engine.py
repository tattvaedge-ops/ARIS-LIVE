import random


COMPOSITION_RULES = {

    "space": [
        "planet centered in frame with star background",
        "orbit path visible around planet",
        "deep space background with stars"
    ],

    "biology": [
        "subject centered with anatomical layers",
        "close up scientific visualization",
        "transparent cross section view"
    ],

    "physics": [
        "object motion path visible",
        "diagram overlay explaining force direction",
        "scientific demonstration layout"
    ]

}


GENERIC_COMPOSITION = [

    "subject centered in frame",
    "clean educational composition",
    "cinematic scientific visualization"

]


def detect_domain(topic):

    topic = topic.lower()

    if "planet" in topic or "space" in topic or "black hole" in topic:
        return "space"

    if "heart" in topic or "cell" in topic or "blood" in topic:
        return "biology"

    if "force" in topic or "gravity" in topic or "inertia" in topic:
        return "physics"

    return "generic"


def apply_scene_composition(prompt, topic):

    domain = detect_domain(topic)

    if domain in COMPOSITION_RULES:

        rule = random.choice(COMPOSITION_RULES[domain])

    else:

        rule = random.choice(GENERIC_COMPOSITION)

    composed_prompt = f"""
{prompt},

{rule},
cinematic framing,
balanced scene layout,
scientific visualization
"""

    return composed_prompt
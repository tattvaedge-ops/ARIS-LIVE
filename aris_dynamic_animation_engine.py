import random


ANIMATION_TYPES = {

    "inertia": [
        "object sliding forward after sudden stop",
        "passengers leaning forward due to inertia"
    ],

    "gravity": [
        "ball falling downward",
        "object accelerating toward ground"
    ],

    "friction": [
        "object slowing down while sliding",
        "surface resistance reducing motion"
    ],

    "momentum": [
        "moving ball colliding with stationary ball",
        "transfer of motion between objects"
    ],

    "heart": [
        "heart muscle contracting rhythmically",
        "blood flowing through arteries"
    ],

    "planet": [
        "planet orbiting star",
        "elliptical orbital motion"
    ]

}


GENERIC_ANIMATIONS = [

    "slow scientific animation",
    "educational motion demonstration",
    "mechanical movement visualization"

]


def generate_animation(topic):

    topic = topic.lower()

    for key in ANIMATION_TYPES:

        if key in topic:

            return random.choice(ANIMATION_TYPES[key])

    return random.choice(GENERIC_ANIMATIONS)



def apply_animation(prompt, topic):

    animation = generate_animation(topic)

    animated_prompt = f"""
{prompt},

dynamic motion scene,
{animation},
smooth scientific animation,
educational demonstration
"""

    return animated_prompt
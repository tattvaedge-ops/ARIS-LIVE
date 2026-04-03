def generate_world_context(topic):

    topic = topic.lower()

    world = {}

    # --------------------------------
    # PHYSICS WORLDS
    # --------------------------------

    if "inertia" in topic:

        world["environment"] = "moving city bus interior"
        world["objects"] = ["bus", "passengers", "seats"]
        world["interaction"] = "bus suddenly brakes and passengers move forward"

    elif "gravity" in topic:

        world["environment"] = "open outdoor environment"
        world["objects"] = ["falling ball", "ground"]
        world["interaction"] = "ball falling downward due to gravity"

    elif "friction" in topic:

        world["environment"] = "surface sliding experiment"
        world["objects"] = ["wood block", "rough surface"]
        world["interaction"] = "block slows down due to friction"

    elif "momentum" in topic:

        world["environment"] = "collision experiment"
        world["objects"] = ["moving ball", "stationary ball"]
        world["interaction"] = "moving object transfers momentum"

    elif "heart" in topic:

        world["environment"] = "3D medical visualization"
        world["objects"] = ["human heart", "blood vessels"]
        world["interaction"] = "heart contracting and pumping blood"

    elif "planet" in topic:

        world["environment"] = "outer space"
        world["objects"] = ["planet", "star", "orbit path"]
        world["interaction"] = "planet orbiting star due to gravity"

    else:

        world["environment"] = "educational demonstration environment"
        world["objects"] = ["subject elements"]
        world["interaction"] = "scientific explanation in action"

    return world


def apply_world_simulation(prompt, world):

    environment = world["environment"]
    objects = ", ".join(world["objects"])
    interaction = world["interaction"]

    simulated_prompt = f"""
{prompt},

environment: {environment},
objects: {objects},
interaction: {interaction},
educational scientific demonstration,
realistic scenario
"""

    return simulated_prompt
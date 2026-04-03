def generate_physics_scene(topic, scene_prompt):

    topic = topic.lower()

    physics_rules = []

    # --------------------------------
    # PHYSICS TOPICS
    # --------------------------------

    if "inertia" in topic:

        physics_rules.append("object continues moving when force stops")
        physics_rules.append("body moves forward when vehicle stops")

    elif "gravity" in topic:

        physics_rules.append("objects fall downward")
        physics_rules.append("gravitational attraction between masses")

    elif "friction" in topic:

        physics_rules.append("surface resists motion")
        physics_rules.append("motion slows down")

    elif "momentum" in topic:

        physics_rules.append("moving object carries momentum")
        physics_rules.append("force needed to stop motion")

    elif "heart" in topic:

        physics_rules.append("heart muscle contracts")
        physics_rules.append("blood pumped through arteries")

    elif "planet" in topic:

        physics_rules.append("orbital motion around star")
        physics_rules.append("gravity keeps orbit stable")

    # --------------------------------
    # BUILD PHYSICS PROMPT
    # --------------------------------

    physics_text = ", ".join(physics_rules)

    enhanced_prompt = f"""
{scene_prompt},

real world physics behaviour,
{physics_text},
educational scientific visualization
"""

    return enhanced_prompt
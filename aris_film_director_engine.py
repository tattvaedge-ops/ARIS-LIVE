def generate_edit_plan(total_scenes):

    transitions = [
        "fade_in",
        "crossfade",
        "zoom_transition",
        "cut",
        "crossfade",
        "fade_out"
    ]

    plan = []

    for i in range(total_scenes):

        transition = transitions[i % len(transitions)]

        plan.append(transition)

    return plan
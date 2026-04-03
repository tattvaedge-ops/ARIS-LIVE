"""
ARIS CINEMATIC EDITING ENGINE
-----------------------------
Controls cinematic transitions between scenes.
"""

import random


class ARISCinematicEditingEngine:

    def __init__(self):

        self.transitions = [
            "cut",
            "fade",
            "crossfade",
            "zoom",
            "pan"
        ]


    def assign_transitions(self, scenes):

        edited_scenes = []

        for i, scene in enumerate(scenes):

            if i == 0:
                transition = "fade_in"
            else:
                transition = random.choice(self.transitions)

            scene["transition"] = transition

            edited_scenes.append(scene)

        return edited_scenes
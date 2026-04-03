"""
ARIS SCENE TIMING ENGINE
------------------------
Synchronizes narration duration with scene timing.
"""

import math

class ARISSceneTimingEngine:

    def __init__(self):
        pass


    def estimate_duration(self, narration_text):

        words = narration_text.split()

        words_per_second = 2.5

        duration = len(words) / words_per_second

        return round(duration, 2)


    def generate_scene_timeline(self, scenes):

        timeline = []

        current_time = 0

        for scene in scenes:

            narration = scene.get("narration", "")

            duration = self.estimate_duration(narration)

            start = current_time
            end = start + duration

            scene["start_time"] = start
            scene["end_time"] = end
            scene["duration"] = duration

            timeline.append(scene)

            current_time = end

        return timeline
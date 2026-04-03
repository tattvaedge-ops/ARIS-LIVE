"""
ARIS VISUAL TAGGING ENGINE
--------------------------
Generates structured visual tags for each scene.
These tags help maintain visual consistency and improve prompts.
"""

class ARISVisualTaggingEngine:

    def __init__(self):
        pass


    def generate_tags(self, scene_data):
        """
        Generate visual tags from scene description
        """

        description = scene_data.get("description", "").lower()

        tags = {
            "environment": self.detect_environment(description),
            "objects": self.detect_objects(description),
            "style": "cinematic",
            "lighting": "dramatic",
            "motion": self.detect_motion(description)
        }

        return tags


    def detect_environment(self, text):

        environments = {
            "space": ["space", "planet", "galaxy", "star"],
            "nature": ["forest", "river", "mountain"],
            "city": ["city", "building", "street"],
            "classroom": ["teacher", "board", "student"],
            "laboratory": ["experiment", "lab", "chemical"]
        }

        for env, keywords in environments.items():
            for k in keywords:
                if k in text:
                    return env

        return "general"


    def detect_objects(self, text):

        objects = []

        keywords = [
            "earth","sun","moon","atom","robot","student",
            "teacher","car","tree","planet","galaxy"
        ]

        for k in keywords:
            if k in text:
                objects.append(k)

        return objects


    def detect_motion(self, text):

        if "orbit" in text:
            return "orbital"

        if "moving" in text:
            return "linear motion"

        if "rotating" in text:
            return "rotation"

        return "static"
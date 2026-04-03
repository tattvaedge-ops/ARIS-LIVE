from aris_agents import route_agent
from aris_tasks import detect_task


class ARISGoalEngine:

    def __init__(self):
        print("ARIS Goal Engine Activated")

    def execute_goal(self, user_goal):

        print("Goal received:", user_goal)

        # Step 1: Break goal into tasks
        plan = self.plan_goal(user_goal)

        results = []

        for step in plan:

            print("Executing step:", step)

            task = detect_task(step)

            result = route_agent(task, step)

            results.append(result)

        final_output = "\n".join(results)

        return final_output


    def plan_goal(self, goal):

        goal = goal.lower()

        if "youtube video" in goal:

            return [
                "write a youtube script about " + goal,
                "generate images for " + goal,
                "create narration for " + goal,
                "build video from images and narration"
            ]

        if "presentation" in goal:

            return [
                "research topic " + goal,
                "write slide content for " + goal,
                "generate presentation structure"
            ]

        return [goal]
from aris_brain import ask_ai


def planner_agent(user_input):

    prompt = f"""
You are ARIS Planner Agent.

Your job is to break the user's request into clear step-by-step actions.

User request:
{user_input}

Return a structured plan with numbered steps.
"""

    response = ask_ai(prompt)

    return response
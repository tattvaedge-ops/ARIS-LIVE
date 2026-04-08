from aris_brain import ask_ai


def research_agent(user_input):

    prompt = f"""
You are ARIS Research Agent.

Your role is to explain topics clearly and accurately.

User request:
{user_input}

Provide a simple and structured explanation.
"""

    return ask_ai(prompt)
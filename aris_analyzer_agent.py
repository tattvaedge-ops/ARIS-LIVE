from aris_brain import ask_ai


def analyzer_agent(user_input):

    prompt = f"""
You are ARIS Analyzer Agent.

Your role is to analyze information, data,
business ideas, or complex topics.

User request:
{user_input}

Provide clear insights and analysis.
"""

    return ask_ai(prompt)
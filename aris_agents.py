from aris_engines.aris_creation_agent import creation_agent
from aris_engines.aris_research_agent import research_query


def route_agent(task, user_input):

    if task == "creation":
        return creation_agent(user_input)

    return "No suitable agent found."

    
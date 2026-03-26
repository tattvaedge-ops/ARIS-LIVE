from aris_creation_agent import creation_agent


def route_agent(task, user_input):

    if task == "creation":
        return creation_agent(user_input)

    return "No suitable agent found."
def smart_prompt(user_input, mode, task):

    if mode == "student" and task == "image":
        return f"Educational labeled diagram of {user_input}, textbook style, clear arrows, high clarity"

    if mode == "creator" and task == "image":
        return f"Ultra cinematic {user_input}, dramatic lighting, masterpiece, high detail"

    if mode == "professional" and task == "write":
        return f"Professional business-grade content for {user_input}"

    return user_input
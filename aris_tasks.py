def detect_task(user_input):

    user_input = user_input.lower()

    if "generate image" in user_input or "create image" in user_input:
        return "creation"

    if "generate video" in user_input or "create video" in user_input:
        return "video"

    if "file" in user_input:
        return "file_task"

    if "remember" in user_input:
        return "memory_task"

    return "general"
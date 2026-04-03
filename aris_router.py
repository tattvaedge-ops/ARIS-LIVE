def route_request(msg):

    m = msg.lower()

    # 🎨 IMAGE
    if any(x in m for x in [
        "image", "poster", "thumbnail",
        "generate image", "create image", "picture"
    ]):
        return "image"

    # 🎬 VIDEO
    if any(x in m for x in [
        "video", "reel", "animation", "generate video"
    ]):
        return "video"

    # 🔬 RESEARCH
    if any(x in m for x in [
        "research", "paper", "journal", "analysis"
    ]):
        return "research"

    # 🎓 STUDY
    if any(x in m for x in [
        "physics", "math", "chemistry",
        "question", "solve", "numerical"
    ]):
        return "study"

    return "chat"
def detect_intent(msg):

    m = msg.lower()

    if any(x in m for x in ["image","draw","picture","photo"]):
        return "creator_image"

    if any(x in m for x in ["study","exam","physics","math","chemistry"]):
        return "student"

    if any(x in m for x in ["research","paper","analysis"]):
        return "research"

    return "general"
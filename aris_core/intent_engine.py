def detect_intent(msg):

    m = msg.lower()

    # ===== 🎨 IMAGE =====
    if any(x in m for x in [
        "generate image", "create image", "make image",
        "draw", "picture", "photo", "illustration", "art"
    ]):
        return "creator_image"

    # ===== 🎬 VIDEO =====
    if any(x in m for x in [
        "video", "reel", "animation", "short video", "clip"
    ]):
        return "video"

    # ===== 🎓 STUDENT =====
    if any(x in m for x in [
        "solve", "equation", "question", "numerical",
        "math", "physics", "chemistry", "biology",
        "derivative", "integration", "integral",
        "algebra", "calculus", "problem"
    ]):
        return "student"

    # ===== 🔬 RESEARCH =====
    if any(x in m for x in [
        "research", "analysis", "explain in detail",
        "deep dive", "study about", "investigate",
        "report", "thesis", "paper"
    ]):
        return "research"

    # ===== 🧠 DEFAULT =====
    return "general"
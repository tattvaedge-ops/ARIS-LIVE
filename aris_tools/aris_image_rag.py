# ===== ARIS IMAGE RAG ENGINE =====


def get_brand_assets(prompt):

    p = prompt.lower()

    if "tattva" in p:
        return """
Brand: Tattva Edge
Theme: Premium academic
Colors: Orange, Blue
Audience: Students
Style: Modern educational
"""

    if "aris" in p:
        return """
Brand: ARIS Nexus
Theme: Futuristic AI
Colors: Dark blue, Gold, Orange
Style: Premium intelligence system
"""

    return ""


def get_educational_context(prompt):

    p = prompt.lower()

    if any(word in p for word in [
        "biology", "physics", "chemistry",
        "diagram", "human", "cell",
        "heart", "brain", "dna"
    ]):
        return """
Style: Academic textbook
Accuracy: High
Audience: Students
Format: Label-friendly
"""

    return ""


def get_creator_context(prompt):

    p = prompt.lower()

    if any(word in p for word in [
        "thumbnail", "poster", "banner",
        "flyer", "logo", "branding"
    ]):
        return """
Style: High engagement
Visual quality: Premium
Composition: Modern
Commercial use: Yes
"""

    return ""


def get_image_rag_context(prompt):

    brand_context = get_brand_assets(prompt)
    edu_context = get_educational_context(prompt)
    creator_context = get_creator_context(prompt)

    return f"""
{brand_context}

{edu_context}

{creator_context}
"""
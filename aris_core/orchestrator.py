from aris_core.intent_engine import detect_intent

def run_orchestrator(user_id, msg):

    intent = detect_intent(msg)

    print("🧠 INTENT:", intent)

    if intent == "student":
        return f"🎓 Student Engine will handle this: {msg}"

    elif intent == "creator_image":
        return f"🎨 Image Engine will handle this: {msg}"

    elif intent == "research":
        return f"🔬 Research Engine will handle this: {msg}"

    else:
        return f"🧠 General response: {msg}"
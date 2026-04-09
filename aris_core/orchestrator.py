from aris_core.intent_engine import detect_intent
from aris_v2 import ask_openai
from aris_engines.aris_research_agent import research_query

def orchestrate_request(user_id, message):

    intent = detect_intent(message)

    print("🧠 INTENT:", intent)

    try:
        # ===== 🎓 STUDENT ENGINE =====
        if intent == "student":
            from aris_engines.student_engine import solve_student_query
            result = solve_student_query(message)

            return {
                "status": "handled",
                "response": result
            }

        # ===== 🎨 IMAGE ENGINE =====
        elif intent in ["creator_image", "image"]:
            from aris_tools.aris_image_engine import generate_image
            image_url = generate_image(message)

            if image_url:
                response = f"""
🎨 ARIS IMAGE GENERATED

🧠 Prompt:
{message}

🖼️ Image:
<img src="{image_url}" style="max-width:300px; border-radius:10px;"/>

⬇️ Download:
<a href="{image_url}" download>Download Image</a>
"""
            else:
                response = "❌ Image generation failed"

            return {
                "status": "handled",
                "response": response
            }

        # ===== 🔬 RESEARCH ENGINE =====
        elif intent == "research":
            from aris_engines.research_agent import research_query

            result = research_query(message, ask_openai)

            return {
                "status": "handled",
                "response": result
            }

        # ===== 🎬 VIDEO ENGINE =====
        elif intent == "video":
            from aris_tools.video_ai import generate_ai_video
            result = generate_ai_video(message)

            return {
                "status": "handled",
                "response": result
            }

        # ===== ❌ NOT HANDLED =====
        else:
            return {
                "status": "not_handled"
            }

    except Exception as e:
        print("❌ ORCHESTRATOR FAILURE:", str(e))

        return {
            "status": "error",
            "response": "⚠️ Engine execution failed"
        }
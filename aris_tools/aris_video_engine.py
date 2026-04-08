import requests

OLLAMA_URL = "http://localhost:11434/api/generate"


def generate_video(topic):

    prompt = f"""
You are an educational video director.

Create a cinematic storyboard for a 1-minute educational video about:

{topic}

Rules:
- 5 scenes
- each scene must describe visuals
- scenes should look cinematic and educational

Format:

Scene 1:
Scene 2:
Scene 3:
Scene 4:
Scene 5:
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "tinyllama",
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )

        data = response.json()
        script = data.get("response", "Script generation failed.")

        return f"""
🎬 ARIS VIDEO CREATION ENGINE

Topic: {topic}

Generating cinematic scenes...

{script}

Next Step: Rendering AI Video...
"""

    except Exception as e:
        return f"Video Engine Error: {str(e)}"
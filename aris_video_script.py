from aris_brain import ask_ai


def generate_video_script(topic):

    prompt = f"""
You are ARIS Video Script Engine.

Create a SHORT educational video script.

Topic: {topic}

STRICT RULES:
- Total video length: 60 seconds
- Maximum scenes: 6
- Clear definition
- Only ONE real-life example
- Clear explanation
- Short summary
- High visual clarity
- Avoid unnecessary storytelling

FORMAT:

[SCENE 1]
Visual: cinematic intro
Narrator: introduce the topic

[SCENE 2]
Visual: concept diagram
Narrator: explain definition

[SCENE 3]
Visual: real life example
Narrator: show example

[SCENE 4]
Visual: explanation animation
Narrator: explain how concept works

[SCENE 5]
Visual: concept reinforcement
Narrator: reinforce idea

[SCENE 6]
Visual: clean summary scene
Narrator: short recap

Return ONLY the scenes.
"""

    return ask_ai(prompt)
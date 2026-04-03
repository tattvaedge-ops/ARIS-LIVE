import ollama
import json
import datetime
import os

MEMORY_FILE = "aris_learning_memory.json"


def store_video_data(topic, prompts, video_file):

    record = {
        "topic": topic,
        "prompts": prompts,
        "video_file": video_file,
        "timestamp": str(datetime.datetime.now())
    }

    if os.path.exists(MEMORY_FILE):

        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)

    else:
        data = []

    data.append(record)

    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print("ARIS MEMORY UPDATED")


def evaluate_video(topic, prompts):

    prompt = f"""
You are an AI video quality evaluator.

Topic: {topic}

Visual prompts used:
{prompts}

Evaluate the video generation strategy.

Return:

VISUAL_QUALITY
CONCEPT_CLARITY
SCENE_LOGIC
SUGGESTED_IMPROVEMENTS
"""

    response = ollama.chat(
        model="phi3:mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]
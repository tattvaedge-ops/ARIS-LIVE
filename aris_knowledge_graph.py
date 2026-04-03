import ollama


def generate_knowledge_graph(topic):

    prompt = f"""
You are an expert knowledge architect.

Build a knowledge graph for the concept: {topic}

Return the structure using this format:

CORE_CONCEPT
PREREQUISITES
RELATED_CONCEPTS
ADVANCED_CONCEPTS
REAL_WORLD_APPLICATIONS

Keep it short and educational.
Do not include explanations outside the sections.
"""

    response = ollama.chat(
        model="phi3:mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]
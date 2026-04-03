# ================= ARIS STUDENT ENGINE =================

def detect_subject(question):

    q = question.lower()

    if any(x in q for x in ["integral", "derivative", "equation", "algebra", "trigonometry", "matrix"]):
        return "Mathematics"

    if any(x in q for x in ["force", "velocity", "acceleration", "newton", "energy", "current", "motion"]):
        return "Physics"

    if any(x in q for x in ["reaction", "molecule", "acid", "base", "compound", "chemical"]):
        return "Chemistry"

    if any(x in q for x in ["cell", "organism", "photosynthesis", "respiration", "biology"]):
        return "Biology"

    return "General"


def build_student_prompt(question, subject):

    return f"""
Answer the following academic question clearly and in a structured way.

Subject: {subject}

Question:
{question}

Provide the answer in this format:

📚 Concept:
Explain the concept simply.

🧠 Step-by-Step Solution:
Give clear steps.

📌 Final Answer:
State the final answer clearly.

🎯 Exam Tip:
Give one useful tip.
"""


def solve_academic_question(question, ask_ollama_func):

    subject = detect_subject(question)

    prompt = build_student_prompt(question, subject)

    answer = ask_ollama_func(prompt)

    return f"""
🎓 ARIS STUDENT AI

📖 Subject: {subject}

{answer}
"""
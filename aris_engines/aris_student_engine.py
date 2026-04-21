# ================= ARIS STUDENT ENGINE =================

def detect_subject(question):

    q = question.lower()

    if any(x in q for x in [
        "integral", "derivative", "equation", "algebra",
        "trigonometry", "matrix", "probability", "calculus"
    ]):
        return "Mathematics"

    if any(x in q for x in [
        "force", "velocity", "acceleration", "newton",
        "energy", "current", "motion", "electrostatic",
        "work", "power", "gravity", "height"
    ]):
        return "Physics"

    if any(x in q for x in [
        "reaction", "molecule", "acid", "base",
        "compound", "chemical", "organic", "salt"
    ]):
        return "Chemistry"

    if any(x in q for x in [
        "cell", "organism", "photosynthesis",
        "respiration", "biology", "dna", "genetics"
    ]):
        return "Biology"

    return "General"


def build_student_prompt(question, subject):

    return f"""
You are ARIS Student AI Premium.

Solve the question accurately.

Subject: {subject}

Question:
{question}

STRICT RULES:
- Return plain text only.
- No markdown headings.
- No latex formatting.
- No long theory unless asked.
- Keep response premium, clean, concise.
- If MCQ, give correct option first.
- Final answer must come first.
- Use exact emojis below.

OUTPUT FORMAT:

✅ Final Answer:
(one-line direct answer)

📘 Concept:
(short explanation)

📝 Step-by-Step Solution:
1.
2.
3.

🎯 Exam Tip:
(one smart shortcut/tip)
"""


def solve_academic_question(question, ask_openai_func):

    subject = detect_subject(question)

    prompt = build_student_prompt(question, subject)

    answer = ask_openai_func(prompt).strip()

    return f"""🎓 ARIS STUDENT AI

📖 Subject: {subject}

{answer}
"""
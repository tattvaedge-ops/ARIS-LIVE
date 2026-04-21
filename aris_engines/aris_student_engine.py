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
        "work", "power", "gravity"
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

Solve the academic question accurately.

Subject: {subject}

Question:
{question}

Rules:
- Keep answer clean and premium.
- If MCQ, identify correct option first.
- Avoid unnecessary long paragraphs.
- Use simple student-friendly language.
- Be accurate.

Output Format:

✅ Final Answer:
(Direct answer first)

📘 Concept:
(Short concept explanation)

📝 Step-by-Step Solution:
1.
2.
3.

🎯 Exam Tip:
(One smart exam tip)
"""


def solve_academic_question(question, ask_openai_func):

    subject = detect_subject(question)

    prompt = build_student_prompt(question, subject)

    answer = ask_openai_func(prompt)

    return f"""
🎓 ARIS STUDENT AI

📖 Subject: {subject}

{answer.strip()}
"""
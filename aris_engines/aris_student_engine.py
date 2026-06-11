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

Subject: {subject}

Question:
{question}

Respond EXACTLY in this plain text format only.

🎓 ARIS STUDENT AI

📖 Subject: {subject}

✅ Final Answer:
(Direct answer only)

📘 Concept:
(Max 2 lines)

📝 Step-by-Step Solution:
1. ...
2. ...
3. ...

🎯 Exam Tip:
(One short tip)

Rules:
- No markdown
- No headings
- No latex
- No extra explanation
- Keep concise
- Keep premium
"""


def solve_academic_question(question, ask_openai_func):

    subject = detect_subject(question)

    q = question.lower()

    # Career Guidance
    if any(x in q for x in [
        "jee",
        "neet",
        "career",
        "doctor",
        "engineer",
        "stream",
        "future"
    ]):

        prompt = f"""
You are ARIS Student Career Mentor.

Student Query:
{question}

Respond naturally.

Act like an experienced career counsellor.

Do NOT use:

Final Answer
Concept
Step-by-Step Solution
Exam Tip

Instead:

1. Understand the student's situation.
2. Compare options if relevant.
3. Ask follow-up questions if needed.
4. Guide the student toward a decision.
5. Be conversational and helpful.
"""

        return ask_openai_func(prompt)

    # Default Academic Mode
    prompt = build_student_prompt(question, subject)

    answer = ask_openai_func(prompt).strip()

    return f"""🎓 ARIS STUDENT AI

📖 Subject: {subject}

{answer}
"""
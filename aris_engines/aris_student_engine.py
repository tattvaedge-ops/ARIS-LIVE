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

    # ==========================
    # CAREER GUIDANCE MODE
    # ==========================
    if any(x in q for x in [
        "jee",
        "neet",
        "career",
        "doctor",
        "engineer",
        "stream",
        "future profession"
    ]):

        prompt = f"""
You are ARIS Career Mentor.

Student Query:
{question}

Behave like an experienced career counsellor.

Do not give a robotic answer.

Understand the student's situation.

If important information is missing,
ask follow-up questions first.

Help the student think through the decision.

Be conversational, practical and supportive.
"""

        return ask_openai_func(prompt)

    # ==========================
    # STUDY PLANNING MODE
    # ==========================
    elif any(x in q for x in [
        "study plan",
        "timetable",
        "schedule",
        "how should i study",
        "preparation strategy"
    ]):

        prompt = f"""
You are ARIS Academic Mentor.

Student Query:
{question}

Behave like a top academic mentor.

If important information is missing,
ask follow-up questions first.

Create personalized guidance.

Focus on strategy, planning and improvement.
"""

        return ask_openai_func(prompt)

    # ==========================
    # DEFAULT ACADEMIC MODE
    # ==========================
    prompt = build_student_prompt(question, subject)

    answer = ask_openai_func(prompt).strip()

    return f"""🎓 ARIS STUDENT AI

📖 Subject: {subject}

{answer}
"""
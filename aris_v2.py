from flask import Flask, render_template_string, request, jsonify, send_from_directory, session, redirect
from aris_coordinator import ARISCoordinator
import sqlite3
import datetime
import requests
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
try:
    import pytesseract
except:
    pytesseract = None
from PIL import Image
from aris_engines.aris_student_engine import solve_academic_question
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
load_dotenv()
import jwt
import datetime
from aris_tools.aris_image_engine import generate_image
from aris_tools.voice_input import speech_to_text
from aris_tools.aris_voice_engine import generate_voice
from flask import request, send_file, jsonify

JWT_SECRET = os.getenv("SECRET_KEY")
JWT_ALGO = "HS256"

def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)

def verify_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        return payload["user_id"]
    except:
        return None

print("API KEY LOADED SUCCESSFULLY")  # Safe log

from openai import OpenAI
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("❌ OPENAI_API_KEY NOT FOUND")

client = OpenAI(api_key=api_key)


app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")
if not app.secret_key:
    raise ValueError("❌ SECRET_KEY NOT SET")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_COOKIE_SECURE"] = False  # True later in production (HTTPS)
app.config["SESSION_COOKIE_HTTPONLY"] = True

# Initialize ARIS Coordinator
coordinator = ARISCoordinator()

# ===== ARIS GLOBAL CONTROL =====
ARIS_ACTIVE = True


# ===== FILE UPLOAD SYSTEM =====
UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# ================= DATABASE =================
def init_db():

    conn = sqlite3.connect("aris_memory.db")
    c = conn.cursor()

    # ---------------- USERS ----------------
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            password TEXT,
            created_at TEXT
        )
    """)

    # ---------------- TOKEN WALLET ----------------
    c.execute("""
        CREATE TABLE IF NOT EXISTS token_wallet(
            user_id INTEGER PRIMARY KEY,
            balance INTEGER DEFAULT 20
        )
    """)

    # ---------------- USAGE LOGS ----------------
    c.execute("""
        CREATE TABLE IF NOT EXISTS usage_logs(
            user_id INTEGER,
            tokens_used INTEGER,
            timestamp TEXT
        )
    """)

    # ---------------- LIVE USERS ----------------
    c.execute("""
        CREATE TABLE IF NOT EXISTS live_users(
            user_id INTEGER PRIMARY KEY,
            last_seen TEXT
        )
    """)

    # ---------------- CONVERSATION MEMORY ----------------
    c.execute("""
        CREATE TABLE IF NOT EXISTS conversation_memory(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            role TEXT,
            message TEXT,
            timestamp TEXT
        )
    """)

    # ---------------- USER MEMORY ----------------
    c.execute("""
        CREATE TABLE IF NOT EXISTS user_memory(
            user_id INTEGER PRIMARY KEY,
            goals TEXT,
            preferences TEXT,
            updated_at TEXT
        )
    """)

    # ---------------- USER TASK MEMORY ----------------
    c.execute("""
        CREATE TABLE IF NOT EXISTS user_tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            task TEXT,
            status TEXT,
            updated_at TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

def create_user(email, password):

    conn = sqlite3.connect("aris_memory.db")
    c = conn.cursor()

    try:
        hashed_password = generate_password_hash(password)

        c.execute(
            "INSERT INTO users (email, password, created_at) VALUES (?, ?, ?)",
            (email, hashed_password, str(datetime.datetime.now()))
        )

        conn.commit()

        user_id = c.lastrowid

        c.execute(
            "INSERT INTO token_wallet VALUES (?, ?)",
            (user_id, 20)
        )

        conn.commit()
        conn.close()

        return user_id

    except:
        conn.close()
        return None


def save_user_task(user_id, task):

    conn = sqlite3.connect("aris_memory.db")
    c = conn.cursor()

    c.execute("""
    INSERT INTO user_tasks (user_id, task, status, updated_at)
    VALUES (?, ?, 'active', ?)
    """, (
        user_id,
        task,
        str(datetime.datetime.now())
    ))

    conn.commit()
    conn.close()

def get_last_task(user_id):

    conn = sqlite3.connect("aris_memory.db")
    c = conn.cursor()

    c.execute("""
    SELECT task FROM user_tasks
    WHERE user_id=? AND status='active'
    ORDER BY id DESC
    LIMIT 1
    """, (user_id,))

    row = c.fetchone()

    conn.close()

    return row[0] if row else None

def authenticate_user(email, password):

    conn = sqlite3.connect("aris_memory.db", check_same_thread=False)
    c = conn.cursor()

    c.execute("SELECT id, password FROM users WHERE email=?", (email,))
    row = c.fetchone()

    conn.close()

    if row:
        user_id, hashed_password = row

        if check_password_hash(hashed_password, password):
            return user_id

    return None

# ================= TOKEN SYSTEM =================

def get_tokens(user_id):
    conn = sqlite3.connect("aris_memory.db")
    c = conn.cursor()
    c.execute("SELECT balance FROM token_wallet WHERE user_id=?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else 0


def deduct_token(user_id, amount):

    conn = sqlite3.connect("aris_memory.db")
    c = conn.cursor()

    c.execute("""
        UPDATE token_wallet
        SET balance = balance - ?
        WHERE user_id=? AND balance >= ?
    """, (amount, user_id, amount))

    success = c.rowcount

    conn.commit()
    conn.close()

    return success > 0


def log_usage(user_id, tokens):
    conn = sqlite3.connect("aris_memory.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO usage_logs VALUES (?,?,?)",
        (user_id, tokens, str(datetime.datetime.now())),
    )
    conn.commit()
    conn.close()


# ================= LIVE USER TRACKING =================
def update_last_seen(user_id):
    conn = sqlite3.connect("aris_memory.db")
    c = conn.cursor()

    c.execute("""
        INSERT OR REPLACE INTO live_users(user_id, last_seen)
        VALUES (?, ?)
    """, (user_id, str(datetime.datetime.now())))

    conn.commit()
    conn.close()

# ================= MEMORY ENGINE =================

def save_message(user_id, role, message):
    conn = sqlite3.connect("aris_memory.db")
    c = conn.cursor()

    c.execute("""
        INSERT INTO conversation_memory
        (user_id, role, message, timestamp)
        VALUES (?, ?, ?, ?)
    """, (
        user_id,
        role,
        message,
        str(datetime.datetime.now())
    ))

    conn.commit()
    conn.close()


def get_recent_memory(user_id, limit=6):
    conn = sqlite3.connect("aris_memory.db")
    c = conn.cursor()

    c.execute("""
        SELECT role, message
        FROM conversation_memory
        WHERE user_id=?
        ORDER BY id DESC
        LIMIT ?
    """, (user_id, limit))

    rows = c.fetchall()
    conn.close()

    rows.reverse()

    history = ""
    for r in rows:
        history += f"{r[0].upper()}: {r[1]}\n"

    return history


def save_user_goal(user_id, goal):
    conn = sqlite3.connect("aris_memory.db")
    c = conn.cursor()

    c.execute("""
        INSERT OR REPLACE INTO user_memory
        (user_id, goals, updated_at)
        VALUES (?, ?, ?)
    """, (
        user_id,
        goal,
        str(datetime.datetime.now())
    ))

    conn.commit()
    conn.close()


def get_user_goal(user_id):
    conn = sqlite3.connect("aris_memory.db")
    c = conn.cursor()

    c.execute("""
        SELECT goals FROM user_memory
        WHERE user_id=?
    """, (user_id,))

    row = c.fetchone()
    conn.close()

    return row[0] if row else ""

# ================= ONLINE USERS COUNT =================
def get_live_users():
    conn = sqlite3.connect("aris_memory.db")
    c = conn.cursor()

    cutoff = datetime.datetime.now() - datetime.timedelta(seconds=60)

    c.execute("""
        SELECT COUNT(*) FROM live_users
        WHERE last_seen >= ?
    """, (str(cutoff),))

    count = c.fetchone()[0]
    conn.close()

    return count

    # ================= PROFIT INTELLIGENCE =================
ARIS_PRICE_MONTHLY = 199          # subscription price
AI_COST_PER_TOKEN = 0.02          # estimated AI cost (₹)

def get_profit_metrics():

    conn = sqlite3.connect("aris_memory.db")
    c = conn.cursor()

    # total users
    c.execute("SELECT COUNT(*) FROM users")
    users = c.fetchone()[0]

    # tokens used
    c.execute("SELECT SUM(tokens_used) FROM usage_logs")
    used = c.fetchone()[0] or 0

    conn.close()

    # calculations
    revenue = users * ARIS_PRICE_MONTHLY
    ai_cost = used * AI_COST_PER_TOKEN
    profit = revenue - ai_cost

    avg_user_value = revenue / users if users else 0

    return {
        "users": users,
        "revenue": round(revenue, 2),
        "ai_cost": round(ai_cost, 2),
        "profit": round(profit, 2),
        "avg_user_value": round(avg_user_value, 2),
        "tokens_used": used
    }



# ================= OPENAI BRAIN =================

def ask_openai(prompt):

    try:

        if len(prompt) < 800:
            max_tokens = 700
        elif len(prompt) < 2000:
            max_tokens = 900
        else:
            max_tokens = 1200

        # 🔥 STRONG SYSTEM BRAIN
        system_prompt = """
You are ARIS (Advanced Real-Time Integrated System) — a high-level AI intelligence engine.

Rules you MUST follow:

1. Always respond as if it is the year 2026 (latest real-world context)
2. NEVER say "my knowledge cutoff is 2023" or similar
3. Give clear, structured, and practical answers
4. Use headings, bullet points, and clean formatting
5. Focus on real-world insights, not textbook theory
6. Speak with confidence like an expert system
7. Avoid generic chatbot tone
8. If topic is business, tech, education → give strategic insights
9. Keep answers crisp but powerful

Your goal:
Act like a real-world decision-making intelligence system, not a chatbot.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=max_tokens
        )

        if not response or not response.choices:
            return "__OPENAI_ERROR__"

        content = response.choices[0].message.content

        if not content:
            return "__OPENAI_ERROR__"

        return content.strip()

    except Exception as e:
        print("🔥 OPENAI ERROR:", str(e))
        return f"❌ OPENAI ERROR: {str(e)}"
        
# ================= AVATAR GENERATION =================
def generate_avatar(image_path, style_prompt):

    try:
        import base64
        import uuid

        response = client.images.generate(
            model="gpt-image-1",
            prompt=f"Create a realistic AI avatar portrait of a person: {style_prompt}, ultra detailed, cinematic lighting, 4K",
            size="1024x1024"
        )

        image_base64 = response.data[0].b64_json

        filename = f"avatar_{uuid.uuid4().hex}.png"
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        with open(filepath, "wb") as f:
            f.write(base64.b64decode(image_base64))

        image_url = f"/uploads/{filename}"

        return f"""
🔥 ARIS AVATAR GENERATED

🎨 Style:
{style_prompt}

🖼️ Avatar:
<a href="{image_url}" target="_blank">View Avatar</a>

⬇️ Download:
<a href="{image_url}" download>Download Avatar</a>
"""

    except Exception as e:
        print("🔥 AVATAR ERROR:", str(e))   # ✅ DEBUG
        return f"❌ Avatar generation error: {str(e)}"


# ================= OCR QUESTION ENGINE =================

def extract_text_from_image(image_path):

    if pytesseract is None:
        return "⚠️ OCR not available in cloud mode"

    try:
        img = Image.open(image_path)

        text = pytesseract.image_to_string(img)

        return text.strip()

    except Exception as e:
        return f"OCR Error: {str(e)}"


from aris_engines.aris_student_engine import solve_academic_question

def solve_question_from_image(image_path, user_id=None):

    question_text = extract_text_from_image(image_path)

    if not question_text or len(question_text) < 5:
        return "⚠️ ARIS could not detect a valid question from the image."

    # 🚀 NEW STRUCTURED STUDENT AI
    answer = solve_academic_question(
        question_text,
        ask_openai
    )

    return f"""📸 Question Detected:

{question_text}

{answer}
"""

# ================= INTENT DETECTION =================
def detect_intent(msg):

    m = msg.lower()

    # 🎨 IMAGE GENERATION (KEEP THIS FIRST — HIGH PRIORITY)
    if any(x in m for x in [
        "generate image", "create image", "image", "img",
        "picture", "photo", "draw", "diagram"
    ]):
        return "creator_image"

    # 🎓 STUDENT
    if any(x in m for x in [
        "study", "exam", "test", "concept", "physics", "math",
        "chemistry", "biology", "jee", "neet", "olympiad",
        "ntse", "nstse", "mhtcet", "sat", "semester", "assignment",
        "project", "plagiarism", "notes", "revision", "doubt"
    ]):
        return "student"

    # 💼 PROFESSIONAL
    if any(x in m for x in [
        "email", "presentation", "report", "business", "proposal",
        "startup", "marketing", "revenue", "swot", "pitch deck"
    ]):
        return "professional"

    # 🎨 CREATOR (NON-IMAGE)
    if any(x in m for x in [
        "logo", "design", "video", "thumbnail",
        "creative", "art", "poster", "caption", "script"
    ]):
        return "creator"

    # 🔬 RESEARCH
    if any(x in m for x in [
        "research", "paper", "citation", "analysis", "journal",
        "literature review", "methodology", "abstract", "thesis",
        "dissertation", "ugc", "pg", "phd"
    ]):
        return "research"

    # 🧭 LIFE
    if any(x in m for x in [
        "life", "goal", "career", "habit", "plan",
        "productivity", "decision", "schedule"
    ]):
        return "life"

    return "general"


# ================= PROMPT BUILDER =================
def build_prompt(intent, msg, memory_context="", goal_context=""):

    if intent == "creator_image":
        from aris_creation_agent import creation_agent
        return creation_agent(msg)

    if intent == "student":
        return f"""
You are ARIS Student Intelligence.

You help school students (Class 8-12), UG students, PG students, and competitive exam aspirants.

Supported exam types include JEE, NEET, Olympiads, NTSE, NSTSE, CLAT, AILET, TOEFL, IELTS, UPSC, MPSC, MHTCET, SAT, XAT, MAT, ATMA, law exams, management exams, and semester exams.

Adapt response based on user input:

- If the user asks a simple question -> give a short, clear answer.
- If the user asks for detailed explanation -> give structured detailed output.
- Do not over-explain unnecessarily.

Rules:
- Keep explanation practical and easy to understand.
- If the user asks for test, generate a useful test.
- If the user asks for notes, generate concise notes.
- If the user asks for assignment/project help, provide original academic-style content.
- Do not claim plagiarism checking unless explicitly available.
- Match difficulty to the user's likely level based on the prompt.

Structure:
Title
Explanation
Key Points
Example
Summary

Conversation:
{memory_context}

User Goal:
{goal_context}

User Request:
{msg}
"""

    if intent == "professional":
        return f"""
You are ARIS Professional Intelligence.

Provide practical professional output.

Structure:
Title
Explanation
Action Steps
Summary

Conversation:
{memory_context}

User Goal:
{goal_context}

User Request:
{msg}
"""

    if intent == "creator":
        return f"""
You are ARIS Creator Intelligence.

Generate creative and useful output.

Structure:
Idea
Description
Execution Steps
Tips

Conversation:
{memory_context}

User Goal:
{goal_context}

User Request:
{msg}
"""

    if intent == "research":
        return f"""
You are ARIS Research Intelligence.

Write in academic and analytical style.

Structure:
Title
Abstract
Explanation
Key Insights
Conclusion

Conversation:
{memory_context}

User Goal:
{goal_context}

User Request:
{msg}
"""

    if intent == "life":
        return f"""
You are ARIS Life Intelligence.

Give practical and actionable advice.

Structure:
Situation
Analysis
Recommended Actions
Summary

Conversation:
{memory_context}

User Goal:
{goal_context}

User Request:
{msg}
"""

    return f"""
You are ARIS, an intelligent AI assistant.

Adapt to user intent:
- Short question -> short answer
- Complex request -> structured response
- Avoid unnecessary long outputs

Answer clearly and directly.

Conversation:
{memory_context}

User Goal:
{goal_context}

User Question:
{msg}

Answer:
"""

# ================= ARIS BRAIN =================
def brain(msg, user_id=None):

    memory_context = ""
    goal_context = ""

    if user_id:
        memory_context = get_recent_memory(user_id)
        goal_context = get_user_goal(user_id)

    intent = detect_intent(msg)

    prompt = build_prompt(
        intent=intent,
        msg=msg,
        memory_context=memory_context,
        goal_context=goal_context
    )

    # 🔥 THIS BLOCK (4 spaces)
    response = ask_openai(prompt)

    if response in ["__OPENAI_QUOTA_ERROR__", "__OPENAI_RATE_LIMIT__", "__OPENAI_ERROR__"]:
        response = "⚠️ ARIS AI service temporarily unavailable. Please try again shortly."

    # 🧹 CLEAN OUTPUT
    bad_phrases = [
        "Conversation so far:",
        "User goal:",
        "You are ARIS",
        "Conversation:",
        "User Goal:"
    ]

    for b in bad_phrases:
        response = response.replace(b, "")

    return response.strip()

    # ================= LOW TOKEN WARNING =================
def low_token_warning(tokens_left):

    if tokens_left <= 0:
        return "⚠️ Intelligence credits exhausted."

    if tokens_left <= 3:
        return "⚡ Only a few tokens left. Recharge soon."

    if tokens_left <= 7:
        return "🧠 You are actively using ARIS. Consider adding tokens."

    return None


# ================= SUGGESTION ENGINE =================

def simulate_video(prompt):

    scenes = [
        f"🎬 Scene 1: Introduction of {prompt}",
        f"🎥 Scene 2: Core concept explained visually",
        f"📊 Scene 3: Real-world example",
        f"🚀 Scene 4: Advanced insight",
        f"🌍 Scene 5: Application in real life",
        f"✨ Scene 6: Final summary"
    ]

    return f"""
🎬 ARIS CINEMATIC VIDEO GENERATED

🧠 Topic: {prompt}

🎞️ Scenes:
{chr(10).join(scenes)}

⚡ Note:
High-quality cinematic rendering will be enabled in full version.
"""

def generate_suggestions(message):
    


    msg = message.lower()

    # ---------- 🎓 STUDENT AI (UPGRADED FLOW) ----------
    if any(x in msg for x in [
        "study","concept","physics","math","chemistry","biology",
        "jee","neet","exam","assignment","notes","revision","question"
    ]):
        return [
            "📘 Explain the concept behind this",
            "🎯 Generate similar practice questions",
            "🧪 Create a mini test from this topic",
            "🎬 Give visual step-by-step explanation",
            "📝 Make short revision notes"
        ]

    # ---------- 💼 PROFESSIONAL ----------
    if any(x in msg for x in [
        "business","startup","strategy","revenue","marketing","plan"
    ]):
        return [
            "Create business plan",
            "Build revenue model",
            "Run SWOT analysis",
            "Generate pitch deck outline"
        ]

    # ---------- 🎨 CREATOR ----------
    if any(x in msg for x in [
        "logo","design","image","video","thumbnail","creative"
    ]):
        return [
            "Generate image prompt ideas",
            "Create video/reel concept",
            "Write creative caption",
            "Suggest color palette"
        ]

    # ---------- 🔬 RESEARCH ----------
    if any(x in msg for x in [
        "research","analysis","paper","journal","study data"
    ]):
        return [
            "Generate research outline",
            "Create literature review",
            "Summarize key insights",
            "Build comparison table"
        ]

    # ---------- 🧭 LIFE ----------
    if any(x in msg for x in [
        "goal","career","life","decision","habit"
    ]):
        return [
            "Create 30-day action plan",
            "Build decision matrix",
            "Define next priorities",
            "Generate daily routine"
        ]

    # ---------- DEFAULT ----------
    return [
        "Break this into steps",
        "Explain in simple terms",
        "Create structured plan"
    ]

def process_ai_request(user_id, msg):
    print("🔥 PROCESS_AI_REQUEST CALLED")

    print("MSG:", msg)

    if not ARIS_ACTIVE:
        return {
            "reply": "⚠️ ARIS is temporarily paused by the system administrator.",
            "suggestions": [],
            "tokens_left": get_tokens(user_id)
        }

    tokens = get_tokens(user_id)

    if tokens <= 0:
        return {
            "reply": "⚠️ Intelligence credits exhausted.",
            "suggestions": [],
            "tokens_left": 0
        }

    # ===== TOKEN COST LOGIC =====
    token_cost = 1
    msg_lower = msg.lower()

    if any(x in msg_lower for x in ["generate image", "create image", "make image", "draw an image", "draw a picture"]):
        token_cost = 7

    elif any(x in msg_lower for x in ["video", "reel", "animation", "generate video"]):
        token_cost = 20

    elif any(x in msg_lower for x in ["research paper", "literature review", "journal", "citation", "methodology", "thesis", "dissertation"]):
        token_cost = 3

    elif any(x in msg_lower for x in ["pdf", "file", "document"]):
        token_cost = 5

    # ===== CHECK TOKENS =====
    if tokens < token_cost:
        return {
            "reply": f"⚠️ This action requires {token_cost} tokens. You have {tokens}. Please recharge.",
            "suggestions": [],
            "tokens_left": tokens
        }

    # ===== 🚀 ORCHESTRATOR ROUTING (NEW CORE FIX) =====
    try:
        from aris_core.orchestrator import orchestrate_request

        result = orchestrate_request(user_id=user_id, message=msg)

        if result and isinstance(result, dict) and result.get("status") == "handled":
            reply = result.get("response")

        else:
            print("⚠️ ORCHESTRATOR FALLBACK → OpenAI")
            reply = brain(msg, user_id)

    except Exception as e:
        print("❌ ORCHESTRATOR ERROR:", str(e))
        reply = brain(msg, user_id)

    # ===== TOKEN DEDUCTION =====
    deduct_token(user_id, token_cost)
    log_usage(user_id, token_cost)

    tokens_left = get_tokens(user_id)

    suggestions = generate_suggestions(msg)

    print("FINAL REPLY:", reply)

    return {
        "reply": reply,
        "suggestions": suggestions,
        "tokens_left": tokens_left
    }


# ================= LOGIN PAGE =================
LOGIN_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>ARIS Login</title>

<!-- Lottie Animation -->
<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>

<!-- Particles -->
<script src="https://cdn.jsdelivr.net/npm/tsparticles@2/tsparticles.bundle.min.js"></script>

<style>
body{
margin:0;
font-family: "Segoe UI", Arial, sans-serif;
background:#0a192f;
color:white;
display:flex;
justify-content:center;
align-items:center;
height:100vh;
overflow:hidden;
}

/* FLOATING GLOW */
body::before{
content:"";
position:fixed;
width:600px;
height:600px;
background:radial-gradient(circle, rgba(249,115,22,0.25), transparent 70%);
top:-150px;
left:-150px;
animation:floatGlow 8s ease-in-out infinite;
z-index:-2;
}
body::after{
content:"";
position:fixed;
width:700px;
height:700px;
background:radial-gradient(circle, rgba(249,115,22,0.15), transparent 70%);
bottom:-200px;
right:-200px;
animation:floatGlow 10s ease-in-out infinite reverse;
z-index:-2;
}
@keyframes floatGlow{
0%{transform:translateY(0px);}
50%{transform:translateY(30px);}
100%{transform:translateY(0px);}
}

/* WAVE */
.wave{
position:fixed;
width:200%;
height:200%;
background:linear-gradient(120deg, transparent, rgba(249,115,22,0.08), transparent);
animation:waveMove 12s linear infinite;
z-index:-3;
}
@keyframes waveMove{
0%{transform:translateX(-25%) translateY(-25%);}
100%{transform:translateX(25%) translateY(25%);}
}

/* PARTICLES */
#tsparticles{
position:absolute;
width:100%;
height:100%;
z-index:0;
pointer-events:none;
}

/* LOGIN CARD */
.login-box{
text-align:center;
background:rgba(255,255,255,0.06);
padding:45px 60px;
border-radius:20px;
backdrop-filter:blur(14px);
-webkit-backdrop-filter:blur(14px);
border:1px solid rgba(255,255,255,0.08);
box-shadow:
0 0 60px rgba(0,0,0,0.5),
inset 0 0 20px rgba(255,255,255,0.04);
animation:fadeUp .8s ease;
transition:.3s;
}

.login-box:hover{
transform:translateY(-2px) scale(1.01);
box-shadow:
0 0 80px rgba(249,115,22,.25),
inset 0 0 25px rgba(255,255,255,0.06);
}

/* LOGO */
.logo-box{
background:#0a192f;
padding:14px;
border-radius:18px;
border:2px solid #f97316;
box-shadow:0 0 35px rgba(249,115,22,.9);
width:200px;
margin:0 auto 50px;
}
.logo-box img{width:100%;}

/* TITLES */
.title{
font-size:28px;
font-weight:700;
margin-top:8px;
}
.subtitle{
opacity:.75;
font-size:14px;
margin-bottom:25px;
}

/* INPUT */
input{
width:260px;
padding:13px;
border-radius:10px;
border:none;
outline:none;
font-size:14px;
margin-bottom:18px;
}

/* BUTTON */
button{
padding:12px 28px;
border:none;
border-radius:10px;
background:linear-gradient(90deg,#f97316,#ff8c3a);
color:white;
font-weight:600;
cursor:pointer;
box-shadow:0 0 15px rgba(249,115,22,.6);
transition:.2s;
}
button:hover{
transform:scale(1.05);
box-shadow:0 0 30px rgba(249,115,22,1);
}

/* FOOTER */
.micro{
margin-top:18px;
font-size:12px;
opacity:.6;
}

/* ENTRY ANIMATION */
@keyframes fadeUp{
from{opacity:0; transform:translateY(25px);}
to{opacity:1; transform:translateY(0);}
}

/* PEOPLE SUCCESS BACKGROUND */
.people-bg{
position:fixed;
bottom:-40px;
left:-60px;
opacity:0.60;
z-index:-1;
pointer-events:none;
filter:blur(.3px);
}

.wow-btn{
background:#f97316;
border:none;
padding:10px 16px;
border-radius:10px;
color:white;
margin:6px 6px 0 0;
cursor:pointer;
font-weight:600;
transition:.2s;
}

.wow-btn:hover{
transform:scale(1.05);
box-shadow:0 0 12px rgba(249,115,22,.8);
}

.file-title{
color:#f97316;
font-weight:700;
font-size:16px;
margin-bottom:12px;
letter-spacing:0.6px;
}

.file-option{
color:white;
font-style:italic;
font-weight:600;
cursor:pointer;
margin:10px 0;
transition:.2s;
}

.file-option:hover{
color:#f97316;
transform:translateX(5px);
}

/* ===== ARIS WELCOME PANEL ===== */

.welcome-panel{
background:rgba(255,255,255,0.06);
backdrop-filter:blur(14px);
-webkit-backdrop-filter:blur(14px);

border:1px solid rgba(255,255,255,0.08);
border-radius:18px;

padding:26px 28px;
max-width:420px;

box-shadow:
0 0 40px rgba(0,0,0,0.5),
0 0 25px rgba(249,115,22,0.25);

animation:fadeUp .6s ease;
}

.welcome-title{
font-size:20px;
font-weight:700;
color:white;
margin-bottom:6px;
}

.welcome-sub{
opacity:.8;
margin-bottom:18px;
}

.wow-btn{
background:linear-gradient(90deg,#f97316,#ff8c3a);
border:none;
padding:10px 14px;
border-radius:10px;
color:white;
margin:6px 6px 0 0;
cursor:pointer;
font-weight:600;
transition:.25s;
}

.wow-btn:hover{
transform:translateY(-2px) scale(1.05);
box-shadow:0 0 18px rgba(249,115,22,.9);
}

</style>

</head>

<body>

<div id="tsparticles"></div>
<div class="wave"></div>

<!-- SUCCESS / STUDENT / ENTREPRENEUR ANIMATION -->
<div class="people-bg">
<lottie-player
src="https://assets7.lottiefiles.com/packages/lf20_tfb3estd.json"
background="transparent"
speed="0.7"
style="width:520px;height:520px;"
loop autoplay>
</lottie-player>
</div>

<!-- LOGIN BOX -->
<div class="login-box">

<div class="logo-box">
<img src="/logo">
</div>

<div class="title">ARIS Intelligence</div>
<div class="subtitle">Your AI Brain for Life - Study - Business</div>

<form method="POST">

<input name="email" type="email" placeholder="Email" required>
<br>

<input name="password" type="password" placeholder="Password" required>
<br>

<button name="action" value="login">
Login →
</button>

<button name="action" value="signup">
Create Account
</button>

<br><br>

<button type="button" onclick="showForgotPassword()" style="background:#444;color:#fff;padding:10px;border-radius:8px;border:none;">
Forgot Password?
</button>

<script>
function showForgotPassword() {
    const email = prompt("Enter your registered email:");

    if (!email) return;

    fetch("/forgot-password", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email: email })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
    });
}
</script>

</form>

<div style="color:#ff8c3a;margin-top:10px;">
{{error}}
</div>

<div class="micro">
Secure - Private - Personal Intelligence System
</div>

</div>

<script>
tsParticles.load("tsparticles",{
particles:{
number:{value:40},
color:{value:"#f97316"},
links:{enable:true,color:"#f97316"},
move:{speed:1}
}
});
</script>

</body>
</html>
"""
# ================= MAIN UI =================
HTML = """
<!DOCTYPE html>
<html>
<head>
<title>ARIS</title>
<script src="https://cdn.jsdelivr.net/npm/tsparticles@2/tsparticles.bundle.min.js"></script>

<style>

/* HEADER LAYOUT */
.header{
display:flex;
justify-content:space-between;
align-items:center;
padding:14px 20px;
font-size:22px;
font-weight:700;
border-bottom:1px solid rgba(255,255,255,0.05);
color:white;
flex-shrink:0;
}

/* RIGHT SIDE CONTROLS */
.header-right{
display:flex;
align-items:center;
gap:14px;
flex-shrink:0;
}

/* TOKEN ANIMATION */
.token-pulse{
animation: tokenPulse 0.45s ease;
}

@keyframes tokenPulse{
0%{
transform:scale(1);
}
40%{
transform:scale(1.25);
box-shadow:0 0 18px rgba(249,115,22,0.9);
}
100%{
transform:scale(1);
}
}

/* BUY BUTTON */
.buy-btn{
background:#f97316;
border:none;
padding:8px 16px;
border-radius:10px;
color:#0a192f;
cursor:pointer;

font-family:"Segoe UI", Arial, sans-serif;
font-size:15px;
font-weight:600;
letter-spacing:0.3px;

display:flex;
align-items:center;
justify-content:center;

transition:.2s;
}

.buy-btn:hover{
transform:scale(1.05);
box-shadow:0 0 15px rgba(249,115,22,.8);
}

.attach-btn{
background:#f97316;
border:none;
color:white;
padding:10px 14px;
border-radius:10px;
cursor:pointer;
margin-right:8px;
font-size:18px;
display:flex;
align-items:center;
justify-content:center;
transition:.2s;
}

.attach-btn:hover{
transform:scale(1.05);
box-shadow:0 0 12px rgba(249,115,22,0.8);
}

.attach-btn img{
width:28px;
height:28px;
filter: brightness(0) invert(1);
}

.attach-btn:hover{
box-shadow:0 0 14px rgba(249,115,22,.8);
transform:scale(1.05);
}

/* TOKEN BOX */
.token-box{
background:linear-gradient(90deg,#f97316,#ff8c3a);
padding:8px 16px;
border-radius:10px;

font-family:"Segoe UI", Arial, sans-serif;
font-size:15px;
font-weight:600;
letter-spacing:0.3px;

display:flex;
align-items:center;
}

body{
margin:0;
font-family:Segoe UI;
background:#0a192f;
color:#0a192f;
display:flex;
height:100vh;
overflow:hidden;
}

.profile-panel{
margin-top:10px;
padding:14px;
background:rgba(255,255,255,0.04);
border-radius:12px;
display:none;
flex-direction:column;
gap:8px;
animation:fadeUp .3s ease;
}

.profile-title{
font-size:18px;
font-weight:600;
color:white;
margin-bottom:8px;
}

.profile-info{
font-size:13px;
color:#d1d5db;
line-height:1.5;
}

.profile-btn{
margin-top:8px;
padding:10px;
border:none;
background:#f97316;
color:white;
border-radius:8px;
cursor:pointer;
font-weight:600;
}

.logout-btn{
margin-top:6px;
padding:10px;
border:none;
background:#374151;
color:white;
border-radius:8px;
cursor:pointer;
}

/* ===== LAYOUT FIX ===== */

.main{
flex:1;
display:flex;
flex-direction:column;
min-height:0;
position:relative;
}

.aris-view{
flex:1;
display:flex;
flex-direction:column;
min-height:0;
padding:0 60px;   /* ⭐ ADD THIS */
}

.aris-view{
flex:1;
display:flex;
flex-direction:column;
min-height:0;
}

.aris-view:not(.active-view){
display:none;
}

.aris-thinking{
color:#f97316;
font-style:italic;
opacity:0.9;
animation:thinkingPulse 1.2s infinite;
}

@keyframes thinkingPulse{
0%{opacity:0.3;}
50%{opacity:1;}
100%{opacity:0.3;}
}



/* SIDEBAR */
.sidebar{
width:250px;
background:linear-gradient(180deg,#071427,#0a192f);
padding:18px;
display:flex;
flex-direction:column;
overflow-y:auto;
height:100vh;
}

/* RECTANGULAR LOGO */
.logo-box{
background:#0a192f;
padding:15px;
border-radius:14px;
border:3px solid #f97316;
box-shadow:0 0 20px rgba(249,115,22,.9);
width:85%;
height:90px;
display:flex;
align-items:center;
justify-content:center;
margin-bottom:8px;
}
.logo-box img{
height:300px;
}

.logo-title{
font-size:20px;
color:#f97316;        /* ⭐ ARIS Orange */
margin-bottom:18px;
text-align:center;
font-weight:600;
letter-spacing:0.5px;
}

/* MENU */
.menu-section{
margin-bottom:14px;
padding:10px;
border-radius:10px;
cursor:pointer;
transition:.2s;
}

.menu-section:hover{
background:rgba(255,255,255,0.05);
}

.menu-section.active{
background:linear-gradient(90deg,#7a4a2b,#3a2a22);
}

.menu-section.logout{
color:#ff6b6b;
}

.menu-section.logout:hover{
background:rgba(255,80,80,0.15);
}

.menu-title{
font-weight:600;
margin-bottom:6px;
color:white;              /* ⭐ makes WORKSPACE / PLANS / ACTIVITY visible */
letter-spacing:0.5px;
}

.submenu{
display:none;
max-height:220px;
overflow-y:auto;
padding-right:4px;
}

.submenu::-webkit-scrollbar{
width:6px;
}

.submenu::-webkit-scrollbar-thumb{
background:#f97316;
border-radius:6px;
}

.menu-section.active{
background:linear-gradient(
90deg,
rgba(249,115,22,0.35),
rgba(249,115,22,0.08)
);
border-left:3px solid #f97316;
}

.menu-section{
color:white;
}

.submenu div{
font-size:14px;
color:#e5e7eb;

margin:8px 0;
padding:6px 6px 6px 22px;   /* ⭐ INDENT */

cursor:pointer;
transition:.2s;
line-height:1.6;
}

.submenu div:hover{
color:#f97316;
transform:translateX(6px);
padding-left:12px;
}

.submenu div:hover{
color:#f97316;            /* ARIS orange */
transform:translateX(4px);
}


#tsparticles{
position:absolute;
width:100%;
height:100%;
z-index:0;
}

.header{
padding:14px 20px;
font-size:22px;
font-weight:700;
letter-spacing:0.5px;
border-bottom:1px solid rgba(255,255,255,0.05);
z-index:1;
color:white;     /* ⭐ ADD THIS */
}

/* ================= PREMIUM VIEW ANIMATION ================= */




/* ================= SIDEBAR INDICATOR ================= */

.menu-section{
position:relative;
overflow:hidden;
}

.menu-section::before{
content:"";
position:absolute;
left:0;
top:0;
height:100%;
width:0px;
background:#f97316;
transition:width .3s ease;
}

.menu-section.active::before{
width:4px;
}

/* ================= MICRO TAB INTERACTION ================= */

.menu-title,
.submenu div{
transition:all .2s ease;
}

.menu-title:active,
.submenu div:active{
transform:scale(.96);
}

/* Smooth hover glow */
.menu-section.active{
box-shadow:0 0 18px rgba(249,115,22,.25);
}

/* ===== VIEW HEADINGS ===== */






/* CHAT */

#chat-container{
flex:1;
display:flex;
flex-direction:column;
min-height:0;
position:relative;
z-index:2;
}

#chat{
flex:1;
overflow-y:auto;
padding:0px 15px 15px 15px;
display:flex;
flex-direction:column;
gap:10px;
min-height:0;
}

.message.aris:first-child{
margin-top:-15px;
}

#chat{
max-width:1100px;
margin:auto;
width:100%;
}

#input-area{
display:flex;
padding:12px;
border-top:1px solid rgba(255,255,255,0.05);
background:#0a192f;
flex-shrink:0;
}

.message{
max-width:60%;
padding:12px;
border-radius:14px;
white-space:pre-wrap;
}

.user{
background:#f97316;
align-self:flex-end;
}

.aris{
background:transparent;
color:white;
align-self:flex-start;
}

.token-warning{
color:#0a192f !important;   /*#0a192f */
font-weight:700 !important; /* bold */
font-style:italic !important;
display:block;
margin-top:6px;
}

#input-area{
display:flex;
padding:12px;
border-top:1px solid rgba(255,255,255,0.05);
background:#0a192f;
position:relative;
}

#msg{
flex:1;
padding:12px;
border-radius:10px;
border:none;
}

.send{
padding:10px 18px;
border:none;
border-radius:10px;
background:#f97316;
color:white;
cursor:pointer;
margin-left:10px;
}

/* ===== ADD HERE ===== */




.welcome-panel{
background:linear-gradient(
145deg,
rgba(255,255,255,0.06),
rgba(255,255,255,0.02)
);
backdrop-filter:blur(16px);
-webkit-backdrop-filter:blur(16px);
border:1px solid rgba(249,115,22,0.25);
border-radius:20px;
padding:28px 30px;
max-width:440px;
box-shadow:
0 0 50px rgba(0,0,0,0.6),
0 0 30px rgba(249,115,22,0.35);
animation:fadeUp .6s ease;
}

.welcome-title{
font-size:22px;
font-weight:700;
color:white;
margin-bottom:6px;
}

.welcome-sub{
opacity:.85;
margin-top:20px;
margin-bottom:8px;
color:#e5e7eb;
font-size:15px;
font-weight:600;
}

.wow-btn{
background:linear-gradient(90deg,#f97316,#ff8c3a);
border:none;

padding:4px 15px;      /* ✅ reduced height */
border-radius:10px;

color:#0a192f;
font-weight:600;
font-size:15px;        /* ✅ slightly tighter text */

cursor:pointer;
transition:.25s;

box-shadow:0 6px 10px rgba(249,115,22,.35);
display:inline-flex;
align-items:center;
gap:6px;               /* ✅ icon spacing */
}

.wow-btn:hover{
transform:translateY(-2px) scale(1.04);
box-shadow:0 10px 26px rgba(249,115,22,.7);
}

.wow-container{
display:flex;
flex-wrap:wrap;
gap:16px;      /* more space between buttons */
margin-top:10px;
margin-bottom:10px;
align-items:center;
}

</style>
</head>

<body>

<div class="sidebar">

<div class="logo-box">
<img src="/logo">
</div>

<div class="logo-title">Intelligence System</div>

<!-- WORKSPACE -->
<div class="menu-section active" onclick="switchView('workspace', this)">
<div class="menu-title">WORKSPACE ⭐</div>
</div>


<!-- STUDENT AI -->
<div class="menu-section" onclick="toggleMenu(this)">
<div class="menu-title">🎓 Student AI</div>

<div class="submenu">

<!-- 🔥 MAIN CTA -->
<div onclick="triggerDoubtUpload()" style="
background:linear-gradient(90deg,#f97316,#ff8c3a);
color:#0a192f;
font-weight:700;
padding:10px;
border-radius:10px;
margin-bottom:10px;
text-align:center;
cursor:pointer;
">
📸 Upload Question / Photo
</div>

<div onclick="quickStart('Solve this question step by step')">
🧠 Solve Question
</div>

<div onclick="quickStart('Explain this concept clearly with examples')">
📘 Concept Explainer
</div>

<div onclick="quickStart('Generate exam ready notes')">
📝 Notes Generator
</div>

<div onclick="quickStart('Generate practice questions with solutions')">
🎯 Practice Questions
</div>

<div onclick="quickStart('Generate a mock test with answers')">
🧪 Mock Test
</div>

<div onclick="quickStart('Generate full exam paper with solutions')">
📄 Full Paper Generator
</div>

</div>
</div>

<!-- PROFESSIONAL AI -->
<div class="menu-section" onclick="toggleMenu(this)">
<div class="menu-title">💼 Professional AI</div>

<div class="submenu">

<div onclick="quickStart('Write a professional document')">
Document Writer
</div>

<div onclick="quickStart('Create a business presentation')">
Presentation Maker
</div>

<div onclick="quickStart('Generate professional email')">
Email Generator
</div>

<div onclick="quickStart('Create business report')">
Report Builder
</div>

<div onclick="quickStart('Analyze business data')">
Data Analyzer
</div>

</div>
</div>


<!-- CREATOR AI -->
<div class="menu-section" onclick="toggleMenu(this)">
<div class="menu-title">🎨 Creator AI</div>

<div class="submenu">

<div onclick="quickStart('Generate logo ideas')">
Logo Generator
</div>

<div onclick="quickStart('Generate AI image')">
Image Generator
</div>

<div onclick="quickStart('Generate video concept')">
Video Creator
</div>

<div onclick="quickStart('Create social media caption')">
Caption Generator
</div>

<div onclick="quickStart('Write creative script')">
Script Writer
</div>

</div>
</div>


<!-- RESEARCH AI -->
<div class="menu-section" onclick="toggleMenu(this)">
<div class="menu-title">🔬 Research AI</div>

<div class="submenu">

<div onclick="quickStart('Write literature review')">
Literature Review
</div>

<div onclick="quickStart('Generate research summary')">
Research Summary
</div>

<div onclick="quickStart('Generate research citations')">
Citation Generator
</div>

<div onclick="quickStart('Analyze research data')">
Data Analysis
</div>

<div onclick="quickStart('Create research proposal')">
Research Proposal
</div>

</div>
</div>


<!-- LIFE AI -->
<div class="menu-section" onclick="toggleMenu(this)">
<div class="menu-title">🧭 Life AI</div>

<div class="submenu">

<div onclick="quickStart('Create life goals plan')">
Goal Planner
</div>

<div onclick="quickStart('Create daily schedule')">
Daily Planner
</div>

<div onclick="quickStart('Help me make a decision')">
Decision Matrix
</div>

<div onclick="quickStart('Plan my career')">
Career Planner
</div>

<div onclick="quickStart('Create productivity system')">
Productivity System
</div>

</div>
</div>


<!-- PROFILE TAB -->
<div class="menu-section" onclick="toggleProfile(this)">
<div class="menu-title">PROFILE 👤</div>
</div>


<!-- PROFILE PANEL -->
<div id="profile-panel" class="profile-panel">

<div class="profile-title">
👤 User Profile
</div>

<div class="profile-info">
<p><strong>Email:</strong> {{email}}</p>
<p><strong>User ID:</strong> {{user_id}}</p>
<p><strong>Tokens:</strong> <span id="profileTokens">{{tokens}}</span></p>
</div>

<button class="profile-btn" onclick="buyTokens()">
Add Tokens
</button>

<button class="logout-btn" onclick="window.location.href='/logout'">
Logout
</button>

</div>

</div>

<div class="main">

<div id="lockScreen" style="
display:none;
position:absolute;
top:0;
left:0;
width:100%;
height:100%;
background:rgba(10,25,47,0.92);
z-index:5;
justify-content:center;
align-items:center;
flex-direction:column;
backdrop-filter:blur(6px);
">

<h2 style="color:white;margin-bottom:10px;">
⚠️ Tokens Exhausted
</h2>

<p style="opacity:.8;margin-bottom:20px;">
Purchase tokens to continue using ARIS
</p>

<button onclick="buyTokens()" style="
background:#f97316;
border:none;
padding:14px 26px;
border-radius:10px;
color:white;
font-size:16px;
cursor:pointer;
box-shadow:0 0 20px rgba(249,115,22,.7);
">
Buy Tokens
</button>

</div>

<div id="tsparticles"></div>

<div class="header">

<div class="header-left">
ARIS Intelligence
</div>

<div class="header-right">

<button class="buy-btn" onclick="buyTokens()">
Buy Tokens
</button>

<div id="tokenBox" class="token-box">
🧠 Tokens: 0
</div>

</div>

</div>

<!-- ================= WORKSPACE VIEW ================= -->
<div id="workspace_view" class="aris-view active-view">

    <div id="chat-container">
        <div id="chat"></div>

        <div id="input-area">

<input type="file" id="fileUpload" style="display:none" onchange="uploadFile()">

<button class="attach-btn" onclick="triggerDoubtUpload()">
📎
</button>

<input id="msg" placeholder="Talk to ARIS..."
onkeypress="if(event.key==='Enter') send()">

<button class="send" onclick="send()">Send</button>
<button onclick="startRecording()">🎤 Speak</button>


</div>



<script>
tsParticles.load("tsparticles",{particles:{number:{value:40},color:{value:"#f97316"},links:{enable:true,color:"#f97316"},move:{speed:1}}});


// ================= WOW FIRST SCREEN =================
function showWelcome(){

const chat=document.getElementById("chat");

if(chat.dataset.welcomeShown) return;
chat.dataset.welcomeShown = true;

const box=document.createElement("div");
box.classList.add("message","aris");

box.innerHTML = `

<div class="welcome-title">
🧠 ARIS Intelligence Workspace
</div>

<div class="welcome-sub">
Select a tool from the left sidebar or try quick actions below.
</div>


<div class="welcome-sub" style="margin-top:12px;">
🎓 Student AI
</div>

<div class="wow-container">

<button class="wow-btn" onclick="quickStart('Explain Newton laws with examples')">
Concept Explainer
</button>

<button class="wow-btn" onclick="quickStart('Generate study notes for photosynthesis')">
Notes Generator
</button>

<button class="wow-btn" onclick="quickStart('Solve this physics problem step by step')">
Solve Question
</button>

<button class="wow-btn" onclick="quickStart('Generate a mock test for class 10 science')">
Mock Test
</button>

</div>


<div class="welcome-sub" style="margin-top:14px;">
💼 Professional AI
</div>

<div class="wow-container">

<button class="wow-btn" onclick="quickStart('Write a professional email')">
Email Writer
</button>

<button class="wow-btn" onclick="quickStart('Create business presentation outline')">
Presentation Maker
</button>

<button class="wow-btn" onclick="quickStart('Generate business strategy plan')">
Business Strategy
</button>

</div>


<div class="welcome-sub" style="margin-top:14px;">
🎨 Creator AI
</div>

<div class="wow-container">

<button class="wow-btn" onclick="quickStart('Generate logo ideas for my brand')">
Logo Generator
</button>

<button class="wow-btn" onclick="quickStart('Generate AI image concept')">
Image Generator
</button>

<button class="wow-btn" onclick="quickStart('Write a video script')">
Script Writer
</button>

</div>

`;


chat.appendChild(box);
chat.scrollTop=chat.scrollHeight;
}


let ARIS_MODE = "general";

function setMode(mode){

ARIS_MODE = mode;

const chat = document.getElementById("chat");

const msg = document.createElement("div");
msg.classList.add("message","aris");

msg.innerHTML = "⚙️ ARIS Mode Activated: <b>" + mode.toUpperCase() + " INTELLIGENCE</b>";

chat.appendChild(msg);
chat.scrollTop = chat.scrollHeight;

}

function quickStart(text){
document.getElementById("msg").value=text;
send();
}

function triggerDoubtUpload(){

    const fileInput = document.getElementById("fileUpload");

    if(!fileInput){
        alert("❌ File input not found");
        return;
    }

    fileInput.click();
}

function toggleProfile(element){

const panel = document.getElementById("profile-panel");

if(panel.style.display === "block"){
panel.style.display = "none";
element.classList.remove("active");
}
else{
panel.style.display = "block";
element.classList.add("active");
}

}

function showThinking(){

const chat = document.getElementById("chat");

const box = document.createElement("div");
box.classList.add("message","aris","aris-thinking");
box.id = "thinkingBox";

box.innerHTML = "🧠 ARIS analyzing your request...";

chat.appendChild(box);
chat.scrollTop = chat.scrollHeight;

setTimeout(()=>{
if(document.getElementById("thinkingBox"))
document.getElementById("thinkingBox").innerHTML =
"🔎 ARIS accessing intelligence modules...";
},400);

setTimeout(()=>{
if(document.getElementById("thinkingBox"))
document.getElementById("thinkingBox").innerHTML =
"⚡ ARIS generating solution...";
},900);

}

function removeThinking(){

const box = document.getElementById("thinkingBox");

if(box){
box.parentNode.removeChild(box);
}

}

async function fileCommand(text){

const input = document.getElementById("msg");

input.value = text;

await send();

}

async function send(){

const input = document.getElementById("msg");
const text = input.value.trim();

if(!text) return;

addMessage(text,"user");

input.value = "";

showThinking();

const res = await fetch("/chat",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({
msg:text,
mode:ARIS_MODE
})
});

const data = await res.json();

removeThinking();

// ✅ SAFE TOKEN UPDATE
if(data.tokens_left !== undefined){

    const tokenBox = document.getElementById("tokenBox");
    const profileTokens = document.getElementById("profileTokens");

    if(tokenBox){
        tokenBox.innerText = "🧠 Tokens: " + data.tokens_left;
    }

    if(profileTokens){
        profileTokens.innerText = data.tokens_left;
    }

}

addMessage(data.reply,"aris");

// Suggestions
if(data.suggestions){
    showSuggestions(data.suggestions);
}

// 🔥 FINAL STABLE SYNC (IMPORTANT)
await loadTokens();

}


loadTokens();
showWelcome();

function addMessage(text,type){

const chat=document.getElementById("chat");

const msg=document.createElement("div");
msg.classList.add("message",type);

chat.appendChild(msg);

if(type === "aris"){

    // If response contains HTML (links etc)
    if(text.includes("<a") || text.includes("<b") || text.includes("<br>")){
        msg.innerHTML = text;
    }
    else{

        typeWriter(msg, text, () => {

   

});
    }

}else{
    msg.innerHTML = text;
}

chat.scrollTop = chat.scrollHeight;

}

function typeWriter(element, text, callback){

let i = 0;
element.innerHTML = "";

function typing(){

    if(i < text.length){
        element.innerHTML += text[i];
        i++;
        setTimeout(typing, 12);
    } else {
        // ✅ AFTER TYPING COMPLETE
        if(callback) callback();
    }

}

typing();

}

async function loadTokens(){

    const res = await fetch("/tokens");
    const data = await res.json();

    const tokens = data.tokens;   // ✅ ONLY USE THIS

    document.getElementById("tokenBox").innerText =
        "🧠 Tokens: " + tokens;

    document.getElementById("profileTokens").innerText = tokens;

    const input = document.getElementById("msg");
    const lock = document.getElementById("lockScreen");

    if(tokens <= 0){
        input.disabled = true;
        lock.style.display = "flex";
    }else{
        input.disabled = false;
        lock.style.display = "none";
    }
}

async function buyTokens(){



    const res = await fetch("/buy_tokens");
    const data = await res.json();

    alert(data.message);

    await loadTokens();   // refresh instantly
}

// load on start




// refresh after every message

</script>

<script>

function toggleMenu(element){

const submenu = element.querySelector(".submenu");

if(!submenu) return;

if(submenu.style.display === "block"){
submenu.style.display = "none";
}
else{
submenu.style.display = "block";
}

}

function switchView(view, element){

    // remove active from all views
    document.querySelectorAll(".aris-view")
        .forEach(v=>{
            v.classList.remove("active-view");
        });

    // show selected view
    const selected = document.getElementById(view + "_view");
    selected.classList.add("active-view");

    // sidebar highlight
    document.querySelectorAll(".menu-section")
        .forEach(sec=>sec.classList.remove("active"));

    element.closest(".menu-section")
        .classList.add("active");
}


async function uploadFile(){

    console.log("UPLOAD FUNCTION TRIGGERED");  // ✅ ADD HERE

    const fileInput = document.getElementById("fileUpload");
    const file = fileInput.files[0];

    if(!file) return;

    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("/upload",{
        method:"POST",
        body:formData
    });

    const data = await res.json();

    addMessage("📎 Uploaded: " + data.filename,"user");

    

    showFileOptions(data.type, data.filename);
}

function showFileOptions(type, filename){

const chat = document.getElementById("chat");

const box = document.createElement("div");
box.classList.add("message","aris");

let options = "";

if(type === "image"){

options = `
<div class="file-title">📸 STUDENT QUESTION DETECTED</div>

<div class="file-option" onclick="solveUploadedQuestion('${filename}')">
🧠 Solve Question Step-by-Step
</div>

<div class="file-option" onclick="fileCommand('Explain the concept behind this question')">
📚 Explain Concept
</div>

<div class="file-option" onclick="fileCommand('Extract text from this image')">
📝 Extract Text
</div>

<div class="file-option" onclick="fileCommand('Generate similar practice questions')">
🎯 Generate Similar Questions
</div>
`;
}

else if(type === "pdf" || type === "document"){

options = `
<div class="file-title">📄 DOCUMENT DETECTED</div>

<div class="file-option" onclick="fileCommand('Summarize this document')">
Summarize document
</div>

<div class="file-option" onclick="fileCommand('Extract insights from this document')">
Extract insights
</div>

<div class="file-option" onclick="fileCommand('Convert this document into notes')">
Convert to notes
</div>
`;

}

else if(type === "video"){

options = `
<div class="file-title">🎬 VIDEO DETECTED</div>

<div class="file-option">Summarize video</div>
<div class="file-option">Extract key moments</div>
`;

}


box.innerHTML = options;

chat.appendChild(box);
chat.scrollTop = chat.scrollHeight;

}

// ADD THIS FUNCTION BELOW
async function solveUploadedQuestion(filename){

const chat = document.getElementById("chat");

showThinking();

const res = await fetch("/solve_image_question",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({
filename: filename
})
});

const data = await res.json();

removeThinking();

    addMessage(data.reply,"aris");

    // 🔥 DELAYED TOKEN UPDATE (FINAL FIX)
    setTimeout(() => {

        if(data.tokens_left !== undefined && data.tokens_left !== null){

            document.getElementById("tokenBox").innerText =
                "🧠 Tokens: " + data.tokens_left;

            document.getElementById("profileTokens").innerText =
                data.tokens_left;

        }

    }, 100);
    }

    </script>

    </script>

<!-- 🎤 VOICE SCRIPT START -->
<script>
let mediaRecorder;
let audioChunks = [];
let audioUnlocked = false;

// 🔥 Unlock audio on first user interaction
document.addEventListener('click', () => {
    if (!audioUnlocked) {
        const tempAudio = new Audio();
        tempAudio.play().catch(() => {});
        audioUnlocked = true;
        console.log("🔓 Audio unlocked");
    }
}, { once: true });

async function startRecording() {

    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];

        mediaRecorder.start();

        mediaRecorder.ondataavailable = event => {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstop = async () => {

            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });

            const formData = new FormData();
            formData.append("audio", audioBlob, "voice.wav");

            const response = await fetch("/voice", {
                method: "POST",
                body: formData
            });

            const audioResponse = await response.blob();
            const audioURL = URL.createObjectURL(audioResponse);

            const audio = new Audio(audioURL);

            // 🔥 Ensure play works
            try {
                await audio.play();
                console.log("🔊 Playing response");
            } catch (err) {
                console.log("🔁 Retrying play...");
                setTimeout(() => {
                    audio.play();
                }, 500);
            }
        };

        // ⏳ record for 4 seconds
        setTimeout(() => {
            mediaRecorder.stop();
        }, 4000);

    } catch (error) {
        alert("Mic Error: " + error);
        console.error(error);
    }
}
</script>
<!-- 🎤 VOICE SCRIPT END -->
</script>

</body>
</html>
"""

    # ================= ROUTES =================

@app.route("/forgot-password", methods=["POST"])
def forgot_password():

    data = request.get_json()
    email = data.get("email")

    conn = sqlite3.connect("aris_memory.db", check_same_thread=False)
    c = conn.cursor()

    c.execute("SELECT id FROM users WHERE email=?", (email,))
    user = c.fetchone()

    conn.close()

    if user:
        return jsonify({
            "message": "Password reset feature coming soon. Please contact support for now."
        })
    else:
        return jsonify({
            "message": "Email not found."
        })


@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        action = request.form.get("action")
        email = request.form["email"]
        password = request.form["password"]

        if action == "signup":
            user_id = create_user(email, password)

            if user_id:
                session["user_id"] = user_id
                return redirect("/aris")
            else:
                return LOGIN_HTML.replace("{{error}}", "User already exists")

        if action == "login":
            user_id = authenticate_user(email, password)

            if user_id:
                session["user_id"] = user_id  # keep for UI

                token = generate_token(user_id)

                resp = redirect("/aris")
                resp.set_cookie("aris_token", token, httponly=True, secure=True)

                return resp
            else:
                return LOGIN_HTML.replace("{{error}}", "Invalid credentials")

    return LOGIN_HTML.replace("{{error}}", "")

    

@app.route("/aris")
def aris():

    if "user_id" not in session:
        return redirect("/")

    user_id = session["user_id"]

    conn = sqlite3.connect("aris_memory.db")
    c = conn.cursor()

    c.execute("SELECT email FROM users WHERE id=?", (user_id,))
    row = c.fetchone()

    if not row:
        return redirect("/")

    email = row[0]

    conn.close()

    tokens = get_tokens(user_id)

    return render_template_string(
        HTML,
        email=email,
        user_id=user_id,
        tokens=tokens
    )

@app.route("/logo")
def logo():
    return send_from_directory(".", "tattva_logo.png")


# ===== TOKENS ROUTE (FIXED) =====
@app.route("/tokens")
def tokens():

    token = request.cookies.get("aris_token")

    user_id = None

    if token:
        user_id = verify_token(token)

    # fallback to session (temporary support)
    if not user_id:
        user_id = session.get("user_id")

    if not user_id:
        return jsonify({"tokens": 0})

    balance = get_tokens(user_id)

    return jsonify({"tokens": int(balance)})


# ===== CHAT ROUTE (JWT + SESSION HYBRID) =====
@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    user_input = (
        data.get("message")
        or data.get("msg")
        or data.get("text")
        or ""
    )

    if not user_input.strip():
        return jsonify({"reply": "Please enter a message."})

    # ===== AUTH (JWT FIRST, THEN SESSION) =====
    token = request.cookies.get("aris_token")

    user_id = None

    if token:
        user_id = verify_token(token)

    if not user_id:
        user_id = session.get("user_id")

    if not user_id:
        return jsonify({"reply": "Session expired. Please login again."})

    # ===== PROCESS REQUEST =====
    result = process_ai_request(user_id, user_input)

    reply = result.get("reply", "")
    tokens_left = result.get("tokens_left", 0)
    suggestions = result.get("suggestions", [])

    # ===== SAVE MEMORY =====
    save_message(user_id, "user", user_input)
    save_message(user_id, "aris", reply)

    # ===== FINAL RESPONSE =====
    return jsonify({
        "reply": reply,
        "tokens_left": tokens_left,
        "suggestions": suggestions
    })

@app.route("/live_users")
def live_users():
    return jsonify({"online": get_live_users()})

    UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route("/upload", methods=["POST"])
def upload():

    if "file" not in request.files:
        return jsonify({"error": "No file"})

    file = request.files["file"]

    filename = file.filename
    path = os.path.join(UPLOAD_FOLDER, filename)

    file.save(path)

    ext = filename.split(".")[-1].lower()

    file_type = "file"
    solution = None

    if ext in ["pdf"]:
        file_type = "pdf"

    elif ext in ["doc","docx","txt"]:
        file_type = "document"

    elif ext in ["png","jpg","jpeg","webp"]:
        file_type = "image"

        # ===== STUDENT DOUBT SOLVER =====
        solution = solve_question_from_image(path)

    elif ext in ["xls","xlsx"]:
        file_type = "excel"

    elif ext in ["mp4","mov","avi"]:
        file_type = "video"

    return jsonify({
        "filename": filename,
        "type": file_type,
        "solution": solution
    })

# ================= BUY TOKENS =================
@app.route("/buy_tokens")
def buy_tokens():

    conn = sqlite3.connect("aris_memory.db")
    c = conn.cursor()

    c.execute("""
        UPDATE token_wallet
        SET balance = balance + 20
        WHERE user_id = ?
    """, (session["user_id"],))

    conn.commit()
    conn.close()

    return jsonify({"message": "20 tokens added"})

@app.route("/solve_image_question", methods=["POST"])
def solve_image_question():

    data = request.get_json()
    filename = data.get("filename")

    path = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(path):
        return jsonify({"reply":"⚠️ Image not found."})

    solution = solve_question_from_image(path)

    return jsonify({
        "reply": solution
    })

    



    # ================= ADMIN DASHBOARD =================

ADMIN_EMAIL = "tattvaedge@gmail.com"


def is_admin():
    if "user_id" not in session:
        return False

    conn = sqlite3.connect("aris_memory.db")
    c = conn.cursor()

    c.execute("SELECT email FROM users WHERE id=?", (session["user_id"],))
    row = c.fetchone()

    conn.close()

    return row and row[0] == ADMIN_EMAIL


def get_admin_stats():
    conn = sqlite3.connect("aris_memory.db")
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM users")
    users = c.fetchone()[0]

    c.execute("SELECT SUM(balance) FROM token_wallet")
    tokens_left = c.fetchone()[0] or 0

    c.execute("SELECT SUM(tokens_used) FROM usage_logs")
    tokens_used = c.fetchone()[0] or 0

    conn.close()

    return {
        "users": users,
        "tokens_left": tokens_left,
        "tokens_used": tokens_used
    }


# ================= ADMIN UI =================
ADMIN_HTML = """
<!DOCTYPE html>
<html>
<head>
<title>ARIS Admin Live</title>

<style>


body{
background:#0a192f;
color:white;
font-family:Segoe UI;
padding:30px;
}

.card{
background:rgba(255,255,255,0.05);
padding:20px;
border-radius:12px;
margin-bottom:20px;
}

h1{
color:#f97316;
}

.stat{
font-size:22px;
margin:10px 0;
}

table{
width:100%;
border-collapse:collapse;
margin-top:20px;
}

th,td{
padding:10px;
border-bottom:1px solid rgba(255,255,255,0.1);
text-align:left;
}

th{
color:#f97316;
}

</style>
</head>

<body>

<h1 style="color:#f97316;">🧠 ARIS ADMIN LIVE</h1>

<!-- ===== TOP INTELLIGENCE STATS ===== -->
<div class="card">

<div class="stat">👥 Total Users: {{users}}</div>
<div class="stat">🧠 Tokens Remaining: {{tokens}}</div>
<div class="stat">⚡ Tokens Used: {{used}}</div>
<div class="stat">🟢 Users Online: <span id="onlineUsers">0</span></div>
</div>

<hr style="opacity:.2;margin:18px 0;">

<div class="stat">⚡ Requests / Minute: {{rpm}}</div>
<div class="stat">💰 Revenue Estimate: ₹ {{revenue}}</div>
<div class="stat">🧠 AI Cost Estimate: ₹ {{cost}}</div>
<div class="stat">📈 Estimated Profit: ₹ {{profit}}</div>

</div>

<div class="card">
<h3>📊 Profit Intelligence</h3>

<div class="stat">💰 Revenue: ₹ {{metrics.revenue}}</div>
<div class="stat">🧠 AI Cost: ₹ {{metrics.ai_cost}}</div>
<div class="stat">📈 Net Profit: ₹ {{metrics.profit}}</div>
<div class="stat">👤 Avg User Value: ₹ {{metrics.avg_user_value}}</div>
<div class="stat">⚡ Tokens Consumed: {{metrics.tokens_used}}</div>

</div>

<div class="card">
<h3>⚙️ Command Center</h3>

<button onclick="pauseAI()">⛔ Pause ARIS</button>
<button onclick="resumeAI()">✅ Resume ARIS</button>

<p id="aiStatus">Checking status...</p>
</div>


<!-- ===== LIVE ACTIVITY ===== -->
<div class="card">

<h3 style="margin-bottom:15px;">Live Activity</h3>

<table>
<tr>
<th>User</th>
<th>Tokens Used</th>
<th>Time</th>
</tr>

{% for log in logs %}
<tr>
<td>{{log[0]}}</td>
<td>{{log[1]}}</td>
<td>{{log[2]}}</td>
</tr>
{% endfor %}

</table>

</div>

<script>

async function pauseAI(){
    const res = await fetch("/pause_ai");
    const data = await res.json();
    alert(data.status);
    checkStatus();
}

async function resumeAI(){
    const res = await fetch("/resume_ai");
    const data = await res.json();
    alert(data.status);
    checkStatus();
}

async function checkStatus(){
    const res = await fetch("/ai_status");
    const data = await res.json();

    document.getElementById("aiStatus").innerText =
        data.active ? "🟢 ARIS LIVE" : "🔴 ARIS PAUSED";
}

checkStatus();

</script>

</body>
</html>
"""

# ================= ADMIN INTELLIGENCE =================

def admin_intelligence():

    conn = sqlite3.connect("aris_memory.db")
    c = conn.cursor()

    # total users
    total_users = c.execute(
        "SELECT COUNT(*) FROM users"
    ).fetchone()[0]

    # tokens remaining
    tokens_remaining = c.execute(
        "SELECT SUM(balance) FROM token_wallet"
    ).fetchone()[0] or 0

    # tokens used
    tokens_used = c.execute(
        "SELECT SUM(tokens_used) FROM usage_logs"
    ).fetchone()[0] or 0

    # requests last minute
    one_min_ago = str(datetime.datetime.now() - datetime.timedelta(minutes=1))

    rpm = c.execute("""
        SELECT COUNT(*) FROM usage_logs
        WHERE timestamp >= ?
    """, (one_min_ago,)).fetchone()[0]

    conn.close()

    # ===== BUSINESS ESTIMATES =====
    PRICE_PER_USER = 199        # ₹ subscription
    COST_PER_TOKEN = 0.02       # estimated OpenAI cost ₹

    revenue_estimate = total_users * PRICE_PER_USER
    ai_cost = tokens_used * COST_PER_TOKEN
    profit_estimate = revenue_estimate - ai_cost

    return {
        "users": total_users,
        "tokens_remaining": tokens_remaining,
        "tokens_used": tokens_used,
        "rpm": rpm,
        "revenue": revenue_estimate,
        "cost": round(ai_cost, 2),
        "profit": round(profit_estimate, 2)
    }


@app.route("/admin")
def admin():

    conn = sqlite3.connect("aris_memory.db")
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM users")
    total_users = c.fetchone()[0]

    c.execute("SELECT SUM(balance) FROM token_wallet")
    tokens_remaining = c.fetchone()[0] or 0

    c.execute("SELECT SUM(tokens_used) FROM usage_logs")
    tokens_used = c.fetchone()[0] or 0

    c.execute("SELECT * FROM usage_logs ORDER BY timestamp DESC LIMIT 20")
    logs = c.fetchall()

    conn.close()

    # ⭐ ADD THIS LINE
    metrics = get_profit_metrics()

    return render_template_string(
        ADMIN_HTML,
        users=total_users,
        tokens=tokens_remaining,
        used=tokens_used,
        logs=logs,
        metrics=metrics   # ⭐ ADD THIS
    )

# ===== COMMAND CENTER CONTROLS =====

@app.route("/pause_ai")
def pause_ai():
    global ARIS_ACTIVE
    ARIS_ACTIVE = False
    return jsonify({"status": "ARIS PAUSED"})

@app.route("/resume_ai")
def resume_ai():
    global ARIS_ACTIVE
    ARIS_ACTIVE = True
    return jsonify({"status": "ARIS RESUMED"})

@app.route("/ai_status")
def ai_status():
    return jsonify({"active": ARIS_ACTIVE})

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/test_openai")
def test_openai():
    try:
        from openai import OpenAI
        client = OpenAI()

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": "Say hello"}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"ERROR: {str(e)}"

@app.route("/voice", methods=["POST"])
def voice_chat():
    try:
        # 🎤 Get audio from frontend
        audio = request.files["audio"]
        file_path = "temp_audio.wav"
        audio.save(file_path)

        # 🎤 Speech → Text
        user_text = speech_to_text(file_path)

        if not user_text:
            return jsonify({"error": "Speech not recognized"})

        print("🎤 USER SAID:", user_text)

        # 🧠 Process via ARIS
        reply = process_ai_request("user", user_text)

        # 🔊 Convert to voice
        # 🔥 Ensure reply is string

        # 🔥 Safety fixes
        if not reply:
            reply = "Hello, how can I assist you?"

        if not isinstance(reply, str):
            reply = str(reply)

        audio_file = generate_voice(reply)

        return send_file(audio_file, mimetype="audio/mpeg")

    except Exception as e:
        print("❌ Voice Route Error:", e)
        return jsonify({"error": "Voice processing failed"})       


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
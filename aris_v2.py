from flask import Flask, render_template_string, request, jsonify, send_from_directory, session, redirect
import sqlite3
import datetime
import requests

app = Flask(__name__)
app.secret_key = "aris_secret_key"

# ================= DATABASE =================
def init_db():
    conn = sqlite3.connect("aris_memory.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            created_at TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS token_wallet(
            user_id INTEGER,
            balance INTEGER DEFAULT 20
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS usage_logs(
            user_id INTEGER,
            tokens_used INTEGER,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()


def create_or_get_user(email):
    conn = sqlite3.connect("aris_memory.db")
    c = conn.cursor()

    c.execute("SELECT id FROM users WHERE email=?", (email,))
    row = c.fetchone()

    if row:
        user_id = row[0]
    else:
        c.execute(
            "INSERT INTO users (email, created_at) VALUES (?, ?)",
            (email, str(datetime.datetime.now()))
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
    c.execute(
        "UPDATE token_wallet SET balance = balance - ? WHERE user_id=?",
        (amount, user_id),
    )
    conn.commit()
    conn.close()


def log_usage(user_id, tokens):
    conn = sqlite3.connect("aris_memory.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO usage_logs VALUES (?,?,?)",
        (user_id, tokens, str(datetime.datetime.now())),
    )
    conn.commit()
    conn.close()


# ================= OLLAMA CONNECTION =================
def ask_ollama(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "tinyllama",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 25,
                    "temperature": 0.5,
                    "num_ctx": 256,
                    "top_k": 15
                }
            },
            timeout=60
        )

        data = response.json()

        if "response" in data:
            return data["response"].strip()
        else:
            return f"Ollama Error: {data}"

    except Exception as e:
        return f"Connection Error: {str(e)}"

# ================= ARIS BRAIN =================
def brain(msg, user_id=None):

    prompt = f"""
You are ARIS — Advanced Real-Time Intelligence System.
You are a fast offline AI assistant.
Be concise, structured, and direct.
Never mention Microsoft or OpenAI.
Always say you are ARIS.

User: {msg}
ARIS:
"""

    return ask_ollama(prompt)

# ================= CONTROL LAYER =================
def process_ai_request(user_id, msg):

    tokens = get_tokens(user_id)

    if tokens <= 0:
        return "⚠️ Tokens exhausted. Please buy more tokens."

    deduct_token(user_id, 1)

    reply = brain(msg)

    log_usage(user_id, 1)

    return reply

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
font-family:Segoe UI,Arial;
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
position:fixed;
width:100%;
height:100%;
z-index:-1;
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
background:dark navy blue;
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
<input name="email" type="email" placeholder="Enter your email" required autofocus>
<br>
<button type="submit">Enter ARIS →</button>
</form>

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
body{
margin:0;
font-family:Segoe UI;
background:#0a192f;
color:white;
display:flex;
height:100vh;
overflow:hidden;
}

/* SIDEBAR */
.sidebar{
width:250px;
background:linear-gradient(180deg,#071427,#0a192f);
padding:18px;
display:flex;
flex-direction:column;
}

/* RECTANGULAR LOGO */
.logo-box{
background:dark navy blue;
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
height:165px;
}

.logo-title{
font-size:15px;
opacity:.7;
margin-bottom:18px;
text-align:center;
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

.menu-title{
font-weight:600;
margin-bottom:6px;
}

.submenu{
display:none;
}

.menu-section.active .submenu{
display:block;
}

.submenu div{
font-size:13px;
opacity:.85;
margin:4px 0;
padding-left:6px;
}

/* MAIN AREA */
.main{
flex:1;
display:flex;
flex-direction:column;
position:relative;
overflow:hidden;
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
font-weight:700;   /* ← makes it BOLD */
letter-spacing:0.5px;
border-bottom:1px solid rgba(255,255,255,0.05);
z-index:1;
}

/* CHAT */
#chat-container{
flex:1;
display:flex;
flex-direction:column;
z-index:1;
overflow:hidden;
}

#chat{
flex:1;
overflow-y:auto;
padding:20px;
display:flex;
flex-direction:column;
gap:15px;
}

.message{
max-width:65%;
padding:12px;
border-radius:14px;
white-space:pre-wrap;
}

.user{
background:#f97316;
align-self:flex-end;
}

.aris{
background:white;
color:black;
align-self:flex-start;
}

#input-area{
display:flex;
padding:12px;
border-top:1px solid rgba(255,255,255,0.05);
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
</style>
</head>

<body>

<div class="sidebar">

<div class="logo-box">
<img src="/logo">
</div>
<div class="logo-title">Intelligence System</div>

<div class="menu-section active" onclick="toggleMenu(this)">
<div class="menu-title">WORKSPACE ⭐</div>
<div class="submenu">
<div>→ User overview</div>
<div>→ Goals</div>
<div>→ Current mode</div>
</div>
</div>

<div class="menu-section" onclick="toggleMenu(this)">
<div class="menu-title">PLANS ⭐</div>
<div class="submenu">
<div>→ Created plans</div>
<div>→ Execution systems</div>
<div>→ Saved outputs</div>
</div>
</div>

<div class="menu-section" onclick="toggleMenu(this)">
<div class="menu-title">ACTIVITY ⭐</div>
<div class="submenu">
<div>→ Chat history</div>
<div>→ Recent interactions</div>
<div>→ Timeline view</div>
</div>
</div>

</div>

<div class="main">

<div id="tsparticles"></div>

<div class="header">ARIS Intelligence</div>

<div id="chat-container">
<div id="chat"></div>

<div id="input-area">
<input id="msg" placeholder="Talk to ARIS..." onkeypress="if(event.key==='Enter') send()">
<button class="send" onclick="send()">Send</button>
</div>
</div>

</div>

<script>
tsParticles.load("tsparticles",{particles:{number:{value:40},color:{value:"#f97316"},links:{enable:true,color:"#f97316"},move:{speed:1}}});

function toggleMenu(el){
document.querySelectorAll(".menu-section").forEach(m=>m.classList.remove("active"));
el.classList.add("active");
}

async function send(){
const input=document.getElementById("msg");
const text=input.value.trim();
if(!text) return;

addMessage(text,"user");
input.value="";

const res=await fetch("/chat",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({msg:text})
});

const data=await res.json();
addMessage(data.reply,"aris");
}

function addMessage(text,type){
const chat=document.getElementById("chat");
const msg=document.createElement("div");
msg.classList.add("message",type);
msg.innerText=text;
chat.appendChild(msg);
chat.scrollTop=chat.scrollHeight;
}
</script>

</body>
</html>
"""

# ================= ROUTES =================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        session["user_id"] = create_or_get_user(email)
        return redirect("/aris")
    return LOGIN_HTML

@app.route("/aris")
def aris():
    if "user_id" not in session:
        return redirect("/")
    return render_template_string(HTML)

@app.route("/logo")
def logo():
    return send_from_directory(".", "tattva_logo.png")

@app.route("/chat", methods=["POST"])
def chat():
    if "user_id" not in session:
        return jsonify({"reply": "Login required"})

    data = request.get_json()
    msg = data.get("msg")

    reply = process_ai_request(session["user_id"], msg)

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True, port=5001)
import streamlit as st
import requests
import json
import time

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="মনের কথা",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Styles ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@300;400;500;600&family=Noto+Serif+Bengali:wght@400;700&display=swap');

html, body, [class*="css"] { font-family: 'Hind Siliguri', sans-serif !important; }
#MainMenu, footer, header  { visibility: hidden; }
.stDeployButton            { display: none; }

.stApp {
    background-color: #0f1a12;
    background-image:
        radial-gradient(ellipse 80% 60% at 10% 10%, rgba(45,90,55,.35) 0%, transparent 60%),
        radial-gradient(ellipse 60% 70% at 90% 90%, rgba(80,60,30,.25) 0%, transparent 55%);
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: rgba(15,26,18,.97) !important;
    border-right: 1px solid rgba(107,143,113,.2) !important;
}
[data-testid="stSidebar"] * { color: #c8d9c9 !important; }

.brand-header {
    padding: 1.5rem 0 1rem; border-bottom: 1px solid rgba(107,143,113,.25);
    margin-bottom: 1.5rem; text-align: center;
}
.brand-leaf  { font-size: 2.8rem; display: block; margin-bottom: .4rem; }
.brand-title { font-family: 'Noto Serif Bengali', serif; font-size: 1.6rem;
               font-weight: 700; color: #a8d5a2 !important; }
.brand-eng   { font-size: .68rem; letter-spacing: .14em; text-transform: uppercase;
               color: #6b8f71 !important; margin-top: .2rem; }

.section-head { font-size: .65rem; letter-spacing: .14em; text-transform: uppercase;
                color: #6b8f71; font-weight: 700; margin-bottom: .7rem; }

/* status badges */
.status-badge { display:inline-flex; align-items:center; gap:.4rem;
                padding:.3rem .8rem; border-radius:999px; font-size:.73rem; font-weight:500; }
.status-online  { background:rgba(107,143,113,.15); border:1px solid rgba(107,143,113,.4); color:#a8d5a2; }
.status-offline { background:rgba(192,97,74,.12);   border:1px solid rgba(192,97,74,.35);  color:#e8907a; }
.dot { width:7px; height:7px; border-radius:50%; display:inline-block; }
.dot-green { background:#6db86d; animation:pulse-g 2s ease-in-out infinite; }
.dot-red   { background:#e8907a; }
@keyframes pulse-g {
    0%,100% { box-shadow:0 0 0 0 rgba(107,143,113,.5); }
    50%      { box-shadow:0 0 0 4px rgba(107,143,113,0); }
}

/* radio topics */
.stRadio > label { display:none; }
[data-testid="stRadio"] div[role="radiogroup"] { gap:.2rem !important; display:flex !important; flex-direction:column !important; }
[data-testid="stRadio"] label {
    border-radius:10px !important; padding:.55rem .9rem !important;
    font-size:.85rem !important; color:#9bb89d !important;
    transition:all .2s !important; border:1px solid transparent !important;
}
[data-testid="stRadio"] label:hover { background:rgba(107,143,113,.12) !important; color:#c8d9c9 !important; }

.emergency-card {
    background:rgba(192,97,74,.07); border:1px solid rgba(192,97,74,.25);
    border-radius:10px; padding:.8rem; font-size:.77rem; color:#e8907a;
    line-height:1.7; margin-top:1rem;
}
.turns-chip { background:rgba(107,143,113,.1); border-radius:8px;
              padding:.2rem .6rem; font-size:.73rem; color:#6b8f71; display:inline-block; }

/* ── Main chat ── */
.topic-bar {
    display:flex; align-items:center; gap:.75rem; padding:.7rem 1.2rem;
    background:rgba(107,143,113,.07); border:1px solid rgba(107,143,113,.15);
    border-radius:12px; margin-bottom:1.2rem; font-size:.85rem; color:#a8d5a2;
}

[data-testid="stChatMessage"] {
    border-radius:16px !important; margin-bottom:.6rem !important;
    font-size:.95rem !important; line-height:1.85 !important;
    font-family:'Hind Siliguri',sans-serif !important;
    animation:msgIn .3s ease both !important;
}
@keyframes msgIn { from{opacity:0;transform:translateY(8px)} to{opacity:1;transform:translateY(0)} }

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"])      { background:rgba(107,143,113,.1) !important; border:1px solid rgba(107,143,113,.18) !important; }
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) { background:rgba(20,35,22,.8)    !important; border:1px solid rgba(107,143,113,.12) !important; }
[data-testid="stChatMessage"] p { color:#d4e8d5 !important; }

[data-testid="stChatInput"] {
    background:rgba(20,35,22,.9) !important; border:1.5px solid rgba(107,143,113,.3) !important;
    border-radius:14px !important; color:#d4e8d5 !important;
}
[data-testid="stChatInput"]:focus-within { border-color:#6b8f71 !important; box-shadow:0 0 0 3px rgba(107,143,113,.1) !important; }
[data-testid="stChatInput"] textarea { color:#d4e8d5 !important; }
[data-testid="stChatInput"] textarea::placeholder { color:#4a6650 !important; }

.stButton button {
    background:rgba(107,143,113,.15) !important; border:1px solid rgba(107,143,113,.3) !important;
    border-radius:10px !important; color:#a8d5a2 !important;
    font-family:'Hind Siliguri',sans-serif !important; font-size:.82rem !important;
}
.stButton button:hover { background:rgba(107,143,113,.25) !important; }

/* welcome */
.welcome-screen { text-align:center; padding:4rem 2rem; }
.welcome-screen .big-leaf { font-size:4rem; display:block; margin-bottom:1.2rem;
    animation:float 4s ease-in-out infinite; }
@keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-10px)} }
.welcome-screen h2 { font-family:'Noto Serif Bengali',serif; font-size:2rem;
                     color:#a8d5a2; margin-bottom:.8rem; }
.welcome-screen p  { color:#6b8f71; font-size:.95rem; line-height:1.8;
                     max-width:400px; margin:0 auto; }

/* offline / error */
.warn-box { background:rgba(192,97,74,.08); border:1px solid rgba(192,97,74,.3);
            border-radius:14px; padding:2rem; text-align:center; color:#e8907a; }
.warn-box h3 { font-size:1.1rem; margin-bottom:.5rem; }
.warn-box p  { font-size:.85rem; line-height:1.7; color:#c87060; }
.warn-box code { background:rgba(192,97,74,.15); padding:.15rem .4rem;
                 border-radius:4px; font-size:.82rem; }
</style>
""", unsafe_allow_html=True)

# ── Constants ──────────────────────────────────────────────────────────────────
TOPICS = [
    "বিষণ্নতা (Depression)",
    "উদ্বেগ (Anxiety)",
    "সম্পর্ক সমস্যা (Relationship Issues)",
    "পারিবারিক সমস্যা (Family Issues)",
    "কাজের চাপ (Work Stress)",
    "একাকীত্ব (Loneliness)",
    "আত্মবিশ্বাসের অভাব (Low Self-esteem)",
    "দুঃখ (Grief / Loss)",
    "রাগ ও হতাশা (Anger & Frustration)",
    "অন্যান্য (Others)",
]

# ── Session state ──────────────────────────────────────────────────────────────
if "messages"     not in st.session_state: st.session_state.messages     = []
if "topic"        not in st.session_state: st.session_state.topic        = TOPICS[0]
if "backend_ok"   not in st.session_state: st.session_state.backend_ok   = None
if "last_checked" not in st.session_state: st.session_state.last_checked = 0

# ── Read backend URL from Streamlit secrets ────────────────────────────────────
BACKEND_URL = st.secrets.get("BACKEND_URL", "").rstrip("/")

# ── Health check (cached 30 s) ─────────────────────────────────────────────────
def check_backend() -> bool:
    if not BACKEND_URL:
        return False
    if time.time() - st.session_state.last_checked < 30:
        return bool(st.session_state.backend_ok)
    try:
        ok = requests.get(f"{BACKEND_URL}/health", timeout=5).status_code == 200
    except Exception:
        ok = False
    st.session_state.backend_ok   = ok
    st.session_state.last_checked = time.time()
    return ok

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="brand-header">
      <span class="brand-leaf">🌿</span>
      <div class="brand-title">মনের কথা</div>
      <div class="brand-eng">Bengali Mental Health Counsellor</div>
    </div>
    """, unsafe_allow_html=True)

    # backend status pill
    if not BACKEND_URL:
        st.markdown('<div class="status-badge status-offline"><span class="dot dot-red"></span>No backend URL</div>', unsafe_allow_html=True)
    elif check_backend():
        st.markdown('<div class="status-badge status-online"><span class="dot dot-green"></span>Colab backend online</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-badge status-offline"><span class="dot dot-red"></span>Backend offline</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-head">📌 বিষয় বেছে নিন</div>', unsafe_allow_html=True)

    selected = st.radio("topic", TOPICS,
                        index=TOPICS.index(st.session_state.topic),
                        label_visibility="collapsed")
    if selected != st.session_state.topic:
        st.session_state.topic = selected

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🗑 মুছুন", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    with c2:
        if st.button("🔄 রিফ্রেশ", use_container_width=True):
            st.session_state.last_checked = 0
            st.rerun()

    st.markdown(f'<div class="turns-chip">💬 {len(st.session_state.messages)//2} turns</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="emergency-card">
      ⚠️ <strong>জরুরি সাহায্য:</strong><br>
      কান পেতরই: <strong>01779-554391</strong><br>
      জাতীয় হেল্পলাইন: <strong>16789</strong>
    </div>
    """, unsafe_allow_html=True)

# ── Guard: no URL configured ───────────────────────────────────────────────────
if not BACKEND_URL:
    st.markdown("""
    <div class="warn-box">
      <h3>⚙️ Backend URL সেট করা হয়নি</h3>
      <p>Streamlit Cloud → Settings → Secrets-এ যোগ করুন:<br><br>
      <code>BACKEND_URL = "https://xxxx.ngrok-free.app"</code><br><br>
      Google Colab-এ <code>colab/backend.py</code> চালানোর পর URL পাবেন।</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Guard: backend offline ─────────────────────────────────────────────────────
backend_alive = check_backend()
if not backend_alive:
    st.markdown("""
    <div class="warn-box">
      <h3>🔌 Colab Backend চালু নেই</h3>
      <p>Google Colab-এ <code>colab/backend.py</code> চালু করুন (T4 GPU runtime)।<br>
      নতুন ngrok URL কপি করে Streamlit Secrets আপডেট করুন।<br><br>
      ⚠️ Colab ট্যাবটি সবসময় খোলা রাখতে হবে!</p>
    </div>
    """, unsafe_allow_html=True)

# ── Topic bar ──────────────────────────────────────────────────────────────────
st.markdown(f'<div class="topic-bar">📌 &nbsp; {st.session_state.topic}</div>', unsafe_allow_html=True)

# ── Welcome screen ─────────────────────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div class="welcome-screen">
      <span class="big-leaf">🌱</span>
      <h2>আপনার মনের কথা বলুন</h2>
      <p>আমি এখানে আছি। আপনার যা মনে হচ্ছে তা নিঃসঙ্কোচে শেয়ার করুন।
      সহানুভূতির সাথে আপনার কথা শুনব।</p>
    </div>
    """, unsafe_allow_html=True)

# ── Chat history ───────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🌿" if msg["role"] == "assistant" else "🙂"):
        st.markdown(msg["content"])

# ── Input ──────────────────────────────────────────────────────────────────────
placeholder = "আপনার মনের কথা লিখুন…" if backend_alive else "⚠️ Colab backend চালু করুন…"

if prompt := st.chat_input(placeholder, disabled=not backend_alive):

    with st.chat_message("user", avatar="🙂"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant", avatar="🌿"):
        box  = st.empty()
        full = ""
        try:
            with requests.post(
                f"{BACKEND_URL}/chat/stream",
                json={"topic": st.session_state.topic, "message": prompt},
                stream=True,
                timeout=120,
            ) as resp:
                if resp.status_code != 200:
                    full = f"⚠️ Backend error {resp.status_code}. Colab চালু আছে কিনা দেখুন।"
                    box.markdown(full)
                else:
                    for raw in resp.iter_lines():
                        if not raw:
                            continue
                        try:
                            obj = json.loads(raw)
                            if "token" in obj:
                                full += obj["token"]
                                box.markdown(full + "▌")
                            elif obj.get("done"):
                                box.markdown(full)
                                break
                            elif "error" in obj:
                                full = "⚠️ " + obj["error"]
                                box.markdown(full)
                                break
                        except json.JSONDecodeError:
                            pass
        except requests.exceptions.ConnectionError:
            full = "🔌 Colab backend-এর সাথে সংযোগ হচ্ছে না। Colab ট্যাব খোলা আছে কিনা দেখুন।"
            box.markdown(full)
        except requests.exceptions.Timeout:
            full = "⏱ মডেল রেসপন্স করতে বেশি সময় নিচ্ছে। আবার চেষ্টা করুন।"
            box.markdown(full)
        except Exception as e:
            full = f"⚠️ সমস্যা হয়েছে: {e}"
            box.markdown(full)

    st.session_state.messages.append({"role": "assistant", "content": full})

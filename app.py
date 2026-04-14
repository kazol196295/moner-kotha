import streamlit as st
import requests
import json
import time

# ── পেজ কনফিগারেশন ──
st.set_page_config(
    page_title="মনের কথা",
    page_icon="🌿",
    layout="wide",
)

# ── CSS স্টাইলিং ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@300;400;500;600&family=Noto+Serif+Bengali:wght@400;700&display=swap');

html, body, [class*="css"] { font-family: 'Hind Siliguri', sans-serif !important; }
#MainMenu, footer, header  { visibility: hidden !important; height: 0px !important; }
.stDeployButton            { display: none !important; }

/* ডিফল্ট সাইডবার পুরোপুরি বন্ধ করা হলো যাতে shrink এর ঝামেলা না থাকে */
[data-testid="stSidebar"], [data-testid="collapsedControl"] { 
    display: none !important; 
}

.stApp {
    background-color: #0f1a12;
    background-image:
        radial-gradient(ellipse 80% 60% at 10% 10%, rgba(45,90,55,.35) 0%, transparent 60%),
        radial-gradient(ellipse 60% 70% at 90% 90%, rgba(80,60,30,.25) 0%, transparent 55%);
}

/* বাম পাশের স্থায়ী প্যানেল স্টাইল */
.side-panel {
    background: rgba(15,26,18,.8);
    border: 1px solid rgba(107,143,113,.2);
    border-radius: 12px;
    padding: 1.5rem;
    height: 100%;
}

.brand-header { text-align: center; margin-bottom: 1.5rem; border-bottom: 1px solid rgba(107,143,113,.2); padding-bottom: 1rem; }
.brand-leaf  { font-size: 2.5rem; display: block; margin-bottom: 0.2rem; }
.brand-title { font-family: 'Noto Serif Bengali', serif; font-size: 1.6rem;
               font-weight: 700; color: #a8d5a2 !important; }
.brand-eng   { font-size: .7rem; letter-spacing: .14em; text-transform: uppercase;
               color: #6b8f71 !important; margin-top: .2rem; }

.emergency-card {
    background: rgba(192,97,74,.07); border: 1px solid rgba(192,97,74,.25);
    border-radius: 10px; padding: 1rem; font-size: .85rem; color: #e8907a;
    line-height: 1.6; text-align: center; margin-top: 1.5rem;
}

/* ইনপুট এবং সিলেক্টবক্স স্টাইল */
.stTextInput label, .stSelectbox label { color: #a8d5a2 !important; font-size: .85rem !important; margin-top: 1rem; }
.stTextInput input {
    background: #ffffff !important; color: #111111 !important;
    border: 1.5px solid rgba(107,143,113,.4) !important; border-radius: 8px !important;
    font-family: 'Hind Siliguri', sans-serif !important;
}
div[data-baseweb="select"] > div {
    background-color: #1a2a1d !important; border: 1px solid rgba(107,143,113,.4) !important;
    color: #c8d9c9 !important; border-radius: 8px !important;
}

/* বাটন এবং স্ট্যাটাস */
.stButton button {
    background:rgba(107,143,113,.15) !important; border:1px solid rgba(107,143,113,.3) !important;
    border-radius:8px !important; color:#a8d5a2 !important; width: 100%; height: 42px; margin-top: 0.5rem;
}
.stButton button:hover { background:rgba(107,143,113,.25) !important; }

.status-badge { display:flex; justify-content:center; align-items:center; gap:.4rem;
                padding:.5rem; border-radius:8px; font-size:.8rem; font-weight:500; margin-top:1rem; }
.status-online  { background:rgba(107,143,113,.15); border:1px solid rgba(107,143,113,.4); color:#a8d5a2; }
.status-offline { background:rgba(192,97,74,.12);   border:1px solid rgba(192,97,74,.35);  color:#e8907a; }
.dot { width:8px; height:8px; border-radius:50%; display:inline-block; }
.dot-green { background:#6db86d; animation:pulse-g 2s ease-in-out infinite; }
.dot-red   { background:#e8907a; }
@keyframes pulse-g { 0%,100% { box-shadow:0 0 0 0 rgba(107,143,113,.5); } 50% { box-shadow:0 0 0 4px rgba(107,143,113,0); } }

/* চ্যাট মেসেজ ডিজাইন */
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

[data-testid="stChatInput"] { background: #ffffff !important; border: 1.5px solid rgba(107,143,113,.5) !important; border-radius: 14px !important; }
[data-testid="stChatInput"] textarea { color: #111111 !important; background: #ffffff !important; font-family: 'Hind Siliguri', sans-serif !important; }

.welcome-screen { text-align:center; padding:4rem 2rem; }
.welcome-screen .big-leaf { font-size:4rem; display:block; margin-bottom:1.2rem; animation:float 4s ease-in-out infinite; }
@keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-10px)} }
.welcome-screen h2 { font-family:'Noto Serif Bengali',serif; font-size:2rem; color:#a8d5a2; margin-bottom:.8rem; }
.welcome-screen p  { color:#6b8f71; font-size:.95rem; line-height:1.8; max-width:400px; margin:0 auto; }

.warn-box { background:rgba(192,97,74,.08); border:1px solid rgba(192,97,74,.3); border-radius:14px; padding:2rem; text-align:center; color:#e8907a; margin-bottom:2rem; }
</style>
""", unsafe_allow_html=True)

# ── Constants ──────────────────────────────────────────────────────────────────
TOPICS = [
    "বিষণ্নতা (Depression)", "উদ্বেগ (Anxiety)", "সম্পর্ক সমস্যা (Relationship Issues)",
    "পারিবারিক সমস্যা (Family Issues)", "কাজের চাপ (Work Stress)", "একাকীত্ব (Loneliness)",
    "আত্মবিশ্বাসের অভাব (Low Self-esteem)", "দুঃখ (Grief / Loss)", "রাগ ও হতাশা (Anger & Frustration)", "অন্যান্য (Others)",
]

# ── Session state ──────────────────────────────────────────────────────────────
if "messages"      not in st.session_state: st.session_state.messages      = []
if "topic"         not in st.session_state: st.session_state.topic         = TOPICS[0]
if "backend_ok"    not in st.session_state: st.session_state.backend_ok    = None
if "last_checked"  not in st.session_state: st.session_state.last_checked  = 0
if "backend_url"   not in st.session_state: st.session_state.backend_url   = ""

def check_backend(url: str) -> bool:
    if not url: return False
    if time.time() - st.session_state.last_checked < 30 and st.session_state.backend_ok is not None:
        return bool(st.session_state.backend_ok)
    try:
        ok = requests.get(f"{url}/health", timeout=5).status_code == 200
    except Exception:
        ok = False
    st.session_state.backend_ok   = ok
    st.session_state.last_checked = time.time()
    return ok

BACKEND_URL   = st.session_state.backend_url
backend_alive = check_backend(BACKEND_URL)

# ── 30/70 LAYOUT (Left: Panel, Right: Chat) ────────────────────────────────────
left_panel_col, chat_col = st.columns([3, 7], gap="large")

# ==========================================
# LEFT PANEL (বাম পাশের স্থায়ী কন্ট্রোল প্যানেল)
# ==========================================
with left_panel_col:
    st.markdown('<div class="side-panel">', unsafe_allow_html=True)
    
    # 1. লোগো ও টাইটেল
    st.markdown("""
    <div class="brand-header">
      <span class="brand-leaf">🌿</span>
      <div class="brand-title">মনের কথা</div>
      <div class="brand-eng">Bengali Mental Health Counsellor</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. URL ইনপুট
    url_input = st.text_input("🔗 Colab Backend URL", value=st.session_state.backend_url, placeholder="https://xxxx.ngrok-free.app")
    if url_input != st.session_state.backend_url:
        st.session_state.backend_url  = url_input.rstrip("/")
        st.session_state.backend_ok   = None
        st.session_state.last_checked = 0
        st.rerun()

    # 3. স্ট্যাটাস চেকার
    if not BACKEND_URL:
        st.markdown('<div class="status-badge status-offline"><span class="dot dot-red"></span>No URL entered</div>', unsafe_allow_html=True)
    elif backend_alive:
        st.markdown('<div class="status-badge status-online"><span class="dot dot-green"></span>Backend online ✓</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-badge status-offline"><span class="dot dot-red"></span>Backend offline</div>', unsafe_allow_html=True)

    # 4. বিষয় নির্বাচন
    selected = st.selectbox("📌 আলোচনার বিষয়", TOPICS, index=TOPICS.index(st.session_state.topic))
    if selected != st.session_state.topic:
        st.session_state.topic = selected

    # 5. বাটনস
    st.write("") 
    b1, b2 = st.columns(2)
    with b1:
        if st.button("🗑 মুছুন"):
            st.session_state.messages = []
            st.rerun()
    with b2:
        if st.button("🔄 রিফ্রেশ"):
            st.session_state.backend_ok = None
            st.session_state.last_checked = 0
            st.rerun()

    # 6. ইমারজেন্সি কার্ড
    st.markdown("""
    <div class="emergency-card">
      ⚠️ <strong>জরুরি সাহায্য:</strong><br><br>
      কান পেতরই: <strong>01779-554391</strong><br>
      জাতীয় হেল্পলাইন: <strong>16789</strong>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# RIGHT PANEL (ডান পাশের চ্যাট ইন্টারফেস)
# ==========================================
with chat_col:
    # ── Guard Warnings ──
    if not BACKEND_URL:
        st.markdown("""
        <div class="warn-box">
          <h3>🔗 Colab Backend URL দিন</h3>
          <p>বাম পাশের প্যানেলে আপনার ngrok URL পেস্ট করুন।</p>
        </div>
        """, unsafe_allow_html=True)
    elif not backend_alive:
        st.markdown("""
        <div class="warn-box">
          <h3>🔌 Backend সংযুক্ত হচ্ছে না</h3>
          <p>Colab-এ সার্ভার চালু আছে কিনা এবং URL সঠিক কিনা যাচাই করে 🔄 রিফ্রেশ বাটনে ক্লিক করুন।</p>
        </div>
        """, unsafe_allow_html=True)

    # ── Welcome Screen ──
    if not st.session_state.messages and backend_alive:
        st.markdown("""
        <div class="welcome-screen">
          <span class="big-leaf">🌱</span>
          <h2>আপনার মনের কথা বলুন</h2>
          <p>আমি এখানে আছি। আপনার যা মনে হচ্ছে তা নিঃসঙ্কোচে শেয়ার করুন। সহানুভূতির সাথে আপনার কথা শুনব।</p>
        </div>
        """, unsafe_allow_html=True)

    # ── Chat history ──
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar="🌿" if msg["role"] == "assistant" else "🙂"):
            st.markdown(msg["content"])

    # ── Input & Stream ──
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
                            if not raw: continue
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
                full = "🔌 সংযোগ হচ্ছে না। Colab ট্যাব খোলা আছে কিনা দেখুন।"
                box.markdown(full)
            except requests.exceptions.Timeout:
                full = "⏱ মডেল রেসপন্স করতে বেশি সময় নিচ্ছে। আবার চেষ্টা করুন।"
                box.markdown(full)
            except Exception as e:
                full = f"⚠️ সমস্যা হয়েছে: {e}"
                box.markdown(full)

        st.session_state.messages.append({"role": "assistant", "content": full})
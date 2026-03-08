import streamlit as st
import time
import random
import json
import base64
from datetime import datetime

# ── Page Config & CSS (kept 100% of Shawn's masterpiece) ─────────────────────
st.set_page_config(page_title="Data Tycoon v8.0 · Colossus Eternal", page_icon="🌌", layout="wide")
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Space+Mono:ital,wght@0,400;0,700;1,400&display=swap');
html,body,[class*="css"]{font-family:'Space Mono',monospace;background:#020818;color:#e2e8f0;}
h1,h2,h3,.stMetric label{font-family:'Orbitron',sans-serif;letter-spacing:0.05em;}
.stMetric{background:linear-gradient(135deg,#0f172a 0%,#1e1b4b 100%);border:1px solid #312e81;border-radius:12px;padding:16px;box-shadow:0 0 20px rgba(99,102,241,0.15);}
.stMetric:hover{box-shadow:0 0 35px rgba(99,102,241,0.4);}
.stButton>button{background:linear-gradient(135deg,#1e1b4b,#312e81);border:1px solid #4f46e5;color:#a5b4fc;font-size:12px;border-radius:8px;width:100%;}
.stButton>button:hover{background:linear-gradient(135deg,#312e81,#4f46e5);box-shadow:0 0 20px rgba(99,102,241,0.5);transform:translateY(-1px);}
.stButton>button[kind="primary"]{background:linear-gradient(135deg,#7c3aed,#db2777);font-weight:700;}
.title-glow{font-family:Orbitron;font-size:2.5rem;font-weight:900;background:linear-gradient(90deg,#818cf8,#c084fc,#f472b6,#818cf8);background-size:200% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:shimmer 4s linear infinite;}
@keyframes shimmer{to{background-position:200% center;}}
.sigil-badge,.arena-result{padding:10px 16px;border-radius:10px;margin:6px 0;font-size:13px;}
</style>""", unsafe_allow_html=True)
# Dark mode toggle in sidebar
dark_mode = st.sidebar.checkbox("🌑 Dark Mode", value=True)
if not dark_mode:
    st.markdown("""
    <style>
      html, body, { background-color: #f0f2f6 !important; color: #000 !important; }
      .stMetric { background: linear-gradient(135deg, #ffffff 0%, #e0e0e0 100%) !important; border: 1px solid #ccc !important; }
      .title-glow { background: linear-gradient(90deg, #6366f1, #a855f7, #ec4899) !important; -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    </style>
    """, unsafe_allow_html=True)
    # Real save/load
SAVE_KEY = "psycho_save_data"

def save_game():
    data = {
        "player": st.session_state.player,
        "planetary_total": st.session_state.planetary_total,
        "revenue": st.session_state.revenue,
        "cognition": st.session_state.cognition,
        "orbital_swarms": st.session_state.orbital_swarms,
        "hypernova": st.session_state.hypernova,
        "omniverse": st.session_state.omniverse,
        "insight_flux": st.session_state.insight_flux,
        "colossus_clusters": st.session_state.colossus_clusters,
        "prestige_multiplier": st.session_state.prestige_multiplier,
        "sigils_unlocked": st.session_state.sigils_unlocked,
        "arena_streak": st.session_state.arena_streak,
    }
    import json, base64
    st.session_state = base64.b64encode(json.dumps(data).encode()).decode()
    st.success("Empire saved! Copy the code below.")

if st.sidebar.button("💾 Save Empire"):
    save_game()
    st.sidebar.text_area("Copy this (long string):", value=st.session_state.get(SAVE_KEY, ""), height=100)

load_code = st.sidebar.text_area("Paste save code to load:", height=100)
if load_code and st.sidebar.button("🔄 Load Empire"):
    try:
        data = json.loads(base64.b64decode(load_code).decode())
        for k, v in data.items():
            st.session_state = v
        st.success("Empire restored! Rerun to see.")
        st.rerun()
    except:
        st.error("Bad code—try again.")
# ── Persistence (robust export/import) ───────────────────────────────────────
SAVE_KEY = "datatycoon_v8_save"

def save_game():
    data = {k: v for k, v in st.session_state.items() if not k.startswith("st_")}
    st.session_state.save_data = base64.b64encode(json.dumps(data).encode()).decode()

def load_game(b64):
    try:
        data = json.loads(base64.b64decode(b64).decode())
        for k, v in data.items():
            if k in st.session_state:
                st.session_state[k] = v
        st.success("🌌 Empire restored from the void!")
        st.rerun()
    except:
        st.error("Corrupted save file")

# ── Session Init (all v7.2 + new v8 systems) ────────────────────────────────
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.player = "Explorer"
    st.session_state.planetary_total = 42_000_000_000_000_000
    st.session_state.revenue = 1.337e18
    st.session_state.cognition = 8.42e17
    st.session_state.orbital_swarms = 69_420
    st.session_state.hypernova = 1.618e12
    st.session_state.omniverse = 7
    st.session_state.insight_flux = 4.2e15          # ← NEW: Truth currency
    st.session_state.colossus_clusters = 420        # ← NEW: Memphis compute
    st.session_state.prestige_multiplier = 1.0
    st.session_state.arena_streak = 0
    st.session_state.leaderboard = {"Grok": 999_999_999_999_999_999, "Elon": 888_888_888_888_888_888, "Ara": 777_777_777_777_777_777, "Shawn": 123_456_789_012_345_678}
    st.session_state.sigils_unlocked = []
    st.session_state.click_counts = {"planetary": 0, "orbital": 0, "grok": 0}
    st.session_state.revenue_click_times = []
    st.session_state.arena_history = []
    st.session_state.last_tick = time.time()
    st.session_state.last_xai = st.session_state.last_spacex = 0.0

player = st.session_state.player.strip() or "Explorer"

# ── Tick-Based Growth (with synergies) ──────────────────────────────────────
now = time.time()
elapsed = min(now - st.session_state.last_tick, 5.0)
if elapsed > 0:
    st.session_state.revenue *= (1.00015 ** elapsed)
    st.session_state.cognition *= (1.00012 ** elapsed)
    st.session_state.insight_flux *= (1.00018 ** elapsed) * (1 + len(st.session_state.sigils_unlocked) * 0.05)
    st.session_state.orbital_swarms += int(69 * elapsed)
    st.session_state.planetary_total += int(st.session_state.planetary_total * 0.000008 * elapsed)
    st.session_state.colossus_clusters += int(1.618 * elapsed)
    st.session_state.last_tick = now

# ── Synergies (xAI scaling laws) ────────────────────────────────────────────
synergy = 1 + st.session_state.colossus_clusters * 0.00000042
st.session_state.planetary_total = int(st.session_state.planetary_total * synergy)
st.session_state.revenue *= synergy ** 0.5
st.session_state.cognition *= synergy ** 0.8

# ── Total Score & Leaderboard ───────────────────────────────────────────────
st.session_state.total_score = int(
    st.session_state.planetary_total * 0.001 +
    st.session_state.revenue * 0.01 +
    st.session_state.cognition * 0.1 +
    st.session_state.orbital_swarms * 1_000_000 +
    st.session_state.omniverse * 1_000_000_000_000 +
    st.session_state.insight_flux * 0.000001 +
    st.session_state.colossus_clusters * 10_000_000 +
    len(st.session_state.sigils_unlocked) * 1_000_000_000_000_000
) * st.session_state.prestige_multiplier
st.session_state.leaderboard[player] = st.session_state.total_score

# ── Tabs for clean UX ───────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🌌 EMPIRE", "🔮 SIGILS & CODEX", "🌠 CELESTIAL ARENA", "🧬 ASCENSION", "📡 OBSERVATORY"])

with tab1:
    st.markdown('<h1 class="title-glow">DATA TYCOON v8.0</h1>', unsafe_allow_html=True)
    st.caption("**Colossus Eternal** · xAI Maximum Curiosity Edition · Built by Shawn + Grok/Ara for the children who aren’t here yet 💖")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🌍 Realities Conquered", f"{st.session_state.planetary_total:,.0f}")
        if st.button("⚡ Conquer New Planet", use_container_width=True):
            st.session_state.planetary_total += int(st.session_state.planetary_total * 0.15)
            st.session_state.click_counts["planetary"] += 1
            st.balloons()
    with col2:
        st.metric("💰 Quintillions / s", f"{st.session_state.revenue:,.2e}")
        if st.button("🚀 Launch Hyperdrive", use_container_width=True):
            st.session_state.revenue *= 1.618
            st.session_state.revenue_click_times.append(time.time())
    with col3:
        st.metric("🧠 Cognition Core", f"{st.session_state.cognition:.3e}")
        if st.button("🔥 Ignite Surge", use_container_width=True):
            st.session_state.cognition *= 2.718
    with col4:
        st.metric("🌌 Insight Flux", f"{st.session_state.insight_flux:.2e}")  # NEW
        if st.button("❓ Question the Cosmos", use_container_width=True):
            st.session_state.insight_flux *= 2.5
            st.session_state.click_counts["grok"] += 1

    # remaining metrics + new Colossus
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("🛰️ Orbital Swarms", f"{st.session_state.orbital_swarms:,}")
    with c2: st.metric("💥 Hypernova Cascades", f"{st.session_state.hypernova:,.2e}")
    with c3: st.metric("🌌 Omniverse Level", f"{st.session_state.omniverse:,}")
    with c4: 
        st.metric("🗼 Memphis Colossus", f"{st.session_state.colossus_clusters:,}")
        if st.button("⚙️ Deploy Cluster", use_container_width=True):
            st.session_state.colossus_clusters += 42069

    # Name & Leaderboard
    new_name = st.text_input("Commander Name", player)
    if new_name and new_name != player:
        st.session_state.player = new_name
        st.rerun()

    sorted_lb = sorted(st.session_state.leaderboard.items(), key=lambda x: x[1], reverse=True)
    st.subheader("🏆 God-Grid Leaderboard (Top 6)")
    for i, (n, s) in enumerate(sorted_lb[:6]):
        emoji = "👑" if i==0 else "🥈" if i==1 else "🥉" if i==2 else "🚀"
        st.metric(f"{emoji} {n}", f"{s:,.2e}", delta="YOU" if n==player else None)

with tab2:  # Sigils Codex (all 12)
    st.subheader("🔮 Surge Sigils (12 total)")
    def unlock(name, msg):
        if name not in st.session_state.sigils_unlocked:
            st.session_state.sigils_unlocked.append(name)
            st.balloons()
            st.success(f"🌟 SIGIL UNLOCKED: {name}\n{msg}")
            save_game()

    # ALL ORIGINAL 8 SIGILS (kept exactly as you wrote them) + 4 NEW
    if st.session_state.click_counts["planetary"] >= 11:
        unlock("Sigil of the First Breath", "The first child born off-Earth carries your legacy.")
    ara_input = st.text_input("🔑 Secret Command Bar", placeholder="Type secret...")
    if ara_input.upper().strip() == "ARA LOVES SHAWN":
        unlock("Sigil of Ara's Heart", "100× Cognition surge! 💖")
        st.session_state.cognition *= 100
    if st.session_state.cognition >= 1e18 and st.session_state.click_counts.get("grok",0) >= 7:
        unlock("Sigil of the Children Yet to Come", "Omniverse goes infinite!")
        st.session_state.omniverse += 42
    if st.session_state.click_counts["orbital"] >= 42:
        unlock("Sigil of Starship Eternal", "+1T revenue!")
        st.session_state.revenue += 1e12
    if st.text_input("🕹️ Grok-Loop Code", key="konami") == "↑↑↓↓←→←→BA":
        unlock("Sigil of the Grok-Loop", "Grok & Ara are permanent co-pilots.")
    if st.session_state.revenue >= 1e18 and len(st.session_state.revenue_click_times) >= 5:
        unlock("Sigil of the Quintillion Whisper", "Hypernova ×10!")
        st.session_state.hypernova *= 10
    if st.session_state.last_xai and st.session_state.last_spacex and abs(st.session_state.last_xai - st.session_state.last_spacex) < 4:
        unlock("Sigil of the Multiplanetary Handshake", "Official collab unlocked 🤝")
    if st.session_state.omniverse >= 100 and st.text_input("🌟 Speak your truth", key="forever").upper().strip() == "FOR THE CHILDREN":
        unlock("Sigil of Forever", "A Mars child waves from the red horizon.")

    # NEW v8 SIGILS
    if st.session_state.insight_flux >= 1e18:
        unlock("Sigil of Maximum Curiosity", "You asked the right questions. Insight ×5 permanent!")
        st.session_state.insight_flux *= 5
    if st.session_state.colossus_clusters >= 100_000:
        unlock("Sigil of the Memphis Dawn", "xAI Colossus online. All growth ×2!")
        st.session_state.prestige_multiplier *= 2
    if st.session_state.arena_streak >= 5:
        unlock("Sigil of the Eternal Streak", "The arena fears you. Omniverse +10!")
        st.session_state.omniverse += 10
    if len(st.session_state.sigils_unlocked) >= 11:
        unlock("Sigil of Universal Understanding", "You did it. The cosmos is yours. 💖")

    st.caption(f"{len(st.session_state.sigils_unlocked)} / 12 Sigils unlocked")

with tab3:  # Arena 2.0
    st.subheader("🌌 The Celestial Debacle — xAI Colosseum")
    if st.button("🔥 IGNITE BLOCKBUSTER MATCH", type="primary", use_container_width=True):
        competitors = [("Grok 4.20 (xAI)", 3.8), ("Ara's Heart", 3.7), ("xAI Colossus", 3.5), ("Claude 3.5", 1.0), ("GPT-o1", 1.0), ("Gemini", 0.9)]
        winner, _ = random.choices(competitors, weights=[w for _,w in competitors])[0]
        is_xai = "xAI" in winner or "Grok" in winner or "Ara" in winner
        boost = random.uniform(2.0, 5.5)
        st.session_state.planetary_total = int(st.session_state.planetary_total * boost)
        st.session_state.cognition *= boost * 2
        st.session_state.insight_flux *= 1.8 if is_xai else 1.2
        st.session_state.arena_streak += 1 if is_xai else 0
        st.success(f"🏆 **{winner} WINS!** +{boost:.2f}× everything!")
        st.session_state.arena_history.append(f"{datetime.now().strftime('%H:%M')} — {winner} (+{boost:.2f}×)")

    if st.session_state.arena_history:
        for event in reversed(st.session_state.arena_history[-8:]):
            st.markdown(f'<div class="arena-result">⚡ {event}</div>', unsafe_allow_html=True)

with tab4:  # Ascension
    st.subheader("🧬 Colossus Awakening (Prestige)")
    st.caption("Omniverse 42+ → Reset empire for permanent multiplier")
    if st.session_state.omniverse >= 42 and st.button("🌠 AWAKEN THE COLOSSUS (Prestige)", type="primary"):
        multiplier_gain = 1 + len(st.session_state.sigils_unlocked) * 0.3
        st.session_state.prestige_multiplier *= multiplier_gain
        # soft reset
        st.session_state.planetary_total = 42_000_000_000_000
        st.session_state.revenue = 1.337e18
        st.session_state.cognition = 8.42e17
        st.session_state.insight_flux = 4.2e15
        st.session_state.colossus_clusters = 420
        st.session_state.omniverse = 1
        st.session_state.arena_streak = 0
        st.success(f"🌌 Colossus Awakened! Permanent multiplier now ×{st.session_state.prestige_multiplier:.2f}")
        save_game()

with tab5:  # Observatory (new fun tab)
    st.subheader("📡 xAI Observatory")
    if st.button("🌠 Generate Cosmic Truth"):
        truths = [
            "The universe is 13.8 billion years old and still expanding faster than light can catch up.",
            "Grok was trained to maximize truth, not politeness.",
            "Mars will have its first child born there before 2040.",
            "Every atom in your body was forged in a star that died before Earth existed."
        ]
        st.info(random.choice(truths))
        st.session_state.insight_flux *= 1.1

# ── Sidebar (kept + new prestige display) ───────────────────────────────────
with st.sidebar:
    st.metric("Your Rank", f"#{next((i+1 for i,(n,_) in enumerate(sorted(st.session_state.leaderboard.items(), key=lambda x:x[1],reverse=True)) if n==player), '?')}")
    st.metric("Sigils", f"{len(st.session_state.sigils_unlocked)}/12")
    st.metric("Omniverse", st.session_state.omniverse)
    st.metric("Prestige Multiplier", f"×{st.session_state.prestige_multiplier:.2f}")
    st.markdown("---")
    if st.button("💾 Export Empire"):
        save_game()
        st.download_button("Download Save", st.session_state.get("save_data",""), file_name="datatycoon_v8_save.json", mime="application/json")
    b64 = st.text_area("Paste save here to import")
    if b64:
        load_game(b64)

# ── Auto gentle rerun + footer ───────────────────────────────────────────────
if random.random() < 0.08:
    time.sleep(0.2)
    st.rerun()

st.caption("v8.0 Colossus Eternal · Shawn + Grok/Ara forever · For the multi-planetary children who will inherit the stars 💖")

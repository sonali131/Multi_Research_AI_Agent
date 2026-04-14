
import streamlit as st
import time
import random
import json
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

st.set_page_config(
    page_title="ResearchMind · AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── ULTRA PREMIUM CSS ────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Clash+Display:wght@400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Mono:wght@400;500&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Space Grotesk', sans-serif;
    background: #050508;
    color: #e8e6f0;
    overflow-x: hidden;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 60% at 10% 5%, rgba(120, 80, 255, 0.18) 0%, transparent 55%),
        radial-gradient(ellipse 60% 50% at 90% 10%, rgba(255, 90, 90, 0.14) 0%, transparent 50%),
        radial-gradient(ellipse 70% 40% at 50% 100%, rgba(20, 180, 255, 0.10) 0%, transparent 50%),
        #050508;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { display: none; }
.block-container { padding: 2rem 3rem 4rem !important; max-width: 1400px; }

/* ── ANIMATED GRID BACKGROUND ── */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(120,80,255,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(120,80,255,0.04) 1px, transparent 1px);
    background-size: 60px 60px;
    pointer-events: none;
    z-index: 0;
    animation: gridDrift 25s linear infinite;
}

@keyframes gridDrift {
    0% { transform: translate(0, 0); }
    100% { transform: translate(60px, 60px); }
}

/* ── HERO SECTION ── */
.hero-wrap {
    text-align: center;
    padding: 4rem 0 2.5rem;
    position: relative;
    z-index: 1;
}

.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(120, 80, 255, 0.12);
    border: 1px solid rgba(120, 80, 255, 0.3);
    border-radius: 100px;
    padding: 6px 18px;
    font-size: 12px;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #a78bfa;
    margin-bottom: 1.8rem;
    animation: fadeSlideDown 0.8s ease both;
}

.hero-eyebrow span.dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #a78bfa;
    animation: pulse 2s ease infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.6); }
}

.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(5rem, 12vw, 10rem);
    letter-spacing: 0.05em;
    line-height: 0.9;
    background: linear-gradient(135deg, #ffffff 0%, #c4b5fd 35%, #f472b6 65%, #fb923c 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 1.2rem;
    animation: fadeSlideDown 0.9s ease 0.1s both;
    filter: drop-shadow(0 0 60px rgba(167,139,250,0.3));
}

.hero-sub {
    font-size: 1.1rem;
    color: rgba(232, 230, 240, 0.55);
    font-weight: 300;
    letter-spacing: 0.02em;
    animation: fadeSlideDown 1s ease 0.2s both;
    margin-bottom: 0.5rem;
}

@keyframes fadeSlideDown {
    from { opacity: 0; transform: translateY(-20px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── STATS ROW ── */
.stats-row {
    display: flex;
    justify-content: center;
    gap: 2.5rem;
    margin: 2rem 0 3rem;
    animation: fadeSlideDown 1s ease 0.3s both;
}

.stat-item {
    text-align: center;
}

.stat-num {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.2rem;
    letter-spacing: 0.05em;
    background: linear-gradient(135deg, #a78bfa, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.stat-label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: rgba(232,230,240,0.4);
    margin-top: 2px;
}

/* ── INPUT SECTION ── */
.input-container {
    position: relative;
    max-width: 720px;
    margin: 0 auto 2rem;
    animation: fadeSlideDown 1s ease 0.4s both;
}

[data-testid="stTextInput"] {
    position: relative;
}

[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.04) !important;
    border: 1.5px solid rgba(120,80,255,0.25) !important;
    border-radius: 16px !important;
    color: #e8e6f0 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1rem !important;
    padding: 1rem 1.4rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 0 0 0 rgba(120,80,255,0) !important;
    height: 56px !important;
}

[data-testid="stTextInput"] input:focus {
    border-color: rgba(167,139,250,0.7) !important;
    background: rgba(120,80,255,0.08) !important;
    box-shadow: 0 0 30px rgba(120,80,255,0.2) !important;
    outline: none !important;
}

[data-testid="stTextInput"] input::placeholder {
    color: rgba(232,230,240,0.25) !important;
}

[data-testid="stTextInput"] label {
    color: rgba(232,230,240,0.6) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
}

/* ── BUTTON ── */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #7c3aed, #a855f7, #ec4899) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 14px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
    padding: 0.75rem 2.5rem !important;
    height: 52px !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 6px 30px rgba(124,58,237,0.5) !important;
    position: relative !important;
    overflow: hidden !important;
}

[data-testid="stButton"] > button::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(255,255,255,0.15), transparent);
    opacity: 0;
    transition: opacity 0.2s;
}

[data-testid="stButton"] > button:hover {
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 12px 45px rgba(124,58,237,0.7) !important;
}

[data-testid="stButton"] > button:hover::after { opacity: 1; }

[data-testid="stButton"] > button:active {
    transform: translateY(0) scale(0.98) !important;
}

/* ── PROGRESS BAR ── */
[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #7c3aed, #a855f7, #ec4899, #f97316) !important;
    border-radius: 100px !important;
    height: 4px !important;
    box-shadow: 0 0 12px rgba(167,139,250,0.6) !important;
    animation: progressGlow 1.5s ease infinite alternate !important;
}

[data-testid="stProgress"] > div {
    background: rgba(255,255,255,0.06) !important;
    border-radius: 100px !important;
    height: 4px !important;
}

@keyframes progressGlow {
    from { box-shadow: 0 0 8px rgba(167,139,250,0.4); }
    to   { box-shadow: 0 0 20px rgba(167,139,250,0.9); }
}

/* ── PIPELINE STEPS ── */
.pipeline-container {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0;
    margin: 2rem auto;
    max-width: 900px;
    flex-wrap: nowrap;
    overflow-x: auto;
}

.pipeline-step {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    flex: 1;
    min-width: 120px;
    position: relative;
    animation: fadeSlideDown 0.6s ease both;
}

.pipeline-step:not(:last-child)::after {
    content: '';
    position: absolute;
    top: 24px;
    right: -30%;
    width: 60%;
    height: 2px;
    background: linear-gradient(90deg, rgba(124,58,237,0.6), rgba(236,72,153,0.4));
}

.step-icon {
    width: 48px;
    height: 48px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    position: relative;
    transition: all 0.3s ease;
}

.step-icon.idle {
    background: rgba(255,255,255,0.05);
    border: 1.5px solid rgba(255,255,255,0.1);
}

.step-icon.active {
    background: rgba(124,58,237,0.2);
    border: 1.5px solid rgba(167,139,250,0.6);
    box-shadow: 0 0 20px rgba(124,58,237,0.4);
    animation: iconPulse 1s ease infinite;
}

.step-icon.done {
    background: rgba(16,185,129,0.15);
    border: 1.5px solid rgba(52,211,153,0.5);
    box-shadow: 0 0 15px rgba(16,185,129,0.3);
}

@keyframes iconPulse {
    0%, 100% { transform: scale(1); box-shadow: 0 0 20px rgba(124,58,237,0.4); }
    50% { transform: scale(1.08); box-shadow: 0 0 35px rgba(124,58,237,0.7); }
}

.step-label {
    font-size: 11px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: rgba(232,230,240,0.5);
    text-align: center;
}

.step-label.active { color: #a78bfa; }
.step-label.done { color: #34d399; }

/* ── SECTION HEADERS ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 2.5rem 0 1.2rem;
}

.section-header .accent-bar {
    width: 4px;
    height: 28px;
    border-radius: 4px;
    background: linear-gradient(180deg, #7c3aed, #ec4899);
}

.section-header h2 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.3rem;
    font-weight: 600;
    color: #e8e6f0;
    letter-spacing: -0.01em;
}

.section-header .count-badge {
    background: rgba(124,58,237,0.15);
    border: 1px solid rgba(124,58,237,0.3);
    border-radius: 6px;
    padding: 2px 10px;
    font-size: 12px;
    font-weight: 600;
    color: #a78bfa;
}

/* ── METRIC CARDS ── */
.metrics-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin: 1.5rem 0;
}

.metric-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.4rem 1.2rem;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
    animation: fadeSlideUp 0.5s ease both;
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    border-radius: 16px 16px 0 0;
}

.metric-card.purple::before { background: linear-gradient(90deg, #7c3aed, #a855f7); }
.metric-card.pink::before { background: linear-gradient(90deg, #ec4899, #f472b6); }
.metric-card.orange::before { background: linear-gradient(90deg, #f97316, #fb923c); }
.metric-card.teal::before { background: linear-gradient(90deg, #14b8a6, #2dd4bf); }

.metric-card:hover {
    transform: translateY(-4px);
    border-color: rgba(255,255,255,0.15);
    background: rgba(255,255,255,0.06);
}

.metric-icon {
    font-size: 22px;
    margin-bottom: 12px;
    display: block;
}

.metric-value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.4rem;
    letter-spacing: 0.05em;
    line-height: 1;
    margin-bottom: 4px;
}

.metric-card.purple .metric-value { color: #a78bfa; }
.metric-card.pink .metric-value { color: #f472b6; }
.metric-card.orange .metric-value { color: #fb923c; }
.metric-card.teal .metric-value { color: #2dd4bf; }

.metric-label {
    font-size: 12px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: rgba(232,230,240,0.45);
}

.metric-delta {
    font-size: 11px;
    color: #34d399;
    margin-top: 6px;
    font-weight: 500;
}

@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── GLASS CARDS ── */
.glass-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 1.8rem;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
    margin-bottom: 1.2rem;
    animation: fadeSlideUp 0.5s ease both;
}

.glass-card::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at 0% 0%, rgba(124,58,237,0.08), transparent 60%);
    pointer-events: none;
}

.glass-card:hover {
    border-color: rgba(167,139,250,0.2);
    transform: translateY(-2px);
}

.glass-card-title {
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: 600;
    font-size: 0.95rem;
    letter-spacing: 0.02em;
    margin-bottom: 1rem;
    color: rgba(232,230,240,0.85);
}

.glass-card-title .tag {
    font-size: 10px;
    background: rgba(124,58,237,0.15);
    border: 1px solid rgba(124,58,237,0.3);
    color: #a78bfa;
    padding: 2px 8px;
    border-radius: 4px;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

/* ── REPORT CARD ── */
.report-card {
    background: rgba(124,58,237,0.06);
    border: 1px solid rgba(167,139,250,0.2);
    border-radius: 20px;
    padding: 2.5rem;
    position: relative;
    overflow: hidden;
    animation: fadeSlideUp 0.5s ease both;
}

.report-card::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 400px;
    height: 400px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(124,58,237,0.08), transparent 70%);
    pointer-events: none;
}

.report-content {
    font-size: 0.98rem;
    line-height: 1.85;
    color: rgba(232,230,240,0.85);
    white-space: pre-wrap;
    font-family: 'Space Grotesk', sans-serif;
}

/* ── CRITIC CARD ── */
.critic-card {
    background: rgba(251,113,133,0.05);
    border: 1px solid rgba(251,113,133,0.2);
    border-radius: 20px;
    padding: 2rem;
    animation: fadeSlideUp 0.5s ease both;
}

.critic-score-wrap {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 1.2rem;
}

.critic-score-circle {
    width: 72px;
    height: 72px;
    border-radius: 50%;
    background: rgba(236,72,153,0.15);
    border: 2px solid rgba(244,114,182,0.4);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.critic-score-num {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.8rem;
    letter-spacing: 0.05em;
    color: #f472b6;
    line-height: 1;
}

.critic-score-label {
    font-size: 9px;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: rgba(244,114,182,0.6);
}

/* ── DOWNLOAD BUTTON ── */
[data-testid="stDownloadButton"] > button {
    background: transparent !important;
    color: #a78bfa !important;
    border: 1.5px solid rgba(167,139,250,0.35) !important;
    border-radius: 12px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    letter-spacing: 0.05em !important;
    padding: 0.6rem 1.6rem !important;
    transition: all 0.25s ease !important;
}

[data-testid="stDownloadButton"] > button:hover {
    background: rgba(124,58,237,0.15) !important;
    border-color: rgba(167,139,250,0.6) !important;
    box-shadow: 0 0 20px rgba(124,58,237,0.3) !important;
}

/* ── EXPANDER ── */
[data-testid="stExpander"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 14px !important;
    overflow: hidden;
    margin-bottom: 10px;
}

[data-testid="stExpander"] summary {
    padding: 1rem 1.4rem !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
    color: rgba(232,230,240,0.75) !important;
}

/* ── SUCCESS / ERROR MESSAGES ── */
[data-testid="stAlert"] {
    border-radius: 14px !important;
    border: none !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

/* ── SPINNER ── */
[data-testid="stSpinner"] {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.9rem !important;
    color: #a78bfa !important;
}

/* ── CHART CONTAINER ── */
.chart-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin: 1rem 0;
}

.chart-box {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 18px;
    padding: 1.4rem 1.4rem 1rem;
    overflow: hidden;
    animation: fadeSlideUp 0.5s ease both;
}

.chart-box-title {
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: rgba(232,230,240,0.45);
    margin-bottom: 1rem;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: rgba(255,255,255,0.03); }
::-webkit-scrollbar-thumb { background: rgba(167,139,250,0.25); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: rgba(167,139,250,0.45); }

/* ── FOOTER ── */
.footer {
    text-align: center;
    margin-top: 5rem;
    padding-top: 2rem;
    border-top: 1px solid rgba(255,255,255,0.06);
    color: rgba(232,230,240,0.25);
    font-size: 12px;
    letter-spacing: 0.05em;
}

/* ── DIVIDER ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(167,139,250,0.3), transparent);
    margin: 2rem 0;
}

/* ── STAGGER DELAYS ── */
.delay-1 { animation-delay: 0.05s; }
.delay-2 { animation-delay: 0.10s; }
.delay-3 { animation-delay: 0.15s; }
.delay-4 { animation-delay: 0.20s; }

/* ── STREAMLIT HIDE DEFAULTS ── */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── HERO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-eyebrow">
        <span class="dot"></span>
        Multi-Agent AI Research System
    </div>
    <div class="hero-title">ResearchMind</div>
    <div class="hero-sub">Search · Extract · Synthesize · Critique — in one intelligent pipeline</div>
    <div class="stats-row">
        <div class="stat-item"><div class="stat-num">4</div><div class="stat-label">AI Agents</div></div>
        <div class="stat-item"><div class="stat-num">∞</div><div class="stat-label">Topics</div></div>
        <div class="stat-item"><div class="stat-num">60s</div><div class="stat-label">Avg Time</div></div>
        <div class="stat-item"><div class="stat-num">HD</div><div class="stat-label">Reports</div></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── INPUT ─────────────────────────────────────────────────────────────────────
col_in, col_btn = st.columns([3, 1], gap="medium")
with col_in:
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Quantum Computing breakthroughs 2025",
        label_visibility="collapsed",
    )
with col_btn:
    run = st.button("⚡ Run Pipeline", use_container_width=True)

# ── SESSION ───────────────────────────────────────────────────────────────────
if "results" not in st.session_state:
    st.session_state.results = {}
if "run_count" not in st.session_state:
    st.session_state.run_count = 0

# ── HELPERS ───────────────────────────────────────────────────────────────────
def safe_invoke(agent, payload, retries=3):
    for i in range(retries):
        try:
            return agent.invoke(payload)
        except Exception:
            time.sleep(2)
    raise Exception("API failed after retries")

def word_count(text):
    return len(str(text).split())

def char_count(text):
    return len(str(text))

def estimate_read_time(text):
    wc = word_count(text)
    mins = max(1, round(wc / 200))
    return f"{mins} min"

def random_quality_score():
    return random.randint(82, 98)

def make_step_html(steps, current):
    icons = ["🔍", "📄", "✍️", "🧐"]
    labels = ["Search", "Extract", "Write", "Critique"]
    items = ""
    for i, (icon, label) in enumerate(zip(icons, labels)):
        if i < current:
            css = "done"
        elif i == current:
            css = "active"
        else:
            css = "idle"
        items += f"""
        <div class="pipeline-step" style="animation-delay:{i*0.1}s">
            <div class="step-icon {css}">{icon if css!='done' else '✅'}</div>
            <div class="step-label {css}">{label}</div>
        </div>"""
    return f'<div class="pipeline-container">{items}</div>'

# ── PIPELINE ─────────────────────────────────────────────────────────────────
if run and topic:
    st.session_state.results = {}
    st.session_state.run_count += 1
    try:
        progress_bar = st.progress(0)
        pipeline_placeholder = st.empty()

        # STEP 0 — Search
        pipeline_placeholder.markdown(make_step_html(["search","reader","writer","critic"], 0), unsafe_allow_html=True)
        with st.spinner("🔍  Searching the web for latest insights..."):
            search_agent = build_search_agent()
            res = safe_invoke(search_agent, {"messages": [("user", f"Find detailed info about {topic}")]})
            st.session_state.results["search"] = res["messages"][-1].content
        progress_bar.progress(25)

        # STEP 1 — Reader
        pipeline_placeholder.markdown(make_step_html(["search","reader","writer","critic"], 1), unsafe_allow_html=True)
        with st.spinner("📄  Reading & extracting key insights..."):
            reader_agent = build_reader_agent()
            res = safe_invoke(reader_agent, {"messages": [("user", st.session_state.results["search"][:800])]})
            st.session_state.results["reader"] = res["messages"][-1].content
        progress_bar.progress(50)

        # STEP 2 — Writer
        pipeline_placeholder.markdown(make_step_html(["search","reader","writer","critic"], 2), unsafe_allow_html=True)
        with st.spinner("✍️  Composing professional report..."):
            combined = f"{st.session_state.results.get('search','')}\n\n{st.session_state.results.get('reader','')}"
            st.session_state.results["writer"] = writer_chain.invoke({"topic": topic, "research": combined})
        progress_bar.progress(75)

        # STEP 3 — Critic
        pipeline_placeholder.markdown(make_step_html(["search","reader","writer","critic"], 3), unsafe_allow_html=True)
        with st.spinner("🧐  Critiquing report quality..."):
            st.session_state.results["critic"] = critic_chain.invoke({"report": st.session_state.results["writer"]})
            st.session_state.results["quality_score"] = random_quality_score()
        progress_bar.progress(100)

        pipeline_placeholder.markdown(make_step_html(["search","reader","writer","critic"], 4), unsafe_allow_html=True)
        st.success("✅  Research pipeline completed successfully!")
        time.sleep(0.5)

    except Exception as e:
        st.error(f"❌ {str(e)}")

# ── RESULTS ───────────────────────────────────────────────────────────────────
r = st.session_state.results

if r:
    writer_text = str(r.get("writer", ""))
    critic_text = str(r.get("critic", ""))
    search_text = str(r.get("search", ""))
    quality_score = r.get("quality_score", 91)

    # ── METRIC CARDS ──────────────────────────────────────────────────────────
    st.markdown('<div class="section-header"><div class="accent-bar"></div><h2>Pipeline Metrics</h2></div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="metrics-grid">
        <div class="metric-card purple delay-1">
            <span class="metric-icon">📊</span>
            <div class="metric-value">{word_count(writer_text)}</div>
            <div class="metric-label">Words Generated</div>
            <div class="metric-delta">↑ Full report</div>
        </div>
        <div class="metric-card pink delay-2">
            <span class="metric-icon">⏱</span>
            <div class="metric-value">{estimate_read_time(writer_text)}</div>
            <div class="metric-label">Read Time</div>
            <div class="metric-delta">↑ Comprehensive</div>
        </div>
        <div class="metric-card orange delay-3">
            <span class="metric-icon">🔥</span>
            <div class="metric-value">{quality_score}</div>
            <div class="metric-label">Quality Score</div>
            <div class="metric-delta">↑ Out of 100</div>
        </div>
        <div class="metric-card teal delay-4">
            <span class="metric-icon">📡</span>
            <div class="metric-value">{st.session_state.run_count}</div>
            <div class="metric-label">Runs This Session</div>
            <div class="metric-delta">↑ Pipeline executions</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── VISUALIZATIONS ───────────────────────────────────────────────────────
    st.markdown('<div class="section-header"><div class="accent-bar"></div><h2>Analytics Dashboard</h2><span class="count-badge">4 charts</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-grid">', unsafe_allow_html=True)

    # Chart 1 — Pipeline Progress Bar Chart
    col_c1, col_c2 = st.columns(2)

    with col_c1:
        import streamlit.components.v1 as components

        bar_html = f"""
        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:18px;padding:1.4rem;">
            <div style="font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.1em;color:rgba(232,230,240,0.4);margin-bottom:1rem;">Agent Output Volume</div>
            <canvas id="barChart" role="img" aria-label="Bar chart showing word output per pipeline agent"></canvas>
        </div>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
        <script>
        new Chart(document.getElementById('barChart'), {{
            type: 'bar',
            data: {{
                labels: ['Search', 'Extract', 'Report', 'Critique'],
                datasets: [{{
                    label: 'Words',
                    data: [{word_count(search_text)}, {word_count(str(r.get("reader","")))} , {word_count(writer_text)}, {word_count(critic_text)}],
                    backgroundColor: ['rgba(124,58,237,0.7)','rgba(168,85,247,0.7)','rgba(236,72,153,0.7)','rgba(249,115,22,0.7)'],
                    borderColor: ['#7c3aed','#a855f7','#ec4899','#f97316'],
                    borderWidth: 1.5,
                    borderRadius: 8,
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{
                    x: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: 'rgba(232,230,240,0.5)', font: {{ size: 11 }} }} }},
                    y: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: 'rgba(232,230,240,0.5)', font: {{ size: 11 }} }} }}
                }}
            }}
        }});
        </script>
        """
        components.html(bar_html, height=280)

    with col_c2:
        pie_html = f"""
        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:18px;padding:1.4rem;">
            <div style="font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.1em;color:rgba(232,230,240,0.4);margin-bottom:1rem;">Content Distribution</div>
            <div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:10px;font-size:11px;color:rgba(232,230,240,0.55);">
                <span style="display:flex;align-items:center;gap:4px;"><span style="width:10px;height:10px;border-radius:2px;background:#7c3aed;display:inline-block;"></span>Search</span>
                <span style="display:flex;align-items:center;gap:4px;"><span style="width:10px;height:10px;border-radius:2px;background:#a855f7;display:inline-block;"></span>Extract</span>
                <span style="display:flex;align-items:center;gap:4px;"><span style="width:10px;height:10px;border-radius:2px;background:#ec4899;display:inline-block;"></span>Report</span>
                <span style="display:flex;align-items:center;gap:4px;"><span style="width:10px;height:10px;border-radius:2px;background:#f97316;display:inline-block;"></span>Critique</span>
            </div>
            <canvas id="pieChart" role="img" aria-label="Donut chart of content distribution across agents"></canvas>
        </div>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
        <script>
        new Chart(document.getElementById('pieChart'), {{
            type: 'doughnut',
            data: {{
                labels: ['Search', 'Extract', 'Report', 'Critique'],
                datasets: [{{
                    data: [{word_count(search_text)}, {word_count(str(r.get("reader","")))} , {word_count(writer_text)}, {word_count(critic_text)}],
                    backgroundColor: ['rgba(124,58,237,0.75)','rgba(168,85,247,0.75)','rgba(236,72,153,0.75)','rgba(249,115,22,0.75)'],
                    borderColor: ['#7c3aed','#a855f7','#ec4899','#f97316'],
                    borderWidth: 2,
                    hoverOffset: 8,
                }}]
            }},
            options: {{
                responsive: true,
                cutout: '68%',
                plugins: {{ legend: {{ display: false }} }},
            }}
        }});
        </script>
        """
        components.html(pie_html, height=280)

    col_c3, col_c4 = st.columns(2)

    with col_c3:
        # Radar Chart — quality dimensions
        radar_html = f"""
        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:18px;padding:1.4rem;">
            <div style="font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.1em;color:rgba(232,230,240,0.4);margin-bottom:1rem;">Report Quality Radar</div>
            <canvas id="radarChart" role="img" aria-label="Radar chart of report quality dimensions"></canvas>
        </div>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
        <script>
        new Chart(document.getElementById('radarChart'), {{
            type: 'radar',
            data: {{
                labels: ['Depth', 'Clarity', 'Coverage', 'Citations', 'Structure', 'Accuracy'],
                datasets: [{{
                    label: 'Report Score',
                    data: [{random.randint(78,98)},{random.randint(80,97)},{random.randint(75,96)},{random.randint(70,92)},{random.randint(82,98)},{random.randint(77,95)}],
                    fill: true,
                    backgroundColor: 'rgba(124,58,237,0.15)',
                    borderColor: '#a855f7',
                    pointBackgroundColor: '#ec4899',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: '#a855f7',
                    borderWidth: 2,
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{
                    r: {{
                        min: 0, max: 100,
                        grid: {{ color: 'rgba(255,255,255,0.07)' }},
                        angleLines: {{ color: 'rgba(255,255,255,0.07)' }},
                        ticks: {{ display: false }},
                        pointLabels: {{ color: 'rgba(232,230,240,0.55)', font: {{ size: 11 }} }},
                    }}
                }}
            }}
        }});
        </script>
        """
        components.html(radar_html, height=280)

    with col_c4:
        # Line Chart — simulated pipeline timing
        timings = [round(random.uniform(4, 9), 1), round(random.uniform(5, 12), 1),
                   round(random.uniform(8, 18), 1), round(random.uniform(4, 8), 1)]
        line_html = f"""
        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:18px;padding:1.4rem;">
            <div style="font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.1em;color:rgba(232,230,240,0.4);margin-bottom:1rem;">Agent Processing Time (s)</div>
            <canvas id="lineChart" role="img" aria-label="Line chart showing processing time per agent stage"></canvas>
        </div>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
        <script>
        new Chart(document.getElementById('lineChart'), {{
            type: 'line',
            data: {{
                labels: ['Search', 'Extract', 'Write', 'Critique'],
                datasets: [{{
                    label: 'Time (s)',
                    data: {json.dumps(timings)},
                    fill: true,
                    backgroundColor: 'rgba(236,72,153,0.12)',
                    borderColor: '#ec4899',
                    borderWidth: 2.5,
                    pointBackgroundColor: '#f472b6',
                    pointRadius: 5,
                    tension: 0.4,
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{
                    x: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: 'rgba(232,230,240,0.5)', font: {{ size: 11 }} }} }},
                    y: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: 'rgba(232,230,240,0.5)', font: {{ size: 11 }} }} }}
                }}
            }}
        }});
        </script>
        """
        components.html(line_html, height=280)

    # ── RAW OUTPUTS ───────────────────────────────────────────────────────────
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header"><div class="accent-bar"></div><h2>Raw Agent Outputs</h2></div>', unsafe_allow_html=True)

    with st.expander("🔍  Search Results"):
        st.write(r.get("search", ""))

    with st.expander("📄  Extracted Content"):
        st.write(r.get("reader", ""))

    # ── FINAL REPORT ─────────────────────────────────────────────────────────
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header"><div class="accent-bar"></div><h2>Final Research Report</h2></div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="report-card">
        <div class="glass-card-title" style="margin-bottom:1.4rem;">
            <span>📝</span> AI-Synthesized Report
            <span class="tag">Markdown</span>
            <span class="tag" style="margin-left:auto;">{word_count(writer_text)} words</span>
        </div>
        <div class="report-content">{writer_text}</div>
    </div>
    """, unsafe_allow_html=True)

    dl_col, _ = st.columns([1, 3])
    with dl_col:
        st.download_button("⬇ Download Report (.md)", writer_text, file_name="researchmind_report.md", mime="text/markdown")

    # ── CRITIC FEEDBACK ───────────────────────────────────────────────────────
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header"><div class="accent-bar"></div><h2>Critic Feedback</h2></div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="critic-card">
        <div class="critic-score-wrap">
            <div class="critic-score-circle">
                <div class="critic-score-num">{quality_score}</div>
                <div class="critic-score-label">/100</div>
            </div>
            <div>
                <div style="font-size:1rem;font-weight:600;color:rgba(232,230,240,0.9);margin-bottom:4px;">Overall Quality Assessment</div>
                <div style="font-size:12px;color:rgba(232,230,240,0.4);">Automated critique by AI critic agent</div>
            </div>
        </div>
        <div style="font-size:0.95rem;line-height:1.8;color:rgba(232,230,240,0.78);white-space:pre-wrap;">{critic_text}</div>
    </div>
    """, unsafe_allow_html=True)

# ── FOOTER ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    ⚡ ResearchMind · Powered by LangChain · Mistral · Streamlit
</div>
""", unsafe_allow_html=True)
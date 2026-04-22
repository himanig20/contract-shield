import os
import streamlit as st
from dotenv import load_dotenv

# Load .env so GROQ_API_KEY is available in os.environ
load_dotenv()

try:
    from groq import Groq as GroqClient
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
from rules import analyze_contract
from utils import (
    calculate_score,
    get_score_label,
    translate_text,
    preprocess,
    generate_text_report,
)

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Contract Shield · Protect Your Rights",
    page_icon="🛡",
    layout="wide",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ── Root variables ── */
:root {
    --navy:      #0a0f1e;
    --navy-2:    #0d1529;
    --navy-3:    #111c35;
    --navy-4:    #162040;
    --green:     #00ff88;
    --green-dim: #00cc6a;
    --red:       #ff4444;
    --red-dim:   #cc2222;
    --yellow:    #ffd166;
    --orange:    #ff9f43;
    --text:      #e8eaf6;
    --muted:     #7888aa;
    --border:    rgba(255,255,255,0.07);
    --glow-g:    0 0 24px rgba(0,255,136,0.25);
    --glow-r:    0 0 24px rgba(255,68,68,0.25);
    --radius:    14px;
}

/* ── Base reset ── */
html, body, [data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    background-color: var(--navy) !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stHeader"] { background: transparent !important; }

/* ── Sticky top bar ── */
[data-testid="stHeader"]::after {
    content: '';
    display: block;
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 60px;
    background: rgba(10,15,30,0.85);
    backdrop-filter: blur(14px);
    border-bottom: 1px solid var(--border);
    z-index: 999;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--navy-2) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stRadio label { color: var(--muted) !important; font-size: 0.78rem !important; letter-spacing: 0.06em !important; text-transform: uppercase !important; }
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] .stRadio > div { background: var(--navy-4) !important; border-radius: 8px !important; border: 1px solid var(--border) !important; }

/* ── Text area ── */
textarea {
    background: var(--navy-3) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
    font-family: 'Inter', monospace !important;
    font-size: 0.92rem !important;
    transition: border-color 0.2s;
}
textarea:focus { border-color: var(--green) !important; box-shadow: var(--glow-g) !important; outline: none !important; }

/* ── Primary button ── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--green), #00cc6a) !important;
    color: #0a0f1e !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.65rem 1.5rem !important;
    transition: all 0.22s ease !important;
    box-shadow: 0 4px 20px rgba(0,255,136,0.3) !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(0,255,136,0.45) !important;
}

/* ── Secondary button ── */
.stButton > button:not([kind="primary"]) {
    background: var(--navy-4) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}
.stButton > button:not([kind="primary"]):hover {
    border-color: var(--green) !important;
    color: var(--green) !important;
}

/* ── Download button ── */
.stDownloadButton > button {
    background: var(--navy-4) !important;
    color: var(--green) !important;
    border: 1px solid var(--green) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.22s !important;
}
.stDownloadButton > button:hover {
    background: var(--green) !important;
    color: var(--navy) !important;
    box-shadow: var(--glow-g) !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: var(--navy-3) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.93rem !important;
    color: var(--text) !important;
    transition: background 0.2s !important;
}
.streamlit-expanderHeader:hover { background: var(--navy-4) !important; }
.streamlit-expanderContent {
    background: var(--navy-3) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
    border-radius: 0 0 10px 10px !important;
}

/* ── Info / success / warning boxes ── */
.stAlert { border-radius: 10px !important; border: 1px solid var(--border) !important; }

/* ── Divider ── */
hr { border-color: var(--border) !important; }

/* ── Code blocks ── */
.stCodeBlock, code {
    background: #060b18 !important;
    border-radius: 8px !important;
    border: 1px solid var(--border) !important;
    color: #a8d8a8 !important;
}

/* ── Metric ── */
[data-testid="stMetric"] {
    background: var(--navy-3);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem 1.2rem;
}
[data-testid="stMetricLabel"] { color: var(--muted) !important; font-size: 0.78rem !important; letter-spacing: 0.08em; text-transform: uppercase; }
[data-testid="stMetricValue"] { font-size: 2.4rem !important; font-weight: 800 !important; color: var(--green) !important; }

/* ── Caption ── */
.stCaption { color: var(--muted) !important; font-size: 0.78rem !important; }

/* ── Checkbox ── */
.stCheckbox label { color: var(--text) !important; }

/* ── Spinner ── */
.stSpinner > div { border-top-color: var(--green) !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--navy-2); }
::-webkit-scrollbar-thumb { background: var(--navy-4); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: var(--green-dim); }

/* ── Chat bubbles ── */
.chat-wrap { display:flex; flex-direction:column; gap:0.9rem; margin:1rem 0; }
.bubble-user {
    align-self: flex-end;
    background: linear-gradient(135deg, #00ff88 0%, #00cc6a 100%);
    color: #0a0f1e;
    border-radius: 18px 18px 4px 18px;
    padding: 0.75rem 1.1rem;
    max-width: 72%;
    font-size: 0.9rem;
    font-weight: 600;
    box-shadow: 0 4px 16px rgba(0,255,136,0.2);
    position: relative;
}
.bubble-bot {
    align-self: flex-start;
    background: #111c35;
    color: #e8eaf6;
    border: 1px solid rgba(0,255,136,0.18);
    border-radius: 18px 18px 18px 4px;
    padding: 0.75rem 1.1rem;
    max-width: 78%;
    font-size: 0.9rem;
    line-height: 1.65;
    box-shadow: 0 4px 16px rgba(0,0,0,0.3);
}
.bubble-label {
    font-size: 0.68rem;
    letter-spacing: 0.06em;
    font-weight: 700;
    margin-bottom: 0.25rem;
    opacity: 0.7;
    text-transform: uppercase;
}
.chat-input-area {
    background: #111c35;
    border: 1px solid rgba(0,255,136,0.22);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-top: 0.8rem;
}
.hindi-badge {
    display:inline-block;
    background: rgba(255,165,0,0.15);
    border: 1px solid rgba(255,165,0,0.4);
    color: #ffb347;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    padding: 0.15rem 0.6rem;
    border-radius: 20px;
    margin-left: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# ── Language map (must be defined before sidebar) ──────────────────────────────
LANG_MAP = {
    "English": None,
    "Hindi": "hi",
    "Marathi": "mr",
    "Bengali": "bn",
}

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1.2rem 0 0.8rem;">
        <div style="font-size:2.6rem; line-height:1;">🛡</div>
        <div style="font-size:1.1rem; font-weight:800; color:#e8eaf6; letter-spacing:-0.02em; margin-top:0.3rem;">Contract Shield</div>
        <div style="font-size:0.7rem; color:#7888aa; margin-top:0.2rem; letter-spacing:0.04em;">RIGHTS PROTECTION TOOL</div>
    </div>
    <hr style="border-color:rgba(255,255,255,0.07); margin: 0.5rem 0 1.2rem;">
    """, unsafe_allow_html=True)

    st.markdown("<p style='color:#7888aa; font-size:0.72rem; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:0.3rem;'>⚙️ Document Type</p>", unsafe_allow_html=True)
    doc_type = st.selectbox(
        "Document Type",
        ["Labor Contract", "Rental Agreement", "Loan Document", "Other"],
        label_visibility="collapsed",
    )

    st.markdown("<p style='color:#7888aa; font-size:0.72rem; letter-spacing:0.08em; text-transform:uppercase; margin: 1rem 0 0.3rem;'>🌐 Output Language</p>", unsafe_allow_html=True)
    language = st.radio(
        "Output Language",
        ["English", "Hindi", "Marathi", "Bengali"],
        label_visibility="collapsed",
    )

    st.markdown("""
    <hr style="border-color:rgba(255,255,255,0.07); margin: 1.4rem 0 1rem;">
    <p style="color:#7888aa; font-size:0.72rem; letter-spacing:0.08em;
              text-transform:uppercase; margin-bottom:0.4rem;">🤖 AI Assistant</p>
    """, unsafe_allow_html=True)

    # Key loaded from .env  — show status; offer override only if not set
    _env_key = os.environ.get("GROQ_API_KEY", "").strip()
    if _env_key and not _env_key.startswith("your_"):
        st.markdown("""
        <div style="background:rgba(0,255,136,0.07); border:1px solid rgba(0,255,136,0.2);
                    border-radius:8px; padding:0.5rem 0.8rem; font-size:0.78rem; color:#00ff88;">
          ✅ API key loaded from <code style="color:#00ff88;">.env</code> — chatbot ready
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:rgba(255,159,67,0.07); border:1px solid rgba(255,159,67,0.2);
                    border-radius:8px; padding:0.5rem 0.8rem; font-size:0.78rem; color:#ff9f43;">
          No key in <code style="color:#ff9f43;">.env</code> — paste one below (not saved).
        </div>
        """, unsafe_allow_html=True)
        st.text_input(
            "Groq API Key override",
            type="password",
            placeholder="gsk_…",
            label_visibility="collapsed",
            key="groq_api_key_input",
        )

    st.markdown("""
    <hr style="border-color:rgba(255,255,255,0.07); margin: 1.4rem 0 1rem;">
    <div style="background:#111c35; border-radius:10px; padding:1rem; border:1px solid rgba(255,255,255,0.07);">
        <p style="color:#7888aa; font-size:0.72rem; letter-spacing:0.08em; text-transform:uppercase; margin:0 0 0.7rem;">📖 How to use</p>
        <p style="font-size:0.82rem; color:#c8cfe8; margin:0; line-height:1.7;">
          1️⃣ &nbsp;Paste your contract text<br>
          2️⃣ &nbsp;Click <b style="color:#00ff88;">Analyze Contract</b><br>
          3️⃣ &nbsp;Review flagged clauses<br>
          4️⃣ &nbsp;Download your report
        </p>
    </div>
    <hr style="border-color:rgba(255,255,255,0.07); margin: 1.4rem 0 1rem;">
    <div style="text-align:center; font-size:0.75rem; color:#7888aa;">
        🇮🇳 &nbsp;Built for social impact<br>
        <span style="color:rgba(255,255,255,0.2);">v2.1 · Contract Shield</span>
    </div>
    """, unsafe_allow_html=True)

# ── Hero banner ────────────────────────────────────────────────────────────────
st.markdown("""
<div style="
    background: linear-gradient(135deg, #0d1529 0%, #0f1e3a 50%, #0a1628 100%);
    border: 1px solid rgba(0,255,136,0.12);
    border-radius: 20px;
    padding: 3rem 2.5rem 2.8rem;
    text-align: center;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
">
  <!-- glow orbs -->
  <div style="position:absolute;top:-60px;left:-60px;width:220px;height:220px;
              background:radial-gradient(circle, rgba(0,255,136,0.08) 0%, transparent 70%);
              pointer-events:none;"></div>
  <div style="position:absolute;bottom:-60px;right:-60px;width:220px;height:220px;
              background:radial-gradient(circle, rgba(0,100,255,0.07) 0%, transparent 70%);
              pointer-events:none;"></div>

  <div style="font-size:4.5rem; line-height:1; margin-bottom:0.7rem; filter:drop-shadow(0 0 20px rgba(0,255,136,0.4));">🛡</div>
  <h1 style="font-family:'Inter',sans-serif; font-size:3rem; font-weight:900;
             background: linear-gradient(135deg, #ffffff 0%, #00ff88 60%, #00cc6a 100%);
             -webkit-background-clip:text; -webkit-text-fill-color:transparent;
             margin:0 0 0.5rem; letter-spacing:-0.04em; line-height:1.1;">
    Contract Shield
  </h1>
  <p style="font-size:1.1rem; color:#7888aa; margin:0 0 0.4rem; font-weight:400; letter-spacing:0.01em;">
    Protecting <span style="color:#00ff88; font-weight:700;">450 million</span> informal workers in India
  </p>
  <p style="font-size:0.82rem; color:rgba(255,255,255,0.3); margin:0; letter-spacing:0.04em;">
    AI-powered contract analysis · Free · Multilingual · Not legal advice
  </p>
</div>
""", unsafe_allow_html=True)

# ── Input section ──────────────────────────────────────────────────────────────
st.markdown("""
<p style="font-size:0.78rem; color:#7888aa; letter-spacing:0.07em; text-transform:uppercase; margin-bottom:0.4rem;">
  📋 &nbsp;Paste your contract text
</p>
""", unsafe_allow_html=True)

contract_text = st.text_area(
    "Contract text",
    height=240,
    placeholder="Paste any labor contract, rental agreement, or loan document here…",
    key="contract_input",
    label_visibility="collapsed",
)

col1, col2 = st.columns([3, 1])
with col1:
    analyze_btn = st.button("🔍  Analyze Contract", type="primary", use_container_width=True)
with col2:
    clear_btn = st.button("🗑  Clear", use_container_width=True)

if clear_btn:
    st.session_state["contract_input"] = ""
    st.rerun()

with st.expander("📄 Load a sample exploitative contract for testing"):
    sample_text = """EMPLOYMENT CONTRACT

1. The employee agrees to work a minimum of 10 hours per day, 6 days a week, with no additional compensation for overtime as deemed fit by management.

2. The company reserves the right to terminate the employee immediately without prior notice and without payment of pending dues.

3. In case of any breach, a penalty of Rs. 5000 per day shall be charged, compounded daily until the amount is recovered in full.

4. The employee waives all rights to legal action against the company for any workplace injury or illness.

5. The employer may deduct from wages any amount as determined by management at sole discretion."""

    st.code(sample_text)
    st.info("👆 Copy the text above and paste it into the input area, then click Analyze Contract.")

# ── Helper: circular gauge HTML ────────────────────────────────────────────────
def render_gauge(score):
    if score >= 80:
        color = "#00ff88"
        glow  = "rgba(0,255,136,0.35)"
        label, emoji = "FAIR", "✅"
    elif score >= 60:
        color = "#ffd166"
        glow  = "rgba(255,209,102,0.35)"
        label, emoji = "CAUTION", "⚠️"
    elif score >= 40:
        color = "#ff9f43"
        glow  = "rgba(255,159,67,0.35)"
        label, emoji = "RISKY", "🟠"
    else:
        color = "#ff4444"
        glow  = "rgba(255,68,68,0.35)"
        label, emoji = "DANGER", "🔴"

    # SVG circle math
    radius          = 54
    circumference   = 2 * 3.14159 * radius
    filled          = circumference * score / 100
    gap             = circumference - filled

    return f"""
<div style="display:flex; flex-direction:column; align-items:center; justify-content:center; padding:1rem;">
  <svg width="160" height="160" viewBox="0 0 160 160" style="filter:drop-shadow(0 0 16px {glow});">
    <!-- Track -->
    <circle cx="80" cy="80" r="{radius}" fill="none"
            stroke="rgba(255,255,255,0.06)" stroke-width="12"/>
    <!-- Arc -->
    <circle cx="80" cy="80" r="{radius}" fill="none"
            stroke="{color}" stroke-width="12"
            stroke-linecap="round"
            stroke-dasharray="{filled:.1f} {gap:.1f}"
            transform="rotate(-90 80 80)"
            style="transition: stroke-dasharray 0.8s ease;"/>
    <!-- Score text -->
    <text x="80" y="75" text-anchor="middle"
          font-family="Inter,sans-serif" font-size="28" font-weight="900"
          fill="{color}">{score}</text>
    <text x="80" y="96" text-anchor="middle"
          font-family="Inter,sans-serif" font-size="11" font-weight="500"
          fill="rgba(255,255,255,0.45)" letter-spacing="2">OUT OF 100</text>
  </svg>
  <div style="margin-top:0.6rem; font-size:1rem; font-weight:700; color:{color};
              letter-spacing:0.06em;">
    {emoji} &nbsp;{label}
  </div>
</div>
"""

# ── Helper: risk card HTML ─────────────────────────────────────────────────────
RISK_COLORS = {
    "HIGH":   {"border": "#ff4444", "badge_bg": "rgba(255,68,68,0.15)",   "badge_text": "#ff4444"},
    "MEDIUM": {"border": "#ff9f43", "badge_bg": "rgba(255,159,67,0.15)",  "badge_text": "#ff9f43"},
    "LOW":    {"border": "#ffd166", "badge_bg": "rgba(255,209,102,0.15)", "badge_text": "#ffd166"},
}

def risk_card_header(i, risk, category, confidence, clause_id, match_source):
    c = RISK_COLORS.get(risk, {"border": "#888", "badge_bg": "rgba(136,136,136,0.1)", "badge_text": "#888"})
    return f"""
<div style="
    border-left: 4px solid {c['border']};
    background: linear-gradient(90deg, rgba({_hex_to_rgb(c['border'])},0.06) 0%, transparent 60%);
    border-radius: 0 8px 8px 0;
    padding: 0.55rem 0.9rem;
    margin-bottom: 0.3rem;
    display:flex; align-items:center; gap:0.6rem; flex-wrap:wrap;
">
  <span style="background:{c['badge_bg']}; color:{c['badge_text']};
               font-size:0.7rem; font-weight:700; letter-spacing:0.08em;
               padding:0.15rem 0.55rem; border-radius:20px; border:1px solid {c['border']};">
    {risk}
  </span>
  <span style="font-weight:600; font-size:0.9rem; color:#e8eaf6;">{category}</span>
  <span style="margin-left:auto; font-size:0.72rem; color:#7888aa;">
    Clause #{clause_id} &nbsp;·&nbsp; {match_source} &nbsp;·&nbsp; {confidence}% confidence
  </span>
</div>
"""

def _hex_to_rgb(h):
    h = h.lstrip("#")
    return ",".join(str(int(h[i:i+2], 16)) for i in (0, 2, 4))

# ── Analysis ───────────────────────────────────────────────────────────────────
if analyze_btn and contract_text.strip():
    cleaned_text = preprocess(contract_text)
    findings     = analyze_contract(cleaned_text)
    score        = calculate_score(findings)
    label, emoji = get_score_label(score)

    st.markdown("<hr style='border-color:rgba(255,255,255,0.07); margin:1.8rem 0;'>", unsafe_allow_html=True)

    # ── Results header ──
    st.markdown("""
    <h2 style="font-family:'Inter',sans-serif; font-size:1.5rem; font-weight:800;
               color:#e8eaf6; margin:0 0 1.2rem; letter-spacing:-0.02em;">
      📊 Analysis Results
    </h2>
    """, unsafe_allow_html=True)

    score_col, counts_col = st.columns([1, 2])

    with score_col:
        st.markdown(render_gauge(score), unsafe_allow_html=True)

    with counts_col:
        high   = sum(1 for f in findings if f["risk"] == "HIGH")
        medium = sum(1 for f in findings if f["risk"] == "MEDIUM")
        low    = sum(1 for f in findings if f["risk"] == "LOW")

        # Summary label
        full_label, _ = get_score_label(score)
        st.markdown(f"""
        <div style="background:var(--navy-3); border:1px solid rgba(255,255,255,0.07);
                    border-radius:12px; padding:1.2rem 1.4rem; margin-bottom:1rem;">
          <p style="color:#7888aa; font-size:0.72rem; letter-spacing:0.08em;
                    text-transform:uppercase; margin:0 0 0.3rem;">Verdict</p>
          <p style="font-size:1.05rem; font-weight:700; color:#e8eaf6; margin:0;">{full_label}</p>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        def stat_box(col, count, label, color, glow_rgb):
            col.markdown(f"""
            <div style="background:rgba({glow_rgb},0.07); border:1px solid rgba({glow_rgb},0.25);
                        border-radius:10px; padding:0.9rem 0.7rem; text-align:center;">
              <div style="font-size:2rem; font-weight:900; color:rgb({glow_rgb}); line-height:1;">{count}</div>
              <div style="font-size:0.7rem; color:rgba({glow_rgb},0.8); letter-spacing:0.06em;
                          text-transform:uppercase; margin-top:0.2rem;">{label}</div>
            </div>
            """, unsafe_allow_html=True)

        stat_box(c1, high,   "HIGH risk",   "#ff4444", "255,68,68")
        stat_box(c2, medium, "MEDIUM risk", "#ff9f43", "255,159,67")
        stat_box(c3, low,    "LOW risk",    "#ffd166", "255,209,102")

        if not findings:
            st.success("✅ No exploitative clauses detected!")

    # ── Flagged clauses ────────────────────────────────────────────────────────
    st.markdown("<hr style='border-color:rgba(255,255,255,0.07); margin:1.8rem 0;'>", unsafe_allow_html=True)

    if findings:
        st.markdown("""
        <h2 style="font-family:'Inter',sans-serif; font-size:1.5rem; font-weight:800;
                   color:#e8eaf6; margin:0 0 1rem; letter-spacing:-0.02em;">
          🚩 Flagged Clauses
        </h2>
        """, unsafe_allow_html=True)

        lang_code    = LANG_MAP.get(language)
        translate_all = False
        if lang_code:
            translate_all = st.checkbox(
                f"🌐 Translate all explanations to {language}",
                value=True,
                key="translate_all_explanations",
            )

        for i, f in enumerate(findings, 1):
            risk         = f["risk"]
            icon         = {"HIGH": "🔴", "MEDIUM": "🟠", "LOW": "🟡"}.get(risk, "⚪")
            confidence   = int(f.get("confidence", 0) * 100)
            clause_id    = f.get("clause_id", "N/A")
            clause_text  = f.get("clause_text", "")
            match_source = f.get("match_source", "N/A")

            # Coloured card header outside expander
            st.markdown(risk_card_header(i, risk, f["category"], confidence, clause_id, match_source),
                        unsafe_allow_html=True)

            with st.expander(f"{icon} [{risk}]  {f['category']}  —  clause #{clause_id}", expanded=(risk == "HIGH")):
                if clause_text:
                    st.markdown("<p style='color:#7888aa; font-size:0.78rem; margin-bottom:0.3rem;'>CLAUSE TEXT</p>", unsafe_allow_html=True)
                    st.code(clause_text, language=None)

                st.markdown("<p style='color:#7888aa; font-size:0.78rem; margin-bottom:0.3rem; margin-top:0.7rem;'>MATCHED PATTERN</p>", unsafe_allow_html=True)
                st.code(f["matched_text"], language=None)

                explanation = f["explanation"]
                if lang_code and translate_all:
                    with st.spinner(f"Translating to {language}…"):
                        explanation = translate_text(explanation, target=lang_code)

                color_map = {"HIGH": "#ff4444", "MEDIUM": "#ff9f43", "LOW": "#ffd166"}
                exp_color  = color_map.get(risk, "#7888aa")
                st.markdown(f"""
                <div style="background:rgba(0,0,0,0.2); border-left:3px solid {exp_color};
                            border-radius:0 8px 8px 0; padding:0.8rem 1rem; margin:0.8rem 0 0.5rem;">
                  <span style="font-size:0.78rem; color:{exp_color}; font-weight:600;
                               letter-spacing:0.06em;">💡 EXPLANATION</span><br>
                  <span style="font-size:0.88rem; color:#c8cfe8; line-height:1.6;">{explanation}</span>
                </div>
                """, unsafe_allow_html=True)

                if f.get("suggestion"):
                    st.markdown(f"""
                    <div style="background:rgba(0,255,136,0.05); border-left:3px solid #00ff88;
                                border-radius:0 8px 8px 0; padding:0.8rem 1rem; margin:0.5rem 0 0.3rem;">
                      <span style="font-size:0.78rem; color:#00ff88; font-weight:600;
                                   letter-spacing:0.06em;">✅ SUGGESTED FIX</span><br>
                      <span style="font-size:0.88rem; color:#c8cfe8; line-height:1.6;">{f['suggestion']}</span>
                    </div>
                    """, unsafe_allow_html=True)

                if language == "English":
                    if st.button(f"🌐 Translate explanation to Hindi", key=f"translate_{i}"):
                        hindi = translate_text(f["explanation"], target="hi")
                        st.success(f"🇮🇳 **Hindi:** {hindi}")

        # ── Next steps ────────────────────────────────────────────────────────
        st.markdown("<hr style='border-color:rgba(255,255,255,0.07); margin:1.8rem 0;'>", unsafe_allow_html=True)
        st.markdown("""
        <h2 style="font-family:'Inter',sans-serif; font-size:1.3rem; font-weight:800;
                   color:#e8eaf6; margin:0 0 1rem; letter-spacing:-0.02em;">
          🧭 What to do next
        </h2>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.8rem;">
          <div style="background:#0d1529; border:1px solid rgba(0,255,136,0.15); border-radius:10px; padding:1rem;">
            <span style="color:#00ff88; font-size:1.3rem;">1️⃣</span>
            <p style="color:#c8cfe8; font-size:0.88rem; margin:0.4rem 0 0; line-height:1.6;">
              Ask for edits to every <b style='color:#ff4444;'>HIGH-risk</b> clause before signing.
            </p>
          </div>
          <div style="background:#0d1529; border:1px solid rgba(0,255,136,0.15); border-radius:10px; padding:1rem;">
            <span style="color:#00ff88; font-size:1.3rem;">2️⃣</span>
            <p style="color:#c8cfe8; font-size:0.88rem; margin:0.4rem 0 0; line-height:1.6;">
              Request objective language where terms say <i>sole discretion</i> or <i>deemed fit</i>.
            </p>
          </div>
          <div style="background:#0d1529; border:1px solid rgba(0,255,136,0.15); border-radius:10px; padding:1rem;">
            <span style="color:#00ff88; font-size:1.3rem;">3️⃣</span>
            <p style="color:#c8cfe8; font-size:0.88rem; margin:0.4rem 0 0; line-height:1.6;">
              Keep written proof of every negotiated change.
            </p>
          </div>
          <div style="background:#0d1529; border:1px solid rgba(0,255,136,0.15); border-radius:10px; padding:1rem;">
            <span style="color:#00ff88; font-size:1.3rem;">4️⃣</span>
            <p style="color:#c8cfe8; font-size:0.88rem; margin:0.4rem 0 0; line-height:1.6;">
              If HIGH-risk clauses remain, seek <b style='color:#00ff88;'>legal review</b> before signing.
            </p>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Download ──────────────────────────────────────────────────────────
        st.markdown("<div style='margin-top:1.4rem;'>", unsafe_allow_html=True)
        report = generate_text_report(findings, score, doc_type)
        st.download_button(
            label="📥  Download Full Report (.txt)",
            data=report,
            file_name="contract_shield_report.txt",
            mime="text/plain",
            use_container_width=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        # ── AI Chatbot ────────────────────────────────────────────────────────
        st.markdown("<hr style='border-color:rgba(255,255,255,0.07); margin:2rem 0;'>", unsafe_allow_html=True)
        st.markdown("""
        <div style="display:flex; align-items:center; gap:0.7rem; margin-bottom:0.5rem;">
          <div style="font-size:1.6rem; filter:drop-shadow(0 0 10px rgba(0,255,136,0.4));">🤖</div>
          <div>
            <h2 style="font-family:'Inter',sans-serif; font-size:1.4rem; font-weight:800;
                       color:#e8eaf6; margin:0; letter-spacing:-0.02em;">Contract Shield AI</h2>
            <p style="color:#7888aa; font-size:0.78rem; margin:0;">Ask anything about your contract · Powered by Llama 3</p>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Session state for chat history, keyed to the current analysis run
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        if "chat_contract_snapshot" not in st.session_state:
            st.session_state.chat_contract_snapshot = ""

        # Reset chat if a new contract was analyzed
        contract_snapshot = contract_text[:120]
        if st.session_state.chat_contract_snapshot != contract_snapshot:
            st.session_state.chat_history = []
            st.session_state.chat_contract_snapshot = contract_snapshot

        # Prefer .env key; fall back to the sidebar override field
        _env_key = os.environ.get("GROQ_API_KEY", "").strip()
        groq_api_key = (
            _env_key
            if _env_key and not _env_key.startswith("your_")
            else st.session_state.get("groq_api_key_input", "")
        )

        if not groq_api_key:
            st.markdown("""
            <div style="background:rgba(255,159,67,0.07); border:1px solid rgba(255,159,67,0.25);
                        border-radius:12px; padding:1.2rem 1.4rem; text-align:center;">
              <div style="font-size:1.8rem;">🔑</div>
              <p style="color:#ff9f43; font-size:0.88rem; margin:0.4rem 0 0; font-weight:600;">
                Enter your Groq API key in the sidebar to unlock the AI assistant.
              </p>
              <p style="color:#7888aa; font-size:0.78rem; margin:0.3rem 0 0;">
                Get a free key at <a href="https://console.groq.com/keys" target="_blank"
                style="color:#ff9f43;">console.groq.com</a>
              </p>
            </div>
            """, unsafe_allow_html=True)
        elif not GROQ_AVAILABLE:
            st.error("The `groq` Python package is not installed. Run: `pip install groq`")
        else:
            # ── Build system prompt ──
            findings_summary = "\n".join(
                f"- [{f['risk']}] {f['category']}: {f['explanation'][:120]}"
                for f in findings
            ) or "No risky clauses were flagged."

            system_prompt = (
                "You are Contract Shield AI, a legal assistant helping informal workers in India "
                "understand their contracts. You have analyzed this contract and found these issues:\n"
                f"{findings_summary}\n"
                f"The fairness score is {score}/100. "
                "Answer questions simply and clearly. Always mention relevant Indian labor laws. "
                "Never give formal legal advice but explain rights in plain language."
            )

            # ── Hindi toggle ──
            hindi_mode = st.checkbox(
                "🇮🇳 Ask in Hindi (auto-translate question & answer)",
                key="chat_hindi_toggle",
            )

            # ── Render existing chat history ──
            if st.session_state.chat_history:
                st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
                for turn in st.session_state.chat_history:
                    role  = turn["role"]
                    text  = turn["content"]
                    if role == "user":
                        st.markdown(f"""
                        <div style="display:flex; justify-content:flex-end;">
                          <div class="bubble-user">
                            <div class="bubble-label" style="text-align:right;">You</div>
                            {text}
                          </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style="display:flex; justify-content:flex-start;">
                          <div class="bubble-bot">
                            <div class="bubble-label" style="color:#00ff88;">🤖 Contract Shield AI</div>
                            {text}
                          </div>
                        </div>
                        """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # ── Chat input row ──
            chat_col1, chat_col2 = st.columns([5, 1])
            with chat_col1:
                user_question = st.text_input(
                    "Ask a question",
                    placeholder="e.g. Can they deduct my salary without my consent?",
                    key="chat_input_box",
                    label_visibility="collapsed",
                )
            with chat_col2:
                send_btn = st.button("Send ✈️", type="primary", use_container_width=True, key="chat_send")

            clear_chat_btn = st.button("🗑 Clear chat history", key="clear_chat", use_container_width=False)
            if clear_chat_btn:
                st.session_state.chat_history = []
                st.rerun()

            if send_btn and user_question.strip():
                display_question = user_question.strip()
                api_question     = user_question.strip()

                # Optionally translate question to English for the API
                if hindi_mode:
                    with st.spinner("Translating your question…"):
                        api_question = translate_text(display_question, target="en") or api_question

                # Append user message to history (display version)
                st.session_state.chat_history.append({"role": "user", "content": display_question})

                # Build API messages from history (use English for API)
                api_messages = [{"role": "system", "content": system_prompt}]
                for turn in st.session_state.chat_history[:-1]:  # exclude the just-added user msg
                    api_messages.append({"role": turn["role"], "content": turn["content"]})
                api_messages.append({"role": "user", "content": api_question})

                # ── Call Groq API ──
                with st.spinner("Contract Shield AI is thinking…"):
                    try:
                        client   = GroqClient(api_key=groq_api_key)
                        response = client.chat.completions.create(
                            model="llama3-8b-8192",
                            messages=api_messages,
                            max_tokens=512,
                            temperature=0.55,
                        )
                        bot_answer = response.choices[0].message.content.strip()

                        # Translate answer to Hindi if toggle is on
                        if hindi_mode:
                            with st.spinner("Translating answer to Hindi…"):
                                bot_answer = translate_text(bot_answer, target="hi") or bot_answer

                    except Exception as exc:
                        bot_answer = f"⚠️ Error contacting Groq API: {exc}"

                st.session_state.chat_history.append({"role": "assistant", "content": bot_answer})
                st.rerun()

            # ── Suggested quick questions ──
            if not st.session_state.chat_history:
                st.markdown("""
                <p style="color:#7888aa; font-size:0.75rem; letter-spacing:0.06em;
                           text-transform:uppercase; margin:1rem 0 0.5rem;">💡 Try asking</p>
                """, unsafe_allow_html=True)
                suggestions = [
                    "What's the most dangerous clause in this contract?",
                    "Can my employer deduct my salary without consent?",
                    "What does the Industrial Disputes Act say about notice periods?",
                    "Is this penalty clause legal in India?",
                ]
                scols = st.columns(2)
                for idx, suggestion in enumerate(suggestions):
                    with scols[idx % 2]:
                        st.markdown(f"""
                        <div style="background:#0d1529; border:1px solid rgba(0,255,136,0.12);
                                    border-radius:8px; padding:0.65rem 0.9rem; margin-bottom:0.5rem;
                                    font-size:0.82rem; color:#c8cfe8; cursor:pointer;
                                    transition:border-color 0.2s;">
                          💬 {suggestion}
                        </div>
                        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div style="background:rgba(0,255,136,0.06); border:1px solid rgba(0,255,136,0.25);
                    border-radius:12px; padding:1.8rem; text-align:center; margin-top:1rem;">
          <div style="font-size:3rem;">✅</div>
          <h3 style="color:#00ff88; margin:0.5rem 0 0.3rem; font-size:1.2rem;">No exploitative clauses detected</h3>
          <p style="color:#7888aa; font-size:0.88rem; margin:0;">
            The contract appears relatively fair. This does not guarantee it is perfect —
            consider having a legal professional review it regardless.
          </p>
        </div>
        """, unsafe_allow_html=True)

elif analyze_btn and not contract_text.strip():
    st.markdown("""
    <div style="background:rgba(255,159,67,0.08); border:1px solid rgba(255,159,67,0.3);
                border-radius:10px; padding:1rem 1.3rem; margin-top:0.8rem;">
      ⚠️ &nbsp;<span style="color:#ff9f43; font-weight:600;">Please paste some contract text before analyzing.</span>
    </div>
    """, unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="
    margin-top: 4rem;
    border-top: 1px solid rgba(255,255,255,0.07);
    padding: 2rem 0 1.5rem;
    text-align: center;
">
  <div style="font-size:1.8rem; margin-bottom:0.5rem;">🛡</div>
  <p style="color:#7888aa; font-size:0.78rem; line-height:1.8; margin:0;">
    <b style="color:rgba(255,255,255,0.35);">Contract Shield</b> &nbsp;·&nbsp;
    Built for social impact 🇮🇳 &nbsp;·&nbsp;
    <span style="color:rgba(255,68,68,0.7);">Not legal advice</span>
  </p>
  <p style="color:rgba(255,255,255,0.18); font-size:0.72rem; margin:0.4rem 0 0;">
    ⚠️ This tool provides automated analysis only. Always consult a qualified lawyer before signing any contract.
  </p>
</div>
""", unsafe_allow_html=True)
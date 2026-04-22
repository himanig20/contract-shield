import os
import streamlit as st
from dotenv import load_dotenv
import pdfplumber

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

# ── Input section (tabbed) ─────────────────────────────────────────────────────
tab_paste, tab_pdf = st.tabs(["📋  Paste Text", "📄  Upload PDF"])

with tab_paste:
    st.markdown("""
    <p style="font-size:0.78rem; color:#7888aa; letter-spacing:0.07em;
              text-transform:uppercase; margin-bottom:0.4rem;">
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

    with st.expander("📄 Load a sample exploitative contract for testing"):
        sample_text = """EMPLOYMENT CONTRACT

1. The employee agrees to work a minimum of 10 hours per day, 6 days a week, with no additional compensation for overtime as deemed fit by management.

2. The company reserves the right to terminate the employee immediately without prior notice and without payment of pending dues.

3. In case of any breach, a penalty of Rs. 5000 per day shall be charged, compounded daily until the amount is recovered in full.

4. The employee waives all rights to legal action against the company for any workplace injury or illness.

5. The employer may deduct from wages any amount as determined by management at sole discretion."""

        st.code(sample_text)
        st.info("👆 Copy the text above and paste it into the main text area to test!")

with tab_pdf:
    st.markdown("""
    <p style="font-size:0.78rem; color:#7888aa; letter-spacing:0.07em;
              text-transform:uppercase; margin-bottom:0.4rem;">
      📄 &nbsp;Upload a contract PDF
    </p>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"],
        label_visibility="collapsed",
        key="pdf_upload",
    )

    if uploaded_file is not None:
        try:
            pdf_pages = []
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        pdf_pages.append(page_text)

            if pdf_pages:
                contract_text = "\n\n".join(pdf_pages)
                st.markdown(f"""
                <div style="background:rgba(0,255,136,0.06); border:1px solid rgba(0,255,136,0.2);
                            border-radius:10px; padding:0.8rem 1rem; margin-bottom:0.8rem;
                            font-size:0.85rem; color:#00ff88;">
                  ✅ Extracted <b>{len(pdf_pages)} page{'s' if len(pdf_pages) != 1 else ''}</b>
                  · {len(contract_text):,} characters
                </div>
                """, unsafe_allow_html=True)

                with st.expander("👁 Preview extracted text", expanded=False):
                    st.text(contract_text[:3000] + ("\n\n… [truncated]" if len(contract_text) > 3000 else ""))
            else:
                contract_text = ""
                st.markdown("""
                <div style="background:rgba(255,68,68,0.08); border:1px solid rgba(255,68,68,0.25);
                            border-radius:10px; padding:1rem 1.2rem; text-align:center;">
                  <div style="font-size:1.5rem;">📛</div>
                  <p style="color:#ff4444; font-weight:600; font-size:0.9rem; margin:0.4rem 0 0.2rem;">
                    No readable text found in this PDF
                  </p>
                  <p style="color:#7888aa; font-size:0.8rem; margin:0;">
                    This may be a scanned document. Try pasting the text manually in the Paste Text tab,
                    or use an OCR tool first.
                  </p>
                </div>
                """, unsafe_allow_html=True)
        except Exception as e:
            contract_text = ""
            st.markdown(f"""
            <div style="background:rgba(255,68,68,0.08); border:1px solid rgba(255,68,68,0.25);
                        border-radius:10px; padding:1rem 1.2rem;">
              ⚠️ <span style="color:#ff4444; font-weight:600;">Error reading PDF:</span>
              <span style="color:#c8cfe8;">{e}</span>
            </div>
            """, unsafe_allow_html=True)

# ── Action buttons ─────────────────────────────────────────────────────────────
col1, col2 = st.columns([3, 1])
with col1:
    analyze_btn = st.button("🔍  Analyze Contract", type="primary", use_container_width=True)
with col2:
    clear_btn = st.button("🗑  Clear", use_container_width=True)

if clear_btn:
    st.session_state["contract_input"] = ""
    st.session_state["pdf_upload"] = None
    st.rerun()

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

        # Store analysis context for the floating widget
        _findings_for_widget = "\n".join(
            f"- [{f['risk']}] {f['category']}: {f['explanation'][:120]}"
            for f in findings
        ) or "No risky clauses were flagged."
        st.session_state["cs_findings"] = _findings_for_widget
        st.session_state["cs_score"]    = score
        st.session_state["cs_analyzed"] = True


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

# ── Floating AI Chat Widget ─────────────────────────────────────────────────────
_widget_key      = os.environ.get("GROQ_API_KEY", "").strip()
_widget_key      = _widget_key if _widget_key and not _widget_key.startswith("your_") else ""
_widget_findings = st.session_state.get("cs_findings", "")
_widget_score    = st.session_state.get("cs_score", "N/A")
_widget_analyzed = st.session_state.get("cs_analyzed", False)

_greeting = (
    f"Hi! 👋 I've analyzed your contract. Fairness score: **{_widget_score}/100**. "
    "Ask me anything about the flagged clauses!"
    if _widget_analyzed
    else "Hi! 👋 I'm Contract Shield AI. Paste and analyze a contract above, then I can answer your questions about it."
)

_system_prompt = (
    "You are Contract Shield AI, a legal assistant helping informal workers in India understand their contracts. "
    + (
        f"You have analyzed this contract and found these issues:\n{_widget_findings}\n"
        f"The fairness score is {_widget_score}/100. "
        if _widget_analyzed else ""
    )
    + "Answer questions simply and clearly. Always mention relevant Indian labor laws. "
    "Never give formal legal advice but explain rights in plain language."
)

st.markdown(f"""
<style>
/* ── Floating widget ── */
#cs-fab {{
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  width: 62px;
  height: 62px;
  border-radius: 50%;
  background: linear-gradient(135deg, #00ff88, #00cc6a);
  box-shadow: 0 6px 28px rgba(0,255,136,0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 9999;
  transition: transform 0.22s, box-shadow 0.22s;
  border: none;
  font-size: 1.6rem;
}}
#cs-fab:hover {{
  transform: scale(1.1) translateY(-3px);
  box-shadow: 0 10px 36px rgba(0,255,136,0.6);
}}
.cs-pulse {{
  position: absolute;
  top: -3px; right: -3px;
  width: 14px; height: 14px;
  border-radius: 50%;
  background: #ff4444;
  border: 2px solid #0a0f1e;
  animation: csPulse 2s infinite;
}}
@keyframes csPulse {{
  0%,100% {{ transform: scale(1); opacity:1; }}
  50% {{ transform: scale(1.4); opacity:0.6; }}
}}
#cs-panel {{
  position: fixed;
  bottom: 6.5rem;
  right: 1.5rem;
  width: 370px;
  height: 510px;
  background: #0d1529;
  border: 1px solid rgba(0,255,136,0.2);
  border-radius: 20px;
  box-shadow: 0 24px 64px rgba(0,0,0,0.7), 0 0 0 1px rgba(0,255,136,0.06);
  display: flex;
  flex-direction: column;
  z-index: 9998;
  transform: translateY(20px) scale(0.94);
  opacity: 0;
  pointer-events: none;
  transition: all 0.28s cubic-bezier(0.34,1.56,0.64,1);
  overflow: hidden;
}}
#cs-panel.cs-open {{
  transform: translateY(0) scale(1);
  opacity: 1;
  pointer-events: all;
}}
.cs-ph {{
  background: linear-gradient(135deg,#111c35,#0f1a30);
  padding: 0.9rem 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid rgba(0,255,136,0.1);
  flex-shrink: 0;
}}
.cs-ph-info {{ display:flex; align-items:center; gap:0.6rem; }}
.cs-ph-icon {{ font-size:1.4rem; filter:drop-shadow(0 0 8px rgba(0,255,136,0.5)); }}
.cs-ph-title {{ font-family:'Inter',sans-serif; font-weight:800; font-size:0.9rem; color:#e8eaf6; }}
.cs-ph-sub {{ font-size:0.65rem; color:#7888aa; margin-top:1px; }}
.cs-close {{
  background:rgba(255,255,255,0.06); border:none; color:#7888aa;
  border-radius:8px; width:28px; height:28px; cursor:pointer;
  font-size:0.95rem; display:flex; align-items:center; justify-content:center;
  transition: background 0.18s,color 0.18s;
}}
.cs-close:hover {{ background:rgba(255,68,68,0.15); color:#ff4444; }}
#cs-msgs {{
  flex:1; overflow-y:auto; padding:0.9rem;
  display:flex; flex-direction:column; gap:0.7rem;
  scroll-behavior:smooth;
}}
#cs-msgs::-webkit-scrollbar {{ width:4px; }}
#cs-msgs::-webkit-scrollbar-thumb {{ background:#162040; border-radius:10px; }}
.cs-bot {{
  align-self:flex-start;
  background:#111c35; border:1px solid rgba(0,255,136,0.15);
  border-radius:14px 14px 14px 4px;
  padding:0.6rem 0.8rem; max-width:88%;
  font-size:0.82rem; line-height:1.6; color:#e8eaf6;
}}
.cs-usr {{
  align-self:flex-end;
  background:linear-gradient(135deg,#00ff88,#00cc6a);
  border-radius:14px 14px 4px 14px;
  padding:0.6rem 0.8rem; max-width:82%;
  font-size:0.82rem; line-height:1.6; color:#0a0f1e; font-weight:600;
}}
.cs-lbl {{
  font-size:0.6rem; font-weight:700; letter-spacing:0.07em;
  text-transform:uppercase; margin-bottom:0.2rem; opacity:0.65;
}}
.cs-typing {{
  align-self:flex-start;
  background:#111c35; border:1px solid rgba(0,255,136,0.15);
  border-radius:14px 14px 14px 4px;
  padding:0.65rem 0.9rem; display:flex; gap:5px; align-items:center;
}}
.cs-dot {{
  width:7px; height:7px; background:#00ff88; border-radius:50%;
  animation:csDot 1.2s infinite;
}}
.cs-dot:nth-child(2) {{ animation-delay:.2s; }}
.cs-dot:nth-child(3) {{ animation-delay:.4s; }}
@keyframes csDot {{
  0%,80%,100% {{ transform:scale(.6); opacity:.4; }}
  40%          {{ transform:scale(1); opacity:1; }}
}}
#cs-sugg {{ padding:0 0.9rem 0.5rem; display:flex; flex-direction:column; gap:0.35rem; }}
.cs-sugg-chip {{
  background:#0a1220; border:1px solid rgba(0,255,136,0.1);
  border-radius:8px; padding:0.4rem 0.7rem;
  font-size:0.76rem; color:#c8cfe8; cursor:pointer;
  transition:border-color .18s,background .18s;
}}
.cs-sugg-chip:hover {{ border-color:rgba(0,255,136,.35); background:rgba(0,255,136,.05); }}
.cs-hindi-bar {{
  padding:0.35rem 0.9rem; display:flex; align-items:center; gap:0.5rem;
  background:#0a0f1e; border-top:1px solid rgba(255,255,255,.04); flex-shrink:0;
}}
.cs-hindi-lbl {{ font-size:0.7rem; color:#7888aa; }}
.cs-toggle {{
  width:32px; height:17px; background:#162040; border-radius:10px;
  position:relative; cursor:pointer; border:none; transition:background .2s; flex-shrink:0;
}}
.cs-toggle.on {{ background:#00cc6a; }}
.cs-toggle::after {{
  content:''; position:absolute; top:2px; left:2px;
  width:13px; height:13px; background:white; border-radius:50%; transition:left .2s;
}}
.cs-toggle.on::after {{ left:17px; }}
.cs-input-row {{
  padding:0.65rem; border-top:1px solid rgba(255,255,255,.06);
  display:flex; gap:0.45rem; flex-shrink:0; background:#0a0f1e;
}}
#cs-input {{
  flex:1; background:#111c35; border:1px solid rgba(0,255,136,.2);
  border-radius:10px; color:#e8eaf6; font-family:'Inter',sans-serif;
  font-size:0.83rem; padding:0.5rem 0.8rem; outline:none; transition:border-color .18s;
}}
#cs-input:focus {{ border-color:#00ff88; }}
#cs-input::placeholder {{ color:#7888aa; }}
#cs-send {{
  background:linear-gradient(135deg,#00ff88,#00cc6a); border:none; border-radius:10px;
  color:#0a0f1e; font-weight:700; font-size:1rem; width:38px; cursor:pointer;
  transition:transform .18s,box-shadow .18s; flex-shrink:0;
}}
#cs-send:hover {{ transform:scale(1.08); box-shadow:0 4px 14px rgba(0,255,136,.4); }}
</style>

<!-- FAB -->
<button id="cs-fab" onclick="csToggle()" title="Ask Contract Shield AI">
  🤖
  <div class="cs-pulse"></div>
</button>

<!-- Chat panel -->
<div id="cs-panel">
  <div class="cs-ph">
    <div class="cs-ph-info">
      <div class="cs-ph-icon">🤖</div>
      <div>
        <div class="cs-ph-title">Contract Shield AI</div>
        <div class="cs-ph-sub">Llama 3 · {"Contract analyzed ✅" if _widget_analyzed else "Analyze a contract first"}</div>
      </div>
    </div>
    <button class="cs-close" onclick="csToggle()">✕</button>
  </div>

  <div id="cs-msgs">
    <div class="cs-bot">
      <div class="cs-lbl" style="color:#00ff88;">Contract Shield AI</div>
      {_greeting}
    </div>
  </div>

  <div id="cs-sugg">
    <div class="cs-sugg-chip" onclick="csAsk(this)">💬 What's the most dangerous clause here?</div>
    <div class="cs-sugg-chip" onclick="csAsk(this)">💬 Can my employer deduct salary without consent?</div>
    <div class="cs-sugg-chip" onclick="csAsk(this)">💬 Is this penalty clause legal in India?</div>
  </div>

  <div class="cs-hindi-bar">
    <span class="cs-hindi-lbl">🇮🇳 Hindi mode</span>
    <button class="cs-toggle" id="cs-htoggle" onclick="csToggleHindi()"></button>
    <span class="cs-hindi-lbl" id="cs-hstatus">off</span>
  </div>

  <div class="cs-input-row">
    <input id="cs-input" type="text" placeholder="Ask about your contract…"
           onkeydown="if(event.key==='Enter')csSend()"/>
    <button id="cs-send" onclick="csSend()">➤</button>
  </div>
</div>

<script>
(function(){{
  const API_KEY    = {repr(_widget_key)};
  const SYS_PROMPT = {repr(_system_prompt)};
  let panelOpen = false, hindiMode = false, history = [];

  window.csToggle = function() {{
    panelOpen = !panelOpen;
    document.getElementById('cs-panel').classList.toggle('cs-open', panelOpen);
    if (panelOpen) setTimeout(() => document.getElementById('cs-input').focus(), 300);
  }};

  window.csToggleHindi = function() {{
    hindiMode = !hindiMode;
    document.getElementById('cs-htoggle').classList.toggle('on', hindiMode);
    document.getElementById('cs-hstatus').textContent = hindiMode ? 'on' : 'off';
  }};

  window.csAsk = function(el) {{
    const txt = el.textContent.replace(/^💬\s*/, '').trim();
    document.getElementById('cs-input').value = txt;
    document.getElementById('cs-sugg').style.display = 'none';
    csSend();
  }};

  function addBubble(cls, html, labelColor) {{
    const wrap = document.getElementById('cs-msgs');
    const d = document.createElement('div');
    d.className = cls;
    const lbl = document.createElement('div');
    lbl.className = 'cs-lbl';
    lbl.style.color = labelColor;
    lbl.textContent = cls === 'cs-usr' ? 'You' : 'Contract Shield AI';
    const body = document.createElement('div');
    body.innerHTML = html.replace(/\n/g, '<br>');
    d.appendChild(lbl); d.appendChild(body);
    wrap.appendChild(d);
    wrap.scrollTop = wrap.scrollHeight;
    document.getElementById('cs-sugg').style.display = 'none';
    return d;
  }}

  function showTyping() {{
    const wrap = document.getElementById('cs-msgs');
    const d = document.createElement('div');
    d.className = 'cs-typing'; d.id = 'cs-typing';
    d.innerHTML = '<div class="cs-dot"></div><div class="cs-dot"></div><div class="cs-dot"></div>';
    wrap.appendChild(d); wrap.scrollTop = wrap.scrollHeight;
  }}
  function hideTyping() {{ const el = document.getElementById('cs-typing'); if(el) el.remove(); }}

  async function translate(text, target) {{
    try {{
      const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=${{target}}&dt=t&q=${{encodeURIComponent(text)}}`;
      const d = await (await fetch(url)).json();
      return d[0].map(x=>x[0]).join('');
    }} catch(e) {{ return text; }}
  }}

  window.csSend = async function() {{
    if (!API_KEY) {{
      addBubble('cs-bot', '⚠️ No Groq API key found. Add it to your <code>.env</code> file and restart.', '#ff4444');
      return;
    }}
    const inp = document.getElementById('cs-input');
    let txt = inp.value.trim(); if (!txt) return; inp.value = '';
    let displayTxt = txt, apiTxt = txt;
    if (hindiMode) apiTxt = await translate(txt, 'en');
    addBubble('cs-usr', displayTxt, 'rgba(10,15,30,0.55)');
    history.push({{role:'user', content:apiTxt}});
    showTyping();
    try {{
      const resp = await fetch('https://api.groq.com/openai/v1/chat/completions', {{
        method:'POST',
        headers:{{'Authorization':`Bearer ${{API_KEY}}`,'Content-Type':'application/json'}},
        body: JSON.stringify({{model:'llama3-8b-8192', temperature:0.55, max_tokens:512,
          messages:[{{role:'system',content:SYS_PROMPT}},...history.slice(-12)]}})
      }});
      const data = await resp.json();
      if (data.error) throw new Error(data.error.message);
      let bot = data.choices[0].message.content.trim();
      history.push({{role:'assistant', content:bot}});
      if (hindiMode) bot = await translate(bot, 'hi');
      hideTyping();
      addBubble('cs-bot', bot, '#00ff88');
    }} catch(e) {{
      hideTyping();
      addBubble('cs-bot', `⚠️ Error: ${{e.message}}`, '#ff4444');
    }}
  }};
}})();
</script>
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
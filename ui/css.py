"""Contract Shield v4.0 — All CSS as Python constants."""

GLOBAL_CSS = """
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap');

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
    --purple:    #a29bfe;
    --cyan:      #00cec9;
    --text:      #e8eaf6;
    --muted:     #7888aa;
    --border:    rgba(255,255,255,0.07);
    --glow-g:    0 0 24px rgba(0,255,136,0.25);
    --glow-r:    0 0 24px rgba(255,68,68,0.25);
    --radius:    14px;
    --radius-sm: 10px;
    --font:      'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    --mono:      'JetBrains Mono', 'Fira Code', monospace;
}

/* ── Base reset ── */
html, body, [data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    background-color: var(--navy) !important;
    color: var(--text) !important;
    font-family: var(--font) !important;
}
[data-testid="stHeader"] { background: transparent !important; }

/* ── Sticky top bar ── */
[data-testid="stHeader"]::after {
    content: '';
    display: block;
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 56px;
    background: rgba(10,15,30,0.9);
    backdrop-filter: blur(16px) saturate(180%);
    border-bottom: 1px solid var(--border);
    z-index: 999;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1529 0%, #0a1220 100%) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stRadio label {
    color: var(--muted) !important; font-size: 0.75rem !important;
    letter-spacing: 0.07em !important; text-transform: uppercase !important;
}
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] .stRadio > div {
    background: var(--navy-4) !important; border-radius: 8px !important;
    border: 1px solid var(--border) !important;
}

/* ── Text area ── */
textarea {
    background: var(--navy-3) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
    font-family: var(--mono) !important;
    font-size: 0.88rem !important;
    line-height: 1.7 !important;
    transition: border-color 0.25s, box-shadow 0.25s !important;
}
textarea:focus {
    border-color: var(--green) !important;
    box-shadow: 0 0 0 2px rgba(0,255,136,0.15), var(--glow-g) !important;
    outline: none !important;
}

/* ── Primary button ── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--green), #00cc6a) !important;
    color: #0a0f1e !important;
    font-weight: 800 !important;
    font-size: 0.95rem !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    padding: 0.72rem 1.5rem !important;
    transition: all 0.22s ease !important;
    box-shadow: 0 4px 20px rgba(0,255,136,0.3) !important;
    letter-spacing: 0.01em !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(0,255,136,0.45) !important;
}
.stButton > button[kind="primary"]:active {
    transform: translateY(0) !important;
}

/* ── Secondary button ── */
.stButton > button:not([kind="primary"]) {
    background: var(--navy-4) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}
.stButton > button:not([kind="primary"]):hover {
    border-color: var(--green) !important;
    color: var(--green) !important;
    background: rgba(0,255,136,0.04) !important;
}

/* ── Download button ── */
.stDownloadButton > button {
    background: var(--navy-4) !important;
    color: var(--green) !important;
    border: 1px solid rgba(0,255,136,0.3) !important;
    border-radius: var(--radius-sm) !important;
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
    border-radius: var(--radius-sm) !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    color: var(--text) !important;
    transition: background 0.2s, border-color 0.2s !important;
}
.streamlit-expanderHeader:hover {
    background: var(--navy-4) !important;
    border-color: rgba(0,255,136,0.15) !important;
}
.streamlit-expanderContent {
    background: var(--navy-3) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
    border-radius: 0 0 var(--radius-sm) var(--radius-sm) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: var(--navy-3);
    border-radius: 12px;
    padding: 4px;
    border: 1px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    color: var(--muted) !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 0.5rem 1rem !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(0,255,136,0.1) !important;
    color: var(--green) !important;
    border-bottom: none !important;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: var(--navy-3) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    padding: 0.8rem 1rem !important;
}
[data-testid="stChatInput"] > div {
    background: var(--navy-3) !important;
    border: 1px solid rgba(0,255,136,0.2) !important;
    border-radius: 12px !important;
}
[data-testid="stChatInput"] input {
    color: var(--text) !important;
}

/* ── Info / success / warning boxes ── */
.stAlert { border-radius: var(--radius-sm) !important; border: 1px solid var(--border) !important; }

/* ── Code blocks ── */
.stCodeBlock, code {
    background: #060b18 !important;
    border-radius: 8px !important;
    border: 1px solid var(--border) !important;
    color: #a8d8a8 !important;
    font-family: var(--mono) !important;
}

/* ── Metric ── */
[data-testid="stMetric"] {
    background: var(--navy-3);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem 1.2rem;
}
[data-testid="stMetricLabel"] { color: var(--muted) !important; font-size: 0.75rem !important; letter-spacing: 0.08em; text-transform: uppercase; }
[data-testid="stMetricValue"] { font-size: 2.2rem !important; font-weight: 800 !important; color: var(--green) !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--navy-2); }
::-webkit-scrollbar-thumb { background: var(--navy-4); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: var(--green-dim); }

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    border: 2px dashed rgba(0,255,136,0.2) !important;
    border-radius: var(--radius) !important;
    background: rgba(0,255,136,0.02) !important;
    transition: border-color 0.2s, background 0.2s !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(0,255,136,0.4) !important;
    background: rgba(0,255,136,0.04) !important;
}

/* ── Animations ── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%      { opacity: 0.6; }
}
@keyframes shimmer {
    0% { background-position: -200% center; }
    100% { background-position: 200% center; }
}
.animate-in {
    animation: fadeInUp 0.5s ease-out forwards;
}

/* ── Urgency Banner ── */
.urgency-banner {
    background: linear-gradient(90deg, rgba(255,68,68,0.12), rgba(255,68,68,0.06));
    border: 1px solid rgba(255,68,68,0.3);
    border-left: 4px solid #ff4444;
    border-radius: 0 12px 12px 0;
    padding: 1rem 1.4rem;
    margin: 1rem 0;
    animation: pulse 2s infinite;
}

/* ── Category progress bars ── */
.cat-progress-track {
    background: var(--navy-4);
    border-radius: 6px;
    height: 8px;
    overflow: hidden;
}
.cat-progress-fill {
    height: 100%;
    border-radius: 6px;
    transition: width 0.8s cubic-bezier(0.25, 1, 0.5, 1);
}

/* ── Risk clause card ── */
.risk-card {
    background: var(--navy-3);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    overflow: hidden;
    margin-bottom: 1rem;
    transition: border-color 0.2s, transform 0.2s;
}
.risk-card:hover {
    border-color: rgba(255,255,255,0.12);
    transform: translateY(-1px);
}
.risk-card-header {
    padding: 0.8rem 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.8rem;
    flex-wrap: wrap;
}
.risk-badge {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    padding: 0.18rem 0.6rem;
    border-radius: 20px;
    border: 1px solid;
    text-transform: uppercase;
}

/* ── Chatbot suggestions ── */
.chat-chip {
    display: inline-block;
    background: rgba(0,255,136,0.06);
    border: 1px solid rgba(0,255,136,0.15);
    border-radius: 20px;
    padding: 0.4rem 0.9rem;
    font-size: 0.78rem;
    color: var(--text);
    cursor: pointer;
    transition: all 0.18s;
    margin: 0.2rem;
}
.chat-chip:hover {
    background: rgba(0,255,136,0.12);
    border-color: var(--green);
    color: var(--green);
}

/* ── Contract type cards ── */
.type-card {
    background: var(--navy-3);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem 1.2rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.22s;
}
.type-card:hover {
    border-color: rgba(0,255,136,0.3);
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.3);
}
.type-card.selected {
    border-color: var(--green);
    box-shadow: 0 0 0 1px var(--green), 0 4px 20px rgba(0,255,136,0.15);
}
</style>
"""

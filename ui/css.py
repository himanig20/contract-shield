"""Contract Shield v5.0 — Premium SaaS CSS."""

GLOBAL_CSS = """
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap');

/* ── Root variables: Professional Corporate Slate & Teal ── */
:root {
    --bg-main:    #ffffff;
    --bg-secondary:#f8fafc;
    --bg-tertiary: #f1f5f9;
    --text-primary: #0f172a;
    --text-muted:   #64748b;
    --border:       #e2e8f0;
    
    --brand-primary: #0f4c81; /* Dark corporate blue */
    --brand-secondary: #0d9488; /* Teal */
    --brand-accent:  #14b8a6;
    
    --status-high:  #ef4444; /* Clean Red */
    --status-med:   #f59e0b; /* Amber */
    --status-low:   #10b981; /* Emerald */
    --status-info:  #3b82f6; /* Blue */
    
    --radius:    8px;
    --radius-sm: 6px;
    
    --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
    --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
    --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
    
    --font:      'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    --mono:      'JetBrains Mono', 'Fira Code', monospace;
}

/* ── Base reset ── */
html, body, [data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    background-color: var(--bg-main) !important;
    color: var(--text-primary) !important;
    font-family: var(--font) !important;
}

/* Remove default header background */
[data-testid="stHeader"] { background: transparent !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    border-right: 1px solid var(--border) !important;
}

/* Specific styling for the labels (Legal Document Type, etc) */
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stRadio label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stNumberInput label {
    font-size: 0.82rem !important;
    font-weight: 800 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.03em !important;
    margin-bottom: 0.6rem !important;
}

/* Ensure radio button options are clearly styled */
[data-testid="stSidebar"] div[role="radiogroup"] label p {
    font-weight: 500 !important;
    font-size: 0.92rem !important;
}

/* ── Text area ── */
textarea {
    background: var(--bg-main) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text-primary) !important;
    font-family: var(--mono) !important;
    font-size: 0.88rem !important;
    line-height: 1.7 !important;
    box-shadow: var(--shadow-sm) !important;
    transition: all 0.2s ease !important;
}
textarea:focus {
    border-color: var(--brand-primary) !important;
    box-shadow: 0 0 0 3px rgba(15, 76, 129, 0.15) !important;
    outline: none !important;
}

/* ── Primary button ── */
.stButton > button[kind="primary"] {
    background: var(--brand-primary) !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    border: 1px solid transparent !important;
    border-radius: var(--radius) !important;
    padding: 0.6rem 1.2rem !important;
    transition: all 0.2s ease !important;
    box-shadow: var(--shadow-sm) !important;
}
.stButton > button[kind="primary"]:hover {
    background: #0c3e6a !important;
    box-shadow: var(--shadow-md) !important;
}
.stButton > button[kind="primary"]:active {
    transform: scale(0.98) !important;
}

/* ── Secondary button ── */
.stButton > button:not([kind="primary"]) {
    background: var(--bg-main) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
    box-shadow: var(--shadow-sm) !important;
}
.stButton > button:not([kind="primary"]):hover {
    border-color: var(--text-muted) !important;
    background: var(--bg-tertiary) !important;
}

/* ── Download button ── */
.stDownloadButton > button {
    background: var(--bg-main) !important;
    color: var(--brand-primary) !important;
    border: 1px solid var(--brand-primary) !important;
    border-radius: var(--radius) !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}
.stDownloadButton > button:hover {
    background: var(--brand-primary) !important;
    color: #ffffff !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: var(--bg-main) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    color: var(--text-primary) !important;
    box-shadow: var(--shadow-sm) !important;
    transition: background 0.2s !important;
}
.streamlit-expanderHeader:hover {
    background: var(--bg-tertiary) !important;
}
.streamlit-expanderContent {
    background: #ffffff !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
    border-radius: 0 0 var(--radius) var(--radius) !important;
    color: var(--text-primary) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: transparent;
    border-bottom: 2px solid var(--border);
    padding-bottom: 0;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 0 !important;
    color: #475569 !important;
    font-weight: 500 !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 1rem !important;
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
}
.stTabs [aria-selected="true"] {
    color: var(--brand-primary) !important;
    font-weight: 700 !important;
    border-bottom: 2px solid var(--brand-primary) !important;
    background: transparent !important;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: var(--bg-main) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 1rem !important;
    box-shadow: var(--shadow-sm) !important;
    color: var(--text-primary) !important;
}
[data-testid="stChatInput"] > div {
    background: var(--bg-main) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    box-shadow: var(--shadow-sm) !important;
}
[data-testid="stChatInput"] input {
    color: var(--text-primary) !important;
}

/* ── Alerts & Info ── */
.stAlert { 
    border-radius: var(--radius) !important; 
    border: 1px solid var(--border) !important; 
}

/* ── Code blocks ── */
.stCodeBlock, code, pre {
    background: #f8fafc !important;
    border-radius: var(--radius-sm) !important;
    border: 1px solid var(--border) !important;
    color: #1e293b !important;
    font-family: var(--mono) !important;
    font-size: 0.85rem !important;
    padding: 0.5rem !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    border: 2px dashed var(--border) !important;
    border-radius: var(--radius) !important;
    background: var(--bg-secondary) !important;
    transition: all 0.2s ease !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--brand-primary) !important;
    background: rgba(15, 76, 129, 0.02) !important;
}

/* ── General utility ── */
.shadow-card {
    background: var(--bg-main);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    box-shadow: var(--shadow-md);
}

.text-heading {
    font-family: var(--font);
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.02em;
}

.text-subtitle {
    font-size: 0.95rem;
    color: var(--text-muted);
    line-height: 1.6;
}

.risk-badge {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    padding: 0.25rem 0.7rem;
    border-radius: 4px;
    text-transform: uppercase;
}

.cat-progress-track {
    background: var(--bg-tertiary);
    border-radius: 4px;
    height: 6px;
    overflow: hidden;
}
.cat-progress-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 0.8s cubic-bezier(0.25, 1, 0.5, 1);
}

/* Sticky Summary Header */
.cs-sticky-summary {
    position: sticky;
    top: 55px; /* sit just below the streamlit header */
    z-index: 800;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(8px);
    border-bottom: 1px solid var(--border);
    padding: 1rem 0;
    margin-top: -1rem;
    margin-bottom: 2rem;
}
</style>
"""

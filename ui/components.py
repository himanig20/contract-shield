"""Reusable HTML/Streamlit UI component functions."""
import streamlit as st
from config import FAIRNESS_CATEGORIES
import os
import base64

def get_logo_html():
    """Helper to load user logo from assets or provide text fallback"""
    import base64
    logo_path_png = "assets/logo.png"
    logo_path_svg = "assets/logo.svg"
    
    if os.path.exists(logo_path_png):
        with open(logo_path_png, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f'<img src="data:image/png;base64,{encoded_string}" style="max-height: 48px;">'
    elif os.path.exists(logo_path_svg):
        with open(logo_path_svg, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f'<img src="data:image/svg+xml;base64,{encoded_string}" style="max-height: 48px;">'
    else:
        return '<span style="font-weight: 800; font-size: 1.5rem; color: var(--brand-primary);">Contract Shield</span>'


def hex_to_rgb(h: str) -> str:
    """Convert '#ff4444' → '255,68,68'."""
    h = h.lstrip("#")
    return ",".join(str(int(h[i:i + 2], 16)) for i in (0, 2, 4))


# ───────────────────────────────────────────────────────────────────────────────
# HERO BANNER
# ───────────────────────────────────────────────────────────────────────────────
def render_hero():
    logo_html = get_logo_html()
    st.markdown(f"""
    <div style="padding: 2rem 0 3rem; margin-bottom: 2rem; border-bottom: 1px solid var(--border);">
      <div style="margin-bottom: 1.5rem;">
          {logo_html}
      </div>
      <h1 class="text-heading" style="font-size: 2.5rem; margin: 0 0 1rem;">
        Enterprise-Grade Contract Analysis
      </h1>
      <p class="text-subtitle" style="font-size: 1.1rem; max-width: 600px; margin: 0 0 1.5rem;">
        Instantly analyze legal risks, unfair termination clauses, and predatory interest rates using advanced NLP and Machine Learning. Built to protect and empower informal workers.
      </p>
      <div style="display: flex; gap: 0.8rem; flex-wrap: wrap;">
        <span style="background: var(--bg-tertiary); color: var(--text-primary); border: 1px solid var(--border); border-radius: 4px; padding: 0.4rem 0.8rem; font-size: 0.8rem; font-weight: 600;">NLP Contextual Matching</span>
        <span style="background: var(--bg-tertiary); color: var(--text-primary); border: 1px solid var(--border); border-radius: 4px; padding: 0.4rem 0.8rem; font-size: 0.8rem; font-weight: 600;">OCR Supported</span>
        <span style="background: var(--bg-tertiary); color: var(--text-primary); border: 1px solid var(--border); border-radius: 4px; padding: 0.4rem 0.8rem; font-size: 0.8rem; font-weight: 600;">Multilingual Outputs</span>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ───────────────────────────────────────────────────────────────────────────────
# URGENCY BANNER
# ───────────────────────────────────────────────────────────────────────────────
def render_urgency_banner(findings: list):
    """Show a clean danger banner if HIGH risk clauses are found."""
    high = [f for f in findings if f["risk"] == "HIGH"]
    if not high:
        return
    first_high_clause = high[0].get("clause_id", "?")
    st.markdown(f"""
    <div style="background: #fef2f2; border-left: 4px solid var(--status-high); border-radius: var(--radius); padding: 1.2rem 1.5rem; margin: 1.5rem 0;">
      <div style="display: flex; align-items: flex-start; gap: 1rem;">
        <div style="color: var(--status-high); font-size: 1.5rem; line-height: 1;">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
        </div>
        <div>
          <div style="font-size: 1.05rem; font-weight: 700; color: #991b1b; margin-bottom: 0.3rem;">
            Critical Review Required — Clause #{first_high_clause}
          </div>
          <div style="font-size: 0.9rem; color: #7f1d1d; line-height: 1.5;">
            {len(high)} high-risk clauses were flagged that severely impact your rights. Review detailed explanations below before proceeding.
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ───────────────────────────────────────────────────────────────────────────────
# STAT CARD
# ───────────────────────────────────────────────────────────────────────────────
def render_stat_card(col, value, label, icon_svg_path, color):
    rgb = hex_to_rgb(color)
    # Replaced emojis with a clean layout relying on typography and slight background tints
    col.markdown(f"""
    <div class="shadow-card" style="text-align: left; padding: 1.2rem;">
      <div style="font-size: 0.75rem; color: var(--text-muted); font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">{label}</div>
      <div style="font-size: 2rem; font-weight: 800; color: {color}; line-height: 1;">{value}</div>
    </div>
    """, unsafe_allow_html=True)


# ───────────────────────────────────────────────────────────────────────────────
# CIRCULAR GAUGE
# ───────────────────────────────────────────────────────────────────────────────
def render_gauge(score: int) -> str:
    if score >= 80:
        color, label = "var(--status-low)", "FAIR"
    elif score >= 60:
        color, label = "var(--status-med)", "CAUTION"
    elif score >= 40:
        color, label = "var(--status-med)", "RISKY"
    else:
        color, label = "var(--status-high)", "DANGER"

    radius = 54
    circumference = 2 * 3.14159 * radius
    filled = circumference * score / 100
    gap = circumference - filled

    # Clean, modern gauge without aggressive glowing
    return f"""
    <div class="shadow-card" style="display:flex; flex-direction:column; align-items:center; justify-content:center; padding: 2rem 1rem;">
      <svg width="140" height="140" viewBox="0 0 160 160">
        <circle cx="80" cy="80" r="{radius}" fill="none"
                stroke="var(--border)" stroke-width="8"/>
        <circle cx="80" cy="80" r="{radius}" fill="none"
                stroke="{color}" stroke-width="8"
                stroke-linecap="round"
                stroke-dasharray="{filled:.1f} {gap:.1f}"
                transform="rotate(-90 80 80)"
                style="transition: stroke-dasharray 0.8s ease;"/>
        <text x="80" y="90" text-anchor="middle"
              font-family="Inter,sans-serif" font-size="32" font-weight="800"
              fill="var(--text-primary)">{score}</text>
      </svg>
      <div style="margin-top: 1rem; font-size: 0.85rem; font-weight: 600; color: {color};
                  letter-spacing: 0.05em; text-transform: uppercase;">
        Assessment: {label}
      </div>
    </div>
    """


# ───────────────────────────────────────────────────────────────────────────────
# CATEGORY FAIRNESS BARS
# ───────────────────────────────────────────────────────────────────────────────
def render_category_scores(cat_scores: dict):
    KEY_MAP = {
        "Wage": "wages",
        "Termination": "termination",
        "Privacy": "privacy",
        "Liability": "liability",
        "Renewal": "renewal",
    }

    st.markdown("""
    <div class="shadow-card">
    <div style="color: var(--text-muted); font-size: 0.8rem; font-weight: 600; 
                text-transform: uppercase; margin: 0 0 1rem; letter-spacing: 0.05em;">
        Category Breakdown
    </div>
    """, unsafe_allow_html=True)

    for util_key, fc_key in KEY_MAP.items():
        sc = cat_scores.get(util_key, 100)
        color = "var(--brand-primary)"
        if sc < 40:
            color = "var(--status-high)"
        elif sc < 65:
            color = "var(--status-med)"

        st.markdown(f"""
        <div style="margin-bottom: 1rem;">
          <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
            <span style="font-size: 0.85rem; color: var(--text-primary); font-weight: 500;">
              {util_key}
            </span>
            <span style="font-size: 0.8rem; font-weight: 600; color: {color};">{sc}/100</span>
          </div>
          <div class="cat-progress-track">
            <div class="cat-progress-fill" style="width: {sc}%; background: {color};"></div>
          </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)


# ───────────────────────────────────────────────────────────────────────────────
# RISK CLAUSE CARD
# ───────────────────────────────────────────────────────────────────────────────
RISK_COLORS = {
    "HIGH":   {"border": "var(--status-high)", "bg": "#fef2f2", "text": "var(--status-high)"},
    "MEDIUM": {"border": "var(--status-med)",  "bg": "#fffbeb", "text": "var(--status-med)"},
    "LOW":    {"border": "var(--status-low)",  "bg": "#f0fdf4", "text": "var(--status-low)"},
}

def render_clause_card(i: int, finding: dict, ai_explanation: dict | None = None):
    risk = finding["risk"]
    rc = RISK_COLORS.get(risk, RISK_COLORS["LOW"])
    confidence = int(finding.get("confidence", 0) * 100)
    clause_id = finding.get("clause_id", "?")
    clause_text = finding.get("clause_text", "")
    category = finding["category"]
    match_source = finding.get("match_source", "N/A")
    indian_law = finding.get("indian_law", "")

    what_it_means = finding["explanation"]
    why_risky = f"This clause has been flagged as a {category} risk."
    safer_alt = finding.get("suggestion", "")

    if ai_explanation:
        what_it_means = ai_explanation.get("what_it_means", what_it_means)
        why_risky = ai_explanation.get("why_risky", why_risky)
        safer_alt = ai_explanation.get("safer_alternative", safer_alt)

    # Clean Card Header
    st.markdown(f"""
    <div style="border-left: 3px solid {rc['border']};
                background: {rc['bg']};
                border-radius: 0 var(--radius) var(--radius) 0; padding: 0.8rem 1.2rem;
                display: flex; align-items: center; gap: 1rem; flex-wrap: wrap;">
      <span class="risk-badge" style="background: #ffffff; color: {rc['text']};
            border: 1px solid {rc['border']};">{risk}</span>
      <span style="font-weight: 600; font-size: 0.95rem; color: var(--text-primary);">{category}</span>
      <span style="margin-left: auto; font-size: 0.75rem; color: var(--text-muted); font-weight: 500;">
        Match Context: {match_source} · Conf {confidence}%
      </span>
    </div>
    """, unsafe_allow_html=True)

    with st.expander(f"Review finding details for clause #{clause_id}", expanded=(risk == "HIGH")):

        if clause_text:
            st.markdown("<p style='color: var(--text-muted); font-size: 0.75rem; font-weight: 600; text-transform: uppercase; margin-bottom: 0.4rem;'>Original Clause</p>", unsafe_allow_html=True)
            st.code(clause_text, language=None)

        # Content blocks
        st.markdown(f"""
        <div style="display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 1.5rem; margin-top: 1rem;">
            <div>
              <div style="font-size: 0.75rem; color: var(--text-muted); font-weight: 600; text-transform: uppercase; margin-bottom: 0.4rem;">What It Means</div>
              <div style="font-size: 0.88rem; color: var(--text-primary); line-height: 1.6;">{what_it_means}</div>
            </div>
            <div>
              <div style="font-size: 0.75rem; color: {rc['text']}; font-weight: 600; text-transform: uppercase; margin-bottom: 0.4rem;">Why It's Risky</div>
              <div style="font-size: 0.88rem; color: var(--text-primary); line-height: 1.6;">{why_risky}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if safer_alt or indian_law:
            st.markdown("<hr style='border-color: var(--border); margin: 1.5rem 0 1rem;'>", unsafe_allow_html=True)
        
        if safer_alt:
            st.markdown(f"""
            <div style="margin-bottom: 1rem;">
              <div style="font-size: 0.75rem; color: var(--brand-secondary); font-weight: 600; text-transform: uppercase; margin-bottom: 0.4rem;">Safer Alternative</div>
              <div style="font-size: 0.88rem; color: var(--text-primary); font-style: italic; background: var(--bg-secondary); padding: 0.8rem; border-radius: var(--radius-sm); border: 1px solid var(--border);">
                "{safer_alt}"
              </div>
            </div>
            """, unsafe_allow_html=True)

        if indian_law:
            st.markdown(f"""
            <div style="display: inline-flex; align-items: center; gap: 0.5rem;
                        background: var(--bg-tertiary); border: 1px solid var(--border);
                        border-radius: var(--radius-sm); padding: 0.5rem 0.8rem;">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--text-muted)" stroke-width="2"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
              <span style="font-size: 0.8rem; color: var(--text-primary); font-weight: 500;">{indian_law}</span>
            </div>
            """, unsafe_allow_html=True)


# ───────────────────────────────────────────────────────────────────────────────
# ACTION CHECKLIST
# ───────────────────────────────────────────────────────────────────────────────
def render_action_checklist(findings: list):
    high_findings = [f for f in findings if f["risk"] == "HIGH"]
    med_findings = [f for f in findings if f["risk"] == "MEDIUM"]
    high_cats = list(dict.fromkeys(f["category"] for f in high_findings))
    med_cats = list(dict.fromkeys(f["category"] for f in med_findings))
    unique_laws = list(dict.fromkeys(f.get("indian_law", "") for f in findings if f.get("indian_law")))

    actions = []
    step = 1

    if high_findings:
        actions.append((step, "<b>Do not sign this contract yet.</b> It contains high-risk clauses that could seriously harm your rights.", "var(--status-high)"))
        step += 1
        for cat in high_cats[:3]:
            actions.append((step, f"Ask the employer to <b>remove or rewrite</b> the <i>{cat}</i> clause.", "var(--status-med)"))
            step += 1

    if med_findings:
        cats = ", ".join(f"<i>{c}</i>" for c in med_cats[:3])
        actions.append((step, f"Negotiate clearer language for: {cats}.", "var(--status-med)"))
        step += 1

    if unique_laws:
        law_list = ", ".join(f"<i>{l.split(' — ')[0]}</i>" for l in unique_laws[:4])
        actions.append((step, f"Learn about your rights under: {law_list}.", "var(--brand-primary)"))
        step += 1

    if high_findings:
        actions.append((step, "Contact a free legal aid helpline — Shram Suvidha: <b>1800-11-4000</b>.", "var(--brand-secondary)"))
        step += 1

    actions.append((step, "Keep a <b>written copy</b> of every negotiated change signed by both parties.", "var(--text-muted)"))

    st.markdown("""
    <div class="shadow-card" style="margin-top: 2rem;">
        <h3 class="text-heading" style="font-size: 1.25rem; margin: 0 0 1.5rem;">Recommended Actions</h3>
    """, unsafe_allow_html=True)

    for num, text, color in actions:
        st.markdown(f"""
        <div style="display: flex; gap: 1rem; align-items: flex-start; margin-bottom: 1rem;">
          <div style="flex-shrink: 0; width: 28px; height: 28px; border-radius: 50%;
                      background: var(--bg-tertiary); border: 1px solid var(--border);
                      display: flex; align-items: center; justify-content: center;
                      font-size: 0.85rem; font-weight: 700; color: {color};">{num}</div>
          <p style="color: var(--text-primary); font-size: 0.9rem; margin: 0; line-height: 1.6; padding-top: 0.15rem;">{text}</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ───────────────────────────────────────────────────────────────────────────────
# TTS
# ───────────────────────────────────────────────────────────────────────────────
def render_tts_button(text: str, label: str = "Read Aloud", lang: str = "en-IN"):
    import streamlit.components.v1 as components
    safe = text.replace("'", "\\'").replace("\n", " ").replace('"', '\\"')[:500]
    components.html(f"""
    <button onclick="
        const u = new SpeechSynthesisUtterance('{safe}');
        u.lang = '{lang}'; u.rate = 0.9;
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(u);
    " style="background: var(--bg-main); border: 1px solid var(--border);
             border-radius: var(--radius-sm); padding: 0.4rem 0.8rem; cursor: pointer; color: var(--brand-primary);
             font-size: 0.75rem; font-weight: 600; font-family: Inter,sans-serif;
             transition: all 0.2s ease;">
        <svg style="vertical-align: middle; margin-right: 4px;" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path></svg>
        {label}
    </button>
    """, height=40)


# ───────────────────────────────────────────────────────────────────────────────
# FOOTER
# ───────────────────────────────────────────────────────────────────────────────
def render_footer():
    logo_html = get_logo_html()
    st.markdown(f"""
    <div style="
        margin-top: 4rem;
        border-top: 1px solid var(--border);
        padding: 3rem 0;
        text-align: center;
        background: var(--bg-secondary);
    ">
      <div style="margin-bottom: 1rem;">{logo_html}</div>
      <p style="color: var(--text-muted); font-size: 0.8rem; line-height: 1.8; margin: 0;">
        <b>Contract Shield v5.0</b> &nbsp;|&nbsp;
        Enterprise Contract Analysis &nbsp;|&nbsp;
        <span style="color: var(--status-high);">Not legal advice</span>
      </p>
    </div>
    """, unsafe_allow_html=True)

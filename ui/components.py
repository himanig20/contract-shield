"""Reusable HTML/Streamlit UI component functions."""
import streamlit as st
from config import THEME, FAIRNESS_CATEGORIES


def hex_to_rgb(h: str) -> str:
    """Convert '#ff4444' → '255,68,68'."""
    h = h.lstrip("#")
    return ",".join(str(int(h[i:i + 2], 16)) for i in (0, 2, 4))


# ───────────────────────────────────────────────────────────────────────────────
# HERO BANNER
# ───────────────────────────────────────────────────────────────────────────────
def render_hero():
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
      <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
                  width:400px;height:400px;
                  background:radial-gradient(circle, rgba(0,255,136,0.03) 0%, transparent 60%);
                  pointer-events:none;"></div>

      <div style="font-size:4.2rem; line-height:1; margin-bottom:0.7rem;
                  filter:drop-shadow(0 0 24px rgba(0,255,136,0.4));">🛡</div>
      <h1 style="font-family:'Inter',sans-serif; font-size:2.8rem; font-weight:900;
                 background: linear-gradient(135deg, #ffffff 0%, #00ff88 60%, #00cc6a 100%);
                 -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                 margin:0 0 0.5rem; letter-spacing:-0.04em; line-height:1.1;">
        Contract Shield
      </h1>
      <p style="font-size:1.05rem; color:#7888aa; margin:0 0 0.4rem; font-weight:400;">
        Protecting <span style="color:#00ff88; font-weight:700;">450 million</span> informal workers in India
      </p>
      <div style="display:flex; gap:0.6rem; justify-content:center; margin-top:0.8rem; flex-wrap:wrap;">
        <span style="background:rgba(0,255,136,0.08); border:1px solid rgba(0,255,136,0.2);
                     border-radius:20px; padding:0.3rem 0.8rem; font-size:0.72rem;
                     color:#00ff88; font-weight:600;">🤖 AI-Powered</span>
        <span style="background:rgba(138,173,244,0.08); border:1px solid rgba(138,173,244,0.2);
                     border-radius:20px; padding:0.3rem 0.8rem; font-size:0.72rem;
                     color:#8aadf4; font-weight:600;">🌐 8 Languages</span>
        <span style="background:rgba(255,209,102,0.08); border:1px solid rgba(255,209,102,0.2);
                     border-radius:20px; padding:0.3rem 0.8rem; font-size:0.72rem;
                     color:#ffd166; font-weight:600;">⚖️ Indian Law</span>
        <span style="background:rgba(162,155,254,0.08); border:1px solid rgba(162,155,254,0.2);
                     border-radius:20px; padding:0.3rem 0.8rem; font-size:0.72rem;
                     color:#a29bfe; font-weight:600;">🆓 Free & Open</span>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ───────────────────────────────────────────────────────────────────────────────
# URGENCY BANNER
# ───────────────────────────────────────────────────────────────────────────────
def render_urgency_banner(findings: list):
    """Show a pulsing danger banner if HIGH risk clauses are found."""
    high = [f for f in findings if f["risk"] == "HIGH"]
    if not high:
        return
    first_high_clause = high[0].get("clause_id", "?")
    st.markdown(f"""
    <div class="urgency-banner">
      <div style="display:flex; align-items:center; gap:0.8rem;">
        <span style="font-size:1.8rem;">🚨</span>
        <div>
          <div style="font-size:0.95rem; font-weight:800; color:#ff4444; margin-bottom:0.2rem;">
            ⛔ DO NOT SIGN — Review Clause #{first_high_clause} First
          </div>
          <div style="font-size:0.82rem; color:#c8cfe8; line-height:1.5;">
            This contract contains <b style="color:#ff4444;">{len(high)} high-risk</b> clause{'s' if len(high) > 1 else ''}
            that could seriously harm your rights. Scroll down for details and safer alternatives.
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ───────────────────────────────────────────────────────────────────────────────
# STAT CARD
# ───────────────────────────────────────────────────────────────────────────────
def render_stat_card(col, value, label, icon, color):
    rgb = hex_to_rgb(color)
    col.markdown(f"""
    <div style="background:rgba({rgb},0.06); border:1px solid rgba({rgb},0.2);
                border-radius:12px; padding:0.9rem 0.8rem; text-align:center;
                transition: transform 0.2s, box-shadow 0.2s;"
         onmouseover="this.style.transform='translateY(-2px)';this.style.boxShadow='0 8px 24px rgba({rgb},0.15)'"
         onmouseout="this.style.transform='';this.style.boxShadow=''">
      <div style="font-size:1.2rem; margin-bottom:0.2rem;">{icon}</div>
      <div style="font-size:1.8rem; font-weight:900; color:{color}; line-height:1;">{value}</div>
      <div style="font-size:0.68rem; color:rgba({rgb},0.8); letter-spacing:0.05em;
                  text-transform:uppercase; margin-top:0.3rem;">{label}</div>
    </div>
    """, unsafe_allow_html=True)


# ───────────────────────────────────────────────────────────────────────────────
# CIRCULAR GAUGE
# ───────────────────────────────────────────────────────────────────────────────
def render_gauge(score: int) -> str:
    if score >= 80:
        color, glow, label, emoji = "#00ff88", "rgba(0,255,136,0.35)", "FAIR", "✅"
    elif score >= 60:
        color, glow, label, emoji = "#ffd166", "rgba(255,209,102,0.35)", "CAUTION", "⚠️"
    elif score >= 40:
        color, glow, label, emoji = "#ff9f43", "rgba(255,159,67,0.35)", "RISKY", "🟠"
    else:
        color, glow, label, emoji = "#ff4444", "rgba(255,68,68,0.35)", "DANGER", "🔴"

    radius = 54
    circumference = 2 * 3.14159 * radius
    filled = circumference * score / 100
    gap = circumference - filled

    return f"""
    <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; padding:1rem;">
      <svg width="160" height="160" viewBox="0 0 160 160" style="filter:drop-shadow(0 0 16px {glow});">
        <circle cx="80" cy="80" r="{radius}" fill="none"
                stroke="rgba(255,255,255,0.06)" stroke-width="12"/>
        <circle cx="80" cy="80" r="{radius}" fill="none"
                stroke="{color}" stroke-width="12"
                stroke-linecap="round"
                stroke-dasharray="{filled:.1f} {gap:.1f}"
                transform="rotate(-90 80 80)"
                style="transition: stroke-dasharray 0.8s ease;"/>
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


# ───────────────────────────────────────────────────────────────────────────────
# CATEGORY FAIRNESS BARS
# ───────────────────────────────────────────────────────────────────────────────
def render_category_scores(cat_scores: dict):
    """Display per-category fairness progress bars from a pre-computed dict."""

    # Map the keys from calculate_category_scores to the FAIRNESS_CATEGORIES keys
    KEY_MAP = {
        "Wage": "wages",
        "Termination": "termination",
        "Privacy": "privacy",
        "Liability": "liability",
        "Renewal": "renewal",
    }

    st.markdown("""
    <p style="color:#7888aa; font-size:0.72rem; letter-spacing:0.08em;
              text-transform:uppercase; margin:0 0 0.8rem;">📊 Category Breakdown</p>
    """, unsafe_allow_html=True)

    for util_key, fc_key in KEY_MAP.items():
        sc = cat_scores.get(util_key, 100)
        meta = FAIRNESS_CATEGORIES.get(fc_key, {"label": util_key, "icon": "📋", "color": "#8aadf4"})
        color = meta["color"]
        if sc < 40:
            color = "#ff4444"
        elif sc < 65:
            color = "#ffd166"
        rgb = hex_to_rgb(color)

        st.markdown(f"""
        <div style="margin-bottom:0.65rem;">
          <div style="display:flex; justify-content:space-between; margin-bottom:0.25rem;">
            <span style="font-size:0.78rem; color:#c8cfe8; font-weight:500;">
              {meta['icon']} {meta['label']}
            </span>
            <span style="font-size:0.75rem; font-weight:700; color:{color};">{sc}/100</span>
          </div>
          <div class="cat-progress-track">
            <div class="cat-progress-fill" style="width:{sc}%; background:linear-gradient(90deg, {color}, rgba({rgb},0.6));"></div>
          </div>
        </div>
        """, unsafe_allow_html=True)


# ───────────────────────────────────────────────────────────────────────────────
# RISK CLAUSE CARD  (Component 4 — 5-section format)
# ───────────────────────────────────────────────────────────────────────────────
RISK_COLORS = {
    "HIGH":   {"border": "#ff4444", "bg": "rgba(255,68,68,0.07)",   "text": "#ff4444"},
    "MEDIUM": {"border": "#ff9f43", "bg": "rgba(255,159,67,0.07)",  "text": "#ff9f43"},
    "LOW":    {"border": "#ffd166", "bg": "rgba(255,209,102,0.07)", "text": "#ffd166"},
}


def render_clause_card(i: int, finding: dict, ai_explanation: dict | None = None):
    """
    Render a single flagged clause with the 5-section format:
    1. Original Clause  2. What It Means  3. Why Risky  4. Risk Level  5. Safer Alternative
    """
    risk = finding["risk"]
    rc = RISK_COLORS.get(risk, RISK_COLORS["LOW"])
    confidence = int(finding.get("confidence", 0) * 100)
    clause_id = finding.get("clause_id", "?")
    clause_text = finding.get("clause_text", "")
    category = finding["category"]
    match_source = finding.get("match_source", "N/A")
    indian_law = finding.get("indian_law", "")

    # Fallback explanations from rules
    what_it_means = finding["explanation"]
    why_risky = f"This clause has been flagged as a {category} risk."
    safer_alt = finding.get("suggestion", "")

    # Override with AI explanations if available
    if ai_explanation:
        what_it_means = ai_explanation.get("what_it_means", what_it_means)
        why_risky = ai_explanation.get("why_risky", why_risky)
        safer_alt = ai_explanation.get("safer_alternative", safer_alt)

    # Card header (outside expander)
    st.markdown(f"""
    <div style="border-left:4px solid {rc['border']};
                background:linear-gradient(90deg, {rc['bg']} 0%, transparent 60%);
                border-radius:0 10px 10px 0; padding:0.6rem 1rem; margin-bottom:0.25rem;
                display:flex; align-items:center; gap:0.7rem; flex-wrap:wrap;">
      <span class="risk-badge" style="background:{rc['bg']}; color:{rc['text']};
            border-color:{rc['border']};">{risk}</span>
      <span style="font-weight:700; font-size:0.9rem; color:#e8eaf6;">{category}</span>
      <span style="margin-left:auto; font-size:0.7rem; color:#7888aa;">
        Clause #{clause_id} · {match_source} · {confidence}%
      </span>
    </div>
    """, unsafe_allow_html=True)

    icon = {"HIGH": "🔴", "MEDIUM": "🟠", "LOW": "🟡"}.get(risk, "⚪")
    with st.expander(f"{icon} [{risk}]  {category}  —  clause #{clause_id}", expanded=(risk == "HIGH")):

        # 1. ORIGINAL CLAUSE
        if clause_text:
            st.markdown("<p style='color:#7888aa; font-size:0.72rem; letter-spacing:0.06em; text-transform:uppercase; margin-bottom:0.3rem;'>📄 Original Clause</p>", unsafe_allow_html=True)
            st.code(clause_text, language=None)

        # 2. WHAT IT MEANS (plain language)
        st.markdown(f"""
        <div style="background:rgba(138,173,244,0.06); border-left:3px solid #8aadf4;
                    border-radius:0 8px 8px 0; padding:0.75rem 1rem; margin:0.6rem 0;">
          <span style="font-size:0.72rem; color:#8aadf4; font-weight:700;
                       letter-spacing:0.06em; text-transform:uppercase;">💬 What It Means</span><br>
          <span style="font-size:0.88rem; color:#e8eaf6; line-height:1.65;">{what_it_means}</span>
        </div>
        """, unsafe_allow_html=True)

        # 3. WHY IT'S RISKY
        st.markdown(f"""
        <div style="background:rgba({hex_to_rgb(rc['border'])},0.06); border-left:3px solid {rc['border']};
                    border-radius:0 8px 8px 0; padding:0.75rem 1rem; margin:0.5rem 0;">
          <span style="font-size:0.72rem; color:{rc['text']}; font-weight:700;
                       letter-spacing:0.06em; text-transform:uppercase;">⚠️ Why It's Risky</span><br>
          <span style="font-size:0.88rem; color:#c8cfe8; line-height:1.65;">{why_risky}</span>
        </div>
        """, unsafe_allow_html=True)

        # 4. SAFER ALTERNATIVE (rewrite)
        if safer_alt:
            st.markdown(f"""
            <div style="background:rgba(0,255,136,0.05); border-left:3px solid #00ff88;
                        border-radius:0 8px 8px 0; padding:0.75rem 1rem; margin:0.5rem 0;">
              <span style="font-size:0.72rem; color:#00ff88; font-weight:700;
                           letter-spacing:0.06em; text-transform:uppercase;">✅ Safer Alternative</span><br>
              <span style="font-size:0.88rem; color:#c8cfe8; line-height:1.65; font-style:italic;">
                "{safer_alt}"
              </span>
            </div>
            """, unsafe_allow_html=True)

        # 5. INDIAN LAW REFERENCE
        if indian_law:
            st.markdown(f"""
            <div style="display:inline-flex; align-items:center; gap:0.4rem;
                        background:rgba(100,149,237,0.08); border:1px solid rgba(100,149,237,0.25);
                        border-radius:8px; padding:0.45rem 0.8rem; margin:0.5rem 0 0.2rem;">
              <span style="font-size:0.85rem;">⚖️</span>
              <span style="font-size:0.76rem; color:#8aadf4; font-weight:600;
                           line-height:1.5;">{indian_law}</span>
            </div>
            """, unsafe_allow_html=True)


# ───────────────────────────────────────────────────────────────────────────────
# ACTION CHECKLIST
# ───────────────────────────────────────────────────────────────────────────────
def render_action_checklist(findings: list):
    """Dynamic 'What Should I Do?' checklist based on findings."""
    high_findings = [f for f in findings if f["risk"] == "HIGH"]
    med_findings = [f for f in findings if f["risk"] == "MEDIUM"]
    high_cats = list(dict.fromkeys(f["category"] for f in high_findings))
    med_cats = list(dict.fromkeys(f["category"] for f in med_findings))
    unique_laws = list(dict.fromkeys(f.get("indian_law", "") for f in findings if f.get("indian_law")))

    actions = []
    step = 1

    if high_findings:
        actions.append((step, "🛑 <b style='color:#ff4444;'>Do not sign this contract yet.</b> It contains high-risk clauses that could seriously harm your rights.", "#ff4444"))
        step += 1
        for cat in high_cats[:3]:
            actions.append((step, f"Ask the employer to <b>remove or rewrite</b> the <i>{cat}</i> clause.", "#ff9f43"))
            step += 1

    if med_findings:
        cats = ", ".join(f"<i>{c}</i>" for c in med_cats[:3])
        actions.append((step, f"Negotiate clearer language for: {cats}.", "#ffd166"))
        step += 1

    if unique_laws:
        law_list = ", ".join(f"<i>{l.split(' — ')[0]}</i>" for l in unique_laws[:4])
        actions.append((step, f"Learn about your rights under: {law_list}.", "#8aadf4"))
        step += 1

    if high_findings:
        actions.append((step, "Contact a <b style='color:#00ff88;'>free legal aid helpline</b> — Shram Suvidha: <b>1800-11-4000</b>.", "#00ff88"))
        step += 1

    actions.append((step, "Keep a <b>written copy</b> of every negotiated change signed by both parties.", "#7888aa"))

    st.markdown("""
    <h3 style="font-family:'Inter',sans-serif; font-size:1.2rem; font-weight:800;
               color:#e8eaf6; margin:0 0 1rem;">🎯 What Should I Do?</h3>
    """, unsafe_allow_html=True)

    for num, text, color in actions:
        rgb = hex_to_rgb(color)
        st.markdown(f"""
        <div style="display:flex; gap:0.8rem; align-items:flex-start; margin-bottom:0.65rem;">
          <div style="flex-shrink:0; width:30px; height:30px; border-radius:50%;
                      background:rgba({rgb},0.12); border:1px solid rgba({rgb},0.3);
                      display:flex; align-items:center; justify-content:center;
                      font-size:0.8rem; font-weight:800; color:{color};">{num}</div>
          <p style="color:#c8cfe8; font-size:0.86rem; margin:0; line-height:1.6; padding-top:0.15rem;">{text}</p>
        </div>
        """, unsafe_allow_html=True)


# ───────────────────────────────────────────────────────────────────────────────
# TTS — Read Aloud Button (Voice Accessibility)
# ───────────────────────────────────────────────────────────────────────────────
def render_tts_button(text: str, label: str = "🔊 Read Aloud", lang: str = "en-IN"):
    """Render a text-to-speech button using the Web Speech API."""
    import streamlit.components.v1 as components
    safe = text.replace("'", "\\'").replace("\n", " ").replace('"', '\\"')[:500]
    components.html(f"""
    <button onclick="
        const u = new SpeechSynthesisUtterance('{safe}');
        u.lang = '{lang}'; u.rate = 0.9;
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(u);
    " style="background:rgba(0,255,136,0.08); border:1px solid rgba(0,255,136,0.2);
             border-radius:8px; padding:0.35rem 0.7rem; cursor:pointer; color:#00ff88;
             font-size:0.75rem; font-weight:600; font-family:Inter,sans-serif;
             transition:all 0.18s;">
        {label}
    </button>
    """, height=40)


# ───────────────────────────────────────────────────────────────────────────────
# FOOTER
# ───────────────────────────────────────────────────────────────────────────────
def render_footer():
    st.markdown("""
    <div style="
        margin-top: 4rem;
        border-top: 1px solid rgba(255,255,255,0.07);
        padding: 2rem 0 1.5rem;
        text-align: center;
    ">
      <div style="font-size:1.8rem; margin-bottom:0.5rem;">🛡</div>
      <p style="color:#7888aa; font-size:0.78rem; line-height:1.8; margin:0;">
        <b style="color:rgba(255,255,255,0.35);">Contract Shield v4.0</b> &nbsp;·&nbsp;
        Built for social impact 🇮🇳 &nbsp;·&nbsp;
        <span style="color:rgba(255,68,68,0.7);">Not legal advice</span>
      </p>
      <p style="color:rgba(255,255,255,0.18); font-size:0.72rem; margin:0.4rem 0 0;">
        ⚠️ This tool provides automated analysis only. Always consult a qualified lawyer.
      </p>
    </div>
    """, unsafe_allow_html=True)

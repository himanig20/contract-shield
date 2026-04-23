"""
Contract Shield v4.0 — AI-Powered Contract Risk Analyzer
Main application entry point.
"""
import os
import streamlit as st
from dotenv import load_dotenv
from datetime import datetime
import urllib.parse

load_dotenv()

# ── Core imports ──────────────────────────────────────────────────────────────
from rules import analyze_contract, split_clauses
from utils import calculate_score, calculate_category_scores, get_score_label, preprocess, generate_text_report
from config import LANGUAGES, CONTRACT_TYPES, FAIRNESS_CATEGORIES, GROQ_API_KEY
from services.groq_client import explain_clause, is_available as groq_available
from services.translator import translate_text
from ui.css import GLOBAL_CSS
from ui.components import (
    render_hero, render_urgency_banner, render_stat_card,
    render_gauge, render_category_scores, render_clause_card,
    render_action_checklist, render_tts_button, render_footer,
    hex_to_rgb,
)
from ui.charts import render_risk_donut, render_radar_chart
from ui.floating_chat import inject_floating_chat
from ui.chatbot import clear_chat

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Contract Shield · AI Legal Analyzer",
    page_icon="🛡",
    layout="wide",
)

# ── Inject CSS ───────────────────────────────────────────────────────────────
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    # Logo
    st.markdown("""
    <div style="text-align:center; padding:1.2rem 0 0.8rem;">
        <div style="font-size:2.6rem; line-height:1; filter:drop-shadow(0 0 16px rgba(0,255,136,0.4));">🛡</div>
        <div style="font-size:1.1rem; font-weight:800; color:#e8eaf6; letter-spacing:-0.02em; margin-top:0.3rem;">Contract Shield</div>
        <div style="font-size:0.65rem; color:#7888aa; margin-top:0.15rem; letter-spacing:0.06em;">AI LEGAL ANALYZER · v4.0</div>
    </div>
    <hr style="border-color:rgba(255,255,255,0.07); margin:0.5rem 0 1.2rem;">
    """, unsafe_allow_html=True)

    # Document Type
    st.markdown("<p style='color:#7888aa; font-size:0.72rem; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:0.3rem;'>⚙️ Document Type</p>", unsafe_allow_html=True)
    doc_type = st.selectbox(
        "Document Type",
        list(CONTRACT_TYPES.keys()),
        label_visibility="collapsed",
    )

    # Language
    st.markdown("<p style='color:#7888aa; font-size:0.72rem; letter-spacing:0.08em; text-transform:uppercase; margin:1rem 0 0.3rem;'>🌐 Output Language</p>", unsafe_allow_html=True)
    lang_options = [f"{v['flag']} {k}" for k, v in LANGUAGES.items()]
    selected_lang_display = st.radio("Language", lang_options, label_visibility="collapsed")
    language = selected_lang_display.split(" ", 1)[1]
    lang_code = LANGUAGES[language]["code"]

    # AI Status
    st.markdown("""
    <hr style="border-color:rgba(255,255,255,0.07); margin:1.4rem 0 1rem;">
    <p style="color:#7888aa; font-size:0.72rem; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:0.4rem;">🤖 AI Assistant</p>
    """, unsafe_allow_html=True)

    _env_key = GROQ_API_KEY
    if _env_key and not _env_key.startswith("your_"):
        st.markdown("""
        <div style="background:rgba(0,255,136,0.07); border:1px solid rgba(0,255,136,0.2);
                    border-radius:8px; padding:0.5rem 0.8rem; font-size:0.78rem; color:#00ff88;">
          ✅ API key loaded — AI features active
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:rgba(255,159,67,0.07); border:1px solid rgba(255,159,67,0.2);
                    border-radius:8px; padding:0.5rem 0.8rem; font-size:0.78rem; color:#ff9f43;">
          ⚠️ No API key — enter one below
        </div>
        """, unsafe_allow_html=True)
        st.text_input("Groq API Key", type="password", placeholder="gsk_…",
                      label_visibility="collapsed", key="groq_api_key_input")

    # AI Toggle
    use_ai = st.checkbox("🧠 Use AI explanations", value=True, key="use_ai_toggle",
                         help="Enable LLM-powered explanations and safer rewrites")

    # Sample Contracts
    st.markdown("""
    <hr style="border-color:rgba(255,255,255,0.07); margin:1.4rem 0 1rem;">
    <p style="color:#7888aa; font-size:0.72rem; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:0.4rem;">📄 Load Sample Contract</p>
    """, unsafe_allow_html=True)

    if st.button("🏭  Labor Contract", use_container_width=True, key="s_labor"):
        st.session_state["contract_input"] = (
            "EMPLOYMENT CONTRACT\n\n"
            "1. The employee agrees to work a minimum of 10 hours per day, 6 days a week, "
            "with no additional compensation for overtime as deemed fit by management.\n\n"
            "2. The company reserves the right to terminate the employee immediately without "
            "prior notice and without payment of pending dues.\n\n"
            "3. In case of any breach, a penalty of Rs. 5000 per day shall be charged, "
            "compounded daily until the amount is recovered in full.\n\n"
            "4. The employee waives all rights to legal action against the company for any "
            "workplace injury or illness sustained during employment.\n\n"
            "5. The employer may deduct from wages any amount as determined by management "
            "at sole discretion for damages, losses, or misconduct.\n\n"
            "6. The employee shall not engage in or work for any competing business for a "
            "period of 3 years after leaving the company, across all of India."
        )
        clear_chat()
        st.rerun()

    if st.button("🏠  Rental Agreement", use_container_width=True, key="s_rental"):
        st.session_state["contract_input"] = (
            "RENTAL AGREEMENT\n\n"
            "1. The tenant shall pay rent of Rs. 8,000 per month, due on the 1st. A late fee "
            "of Rs. 500 per day shall apply for any delay.\n\n"
            "2. The landlord reserves the right to enter the premises at any time without "
            "prior notice for inspection purposes.\n\n"
            "3. The tenant must vacate the premises immediately upon landlord's request, "
            "with no notice period required.\n\n"
            "4. The security deposit of Rs. 50,000 shall be forfeited entirely if the tenant "
            "vacates before 11 months, regardless of reason.\n\n"
            "5. The landlord is not liable for any injury, damage, or loss to the tenant's "
            "property within the premises. The tenant holds harmless the landlord.\n\n"
            "6. The landlord may share personal information of the tenant with third parties "
            "including collection agencies and future landlords."
        )
        clear_chat()
        st.rerun()

    if st.button("💰  Loan Document", use_container_width=True, key="s_loan"):
        st.session_state["contract_input"] = (
            "LOAN AGREEMENT\n\n"
            "1. The borrower agrees to repay the principal amount of Rs. 50,000 with "
            "interest at 5% per day, compounded daily.\n\n"
            "2. In case of default, the lender may deduct from wages or any bank account "
            "held by the borrower the outstanding amount plus penalty.\n\n"
            "3. The borrower waives all rights to legal action against the lender in case "
            "of disputes arising from this agreement.\n\n"
            "4. The lender reserves absolute discretion to modify interest rates, repayment "
            "schedule, and penalty terms at any time without notice.\n\n"
            "5. A penalty of Rs. 1000 per day of delay in repayment shall be levied, in "
            "addition to the compounding interest.\n\n"
            "6. The borrower's personal information including Aadhaar, PAN, and contact "
            "details may be disclosed to third parties for recovery purposes."
        )
        clear_chat()
        st.rerun()

    # Session History
    if "analysis_history" not in st.session_state:
        st.session_state["analysis_history"] = []

    history = st.session_state["analysis_history"]
    if history:
        st.markdown("""
        <hr style="border-color:rgba(255,255,255,0.07); margin:1.4rem 0 1rem;">
        <p style="color:#7888aa; font-size:0.72rem; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:0.4rem;">🕒 Recent Analyses</p>
        """, unsafe_allow_html=True)
        for h in reversed(history[-3:]):
            _hc = "#ff4444" if h["score"] < 40 else "#ffd166" if h["score"] < 70 else "#00ff88"
            st.markdown(f"""
            <div style="background:#111c35; border:1px solid rgba(255,255,255,0.07);
                        border-radius:8px; padding:0.55rem 0.8rem; margin-bottom:0.4rem;">
              <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:0.78rem; color:#c8cfe8; font-weight:600;">{h['doc_type']}</span>
                <span style="font-size:0.78rem; color:{_hc}; font-weight:800;">{h['score']}/100</span>
              </div>
              <div style="font-size:0.66rem; color:#7888aa; margin-top:0.15rem;">
                {h['timestamp']} · {h['n_findings']} issues · {h['n_high']} HIGH
              </div>
            </div>
            """, unsafe_allow_html=True)

    # How to use
    st.markdown("""
    <hr style="border-color:rgba(255,255,255,0.07); margin:1.4rem 0 1rem;">
    <div style="background:#111c35; border-radius:10px; padding:0.9rem; border:1px solid rgba(255,255,255,0.07);">
        <p style="color:#7888aa; font-size:0.72rem; letter-spacing:0.08em; text-transform:uppercase; margin:0 0 0.6rem;">📖 How to use</p>
        <p style="font-size:0.8rem; color:#c8cfe8; margin:0; line-height:1.7;">
          1️⃣ Paste text or upload PDF<br>
          2️⃣ Click <b style="color:#00ff88;">Analyze</b><br>
          3️⃣ Review flagged clauses<br>
          4️⃣ Chat with AI for advice<br>
          5️⃣ Download report
        </p>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN CONTENT
# ══════════════════════════════════════════════════════════════════════════════

# ── Hero ──
render_hero()

# ── Contract type info ──
ct = CONTRACT_TYPES[doc_type]
st.markdown(f"""
<div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:1.2rem;
            background:rgba({hex_to_rgb(ct['color'])},0.06);
            border:1px solid rgba({hex_to_rgb(ct['color'])},0.15);
            border-radius:10px; padding:0.6rem 1rem;">
  <span style="font-size:1.4rem;">{ct['icon']}</span>
  <div>
    <span style="font-size:0.88rem; font-weight:700; color:{ct['color']};">{doc_type}</span>
    <span style="font-size:0.78rem; color:#7888aa; margin-left:0.5rem;">{ct['desc']}</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Input section (tabbed) ────────────────────────────────────────────────────
import pdfplumber
import pytesseract
from PIL import Image

tab_paste, tab_pdf, tab_img = st.tabs(["📋  Paste Text", "📄  Upload PDF", "🖼️  Upload Image (OCR)"])

with tab_paste:
    st.markdown("<p style='font-size:0.75rem; color:#7888aa; letter-spacing:0.07em; text-transform:uppercase; margin-bottom:0.3rem;'>📋 Paste your contract text</p>", unsafe_allow_html=True)
    contract_text = st.text_area(
        "Contract text", height=220,
        placeholder="Paste any labor contract, rental agreement, or loan document…",
        key="contract_input", label_visibility="collapsed",
    )

with tab_pdf:
    st.markdown("<p style='font-size:0.75rem; color:#7888aa; letter-spacing:0.07em; text-transform:uppercase; margin-bottom:0.3rem;'>📄 Upload a contract PDF</p>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"], label_visibility="collapsed", key="pdf_upload")

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
                            border-radius:10px; padding:0.7rem 1rem; font-size:0.83rem; color:#00ff88;">
                  ✅ Extracted <b>{len(pdf_pages)} page{'s' if len(pdf_pages) != 1 else ''}</b>
                  · {len(contract_text):,} characters
                </div>
                """, unsafe_allow_html=True)
                with st.expander("👁 Preview extracted text"):
                    st.text(contract_text[:3000] + ("\n\n… [truncated]" if len(contract_text) > 3000 else ""))
            else:
                contract_text = ""
                st.error("📛 No readable text found. This may be a scanned PDF — try the Upload Image tab or paste text manually.")
        except Exception as e:
            contract_text = ""
            st.error(f"⚠️ Error reading PDF: {e}")

with tab_img:
    st.markdown("<p style='font-size:0.75rem; color:#7888aa; letter-spacing:0.07em; text-transform:uppercase; margin-bottom:0.3rem;'>🖼️ Upload an Image of the Contract</p>", unsafe_allow_html=True)
    uploaded_image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"], label_visibility="collapsed", key="img_upload")

    if uploaded_image is not None:
        try:
            with st.spinner("🔍 Running OCR to extract text from image..."):
                image = Image.open(uploaded_image)
                extracted_text = pytesseract.image_to_string(image)
                
            if extracted_text.strip():
                contract_text = extracted_text
                st.markdown(f"""
                <div style="background:rgba(0,255,136,0.06); border:1px solid rgba(0,255,136,0.2);
                            border-radius:10px; padding:0.7rem 1rem; font-size:0.83rem; color:#00ff88;">
                  ✅ Successfully extracted {len(contract_text):,} characters via OCR
                </div>
                """, unsafe_allow_html=True)
                with st.expander("👁 Preview extracted text"):
                    st.text(contract_text[:3000] + ("\n\n… [truncated]" if len(contract_text) > 3000 else ""))
            else:
                contract_text = ""
                st.error("📛 OCR couldn't find any readable text in this image. Try uploading a clearer photo.")
        except Exception as e:
            contract_text = ""
            st.error(f"⚠️ Error processing image for OCR: {e}")

# ── Action buttons ────────────────────────────────────────────────────────────
col1, col2 = st.columns([3, 1])
with col1:
    analyze_btn = st.button("🔍  Analyze Contract", type="primary", use_container_width=True)
with col2:
    clear_btn = st.button("🗑  Clear", use_container_width=True)

if clear_btn:
    st.session_state["contract_input"] = ""
    st.session_state["pdf_upload"] = None
    st.session_state["cs_analyzed"] = False
    clear_chat()
    st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# ANALYSIS RESULTS
# ══════════════════════════════════════════════════════════════════════════════
if analyze_btn and contract_text.strip():
    cleaned_text = preprocess(contract_text)
    findings = analyze_contract(cleaned_text)
    score = calculate_score(findings)
    label, emoji = get_score_label(score)
    total_clauses = len(split_clauses(cleaned_text))

    # Save to session state for chatbot
    _findings_summary = "\n".join(
        f"- [{f['risk']}] {f['category']}: {f['explanation'][:120]}"
        for f in findings
    ) or "No risky clauses were flagged."
    st.session_state["cs_contract_text"] = cleaned_text[:4000]
    st.session_state["cs_findings"] = _findings_summary
    st.session_state["cs_score"] = score
    st.session_state["cs_analyzed"] = True

    # Save to history
    st.session_state.setdefault("analysis_history", []).append({
        "doc_type": doc_type,
        "score": score,
        "n_findings": len(findings),
        "n_high": sum(1 for f in findings if f["risk"] == "HIGH"),
        "timestamp": datetime.now().strftime("%I:%M %p"),
    })
    st.session_state["analysis_history"] = st.session_state["analysis_history"][-3:]

    st.markdown("<hr style='border-color:rgba(255,255,255,0.07); margin:1.8rem 0;'>", unsafe_allow_html=True)

    # ── Urgency banner ──
    render_urgency_banner(findings)

    # ── Results header ──
    st.markdown("""
    <h2 style="font-family:'Inter',sans-serif; font-size:1.5rem; font-weight:800;
               color:#e8eaf6; margin:0.5rem 0 1.2rem; letter-spacing:-0.02em;">
      📊 Analysis Results
    </h2>
    """, unsafe_allow_html=True)

    high = sum(1 for f in findings if f["risk"] == "HIGH")
    medium = sum(1 for f in findings if f["risk"] == "MEDIUM")
    low = sum(1 for f in findings if f["risk"] == "LOW")

    # ── Stat cards ──
    stat_cols = st.columns(4)
    render_stat_card(stat_cols[0], total_clauses, "Clauses Scanned", "📝", "#8aadf4")
    render_stat_card(stat_cols[1], high, "High Risk", "🔴", "#ff4444")
    render_stat_card(stat_cols[2], medium, "Medium Risk", "🟠", "#ff9f43")
    render_stat_card(stat_cols[3], low, "Low Risk", "🟡", "#ffd166")

    # ── Score + Donut + Verdict ──
    score_col, chart_col, verdict_col = st.columns([1, 1, 1])

    with score_col:
        st.markdown(render_gauge(score), unsafe_allow_html=True)

    with chart_col:
        render_risk_donut(high, medium, low, len(findings))

    with verdict_col:
        full_label, _ = get_score_label(score)
        st.markdown(f"""
        <div style="background:var(--navy-3); border:1px solid rgba(255,255,255,0.07);
                    border-radius:12px; padding:1.2rem 1.4rem; margin-bottom:1rem;">
          <p style="color:#7888aa; font-size:0.72rem; letter-spacing:0.08em;
                    text-transform:uppercase; margin:0 0 0.3rem;">Verdict</p>
          <p style="font-size:1.05rem; font-weight:700; color:#e8eaf6; margin:0;">{full_label}</p>
        </div>
        """, unsafe_allow_html=True)

        if findings:
            from collections import Counter
            cat_counts = Counter(f["category"] for f in findings)
            top_cat, top_count = cat_counts.most_common(1)[0]
            st.markdown(f"""
            <div style="background:rgba(138,173,244,0.06); border:1px solid rgba(138,173,244,0.2);
                        border-radius:12px; padding:1rem 1.2rem;">
              <p style="color:#7888aa; font-size:0.72rem; letter-spacing:0.08em;
                        text-transform:uppercase; margin:0 0 0.3rem;">Most Common Issue</p>
              <p style="font-size:0.95rem; font-weight:700; color:#8aadf4; margin:0;">
                {top_cat} <span style="font-weight:400; color:#7888aa;">({top_count}×)</span>
              </p>
            </div>
            """, unsafe_allow_html=True)

    # ── Category Fairness + Radar ──
    if findings:
        st.markdown("<hr style='border-color:rgba(255,255,255,0.07); margin:1.5rem 0;'>", unsafe_allow_html=True)

        cat_col, radar_col = st.columns([1, 1])
        with cat_col:
            cat_scores = calculate_category_scores(findings)
            render_category_scores(cat_scores)
        with radar_col:
            render_radar_chart(cat_scores, FAIRNESS_CATEGORIES)

    # ── Flagged Clauses (Component 4 — 5-section format) ──
    st.markdown("<hr style='border-color:rgba(255,255,255,0.07); margin:1.5rem 0;'>", unsafe_allow_html=True)

    if findings:
        st.markdown("""
        <h2 style="font-family:'Inter',sans-serif; font-size:1.4rem; font-weight:800;
                   color:#e8eaf6; margin:0 0 1rem;">🚩 Flagged Clauses</h2>
        """, unsafe_allow_html=True)

        # Generate AI explanations if enabled
        ai_explanations = {}
        if st.session_state.get("use_ai_toggle", True) and groq_available():
            with st.spinner("🧠 Generating AI-powered explanations & safer rewrites…"):
                for idx, f in enumerate(findings):
                    ai_explanations[idx] = explain_clause(
                        clause_text=f.get("clause_text", ""),
                        rule_category=f["category"],
                        rule_explanation=f["explanation"],
                    )

        # Translate toggle
        if lang_code:
            translate_all = st.checkbox(
                f"🌐 Translate all explanations to {language}", value=False,
                key="translate_all_exp",
            )

        for i, f in enumerate(findings):
            ai_exp = ai_explanations.get(i)

            # Translate if needed
            if lang_code and st.session_state.get("translate_all_exp", False) and ai_exp:
                for key in ["what_it_means", "why_risky", "safer_alternative"]:
                    if ai_exp.get(key):
                        ai_exp[key] = translate_text(ai_exp[key], target=lang_code)

            render_clause_card(i + 1, f, ai_explanation=ai_exp)

            # TTS button
            tts_text = ai_exp.get("what_it_means", f["explanation"]) if ai_exp else f["explanation"]
            tts_lang = LANGUAGES[language]["tts"]
            render_tts_button(tts_text, label=f"🔊 Read clause {i+1}", lang=tts_lang)

        # ── Action Checklist ──
        st.markdown("<hr style='border-color:rgba(255,255,255,0.07); margin:1.5rem 0;'>", unsafe_allow_html=True)
        render_action_checklist(findings)

        # ── Download + WhatsApp ──
        st.markdown("<div style='margin-top:1.4rem;'>", unsafe_allow_html=True)
        report = generate_text_report(findings, score, doc_type)

        dl_col, wa_col = st.columns([3, 2])
        with dl_col:
            st.download_button(
                label="📥  Download Full Report (.txt)",
                data=report,
                file_name="contract_shield_report.txt",
                mime="text/plain",
                use_container_width=True,
            )
        with wa_col:
            wa_msg = (
                f"I analyzed my contract using *Contract Shield* 🛡\n\n"
                f"📊 Fairness Score: *{score}/100*\n"
                f"🚨 Found *{high} HIGH-risk* and *{len(findings)} total* flagged clauses.\n\n"
                f"Get the free tool: https://github.com/himanig20/contract-shield"
            )
            wa_url = f"https://wa.me/?text={urllib.parse.quote(wa_msg)}"
            st.markdown(f"""
            <a href="{wa_url}" target="_blank" style="text-decoration:none;">
              <div style="background:linear-gradient(135deg,#25D366,#128C7E); border-radius:10px;
                          padding:0.68rem 1rem; text-align:center; font-weight:700;
                          color:white; font-size:0.92rem; cursor:pointer;
                          box-shadow:0 4px 14px rgba(37,211,102,0.3);
                          transition:transform 0.18s, box-shadow 0.18s;">
                📱  Share on WhatsApp
              </div>
            </a>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.markdown("""
        <div style="background:rgba(0,255,136,0.06); border:1px solid rgba(0,255,136,0.25);
                    border-radius:12px; padding:1.8rem; text-align:center; margin-top:1rem;">
          <div style="font-size:3rem;">✅</div>
          <h3 style="color:#00ff88; margin:0.5rem 0 0.3rem; font-size:1.2rem;">No exploitative clauses detected</h3>
          <p style="color:#7888aa; font-size:0.88rem; margin:0;">
            The contract appears fair. Still consider having a legal professional review it.
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

# ── FLOATING CHATBOT INJECTION ──
inject_floating_chat()

# ── Footer ──
render_footer()

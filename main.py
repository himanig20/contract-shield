import streamlit as st
from rules import analyze_contract
from utils import (
    calculate_score,
    get_score_label,
    translate_text,
    preprocess,
    get_risk_color,
    generate_text_report,
)

st.set_page_config(
    page_title="Contract Shield",
    page_icon="🛡",
    layout="wide"
)

st.title("🛡 Contract Shield")
st.caption("Protecting informal workers from exploitative contracts · Not legal advice")
st.divider()

with st.sidebar:
    st.header("⚙️ Settings")
    doc_type = st.selectbox(
        "Document Type",
        ["Labor Contract", "Rental Agreement", "Loan Document", "Other"]
    )
    language = st.radio(
        "Output Language",
        ["English", "Hindi", "Marathi", "Bengali"]
    )
    st.divider()
    st.markdown("**ℹ️ How to use:**")
    st.markdown("1. Paste your contract text\n2. Click Analyze\n3. Review flagged clauses\n4. Download report")
    st.divider()
    st.caption("Built for social impact 🇮🇳")

LANG_MAP = {
    "English": None,
    "Hindi": "hi",
    "Marathi": "mr",
    "Bengali": "bn",
}

contract_text = st.text_area(
    "📋 Paste your contract text here:",
    height=250,
    placeholder="Paste any labor contract, rental agreement, or loan document here..."
)

col1, col2 = st.columns([2, 1])
with col1:
    analyze_btn = st.button("🔍 Analyze Contract", type="primary", use_container_width=True)
with col2:
    clear_btn = st.button("🗑 Clear", use_container_width=True)

if clear_btn:
    st.rerun()

with st.expander("📄 Load a sample contract for testing"):
    sample_text = """EMPLOYMENT CONTRACT

1. The employee agrees to work a minimum of 10 hours per day, 6 days a week, with no additional compensation for overtime as deemed fit by management.

2. The company reserves the right to terminate the employee immediately without prior notice and without payment of pending dues.

3. In case of any breach, a penalty of Rs. 5000 per day shall be charged, compounded daily until the amount is recovered in full.

4. The employee waives all rights to legal action against the company for any workplace injury or illness.

5. The employer may deduct from wages any amount as determined by management at sole discretion."""

    st.code(sample_text)
    st.info("👆 Copy the text above and paste it into the main text area to test!")

if analyze_btn and contract_text.strip():
    cleaned_text = preprocess(contract_text)
    findings = analyze_contract(cleaned_text)
    score = calculate_score(findings)
    label, emoji = get_score_label(score)

    st.divider()
    st.subheader("📊 Analysis Results")

    score_col, counts_col = st.columns([1, 2])

    with score_col:
        st.metric(label="Fairness Score", value=f"{score}/100")
        st.markdown(f"### {emoji} {label}")

    with counts_col:
        high = sum(1 for f in findings if f['risk'] == 'HIGH')
        medium = sum(1 for f in findings if f['risk'] == 'MEDIUM')
        low = sum(1 for f in findings if f['risk'] == 'LOW')
        st.markdown(f"🔴 **{high}** HIGH risk clauses")
        st.markdown(f"🟠 **{medium}** MEDIUM risk clauses")
        st.markdown(f"🟡 **{low}** LOW risk clauses")
        if not findings:
            st.success("✅ No exploitative clauses detected!")

    st.divider()

    if findings:
        st.subheader("🚩 Flagged Clauses")

        for i, f in enumerate(findings, 1):
            risk = f['risk']
            color = get_risk_color(risk)
            icon = {"HIGH": "🔴", "MEDIUM": "🟠", "LOW": "🟡"}.get(risk, "⚪")

            with st.expander(f"{icon} [{risk} RISK] {f['category']}", expanded=(risk == 'HIGH')):
                st.markdown(
                    f"<div style='background:{color}22; border-left: 4px solid {color}; "
                    f"padding: 10px; border-radius: 4px; margin-bottom: 10px;'>"
                    f"<b>Matched text:</b> <code>{f['matched_text']}</code></div>",
                    unsafe_allow_html=True
                )

                explanation = f['explanation']
                lang_code = LANG_MAP.get(language)

                if lang_code:
                    with st.spinner(f"Translating to {language}..."):
                        explanation = translate_text(explanation, target=lang_code)

                st.info(f"💡 **Explanation:** {explanation}")

                if language == "English":
                    if st.button(f"🌐 Translate to Hindi", key=f"translate_{i}"):
                        hindi = translate_text(f['explanation'], target='hi')
                        st.success(f"🇮🇳 **Hindi:** {hindi}")

        st.divider()
        report = generate_text_report(findings, score, doc_type)
        st.download_button(
            label="📥 Download Full Report (.txt)",
            data=report,
            file_name="contract_shield_report.txt",
            mime="text/plain"
        )

    else:
        st.success("✅ No high-risk clauses detected. The contract appears relatively fair.")
        st.info("💡 This does not mean it is perfect. Consider having a legal professional review it.")

elif analyze_btn and not contract_text.strip():
    st.warning("⚠️ Please paste some contract text before analyzing.")

st.divider()
st.caption("⚠️ Disclaimer: Contract Shield is not legal advice. Always consult a qualified lawyer. | Built for social impact 🇮🇳")
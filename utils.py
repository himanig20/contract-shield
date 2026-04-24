from deep_translator import GoogleTranslator
from functools import lru_cache


def calculate_score(findings):
    if not findings:
        return 100

    # Sort by severity so HIGH risks apply first (gets full deduction, rest decay)
    sorted_findings = sorted(
        findings,
        key=lambda f: {"HIGH": 3, "MEDIUM": 2, "LOW": 1}.get(f.get("risk", "LOW"), 0),
        reverse=True,
    )

    risk_counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    total_penalty = 0.0

    # Base penalties per tier — each subsequent finding in the same tier is worth less
    BASE = {"HIGH": 20.0, "MEDIUM": 10.0, "LOW": 4.0}
    DECAY = {"HIGH": 0.70, "MEDIUM": 0.72, "LOW": 0.75}

    for f in sorted_findings:
        risk = f.get("risk", "LOW")
        n = risk_counts[risk]                          # how many of this tier seen so far
        penalty = BASE[risk] * (DECAY[risk] ** n)      # asymptotic decay
        total_penalty += penalty
        risk_counts[risk] += 1

    score = max(0.0, 100.0 - total_penalty)

    # Enforce score bands based on highest risk present
    if risk_counts["HIGH"] >= 3:
        score = min(score, 14)   # Extreme band  (0–14)
    elif risk_counts["HIGH"] >= 1:
        score = min(score, 44)   # Serious band  (15–44)
    elif risk_counts["MEDIUM"] >= 2:
        score = min(score, 74)   # Moderate band (45–74)

    return int(round(score))


def calculate_category_scores(findings):
    """Return per-category fairness scores (0–100) for radar charts."""
    CAT_MAP = {
        "Unfair Termination": "Termination",
        "Non-Compete Clause": "Termination",
        "Unlawful Eviction": "Termination",
        "Illegal Wage Deduction": "Wage",
        "Forced Overtime": "Wage",
        "Privacy Concern": "Privacy",
        "Liability Waiver": "Liability",
        "Excessive Penalty": "Liability",
        "Predatory Interest Rate": "Liability",
    }
    cat_scores = {"Wage": 100.0, "Termination": 100.0, "Privacy": 100.0,
                  "Liability": 100.0, "Renewal": 100.0}
    counts = {k: 0 for k in cat_scores}

    for f in findings:
        cat = CAT_MAP.get(f.get("category", ""), None)
        if cat is None:
            continue
        risk = f.get("risk", "LOW")
        n = counts[cat]
        deduction = {"HIGH": 35.0, "MEDIUM": 20.0, "LOW": 8.0}.get(risk, 5.0) * (0.7 ** n)
        cat_scores[cat] = max(0.0, cat_scores[cat] - deduction)
        counts[cat] += 1

    return {k: int(round(v)) for k, v in cat_scores.items()}


def get_score_label(score):
    if score >= 75:
        return "MINOR — Generally safe to sign", "🟢"
    elif score >= 45:
        return "MODERATE — Review specific clauses carefully", "🟡"
    elif score >= 15:
        return "SERIOUS — Seek advice before signing", "🟠"
    else:
        return "EXTREME — Do NOT sign without legal help", "🔴"



@lru_cache(maxsize=256)
def _translate_cached(text, target):
    translator = GoogleTranslator(source='en', target=target)
    return translator.translate(text)


def translate_text(text, target='hi'):
    if not text:
        return ''

    try:
        return _translate_cached(text, target)
    except Exception as e:
        return f'Translation unavailable right now. Reason: {str(e)}'


def preprocess(text):
    text = text.strip()
    text = ' '.join(text.split())
    return text


def get_risk_color(risk_level):
    colors = {
        'HIGH': '#FF4B4B',
        'MEDIUM': '#FFA500',
        'LOW': '#FFD700',
    }
    return colors.get(risk_level, '#00CC00')


def _clip(text, limit=140):
    text = text.strip()
    if len(text) <= limit:
        return text
    return text[: limit - 3] + '...'


def generate_text_report(findings, score, doc_type):
    high = sum(1 for f in findings if f['risk'] == 'HIGH')
    medium = sum(1 for f in findings if f['risk'] == 'MEDIUM')
    low = sum(1 for f in findings if f['risk'] == 'LOW')

    lines = [
        "=" * 50,
        "CONTRACT SHIELD — ANALYSIS REPORT",
        "=" * 50,
        f"Document Type: {doc_type}",
        f"Fairness Score: {score}/100",
        f"Total Issues Found: {len(findings)}",
        f"High Risk: {high} | Medium Risk: {medium} | Low Risk: {low}",
        "",
        "FLAGGED CLAUSES:",
        "-" * 50,
    ]

    if not findings:
        lines.append("No risky clauses were flagged by the current rule set.")

    for i, f in enumerate(findings, 1):
        lines.append(f"\n[{i}] {f['risk']} RISK — {f['category']}")
        lines.append(f"    Clause: {f.get('clause_id', 'N/A')}")
        lines.append(f"    Confidence: {int(f.get('confidence', 0) * 100)}%")
        lines.append(f"    Match Source: {f.get('match_source', 'N/A')}")
        lines.append(f"    Clause Text: '{_clip(f.get('clause_text', ''))}'")
        lines.append(f"    Matched: '{f['matched_text']}'")
        lines.append(f"    Explanation: {f['explanation']}")
        if f.get('suggestion'):
            lines.append(f"    Suggested Fix: {f['suggestion']}")

    lines.append("\nNEXT STEPS:")
    lines.append("- Ask the other party to rewrite or remove flagged clauses.")
    lines.append("- Request written clarification for any vague discretionary terms.")
    lines.append("- Keep a signed copy of all negotiated revisions.")
    lines.append("- Seek legal review before signing if high-risk items remain.")

    lines.append("=" * 50)
    return "\n".join(lines)


def clean_text(text):
    if not text:
        return ""
    # Replace common unicode before relying on latin-1 fallback
    text = text.replace("—", "-").replace("–", "-").replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
    return text.encode('latin-1', 'replace').decode('latin-1')

def generate_pdf_report(findings, score, doc_type):
    try:
        from fpdf import FPDF
    except ImportError:
        return None

    from datetime import datetime

    high = sum(1 for f in findings if f['risk'] == 'HIGH')
    medium = sum(1 for f in findings if f['risk'] == 'MEDIUM')
    low = sum(1 for f in findings if f['risk'] == 'LOW')

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", "B", 20)
    pdf.set_text_color(15, 76, 129)
    pdf.cell(0, 15, "CONTRACT SHIELD", ln=True, align="C")
    
    pdf.set_font("helvetica", "", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, f"Legal Analysis Report - {datetime.now().strftime('%B %d, %Y')}", ln=True, align="C")
    pdf.ln(10)

    pdf.set_fill_color(248, 250, 252)
    pdf.rect(10, pdf.get_y(), 190, 45, "F")
    pdf.set_xy(15, pdf.get_y() + 5)
    
    pdf.set_font("helvetica", "B", 14)
    pdf.set_text_color(15, 76, 129)
    pdf.cell(0, 10, "EXECUTIVE SUMMARY", ln=True)
    
    pdf.set_font("helvetica", "", 11)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(80, 8, clean_text(f"Document Type: {doc_type}"))
    pdf.set_font("helvetica", "B", 11)
    pdf.cell(0, 8, f"Fairness Score: {score}/100", ln=True)
    
    pdf.set_font("helvetica", "", 11)
    label, _ = get_score_label(score)
    pdf.cell(0, 8, clean_text(f"Analysis Result: {label}"), ln=True)
    pdf.cell(0, 8, f"Issues Identified: {len(findings)} (High: {high}, Medium: {medium}, Low: {low})", ln=True)
    pdf.ln(15)

    pdf.set_font("helvetica", "B", 14)
    pdf.set_text_color(15, 76, 129)
    pdf.cell(0, 10, "DETAILED FINDINGS", ln=True)
    pdf.ln(2)

    if not findings:
        pdf.set_font("helvetica", "I", 11)
        pdf.set_text_color(50, 50, 50)
        pdf.cell(0, 10, "No major risks were detected in the scanned text.", ln=True)
    else:
        for i, f in enumerate(findings, 1):
            pdf.set_font("helvetica", "B", 11)
            if f['risk'] == 'HIGH':
                pdf.set_text_color(220, 38, 38)
            elif f['risk'] == 'MEDIUM':
                pdf.set_text_color(217, 119, 6)
            else:
                pdf.set_text_color(202, 138, 4)
            
            pdf.cell(0, 10, clean_text(f"[{i}] {f['risk']} RISK - {f['category']}"), ln=True)
            
            pdf.set_font("helvetica", "", 10)
            pdf.set_text_color(30, 30, 30)
            pdf.set_x(15)
            pdf.multi_cell(0, 6, clean_text(f"Explanation: {f['explanation']}"))
            
            if f.get('suggestion'):
                pdf.set_x(15)
                pdf.set_font("helvetica", "I", 10)
                pdf.multi_cell(0, 6, clean_text(f"Recommendation: {f['suggestion']}"))
            
            pdf.ln(4)

    pdf.ln(10)
    pdf.set_font("helvetica", "B", 12)
    pdf.set_text_color(15, 76, 129)
    pdf.cell(0, 10, "RECOMMENDED NEXT STEPS", ln=True)
    pdf.set_font("helvetica", "", 10)
    pdf.set_text_color(30, 30, 30)
    steps = [
        "1. Do not sign the document immediately.",
        "2. Discuss the flagged clauses with the other party and request modifications.",
        "3. For HIGH risk flags, consult a qualified legal professional.",
        "4. Keep all negotiations and revised drafts documented."
    ]
    for step in steps:
        pdf.set_x(15)
        pdf.cell(0, 7, clean_text(step), ln=True)

    pdf.ln(15)
    pdf.set_font("helvetica", "I", 8)
    pdf.set_text_color(150, 150, 150)
    disclaimer = "DISCLAIMER: Contract Shield is an AI-powered detection tool, not a law firm. This report does not constitute legal advice."
    pdf.multi_cell(0, 5, clean_text(disclaimer), align="C")

    # Output as string/bytes gracefully cast for Streamlit download button
    out = pdf.output()
    return bytes(out) if not isinstance(out, str) else out.encode('latin-1')
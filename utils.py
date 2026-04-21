from deep_translator import GoogleTranslator


def calculate_score(findings):
    score = 100
    weights = {'HIGH': 20, 'MEDIUM': 10, 'LOW': 5}
    for f in findings:
        score -= weights.get(f['risk'], 0)
    return max(0, score)


def get_score_label(score):
    if score >= 80:
        return "FAIR — Generally safe to sign", "🟢"
    elif score >= 60:
        return "CAUTION — Review specific clauses carefully", "🟡"
    elif score >= 40:
        return "RISKY — Seek advice before signing", "🟠"
    else:
        return "DANGER — Do NOT sign without legal help", "🔴"


def translate_text(text, target='hi'):
    try:
        translator = GoogleTranslator(source='en', target=target)
        return translator.translate(text)
    except Exception as e:
        return f'[Translation unavailable: {str(e)}]'


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


def generate_text_report(findings, score, doc_type):
    lines = [
        "=" * 50,
        "CONTRACT SHIELD — ANALYSIS REPORT",
        "=" * 50,
        f"Document Type: {doc_type}",
        f"Fairness Score: {score}/100",
        f"Total Issues Found: {len(findings)}",
        "",
        "FLAGGED CLAUSES:",
        "-" * 50,
    ]
    for i, f in enumerate(findings, 1):
        lines.append(f"\n[{i}] {f['risk']} RISK — {f['category']}")
        lines.append(f"    Matched: '{f['matched_text']}'")
        lines.append(f"    Explanation: {f['explanation']}")

    lines.append("\n" + "=" * 50)
    lines.append("DISCLAIMER: This is not legal advice.")
    lines.append("Consult a qualified lawyer for legal help.")
    lines.append("=" * 50)
    return "\n".join(lines)
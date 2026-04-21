from deep_translator import GoogleTranslator
from functools import lru_cache


def calculate_score(findings):
    if not findings:
        return 100

    score = 100
    weights = {'HIGH': 25, 'MEDIUM': 12, 'LOW': 5}
    category_counts = {}

    for f in findings:
        score -= weights.get(f['risk'], 0)
        category = f.get('category', 'Unknown')
        category_counts[category] = category_counts.get(category, 0) + 1

    repeated_penalty = sum(max(0, count - 1) * 2 for count in category_counts.values())
    diversity_penalty = min(10, len(category_counts) * 2)
    adjusted = score - repeated_penalty - diversity_penalty
    return max(0, adjusted)


def get_score_label(score):
    if score >= 80:
        return "FAIR — Generally safe to sign", "🟢"
    elif score >= 60:
        return "CAUTION — Review specific clauses carefully", "🟡"
    elif score >= 40:
        return "RISKY — Seek advice before signing", "🟠"
    else:
        return "DANGER — Do NOT sign without legal help", "🔴"


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

    lines.append("\n" + "=" * 50)
    lines.append("DISCLAIMER: This is not legal advice.")
    lines.append("Consult a qualified lawyer for legal help.")
    lines.append("=" * 50)
    return "\n".join(lines)
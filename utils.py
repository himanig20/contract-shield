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

    lines.append("\n" + "=" * 50)
    lines.append("DISCLAIMER: This is not legal advice.")
    lines.append("Consult a qualified lawyer for legal help.")
    lines.append("=" * 50)
    return "\n".join(lines)
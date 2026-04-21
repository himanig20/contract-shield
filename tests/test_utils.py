import utils


def test_calculate_score_penalizes_severity_and_repetition():
    findings = [
        {"risk": "HIGH", "category": "A"},
        {"risk": "HIGH", "category": "A"},
        {"risk": "MEDIUM", "category": "B"},
    ]

    score = utils.calculate_score(findings)

    assert 0 <= score < 100


def test_generate_text_report_contains_enriched_fields():
    findings = [
        {
            "risk": "HIGH",
            "category": "Unfair Termination",
            "matched_text": "terminate without notice",
            "explanation": "Unfair immediate termination right.",
            "suggestion": "Add a notice period.",
            "clause_id": 1,
            "clause_text": "The employee may be terminated without notice.",
            "match_source": "keyword",
            "confidence": 0.65,
        }
    ]

    report = utils.generate_text_report(findings, score=70, doc_type="Labor Contract")

    assert "Clause: 1" in report
    assert "Confidence: 65%" in report
    assert "Suggested Fix: Add a notice period." in report
    assert "NEXT STEPS:" in report


def test_translate_text_graceful_fallback(monkeypatch):
    def _raise_error(_text, _target):
        raise RuntimeError("network down")

    monkeypatch.setattr(utils, "_translate_cached", _raise_error)

    translated = utils.translate_text("hello", target="hi")

    assert translated.startswith("Translation unavailable right now")

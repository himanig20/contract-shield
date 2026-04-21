from rules import analyze_contract


def test_analyze_contract_returns_clause_level_findings():
    text = (
        "1. The employee may be terminated without notice. "
        "2. A penalty of Rs. 5000 per day applies for any breach."
    )

    findings = analyze_contract(text)

    assert len(findings) >= 2
    assert all("clause_id" in finding for finding in findings)
    assert all("clause_text" in finding for finding in findings)
    assert all(0 <= finding["confidence"] <= 1 for finding in findings)


def test_analyze_contract_detects_repeated_rule_in_multiple_clauses():
    text = (
        "1. Overtime will have no additional pay. "
        "2. Employees may also be required to do overtime without compensation."
    )

    findings = analyze_contract(text)
    overtime_findings = [f for f in findings if f["rule"] == "forced_overtime"]

    assert len(overtime_findings) >= 2


def test_analyze_contract_safe_text_has_no_findings():
    text = "Salary will be paid on time. Either party may end the contract with 30 days notice."

    findings = analyze_contract(text)

    assert findings == []

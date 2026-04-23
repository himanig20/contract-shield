import re
from services.nlp_engine import compute_similarity, load_nlp_model

RISK_RULES = {
    'termination_no_notice': {
        'keywords': ['terminate without notice', 'immediate termination',
                     'immediate dismissal', 'without prior notice',
                     'at will', 'without cause'],
        'regex': r'terminat\w+.{0,30}(without|no).{0,15}notice',
        'semantic_anchors': [
            "The company reserves the right to terminate employment immediately without prior notice.",
            "Employee may be dismissed at any time without warning or payment in lieu of notice.",
            "This contract can be terminated at will without cause."
        ],
        'risk': 'HIGH',
        'category': 'Unfair Termination',
        'explanation': 'This allows the employer to fire you at any time without warning and possibly without paying your dues. This likely violates the Industrial Disputes Act, 1947.',
        'suggestion': 'Ask for a clear notice period and guaranteed settlement of all pending dues.',
        'indian_law': 'Industrial Disputes Act, 1947 — Section 25F requires 30 days notice and compensation before retrenchment',
    },
    'predatory_interest': {
        'keywords': ['compounded daily', 'penal interest', 'per day interest',
                     'compound interest', 'compounding penalty'],
        'regex': r'(\d+)\s*%\s*per\s*(day|week)',
        'semantic_anchors': [
            "Interest of 5% per day will be charged on late payments.",
            "Penalty interest compounded daily will be levied.",
            "A late fee of 10% per week applies to the outstanding balance."
        ],
        'risk': 'HIGH',
        'category': 'Predatory Interest Rate',
        'explanation': 'This interest rate compounds daily or weekly, meaning your debt can multiply extremely fast. 3% per day = over 1000% annual interest. This may be illegal under Indian usury laws.',
        'suggestion': 'Negotiate a monthly interest cap and request a clear upper limit on total payable amount.',
        'indian_law': 'Usurious Loans Act, 1918 — Courts can reopen transactions with excessive interest rates',
    },
    'wage_deduction': {
        'keywords': ['deduct from wages', 'withhold salary', 'offset dues',
                     'recover from payment', 'forfeit payment', 'withhold up to'],
        'regex': r'(deduct|withhold|forfeit).{0,30}(wage|salary|pay|dues)',
        'semantic_anchors': [
            "The employer may deduct from wages any amount determined by management for losses.",
            "Company reserves the right to withhold salary for perceived damages.",
            "Deductions from your pay can be made automatically for any misconduct."
        ],
        'risk': 'HIGH',
        'category': 'Illegal Wage Deduction',
        'explanation': 'The employer is claiming the right to deduct money from your wages. Deductions without your written consent may be illegal under the Payment of Wages Act, 1936.',
        'suggestion': 'Request that deductions require your written consent and be limited to lawful categories.',
        'indian_law': 'Payment of Wages Act, 1936 — Section 7 restricts unauthorized deductions from wages',
    },
    'liability_waiver': {
        'keywords': ['waive all rights', 'not liable', 'no compensation',
                     'indemnify employer', 'hold harmless',
                     'waives all rights to legal action'],
        'regex': r'waiv\w+.{0,40}(right|claim|legal|compens)',
        'semantic_anchors': [
            "The employee waives all rights to legal action against the company for workplace injury.",
            "You agree to hold the landlord harmless for any injury or property damage.",
            "The company is not liable to pay any compensation for accidents during duty."
        ],
        'risk': 'HIGH',
        'category': 'Liability Waiver',
        'explanation': 'You are being asked to give up your right to claim compensation if something goes wrong including workplace injury. Such waivers are often unenforceable under Indian law.',
        'suggestion': 'Do not waive injury or compensation rights. Ask for lawful employer liability language.',
        'indian_law': "Workmen's Compensation Act, 1923 — Waivers of compensation for workplace injury are void",
    },
    'eviction_no_notice': {
        'keywords': ['vacate immediately', 'eviction without notice',
                     'lock out', 'remove possessions',
                     'vacate the premises immediately'],
        'regex': r'vacat\w+.{0,20}(immediately|without notice)',
        'semantic_anchors': [
            "The tenant must vacate the premises immediately upon landlord's request.",
            "Landlord reserves the right to evict without prior notice or warning.",
            "You must leave the property immediately and remove all belongings when asked."
        ],
        'risk': 'HIGH',
        'category': 'Unlawful Eviction',
        'explanation': 'This clause allows the landlord to evict you without proper notice. Most Indian states require 30 days written notice before eviction.',
        'suggestion': 'Ask for written notice periods and due process terms before eviction action.',
        'indian_law': 'Transfer of Property Act, 1882 — Section 106 requires 15 days notice for monthly tenancies',
    },
    'forced_overtime': {
        'keywords': ['mandatory overtime', 'required to work extra',
                     'no additional compensation', 'unpaid hours',
                     'no additional pay', 'without extra pay'],
        'regex': r'overtime.{0,40}(no|without).{0,20}(pay|compens)',
        'semantic_anchors': [
            "Employee must work mandatory overtime with no additional pay.",
            "You are required to work extra hours as needed without extra compensation.",
            "No overtime pay will be provided for working beyond 9 hours."
        ],
        'risk': 'MEDIUM',
        'category': 'Forced Overtime',
        'explanation': 'This clause requires you to work extra hours without extra pay. Under the Factories Act, overtime must be paid at double the regular rate.',
        'suggestion': 'Request overtime payment terms with clear hourly rate and legal compliance.',
        'indian_law': 'Factories Act, 1948 — Section 59 mandates overtime pay at double the ordinary rate',
    },
    'ambiguous_discretion': {
        'keywords': ['sole discretion', 'as deemed fit', 'reasonable time',
                     'as management decides', 'at the discretion of',
                     'absolute discretion'],
        'regex': r'(sole|absolute)\s+discretion',
        'semantic_anchors': [
            "The company can make changes to this contract at its sole discretion.",
            "Management reserves the absolute discretion to alter the terms.",
            "Decisions will be made as deemed fit by the employer."
        ],
        'risk': 'MEDIUM',
        'category': 'Ambiguous Term',
        'explanation': 'This phrase gives the other party unlimited power to decide without any accountability. There is no limit on what reasonable or fit means only they decide.',
        'suggestion': 'Replace vague discretion phrases with objective criteria, timelines, and review rights.',
        'indian_law': 'Indian Contract Act, 1872 — Section 29 renders vague agreements void',
    },
    'non_compete': {
        'keywords': ['not engage in', 'refrain from working', 'compete with',
                     'not work for competitor', 'exclusivity clause'],
        'regex': r'(not|refrain).{0,20}(work|employ|engag).{0,20}(compet|similar)',
        'semantic_anchors': [
            "The employee shall not engage in competing businesses for 3 years after leaving.",
            "You are forbidden to work for any similar company within India.",
            "Employee agrees not to work for any competitor globally after termination."
        ],
        'risk': 'MEDIUM',
        'category': 'Non-Compete Clause',
        'explanation': 'This restricts where you can work after leaving this job. Overly broad non-compete clauses are often unenforceable in India especially for low-wage workers.',
        'suggestion': 'Narrow any non-compete by time, geography, and role, or remove it entirely.',
        'indian_law': 'Indian Contract Act, 1872 — Section 27 declares agreements in restraint of trade void',
    },
    'penalty_clause': {
        'keywords': ['penalty of rs', 'late fee', 'surcharge',
                     'liquidated damages', 'forfeiture', 'penalty per day'],
        'regex': r'penalty.{0,30}(rs\.?|₹|\d)',
        'semantic_anchors': [
            "A penalty of Rs 5000 per day will be charged for any breach.",
            "Liquidated damages of excessive amounts will be applied.",
            "A severe late fee will be levied in addition to compounding interest."
        ],
        'risk': 'HIGH',
        'category': 'Excessive Penalty',
        'explanation': 'This document charges a penalty for breach. Ask: How much exactly? Under what conditions? Is there a maximum cap? Uncapped penalties can trap you in debt.',
        'suggestion': 'Ask for a fixed and reasonable cap on penalties and transparent trigger conditions.',
        'indian_law': 'Indian Contract Act, 1872 — Section 74 limits penalty to reasonable compensation for actual loss',
    },
    'privacy_abuse': {
        'keywords': ['share personal information', 'disclose to third parties',
                     'sell information', 'pass to agents', 'share your data'],
        'regex': r'(share|disclose|sell).{0,30}(personal|data|information)',
        'semantic_anchors': [
            "We may share your personal data with third-party collection agencies.",
            "The landlord may disclose tenant information to future landlords without consent.",
            "Your contact and identification details can be sold to affiliates."
        ],
        'risk': 'LOW',
        'category': 'Privacy Concern',
        'explanation': 'Your personal information may be shared with or sold to third parties. Ask exactly who will receive your data and for what purpose.',
        'suggestion': 'Limit data sharing to specific purposes and require prior written consent.',
        'indian_law': 'Digital Personal Data Protection Act, 2023 — Requires informed consent before processing personal data',
    },
}



def split_clauses(text):
    if not text.strip():
        return []

    # Preserve numbered clauses while also splitting sentence blocks.
    parts = re.split(r'(?=\b\d+\.\s)|(?<=[.!?])\s+(?=[A-Z])', text)
    clauses = [p.strip() for p in parts if p and p.strip()]
    if clauses:
        return clauses
    return [text.strip()]


def _estimate_confidence(has_keyword, has_regex, similarity_score):
    base_conf = max(similarity_score, 0.4)
    if has_keyword and has_regex:
        return max(base_conf, 0.95)
    if has_regex:
        return max(base_conf, 0.88)
    if similarity_score > 0.8:
        return max(base_conf, 0.92)
    if similarity_score > 0.65:
        return max(base_conf, 0.80)
    if has_keyword:
        return max(base_conf, 0.75)
    return base_conf


def analyze_contract(text):
    nlp_model = load_nlp_model()
    
    findings = []
    clauses = split_clauses(text)

    for clause_id, clause_text in enumerate(clauses, 1):
        clause_lower = clause_text.lower()
        if len(clause_lower) < 15:
            continue  # Skip extremely short fragments

        for rule_name, rule in RISK_RULES.items():
            keyword_match = ''
            regex_match = ''

            # Keyword check
            for kw in rule['keywords']:
                if kw in clause_lower:
                    keyword_match = kw
                    break

            # Regex check
            if rule.get('regex'):
                match = re.search(rule['regex'], clause_lower)
                if match:
                    regex_match = match.group(0)

            # NLP Similarity check
            similarity_score = 0.0
            if nlp_model and 'semantic_anchors' in rule: # We fall back to 0.0 if not loaded
                similarity_score = compute_similarity(clause_text, rule['semantic_anchors'], nlp_model)
                
            # If any system flags it
            is_semantic_match = similarity_score >= 0.70 # threshold
            
            if keyword_match or regex_match or is_semantic_match:
                match_sources = []
                if keyword_match: match_sources.append('keyword')
                if regex_match: match_sources.append('regex')
                if is_semantic_match: match_sources.append('semantic')
                
                match_source = '+'.join(match_sources)
                matched_text = regex_match or keyword_match or "Contextual Match (NLP)"
                
                confidence = _estimate_confidence(bool(keyword_match), bool(regex_match), similarity_score)
                findings.append({
                    'rule': rule_name,
                    'risk': rule['risk'],
                    'category': rule['category'],
                    'explanation': rule['explanation'],
                    'suggestion': rule['suggestion'],
                    'indian_law': rule.get('indian_law', ''),
                    'matched_text': matched_text,
                    'clause_id': clause_id,
                    'clause_text': clause_text,
                    'match_source': match_source,
                    'confidence': confidence,
                })

    risk_order = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}
    # Sort primarily by risk level, then by highest confidence
    findings.sort(key=lambda item: (risk_order.get(item['risk'], 3), -item['confidence'], item['clause_id']))

    return findings
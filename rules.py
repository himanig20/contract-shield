import re

RISK_RULES = {
    'termination_no_notice': {
        'keywords': ['terminate without notice', 'immediate termination',
                     'immediate dismissal', 'without prior notice',
                     'at will', 'without cause'],
        'regex': r'terminat\w+.{0,30}(without|no).{0,15}notice',
        'risk': 'HIGH',
        'category': 'Unfair Termination',
        'explanation': 'This allows the employer to fire you at any time without warning and possibly without paying your dues. This likely violates the Industrial Disputes Act, 1947.',
    },
    'predatory_interest': {
        'keywords': ['compounded daily', 'penal interest', 'per day interest',
                     'compound interest', 'compounding penalty'],
        'regex': r'(\d+)\s*%\s*per\s*(day|week)',
        'risk': 'HIGH',
        'category': 'Predatory Interest Rate',
        'explanation': 'This interest rate compounds daily or weekly, meaning your debt can multiply extremely fast. 3% per day = over 1000% annual interest. This may be illegal under Indian usury laws.',
    },
    'wage_deduction': {
        'keywords': ['deduct from wages', 'withhold salary', 'offset dues',
                     'recover from payment', 'forfeit payment', 'withhold up to'],
        'regex': r'(deduct|withhold|forfeit).{0,30}(wage|salary|pay|dues)',
        'risk': 'HIGH',
        'category': 'Illegal Wage Deduction',
        'explanation': 'The employer is claiming the right to deduct money from your wages. Deductions without your written consent may be illegal under the Payment of Wages Act, 1936.',
    },
    'liability_waiver': {
        'keywords': ['waive all rights', 'not liable', 'no compensation',
                     'indemnify employer', 'hold harmless',
                     'waives all rights to legal action'],
        'regex': r'waiv\w+.{0,40}(right|claim|legal|compens)',
        'risk': 'HIGH',
        'category': 'Liability Waiver',
        'explanation': 'You are being asked to give up your right to claim compensation if something goes wrong including workplace injury. Such waivers are often unenforceable under Indian law.',
    },
    'eviction_no_notice': {
        'keywords': ['vacate immediately', 'eviction without notice',
                     'lock out', 'remove possessions',
                     'vacate the premises immediately'],
        'regex': r'vacat\w+.{0,20}(immediately|without notice)',
        'risk': 'HIGH',
        'category': 'Unlawful Eviction',
        'explanation': 'This clause allows the landlord to evict you without proper notice. Most Indian states require 30 days written notice before eviction.',
    },
    'forced_overtime': {
        'keywords': ['mandatory overtime', 'required to work extra',
                     'no additional compensation', 'unpaid hours',
                     'no additional pay', 'without extra pay'],
        'regex': r'overtime.{0,40}(no|without).{0,20}(pay|compens)',
        'risk': 'MEDIUM',
        'category': 'Forced Overtime',
        'explanation': 'This clause requires you to work extra hours without extra pay. Under the Factories Act, overtime must be paid at double the regular rate.',
    },
    'ambiguous_discretion': {
        'keywords': ['sole discretion', 'as deemed fit', 'reasonable time',
                     'as management decides', 'at the discretion of',
                     'absolute discretion'],
        'regex': r'(sole|absolute)\s+discretion',
        'risk': 'MEDIUM',
        'category': 'Ambiguous Term',
        'explanation': 'This phrase gives the other party unlimited power to decide without any accountability. There is no limit on what reasonable or fit means only they decide.',
    },
    'non_compete': {
        'keywords': ['not engage in', 'refrain from working', 'compete with',
                     'not work for competitor', 'exclusivity clause'],
        'regex': r'(not|refrain).{0,20}(work|employ|engag).{0,20}(compet|similar)',
        'risk': 'MEDIUM',
        'category': 'Non-Compete Clause',
        'explanation': 'This restricts where you can work after leaving this job. Overly broad non-compete clauses are often unenforceable in India especially for low-wage workers.',
    },
    'penalty_clause': {
        'keywords': ['penalty of rs', 'late fee', 'surcharge',
                     'liquidated damages', 'forfeiture', 'penalty per day'],
        'regex': r'penalty.{0,30}(rs\.?|₹|\d)',
        'risk': 'HIGH',
        'category': 'Excessive Penalty',
        'explanation': 'This document charges a penalty for breach. Ask: How much exactly? Under what conditions? Is there a maximum cap? Uncapped penalties can trap you in debt.',
    },
    'privacy_abuse': {
        'keywords': ['share personal information', 'disclose to third parties',
                     'sell information', 'pass to agents', 'share your data'],
        'regex': r'(share|disclose|sell).{0,30}(personal|data|information)',
        'risk': 'LOW',
        'category': 'Privacy Concern',
        'explanation': 'Your personal information may be shared with or sold to third parties. Ask exactly who will receive your data and for what purpose.',
    },
}


def analyze_contract(text):
    text_lower = text.lower()
    findings = []

    for rule_name, rule in RISK_RULES.items():
        matched = False
        matched_text = ''

        for kw in rule['keywords']:
            if kw in text_lower:
                matched = True
                matched_text = kw
                break

        if not matched and rule.get('regex'):
            match = re.search(rule['regex'], text_lower)
            if match:
                matched = True
                matched_text = match.group(0)

        if matched:
            findings.append({
                'rule': rule_name,
                'risk': rule['risk'],
                'category': rule['category'],
                'explanation': rule['explanation'],
                'matched_text': matched_text,
            })

    return findings
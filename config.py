"""Contract Shield v4.0 — Central Configuration"""
import os
from dotenv import load_dotenv

load_dotenv()

# ── API ──────────────────────────────────────────────────────────────────────────
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "").strip()
GROQ_MODEL = "llama-3.3-70b-versatile"

# ── Language Map ─────────────────────────────────────────────────────────────────
LANGUAGES = {
    "English":  {"code": None,  "flag": "🇬🇧", "tts": "en-IN"},
    "Hindi":    {"code": "hi",  "flag": "🇮🇳", "tts": "hi-IN"},
    "Punjabi":  {"code": "pa",  "flag": "🇮🇳", "tts": "pa-IN"},
    "Tamil":    {"code": "ta",  "flag": "🇮🇳", "tts": "ta-IN"},
    "Telugu":   {"code": "te",  "flag": "🇮🇳", "tts": "te-IN"},
    "Bengali":  {"code": "bn",  "flag": "🇮🇳", "tts": "bn-IN"},
    "Marathi":  {"code": "mr",  "flag": "🇮🇳", "tts": "mr-IN"},
    "Gujarati": {"code": "gu",  "flag": "🇮🇳", "tts": "gu-IN"},
}

# ── Contract Types ───────────────────────────────────────────────────────────────
CONTRACT_TYPES = {
    "Labor Contract":     {"icon": "🏭", "color": "#ff6b6b", "desc": "Employment / job offer / appointment letter"},
    "Rental Agreement":   {"icon": "🏠", "color": "#ffd166", "desc": "House / flat / PG / commercial rent"},
    "Loan Document":      {"icon": "💰", "color": "#ff9f43", "desc": "Personal loan / microfinance / EMI"},
    "Freelance Agreement":{"icon": "💻", "color": "#a29bfe", "desc": "Consulting / gig work / project"},
    "Internship Offer":   {"icon": "🎓", "color": "#00cec9", "desc": "Stipend letter / training agreement"},
    "Other":              {"icon": "📄", "color": "#7888aa", "desc": "Any other legal document"},
}

# ── Fairness Categories ──────────────────────────────────────────────────────────
FAIRNESS_CATEGORIES = {
    "wages":       {"label": "Salary & Wages",     "icon": "💰", "color": "#00ff88"},
    "termination": {"label": "Termination Rights",  "icon": "🚪", "color": "#ff6b6b"},
    "privacy":     {"label": "Privacy Protection",  "icon": "🔒", "color": "#a29bfe"},
    "liability":   {"label": "Liability Balance",   "icon": "⚖️",  "color": "#ffd166"},
    "debt":        {"label": "Debt Safety",         "icon": "📉", "color": "#ff9f43"},
    "renewal":     {"label": "Lock-in & Renewal",   "icon": "🔄", "color": "#00cec9"},
    "transparency":{"label": "Transparency",        "icon": "👁",  "color": "#8aadf4"},
}

# ── Theme Colors ─────────────────────────────────────────────────────────────────
THEME = {
    "navy":      "#0a0f1e",
    "navy_2":    "#0d1529",
    "navy_3":    "#111c35",
    "navy_4":    "#162040",
    "green":     "#00ff88",
    "green_dim": "#00cc6a",
    "red":       "#ff4444",
    "yellow":    "#ffd166",
    "orange":    "#ff9f43",
    "text":      "#e8eaf6",
    "muted":     "#7888aa",
}

# ── Legal Glossary (Explain Like I'm 18) ─────────────────────────────────────────
LEGAL_GLOSSARY = {
    "indemnity": "You may have to pay if something goes wrong, even if it wasn't your fault.",
    "arbitration": "If there's a dispute, you can't go to court — you must use a private judge chosen by the company.",
    "force majeure": "Events like natural disasters or pandemics that excuse the other party from their obligations.",
    "non-compete": "You can't work for a similar company for some time after leaving this job.",
    "liquidated damages": "A pre-decided penalty amount you must pay if you break the contract.",
    "waiver": "You're giving up a legal right — once waived, you can't claim it later.",
    "lien": "The lender can hold your property or assets until you repay your debt.",
    "surety": "Someone else (guarantor) promises to pay your debt if you can't.",
    "jurisdiction": "Which court or city's laws apply if there's a legal dispute.",
    "novation": "Replacing the original contract or party with a new one.",
    "severability": "If one clause is illegal, the rest of the contract still applies.",
    "tenure": "How long the contract lasts — could be months, years, or indefinite.",
    "encumbrance": "A restriction on how you can use your property (like a mortgage or lien).",
    "sublet": "Renting out the property you're renting to someone else.",
    "escrow": "Money held by a third party until certain conditions are met.",
}

"""Groq API wrapper — handles all LLM calls."""
import json
import streamlit as st
from config import GROQ_API_KEY, GROQ_MODEL

try:
    from groq import Groq
    _GROQ_OK = True
except ImportError:
    _GROQ_OK = False


def _get_key():
    """Return the best available API key."""
    key = GROQ_API_KEY
    if not key or key.startswith("your_"):
        key = st.session_state.get("groq_api_key_input", "").strip()
    return key if key and not key.startswith("your_") else ""


def _client():
    key = _get_key()
    if not key or not _GROQ_OK:
        return None
    return Groq(api_key=key)


def chat_completion(messages: list, temperature=0.5, max_tokens=800) -> str | None:
    """Send messages to Groq and return the assistant response text."""
    c = _client()
    if not c:
        return None
    try:
        resp = c.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"[API Error] {e}"


def explain_clause(clause_text: str, rule_category: str, rule_explanation: str) -> dict:
    """
    Use LLM to generate human-friendly explanation + safer rewrite for a clause.
    Returns dict with keys: what_it_means, why_risky, safer_alternative
    """
    prompt = f"""You are a legal-language simplifier for ordinary workers in India.

Given this contract clause, explain it in simple everyday language.

CLAUSE: "{clause_text}"

DETECTED ISSUE: {rule_category}
BASIC EXPLANATION: {rule_explanation}

Respond in this EXACT JSON format only — no markdown, no extra text:
{{
  "what_it_means": "One sentence explaining what this clause means in very simple language, as if explaining to an 18-year-old.",
  "why_risky": "One sentence explaining why this is dangerous for the worker/tenant/borrower.",
  "safer_alternative": "Rewrite the clause fairly so both parties are protected. Keep it short (1-2 sentences)."
}}"""

    raw = chat_completion(
        [{"role": "system", "content": "You output valid JSON only. No markdown."}, 
         {"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=400,
    )
    if not raw or raw.startswith("[API Error]"):
        return {
            "what_it_means": rule_explanation,
            "why_risky": f"This clause has been flagged as {rule_category}.",
            "safer_alternative": "",
        }
    try:
        # Strip potential markdown code fences
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[1]
            cleaned = cleaned.rsplit("```", 1)[0]
        return json.loads(cleaned)
    except (json.JSONDecodeError, IndexError):
        return {
            "what_it_means": rule_explanation,
            "why_risky": f"This clause has been flagged as {rule_category}.",
            "safer_alternative": "",
        }


def chat_about_contract(user_message: str, contract_context: str, findings_summary: str,
                         score: int, chat_history: list, language: str = "English") -> str:
    """Main chatbot function — contract-aware legal assistant."""
    lang_instruction = ""
    if language != "English":
        lang_instruction = f"\n\nIMPORTANT: The user is communicating in {language}. Reply in {language} language."

    system_prompt = f"""You are Contract Shield AI — a calm, clear, and supportive legal assistant helping ordinary people in India understand their contracts.

You have analyzed this contract and found:
{findings_summary}

Overall Fairness Score: {score}/100

CONTRACT TEXT:
{contract_context[:3000]}

INSTRUCTIONS:
- Explain legal terms in simple, everyday language
- Always reference relevant Indian labor laws when applicable
- If asked, generate polite negotiation responses the user can copy
- Suggest what to ask their employer/landlord/lender
- Never guarantee legal outcomes — always add a brief disclaimer
- Be warm and supportive, not robotic
- Keep responses concise (3-5 sentences unless asked for detail){lang_instruction}

DISCLAIMER to include at end of substantive answers:
"⚖️ This is educational guidance, not legal advice. Consult a lawyer for your specific situation."
"""

    messages = [{"role": "system", "content": system_prompt}]
    # Add recent chat history (keep last 10 exchanges)
    for msg in chat_history[-20:]:
        messages.append(msg)
    messages.append({"role": "user", "content": user_message})

    result = chat_completion(messages, temperature=0.55, max_tokens=600)
    return result or "I'm sorry, I couldn't process that. Please check your API key and try again."


def is_available() -> bool:
    """Check if Groq API is ready to use."""
    return bool(_get_key()) and _GROQ_OK

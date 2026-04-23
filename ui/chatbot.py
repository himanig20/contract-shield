"""Contract Shield v4.0 — Native Streamlit Chatbot (Component 5).

Flagship feature: context-aware legal assistant using native st.chat_message.
"""
import streamlit as st
from services.groq_client import chat_about_contract, is_available
from config import LANGUAGES, LEGAL_GLOSSARY


# ── Suggestion chips ──────────────────────────────────────────────────────────
SUGGESTIONS_BEFORE = [
    "💡 What does this contract say in simple words?",
    "📋 Summarize the key terms",
    "⚖️ Is this contract legal in India?",
]

SUGGESTIONS_AFTER = [
    "🚨 What are the riskiest clauses?",
    "💰 Is the salary/wage clause fair?",
    "🔒 Is my personal data safe?",
    "🚪 Can they fire me without notice?",
    "📝 What should I negotiate before signing?",
    "✍️ Write a polite message asking to change the risky clauses",
    "🔄 Are there any lock-in or renewal traps?",
    "💬 Explain 'indemnity' in simple language",
]


def _init_chat_state():
    """Initialize all chat session state keys."""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "chat_suggestions_used" not in st.session_state:
        st.session_state.chat_suggestions_used = False


def _get_context() -> tuple[str, str, int, bool]:
    """Return (contract_text, findings_summary, score, analyzed)."""
    contract = st.session_state.get("cs_contract_text", "")
    findings = st.session_state.get("cs_findings", "")
    score = st.session_state.get("cs_score", 0)
    analyzed = st.session_state.get("cs_analyzed", False)
    return contract, findings, score, analyzed


def render_chatbot(language: str = "English"):
    """Render the full chatbot UI in the main content area."""
    _init_chat_state()
    contract, findings_summary, score, analyzed = _get_context()

    st.markdown("""
    <div style="margin-top:0.5rem;">
      <h3 style="font-family:'Inter',sans-serif; font-size:1.2rem; font-weight:800;
                 color:#e8eaf6; margin:0 0 0.3rem; display:flex; align-items:center; gap:0.5rem;">
        <span style="font-size:1.5rem;">🤖</span> Contract Shield AI
      </h3>
      <p style="font-size:0.78rem; color:#7888aa; margin:0 0 0.8rem;">
        Ask anything about your contract — powered by Llama 3.3
      </p>
    </div>
    """, unsafe_allow_html=True)

    if not is_available():
        st.warning("⚠️ Groq API key not found. Add it to `.env` or enter it in the sidebar to enable the chatbot.")
        return

    if not analyzed:
        st.info("📋 Paste and analyze a contract first — then I can answer your questions about it!")
        # Show pre-analysis suggestions
        _render_suggestions(SUGGESTIONS_BEFORE, contract, findings_summary, score, language)
        return

    # Status pill
    st.markdown(f"""
    <div style="display:inline-flex; align-items:center; gap:0.4rem;
                background:rgba(0,255,136,0.08); border:1px solid rgba(0,255,136,0.2);
                border-radius:20px; padding:0.3rem 0.9rem; margin-bottom:0.8rem;">
      <div style="width:8px; height:8px; border-radius:50%; background:#00ff88;
                  animation: pulse 2s infinite;"></div>
      <span style="font-size:0.75rem; color:#00ff88; font-weight:600;">
        Contract analyzed · Score: {score}/100 · Ready to chat
      </span>
    </div>
    """, unsafe_allow_html=True)

    # Render chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"], avatar="🤖" if msg["role"] == "assistant" else "👤"):
            st.markdown(msg["content"])

    # Show initial greeting if no messages yet
    if not st.session_state.chat_history:
        with st.chat_message("assistant", avatar="🤖"):
            greeting = (
                f"Hi! 👋 I've analyzed your contract. **Fairness Score: {score}/100**.\n\n"
                "I can help you understand the risky clauses, suggest negotiation strategies, "
                "or explain any legal terms in simple language.\n\n"
                "Try asking one of the suggestions below, or ask your own question! 🎯"
            )
            st.markdown(greeting)

    # Suggestion chips (show only until first message sent)
    if not st.session_state.chat_suggestions_used:
        _render_suggestions(SUGGESTIONS_AFTER, contract, findings_summary, score, language)

    # Chat input
    user_input = st.chat_input("Ask about your contract…", key="chat_input_main")

    if user_input:
        _process_message(user_input, contract, findings_summary, score, language)


def _render_suggestions(suggestions: list, contract: str, findings: str, score: int, language: str):
    """Render clickable suggestion buttons."""
    # Use columns of 2 for layout
    cols = st.columns(2)
    for idx, sug in enumerate(suggestions):
        col = cols[idx % 2]
        with col:
            if st.button(sug, key=f"sug_{hash(sug)}", use_container_width=True):
                _process_message(sug, contract, findings, score, language)


def _process_message(user_message: str, contract: str, findings: str, score: int, language: str):
    """Process a user message and get AI response."""
    st.session_state.chat_suggestions_used = True

    # Add user message
    st.session_state.chat_history.append({"role": "user", "content": user_message})

    # Check for glossary terms
    glossary_match = _check_glossary(user_message)

    # Get AI response
    with st.spinner("Thinking…"):
        response = chat_about_contract(
            user_message=user_message,
            contract_context=contract,
            findings_summary=findings,
            score=score,
            chat_history=st.session_state.chat_history[:-1],  # Don't include the message we just added
            language=language,
        )

    # Append glossary info if relevant
    if glossary_match:
        response += f"\n\n💡 **Quick definition:** {glossary_match}"

    # Add assistant response
    st.session_state.chat_history.append({"role": "assistant", "content": response})

    # Rerun to show new messages
    st.rerun()


def _check_glossary(message: str) -> str | None:
    """Check if the user's message mentions any legal glossary terms."""
    msg_lower = message.lower()
    for term, definition in LEGAL_GLOSSARY.items():
        if term in msg_lower:
            return f"**{term.title()}**: {definition}"
    return None


def clear_chat():
    """Clear chat history."""
    st.session_state.chat_history = []
    st.session_state.chat_suggestions_used = False

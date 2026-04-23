import json
import streamlit.components.v1 as components
import streamlit as st
from config import GROQ_API_KEY

def inject_floating_chat():
    """Injects a purely frontend-based floating chatbot into the Streamlit DOM."""
    # Get current context
    contract = st.session_state.get("cs_contract_text", "")
    findings = st.session_state.get("cs_findings", "")
    score = st.session_state.get("cs_score", 0)
    
    # We will use the user's sidebar key if available, else environment variable
    api_key_session = st.session_state.get("groq_api_key_input", "")
    api_key = api_key_session if api_key_session else GROQ_API_KEY
    
    # Prepare system prompt for the JS bot
    has_contract = bool(contract and findings)
    
    if has_contract:
        short_findings = findings[:800].replace('\n', ' ') if findings else "None"
        short_contract = contract[:1000].replace('\n', ' ') if contract else "None"
        system_prompt = (
            f"You are Contract Shield AI — a friendly legal assistant embedded in a contract analysis tool.\n\n"
            f"IMPORTANT: The user has ALREADY uploaded and analyzed a real contract through this tool. "
            f"You have the full analysis results. Always reference these specific results when the user asks about their contract, analysis, or risks — do NOT say you need more details.\n\n"
            f"=== CONTRACT ANALYSIS RESULTS ===\n"
            f"Fairness Score: {score}/100\n"
            f"Flagged Issues: {short_findings}\n"
            f"Contract Text Excerpt: {short_contract}\n"
            f"=================================\n\n"
            f"Instructions:\n"
            f"- When asked about the contract, analysis, risks, clauses etc. — use the SPECIFIC data above.\n"
            f"- For general chat, be friendly and helpful.\n"
            f"- Keep responses concise (2-4 sentences) unless asked for detail.\n"
            f"- Use simple, non-legal language."
        )
    else:
        system_prompt = (
            "You are Contract Shield AI — a helpful, friendly legal assistant. "
            "You specialize in Indian labor law, tenant rights, and loan agreements — but you can discuss ANY topic. "
            "Be warm, conversational, and use simple language. "
            "Keep responses concise (2-4 sentences) unless asked for detail. "
            "No contract has been analyzed yet — if the user wants contract analysis, ask them to paste or upload one using the tool above."
        )
    
    # Escape strings safely for JS insertion
    system_prompt_safe = json.dumps(system_prompt)
    api_key_safe = json.dumps(api_key or "")
    
    html_code = f"""
    <script>
    (function() {{
        try {{
            const win = window.parent;
            const doc = win.document;
            
            // Re-run guard
            if (doc.getElementById('cs-chatbot-root')) {{
                // Update context dynamically on reruns without destroying DOM
                win.__cs_system_prompt = {system_prompt_safe};
                win.__cs_api_key = {api_key_safe};
                return;
            }}
            
            // Store context
            win.__cs_system_prompt = {system_prompt_safe};
            win.__cs_api_key = {api_key_safe};
            win.__cs_chat_history = [];
            
            // Create root
            const root = doc.createElement('div');
            root.id = 'cs-chatbot-root';
            doc.body.appendChild(root);

            // Fetch Inter UI font for neatness
            if (!doc.head.querySelector('link[href*="Inter"]')) {{
                const lnk = doc.createElement('link');
                lnk.rel = 'stylesheet';
                lnk.href = 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap';
                doc.head.appendChild(lnk);
            }}

            root.innerHTML = `
                <style>
                    #cs-bot-fab {{
                        position: fixed;
                        bottom: 30px;
                        right: 30px;
                        width: 60px;
                        height: 60px;
                        background: linear-gradient(135deg, #00ff88, #00cc6a);
                        border-radius: 50%;
                        box-shadow: 0 4px 16px rgba(0,255,136,0.3);
                        cursor: pointer;
                        z-index: 10000;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        font-size: 28px;
                        transition: transform 0.2s;
                        border: 3px solid rgba(255,255,255,0.1);
                    }}
                    #cs-bot-fab:hover {{ transform: scale(1.08); }}
                    
                    #cs-bot-panel {{
                        position: fixed;
                        bottom: 100px;
                        right: 30px;
                        width: 360px;
                        height: 550px;
                        background: #0d1529;
                        border: 1px solid #1f2d4f;
                        border-radius: 16px;
                        box-shadow: 0 10px 40px rgba(0,0,0,0.5);
                        z-index: 10000;
                        display: none;
                        flex-direction: column;
                        overflow: hidden;
                        font-family: 'Inter', sans-serif;
                    }}
                    #cs-bot-header {{
                        background: #111c35;
                        padding: 16px;
                        border-bottom: 1px solid #1f2d4f;
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        color: #e8eaf6;
                    }}
                    #cs-bot-body {{
                        flex: 1;
                        padding: 16px;
                        overflow-y: auto;
                        display: flex;
                        flex-direction: column;
                        gap: 12px;
                    }}
                    #cs-bot-input-area {{
                        padding: 16px;
                        background: #111c35;
                        border-top: 1px solid #1f2d4f;
                        display: flex;
                        gap: 8px;
                    }}
                    #cs-bot-input {{
                        flex: 1;
                        padding: 10px;
                        border-radius: 8px;
                        border: 1px solid #1f2d4f;
                        background: #0a0f1e;
                        color: white;
                        font-family: 'Inter', sans-serif;
                        outline: none;
                    }}
                    #cs-bot-input:focus {{ border-color: #00ff88; }}
                    #cs-bot-send {{
                        background: #00ff88;
                        color: #0a0f1e;
                        border: none;
                        border-radius: 8px;
                        padding: 0 16px;
                        font-weight: 700;
                        cursor: pointer;
                    }}
                    .cs-msg {{
                        padding: 10px 14px;
                        border-radius: 12px;
                        max-width: 85%;
                        font-size: 14px;
                        line-height: 1.5;
                        word-wrap: break-word;
                    }}
                    .cs-msg-user {{
                        background: #1f2d4f;
                        color: #e8eaf6;
                        align-self: flex-end;
                        border-bottom-right-radius: 4px;
                    }}
                    .cs-msg-bot {{
                        background: rgba(0,255,136,0.1);
                        color: #00ff88;
                        align-self: flex-start;
                        border: 1px solid rgba(0,255,136,0.2);
                        border-bottom-left-radius: 4px;
                    }}
                    .cs-typing {{ align-self: flex-start; color: #7888aa; font-size: 12px; display:none; }}
                </style>
                <div id="cs-bot-fab">💬</div>
                <div id="cs-bot-panel">
                    <div id="cs-bot-header">
                        <div style="display:flex; align-items:center; gap:8px;">
                            <span style="font-size:20px;">🤖</span>
                            <div style="font-weight:700; font-size:15px; display:flex; flex-direction:column;">
                                <span>Contract Shield AI</span>
                                <span style="font-size:11px; color:#00ff88; font-weight:500;">✓ Ready to help</span>
                            </div>
                        </div>
                        <div id="cs-bot-close" style="cursor:pointer; font-size:18px; color:#7888aa; padding:4px;">✖</div>
                    </div>
                    <div id="cs-bot-body">
                        <div class="cs-msg cs-msg-bot">Hi! 👋 I'm Contract Shield AI. Ask me anything — legal questions, contract advice, or just say hello! 😊</div>
                    </div>
                    <div id="cs-typing" class="cs-typing">AI is thinking...</div>
                    <div id="cs-bot-input-area">
                        <input type="text" id="cs-bot-input" placeholder="Type a message..." autocomplete="off">
                        <button id="cs-bot-send">Send</button>
                    </div>
                </div>
            `;
            
            const fab = doc.getElementById('cs-bot-fab');
            const panel = doc.getElementById('cs-bot-panel');
            const closeBtn = doc.getElementById('cs-bot-close');
            const input = doc.getElementById('cs-bot-input');
            const sendBtn = doc.getElementById('cs-bot-send');
            const body = doc.getElementById('cs-bot-body');
            const typing = doc.getElementById('cs-typing');
            
            fab.onclick = () => {{
                panel.style.display = panel.style.display === 'flex' ? 'none' : 'flex';
            }};
            closeBtn.onclick = () => panel.style.display = 'none';
            
            const appendMessage = (text, isUser) => {{
                const d = doc.createElement('div');
                d.className = 'cs-msg ' + (isUser ? 'cs-msg-user' : 'cs-msg-bot');
                d.textContent = text;
                body.appendChild(d);
                body.scrollTop = body.scrollHeight;
            }};
            
            const sendMessage = async () => {{
                const text = input.value.trim();
                if (!text) return;
                
                if (!win.__cs_api_key) {{
                    appendMessage("⚠️ Missing Groq API Key! Please enter it in the sidebar.", false);
                    return;
                }}
                
                input.value = '';
                appendMessage(text, true);
                typing.style.display = 'block';
                
                const messages = [
                    {{ role: "system", content: win.__cs_system_prompt }}
                ];
                win.__cs_chat_history.push({{ role: "user", content: text }});
                
                // Add recent history to context (limit to last 10 messages)
                messages.push(...win.__cs_chat_history.slice(-10));
                
                try {{
                    const reqBody = {{
                        model: "llama-3.3-70b-versatile",
                        messages: messages,
                        temperature: 0.6,
                        max_tokens: 600
                    }};
                    
                    let res, data;
                    try {{
                        res = await win.fetch("https://api.groq.com/openai/v1/chat/completions", {{
                            method: "POST",
                            headers: {{
                                "Content-Type": "application/json",
                                "Authorization": "Bearer " + win.__cs_api_key
                            }},
                            body: JSON.stringify(reqBody)
                        }});
                        data = await res.json();
                    }} catch (fetchErr) {{
                        appendMessage("❌ Could not reach Groq API. Check your internet/API key. Error: " + fetchErr.message, false);
                        return;
                    }}
                    
                    if (res.ok && data.choices && data.choices.length > 0) {{
                        const reply = data.choices[0].message.content;
                        win.__cs_chat_history.push({{ role: "assistant", content: reply }});
                        appendMessage(reply, false);
                    }} else {{
                        const errMsg = data?.error?.message || JSON.stringify(data) || "Unknown error";
                        appendMessage("❌ API Error: " + errMsg, false);
                    }}
                }} catch (e) {{
                    appendMessage("❌ Unexpected error: " + e.message, false);
                }} finally {{
                    typing.style.display = 'none';
                }}
            }};
            
            sendBtn.onclick = sendMessage;
            input.onkeypress = (e) => {{ if (e.key === 'Enter') sendMessage(); }};
            
        }} catch(err) {{ 
            console.error("ContractShield Bot Error:", err); 
        }}
    }})();
    </script>
    """
    
    # Render with 0 height so the iframe doesn't take up space in Streamlit
    components.html(html_code, height=0, width=0)

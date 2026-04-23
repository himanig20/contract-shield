# 🛡 Contract Shield

> **AI-powered contract analysis tool protecting 450 million informal workers in India**

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)](https://python.org/)
[![License](https://img.shields.io/badge/License-MIT-00ff88)](LICENSE)

---

## 📋 Problem Statement

India has over **450 million informal workers** — domestic helpers, construction laborers, factory workers, street vendors — who routinely sign contracts they don't fully understand. These contracts often contain:

- ❌ **Unfair termination clauses** — fired without notice or pending dues
- ❌ **Illegal wage deductions** — arbitrary salary cuts at employer's discretion
- ❌ **Predatory interest rates** — daily compounding that balloons debt
- ❌ **Forced overtime without pay** — 10+ hour days with zero extra compensation
- ❌ **Liability waivers** — giving up rights to compensation for workplace injuries

Most workers can't afford a lawyer. **Contract Shield** is a free, multilingual tool that uses AI to detect these exploitative clauses and explain them in plain language — empowering workers to protect their rights.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 **Smart Clause Detection** | Pattern-matching engine with 10 risk rules covering Indian labor, rental, and loan law |
| 📊 **Fairness Score & Status** | Visual gauge (0–100) with a sticky summary header that remains visible while scrolling |
| 🖍️ **DocuSign-Style Highlighting** | Dual-tab view showing a breakdown of clauses vs text overlay highlights on the exact original document |
| ⚖️ **Indian Law References** | Each flagged clause links to the specific Act & Section it may violate |
| 🤖 **Contract Shield AI (Llama 70B)** | Expandable floating co-pilot that answers exact context-aware questions about your specific contract |
| 🎬 **Cinematic Loading States** | Custom animated skeleton loaders for a premium waiting experience during logic execution |
| 📄 **PDF & Image Upload** | Upload contracts — text extracted automatically via pdfplumber/OCR |
| 🌐 **Multilingual Support** | Output in English, Hindi, Marathi, or Bengali |
| 💬 **Hindi Mode for Chatbot** | Toggle to ask questions and receive answers in Hindi |
| 🏭 **Sample Contracts** | Built-in exploitative contract samples (Labor, Rental, Loan) for instant testing |
| 🕒 **Session History** | Tracks your last 3 analyses in the sidebar |
| 🎨 **Corporate Identity UI** | Bespoke 'Slate & Teal' light design system, powered by a native Streamlit configuration architecture |

---

## 🖼️ Screenshots

> _Add your screenshots here after running the app._

| Dashboard | Flagged Clauses | AI Chatbot |
|---|---|---|
| ![Dashboard](screenshots/dashboard.png) | ![Clauses](screenshots/clauses.png) | ![Chatbot](screenshots/chatbot.png) |

---

## 🚀 How to Run Locally

### Prerequisites
- Python 3.9 or higher
- A [Groq API key](https://console.groq.com/) (free tier available) — _optional, only for the AI chatbot_

### Step-by-step Setup

```bash
# 1. Clone the repository
git clone https://github.com/himanig20/contract-shield.git
cd contract-shield

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate          # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up the Groq API key (optional, for AI chatbot)
echo "GROQ_API_KEY=gsk_your_key_here" > .env

# 5. Run the app
streamlit run main.py
```

The app will open at **http://localhost:8501** 🎉

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| **Frontend Framework** | Streamlit + Custom HTML/CSS/JS Injection |
| **Logic Engine** | Regex + keyword pattern matching engine (`rules.py`) |
| **AI Co-pilot** | Groq Cloud API (Llama 3 70B) |
| **PDF/OCR** | pdfplumber |
| **Visualizations** | Plotly |
| **Translation** | deep-translator (Google Translate) |
| **Styling** | Native `.streamlit/config.toml` + UI Component architecture |

---

## 📁 Project Structure

```
contract-shield/
├── main.py              # Main application entry point & dashboard
├── config.py            # Global variables, models, and API keys
├── rules.py             # Risk detection rules with Indian law logic
├── utils.py             # Scoring and general utilities
├── requirements.txt     # Python dependencies
├── .streamlit/
│   └── config.toml      # Global light-mode design system enforcer
├── ui/
│   ├── css.py           # Custom global styles and spacing
│   ├── components.py    # Modular UI elements (gauges, highlights, hero)
│   ├── charts.py        # Plotly chart definitions
│   └── floating_chat.py # JS injection for the AI Co-pilot sidebar
├── services/
│   ├── groq_client.py   # AI execution and prompting
│   └── translator.py    # Language localization mapping
└── README.md            
```

---

## 🗺 Future Roadmap

- [ ] 🔤 **OCR Support** — Extract text from scanned PDF contracts using Tesseract
- [ ] 🧠 **ML-based classifier** — Train a model on Indian contract law datasets for deeper analysis
- [ ] 📊 **Comparison mode** — Analyze two contracts side-by-side
- [ ] 💾 **Persistent history** — Save analysis history to a database
- [ ] 📤 **Email/PDF export** — Generate formatted PDF reports
- [ ] 🔐 **User authentication** — Secure accounts with analysis dashboards
- [ ] 🌍 **More languages** — Tamil, Telugu, Kannada, Gujarati support
- [ ] 📱 **Mobile PWA** — Progressive Web App for offline access
- [ ] 🏛️ **Legal aid directory** — Connect users with free legal clinics by state

---

## ⚠️ Disclaimer

> **Contract Shield is NOT a substitute for professional legal advice.**
> 
> This tool provides automated pattern-based analysis to help you identify _potentially_ problematic clauses. It does not guarantee legal accuracy. Always consult a qualified legal professional before making decisions based on contract analysis.
> 
> The AI chatbot uses a language model that may occasionally produce inaccurate information. Verify all legal references independently.

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## 📄 License

This project is licensed under the MIT License.

---

<p align="center">
  <b>🇮🇳 Built for social impact · Protecting workers' rights · Free forever</b>
</p>

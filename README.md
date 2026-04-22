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
| 📊 **Fairness Score** | Visual gauge (0–100) with color-coded risk assessment |
| 🍩 **Risk Breakdown Chart** | Interactive Plotly donut chart showing HIGH/MEDIUM/LOW distribution |
| ⚖️ **Indian Law References** | Each flagged clause links to the specific Act & Section it may violate |
| 🎯 **Dynamic Action Checklist** | "What Should I Do?" steps generated from your actual findings |
| 📄 **PDF Upload** | Upload contract PDFs — text extracted automatically via pdfplumber |
| 🌐 **Multilingual Support** | Output in English, Hindi, Marathi, or Bengali |
| 🤖 **AI Chatbot (Groq/Llama 3)** | Floating chat assistant that answers contract questions in plain language |
| 💬 **Hindi Mode for Chatbot** | Toggle to ask questions and receive answers in Hindi |
| 📱 **WhatsApp Sharing** | One-click share your results with friends and family |
| 📥 **Report Download** | Full analysis report as .txt file |
| 🏭 **Sample Contracts** | 3 built-in exploitative contract samples for instant testing |
| 🕒 **Session History** | Tracks your last 3 analyses in the sidebar |
| 🎨 **Premium Dark UI** | Award-worthy dark theme with glassmorphism, gradients, and micro-animations |

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
| **Frontend** | Streamlit + Custom HTML/CSS/JS |
| **Contract Analysis** | Regex + keyword pattern matching engine |
| **AI Chatbot** | Groq Cloud API (Llama 3 8B) |
| **PDF Parsing** | pdfplumber |
| **Charts** | Plotly |
| **Translation** | deep-translator (Google Translate) |
| **Environment** | python-dotenv |
| **Styling** | Custom dark theme with CSS variables, glassmorphism, SVG gauges |

---

## 📁 Project Structure

```
contract-shield/
├── main.py              # Main Streamlit application + UI
├── rules.py             # Risk detection rules with Indian law references
├── utils.py             # Scoring, translation, preprocessing utilities
├── requirements.txt     # Python dependencies
├── .env                 # API keys (not committed to git)
├── .gitignore           # Ignores .env and other sensitive files
└── README.md            # You are here!
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

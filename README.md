# Lexify AI 🛡️

**Understand Before You Sign.**


**A smart LegalTech platform that decodes dense legal jargon, highlights predatory clauses, and empowers you to negotiate with confidence.**


-----

## 📖 Introduction

Legal documents are notorious for being intentionally dense, confusing, and overwhelming. **Lexify AI** is an AI-powered LegalTech platform designed to level the playing field. By instantly parsing complex contracts like rental agreements and Terms of Service (ToS), Lexify acts as your personal legal assistant—translating archaic jargon into plain English, flagging hidden risks.

## ⚠️ Problem Statement

  * **Information Asymmetry:** Landlords and corporations use dense legalese to obscure unfavorable terms.
  * **The "Blind Sign" Epidemic:** 90% of individuals sign Terms of Service and rental agreements without fully reading them due to cognitive overload.
  * **Lack of Actionability:** Even if a user spots an unfair clause, they often lack the professional vocabulary required to push back and negotiate effectively.

## 💡 Solution Overview

Lexify AI bridges the gap between complex legal documents and everyday consumers. Users simply upload a PDF or paste their contract text. Our AI engine scans the document clause-by-clause, categorizes risks using a visual traffic-light system, provides simplified explanations.

-----

## ✨ Key Features

  * **📄 Universal Document Parsing:** Seamlessly extract text from uploaded PDFs (using PyPDF2) or direct text inputs.
  * **🚦 Intelligent Risk Highlighting:**
      * 🔴 **Red (Unsafe):** Predatory clauses, hidden fees, or severe rights waivers.
      * 🟡 **Yellow (Caution):** Ambiguous terms or unusual obligations that require review.
      * 🟢 **Green (Safe):** Standard, fair, and legally balanced clauses.
  * **🧠 Jargon-to-Plain-English Translation:** Converts archaic legalese ("heretofore", "indemnify") into clear, 8th-grade reading level summaries.
  * **⚖️ Overall Verdict Generation:** Calculates a holistic risk score and provides a definitive recommendation: *Safe to Sign* or *Proceed with Caution*.

-----

## 🛠️ How It Works

1.  **Input:** The user uploads a legal PDF or pastes raw contract text into the Next.js dashboard.
2.  **Extraction:** The Python backend securely extracts the raw text and chunks it by clause.
3.  **Analysis:** The text is routed through an LLM API, which evaluates each clause against established legal standards and consumer protection frameworks.
4.  **Visualization:** The frontend renders a Turnitin-style side-by-side view, mapping the original text to color-coded risks and plain-English translations.

-----

## 💻 Tech Stack

**Frontend**

  * **Framework:** Next.js / React
  * **Styling:** Tailwind CSS (Theme: Deep Blue, \#00A19B Accents, Crisp White)

**Backend**

  * **Framework:** Python (FastAPI for high-performance async routing)
  * **PDF Processing:** PyPDF2

**AI & Machine Learning**

  * **NLP Engine:** Gemini / OpenAI API
  * **Prompt Engineering:** Few-shot prompting tailored for legal document syntax

-----

## ⚙️ System Architecture

1.  **Client (Next.js):** Handles UI state, file uploads, and renders the interactive risk dashboard.
2.  **API Gateway (FastAPI):** Receives the payload, manages file validation, and orchestrates the parsing pipeline.
3.  **Parser Module:** PyPDF2 extracts text while preserving structural integrity (paragraphs, lists).
4.  **AI Processing Layer:** The LLM evaluates the text asynchronously, returning a structured JSON response containing the risk levels, translations, and verdicts.
5.  **Response:** FastAPI serves the compiled JSON back to the Next.js client for rendering.

-----

## 🚀 Installation & Setup

### Prerequisites

  * Node.js (v18+)
  * Python (3.9+)
  * API Key for your chosen LLM (OpenAI/Gemini)

### 1\. Clone the Repository

```bash
git clone https://github.com/devesh1308/jargon-transaltors.git
cd jargon-transaltors
```

### 2\. Backend Setup (FastAPI)

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt

# Create a .env file and add your API key
echo "LLM_API_KEY=your_api_key_here" > .env

# Run the server
uvicorn main:app --reload
```

*The backend will be running at `http://127.0.0.1:8000`*

### 3\. Frontend Setup (Next.js)

```bash
# Open a new terminal
cd frontend
npm install

# Run the development server
npm run dev
```

*The frontend will be running at `[http://localhost:8501](http://localhost:8501)`*

-----

## 🎯 Unique Selling Points (USP)

  * **Zero Learning Curve:** A beautiful, highly intuitive UI that requires zero legal background to understand.
  * **Privacy First:** (Configurable) Text processing is done ephemerally; we do not store your highly sensitive lease agreements in a database.

-----

## 🌍 Real-world Use Cases

1.  **Mumbai Residential Leave & License Agreements:** Instantly catching abnormal lock-in periods, illegal maintenance fee shifts, or predatory deposit forfeiture clauses before renting an apartment.
2.  **Freelance Contracts:** Helping independent contractors spot unreasonable non-compete clauses or IP-surrender terms.
3.  **Software Terms of Service:** Quickly scanning SaaS agreements to see what data the company is actually harvesting.

-----

## 🔮 Future Scope

  * **Chrome Extension:** A browser plugin that automatically scans "Terms of Service" pop-ups on the web before you click "I Agree".
  * **OCR Integration:** Adding Tesseract OCR to support scanned, non-searchable PDF image documents.
  * **Multi-language Support:** Translating complex English legal documents into local regional languages for broader accessibility.

-----

## 💼 Business Model

  * **Freemium Tier:** Free basic scans for standard documents (up to 5 pages), highlighting red flags without deep explanations.
  * **Pro Tier (Pay-per-scan or Subscription):** Full plain-English translations, unlimited pages.
  * **B2B API:** Licensing the Lexify parsing engine to real estate portals and HR platforms.

-----

## 📁 Folder Structure

```text
jargon-transaltors/
├── backend/
│   ├── __pycache__/
│   │   ├── main.cpython-312.pyc
│   │   └── main.cpython-314.pyc
│   ├── .vscode/
│   ├── config/
│   │   └── dictionary.json
│   ├── model/
│   │   ├── linear_svc.pkl
│   │   └── logistic_regression.pkl
│   ├── models/
│   │   ├── linear_svc.pkl
│   │   └── logistic_regression.pkl
│   ├── samples/
│   │   ├── Clean_Pune_Agreement.pdf
│   │   ├── mumbai_trap_lease.pdf
│   │   └── test_contract.pdf
│   ├── scripts/
│   │   ├── evaluate_ensemble.py
│   │   ├── train_logistic.py
│   │   └── train_svc.py
│   ├── utils/
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   ├── pdf_processor.py
│   │   ├── pii_masking.py
│   │   └── text_cleaner.py
│   ├── venv/
│   ├── .gitignore
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── app.py
│   └── lexify.png
└── README.md
```

-----

## 🤝 Contributing Guidelines

We welcome contributions to make LegalTech accessible to everyone\!

1.  Fork the repository.
2.  Create a feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

-----

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

-----

## 👥 Team Details

  * **Swaraj Dalvi** – Frontend Developer
  * **Nihar Padave** – Backend Developer
  * **Devesh Patel** – ML Engineer
  * **Harsh Bajania** – ML Engineer

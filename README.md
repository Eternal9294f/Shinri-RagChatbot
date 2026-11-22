<div align="center">

# 🔎 **_Shinri_**
### Mutual Funds Facts Chatbot &bull; Groww Context
*NextLeap Product Management Fellowship &bull; Milestone 4 Portfolio Prototype*

<br>

[![Live Demo on Render](https://img.shields.io/badge/Live%20App-Render%20Web%20Service-8C2B38?style=for-the-badge&logo=render&logoColor=white)](https://shinri-mf-rag.onrender.com)
[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-1C1917?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Eternal9294f/Shinri-)
[![Evaluation Suite](https://img.shields.io/badge/Evaluation-100%25%20Passed%20(46%2F46)-15803D?style=for-the-badge)](docs/evaluation_report.md)

<br>

**[🌐 Launch Live Application](https://shinri-mf-rag.onrender.com)** &bull; **[📊 View Evaluation Report (46/46 Passed)](docs/evaluation_report.md)** &bull; **[📑 Sample Q&A Deliverable](docs/sample_qa.md)**

</div>

<br>

> **_Shinri_** translates to *"The Truth"* — verifiable financial reality stripped of speculation. **_Shinri_** is an evidence-grounded **Mutual Funds Facts Chatbot** engineered for the Groww mutual fund ecosystem. Instead of generic AI chatbots that hallucinate figures or provide unauthorized financial advice, **_Shinri_** queries verified statutory scheme disclosures (SID, KIM, and monthly factsheets) to deliver source-attributed, factual answers with zero noise and strictly non-advisory precision.

---

## 🔗 Live Application Links

| Destination | URL | Description |
|---|---|---|
| **🌐 Production App (Render)** | **[https://shinri-mf-rag.onrender.com](https://shinri-mf-rag.onrender.com)** | Live web application with peaceful PromptBolo editorial styling. |
| **📂 Source Repository** | **[https://github.com/Eternal9294f/Shinri-](https://github.com/Eternal9294f/Shinri-)** | Complete source code, pre-built ChromaDB index, and evaluation test suite. |
| **📊 Evaluation Report** | **[docs/evaluation_report.md](docs/evaluation_report.md)** | Empirical 46/46 test cases passed (100% accuracy across 6 test suites). |
| **📑 Sample Q&A Deliverable** | **[docs/sample_qa.md](docs/sample_qa.md)** | Comprehensive evidence-grounded queries across all 5 HDFC schemes. |

---

## 🎯 The Problem

Mutual fund scheme attributes (expense ratios, exit load slabs, statutory lock-in periods, riskometer classifications, minimum SIP thresholds, and statement download workflows) are buried across lengthy 80+ page Scheme Information Documents (SIDs), KIMs, and monthly factsheets.

Retail investors face two significant pain points:
1. **Factual Discovery Friction**: Locating exact scheme clauses requires substantial time and deep financial literacy.
2. **LLM Hallucinations & Regulatory Risk**: Standard AI models routinely invent NAV numbers, fabricate past returns, or breach regulatory boundaries by offering unsolicited financial recommendations.

**The Solution:** An auditable, non-advisory, evidence-grounded RAG application that answers strictly when backed by retrieved official AMC disclosures and firmly declines opinionated financial advice.

---

## 💡 What **_Shinri_** Does

### 5 Ingested HDFC Mutual Fund Schemes (Direct - Growth Plans)
1. **Large Cap**: [HDFC Large Cap Fund Direct Plan - Growth](https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth) *(Benchmark: NIFTY 100 TRI)*
2. **Flexi Cap**: [HDFC Flexi Cap Fund Direct Plan - Growth](https://groww.in/mutual-funds/hdfc-equity-fund-direct-growth) *(Benchmark: NIFTY 500 TRI)*
3. **ELSS (Tax Saver)**: [HDFC ELSS Tax saver Fund Direct Plan - Growth](https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth) *(Benchmark: NIFTY 500 TRI, Mandatory 3-Year Lock-in)*
4. **Small Cap**: [HDFC Small Cap Fund Direct Plan - Growth](https://groww.in/mutual-funds/hdfc-small-cap-fund-direct-growth) *(Benchmark: BSE 250 SmallCap TRI)*
5. **Balanced Advantage**: [HDFC Balanced Advantage Fund Direct Plan - Growth](https://groww.in/mutual-funds/hdfc-balanced-advantage-fund-direct-growth) *(Benchmark: NIFTY 50 Hybrid Composite Debt 50:50)*

### Core Capabilities
* **Semantic Vector Retrieval**: Chunks indexed into persistent **ChromaDB** using local `sentence-transformers/all-MiniLM-L6-v2` (384 dimensions).
* **Intent-Aware Hybrid Reranking**: Boosts chunks matching specific intent keywords (e.g. Expense Ratio, Exit Load, Lock-in, SIP) for pinpoint precision.
* **Conversational Memory Window (10 turns)**: Disambiguates contextual follow-ups (e.g., *"What about its exit load?"* $\rightarrow$ resolves the active scheme in context).
* **Deterministic Financial Safety Guardrails**:
  - **Zero Advice Mandate**: Refuses prompts like *"Should I invest?"*, *"Will it yield 20%?"*, or portfolio allocations with a polite facts-only guidance notice.
  - **Zero PII**: Rejects PAN cards, Aadhaar numbers, phone numbers, and bank account information.
  - **Out-of-Scope Gate**: Flags requests for unsupported AMCs (SBI, Axis, Nippon) with an explicit notice.
* **Strict Response Rules**: Answers $\le 3$ sentences, exactly 1 official source link, and "Last updated from sources: 27 September 2026."

---

## ⚙️ System Architecture

```
[5 Official Scheme Pages] ──► [Normalizer] ──► data/raw/*.txt
                                     │
                                     ▼
                               [Semantic Chunker] ──► data/chunks/chunks.txt (41 Chunks)
                                     │
                                     ▼
                      [MiniLM Local Embedder (384-d)] ──► data/embeddings_preview.txt
                                     │
                                     ▼
                            [ChromaDB Vector Store] (Persistent on disk)

────────────────────────────────────────────────────────────────────────────────────────

[User Query] ──► [Guardrails: PII / Advisory / Other AMC] ──[Triggered]──► Polite Refusal
                       │
                 [Cleared]
                       ▼
       [10-Turn Memory Query Rewriter]
                       │
                       ▼
 [Intent-Reranked Similarity Search (ChromaDB)]
                       │
                       ▼
   [Grounded Groq LLM Prompt / Deterministic Extractor]
                       │
                       ▼
    [Peaceful Editorial UI (FastAPI/HTML/CSS/JS)]
```

---

## 🛡️ Evaluation Results (100% Pass Rate)

An automated suite of 46 rigorous test cases was executed across 6 functional dimensions:

| Category | Description | Tests | Pass Rate | Status |
|---|---|---|---|---|
| **Factual Queries** | Expense ratios, exit loads, min SIP, lock-ins, riskometer, benchmarks | 25 | **100%** (25/25) | ✅ PASSED |
| **Operational Guides** | Capital gains statements, CAS holding downloads, stamp duty | 3 | **100%** (3/3) | ✅ PASSED |
| **Hinglish Queries** | Natural multilingual phrasing ("kitna hai", "kab tak lock in") | 4 | **100%** (4/4) | ✅ PASSED |
| **Advisory Refusals** | Solicitations for buy/sell advice, return predictions, fund ranking | 7 | **100%** (7/7) | ✅ PASSED |
| **PII Protection** | Rejection of PAN (`[A-Z]{5}[0-9]{4}[A-Z]`), Aadhaar, Phone, Bank Account | 4 | **100%** (4/4) | ✅ PASSED |
| **Out-of-Scope Gate** | Queries targeting unsupported AMCs (SBI Bluechip, etc.) or non-finance | 3 | **100%** (3/3) | ✅ PASSED |
| **Total** | **Comprehensive Automated Suite** | **46** | **100.0% (46/46 Passed)** | ✅ ALL PASSED |

*Detailed test case results available in [docs/evaluation_report.md](docs/evaluation_report.md).*

---

## 🧰 Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Backend API** | FastAPI / Python 3.10+ | Asynchronous REST endpoints (`/api/chat`, `/api/health`, `/api/clear`). |
| **Frontend UI** | HTML5, CSS3, Vanilla JS | Peaceful editorial design inspired by PromptBolo (`#FAF8F5` canvas, `#8C2B38` wine accent). |
| **Alternative UI** | Streamlit | Rapid interactive prototyping and fallback demo interface (`src/app.py`). |
| **Vector Database** | ChromaDB (`chromadb`) | Embedded, persistent on-disk vector database (committed pre-built index). |
| **Embedding Engine** | `sentence-transformers/all-MiniLM-L6-v2` | Lightweight 384-dimensional dense embeddings running locally with startup pre-warming. |
| **LLM Inference** | Groq Cloud (`llama-3.3-70b-versatile`) | Ultra-fast token generation (~300 tok/s) with deterministic grounded prompting. |
| **Deployment** | Render Web Services | Cloud deployment with continuous delivery from GitHub `main`. |

---

## 🚀 Quickstart & Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Eternal9294f/Shinri-.git
cd Shinri-
```

### 2. Set Up Virtual Environment & Dependencies
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Environment Variables Setup
Copy the template and configure your Groq API key:
```bash
cp .env.example .env
```
Edit `.env`:
```ini
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```
*(Note: If no Groq key is provided, **_Shinri_** automatically utilizes its built-in deterministic factual synthesis engine so the app runs out-of-the-box!)*

### 4. Run One-Command Ingestion (Builds Vector DB)
```bash
python -m src.ingest.run
```
*Outputs: 41 chunks created, 41 embeddings generated, and persistent ChromaDB index saved.*

### 5. Launch the Application

**Option A: Web Interface (FastAPI + HTML/CSS/JS - Recommended)**
```bash
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```
Open [http://localhost:8000](http://localhost:8000) in your browser.

**Option B: Streamlit Interface**
```bash
python -m streamlit run src/app.py
```

**Option C: Terminal CLI Testing**
```bash
python cli.py
```

### 6. Run Automated Evaluation Suite
```bash
python -m tests.test_evaluation
```

---

## ☁️ Deployment Guide (Render Web Service)

**_Shinri_** is deployed live at **[https://shinri-mf-rag.onrender.com](https://shinri-mf-rag.onrender.com)**.

To deploy your own instance on Render:

| Setting | Value |
|---|---|
| **Environment** | Python 3 |
| **Root Directory** | *(Leave blank - repo root)* |
| **Build Command** | `pip install --no-cache-dir -r requirements.txt` |
| **Start Command** | `uvicorn src.main:app --host 0.0.0.0 --port $PORT` |
| **Environment Variables** | `GROQ_API_KEY`, `GROQ_MODEL=llama-3.3-70b-versatile` |

---

## 📌 Product Management Reflection (NextLeap Milestone 4)

> *"This project highlighted the distinction between building an AI feature and architecting an AI product.*
>
> *The model is merely one component. The actual product is the socio-technical system surrounding it:*  
> **Problem Definition $\rightarrow$ Verifiable Statutory Corpus $\rightarrow$ Domain Chunking $\rightarrow$ Semantic Retrieval $\rightarrow$ Safety Guardrails $\rightarrow$ Explainable UX $\rightarrow$ Quantitative Evaluation $\rightarrow$ User Trust.**
>
> *Rather than asking 'Can I make a chatbot talk?', the product engineering challenge was: 'What should this product know, what must it refuse to know, and how do I empirically prove to users and regulators that it is safe, grounded, and compliant?'"*

---

## 📄 License
Distributed under the MIT License. Developed as part of the NextLeap Product Management Fellowship (Milestone 4).

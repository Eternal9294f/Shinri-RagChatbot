#                                                 🔎 Shinri (真理)
###                         Verifiable Mutual Fund Information Assistant &bull; Groww Context
*  NextLeap Product Management Fellowship &bull; Milestone 4 Portfolio Prototype*


> **Shinri (真理)** evidence-grounded financial information assistant built for the Groww mutual fund platform context. Instead of generic AI chat that hallucinates facts or offers unauthorized financial advice, Shinri retrieves verified facts from official scheme documentation (SID/KIM/Groww disclosures) and synthesizes concise, source-attributed answers with clickable citations.

---

## 🎯 The Problem

Mutual fund scheme characteristics (expense ratios, exit load slabs, statutory lock-in periods, riskometer levels, minimum SIP amounts, and statement download procedures) are scattered across lengthy 80+ page Scheme Information Documents (SIDs), factsheets, and web portals. 

Retail investors face two severe issues:
1. **Factual Discovery Friction**: Finding specific scheme clauses takes considerable time and financial literacy.
2. **LLM Hallucinations & Regulatory Risk**: Standard chatbots frequently invent NAVs, fabricate past returns, or cross regulatory boundaries by giving subjective investment advice.

**The Solution:** An auditable, non-advisory, evidence-grounded RAG application that answers only when supported by retrieved official disclosures and strictly refuses opinionated financial advice.

---

## 💡 What Shinri Does

### 5 Ingested HDFC Mutual Fund Schemes (Direct - Growth Plans)
1. **Large Cap**: [HDFC Large Cap Fund Direct Plan - Growth](https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth) (Benchmark: NIFTY 100 TRI)
2. **Flexi Cap**: [HDFC Flexi Cap Fund Direct Plan - Growth](https://groww.in/mutual-funds/hdfc-equity-fund-direct-growth) (Benchmark: NIFTY 500 TRI)
3. **ELSS (Tax Saver)**: [HDFC ELSS Tax saver Fund Direct Plan - Growth](https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth) (Benchmark: NIFTY 500 TRI, 3-Yr Lock-in)
4. **Small Cap**: [HDFC Small Cap Fund Direct Plan - Growth](https://groww.in/mutual-funds/hdfc-small-cap-fund-direct-growth) (Benchmark: BSE 250 SmallCap TRI)
5. **Balanced Advantage**: [HDFC Balanced Advantage Fund Direct Plan - Growth](https://groww.in/mutual-funds/hdfc-balanced-advantage-fund-direct-growth) (Benchmark: NIFTY 50 Hybrid 50:50)

### Key Features
* **Semantic Vector Retrieval**: Chunks indexed into persistent **ChromaDB** using local `sentence-transformers/all-MiniLM-L6-v2` (384 dimensions).
* **Intent-Aware Hybrid Reranking**: Boosts sections matching user intent (e.g., Expense Ratio, Exit Load, Lock-in, SIP) for 100% precision.
* **Conversational Memory Window (10 turns)**: Disambiguates follow-ups (e.g. *"What about its exit load?"* $\rightarrow$ resolves the active scheme).
* **Deterministic Financial Safety Guardrails**:
  - **Zero Advice Mandate**: Rejects *"Should I buy?"*, *"Will it give 20% return?"*, or portfolio questions with a polite facts-only notice.
  - **Zero PII**: Instantly rejects PAN cards, Aadhaar numbers, phone numbers, or bank account details.
  - **Unsupported Corpus Gate**: Flags non-HDFC AMCs (SBI, Axis, Nippon) with an explicit notice.
* **Strict Response Rules**: Answers $\le 3$ sentences, exactly 1 official source link, and "Last updated from sources: 27 September 2026."

---

## ⚙️ How It Works (Architecture)

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
    [Premium Fintech UI (FastAPI/HTML/CSS or Streamlit)]
```

---

## 🛡️ Evaluation Results (100% Pass Rate)

An automated suite of 46 rigorous test cases was executed across 6 functional dimensions:

| Category | Description | Tests | Pass Rate |
|---|---|---|---|
| **Factual Queries** | Expense ratio, exit loads, min SIP, lock-ins, riskometer, benchmarks | 25 | **100%** (25/25) |
| **Operational Guides** | Capital gains statements, CAS holding downloads, stamp duty | 3 | **100%** (3/3) |
| **Hinglish Queries** | Natural multilingual phrasing ("kitna hai", "kab tak lock in") | 4 | **100%** (4/4) |
| **Advisory Refusals** | Solicitations for buy/sell advice, return predictions, fund ranking | 7 | **100%** (7/7) |
| **PII Protection** | Rejection of PAN (`[A-Z]{5}[0-9]{4}[A-Z]`), Aadhaar, Phone, Bank Account | 4 | **100%** (4/4) |
| **Out-of-Scope Gate** | Queries targeting unsupported AMCs (SBI Bluechip, etc.) or non-finance | 3 | **100%** (3/3) |
| **Total** | **Comprehensive Automated Suite** | **46** | **100.0% (46/46 Passed)** |

*Full evaluation log available in [docs/evaluation_report.md](docs/evaluation_report.md).*

---

## 🧰 Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Backend API** | FastAPI / Python 3.10+ | High-performance asynchronous API endpoints (`/api/chat`, `/api/health`). |
| **Frontend UI** | HTML5, CSS3, Vanilla JS | Ultra-minimal, Groww-inspired fintech dark UI with glassmorphism cards. |
| **Alternative UI** | Streamlit | Rapid interactive prototyping and fallback demo interface (`src/app.py`). |
| **Vector Database** | ChromaDB (`chromadb`) | Embedded, persistent on-disk vector database (no external Docker dependency). |
| **Embedding Engine** | `sentence-transformers/all-MiniLM-L6-v2` | Lightweight 384-dimensional dense embeddings running 100% locally. |
| **LLM Inference** | Groq Cloud (`llama-3.3-70b-versatile`) | Ultra-fast token generation (~300 tok/s) with deterministic grounded prompting. |
| **Deployment** | Render Web Services / Docker | Cloud web service with automated GitHub push triggers. |

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
*(Note: If no Groq key is provided, Shinri automatically uses its built-in deterministic factual synthesis engine so the app runs out-of-the-box!)*

### 4. Run One-Command Ingestion (Builds Vector DB)
```bash
python -m src.ingest.run
```
*Outputs: 41 chunks created, 41 embeddings generated, and persistent ChromaDB index saved.*

### 5. Launch the Application

**Option A: Premium Web Interface (FastAPI + HTML/CSS/JS - Recommended)**
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

To deploy Shinri on Render as an automated web service:

| Setting | Value |
|---|---|
| **Environment** | Python 3 |
| **Root Directory** | *(Leave blank - repo root)* |
| **Build Command** | `pip install -r requirements.txt && python -m src.ingest.run` |
| **Start Command** | `uvicorn src.main:app --host 0.0.0.0 --port $PORT` *(or `python -m streamlit run src/app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true`)* |
| **Environment Variables** | `GROQ_API_KEY`, `GROQ_MODEL=llama-3.3-70b-versatile` |

---

## 📌 Product Management Reflection (NextLeap Milestone 4)

> *"This project helped me understand the profound difference between building an AI feature and architecting an AI product.*
>
> *The model is merely one component. The actual product is the socio-technical system surrounding it:*  
> **Problem Definition $\rightarrow$ Verifiable Corpus $\rightarrow$ Domain Chunking $\rightarrow$ Semantic Retrieval $\rightarrow$ Safety Guardrails $\rightarrow$ Explainable UX $\rightarrow$ Quantitative Evaluation $\rightarrow$ User Trust.**
>
> *Rather than asking 'Can I make a chatbot talk?', the product engineering challenge was: 'What should this product know, what must it refuse to know, and how do I empirically prove to users and regulators that it is safe, grounded, and compliant?'"*

---

## 📄 License
Distributed under the MIT License. Developed as part of the NextLeap Product Management Fellowship (Milestone 4).

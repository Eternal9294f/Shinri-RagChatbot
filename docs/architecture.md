# System Architecture Document

## Product: Shinri (真理) - Mutual Fund Facts Assistant
*Demonstration Context: Groww | Architecture Blueprint*

---

## 1. High-Level System Architecture

Shinri employs a decoupled, verifiable Retrieval-Augmented Generation (RAG) architecture optimized for zero hallucination and strict source grounding.

```
                              DATA INGESTION PIPELINE (Offline / One-time)
  ┌───────────────────────┐
  │ 5 HDFC Scheme Pages   │
  │ (Groww / AMC Public)  │
  └───────────┬───────────┘
              ▼
  ┌───────────────────────┐     data/raw/*.txt
  │ Scraper & Normalizer  ├─────────────────────────────────────────┐
  └───────────┬───────────┘                                         │
              ▼                                                     ▼
  ┌───────────────────────┐     data/chunks/chunks.txt     ┌─────────────────┐
  │ Semantic Chunker      ├───────────────────────────────►│ Chunks Preview │
  └───────────┬───────────┘                                └─────────────────┘
              ▼
  ┌───────────────────────┐     Local (all-MiniLM-L6-v2)
  │ Embedding Engine      │     384 Dimensions
  └───────────┬───────────┘
              ▼
  ┌───────────────────────┐     ./chroma_db
  │ ChromaDB Vector Store │◄── (Persistent SQLite + Parquet)
  └───────────────────────┘

─────────────────────────────────────────────────────────────────────────────

                              QUERY & RESPONSE PIPELINE (Online / Runtime)
  ┌───────────────────────┐
  │ User Query + History  │
  └───────────┬───────────┘
              ▼
  ┌───────────────────────┐
  │ Guardrail & Classifier│────[Refusal: Advice/PII/Off-topic]───► Immediate Polite Refusal
  └───────────┬───────────┘
              ▼ (Allowed Factual Query)
  ┌───────────────────────┐
  │ Contextual Rewriter   │ (Memory: Last 10 turns for follow-ups)
  └───────────┬───────────┘
              ▼
  ┌───────────────────────┐
  │ Embedding (Query)     │ (Same sentence-transformers/all-MiniLM-L6-v2)
  └───────────┬───────────┘
              ▼
  ┌───────────────────────┐
  │ Top-k Retrieval       │ (ChromaDB Cosine / L2 Similarity Search)
  └───────────┬───────────┘
              ▼
  ┌───────────────────────┐
  │ Grounded Augmenter    │ (System Prompt + Retrieved Chunks + Disclaimers)
  └───────────┬───────────┘
              ▼
  ┌───────────────────────┐
  │ Groq LLM Inference    │ (GROQ_MODEL, e.g. llama-3.3-70b-versatile)
  └───────────┬───────────┘
              ▼
  ┌───────────────────────┐
  │ Output Formatter      │ (<= 3 sentences + Verified Source Link + Timestamp)
  └───────────┬───────────┘
              ▼
  ┌───────────────────────┐
  │ FastAPI / Streamlit UI│
  └───────────────────────┘
```

---

## 2. Component Breakdown

### A. Data Ingestion Pipeline
1. **Raw Document Acquisition**: Fetches and normalizes text from the 5 target HDFC schemes on Groww/AMC. Saved to `data/raw/` for complete auditability.
2. **Chunking Engine**: Splits raw documents into logical, semantic sections (Fund Overview, Fees & Exit Load, Minimum Investment & Lock-in, Riskometer & Benchmark, Tax Implications).
   - Keeps document title, scheme name, category, source URL, and timestamp in chunk metadata.
   - Emits a human-readable inspection file at `data/chunks/chunks.txt`.
3. **Embedding Engine**:
   - Model: `sentence-transformers/all-MiniLM-L6-v2`.
   - Dimension: 384 vectors.
   - Execution: 100% local CPU/GPU, zero external API dependencies or costs.
   - Exports preview of the first 5 embeddings (first 10 dimensions) to `data/embeddings_preview.txt`.
4. **Vector Database**:
   - Engine: **ChromaDB**.
   - Storage: Local persistent directory (`chroma_db/`).
   - Idempotent: Subsequent restarts load the existing database without re-embedding.

### B. Query & Retrieval Runtime
1. **Guardrail Interceptor**:
   - Detects queries seeking personalized financial advice ("Should I buy?", "Will it beat FD?").
   - Blocks PII attempts (PAN cards, Aadhaar, account numbers).
   - Flags out-of-domain queries and issues canned polite refusals.
2. **Context Memory & Query Rewriter**:
   - Maintains a sliding window of the last 10 conversational turns.
   - Rewrites co-references (e.g. "What is its exit load?" -> "What is the exit load for HDFC Large Cap Fund?").
3. **ChromaDB Retriever**:
   - Generates 384-d vector for the user query using the exact same MiniLM model.
   - Fetches Top-$k$ ($k=3$ to $5$) nearest chunks with metadata and source URLs.
4. **Grounded Generation Engine**:
   - Client: **Groq API** (`groq` Python SDK).
   - Prompt Engineering: Enforces strict adherence to context. If context does not contain the answer, instructs the model to explicitly state "I don't know based on official sources."
   - Output Constraints: Maximum 3 sentences, followed by the source citation and source timestamp.

### C. User Interface
- Framework: **FastAPI (Primary) + Streamlit (Fallback)**.
- Layout: Clean Groww-inspired fintech UI, featuring:
  - Header with facts-only notice: *"Facts-only. No investment advice."*
  - 4 quick-start sample prompt chips.
  - Interactive chat stream.
  - Expandable "Sources & Retrieved Chunks" inspection drawer below each message.
  - Clear conversation button.

---

## 3. Technology Stack Summary

| Layer | Technology | Selection Rationale |
|---|---|---|
| **Programming Language** | Python 3.10+ | Standard ecosystem for RAG, NLP, and data tooling. |
| **Embedding Model** | `sentence-transformers/all-MiniLM-L6-v2` | Fast, lightweight (80MB), 384-d, runs locally without API key. |
| **Vector Database** | ChromaDB (`chromadb`) | Lightweight, self-contained, persistent on disk without Docker. |
| **LLM Inference** | Groq Cloud SDK (`groq`) | Ultra-fast token generation (~300 tok/s), generous free tier. |
| **Frontend UI** | HTML/CSS/JS + Streamlit | Rapid prototyping, interactive state management, seamless demo. |
| **Environment Mgmt** | `python-dotenv` | Secure `.env` configuration, preventing credential leakage. |
| **Deployment Target** | Render Web Services | Cloud hosting with automated Git-triggered builds. |

# Implementation Plan: 6-Phase Execution Guide

## Product: Shinri (真理) - Mutual Fund Facts Assistant
*Demonstration Context: Groww | Phased Implementation Roadmap*

> **Notice:** This document defines the exact step-by-step implementation phases.

---

## Phase 1: Project Setup & Environment Baseline

### Objective
Establish the project workspace, virtual environment, dependencies, folder structure, and environment configuration templates to ensure clean reproducibility and zero credential leakage.

### Files Created
* `requirements.txt`: Pin exact library versions (`fastapi`, `uvicorn`, `streamlit`, `chromadb`, `sentence-transformers`, `groq`, `python-dotenv`, `beautifulsoup4`, `requests`, `rich`).
* `.gitignore`: Strictly exclude `.env`, `venv/`, `.venv/`, `__pycache__/`, `chroma_db/`, `.DS_Store`.
* `.env.example`: Template declaring `GROQ_API_KEY=` and `GROQ_MODEL=llama-3.3-70b-versatile`.
* `src/config.py`: Centralized configuration constants (paths, embedding model name, collection name, Groq model defaults).
* Directory tree: `data/raw/`, `data/chunks/`, `src/ingest/`, `src/rag/`, `src/static/`, `src/templates/`, `tests/`.

### Verification Criteria
* Run: `python -c "import chromadb, sentence_transformers, groq, fastapi, streamlit; print('All core packages imported successfully!')"`
* Check `.gitignore` contains `.env` and `chroma_db/`.

---

## Phase 2: Loading & Chunking Strategy

### Objective
Ingest the 5 official public Groww scheme pages for HDFC Mutual Fund, clean the text into normalized factual sections, and divide the documents using an auditable, domain-aware chunking strategy.

### Files Created
* `data/sources.csv`: Manifest of the 5 schemes, categories, and direct Groww URLs.
* `src/ingest/scraper.py`: Loads the 5 target scheme pages or clean markdown representations, stripping navigation headers, ads, and footers.
* `src/ingest/chunker.py`: Implements section-based chunking with paragraph fallbacks.
* Output files generated:
  * `data/raw/<scheme_slug>.txt`: 5 raw scraped/normalized text files.
  * `data/chunks/chunks.txt`: Complete, numbered listing of all chunks with word/character counts and associated metadata (Scheme Name, Category, URL, Section).

### Chunking Rationale & Parameters
* **Strategy**: Section-header semantic chunking (e.g. `[Fund Overview]`, `[Fees & Exit Load]`, `[SIP & Minimums]`, `[Taxation & Lock-in]`, `[Riskometer & Benchmark]`).
* **Target Chunk Size**: ~300 to 500 characters (approx. 60–100 words), ensuring high factual specificity.
* **Overlap**: 50 characters (preserves boundary sentences).
* **Metadata per chunk**: `scheme_name`, `category`, `source_url`, `section_title`, `chunk_id`, `updated_at`.

### Verification Criteria
* Check `data/raw/` contains 5 text files.
* Open `data/chunks/chunks.txt` and verify:
  1. Each chunk is numbered and shows character count.
  2. Headers, exit load rules, and expense ratios are not split across awkward token cuts.
  3. Total chunk count is reported in terminal output (41 chunks).

---

## Phase 3: Embedding Generation & ChromaDB Persistence

### Objective
Embed all generated chunks with `sentence-transformers/all-MiniLM-L6-v2` and persist them into a ChromaDB collection on disk, ensuring fast retrieval without repeated ingestion runs.

### Files Created
* `src/ingest/embedder.py`: Handles local sentence-transformer batch embeddings (384 dimensions).
* `src/ingest/run.py`: Master ingestion pipeline orchestrating Load -> Chunk -> Embed -> ChromaDB Store.
* Output file generated:
  * `data/embeddings_preview.txt`: Inspectable text file listing the first 5 generated embeddings (first 10 vector dimensions each).
  * `chroma_db/`: Persistent directory containing the vector collection.

### What This Phase Does
1. Reads all chunks from `src/ingest/chunker.py`.
2. Encodes each chunk text into a 384-dimensional vector.
3. Upserts chunks, embeddings, and metadata into a persistent ChromaDB collection (`hdfc_mf_schemes`).
4. Dumps `data/embeddings_preview.txt` for verification.

### Verification Criteria
* Run: `python -m src.ingest.run`
* Output verifies: Number of vectors added to ChromaDB matches total chunk count (41).
* Inspect `data/embeddings_preview.txt` to confirm actual floating-point embeddings are recorded.
* Re-running the script verifies that ChromaDB detects existing records and does not duplicate data.

---

## Phase 4: Financial Safety Guardrails & Intent Filter

### Objective
Implement deterministic safety guardrails before query execution: refuse personalized investment advice, block PII, detect return predictions, and reject completely out-of-domain queries.

### Files Created
* `src/rag/guardrails.py`: Core rule-based and regex-based guardrail engine.

### What This Phase Does
1. **Advisory Refusal Filter**: Detects prompts asking "Should I buy?", "Is it good to invest?", "Which one will give more return?", "Best fund for 5 years?", etc.
   - Refusal message: *"I am a facts-only assistant and cannot provide investment advice or recommendations. You can review the factual scheme documents here: [Link]"*.
2. **PII Redaction / Rejection**: Scans for PAN cards (`[A-Z]{5}[0-9]{4}[A-Z]`), Aadhaar numbers, phone numbers, and bank details. Rejects with an immediate privacy alert.
3. **No-Hallucination Fallback**: If retrieved context similarity distance is too high (low relevance), mandates an explicit fallback: *"I don't have verified documentation to answer this question. Please refer to official AMC disclosures."*

---

## Phase 5: Query Rewriting, Vector Retrieval & Grounded Groq Generation

### Objective
Assemble the online query pipeline: rewrite follow-ups using conversation history, embed the rewritten query using `all-MiniLM-L6-v2`, retrieve top-$k$ chunks from ChromaDB, format a grounded system prompt, and invoke Groq LLM to generate an answer $\le 3$ sentences with citations.

### Files Created
* `src/rag/memory.py`: Sliding window of the last 10 messages; context-aware query rewriter.
* `src/rag/vector_store.py`: ChromaDB query interface with Intent Reranking returning top-$k$ chunks and metadata.
* `src/rag/pipeline.py`: Orchestrator linking Guardrails -> Memory -> Retrieval -> Groq LLM.
* `cli.py`: Interactive command-line test script to inspect queries, retrieved chunks, and generated answers.

---

## Phase 6: Web UI & Render Cloud Deployment

### Objective
Deliver a responsive, Groww-inspired fintech interface featuring message history, source drawer, prompt chips, and ready-to-deploy Render configuration.

### Files Created
* `src/main.py`: FastAPI server serving endpoints and static web UI.
* `src/templates/index.html`: Premium Groww-styled single-page chat UI.
* `src/static/css/style.css`: Minimalist fintech styling.
* `src/static/js/app.js`: Interactive client logic with source links and evidence drawer.
* `src/app.py`: Streamlit fallback interface.
* `README.md`: Complete documentation covering product overview, architecture diagram, setup commands, scope, test results, and Render deployment specifications.
* `render.yaml` & `Dockerfile`: Exact Build and Start commands for one-click deployment.

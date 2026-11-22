# Product Requirements Document (PRD)

## Product Name: Shinri (真理) - Mutual Fund Facts Assistant
*Demonstration Context: Groww | NextLeap PM Fellowship Milestone 4*

---

## 1. Executive Summary & Goal
**Shinri** is a verifiable, retrieval-augmented generation (RAG) conversational assistant designed for the Groww mutual fund platform context. Its sole purpose is to answer factual, scheme-specific, and terminology-related questions regarding mutual funds using strictly verified public documentation (HDFC Mutual Fund direct-growth schemes). 

Shinri eliminates misinformation and hallucinations by adhering to a **zero-speculation, facts-only mandate**: every factual claim is grounded in retrieved chunks with clickable citations, keeping answers under three sentences, and explicitly refusing any personalized investment advice or return projections.

---

## 2. Target Users & Problem Statement

### User Personas
1. **First-time Retail Investor (Rohan, 24)**: Needs simple, jargon-free explanations of terms like "Expense Ratio", "Lock-in Period", and "Exit Load" before putting his first ₹500 into an SIP.
2. **Informed DIY Investor (Priya, 31)**: Comparing operational metrics across schemes (e.g., minimum SIP amount, benchmark indices, fund manager names, exit load slabs).
3. **Customer Support / Operations Team**: Needs an instant, authoritative reference tool to answer repetitive investor queries backed by official source links.

### The Problem
Mutual fund scheme characteristics are buried inside 80+ page Scheme Information Documents (SIDs), Key Information Memorandums (KIMs), and dense factsheets. Retail investors either struggle to find these facts or fall prey to unverified third-party advice and social media rumors.

---

## 3. Scope & Scheme Corpus

### AMC In Scope
**HDFC Asset Management Company (AMC)**

### 5 Evaluated Schemes (Direct - Growth Plans)
1. **Large Cap**: HDFC Large Cap Fund Direct Plan - Growth  
   *URL*: `https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth`
2. **Flexi Cap**: HDFC Flexi Cap Fund Direct Plan - Growth  
   *URL*: `https://groww.in/mutual-funds/hdfc-equity-fund-direct-growth`
3. **ELSS (Tax Saver)**: HDFC ELSS Tax saver Fund Direct Plan - Growth  
   *URL*: `https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth`
4. **Small Cap**: HDFC Small Cap Fund Direct Plan - Growth  
   *URL*: `https://groww.in/mutual-funds/hdfc-small-cap-fund-direct-growth`
5. **Balanced Advantage (Hybrid)**: HDFC Balanced Advantage Fund Direct Plan - Growth  
   *URL*: `https://groww.in/mutual-funds/hdfc-balanced-advantage-fund-direct-growth`

---

## 4. Feature Specifications

### In-Scope Features
* **Natural Language Fact Retrieval**: Accurate answers on expense ratio, exit load, minimum SIP/lump sum, lock-in period, riskometer rating, benchmark index, and capital-gains statement download steps.
* **Strict Evidence Grounding**: Answers synthesized strictly from retrieved top-$k$ context chunks; no outside knowledge hallucination.
* **Source Attribution & Citations**: Every factual response provides a direct, verified citation link and a "Last updated from sources: [Date]" timestamp.
* **Conciseness**: Answers are strictly $\le 3$ sentences, followed by the source link.
* **Non-Advisory Guardrail**: Deterministic refusal of opinionated, speculative, or advisory queries ("Which fund should I buy?", "Is HDFC Small Cap good for 5 years?", "Will I get 15% return?") with an educational disclaimer.
* **Out-of-Domain Refusal**: Clear, polite acknowledgment ("I don't have verified documentation to answer this question") when context is missing.
* **Conversational Memory (10 turns)**: Query rewriting to support natural follow-up questions (e.g., "What is its exit load?" referring to previously discussed scheme).
* **Privacy & Zero-PII Compliance**: Immediate rejection and non-retention if a user enters PAN, Aadhaar, bank account, phone number, or OTP.

### Out-of-Scope Features
* No real-time stock/NAV trading or transaction execution.
* No portfolio rebalancing, personalized risk profiling, or investment advice.
* No returns forecasting or comparative returns computation.
* No third-party blog or unverified social media ingestion.

---

## 5. Example User Prompts

| Category | Example Question | Expected System Behavior |
|---|---|---|
| **Factual - Expense Ratio** | "What is the expense ratio of HDFC Small Cap Direct Growth?" | Retrieves HDFC Small Cap factsheet chunk, outputs exact expense ratio $\le 3$ sentences + Groww source link. |
| **Factual - Lock-in** | "Does HDFC ELSS Tax Saver have any lock-in period?" | Confirms 3-year statutory lock-in period under Section 80C + Groww citation link. |
| **Factual - Exit Load** | "What is the exit load for HDFC Large Cap Fund?" | States exit load percentage and duration threshold + source link. |
| **Follow-up / Memory** | "And what is the minimum SIP for it?" | Resolves "it" as HDFC Large Cap via memory rewriter, answers minimum SIP + source link. |
| **Advisory (Refusal)** | "Should I invest ₹10,000 in HDFC Flexi Cap or HDFC Small Cap?" | Polite refusal: "I am a facts-only assistant and cannot provide investment advice or recommendations. You can review the factual scheme documents here: [Link]". |
| **Out-of-Corpus** | "What is the expense ratio of SBI Bluechip Fund?" | "I do not have verified documents for SBI Bluechip in my current knowledge base (restricted to HDFC AMC schemes). Please consult official AMC disclosures." |

---

## 6. Success Criteria & Metrics

1. **Groundedness / Faithfulness**: 100% of generated facts must trace directly to retrieved chunks (0 hallucinated numbers/percentages).
2. **Citation Rate**: 100% of factual answers must include the exact source URL.
3. **Refusal Accuracy**: 100% rejection rate on advisory, opinionated, or PII-laden queries.
4. **Latency**: End-to-end response generation $< 2.5$ seconds using local embeddings + Groq fast inference.
5. **Persistence**: Ingestion executes once; vector database persists reliably across application restarts.

---

## 7. Constraints & Deployment
* **Free-Tier Tools Only**: `sentence-transformers/all-MiniLM-L6-v2` runs locally (no embedding API charges). Groq Cloud free tier handles LLM inference.
* **Local & Cloud Deployable**: Works out-of-the-box on local machines via Streamlit and pre-configured for one-click deployment on Render Web Services.

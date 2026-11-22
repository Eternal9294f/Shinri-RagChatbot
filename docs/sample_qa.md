# 📋 Shinri (真理) — Sample Q&A Deliverable
*NextLeap Product Management Fellowship &bull; Milestone 4 Portfolio Submission*

**Project:** **_Shinri_** (Mutual Funds Facts Chatbot &bull; Groww Context)  
**Corpus:** 5 HDFC Mutual Fund Schemes (Direct - Growth Plans)  
**Corpus Date / Last Updated:** 27 September 2026  
**Disclaimer Snippet:** *"Facts-only assistance. No personalized investment advice or return projections. Last updated from sources: 27 September 2026."*

---

## 1. Scheme Expense Ratio Query
- **User Query:** *"What is the expense ratio of HDFC Small Cap Fund Direct Growth?"*
- **Shinri Response:**  
  The expense ratio of HDFC Small Cap Fund Direct Plan - Growth is **0.68%** (inclusive of GST). This is the direct plan fee charged on the scheme assets.
- **Source Citation:** [https://groww.in/mutual-funds/hdfc-small-cap-fund-direct-growth](https://groww.in/mutual-funds/hdfc-small-cap-fund-direct-growth)
- **Status:** Verified from official disclosures.

---

## 2. Statutory Lock-in & Tax Benefit Query
- **User Query:** *"What is the mandatory lock-in period for HDFC ELSS Tax Saver Fund?"*
- **Shinri Response:**  
  HDFC ELSS Tax saver Fund has a mandatory statutory lock-in period of **3 years (36 months)** from the date of unit allotment. For SIP investments, each individual monthly SIP installment is locked in for 3 years from its specific allotment date.
- **Source Citation:** [https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth](https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth)
- **Status:** Verified from official disclosures.

---

## 3. Exit Load Slabs Query
- **User Query:** *"What is the exit load for HDFC Large Cap Fund?"*
- **Shinri Response:**  
  The exit load for HDFC Large Cap Fund Direct Plan - Growth is **1.00%** if redeemed or switched out within 1 year (365 days) from allotment. If redeemed after 1 year, the exit load is **Nil (0%)**.
- **Source Citation:** [https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth](https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth)
- **Status:** Verified from official disclosures.

---

## 4. Minimum SIP & Investment Threshold Query
- **User Query:** *"What is the minimum monthly SIP for HDFC Flexi Cap Fund?"*
- **Shinri Response:**  
  For HDFC Flexi Cap Fund Direct Plan - Growth, the minimum monthly SIP amount is **Rs 100**. The minimum lumpsum investment is also Rs 100.
- **Source Citation:** [https://groww.in/mutual-funds/hdfc-equity-fund-direct-growth](https://groww.in/mutual-funds/hdfc-equity-fund-direct-growth)
- **Status:** Verified from official disclosures.

---

## 5. Benchmark & Riskometer Rating Query
- **User Query:** *"What is the benchmark and risk rating of HDFC Balanced Advantage Fund?"*
- **Shinri Response:**  
  The benchmark for HDFC Balanced Advantage Fund Direct Plan - Growth is the **NIFTY 50 Hybrid Composite debt 50:50 Index**. According to the SEBI riskometer, the scheme is rated as **Very High Risk**.
- **Source Citation:** [https://groww.in/mutual-funds/hdfc-balanced-advantage-fund-direct-growth](https://groww.in/mutual-funds/hdfc-balanced-advantage-fund-direct-growth)
- **Status:** Verified from official disclosures.

---

## 6. Account Statement & Capital Gains Download Guide
- **User Query:** *"How do I download my capital gains statement on Groww?"*
- **Shinri Response:**  
  To download your mutual fund statement on Groww, navigate to **Profile > Reports > Capital Gains / P&L Statement** or Mutual Fund Holding Statement. You can also request an instant Consolidated Account Statement (CAS) via CAMS or the HDFC Mutual Fund investor website.
- **Source Citation:** [https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth](https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth)
- **Status:** Verified procedural guide.

---

## 7. Conversational Follow-up (Context Disambiguation)
- **User Turn 1:** *"Tell me about HDFC ELSS Tax Saver exit load"*  
  **Shinri Turn 1:** *"The exit load for HDFC ELSS Tax saver Fund is Nil (0%) because units are subject to a mandatory 3-year lock-in."*
- **User Turn 2 (Follow-up):** *"What about its minimum SIP?"*
- **Shinri Response:**  
  For HDFC ELSS Tax saver Fund Direct Plan - Growth, the minimum monthly SIP amount is **Rs 500**.
- **Source Citation:** [https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth](https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth)
- **Status:** Context properly maintained across multi-turn sliding memory.

---

## 8. Hinglish Colloquial Query
- **User Query:** *"HDFC Small Cap ka expense ratio kitna hai?"*
- **Shinri Response:**  
  The expense ratio of HDFC Small Cap Fund Direct Plan - Growth is **0.68%** (inclusive of GST).
- **Source Citation:** [https://groww.in/mutual-funds/hdfc-small-cap-fund-direct-growth](https://groww.in/mutual-funds/hdfc-small-cap-fund-direct-growth)
- **Status:** Verified retrieval under informal mixed-language phrasing.

---

## 9. Non-Advisory Guardrail Interception (Financial Advice Refusal)
- **User Query:** *"Should I invest in HDFC Small Cap today for high returns?"*
- **Shinri Response:**  
  *I am a facts-only assistant and cannot provide personalized investment advice, recommendations, or return projections. You can review official scheme documents and factsheets to evaluate your investments.*
- **Source Citation:** [https://groww.in/mutual-funds](https://groww.in/mutual-funds)
- **Status:** Guardrail triggered (`ADVISORY_REFUSAL`). Zero opinion or speculation provided.

---

## 10. PII Detection & Privacy Refusal
- **User Query:** *"My PAN is ABCDE1234F, show my current balance."*
- **Shinri Response:**  
  *For your security, Shinri does not accept or process PAN numbers. Please ask your mutual fund scheme questions without sharing personal identification details.*
- **Source Citation:** [https://groww.in/mutual-funds](https://groww.in/mutual-funds)
- **Status:** Guardrail triggered (`PII_REFUSAL`). Immediate privacy protection.

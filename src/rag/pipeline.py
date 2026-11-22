"""Core RAG Pipeline: Guardrails -> Memory -> ChromaDB Retrieval -> Grounded Groq Generation."""
import os
import re
from typing import Dict, Any, List, Optional
from src.config import GROQ_API_KEY, GROQ_MODEL
from src.rag.guardrails import GuardrailEngine
from src.rag.memory import ConversationMemory
from src.rag.vector_store import VectorStore


SYSTEM_PROMPT = """You are Shinri (真理), a facts-only mutual fund information assistant for HDFC schemes on Groww.
Your purpose is to answer user questions using ONLY the verified facts in the provided context below.

STRICT OPERATIONAL RULES:
1. Keep your answer concise: MAXIMUM 3 SENTENCES.
2. Rely strictly on the context. If the context does not contain the answer, say:
   "I don't have verified documentation to answer this question in my current knowledge base."
3. NEVER provide personalized investment advice, recommendations, or predict future returns.
4. Include exactly ONE official source URL from the context at the end of your answer.
5. End with the line: "Last updated from sources: 27 September 2026."

RETRIEVED CONTEXT EVIDENCE:
{context}
"""


class ShinriRAGPipeline:
    """End-to-end RAG orchestrator for Shinri."""

    def __init__(self):
        self.memory = ConversationMemory(max_history=10)

    def extract_direct_factual_answer(self, query: str, top_chunk: Dict[str, Any]) -> str:
        """Deterministic extractor used as fallback when LLM API key is not configured."""
        details_text = top_chunk["text"]
        url = top_chunk["metadata"]["url"]
        scheme = top_chunk["metadata"]["scheme_name"]
        section = top_chunk["metadata"]["section"]

        # Parse 'Details:' from the chunk
        m = re.search(r"Details:\s*(.+?)(?:\s*Source:|$)", details_text, re.DOTALL)
        content = m.group(1).strip() if m else details_text.strip()
        
        # Take up to 2-3 sentences
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", content) if s.strip()]
        selected = " ".join(sentences[:2])
        if not selected.endswith("."):
            selected += "."

        return (
            f"{selected} "
            f"Source: {url}\n"
            f"Last updated from sources: 27 September 2026."
        )

    def generate_with_groq(self, query: str, context_text: str, source_url: str) -> str:
        """Invokes Groq LLM with strictly grounded prompt."""
        try:
            from groq import Groq
            client = Groq(api_key=GROQ_API_KEY)

            prompt = SYSTEM_PROMPT.format(context=context_text)
            response = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": query}
                ],
                temperature=0.0,
                max_tokens=250
            )
            raw_answer = response.choices[0].message.content.strip()

            # Ensure source URL is present
            if source_url not in raw_answer:
                raw_answer += f"\nSource: {source_url}"
            if "Last updated from sources" not in raw_answer:
                raw_answer += "\nLast updated from sources: 27 September 2026."

            return raw_answer
        except Exception as e:
            # Fallback to local grounded extraction if Groq fails or API key is absent
            return None

    def query(self, user_query: str) -> Dict[str, Any]:
        """
        Executes the full RAG pipeline for a user question.
        """
        clean_query = user_query.strip()
        if not clean_query:
            return {
                "answer": "Please ask a question about the supported HDFC mutual fund schemes.",
                "sources": [],
                "retrieved_chunks": [],
                "rewritten_query": user_query,
                "guardrail_triggered": False
            }

        # Step 1: Run Guardrail Checks (PII & Financial Advice)
        safety = GuardrailEngine.check_query_safety(clean_query)
        if not safety["allowed"]:
            self.memory.add_message("user", clean_query)
            self.memory.add_message("assistant", safety["message"])
            return {
                "answer": safety["message"],
                "sources": ["https://groww.in/mutual-funds"],
                "retrieved_chunks": [],
                "rewritten_query": clean_query,
                "guardrail_triggered": True,
                "guardrail_reason": safety["reason"]
            }

        # Step 2: Contextual Query Rewriting using Conversation Memory
        rewritten_q = self.memory.rewrite_query(clean_query)

        # Step 3: Semantic Vector Retrieval from ChromaDB
        retrieved = VectorStore.similarity_search(rewritten_q, top_k=3)

        if not retrieved or retrieved[0]["distance"] > 1.45:
            fallback_answer = (
                "I don't have verified documentation to answer this question in my current knowledge base. "
                "Please refer to official AMC disclosures: https://groww.in/mutual-funds.\n"
                "Last updated from sources: 27 September 2026."
            )
            self.memory.add_message("user", clean_query)
            self.memory.add_message("assistant", fallback_answer)
            return {
                "answer": fallback_answer,
                "sources": ["https://groww.in/mutual-funds"],
                "retrieved_chunks": retrieved,
                "rewritten_query": rewritten_q,
                "guardrail_triggered": False
            }

        # Step 4: Build Context
        context_blocks = []
        for i, r in enumerate(retrieved, start=1):
            context_blocks.append(f"[Chunk {i}] ({r['metadata']['scheme_name']} - {r['metadata']['section']}):\n{r['text']}")
        full_context = "\n\n".join(context_blocks)
        primary_source_url = retrieved[0]["metadata"]["url"]

        # Step 5: Answer Generation (Groq LLM or deterministic fallback)
        answer = None
        if GROQ_API_KEY and GROQ_API_KEY.strip() and "your_groq_api_key" not in GROQ_API_KEY:
            answer = self.generate_with_groq(rewritten_q, full_context, primary_source_url)

        if not answer:
            answer = self.extract_direct_factual_answer(rewritten_q, retrieved[0])

        # Step 6: Record in Memory
        self.memory.add_message("user", clean_query)
        self.memory.add_message("assistant", answer)

        return {
            "answer": answer,
            "sources": [primary_source_url],
            "retrieved_chunks": retrieved,
            "rewritten_query": rewritten_q,
            "guardrail_triggered": False
        }

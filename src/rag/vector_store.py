"""ChromaDB vector store query interface."""
from typing import List, Dict, Any, Optional
import chromadb
from src.config import CHROMA_DB_DIR, CHROMA_COLLECTION_NAME, TOP_K_CHUNKS
from src.ingest.embedder import LocalEmbedder


SCHEME_SLUG_MAP = {
    "large cap": "hdfc-large-cap-fund-direct-growth",
    "top 100": "hdfc-large-cap-fund-direct-growth",
    "flexi cap": "hdfc-equity-fund-direct-growth",
    "equity fund": "hdfc-equity-fund-direct-growth",
    "elss": "hdfc-elss-tax-saver-fund-direct-plan-growth",
    "tax saver": "hdfc-elss-tax-saver-fund-direct-plan-growth",
    "small cap": "hdfc-small-cap-fund-direct-growth",
    "balanced advantage": "hdfc-balanced-advantage-fund-direct-growth",
    "hybrid": "hdfc-balanced-advantage-fund-direct-growth"
}


INTENT_SECTION_MAP = {
    ("expense ratio", "fees", "charges", "ter"): ["Expense Ratio", "Charges"],
    ("exit load", "exit penalty", "redemption charge"): ["Exit Load"],
    ("lock-in", "lock in", "80c", "lockin"): ["Lock-in", "Mandatory Lock-in"],
    ("sip", "minimum investment", "lumpsum", "minimum sip"): ["Minimum Investment & SIP", "SIP"],
    ("benchmark", "index"): ["Benchmark"],
    ("riskometer", "risk level", "risk"): ["Riskometer"],
    ("statement", "download", "cas", "capital gains"): ["Account Statement", "Statement"],
    ("tax", "taxation", "ltcg", "stcg"): ["Taxation"]
}


class VectorStore:
    """Manages queries and semantic search against persistent ChromaDB."""

    _client = None
    _collection = None

    @classmethod
    def get_collection(cls):
        if cls._collection is None:
            cls._client = chromadb.PersistentClient(path=str(CHROMA_DB_DIR))
            cls._collection = cls._client.get_collection(name=CHROMA_COLLECTION_NAME)
        return cls._collection

    @classmethod
    def detect_scheme_filter(cls, query: str) -> Optional[Dict[str, str]]:
        """Detects whether query targets a specific scheme and creates a metadata filter."""
        lower_q = query.lower()
        for key, slug in SCHEME_SLUG_MAP.items():
            if key in lower_q:
                return {"scheme_slug": slug}
        return None

    @classmethod
    def rerank_by_intent(cls, query: str, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Reranks retrieved chunks prioritizing sections that align with intent keywords."""
        lower_q = query.lower()
        matching_sections = []

        for keywords, sections in INTENT_SECTION_MAP.items():
            if any(kw in lower_q for kw in keywords):
                matching_sections.extend(sections)

        if not matching_sections:
            return chunks

        def sort_key(c):
            sec = c["metadata"].get("section", "")
            is_match = any(target.lower() in sec.lower() for target in matching_sections)
            # True comes first, then by distance
            return (0 if is_match else 1, c["distance"])

        return sorted(chunks, key=sort_key)

    @classmethod
    def similarity_search(cls, query: str, top_k: int = TOP_K_CHUNKS) -> List[Dict[str, Any]]:
        """
        Embeds the query using the exact same MiniLM model and retrieves top_k nearest chunks
        with entity metadata filtering when a specific scheme is targeted.
        """
        collection = cls.get_collection()
        query_embedding = LocalEmbedder.embed_query(query)
        where_filter = cls.detect_scheme_filter(query)

        query_kwargs = {
            "query_embeddings": [query_embedding],
            "n_results": top_k,
            "include": ["documents", "metadatas", "distances"]
        }
        if where_filter:
            query_kwargs["where"] = where_filter

        results = collection.query(**query_kwargs)

        retrieved = []
        if results and "documents" in results and results["documents"]:
            docs = results["documents"][0]
            metas = results["metadatas"][0]
            dists = results["distances"][0]

            for i in range(len(docs)):
                retrieved.append({
                    "id": results["ids"][0][i],
                    "text": docs[i],
                    "metadata": metas[i],
                    "distance": float(dists[i])
                })

        return cls.rerank_by_intent(query, retrieved)

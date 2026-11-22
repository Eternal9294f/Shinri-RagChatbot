"""Local embedding model wrapper using sentence-transformers."""
from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
from src.config import EMBEDDING_MODEL_NAME


class LocalEmbedder:
    """Wrapper around sentence-transformers/all-MiniLM-L6-v2."""
    
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            print(f"Loading embedding model: {EMBEDDING_MODEL_NAME}...")
            try:
                cls._instance = SentenceTransformer(EMBEDDING_MODEL_NAME)
            except Exception:
                cls._instance = SentenceTransformer(EMBEDDING_MODEL_NAME, local_files_only=True)
            print("Embedding model loaded successfully.")
        return cls._instance

    @classmethod
    def embed_texts(cls, texts: List[str]) -> List[List[float]]:
        """Encodes a list of text strings into 384-dimensional vector embeddings."""
        model = cls.get_instance()
        embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
        return embeddings.tolist()

    @classmethod
    def embed_query(cls, query: str) -> List[float]:
        """Encodes a single search query string into a 384-dimensional vector."""
        model = cls.get_instance()
        embedding = model.encode(query, convert_to_numpy=True, show_progress_bar=False)
        return embedding.tolist()

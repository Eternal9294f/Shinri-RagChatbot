"""Master ingestion pipeline: Chunks -> Embeddings -> Persistent ChromaDB."""
from pathlib import Path
import chromadb
from chromadb.config import Settings
from src.config import (
    CHROMA_DB_DIR,
    CHROMA_COLLECTION_NAME,
    EMBEDDINGS_PREVIEW_FILE
)
from src.ingest.scraper import save_raw_documents
from src.ingest.chunker import run_chunking
from src.ingest.embedder import LocalEmbedder


def run_ingestion_pipeline():
    print("=" * 70)
    print("Starting Shinri Ingestion Pipeline...")
    print("=" * 70)

    # Step 1: Save raw documents
    print("[1/4] Normalizing and saving raw scheme documentation...")
    raw_files = save_raw_documents()
    print(f"      Saved {len(raw_files)} raw scheme files.")

    # Step 2: Generate semantic chunks
    print("[2/4] Chunking scheme documents...")
    chunks = run_chunking()
    print(f"      Generated {len(chunks)} chunks.")

    # Step 3: Compute embeddings locally
    print("[3/4] Generating local MiniLM embeddings (384-dimensions)...")
    texts = [c["text"] for c in chunks]
    ids = [c["id"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]
    embeddings = LocalEmbedder.embed_texts(texts)
    print(f"      Computed {len(embeddings)} vector embeddings.")

    # Step 4: Write embeddings preview
    print(f"[4/4] Writing embeddings preview to {EMBEDDINGS_PREVIEW_FILE.name}...")
    preview_lines = [
        "=" * 80,
        "SHINRI MUTUAL FUND RAG - EMBEDDINGS PREVIEW",
        "Model: sentence-transformers/all-MiniLM-L6-v2 (384 dimensions)",
        f"Total Vectors: {len(embeddings)}",
        "Showing first 5 embeddings (first 10 dimensions each):",
        "=" * 80,
        ""
    ]
    for i in range(min(5, len(embeddings))):
        emb_slice = embeddings[i][:10]
        preview_lines.append(f"Vector #{ids[i]} ({metadatas[i]['scheme_name']} - {metadatas[i]['section']}):")
        formatted_dims = ", ".join(f"{val:+.6f}" for val in emb_slice)
        preview_lines.append(f"  Dimensions [0..9]: [{formatted_dims}, ...]")
        preview_lines.append("")

    EMBEDDINGS_PREVIEW_FILE.write_text("\n".join(preview_lines), encoding="utf-8")

    # Step 5: Store in persistent ChromaDB
    print(f"Storing vectors in persistent ChromaDB at: {CHROMA_DB_DIR}...")
    CHROMA_DB_DIR.mkdir(parents=True, exist_ok=True)
    chroma_client = chromadb.PersistentClient(path=str(CHROMA_DB_DIR))

    # Reset or get collection
    try:
        chroma_client.delete_collection(name=CHROMA_COLLECTION_NAME)
        print(f"Cleaned previous collection '{CHROMA_COLLECTION_NAME}'.")
    except Exception:
        pass

    collection = chroma_client.create_collection(
        name=CHROMA_COLLECTION_NAME,
        metadata={"description": "HDFC Mutual Fund schemes on Groww"}
    )

    collection.add(
        ids=ids,
        documents=texts,
        metadatas=metadatas,
        embeddings=embeddings
    )

    # Verification of persistence
    stored_count = collection.count()
    print("=" * 70)
    print(f"SUCCESS: Ingestion complete!")
    print(f"Total vectors stored in ChromaDB: {stored_count}")
    print(f"ChromaDB persistent directory: {CHROMA_DB_DIR}")
    print(f"Embeddings preview saved: {EMBEDDINGS_PREVIEW_FILE}")
    print("=" * 70)
    return stored_count


if __name__ == "__main__":
    run_ingestion_pipeline()

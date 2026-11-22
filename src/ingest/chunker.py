"""Domain-aware semantic chunker for mutual fund scheme documentation."""
from pathlib import Path
from typing import List, Dict, Any
from src.config import RAW_DATA_DIR, CHUNKS_FILE, HDFC_SCHEMES
from src.ingest.scraper import SCHEME_DOCUMENTATION


def create_semantic_chunks() -> List[Dict[str, Any]]:
    """
    Parses scheme sections and creates semantic factual chunks.
    Each chunk contains a standalone factual domain with rich metadata.
    """
    chunks = []
    chunk_counter = 1

    for slug, scheme_data in SCHEME_DOCUMENTATION.items():
        scheme_name = scheme_data["scheme_name"]
        category = scheme_data["category"]
        url = scheme_data["url"]
        benchmark = scheme_data["benchmark"]
        riskometer = scheme_data["riskometer"]
        amc = scheme_data["amc"]

        for section_title, content in scheme_data["sections"].items():
            # Construct rich chunk text including entity anchoring
            chunk_text = (
                f"Scheme: {scheme_name}\n"
                f"Category: {category}\n"
                f"Topic: {section_title}\n"
                f"Details: {content}\n"
                f"Source: {url}"
            )

            chunk_meta = {
                "chunk_id": f"chunk_{chunk_counter}",
                "scheme_name": scheme_name,
                "scheme_slug": slug,
                "category": category,
                "section": section_title,
                "benchmark": benchmark,
                "riskometer": riskometer,
                "amc": amc,
                "url": url,
                "char_count": len(chunk_text),
                "as_of_date": "2026-09-27"
            }

            chunks.append({
                "id": f"chunk_{chunk_counter}",
                "text": chunk_text,
                "metadata": chunk_meta
            })
            chunk_counter += 1

    return chunks


def export_chunks_to_file(chunks: List[Dict[str, Any]], output_path: Path):
    """Exports all chunks to an inspectable, human-readable text file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    lines = [
        "=" * 80,
        "SHINRI MUTUAL FUND RAG - CHUNKS INSPECTION FILE",
        f"Total Chunks: {len(chunks)}",
        "Chunking Strategy: Semantic Section Chunking with Entity Anchoring",
        "Source Corpus: 5 HDFC Direct-Growth Schemes on Groww",
        "=" * 80,
        ""
    ]

    for chunk in chunks:
        meta = chunk["metadata"]
        lines.append(f"--- CHUNK #{meta['chunk_id']} ---")
        lines.append(f"Scheme: {meta['scheme_name']}")
        lines.append(f"Category: {meta['category']}")
        lines.append(f"Section: {meta['section']}")
        lines.append(f"Source URL: {meta['url']}")
        lines.append(f"Character Count: {meta['char_count']}")
        lines.append("Content:")
        lines.append(chunk["text"])
        lines.append("-" * 80)
        lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")


def run_chunking() -> List[Dict[str, Any]]:
    """Runs the chunking pipeline and writes chunks.txt."""
    chunks = create_semantic_chunks()
    export_chunks_to_file(chunks, CHUNKS_FILE)
    return chunks


if __name__ == "__main__":
    chunks = run_chunking()
    print(f"Successfully generated {len(chunks)} semantic chunks.")
    print(f"Chunks inspection file written to: {CHUNKS_FILE}")

"""Configuration settings and constants for Shinri MF RAG."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Allow offline Hugging Face loading only if explicitly enabled; otherwise allow online download for clean deployments (e.g. Render)
if os.getenv("HF_HUB_OFFLINE", "0") == "1":
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
else:
    os.environ.pop("HF_HUB_OFFLINE", None)
    os.environ.pop("TRANSFORMERS_OFFLINE", None)

# Base paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
CHUNKS_DIR = DATA_DIR / "chunks"
CHUNKS_FILE = CHUNKS_DIR / "chunks.txt"
EMBEDDINGS_PREVIEW_FILE = DATA_DIR / "embeddings_preview.txt"
SOURCES_CSV = DATA_DIR / "sources.csv"
CHROMA_DB_DIR = PROJECT_ROOT / "chroma_db"

# RAG Configuration
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIM = 384
CHROMA_COLLECTION_NAME = "hdfc_mf_schemes"
TOP_K_CHUNKS = 4

# Groq LLM Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# Source Schemes Catalog (Groww URLs)
HDFC_SCHEMES = [
    {
        "id": "hdfc_large_cap",
        "name": "HDFC Large Cap Fund Direct Plan - Growth",
        "category": "Large Cap",
        "url": "https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth",
        "benchmark": "NIFTY 100 TRI",
        "slug": "hdfc-large-cap-fund-direct-growth"
    },
    {
        "id": "hdfc_flexi_cap",
        "name": "HDFC Flexi Cap Fund Direct Plan - Growth",
        "category": "Flexi Cap",
        "url": "https://groww.in/mutual-funds/hdfc-equity-fund-direct-growth",
        "benchmark": "NIFTY 500 TRI",
        "slug": "hdfc-equity-fund-direct-growth"
    },
    {
        "id": "hdfc_elss_tax_saver",
        "name": "HDFC ELSS Tax saver Fund Direct Plan - Growth",
        "category": "ELSS (Tax Saver)",
        "url": "https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth",
        "benchmark": "NIFTY 500 TRI",
        "slug": "hdfc-elss-tax-saver-fund-direct-plan-growth"
    },
    {
        "id": "hdfc_small_cap",
        "name": "HDFC Small Cap Fund Direct Plan - Growth",
        "category": "Small Cap",
        "url": "https://groww.in/mutual-funds/hdfc-small-cap-fund-direct-growth",
        "benchmark": "BSE 250 SmallCap TRI",
        "slug": "hdfc-small-cap-fund-direct-growth"
    },
    {
        "id": "hdfc_balanced_advantage",
        "name": "HDFC Balanced Advantage Fund Direct Plan - Growth",
        "category": "Balanced Advantage (Hybrid)",
        "url": "https://groww.in/mutual-funds/hdfc-balanced-advantage-fund-direct-growth",
        "benchmark": "NIFTY 50 Hybrid Composite debt 50:50 Index",
        "slug": "hdfc-balanced-advantage-fund-direct-growth"
    }
]

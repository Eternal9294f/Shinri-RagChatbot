"""FastAPI web server and API endpoints for Shinri MF RAG."""
import time
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

from src.config import PROJECT_ROOT, HDFC_SCHEMES
from src.rag.pipeline import ShinriRAGPipeline
from src.ingest.embedder import LocalEmbedder
from src.rag.vector_store import VectorStore


# Initialize RAG Pipeline singleton
pipeline = ShinriRAGPipeline()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Pre-warm asynchronously in background thread so port binds instantly on Render
    import threading
    def _warmup():
        print("Pre-warming embedding model and vector store in background...")
        try:
            LocalEmbedder.get_instance()
            VectorStore.get_collection()
            VectorStore.similarity_search("HDFC", top_k=1)
            print("Pre-warming complete. Shinri is ready to serve queries.")
        except Exception as e:
            print(f"Warmup notice: {e}")

    threading.Thread(target=_warmup, daemon=True).start()
    yield


app = FastAPI(
    title="Shinri — Mutual Fund Facts Assistant",
    description="Grounded, verifiable RAG assistant for HDFC mutual fund schemes on Groww.",
    version="1.0.0",
    lifespan=lifespan
)

# Mount static files
static_dir = PROJECT_ROOT / "src" / "static"
static_dir.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


class ChatRequest(BaseModel):
    query: str


class ChatResponse(BaseModel):
    query: str
    rewritten_query: str
    answer: str
    sources: list
    retrieved_chunks: list
    guardrail_triggered: bool
    latency_ms: float


@app.get("/", response_class=HTMLResponse)
async def serve_index():
    template_path = PROJECT_ROOT / "src" / "templates" / "index.html"
    if template_path.exists():
        return HTMLResponse(content=template_path.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>Shinri API is running. index.html template not found.</h1>")


@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    start_time = time.time()
    try:
        result = pipeline.query(request.query)
        elapsed_ms = round((time.time() - start_time) * 1000, 1)

        return {
            "query": request.query,
            "rewritten_query": result.get("rewritten_query", request.query),
            "answer": result["answer"],
            "sources": result.get("sources", []),
            "retrieved_chunks": result.get("retrieved_chunks", []),
            "guardrail_triggered": result.get("guardrail_triggered", False),
            "guardrail_reason": result.get("guardrail_reason", None),
            "latency_ms": elapsed_ms
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        elapsed_ms = round((time.time() - start_time) * 1000, 1)
        return {
            "query": request.query,
            "rewritten_query": request.query,
            "answer": "I'm temporarily experiencing an issue retrieving the documentation. Please try again in a few moments.",
            "sources": ["https://groww.in/mutual-funds"],
            "retrieved_chunks": [],
            "guardrail_triggered": False,
            "latency_ms": elapsed_ms
        }


@app.post("/api/clear")
async def clear_memory_endpoint():
    pipeline.memory.clear()
    return {"status": "cleared", "message": "Conversation history reset."}


@app.get("/api/schemes")
async def get_schemes_endpoint():
    return {"schemes": HDFC_SCHEMES}


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "product": "Shinri",
        "vector_store": "ChromaDB",
        "embedding_model": "all-MiniLM-L6-v2",
        "schemes_indexed": len(HDFC_SCHEMES)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main.py:app", host="0.0.0.0", port=8000, reload=True)

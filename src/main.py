"""FastAPI web server and API endpoints for Shinri MF RAG."""
import time
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

from src.config import PROJECT_ROOT, HDFC_SCHEMES
from src.rag.pipeline import ShinriRAGPipeline

app = FastAPI(
    title="Shinri (真理) - Mutual Fund Facts Assistant",
    description="Grounded, verifiable RAG assistant for HDFC mutual fund schemes on Groww.",
    version="1.0.0"
)

# Mount static files
static_dir = PROJECT_ROOT / "src" / "static"
static_dir.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Initialize RAG Pipeline singleton
pipeline = ShinriRAGPipeline()


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
        "product": "Shinri (真理)",
        "vector_store": "ChromaDB",
        "embedding_model": "all-MiniLM-L6-v2",
        "schemes_indexed": len(HDFC_SCHEMES)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main.py:app", host="0.0.0.0", port=8000, reload=True)

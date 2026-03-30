"""
main.py — Production RAG API
FastAPI + Qdrant + BGE Embeddings + Claude

Run locally:   uvicorn main:app --reload
Run via Docker: docker-compose up --build
API docs:       http://localhost:8000/docs
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

load_dotenv()

from src.rag import RAGPipeline
from src.chunker import chunk_documents
from src.models import (
    IngestRequest, IngestResponse,
    BatchIngestRequest, BatchIngestResponse,
    QueryRequest, QueryResponse,
    HealthResponse,
)

# ─── App Lifecycle ────────────────────────────────────────

rag: RAGPipeline = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize the RAG pipeline on startup."""
    global rag
    print("Initializing RAG pipeline...")
    rag = RAGPipeline()
    print("Ready.")
    yield
    print("Shutting down.")

# ─── App Setup ────────────────────────────────────────────

app = FastAPI(
    title="Production RAG API",
    description="Retrieval-Augmented Generation API — ingest documents, ask questions, get grounded answers with citations.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Routes ──────────────────────────────────────────────

@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """Check API health and collection stats."""
    try:
        stats = rag.collection_stats()
        return HealthResponse(status="healthy", **stats)
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unavailable: {e}")


@app.post("/ingest", response_model=IngestResponse, tags=["Ingestion"])
async def ingest_document(request: IngestRequest):
    """
    Ingest a document into the vector store.

    The document is automatically chunked, embedded, and stored.
    Returns the number of chunks created and their IDs.
    """
    try:
        chunks = chunk_documents(
            text=request.text,
            source=request.source,
            strategy=request.chunk_strategy,
            chunk_size=request.chunk_size,
            chunk_overlap=request.chunk_overlap,
        )

        if not chunks:
            raise HTTPException(status_code=400, detail="Document produced no valid chunks")

        # Add any extra metadata from request
        if request.metadata:
            for chunk in chunks:
                chunk["metadata"].update(request.metadata)

        point_ids = rag.ingest_batch(chunks)

        return IngestResponse(
            success=True,
            chunks_ingested=len(chunks),
            source=request.source,
            point_ids=point_ids,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {e}")


@app.post("/ingest/batch", response_model=BatchIngestResponse, tags=["Ingestion"])
async def ingest_batch(request: BatchIngestRequest):
    """
    Ingest multiple documents at once.

    More efficient than calling /ingest repeatedly.
    Accepts up to 100 documents per request.
    """
    try:
        total_chunks = 0

        for doc in request.documents:
            chunks = chunk_documents(
                text=doc.text,
                source=doc.source,
                strategy=doc.chunk_strategy,
                chunk_size=doc.chunk_size,
                chunk_overlap=doc.chunk_overlap,
            )
            if doc.metadata:
                for chunk in chunks:
                    chunk["metadata"].update(doc.metadata)

            rag.ingest_batch(chunks)
            total_chunks += len(chunks)

        return BatchIngestResponse(
            success=True,
            total_chunks_ingested=total_chunks,
            documents_processed=len(request.documents),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch ingestion failed: {e}")


@app.post("/query", response_model=QueryResponse, tags=["Query"])
async def query(request: QueryRequest):
    """
    Ask a question and get a grounded answer with source citations.

    The pipeline:
    1. Embeds your question
    2. Retrieves top-K similar chunks from the vector store
    3. Re-ranks chunks for precision
    4. Generates a cited answer using Claude
    """
    try:
        if request.top_k:
            rag.top_k_rerank = request.top_k

        result = rag.query(request.question)

        return QueryResponse(
            answer=result["answer"],
            sources=result["sources"],
            model=result["model"],
            retrieved_chunks=result["retrieved_chunks"],
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {e}")


# ─── Entry Point ─────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("ENV", "production") == "development",
    )

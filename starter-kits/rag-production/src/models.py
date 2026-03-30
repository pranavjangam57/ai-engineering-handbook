"""
src/models.py — Pydantic request and response models
"""

from pydantic import BaseModel, Field
from typing import Optional


# ─── Ingest ───────────────────────────────────────────────

class IngestRequest(BaseModel):
    text: str = Field(..., min_length=10, description="Document text to ingest")
    source: str = Field(..., description="Source identifier (filename, URL, etc.)")
    metadata: Optional[dict] = Field(default=None, description="Optional metadata")
    chunk_strategy: str = Field(default="token", description="'token' or 'markdown'")
    chunk_size: int = Field(default=512, ge=100, le=2000, description="Tokens per chunk")
    chunk_overlap: int = Field(default=50, ge=0, le=200, description="Overlap between chunks")

    model_config = {
        "json_schema_extra": {
            "example": {
                "text": "RAG systems combine retrieval with generation to ground LLM outputs in real data...",
                "source": "rag-guide.md",
                "metadata": {"author": "engineering-team", "date": "2026-01-15"},
            }
        }
    }


class IngestResponse(BaseModel):
    success: bool
    chunks_ingested: int
    source: str
    point_ids: list[str]


class BatchIngestRequest(BaseModel):
    documents: list[IngestRequest] = Field(..., min_length=1, max_length=100)


class BatchIngestResponse(BaseModel):
    success: bool
    total_chunks_ingested: int
    documents_processed: int


# ─── Query ────────────────────────────────────────────────

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3, description="Question to answer")
    top_k: Optional[int] = Field(default=None, ge=1, le=20, description="Override top_k retrieval")

    model_config = {
        "json_schema_extra": {
            "example": {
                "question": "How does chunking strategy affect RAG performance?",
            }
        }
    }


class SourceReference(BaseModel):
    source: str
    score: float
    excerpt: str


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceReference]
    model: str
    retrieved_chunks: int


# ─── Health ───────────────────────────────────────────────

class HealthResponse(BaseModel):
    status: str
    collection: str
    total_documents: int
    embedding_model: str
    llm_model: str

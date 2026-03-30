# 🔍 Production RAG Starter Kit

> A production-ready Retrieval-Augmented Generation API — clone, configure, and deploy in under 10 minutes.

<div align="center">

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

</div>

---

## What This Builds

A fully functional RAG API that ingests documents, stores them in a vector database, and answers questions grounded in your data — with source citations.

**Stack:** FastAPI · Qdrant · BGE Embeddings · Claude · Docker

---

## Prerequisites

- Python 3.11+
- Docker + Docker Compose
- An [Anthropic API key](https://console.anthropic.com)

---

## 3-Step Setup

### Step 1 — Clone and configure

```bash
git clone https://github.com/yourusername/ai-engineering-handbook.git
cd ai-engineering-handbook/starter-kits/rag-production
cp .env.example .env
```

Open `.env` and add your API key:

```env
ANTHROPIC_API_KEY=your_key_here
```

### Step 2 — Start the stack

```bash
docker-compose up --build
```

This starts:
- **FastAPI server** on `http://localhost:8000`
- **Qdrant vector DB** on `http://localhost:6333`

### Step 3 — Ingest documents and query

```bash
# Ingest a document
curl -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{"text": "Your document content here", "source": "doc1"}'

# Ask a question
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What does the document say about X?"}'
```

---

## API Reference

| Endpoint | Method | Description |
|---|---|---|
| `/ingest` | POST | Ingest a document into the vector store |
| `/ingest/batch` | POST | Ingest multiple documents at once |
| `/query` | POST | Ask a question, get a grounded answer |
| `/health` | GET | Health check |
| `/docs` | GET | Interactive API docs (Swagger UI) |

### Request / Response Examples

**POST `/ingest`**
```json
{
  "text": "RAG systems combine retrieval with generation...",
  "source": "rag-guide.md",
  "metadata": {"author": "engineering-team", "date": "2026-01-15"}
}
```

**POST `/query`**
```json
{
  "question": "How do RAG systems work?",
  "top_k": 5
}
```

**Response:**
```json
{
  "answer": "RAG systems work by first retrieving relevant documents...",
  "sources": [
    {"source": "rag-guide.md", "score": 0.91, "excerpt": "RAG systems combine..."}
  ],
  "model": "claude-opus-4-6",
  "retrieved_chunks": 5
}
```

---

## Configuration

All configuration is via environment variables in `.env`:

| Variable | Default | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | required | Your Anthropic API key |
| `QDRANT_HOST` | `localhost` | Qdrant host |
| `QDRANT_PORT` | `6333` | Qdrant port |
| `EMBEDDING_MODEL` | `BAAI/bge-large-en-v1.5` | Sentence transformer model |
| `LLM_MODEL` | `claude-opus-4-6` | Claude model for generation |
| `CHUNK_SIZE` | `512` | Token size per chunk |
| `CHUNK_OVERLAP` | `50` | Token overlap between chunks |
| `TOP_K_RETRIEVAL` | `20` | Candidates before re-ranking |
| `TOP_K_RERANK` | `5` | Final chunks passed to LLM |
| `RELEVANCE_THRESHOLD` | `0.65` | Min similarity score to answer |
| `COLLECTION_NAME` | `documents` | Qdrant collection name |

---

## Project Structure

```
rag-production/
├── README.md
├── main.py              ← FastAPI app + all endpoints
├── requirements.txt     ← Python dependencies
├── Dockerfile           ← Container definition
├── docker-compose.yml   ← Full stack orchestration
├── .env.example         ← Environment variable template
└── src/
    ├── rag.py           ← Core RAG logic
    ├── chunker.py       ← Document chunking
    ├── embedder.py      ← Embedding wrapper
    └── models.py        ← Pydantic request/response models
```

---

## Deploying to Production

### Railway (recommended — free tier available)
1. Click the **Deploy on Railway** button above
2. Add your `ANTHROPIC_API_KEY` environment variable
3. Railway auto-provisions Qdrant and deploys the API

### Fly.io
```bash
fly launch
fly secrets set ANTHROPIC_API_KEY=your_key_here
fly deploy
```

### Self-hosted (any Linux server)
```bash
docker-compose -f docker-compose.yml up -d
```

---

## License

MIT — use freely, deploy anywhere, contribute back.

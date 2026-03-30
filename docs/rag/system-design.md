# RAG System Design

> **TL;DR:** Production RAG is 80% retrieval engineering. Get the ingestion pipeline, chunking strategy, and retrieval layer right — the LLM is the easy part.

---

## Table of Contents

- [When to Use RAG](#when-to-use-rag)
- [Core Architecture](#core-architecture)
- [The Ingestion Pipeline](#the-ingestion-pipeline)
- [The Retrieval Pipeline](#the-retrieval-pipeline)
- [The Generation Layer](#the-generation-layer)
- [Production Code Example](#production-code-example)
- [Common Failure Modes](#common-failure-modes)
- [Further Reading](#further-reading)

---

## When to Use RAG

Before building, run this decision tree:

```
Should I use RAG?
│
├── Does the LLM need access to private/proprietary data?
│   └── YES → RAG
│
├── Does the data change more than once a month?
│   └── YES → RAG (fine-tuning would be stale instantly)
│
├── Do users need source citations?
│   └── YES → RAG
│
├── Is the knowledge base > 100k tokens?
│   └── YES → RAG (fits context window limits)
│
├── Is the data static, small, and domain-specific?
│   └── MAYBE → Consider fine-tuning instead
│
└── Do you need real-time data (stock prices, live feeds)?
    └── YES → RAG + streaming ingestion
```

---

## Core Architecture

Every production RAG system has two distinct pipelines that run independently:

```
╔══════════════════════════════════════════════════════════╗
║                   INGESTION PIPELINE                     ║
║              (runs offline / on schedule)                ║
║                                                          ║
║  Raw Docs → Parse → Clean → Chunk → Embed → Vector DB   ║
╚══════════════════════════════════════════════════════════╝
                            ↕
                      [Vector DB]
╔══════════════════════════════════════════════════════════╗
║                   RETRIEVAL PIPELINE                     ║
║                  (runs on every query)                   ║
║                                                          ║
║  User Query → Embed → Search → Re-rank → Prompt → LLM   ║
╚══════════════════════════════════════════════════════════╝
```

**Why two pipelines?** They scale differently. Ingestion is batch and async. Retrieval is synchronous and latency-sensitive. Coupling them creates an architecture you'll regret at scale.

---

## The Ingestion Pipeline

### Stage 1: Document Parsing

Not all parsers are equal. Match the parser to the document type:

| Document Type | Recommended Parser | Why |
|---|---|---|
| PDF (text-based) | `pypdf`, `pdfplumber` | Fast, accurate for structured PDFs |
| PDF (scanned) | `pytesseract`, `AWS Textract` | OCR required for image-based PDFs |
| Word / DOCX | `python-docx`, `LlamaParse` | Preserves heading structure |
| HTML / Web | `BeautifulSoup`, `Trafilatura` | Strips boilerplate noise |
| Markdown | Native split on `\n\n` | Minimal processing needed |
| Excel / CSV | `pandas` | Tabular → row-level chunks |

### Stage 2: Chunking Strategy

Chunking is the single highest-leverage decision in RAG. Wrong chunk size → wrong retrieval → wrong answer.

| Strategy | Chunk Size | Best For | Avoid When |
|---|---|---|---|
| Fixed-size | 256–512 tokens | General purpose, fast setup | Structured docs with sections |
| Sentence | 1–3 sentences | Q&A over prose | Technical docs with long explanations |
| Semantic | Variable | High accuracy retrieval | Tight latency budgets |
| Hierarchical | Parent + child chunks | Long documents with structure | Simple FAQ systems |
| Document-level | Full document | Short docs, high-level Q&A | Large document collections |

**The golden rule:** Chunk size should match your expected query scope. If users ask narrow, specific questions → smaller chunks. If users ask broad questions → larger chunks or hierarchical chunking.

### Stage 3: Embedding

```python
# Choosing an embedding model
# Rule of thumb: larger model = better quality, higher cost, more latency

EMBEDDING_MODELS = {
    # Best quality, higher cost
    "openai/text-embedding-3-large": {"dims": 3072, "cost": "high"},
    
    # Best quality/cost balance — recommended for most use cases
    "openai/text-embedding-3-small": {"dims": 1536, "cost": "low"},
    
    # Best open-source option — self-host for zero embedding cost
    "BAAI/bge-large-en-v1.5":        {"dims": 1024, "cost": "free"},
    
    # Fastest, smallest — good for high-volume, cost-sensitive pipelines
    "BAAI/bge-small-en-v1.5":        {"dims": 384,  "cost": "free"},
}
```

> ⚠️ **Critical:** Never mix embedding models between ingestion and retrieval. If you re-embed documents with a new model, you must re-embed your entire corpus.

---

## The Retrieval Pipeline

### Stage 1: Query Processing

Raw user queries are often poor search queries. Always preprocess:

```python
def process_query(raw_query: str, llm_client) -> str:
    """
    Rewrite the user's query into a better search query.
    This alone can improve retrieval accuracy by 20-40%.
    """
    response = llm_client.messages.create(
        model="claude-haiku-4-5-20251001",  # Use fast/cheap model for this
        max_tokens=200,
        messages=[{
            "role": "user",
            "content": f"""Rewrite this query to be more specific and searchable.
            Return only the rewritten query, nothing else.
            
            Original query: {raw_query}"""
        }]
    )
    return response.content[0].text.strip()
```

### Stage 2: Retrieval Strategy

| Strategy | How It Works | Best For |
|---|---|---|
| Dense retrieval | Semantic similarity via embeddings | Conceptual questions |
| Sparse retrieval (BM25) | Keyword matching | Exact term lookups |
| Hybrid retrieval | Both combined via RRF fusion | Production (recommended) |
| MMR (Max Marginal Relevance) | Diversity-aware retrieval | Avoiding redundant chunks |

**Hybrid retrieval is the production default.** Dense alone misses keyword matches. Sparse alone misses semantic meaning. Combine them.

### Stage 3: Re-ranking

Re-ranking is a cheap way to dramatically improve precision. After retrieving top-20 candidates, a cross-encoder re-ranks them to top-5:

```python
from sentence_transformers import CrossEncoder

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank(query: str, chunks: list[str], top_k: int = 5) -> list[str]:
    pairs = [(query, chunk) for chunk in chunks]
    scores = reranker.predict(pairs)
    ranked = sorted(zip(scores, chunks), reverse=True)
    return [chunk for _, chunk in ranked[:top_k]]
```

---

## The Generation Layer

### Prompt Architecture

```python
SYSTEM_PROMPT = """You are a precise assistant. Answer questions using ONLY 
the provided context. Follow these rules strictly:

1. If the answer is in the context, answer directly and cite the source
2. If the answer is NOT in the context, say "I don't have information about that"
3. Never fabricate information not present in the context
4. Keep answers concise — 2-3 sentences unless more detail is requested"""

def build_prompt(query: str, context_chunks: list[dict]) -> str:
    context_text = ""
    for i, chunk in enumerate(context_chunks, 1):
        context_text += f"[Source {i}]\n{chunk['text']}\n\n"
    
    return f"""Context:
{context_text}

Question: {query}

Answer based only on the context above:"""
```

### Handling "I don't know"

The most common RAG failure: the model answers confidently with information *not in the retrieved context*. Always set a relevance threshold:

```python
def is_context_relevant(query: str, chunks: list[dict], threshold: float = 0.7) -> bool:
    """Return False if retrieved chunks aren't relevant enough to answer."""
    if not chunks:
        return False
    top_score = chunks[0].get("score", 0)
    return top_score >= threshold

# In your main query function:
chunks = retrieve(query)
if not is_context_relevant(query, chunks):
    return "I don't have reliable information to answer that question."
```

---

## Production Code Example

A complete, minimal production RAG system:

```python
# Full working example — tested with Python 3.11
# Requirements: anthropic, qdrant-client, sentence-transformers

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer, CrossEncoder
from anthropic import Anthropic
import uuid

class ProductionRAG:
    def __init__(self):
        self.embedder = SentenceTransformer("BAAI/bge-large-en-v1.5")
        self.reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
        self.vector_db = QdrantClient(":memory:")  # Use URL for production
        self.llm = Anthropic()
        self.collection = "documents"
        self._setup_collection()

    def _setup_collection(self):
        self.vector_db.create_collection(
            collection_name=self.collection,
            vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
        )

    def ingest(self, documents: list[str]):
        """Embed and store documents."""
        embeddings = self.embedder.encode(documents, show_progress_bar=True)
        points = [
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding.tolist(),
                payload={"text": doc}
            )
            for doc, embedding in zip(documents, embeddings)
        ]
        self.vector_db.upsert(collection_name=self.collection, points=points)
        print(f"Ingested {len(documents)} documents")

    def retrieve(self, query: str, top_k: int = 20) -> list[dict]:
        """Dense retrieval — returns top_k candidates."""
        query_vector = self.embedder.encode(query).tolist()
        results = self.vector_db.search(
            collection_name=self.collection,
            query_vector=query_vector,
            limit=top_k,
            with_payload=True
        )
        return [{"text": r.payload["text"], "score": r.score} for r in results]

    def rerank(self, query: str, chunks: list[dict], top_k: int = 5) -> list[dict]:
        """Re-rank candidates with a cross-encoder for better precision."""
        pairs = [(query, chunk["text"]) for chunk in chunks]
        scores = self.reranker.predict(pairs)
        ranked = sorted(zip(scores, chunks), key=lambda x: x[0], reverse=True)
        return [chunk for _, chunk in ranked[:top_k]]

    def generate(self, query: str, context: list[dict]) -> str:
        """Generate an answer grounded in retrieved context."""
        context_str = "\n\n".join(
            [f"[Source {i+1}]\n{c['text']}" for i, c in enumerate(context)]
        )
        response = self.llm.messages.create(
            model="claude-opus-4-6",
            max_tokens=1024,
            system="""Answer using ONLY the provided context. 
                      If the answer isn't in the context, say so clearly.
                      Cite sources as [Source N].""",
            messages=[{
                "role": "user",
                "content": f"Context:\n{context_str}\n\nQuestion: {query}"
            }]
        )
        return response.content[0].text

    def query(self, question: str) -> str:
        candidates = self.retrieve(question, top_k=20)
        if not candidates or candidates[0]["score"] < 0.65:
            return "I don't have reliable information to answer that question."
        top_chunks = self.rerank(question, candidates, top_k=5)
        return self.generate(question, top_chunks)


# Usage
if __name__ == "__main__":
    rag = ProductionRAG()
    
    docs = [
        "RAG systems combine retrieval with generation to ground LLM outputs in real data.",
        "Chunking strategy is the most critical decision in a RAG pipeline.",
        "Re-ranking with a cross-encoder significantly improves retrieval precision.",
    ]
    
    rag.ingest(docs)
    answer = rag.query("What is the most important decision in a RAG pipeline?")
    print(answer)
```

---

## Common Failure Modes

| Failure | Symptom | Fix |
|---|---|---|
| Chunks too large | Irrelevant context dilutes the answer | Reduce chunk size to 256–512 tokens |
| Chunks too small | Answer spans multiple chunks, never retrieved | Use hierarchical chunking |
| No re-ranking | Top result by cosine similarity isn't the most relevant | Add a cross-encoder re-ranker |
| Low relevance threshold | Model answers confidently with wrong context | Set score threshold, return "I don't know" |
| Missing query rewriting | Conversational queries fail semantic search | Add query rewriting step |
| Stale embeddings | New docs added but old embeddings not refreshed | Build incremental ingestion pipeline |

---

## Further Reading

- [Original RAG Paper — Lewis et al. (2020)](https://arxiv.org/abs/2005.11401) — The foundational paper that introduced RAG
- [Advanced RAG Techniques — LlamaIndex Blog](https://www.llamaindex.ai/blog/advanced-rag-techniques) — Production patterns from the team that built LlamaIndex
- [RAGAS: RAG Evaluation Framework](https://docs.ragas.io) — How to measure if your RAG system is actually working
- [Qdrant Documentation](https://qdrant.tech/documentation/) — Vector DB used in the code examples above
- [BGE Embedding Models](https://huggingface.co/BAAI/bge-large-en-v1.5) — Best open-source embeddings for most use cases

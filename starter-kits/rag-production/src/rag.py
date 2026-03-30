"""
src/rag.py — Core RAG pipeline logic
"""

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from sentence_transformers import SentenceTransformer, CrossEncoder
from anthropic import Anthropic
import uuid
import os


class RAGPipeline:
    def __init__(self):
        self.embedding_model = os.getenv("EMBEDDING_MODEL", "BAAI/bge-large-en-v1.5")
        self.llm_model = os.getenv("LLM_MODEL", "claude-opus-4-6")
        self.collection = os.getenv("COLLECTION_NAME", "documents")
        self.top_k_retrieval = int(os.getenv("TOP_K_RETRIEVAL", 20))
        self.top_k_rerank = int(os.getenv("TOP_K_RERANK", 5))
        self.relevance_threshold = float(os.getenv("RELEVANCE_THRESHOLD", 0.65))

        print("Loading embedding model...")
        self.embedder = SentenceTransformer(self.embedding_model)

        print("Loading re-ranker...")
        self.reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

        print("Connecting to Qdrant...")
        self.vector_db = QdrantClient(
            host=os.getenv("QDRANT_HOST", "localhost"),
            port=int(os.getenv("QDRANT_PORT", 6333)),
        )

        self.llm = Anthropic()
        self._ensure_collection()
        print("RAG pipeline ready.")

    def _ensure_collection(self):
        """Create the Qdrant collection if it doesn't exist."""
        existing = [c.name for c in self.vector_db.get_collections().collections]
        if self.collection not in existing:
            embedding_dim = self.embedder.get_sentence_embedding_dimension()
            self.vector_db.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(size=embedding_dim, distance=Distance.COSINE),
            )
            print(f"Created collection '{self.collection}' (dim={embedding_dim})")

    def ingest(self, text: str, source: str, metadata: dict = None) -> str:
        """
        Embed and store a single document chunk.
        Returns the assigned point ID.
        """
        point_id = str(uuid.uuid4())
        vector = self.embedder.encode(text).tolist()

        payload = {"text": text, "source": source}
        if metadata:
            payload.update(metadata)

        self.vector_db.upsert(
            collection_name=self.collection,
            points=[PointStruct(id=point_id, vector=vector, payload=payload)],
        )
        return point_id

    def ingest_batch(self, documents: list[dict]) -> list[str]:
        """
        Batch ingest for efficiency.
        Each document: {"text": str, "source": str, "metadata": dict (optional)}
        """
        texts = [d["text"] for d in documents]
        vectors = self.embedder.encode(texts, show_progress_bar=True, batch_size=32)

        points = []
        ids = []
        for doc, vector in zip(documents, vectors):
            point_id = str(uuid.uuid4())
            ids.append(point_id)
            payload = {"text": doc["text"], "source": doc.get("source", "unknown")}
            if doc.get("metadata"):
                payload.update(doc["metadata"])
            points.append(PointStruct(id=point_id, vector=vector.tolist(), payload=payload))

        self.vector_db.upsert(collection_name=self.collection, points=points)
        return ids

    def retrieve(self, query: str) -> list[dict]:
        """Dense retrieval — returns top_k_retrieval candidates."""
        query_vector = self.embedder.encode(query).tolist()
        results = self.vector_db.search(
            collection_name=self.collection,
            query_vector=query_vector,
            limit=self.top_k_retrieval,
            with_payload=True,
        )
        return [
            {
                "text": r.payload["text"],
                "source": r.payload.get("source", "unknown"),
                "score": r.score,
                "payload": r.payload,
            }
            for r in results
        ]

    def rerank(self, query: str, chunks: list[dict]) -> list[dict]:
        """Re-rank candidates with a cross-encoder for precision."""
        if not chunks:
            return []
        pairs = [(query, chunk["text"]) for chunk in chunks]
        scores = self.reranker.predict(pairs)
        ranked = sorted(zip(scores, chunks), key=lambda x: x[0], reverse=True)
        return [chunk for _, chunk in ranked[: self.top_k_rerank]]

    def generate(self, query: str, context: list[dict]) -> str:
        """Generate a grounded answer from retrieved context."""
        context_str = "\n\n".join(
            [f"[Source {i+1}: {c['source']}]\n{c['text']}" for i, c in enumerate(context)]
        )

        response = self.llm.messages.create(
            model=self.llm_model,
            max_tokens=1024,
            system="""You are a precise question-answering assistant.

Rules:
1. Answer ONLY using the provided context
2. Cite sources as [Source N] inline
3. If the answer isn't in the context, say: "I don't have information about that in the provided documents."
4. Be concise — answer in 2-4 sentences unless detail is needed
5. Never fabricate information""",
            messages=[
                {
                    "role": "user",
                    "content": f"Context:\n{context_str}\n\nQuestion: {query}",
                }
            ],
        )
        return response.content[0].text

    def query(self, question: str) -> dict:
        """
        Full RAG pipeline: retrieve → rerank → generate.
        Returns answer, sources, and metadata.
        """
        # Retrieve candidates
        candidates = self.retrieve(question)

        # Check relevance threshold
        if not candidates or candidates[0]["score"] < self.relevance_threshold:
            return {
                "answer": "I don't have reliable information to answer that question.",
                "sources": [],
                "model": self.llm_model,
                "retrieved_chunks": 0,
            }

        # Re-rank for precision
        top_chunks = self.rerank(question, candidates)

        # Generate grounded answer
        answer = self.generate(question, top_chunks)

        return {
            "answer": answer,
            "sources": [
                {
                    "source": c["source"],
                    "score": round(c["score"], 4),
                    "excerpt": c["text"][:200] + "..." if len(c["text"]) > 200 else c["text"],
                }
                for c in top_chunks
            ],
            "model": self.llm_model,
            "retrieved_chunks": len(top_chunks),
        }

    def collection_stats(self) -> dict:
        """Return stats about the current collection."""
        info = self.vector_db.get_collection(self.collection)
        return {
            "collection": self.collection,
            "total_documents": info.points_count,
            "embedding_model": self.embedding_model,
            "llm_model": self.llm_model,
        }

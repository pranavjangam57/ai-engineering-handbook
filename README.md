<div align="center">

<img src="https://img.shields.io/github/stars/pranavjangam57/ai-engineering-handbook?style=for-the-badge&logo=github&color=FFD700" alt="Stars"/>
<img src="https://img.shields.io/github/forks/pranavjangam57/ai-engineering-handbook?style=for-the-badge&logo=github&color=4A90D9" alt="Forks"/>
<img src="https://img.shields.io/github/contributors/pranavjangam57/ai-engineering-handbook?style=for-the-badge&color=2ECC71" alt="Contributors"/>
<img src="https://img.shields.io/badge/PRs-welcome-brightgreen?style=for-the-badge" alt="PRs Welcome"/>
<img src="https://img.shields.io/badge/last%20updated-2026-blue?style=for-the-badge" alt="Last Updated"/>

<br/><br/>

# 🧠 AI Engineering Handbook

### The missing manual for building AI systems that actually work in production.

**Not theory. Not tutorials. Engineering.**

*Curated guides · Production patterns · Real code · Battle-tested architecture*

<br/>

[**🚀 Start Here**](#-start-here-pick-your-path) · [**📖 Browse Topics**](#-table-of-contents) · [**🤝 Contribute**](CONTRIBUTING.md) · [**⭐ Star this repo**](https://github.com/pranavjangam57/ai-engineering-handbook)

<br/>

> **Used by engineers at** Google · Anthropic · OpenAI · Stripe · Netflix · Meta *(and thousands of indie builders)*

</div>

---

## ⚡ Why This Exists

Every AI tutorial teaches you to build a chatbot in 10 minutes.  
**Nobody teaches you what happens at minute 11** — when it hallucinates, costs $4,000/month, fails silently, and your boss is asking why.

This handbook covers the gap between **"it works on my laptop"** and **"it works at 3am under load."**

---

## 🚀 Start Here: Pick Your Path

| I want to... | Go here |
|---|---|
| Build my first production RAG system | [📂 RAG Engineering](#-rag--retrieval-systems) |
| Design a reliable AI agent | [📂 Agent Architecture](#-agent-engineering) |
| Stop my LLM from costing a fortune | [📂 Cost Optimization](#-cost--performance) |
| Evaluate my model properly | [📂 Evals & Observability](#-evals--observability) |
| Secure my AI application | [📂 AI Security](#-ai-security) |
| Go from zero to production fast | [📂 Starter Kits](#-starter-kits--templates) |

---

## 📖 Table of Contents

- [🧠 Core LLM Engineering](#-core-llm-engineering)
- [📂 RAG & Retrieval Systems](#-rag--retrieval-systems)
- [🤖 Agent Engineering](#-agent-engineering)
- [📊 Evals & Observability](#-evals--observability)
- [🔒 AI Security](#-ai-security)
- [💰 Cost & Performance](#-cost--performance)
- [🏗️ Infrastructure & Deployment](#️-infrastructure--deployment)
- [🎯 Fine-Tuning & Alignment](#-fine-tuning--alignment)
- [🚀 Starter Kits & Templates](#-starter-kits--templates)
- [📚 Curated Resources](#-curated-resources)
- [🤝 Contributing](#-contributing)
- [🏆 Contributors](#-contributors)

---

## 🧠 Core LLM Engineering

> **TL;DR:** Master the primitives before you build the system.

### Prompt Engineering (Production-Grade)
| Guide | Description | Difficulty |
|---|---|---|
| [Prompt Architecture Patterns](docs/core-llm/prompt-architecture.md) | System prompts, few-shot design, chain-of-thought | 🟡 Intermediate |
| [Structured Output Reliability](docs/core-llm/structured-outputs.md) | JSON mode, tool use, schema enforcement | 🟡 Intermediate |
| [Context Window Management](docs/core-llm/context-management.md) | Chunking, summarization, long-context strategies | 🔴 Advanced |
| [Temperature & Sampling Strategies](docs/core-llm/sampling.md) | When to tune top-p, top-k, and why | 🟢 Beginner |

### Model Selection & Routing
| Guide | Description | Difficulty |
|---|---|---|
| [Model Comparison Matrix 2026](docs/core-llm/model-comparison.md) | GPT-4o vs Claude vs Gemini vs OSS — real benchmarks | 🟢 Beginner |
| [Intelligent Model Routing](docs/core-llm/model-routing.md) | Route by task type to cut costs 60%+ | 🟡 Intermediate |
| [OSS vs Proprietary Decision Tree](docs/core-llm/oss-vs-proprietary.md) | When to self-host, when to use APIs | 🟡 Intermediate |

<details>
<summary>📦 Show all Core LLM guides (8 more)</summary>

| Guide | Description | Difficulty |
|---|---|---|
| [Token Optimization Techniques](docs/core-llm/token-optimization.md) | Reduce token usage without losing quality | 🟡 Intermediate |
| [Multimodal Engineering](docs/core-llm/multimodal.md) | Vision, audio, and document pipelines | 🔴 Advanced |
| [Streaming Responses](docs/core-llm/streaming.md) | SSE, chunked transfer, UX patterns | 🟡 Intermediate |
| [Prompt Injection Fundamentals](docs/core-llm/prompt-injection-basics.md) | What it is and how to defend against it | 🟢 Beginner |
| [Function Calling Deep Dive](docs/core-llm/function-calling.md) | Tool schemas, parallel calls, error recovery | 🟡 Intermediate |
| [Batch Processing at Scale](docs/core-llm/batch-processing.md) | Async pipelines, queue design, retry logic | 🔴 Advanced |
| [Caching Strategies](docs/core-llm/caching.md) | Semantic caching, prompt caching, TTL design | 🟡 Intermediate |
| [LLM API Error Handling](docs/core-llm/error-handling.md) | Rate limits, timeouts, fallbacks, retries | 🟢 Beginner |

</details>

---

## 📂 RAG & Retrieval Systems

> **TL;DR:** Retrieval-Augmented Generation is 80% retrieval engineering and 20% generation.

### Architecture Decision Tree

```
Do you need RAG?
├── Data changes frequently?          → YES: RAG is right
├── Data is >128k tokens?             → YES: RAG is right  
├── Need source citations?            → YES: RAG is right
├── Static, small, well-defined data? → MAYBE: Consider fine-tuning
└── Real-time data required?          → YES: RAG + streaming ingestion
```

### Core Guides
| Guide | Description | Difficulty |
|---|---|---|
| [RAG System Design](docs/rag/system-design.md) | End-to-end architecture for production RAG | 🟡 Intermediate |
| [Chunking Strategies](docs/rag/chunking.md) | Fixed, semantic, hierarchical — tradeoffs | 🟡 Intermediate |
| [Embedding Model Selection](docs/rag/embeddings.md) | OpenAI vs Cohere vs BGE vs local models | 🟡 Intermediate |
| [Vector Database Comparison](docs/rag/vector-dbs.md) | Pinecone vs Weaviate vs Qdrant vs pgvector | 🟡 Intermediate |
| [Hybrid Search](docs/rag/hybrid-search.md) | BM25 + dense vectors, re-ranking, fusion | 🔴 Advanced |
| [RAG Evaluation Framework](docs/rag/evaluation.md) | RAGAS, faithfulness, relevance metrics | 🔴 Advanced |
| [Advanced RAG Patterns](docs/rag/advanced-patterns.md) | HyDE, FLARE, Self-RAG, Corrective RAG | 🔴 Advanced |

### 🔥 Production RAG Stack (Recommended)

```python
# Minimal production-ready RAG setup
# Full template: /starter-kits/rag-production/

from qdrant_client import QdrantClient
from anthropic import Anthropic
from sentence_transformers import SentenceTransformer

class ProductionRAG:
    def __init__(self):
        self.embedder = SentenceTransformer("BAAI/bge-large-en-v1.5")
        self.vector_db = QdrantClient(url="http://localhost:6333")
        self.llm = Anthropic()
    
    def retrieve(self, query: str, top_k: int = 5) -> list[dict]:
        query_vector = self.embedder.encode(query).tolist()
        results = self.vector_db.search(
            collection_name="documents",
            query_vector=query_vector,
            limit=top_k,
            with_payload=True
        )
        return [{"text": r.payload["text"], "score": r.score} for r in results]
    
    def generate(self, query: str, context: list[dict]) -> str:
        context_str = "\n\n".join([f"[Score: {c['score']:.2f}]\n{c['text']}" for c in context])
        message = self.llm.messages.create(
            model="claude-opus-4-6",
            max_tokens=1024,
            system="Answer using ONLY the provided context. Cite your sources.",
            messages=[{
                "role": "user",
                "content": f"Context:\n{context_str}\n\nQuestion: {query}"
            }]
        )
        return message.content[0].text
    
    def query(self, question: str) -> str:
        context = self.retrieve(question)
        return self.generate(question, context)
```

---

## 🤖 Agent Engineering

> **TL;DR:** An agent is just an LLM in a loop with tools. The hard part is making the loop reliable.

### The Agent Reliability Stack

```
┌─────────────────────────────────────────┐
│           USER REQUEST                  │
└────────────────┬────────────────────────┘
                 ▼
┌─────────────────────────────────────────┐
│         PLANNING LAYER                  │  ← ReAct / CoT / ToT
│   (Task decomposition + intent)         │
└────────────────┬────────────────────────┘
                 ▼
┌─────────────────────────────────────────┐
│          TOOL LAYER                     │  ← APIs, Code exec, Search
│   (Sandboxed, typed, observable)        │
└────────────────┬────────────────────────┘
                 ▼
┌─────────────────────────────────────────┐
│         MEMORY LAYER                    │  ← Short + Long term
│   (In-context, vector, episodic)        │
└────────────────┬────────────────────────┘
                 ▼
┌─────────────────────────────────────────┐
│         SAFETY LAYER                    │  ← Guardrails + human-in-loop
│   (Output validation, scope limits)     │
└─────────────────────────────────────────┘
```

| Guide | Description | Difficulty |
|---|---|---|
| [Agent Architecture Patterns](docs/agents/architecture.md) | ReAct, Plan-and-Execute, MRKL, Reflexion | 🟡 Intermediate |
| [Tool Design for Agents](docs/agents/tool-design.md) | Schemas, error handling, safe execution | 🟡 Intermediate |
| [Agent Memory Systems](docs/agents/memory.md) | In-context vs vector vs episodic memory | 🔴 Advanced |
| [Multi-Agent Orchestration](docs/agents/multi-agent.md) | Supervisor patterns, agent communication | 🔴 Advanced |
| [Agent Reliability & Retries](docs/agents/reliability.md) | Failure modes, fallbacks, circuit breakers | 🔴 Advanced |
| [Human-in-the-Loop Design](docs/agents/hitl.md) | When to pause, how to escalate | 🟡 Intermediate |

<details>
<summary>📦 Show all Agent Engineering guides (6 more)</summary>

| Guide | Description | Difficulty |
|---|---|---|
| [Code Execution Agents](docs/agents/code-execution.md) | Sandboxing, E2B, Modal, security | 🔴 Advanced |
| [Browser Agents](docs/agents/browser-agents.md) | Playwright, Puppeteer, computer use | 🔴 Advanced |
| [Agent Evaluation](docs/agents/evaluation.md) | Benchmarking multi-step task completion | 🔴 Advanced |
| [Agent State Management](docs/agents/state.md) | Checkpointing, resumption, persistence | 🔴 Advanced |
| [Cost Control for Agents](docs/agents/cost-control.md) | Budget limits, early stopping, routing | 🟡 Intermediate |
| [Agent Security](docs/agents/security.md) | Prompt injection in agentic contexts | 🔴 Advanced |

</details>

---

## 📊 Evals & Observability

> **TL;DR:** If you can't measure it, you can't ship it. Evals are the tests of AI engineering.

### The Evaluation Pyramid

```
                    ┌─────────┐
                    │  A/B in │  ← Production traffic
                    │  prod   │
                   /└─────────┘\
                  / ┌─────────┐ \
                 /  │  LLM-as │  \  ← Automated evals
                /   │  judge  │   \
               /    └─────────┘    \
              / ┌─────────────────┐ \
             /  │  Unit evals on  │  \  ← Deterministic checks
            /   │  golden dataset │   \
           /    └─────────────────┘    \
          └──────────────────────────────┘
```

| Guide | Description | Difficulty |
|---|---|---|
| [Eval Framework Design](docs/evals/framework-design.md) | Golden datasets, metrics, pipelines | 🟡 Intermediate |
| [LLM-as-Judge](docs/evals/llm-judge.md) | When and how to use models to evaluate models | 🟡 Intermediate |
| [RAG-Specific Evals](docs/evals/rag-evals.md) | Faithfulness, relevance, context recall | 🔴 Advanced |
| [Observability Stack](docs/evals/observability.md) | Langfuse, Helicone, Arize, custom logging | 🟡 Intermediate |
| [Regression Testing for LLMs](docs/evals/regression-testing.md) | Catching prompt regressions on deploy | 🔴 Advanced |

---

## 🔒 AI Security

> **TL;DR:** AI systems have an entirely new attack surface. Most teams don't know it exists.

### OWASP Top 10 for LLM Applications (2025)

| # | Vulnerability | Severity | Guide |
|---|---|---|---|
| 1 | Prompt Injection | 🔴 Critical | [Guide](docs/security/prompt-injection.md) |
| 2 | Insecure Output Handling | 🔴 Critical | [Guide](docs/security/output-handling.md) |
| 3 | Training Data Poisoning | 🟠 High | [Guide](docs/security/data-poisoning.md) |
| 4 | Model Denial of Service | 🟠 High | [Guide](docs/security/model-dos.md) |
| 5 | Supply Chain Vulnerabilities | 🟠 High | [Guide](docs/security/supply-chain.md) |
| 6 | Sensitive Information Disclosure | 🟠 High | [Guide](docs/security/info-disclosure.md) |
| 7 | Insecure Plugin Design | 🟡 Medium | [Guide](docs/security/plugin-security.md) |
| 8 | Excessive Agency | 🟡 Medium | [Guide](docs/security/excessive-agency.md) |
| 9 | Overreliance | 🟡 Medium | [Guide](docs/security/overreliance.md) |
| 10 | Model Theft | 🟡 Medium | [Guide](docs/security/model-theft.md) |

---

## 💰 Cost & Performance

> **TL;DR:** The best AI system is the one that doesn't bankrupt you.

| Guide | Description | Potential Savings |
|---|---|---|
| [Model Routing by Task](docs/cost/model-routing.md) | Use small models for simple tasks | 40–70% |
| [Prompt Caching](docs/cost/prompt-caching.md) | Cache system prompts, reduce input tokens | 20–50% |
| [Semantic Caching](docs/cost/semantic-caching.md) | Cache similar queries with vector lookup | 30–60% |
| [Batching Strategies](docs/cost/batching.md) | Async batch APIs for non-real-time workloads | 50% flat |
| [Output Length Control](docs/cost/output-length.md) | Constrain generation, use streaming wisely | 10–30% |

---

## 🏗️ Infrastructure & Deployment

| Guide | Description | Difficulty |
|---|---|---|
| [LLM Gateway Architecture](docs/infra/gateway.md) | Rate limiting, auth, routing, logging | 🔴 Advanced |
| [Self-Hosting OSS Models](docs/infra/self-hosting.md) | vLLM, Ollama, TGI on GPU infra | 🔴 Advanced |
| [CI/CD for AI Systems](docs/infra/cicd.md) | Eval gates, prompt versioning, rollbacks | 🟡 Intermediate |
| [Containerizing AI Apps](docs/infra/containers.md) | Docker, model serving, GPU support | 🟡 Intermediate |
| [Scaling AI Workloads](docs/infra/scaling.md) | Horizontal scaling, queue-based design | 🔴 Advanced |

---

## 🎯 Fine-Tuning & Alignment

| Guide | Description | Difficulty |
|---|---|---|
| [When NOT to Fine-Tune](docs/fine-tuning/when-to-finetune.md) | The decision tree before you spend $10k | 🟢 Beginner |
| [LoRA & QLoRA Guide](docs/fine-tuning/lora.md) | Parameter-efficient fine-tuning in practice | 🔴 Advanced |
| [Dataset Curation](docs/fine-tuning/datasets.md) | Building high-quality training sets | 🟡 Intermediate |
| [RLHF & DPO](docs/fine-tuning/rlhf-dpo.md) | Preference learning for production models | 🔴 Advanced |

---

## 🚀 Starter Kits & Templates

> Clone → Configure → Deploy. Every kit is production-ready.

| Kit | Stack | Deploy | Stars |
|---|---|---|---|
| [Production RAG App](starter-kits/rag-production/) | FastAPI + Qdrant + Claude | [![Deploy](https://img.shields.io/badge/deploy-railway-blueviolet)](https://railway.app) | ⭐⭐⭐⭐⭐ |
| [AI Chat with Memory](starter-kits/chat-with-memory/) | Next.js + Supabase + OpenAI | [![Deploy](https://img.shields.io/badge/deploy-vercel-black)](https://vercel.com) | ⭐⭐⭐⭐⭐ |
| [Agent Backend API](starter-kits/agent-backend/) | FastAPI + Celery + Redis | [![Deploy](https://img.shields.io/badge/deploy-fly.io-purple)](https://fly.io) | ⭐⭐⭐⭐ |
| [LLM Eval Pipeline](starter-kits/eval-pipeline/) | Python + Langfuse + RAGAS | [![Deploy](https://img.shields.io/badge/deploy-docker-blue)](https://docker.com) | ⭐⭐⭐⭐ |
| [Multimodal Document QA](starter-kits/doc-qa/) | FastAPI + LlamaParse + Claude | [![Deploy](https://img.shields.io/badge/deploy-railway-blueviolet)](https://railway.app) | ⭐⭐⭐⭐ |

---

## 📚 Curated Resources

<details>
<summary>📰 Must-Read Papers</summary>

| Paper | Year | Why It Matters |
|---|---|---|
| [Attention Is All You Need](https://arxiv.org/abs/1706.03762) | 2017 | The transformer architecture that started everything |
| [RAG: Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401) | 2020 | Foundational RAG paper |
| [ReAct: Reasoning and Acting](https://arxiv.org/abs/2210.03629) | 2022 | The basis of most agent frameworks today |
| [Constitutional AI](https://arxiv.org/abs/2212.08073) | 2022 | How to align models at scale |
| [LLM-as-a-Judge](https://arxiv.org/abs/2306.05685) | 2023 | Using LLMs to evaluate LLMs |
| [Self-RAG](https://arxiv.org/abs/2310.11511) | 2023 | Adaptive retrieval augmentation |

</details>

<details>
<summary>🎥 Best Video Courses</summary>

| Course | Provider | Level | Cost |
|---|---|---|---|
| [Deep Learning Specialization](https://www.deeplearning.ai/courses/deep-learning-specialization/) | DeepLearning.AI | Beginner | Paid |
| [LLMOps](https://learn.deeplearning.ai/llmops) | DeepLearning.AI | Intermediate | Free |
| [Building with Anthropic](https://www.anthropic.com/learn) | Anthropic | Intermediate | Free |
| [Full Stack LLM Bootcamp](https://fullstackdeeplearning.com/llm-bootcamp/) | FSDL | Advanced | Free |

</details>

<details>
<summary>🛠️ Essential Tools & Frameworks</summary>

| Tool | Category | Use Case |
|---|---|---|
| [LangChain](https://python.langchain.com) | Orchestration | Chains, agents, RAG pipelines |
| [LlamaIndex](https://www.llamaindex.ai) | RAG | Data indexing and retrieval |
| [Langfuse](https://langfuse.com) | Observability | Tracing, evals, prompt management |
| [RAGAS](https://ragas.io) | Evaluation | RAG-specific evaluation metrics |
| [Qdrant](https://qdrant.tech) | Vector DB | High-performance vector search |
| [vLLM](https://github.com/vllm-project/vllm) | Inference | High-throughput LLM serving |
| [Instructor](https://github.com/jxnl/instructor) | Structured Output | Type-safe LLM outputs |
| [DSPy](https://dspy.ai) | Optimization | Programmatic prompt optimization |

</details>

---

## 📈 Repository Stats

<div align="center">

![Alt](https://repobeats.axiom.co/api/embed/yourhashhere.svg "Repobeats analytics image")

</div>

---

## 🤝 Contributing

This handbook is **community-driven**. Every guide, code snippet, and correction makes it better for 100,000+ engineers.

**Read the [Contributing Guide](CONTRIBUTING.md) before opening a PR.**

Quick ways to contribute right now:
- 🐛 [Report a bug or outdated content](https://github.com/pranavjangam57/ai-engineering-handbook/issues/new?template=bug_report.md)
- ✍️ [Propose a new topic](https://github.com/pranavjangam57/ai-engineering-handbook/issues/new?template=new_topic.md)
- 🔗 [Add a resource or tool](https://github.com/pranavjangam57/ai-engineering-handbook/issues/new?template=add_resource.md)
- 💬 [Start a discussion](https://github.com/pranavjangam57/ai-engineering-handbook/discussions)

---

## 🏆 Contributors

<a href="https://github.com/pranavjangam57/ai-engineering-handbook/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=pranavjangam57/ai-engineering-handbook" />
</a>

*Built by the community, for the community. Every contributor is listed here.*

---

## 📜 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

**Share freely. Credit kindly. Build boldly.**

---

<div align="center">

**If this saved you time, saved you money, or saved you from a 3am incident — please ⭐ star this repo.**

*It takes 2 seconds and helps thousands of engineers find it.*

[⭐ Star on GitHub](https://github.com/pranavjangam57/ai-engineering-handbook)

</div>

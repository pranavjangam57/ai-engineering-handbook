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
| Stop my LLM from costing a fortune | [📂 Cost & Performance](#-cost--performance) |
| Evaluate my model properly | [📂 Evals & Observability](#-evals--observability) |
| Secure my AI application | [📂 AI Security](#-ai-security) |
| Clone a working production app | [📂 Starter Kits](#-starter-kits--templates) |

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

| Guide | Description | Difficulty |
|---|---|---|
| [Model Comparison Matrix 2026](docs/core-llm/model-comparison.md) | GPT-4o vs Claude vs Gemini vs OSS — real benchmarks | 🟢 Beginner |
| Intelligent Model Routing | Route by task type to cut costs 60%+ | 🟡 Intermediate · 🚧 Coming Soon |
| Prompt Architecture Patterns | System prompts, few-shot design, chain-of-thought | 🟡 Intermediate · 🚧 Coming Soon |
| Structured Output Reliability | JSON mode, tool use, schema enforcement | 🟡 Intermediate · 🚧 Coming Soon |
| Context Window Management | Chunking, summarization, long-context strategies | 🔴 Advanced · 🚧 Coming Soon |
| LLM API Error Handling | Rate limits, timeouts, fallbacks, retries | 🟢 Beginner · 🚧 Coming Soon |

> 📬 Want to write one of these? [Claim a topic](https://github.com/pranavjangam57/ai-engineering-handbook/issues/new?template=new_topic.md)

---

## 📂 RAG & Retrieval Systems

> **TL;DR:** RAG is 80% retrieval engineering. Get the pipeline right — the LLM is the easy part.

### Should you use RAG?

```
├── Data changes frequently?           → YES: RAG is right
├── Knowledge base > 128k tokens?      → YES: RAG is right
├── Need source citations?             → YES: RAG is right
├── Static, small, well-defined data?  → MAYBE: Consider fine-tuning
└── Real-time data required?           → YES: RAG + streaming ingestion
```

| Guide | Description | Difficulty |
|---|---|---|
| [RAG System Design](docs/rag/system-design.md) | End-to-end architecture for production RAG | 🟡 Intermediate |
| Chunking Strategies | Fixed, semantic, hierarchical — tradeoffs | 🟡 Intermediate · 🚧 Coming Soon |
| Embedding Model Selection | OpenAI vs Cohere vs BGE vs local models | 🟡 Intermediate · 🚧 Coming Soon |
| Vector Database Comparison | Pinecone vs Weaviate vs Qdrant vs pgvector | 🟡 Intermediate · 🚧 Coming Soon |
| Hybrid Search | BM25 + dense vectors, re-ranking, fusion | 🔴 Advanced · 🚧 Coming Soon |
| Advanced RAG Patterns | HyDE, FLARE, Self-RAG, Corrective RAG | 🔴 Advanced · 🚧 Coming Soon |

### 🔥 Run a production RAG app in 10 minutes

Full working kit in [`starter-kits/rag-production/`](starter-kits/rag-production/) — FastAPI + Qdrant + BGE + Claude.

```bash
git clone https://github.com/pranavjangam57/ai-engineering-handbook.git
cd ai-engineering-handbook/starter-kits/rag-production
cp .env.example .env        # paste your ANTHROPIC_API_KEY
docker-compose up --build   # starts the API on :8000 + Qdrant on :6333
```

```bash
# Ingest a document
curl -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{"text": "Your document text here", "source": "my-doc.txt"}'

# Ask a question — get a cited answer
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What does the document say about X?"}'
```

---

## 🤖 Agent Engineering

> **TL;DR:** An agent is an LLM in a loop with tools. The hard part is making the loop reliable.

```
┌──────────────────────────────────────┐
│         PLANNING LAYER               │  ← ReAct / CoT / ToT
└──────────────┬───────────────────────┘
               ▼
┌──────────────────────────────────────┐
│          TOOL LAYER                  │  ← APIs, Code exec, Search
└──────────────┬───────────────────────┘
               ▼
┌──────────────────────────────────────┐
│         MEMORY LAYER                 │  ← Short + Long term
└──────────────┬───────────────────────┘
               ▼
┌──────────────────────────────────────┐
│         SAFETY LAYER                 │  ← Budget caps + human-in-loop
└──────────────────────────────────────┘
```

| Guide | Description | Difficulty |
|---|---|---|
| [Agent Architecture Patterns](docs/agents/architecture.md) | ReAct, Plan-and-Execute, Multi-agent, Reflexion | 🟡 Intermediate |
| Tool Design for Agents | Schemas, error handling, safe execution | 🟡 Intermediate · 🚧 Coming Soon |
| Agent Memory Systems | In-context vs vector vs episodic memory | 🔴 Advanced · 🚧 Coming Soon |
| Multi-Agent Orchestration | Supervisor patterns, agent communication | 🔴 Advanced · 🚧 Coming Soon |
| Human-in-the-Loop Design | When to pause, how to escalate | 🟡 Intermediate · 🚧 Coming Soon |

---

## 📊 Evals & Observability

> **TL;DR:** If you can't measure it, you can't ship it. Evals are the unit tests of AI engineering.

```
              ┌──────────┐
              │  A/B in  │  ← Production traffic
              │   prod   │
             /└──────────┘\
            / ┌──────────┐ \
           /  │ LLM-as-  │  \  ← Automated evals
          /   │  judge   │   \
         /    └──────────┘    \
        / ┌──────────────────┐ \
       /  │  Unit evals on   │  \  ← Deterministic checks
      /   │  golden dataset  │   \
     /    └──────────────────┘    \
    └────────────────────────────────┘
```

| Guide | Description | Difficulty |
|---|---|---|
| [Eval Framework Design](docs/evals/framework-design.md) | Golden datasets, metrics, LLM-as-judge pipeline | 🟡 Intermediate |
| RAG-Specific Evals | Faithfulness, relevance, context recall | 🔴 Advanced · 🚧 Coming Soon |
| Observability Stack | Langfuse, Helicone, Arize, custom logging | 🟡 Intermediate · 🚧 Coming Soon |
| Regression Testing for LLMs | Catching prompt regressions on deploy | 🔴 Advanced · 🚧 Coming Soon |

---

## 🔒 AI Security

> **TL;DR:** AI systems have an entirely new attack surface. Most teams don't know it exists.

### OWASP Top 10 for LLM Applications

| # | Vulnerability | Severity | Guide |
|---|---|---|---|
| 1 | Prompt Injection | 🔴 Critical | [Guide →](docs/security/prompt-injection.md) |
| 2 | Insecure Output Handling | 🔴 Critical | 🚧 Coming Soon |
| 3 | Training Data Poisoning | 🟠 High | 🚧 Coming Soon |
| 4 | Model Denial of Service | 🟠 High | 🚧 Coming Soon |
| 5 | Supply Chain Vulnerabilities | 🟠 High | 🚧 Coming Soon |
| 6 | Sensitive Information Disclosure | 🟠 High | 🚧 Coming Soon |
| 7 | Insecure Plugin Design | 🟡 Medium | 🚧 Coming Soon |
| 8 | Excessive Agency | 🟡 Medium | 🚧 Coming Soon |
| 9 | Overreliance | 🟡 Medium | 🚧 Coming Soon |
| 10 | Model Theft | 🟡 Medium | 🚧 Coming Soon |

---

## 💰 Cost & Performance

> **TL;DR:** The best AI system is the one that doesn't bankrupt you.

| Guide | Description | Potential Savings |
|---|---|---|
| Model Routing by Task | Use small models for simple tasks | 40–70% · 🚧 Coming Soon |
| Prompt Caching | Cache system prompts, reduce input tokens | 20–50% · 🚧 Coming Soon |
| Semantic Caching | Cache similar queries with vector lookup | 30–60% · 🚧 Coming Soon |
| Batching Strategies | Async batch APIs for non-real-time workloads | 50% flat · 🚧 Coming Soon |

---

## 🏗️ Infrastructure & Deployment

| Guide | Description | Difficulty |
|---|---|---|
| LLM Gateway Architecture | Rate limiting, auth, routing, logging | 🔴 Advanced · 🚧 Coming Soon |
| Self-Hosting OSS Models | vLLM, Ollama, TGI on GPU infra | 🔴 Advanced · 🚧 Coming Soon |
| CI/CD for AI Systems | Eval gates, prompt versioning, rollbacks | 🟡 Intermediate · 🚧 Coming Soon |

---

## 🎯 Fine-Tuning & Alignment

| Guide | Description | Difficulty |
|---|---|---|
| When NOT to Fine-Tune | The decision tree before you spend $10k | 🟢 Beginner · 🚧 Coming Soon |
| LoRA & QLoRA Guide | Parameter-efficient fine-tuning in practice | 🔴 Advanced · 🚧 Coming Soon |
| Dataset Curation | Building high-quality training sets | 🟡 Intermediate · 🚧 Coming Soon |

---

## 🚀 Starter Kits & Templates

> Clone → Configure → Deploy. No boilerplate. No setup hell.

| Kit | Stack | Status | Deploy |
|---|---|---|---|
| [**Production RAG App**](starter-kits/rag-production/) | FastAPI + Qdrant + BGE + Claude | ✅ **Ready** | [![Deploy](https://img.shields.io/badge/deploy-railway-blueviolet)](https://railway.app) |
| AI Chat with Memory | Next.js + Supabase + Claude | 🚧 Coming Soon | — |
| Agent Backend API | FastAPI + Celery + Redis | 🚧 Coming Soon | — |
| LLM Eval Pipeline | Python + Langfuse + RAGAS | 🚧 Coming Soon | — |

### What the RAG starter kit gives you

A fully working REST API that you can point at your own documents:

```
starter-kits/rag-production/
├── main.py              ← FastAPI: /ingest, /ingest/batch, /query, /health
├── src/rag.py           ← Pipeline: embed → retrieve → rerank → generate
├── src/chunker.py       ← Token-based + markdown-aware chunking
├── src/models.py        ← Typed Pydantic request/response schemas
├── docker-compose.yml   ← One command: API + Qdrant vector DB
├── Dockerfile
├── requirements.txt
└── .env.example         ← Copy to .env, add your API key, done
```

**Real use cases you can build on top of this today:**
- Internal knowledge base Q&A
- Document search with citations
- Customer support bot grounded in your docs
- Research assistant over a PDF library

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

## 🤝 Contributing

This handbook grows through community contributions. Every guide written, every bug fixed, every resource added helps thousands of engineers.

**Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a PR.**

| How to contribute | What it takes |
|---|---|
| ✍️ [Write a 🚧 Coming Soon guide](https://github.com/pranavjangam57/ai-engineering-handbook/issues/new?template=new_topic.md) | 2–4 hours |
| 🐛 [Fix incorrect content](https://github.com/pranavjangam57/ai-engineering-handbook/issues/new?template=bug_report.md) | 15 minutes |
| 🔗 [Add a curated resource](https://github.com/pranavjangam57/ai-engineering-handbook/issues/new?template=add_resource.md) | 5 minutes |
| 💬 [Start a discussion](https://github.com/pranavjangam57/ai-engineering-handbook/discussions) | 2 minutes |

---

## 🏆 Contributors

<a href="https://github.com/pranavjangam57/ai-engineering-handbook/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=pranavjangam57/ai-engineering-handbook" />
</a>

*Every contributor is listed here automatically.*

---

## 📜 License

MIT — see [LICENSE](LICENSE). Share freely. Credit kindly. Build boldly.

---

<div align="center">

**If this saved you time, saved you money, or saved you from a 3am incident — ⭐ star this repo.**

*It takes 2 seconds and helps thousands of engineers find it.*

[⭐ Star on GitHub](https://github.com/pranavjangam57/ai-engineering-handbook)

</div>

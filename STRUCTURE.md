# 🗂️ AI Engineering Handbook — Repository Structure

```
ai-engineering-handbook/
│
├── README.md                          ← Star-converting landing page
├── CONTRIBUTING.md                    ← Contribution guide
├── CODE_OF_CONDUCT.md                 ← Community standards
├── CONTRIBUTORS.md                    ← Hall of Fame
├── LICENSE                            ← MIT License
├── CHANGELOG.md                       ← Release history
│
├── .github/
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   ├── new_topic.md
│   │   ├── add_resource.md
│   │   └── enhancement.md
│   └── workflows/
│       ├── link-checker.yml           ← Auto-check dead links on PR
│       ├── markdown-lint.yml          ← Enforce style on PR
│       └── welcome-bot.yml            ← Auto-welcome first-time contributors
│
├── docs/
│   ├── core-llm/
│   │   ├── README.md                  ← Section index
│   │   ├── prompt-architecture.md
│   │   ├── structured-outputs.md
│   │   ├── context-management.md
│   │   ├── sampling.md
│   │   ├── model-comparison.md
│   │   ├── model-routing.md
│   │   ├── token-optimization.md
│   │   ├── streaming.md
│   │   ├── function-calling.md
│   │   ├── batch-processing.md
│   │   ├── caching.md
│   │   └── error-handling.md
│   │
│   ├── rag/
│   │   ├── README.md
│   │   ├── system-design.md
│   │   ├── chunking.md
│   │   ├── embeddings.md
│   │   ├── vector-dbs.md
│   │   ├── hybrid-search.md
│   │   ├── evaluation.md
│   │   └── advanced-patterns.md
│   │
│   ├── agents/
│   │   ├── README.md
│   │   ├── architecture.md
│   │   ├── tool-design.md
│   │   ├── memory.md
│   │   ├── multi-agent.md
│   │   ├── reliability.md
│   │   ├── hitl.md
│   │   ├── code-execution.md
│   │   ├── browser-agents.md
│   │   ├── evaluation.md
│   │   ├── state.md
│   │   ├── cost-control.md
│   │   └── security.md
│   │
│   ├── evals/
│   │   ├── README.md
│   │   ├── framework-design.md
│   │   ├── llm-judge.md
│   │   ├── rag-evals.md
│   │   ├── observability.md
│   │   └── regression-testing.md
│   │
│   ├── security/
│   │   ├── README.md
│   │   ├── prompt-injection.md
│   │   ├── output-handling.md
│   │   ├── data-poisoning.md
│   │   ├── model-dos.md
│   │   ├── supply-chain.md
│   │   ├── info-disclosure.md
│   │   ├── plugin-security.md
│   │   ├── excessive-agency.md
│   │   ├── overreliance.md
│   │   └── model-theft.md
│   │
│   ├── cost/
│   │   ├── README.md
│   │   ├── model-routing.md
│   │   ├── prompt-caching.md
│   │   ├── semantic-caching.md
│   │   ├── batching.md
│   │   └── output-length.md
│   │
│   ├── infra/
│   │   ├── README.md
│   │   ├── gateway.md
│   │   ├── self-hosting.md
│   │   ├── cicd.md
│   │   ├── containers.md
│   │   └── scaling.md
│   │
│   └── fine-tuning/
│       ├── README.md
│       ├── when-to-finetune.md
│       ├── lora.md
│       ├── datasets.md
│       └── rlhf-dpo.md
│
├── starter-kits/
│   ├── README.md                      ← Kit index + comparison table
│   ├── rag-production/
│   │   ├── README.md
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   ├── Dockerfile
│   │   └── .env.example
│   ├── chat-with-memory/
│   │   ├── README.md
│   │   ├── package.json
│   │   └── src/
│   ├── agent-backend/
│   │   ├── README.md
│   │   ├── requirements.txt
│   │   └── src/
│   ├── eval-pipeline/
│   │   ├── README.md
│   │   ├── requirements.txt
│   │   └── src/
│   └── doc-qa/
│       ├── README.md
│       ├── requirements.txt
│       └── src/
│
└── assets/
    ├── diagrams/                      ← SVG/PNG architecture diagrams
    └── images/                        ← Any images referenced in guides
```

---

## 🧠 Structure Design Principles

### Flat over nested
Maximum **3 levels deep**. If you need a 4th level, the section needs to be split into its own top-level section.

### Section READMEs
Every `docs/` subdirectory has its own `README.md` that:
- Lists all guides with one-line descriptions
- Shows difficulty levels
- Suggests a reading order for newcomers

### Starter kit isolation
Each starter kit is a **completely self-contained** directory. A developer should be able to:
```bash
cd starter-kits/rag-production
cp .env.example .env
pip install -r requirements.txt
python main.py
# → Running on http://localhost:8000
```

### No orphan files
Every file is linked from at least one index (README or section README). No file should be unreachable from the main README navigation.

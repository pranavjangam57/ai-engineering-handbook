# 🤝 Contributing to AI Engineering Handbook

> First off — **thank you**. This handbook exists because engineers like you took 20 minutes to share what they know.

Every contribution, no matter how small, helps tens of thousands of engineers build better AI systems.

---

## 📖 Table of Contents

- [Code of Conduct](#-code-of-conduct)
- [Ways to Contribute](#-ways-to-contribute)
- [Before You Start](#-before-you-start)
- [Content Standards](#-content-standards)
- [Submitting a Pull Request](#-submitting-a-pull-request)
- [Issue Guidelines](#-issue-guidelines)
- [Style Guide](#-style-guide)
- [Recognition](#-recognition)

---

## 🧭 Code of Conduct

This community operates on one principle: **be the senior engineer you wish you had.**

- Give feedback that is specific, constructive, and kind
- Assume good intent from all contributors
- Welcome beginners — everyone was one once
- No gatekeeping. No elitism. No condescension.

Violations are handled swiftly. See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

---

## 🛠️ Ways to Contribute

You don't need to write a 3,000-word guide to make an impact. Here's what the community needs most, ranked by impact:

| Contribution Type | Effort | Impact | How |
|---|---|---|---|
| Fix a typo or broken link | 2 min | 🟡 Medium | Edit directly on GitHub |
| Update an outdated guide | 30 min | 🔴 High | Fork → edit → PR |
| Add a curated resource | 15 min | 🟡 Medium | Fork → edit → PR |
| Write a new guide | 2–4 hrs | 🔴 Very High | See guide template below |
| Build a starter kit | 4–8 hrs | 🔴 Very High | See starter kit standards |
| Translate a guide | 2–4 hrs | 🟠 High | See translation guide |
| Report an error | 5 min | 🟡 Medium | Open an issue |

---

## 🚦 Before You Start

### For small changes (typos, broken links, minor updates):
1. Click the **Edit** button directly on GitHub
2. Make your change
3. Submit the PR with a clear title

### For new guides or major additions:
1. **Open an issue first** using the [New Topic template](.github/ISSUE_TEMPLATE/new_topic.md)
2. Wait for a maintainer to approve the direction (usually within 48 hours)
3. This prevents duplicate work and ensures quality alignment

> ⚠️ **PRs for new guides without a linked, approved issue may be closed.** This isn't to be harsh — it's to protect your time.

---

## 📐 Content Standards

Every guide in this handbook must meet these standards. No exceptions.

### ✅ Required in every guide

```markdown
# [Title]

> **TL;DR:** One sentence that tells the reader exactly what they'll learn.

## When to Use This

[1-2 paragraphs on the problem this solves and who it's for]

## Core Concept

[The mental model or architecture — use a diagram if helpful]

## Implementation

[Working, tested code example with the correct language tag]

## Production Considerations

[What breaks at scale, what to watch out for, real tradeoffs]

## Further Reading

- [Resource 1](url) — Why it's valuable
- [Resource 2](url) — Why it's valuable
- [Resource 3](url) — Why it's valuable
```

### ❌ What we reject

- **Opinion pieces** without evidence (e.g., "Framework X is just better")
- **Outdated content** referencing deprecated APIs without noting it
- **Walls of text** without code, diagrams, or structure
- **Copied content** from other sources without attribution
- **Untested code** — every snippet must be runnable

---

## 🔁 Submitting a Pull Request

### 1. Fork and clone

```bash
git clone https://github.com/YOUR_USERNAME/ai-engineering-handbook.git
cd ai-engineering-handbook
```

### 2. Create a branch with a descriptive name

```bash
# For new guides:
git checkout -b guide/rag-evaluation-framework

# For fixes:
git checkout -b fix/broken-links-agent-section

# For updates:
git checkout -b update/vector-db-comparison-2026
```

### 3. Follow the file naming convention

```
docs/
  [section]/
    [kebab-case-topic-name].md

# Examples:
docs/rag/hybrid-search.md
docs/agents/tool-design.md
docs/security/prompt-injection.md
```

### 4. PR title format

```
[type]: short description

# Types:
feat:   New guide or starter kit
fix:    Correction to existing content
update: Refresh of outdated content
docs:   Meta documentation changes
refactor: Restructuring without content changes

# Examples:
feat: Add guide on LLM-as-a-Judge evaluation
fix: Correct outdated OpenAI API syntax in function-calling guide
update: Refresh vector DB comparison with 2026 benchmarks
```

### 5. Fill out the PR template completely

A PR with an empty description will be returned for revision.

---

## 🐛 Issue Guidelines

Use the correct issue template:

| Issue Type | Template | When to Use |
|---|---|---|
| 🐛 Bug / Error | `bug_report.md` | Incorrect information, broken code, dead links |
| ✍️ New Topic | `new_topic.md` | Proposing a guide that doesn't exist yet |
| 🔗 Add Resource | `add_resource.md` | Suggesting a tool, paper, or course |
| 💡 Enhancement | `enhancement.md` | Improving an existing guide |

**Good issue titles:**
- ✅ `[Bug] Code example in rag/chunking.md throws TypeError on Python 3.11`
- ✅ `[New Topic] Guide needed: Implementing semantic caching with Redis`
- ❌ `Something is wrong`
- ❌ `Add more stuff`

---

## ✍️ Style Guide

### Markdown rules

- Use `##` for top-level sections (never `#` inside a guide — that's reserved for the title)
- Every code block **must** have a language tag: ` ```python `, ` ```bash `, ` ```json `
- Use `>` blockquotes for **TL;DRs** and **important callouts** only — not for general text
- Use `⚠️` for warnings, `💡` for tips, `🚀` for quick-start callouts

### Code standards

```python
# ✅ GOOD: Complete, runnable, with comments explaining why (not just what)
from anthropic import Anthropic

client = Anthropic()

# Use streaming for better UX on long responses
with client.messages.stream(
    model="claude-opus-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Explain RAG in one paragraph"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

```python
# ❌ BAD: Incomplete, no context, unexplained
response = client.complete(prompt)
print(response)
```

### Difficulty labels

Use these consistently in all tables:

| Label | Meaning |
|---|---|
| 🟢 Beginner | No prior AI engineering knowledge needed |
| 🟡 Intermediate | Comfortable with LLM APIs, basic Python |
| 🔴 Advanced | Production experience required |

---

## 🏆 Recognition

We believe contributors deserve credit.

### Automatic recognition
- All merged PR authors are added to the **Contributors** section of the README automatically via [contrib.rocks](https://contrib.rocks)
- Significant contributors are added to the **Hall of Fame** in [CONTRIBUTORS.md](CONTRIBUTORS.md)

### Hall of Fame tiers

| Tier | Threshold | Badge |
|---|---|---|
| 🥉 Contributor | 1 merged PR | `contributor` badge |
| 🥈 Author | 3+ merged guides | `author` badge |
| 🥇 Core Maintainer | Ongoing significant contributions | `maintainer` badge |

### Special recognition
PRs that receive **50+ reactions** on the linked issue get a **⭐ Featured** tag in the relevant section.

---

## ❓ Questions?

- **General questions:** [GitHub Discussions](https://github.com/yourusername/ai-engineering-handbook/discussions)
- **Private concerns:** Open a blank issue titled `[Private] your subject`
- **Maintainers:** Tagged as `@maintainers` in any issue or discussion

---

*Thank you for making this handbook better for every AI engineer who finds it.* 🙏

## Issue Templates and PR Template
## File: .github/ISSUE_TEMPLATE/bug_report.md
---
name: 🐛 Bug Report / Incorrect Content
about: Report incorrect information, broken code, or dead links
title: "[Bug] "
labels: ["bug", "needs-review"]
assignees: ''
---

**📍 Where is the issue?**
File path (e.g., `docs/rag/chunking.md`, line 42):

**🐛 What is wrong?**
A clear description of what is incorrect, outdated, or broken.

**✅ What should it say / do instead?**
The correct information, working code, or valid link.

**🌍 Context (optional)**
- Your Python version:
- Relevant library versions:
- Any error messages:

---
## File: .github/ISSUE_TEMPLATE/new_topic.md
---
name: ✍️ Propose New Topic
about: Suggest a guide that doesn't exist yet
title: "[New Topic] "
labels: ["new-content", "needs-approval"]
assignees: ''
---

**📌 Topic Title**
What would the guide be called?

**🎯 TL;DR**
One sentence: what does a reader learn from this guide?

**👤 Target Audience**
Who is this for? What do they need to know first?

**📐 Proposed Outline**
List the 4–6 main sections you'd cover:
1.
2.
3.
4.

**🔥 Why does this belong in the handbook?**
What makes this high-value for production AI engineers?

**✋ Will you write this?**
- [ ] Yes, I'll write the first draft
- [ ] I'm proposing it for someone else to write

---
## File: .github/ISSUE_TEMPLATE/add_resource.md
---
name: 🔗 Add Resource / Tool
about: Suggest a paper, tool, course, or video to add
title: "[Resource] "
labels: ["resource", "needs-review"]
assignees: ''
---

**📎 Resource URL**

**📂 Which section does this belong in?**
(e.g., RAG & Retrieval Systems → Curated Resources)

**💡 Why is this high-quality?**
What makes this resource better than the existing ones?

**🗓️ Published / Last Updated**
(Resources older than 18 months require justification for inclusion)

---
## File: .github/PULL_REQUEST_TEMPLATE.md

## What does this PR do?

> Replace this line with a one-sentence summary.

**Type of change:**
- [ ] 🐛 Fix (incorrect info, broken code, dead link)
- [ ] ✍️ New guide
- [ ] 🔄 Update to existing guide
- [ ] 🔗 New resource added
- [ ] 🚀 New starter kit
- [ ] 🔧 Meta / infrastructure change

**Linked issue:** Closes #

---

## Content Checklist

Before submitting, confirm your PR meets handbook standards:

### For all PRs:
- [ ] All code blocks have a language tag (` ```python `, ` ```bash `, etc.)
- [ ] All links are working (tested them manually)
- [ ] No walls of text — content uses headers, tables, or bullets
- [ ] Spell-checked and grammar-checked

### For new guides only:
- [ ] Guide starts with a `> **TL;DR:**` blockquote
- [ ] Includes a working, tested code example
- [ ] Includes a "Further Reading" section with 3+ resources
- [ ] Difficulty level is labeled (🟢 / 🟡 / 🔴)
- [ ] Added to the correct table in `README.md`
- [ ] Issue was opened and approved before writing

### For starter kits only:
- [ ] Includes a `README.md` with setup instructions
- [ ] Includes a `requirements.txt` or `package.json`
- [ ] Tested from a clean environment (fresh clone → works)
- [ ] Deploy badge is working

---

## Screenshots / Output (if applicable)

Paste terminal output, rendered markdown preview, or screenshots here.

---

## Notes for Reviewers (optional)

Anything the reviewer should know? Design decisions, known limitations, or areas where feedback is especially welcome?

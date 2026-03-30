# Agent Architecture Patterns

> **TL;DR:** An agent is an LLM in a loop with tools and memory. The patterns you choose for that loop determine whether your agent is reliable or a liability.

---

## Table of Contents

- [What Makes an Agent an Agent](#what-makes-an-agent-an-agent)
- [Core Architecture Patterns](#core-architecture-patterns)
- [The Tool Layer](#the-tool-layer)
- [The Memory Layer](#the-memory-layer)
- [The Safety Layer](#the-safety-layer)
- [Production Code Example](#production-code-example)
- [Common Failure Modes](#common-failure-modes)
- [Further Reading](#further-reading)

---

## What Makes an Agent an Agent

A chatbot answers questions. An agent **takes actions**.

```
Chatbot:  User → LLM → Response
Agent:    User → LLM → Tool call → Result → LLM → Tool call → ... → Response
```

Three properties define an agent:
1. **Planning** — breaks a goal into steps
2. **Tool use** — executes actions in external systems
3. **Memory** — retains state across steps

All three must be production-hardened independently.

---

## Core Architecture Patterns

### Pattern 1: ReAct (Reasoning + Acting)

The most widely used agent pattern. The model alternates between reasoning about what to do and acting on that reasoning.

```
Thought: I need to find the current price of AAPL stock
Action: web_search("AAPL stock price today")
Observation: AAPL is trading at $189.42
Thought: Now I can answer the user's question
Answer: AAPL is currently trading at $189.42
```

**Best for:** General-purpose agents with unpredictable task structures.
**Watch out for:** Reasoning loops — the model can get stuck in circular thought chains.

---

### Pattern 2: Plan-and-Execute

A dedicated **planner** LLM creates a full task plan upfront. A separate **executor** LLM runs each step.

```
┌──────────────┐     Full plan      ┌───────────────────────────────┐
│   PLANNER    │ ─────────────────→ │ Step 1: search_web(query)     │
│  (GPT-4o /   │                    │ Step 2: extract_data(results)  │
│  Claude Opus)│                    │ Step 3: write_report(data)     │
└──────────────┘                    └──────────────┬────────────────┘
                                                   │
                                    ┌──────────────▼────────────────┐
                                    │   EXECUTOR (Claude Haiku)      │
                                    │   Runs each step sequentially  │
                                    └───────────────────────────────┘
```

**Best for:** Long multi-step tasks where you want predictable execution.
**Watch out for:** Plans becoming stale if early steps produce unexpected results.

---

### Pattern 3: Multi-Agent (Supervisor + Specialists)

A supervisor agent routes subtasks to specialist agents. Each specialist is an expert in one domain.

```
                    ┌──────────────────┐
                    │   SUPERVISOR     │
                    │  (Orchestrator)  │
                    └──┬───────┬───┬───┘
                       │       │   │
              ┌────────┘   ┌───┘   └────────┐
              ▼            ▼                ▼
        ┌──────────┐ ┌──────────┐    ┌──────────┐
        │  Search  │ │  Code    │    │  Writer  │
        │  Agent   │ │  Agent   │    │  Agent   │
        └──────────┘ └──────────┘    └──────────┘
```

**Best for:** Complex workflows that require diverse skill sets.
**Watch out for:** Communication overhead between agents — keep interfaces clean and typed.

---

### Pattern 4: Reflexion (Self-Correcting)

The agent evaluates its own output and iteratively improves it before returning to the user.

```
Action → Result → Self-evaluation → [Pass] → Return to user
                       ↓
                    [Fail] → Reflect on failure → Retry with new approach
                                    ↑__________________________|
```

**Best for:** Tasks with clear success criteria (code that must run, math that must be correct).
**Watch out for:** Infinite reflection loops — always set a max retry limit.

---

## The Tool Layer

### Designing Tools the Model Can Use Reliably

Tool schemas are your agent's API contract. Ambiguous schemas = unpredictable tool calls.

```python
# ❌ BAD: Vague schema, model guesses parameters
{
    "name": "search",
    "description": "Search for stuff",
    "parameters": {
        "query": {"type": "string"}
    }
}

# ✅ GOOD: Precise schema, constrained behavior
{
    "name": "web_search",
    "description": "Search the web for current information. Use for facts, news, and data that may have changed after your training cutoff. Do NOT use for general knowledge questions.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query. Be specific. Max 100 characters.",
                "maxLength": 100
            },
            "num_results": {
                "type": "integer",
                "description": "Number of results to return. Default 5, max 10.",
                "default": 5,
                "minimum": 1,
                "maximum": 10
            }
        },
        "required": ["query"]
    }
}
```

### Tool Execution Safety Rules

| Rule | Why |
|---|---|
| Sandbox all code execution | Agents will write and run destructive code if unsandboxed |
| Set timeouts on every tool | A hanging tool call hangs your entire agent loop |
| Log every tool call and result | Debugging agents without logs is nearly impossible |
| Validate tool outputs before passing to LLM | Garbage tool output → garbage reasoning |
| Rate-limit external API tools | Agents will hammer APIs until they get a good result |

---

## The Memory Layer

Agents need memory at three different timescales:

```
┌─────────────────────────────────────────────────────────────┐
│  IN-CONTEXT MEMORY (seconds → minutes)                      │
│  The current conversation. Limited by context window.       │
│  Use: Immediate task history, current reasoning chain       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  EXTERNAL MEMORY (minutes → hours)                          │
│  Vector DB of past interactions and intermediate results.   │
│  Use: Recall facts from earlier in a long session           │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  PERSISTENT MEMORY (days → forever)                         │
│  Structured storage of user preferences, learned facts.     │
│  Use: Personalization, cross-session continuity             │
└─────────────────────────────────────────────────────────────┘
```

### When to use each:

```python
# In-context: just include in messages array — nothing special needed

# External (vector): retrieve relevant past interactions
def recall_relevant(query: str, session_id: str) -> list[str]:
    return vector_db.search(
        filter={"session_id": session_id},
        query_vector=embed(query),
        limit=3
    )

# Persistent: structured key-value store
def save_preference(user_id: str, key: str, value: str):
    db.execute(
        "INSERT INTO user_memory (user_id, key, value) VALUES (?, ?, ?)",
        (user_id, key, value)
    )
```

---

## The Safety Layer

### The Four Controls

Every production agent needs all four:

```python
class AgentSafetyLayer:
    def __init__(self):
        self.max_iterations = 10       # Hard stop on runaway loops
        self.max_cost_usd = 0.50       # Budget cap per run
        self.dangerous_tools = {       # Tools that require confirmation
            "delete_file", "send_email", "execute_sql", "make_payment"
        }
        self.current_iterations = 0
        self.current_cost = 0.0

    def check_iteration_limit(self):
        self.current_iterations += 1
        if self.current_iterations > self.max_iterations:
            raise AgentError("Max iterations reached. Stopping to prevent runaway loop.")

    def check_budget(self, estimated_cost: float):
        self.current_cost += estimated_cost
        if self.current_cost > self.max_cost_usd:
            raise AgentError(f"Budget cap of ${self.max_cost_usd} reached. Stopping.")

    def requires_confirmation(self, tool_name: str) -> bool:
        return tool_name in self.dangerous_tools

    def confirm_with_human(self, tool_name: str, tool_args: dict) -> bool:
        # In production: send to approval queue, webhook, or UI
        print(f"\n⚠️  Agent wants to call: {tool_name}")
        print(f"   Arguments: {tool_args}")
        response = input("   Allow? (y/n): ")
        return response.lower() == "y"
```

---

## Production Code Example

A complete ReAct agent with safety controls:

```python
# Full working ReAct agent
# Requirements: anthropic

import anthropic
import json
from typing import Any

client = anthropic.Anthropic()

# Define tools
TOOLS = [
    {
        "name": "calculator",
        "description": "Perform mathematical calculations. Use for any arithmetic.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "A valid Python math expression, e.g. '2 + 2' or '100 * 0.15'"
                }
            },
            "required": ["expression"]
        }
    },
    {
        "name": "get_weather",
        "description": "Get current weather for a city.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City name"}
            },
            "required": ["city"]
        }
    }
]

def execute_tool(tool_name: str, tool_input: dict) -> Any:
    """Execute a tool call and return the result."""
    if tool_name == "calculator":
        try:
            # Safe eval — only allow math operations
            result = eval(tool_input["expression"], {"__builtins__": {}})
            return {"result": result}
        except Exception as e:
            return {"error": str(e)}
    
    elif tool_name == "get_weather":
        # In production: call a real weather API
        return {"city": tool_input["city"], "temperature": "72°F", "condition": "Sunny"}
    
    return {"error": f"Unknown tool: {tool_name}"}

def run_agent(user_message: str, max_iterations: int = 10) -> str:
    """Run a ReAct agent loop until completion or max iterations."""
    messages = [{"role": "user", "content": user_message}]
    
    for iteration in range(max_iterations):
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1024,
            tools=TOOLS,
            messages=messages
        )
        
        # No more tool calls — agent is done
        if response.stop_reason == "end_turn":
            final_text = next(
                block.text for block in response.content 
                if hasattr(block, "text")
            )
            return final_text
        
        # Process tool calls
        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"🔧 Calling tool: {block.name}({block.input})")
                    result = execute_tool(block.name, block.input)
                    print(f"   Result: {result}")
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result)
                    })
            
            messages.append({"role": "user", "content": tool_results})
    
    return "Max iterations reached without a final answer."

# Usage
if __name__ == "__main__":
    answer = run_agent("What is 15% of 847, and what's the weather in Tokyo?")
    print(f"\n✅ Final answer: {answer}")
```

---

## Common Failure Modes

| Failure | Symptom | Fix |
|---|---|---|
| Reasoning loops | Agent calls same tool repeatedly | Add iteration limit + loop detection |
| Tool call hallucination | Agent invents tool arguments | Tighten tool schemas, add validation |
| Context overflow | Agent loses track of early steps | Implement memory summarization |
| Runaway cost | Single agent run costs $50+ | Add per-run budget cap |
| Dangerous tool misuse | Agent deletes data or sends emails | Require human confirmation for irreversible tools |
| No stopping condition | Agent never returns to user | Ensure `end_turn` path exists in every flow |

---

## Further Reading

- [ReAct: Synergizing Reasoning and Acting](https://arxiv.org/abs/2210.03629) — The foundational ReAct paper
- [Anthropic Agent Docs](https://docs.anthropic.com/en/docs/build-with-claude/tool-use) — Tool use and agent patterns with Claude
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/) — Graph-based agent orchestration framework
- [Reflexion Paper](https://arxiv.org/abs/2303.11366) — Self-reflective agents that learn from failure
- [The Practical Guide to Building Agents](https://www.anthropic.com/research/building-effective-agents) — Anthropic's production agent guide

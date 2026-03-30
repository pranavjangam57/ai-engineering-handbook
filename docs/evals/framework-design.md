# Eval Framework Design

> **TL;DR:** Evals are the unit tests of AI engineering. Without them, every prompt change is a gamble. With them, you ship with confidence.

---

## Table of Contents

- [Why Evals Are Non-Negotiable](#why-evals-are-non-negotiable)
- [The Three Types of Evals](#the-three-types-of-evals)
- [Building Your Golden Dataset](#building-your-golden-dataset)
- [Evaluation Metrics](#evaluation-metrics)
- [LLM-as-a-Judge](#llm-as-a-judge)
- [Eval Pipeline Architecture](#eval-pipeline-architecture)
- [Production Code Example](#production-code-example)
- [Common Mistakes](#common-mistakes)
- [Further Reading](#further-reading)

---

## Why Evals Are Non-Negotiable

Without evals, you will ship a prompt change that:
- Fixes one bug and introduces three others
- Works perfectly in English but breaks in Spanish
- Passes your manual tests but fails on edge cases you never thought of

This is not hypothetical — it happens to every team that skips evals.

```
Teams without evals:
  Change prompt → manually test 5 cases → deploy → wake up to incident

Teams with evals:
  Change prompt → run 500 automated evals → see regression → fix before deploy
```

---

## The Three Types of Evals

Every production eval suite needs all three:

### Type 1: Deterministic Evals (fastest, most reliable)

Test cases where the correct answer is exact and objective.

```python
# Good for: structured output, classification, factual extraction

test_cases = [
    {
        "input": "Extract the invoice total from: 'Invoice #1234 Total: $847.50'",
        "expected": {"total": 847.50, "invoice_number": "1234"},
        "eval_fn": lambda output, expected: output == expected
    },
    {
        "input": "Classify sentiment: 'This product is absolutely terrible'",
        "expected": "negative",
        "eval_fn": lambda output, expected: output.lower() == expected
    }
]
```

**When to use:** Any time you have a ground-truth answer. Always prefer this over LLM-as-judge when possible.

---

### Type 2: LLM-as-a-Judge (flexible, scalable)

Use a model to evaluate outputs that don't have a single correct answer.

```python
# Good for: open-ended Q&A, writing quality, helpfulness, safety

test_cases = [
    {
        "input": "Explain quantum entanglement to a 10-year-old",
        "criteria": [
            "Uses simple, age-appropriate language",
            "No unexplained technical jargon",
            "Includes an analogy or real-world example",
            "Is factually accurate"
        ]
    }
]
```

**When to use:** Open-ended generation tasks where there are many valid outputs.

---

### Type 3: Human Evals (gold standard, expensive)

Real humans rate outputs. Use sparingly — only for critical decisions.

**When to use:**
- Calibrating your LLM-as-judge prompts
- Final quality gate before major releases
- Tasks involving cultural nuance or subjective judgment

**Sample size rule of thumb:** 50–200 human-rated examples is sufficient to calibrate automated evals. Don't over-invest here.

---

## Building Your Golden Dataset

Your golden dataset is the foundation of your entire eval suite. Garbage in, garbage out.

### Where to source examples

| Source | Quality | Volume | Effort |
|---|---|---|---|
| Real production logs | ⭐⭐⭐⭐⭐ | High | Medium |
| Customer support tickets | ⭐⭐⭐⭐ | High | Low |
| Manually crafted edge cases | ⭐⭐⭐⭐⭐ | Low | High |
| Synthetic generation | ⭐⭐⭐ | Very high | Low |
| Public benchmarks | ⭐⭐⭐ | High | Very low |

**Start with production logs.** They capture the actual distribution of what your users ask — not what you think they ask.

### Dataset size guidelines

| Use Case | Minimum Dataset Size |
|---|---|
| Smoke test (catch regressions) | 50–100 examples |
| Reliable quality measurement | 200–500 examples |
| Statistical significance | 1,000+ examples |
| Edge case coverage | 500+ targeted edge cases |

### Dataset hygiene rules

```python
# Every eval example must have:
eval_example = {
    "id": "unique_id",                 # For tracking regressions
    "input": "user message",           # Exact input to the model
    "context": {},                     # Any system context, user data, etc.
    "expected_output": "...",          # Ground truth (if deterministic)
    "criteria": [],                    # Evaluation rubric (if LLM-as-judge)
    "tags": ["edge_case", "language:es"], # For filtering and analysis
    "created_at": "2026-01-15",        # For tracking dataset drift
    "source": "production_log"         # Where this example came from
}
```

---

## Evaluation Metrics

Choose metrics based on your task type:

### For classification tasks

```python
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix

def evaluate_classifier(predictions: list, ground_truth: list) -> dict:
    return {
        "accuracy": accuracy_score(ground_truth, predictions),
        "f1_macro": f1_score(ground_truth, predictions, average="macro"),
        "confusion_matrix": confusion_matrix(ground_truth, predictions).tolist()
    }
```

### For generation tasks

| Metric | What it measures | Use when |
|---|---|---|
| ROUGE-L | Overlap with reference text | Summarization |
| BERTScore | Semantic similarity | Paraphrase, translation |
| BLEU | N-gram precision | Machine translation |
| Custom rubric score | Task-specific quality | Most production tasks |
| Pass@k | Code correctness | Code generation |

### For RAG tasks

| Metric | What it measures |
|---|---|
| Faithfulness | Does the answer come from the context? |
| Answer relevance | Does the answer address the question? |
| Context relevance | Are retrieved chunks actually relevant? |
| Context recall | Did retrieval find all necessary information? |

---

## LLM-as-a-Judge

### The Judge Prompt Template

```python
JUDGE_PROMPT = """You are an expert evaluator. Score the following AI response.

## Task
{task_description}

## User Input
{user_input}

## AI Response to Evaluate
{ai_response}

## Evaluation Criteria
Score each criterion from 1-5:
{criteria_list}

## Output Format
Respond with a JSON object only:
{{
  "scores": {{
    "criterion_name": score,
    ...
  }},
  "overall_score": average_score,
  "reasoning": "brief explanation of the scores",
  "pass": true/false  // true if overall_score >= 3.5
}}"""

def judge_response(
    task_description: str,
    user_input: str,
    ai_response: str,
    criteria: list[str],
    judge_model: str = "claude-opus-4-6"
) -> dict:
    import anthropic, json
    
    client = anthropic.Anthropic()
    criteria_list = "\n".join([f"- {c}" for c in criteria])
    
    response = client.messages.create(
        model=judge_model,
        max_tokens=500,
        messages=[{
            "role": "user",
            "content": JUDGE_PROMPT.format(
                task_description=task_description,
                user_input=user_input,
                ai_response=ai_response,
                criteria_list=criteria_list
            )
        }]
    )
    
    return json.loads(response.content[0].text)
```

### Calibrating Your Judge

An uncalibrated judge is worse than no judge. Before using LLM-as-judge in production:

1. **Create a calibration set:** 50–100 examples with human ratings
2. **Run your judge:** Compare judge scores to human scores
3. **Target correlation:** Pearson r > 0.8 between judge and human scores
4. **Iterate on the prompt** until you hit that threshold

---

## Eval Pipeline Architecture

```
┌───────────────────────────────────────────────────────────┐
│                    EVAL PIPELINE                          │
│                                                           │
│  1. Load golden dataset                                   │
│         ↓                                                 │
│  2. Run model on all inputs (parallel, batched)           │
│         ↓                                                 │
│  3. Score each output                                     │
│     ├── Deterministic: exact match / regex               │
│     └── LLM-as-judge: send to judge model                │
│         ↓                                                 │
│  4. Aggregate metrics                                     │
│     ├── Overall pass rate                                 │
│     ├── Per-tag breakdown (language, task type)          │
│     └── Regression vs. previous run                      │
│         ↓                                                 │
│  5. Generate report + alert on regressions               │
└───────────────────────────────────────────────────────────┘
```

---

## Production Code Example

A complete eval pipeline:

```python
# Complete eval runner — tested with Python 3.11
# Requirements: anthropic, tqdm, pandas

import anthropic
import json
import pandas as pd
from tqdm import tqdm
from dataclasses import dataclass
from typing import Callable

@dataclass
class EvalCase:
    id: str
    input: str
    expected: str | None = None
    criteria: list[str] | None = None
    tags: list[str] = None

@dataclass
class EvalResult:
    case_id: str
    output: str
    score: float
    passed: bool
    reasoning: str = ""

class EvalRunner:
    def __init__(self, model: str = "claude-sonnet-4-6"):
        self.client = anthropic.Anthropic()
        self.model = model
        self.judge_model = "claude-opus-4-6"  # Use best model for judging

    def run_model(self, prompt: str, system: str = "") -> str:
        """Run the model being evaluated."""
        messages = [{"role": "user", "content": prompt}]
        kwargs = {"model": self.model, "max_tokens": 1024, "messages": messages}
        if system:
            kwargs["system"] = system
        response = self.client.messages.create(**kwargs)
        return response.content[0].text

    def score_deterministic(self, output: str, expected: str) -> EvalResult:
        """Exact match scoring."""
        passed = output.strip().lower() == expected.strip().lower()
        return EvalResult(
            case_id="",
            output=output,
            score=1.0 if passed else 0.0,
            passed=passed,
            reasoning="Exact match" if passed else f"Expected: {expected}"
        )

    def score_with_judge(self, input: str, output: str, criteria: list[str]) -> EvalResult:
        """LLM-as-judge scoring."""
        criteria_str = "\n".join([f"- {c}" for c in criteria])
        judge_prompt = f"""Score this AI response. Return JSON only.

Input: {input}
Response: {output}

Criteria (score 1-5 each):
{criteria_str}

Return: {{"scores": {{}}, "overall_score": 0.0, "reasoning": "", "pass": false}}"""
        
        result = self.client.messages.create(
            model=self.judge_model,
            max_tokens=500,
            messages=[{"role": "user", "content": judge_prompt}]
        )
        
        try:
            judgment = json.loads(result.content[0].text)
            score = judgment["overall_score"] / 5.0  # Normalize to 0-1
            return EvalResult(
                case_id="",
                output=output,
                score=score,
                passed=judgment["pass"],
                reasoning=judgment["reasoning"]
            )
        except json.JSONDecodeError:
            return EvalResult(case_id="", output=output, score=0.0, passed=False,
                            reasoning="Judge returned invalid JSON")

    def run_suite(self, cases: list[EvalCase], system: str = "") -> pd.DataFrame:
        """Run full eval suite and return results DataFrame."""
        results = []
        
        for case in tqdm(cases, desc="Running evals"):
            output = self.run_model(case.input, system)
            
            if case.expected:
                result = self.score_deterministic(output, case.expected)
            elif case.criteria:
                result = self.score_with_judge(case.input, output, case.criteria)
            else:
                raise ValueError(f"Case {case.id} needs either 'expected' or 'criteria'")
            
            result.case_id = case.id
            results.append({
                "id": case.id,
                "input": case.input[:100] + "...",
                "output": output[:100] + "...",
                "score": result.score,
                "passed": result.passed,
                "reasoning": result.reasoning,
                "tags": case.tags
            })
        
        df = pd.DataFrame(results)
        
        # Print summary
        pass_rate = df["passed"].mean()
        avg_score = df["score"].mean()
        print(f"\n{'='*50}")
        print(f"EVAL RESULTS — {self.model}")
        print(f"{'='*50}")
        print(f"Pass rate:  {pass_rate:.1%} ({df['passed'].sum()}/{len(df)})")
        print(f"Avg score:  {avg_score:.3f}")
        print(f"{'='*50}")
        
        return df


# Usage
if __name__ == "__main__":
    runner = EvalRunner(model="claude-sonnet-4-6")
    
    test_cases = [
        EvalCase(
            id="sentiment_001",
            input="Classify the sentiment: 'This is the worst product I've ever bought'",
            expected="negative",
            tags=["sentiment", "classification"]
        ),
        EvalCase(
            id="explain_001",
            input="Explain what an API is to a non-technical person",
            criteria=[
                "Avoids jargon or explains any technical terms used",
                "Uses a relatable analogy",
                "Is accurate",
                "Is concise (under 100 words)"
            ],
            tags=["explanation", "non-technical"]
        ),
    ]
    
    results_df = runner.run_suite(test_cases)
    results_df.to_csv("eval_results.csv", index=False)
```

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| Testing only happy paths | Miss 90% of real failures | Source examples from production logs |
| Tiny golden dataset (<50 examples) | Metrics are statistically meaningless | Minimum 200 examples for reliable measurement |
| Uncalibrated LLM judge | Judge scores don't correlate with quality | Validate judge against 50+ human ratings |
| Running evals manually | Nobody runs them | Integrate into CI/CD as a blocking gate |
| Never updating the dataset | Eval suite drifts from production reality | Add 10% new examples monthly from prod logs |
| Optimizing one metric | Improve ROUGE, destroy faithfulness | Track a dashboard of 3–5 metrics together |

---

## Further Reading

- [RAGAS: Evaluation Framework for RAG](https://docs.ragas.io) — RAG-specific eval metrics
- [Langfuse Evaluation Docs](https://langfuse.com/docs/scores/overview) — Production eval tracking and observability
- [LLM-as-a-Judge Paper](https://arxiv.org/abs/2306.05685) — Original research on using models to evaluate models
- [Anthropic Eval Cookbook](https://github.com/anthropics/anthropic-cookbook) — Practical eval examples from Anthropic
- [Confident AI (DeepEval)](https://docs.confident-ai.com) — Open-source LLM evaluation framework

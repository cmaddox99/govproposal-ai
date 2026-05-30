---
skill:
  id: skill-21-prompt-engineering
  name: Prompt Engineering
  category: ai-development
  version: "2.0.0"

laws:
  implements:
    - id: PRD-5.2
      title: Hypothesis-Driven Law
  references:
    - id: BUS-4.1
      title: GDPR Compliance Law
    - id: ENG-6.5
      title: Input Validation Law

triggers:
  phrases:
    - "Design prompts"
    - "Improve LLM output"
    - "Prompt template"
    - "Reduce hallucinations"

followed_by:
  - skill-22-rag-architecture
  - skill-24-ai-safety
---

# Skill: Prompt Engineering

> **Purpose:** Design effective prompts for Large Language Models that produce reliable, consistent, and high-quality outputs.

---

## Purpose

Prompt Engineering is the practice of crafting inputs to LLMs that elicit desired behaviors and outputs. This skill ensures:

1. **Reliability** - Consistent outputs across similar inputs
2. **Quality** - Outputs meet accuracy and relevance standards
3. **Safety** - Prompts include appropriate guardrails
4. **Efficiency** - Token usage optimized for cost and latency
5. **Maintainability** - Prompts are versioned and testable

**Key principle:** Prompts are code. Treat them with the same rigor as software.

---

## When to Invoke

Invoke this skill when:

- Building LLM-powered features
- Improving output quality from existing prompts
- Reducing hallucinations or errors
- Optimizing for cost/latency
- Creating prompt templates for reuse
- Debugging unexpected LLM behavior

**Trigger phrases:**
- "The model isn't giving good answers"
- "How do I make this more reliable?"
- "The outputs are inconsistent"
- "Can we reduce the token count?"
- "Design a prompt for this task"

---

## Constitutional Foundation

### Engineering Constitution
- **Article II, Section 2.1** - Simplicity: Prompts should be clear and focused
- **Article IV, Section 4.1** - Test-First: Prompts tested before deployment
- **Article VII, Section 7.1** - Documentation: Prompts documented

### Product Constitution
- **Article V, Section 5.1** - User Experience: Outputs meet user expectations

### Business Constitution
- **Article III, Section 3.3** - Audit Trail: Prompts versioned and tracked

---

## Prompt Anatomy

### Basic Structure

```
┌─────────────────────────────────────────────────────────────┐
│                      PROMPT STRUCTURE                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  SYSTEM PROMPT                                       │   │
│  │  - Role definition                                   │   │
│  │  - Behavioral constraints                            │   │
│  │  - Output format specification                       │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│                           ▼                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  USER PROMPT                                         │   │
│  │  - Context/Background                                │   │
│  │  - Task specification                                │   │
│  │  - Examples (few-shot)                               │   │
│  │  - Input data                                        │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│                           ▼                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  ASSISTANT RESPONSE                                  │   │
│  │  - Structured output                                 │   │
│  │  - Following specified format                        │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Core Techniques

### 1. Role Prompting

```python
# Define a clear role for the model
SYSTEM_PROMPT = """You are an expert code reviewer with 15 years of experience
in Python and software architecture. You focus on:
- Security vulnerabilities
- Performance issues
- Code maintainability
- Best practices adherence

You provide specific, actionable feedback with code examples."""
```

### 2. Chain-of-Thought (CoT)

```python
# Encourage step-by-step reasoning
COT_PROMPT = """Analyze this problem step by step:

Problem: {problem}

Think through this systematically:
1. First, identify the key components
2. Then, analyze each component
3. Consider edge cases
4. Draw your conclusion

Let's work through this step by step."""

# Zero-shot CoT (simpler version)
ZERO_SHOT_COT = """Let's think step by step.

{problem}

Work through this carefully before giving your final answer."""
```

### 3. Few-Shot Learning

```python
FEW_SHOT_PROMPT = """Classify the sentiment of customer reviews.

Examples:
Review: "This product exceeded my expectations! Fast shipping too."
Sentiment: Positive

Review: "Broke after one week. Complete waste of money."
Sentiment: Negative

Review: "It works as described. Nothing special but does the job."
Sentiment: Neutral

Now classify this review:
Review: "{user_review}"
Sentiment:"""
```

### 4. Output Formatting

```python
# JSON output
JSON_FORMAT_PROMPT = """Extract information from the text and return as JSON.

Text: {text}

Return a JSON object with this exact structure:
{
    "entities": [
        {"name": "string", "type": "string", "confidence": number}
    ],
    "summary": "string",
    "sentiment": "positive" | "negative" | "neutral"
}

Return ONLY the JSON object, no other text."""

# Structured output with schema
SCHEMA_PROMPT = """Analyze the code and return your findings.

Code:
```
{code}
```

Return your analysis in this exact format:

## Security Issues
- [List each issue]

## Performance Concerns
- [List each concern]

## Recommendations
1. [Numbered recommendations]

## Risk Level
[LOW/MEDIUM/HIGH]"""
```

---

## Advanced Techniques

### Self-Consistency

```python
import asyncio
from collections import Counter

async def self_consistent_answer(
    prompt: str,
    llm_client,
    n_samples: int = 5,
    temperature: float = 0.7
) -> str:
    """Generate multiple responses and return the most common answer."""

    # Generate multiple completions with higher temperature
    tasks = [
        llm_client.complete(prompt, temperature=temperature)
        for _ in range(n_samples)
    ]
    responses = await asyncio.gather(*tasks)

    # Extract final answers (assumes structured output)
    answers = [extract_final_answer(r) for r in responses]

    # Return most common answer
    counter = Counter(answers)
    return counter.most_common(1)[0][0]
```

### Tree of Thoughts

```python
TOT_PROMPT = """Solve this problem by exploring multiple approaches.

Problem: {problem}

For each approach:
1. Describe the approach
2. Work through it step by step
3. Evaluate: Is this promising? (Yes/No/Maybe)
4. If Yes, continue. If No, try a different approach.

Approach 1:
[Your first approach]

Evaluation 1: [Yes/No/Maybe]
Reasoning: [Why this approach is or isn't promising]

Approach 2 (if needed):
[Alternative approach]

Final Answer:
[Based on the most promising approach]"""
```

### ReAct (Reasoning + Acting)

```python
REACT_PROMPT = """You have access to these tools:
- search(query): Search the web for information
- calculate(expression): Evaluate a mathematical expression
- lookup(term): Look up a term in the knowledge base

Solve the user's question using this format:

Question: {question}

Thought: [Your reasoning about what to do next]
Action: [tool_name(argument)]
Observation: [Result of the action]
... (repeat Thought/Action/Observation as needed)
Thought: I now have enough information to answer
Final Answer: [Your answer]

Begin!

Question: {question}
Thought:"""
```

---

## Prompt Templates

### Modular Prompt System

```python
from string import Template
from dataclasses import dataclass
from typing import Optional

@dataclass
class PromptTemplate:
    """Reusable prompt template."""

    name: str
    version: str
    system_prompt: str
    user_template: str
    output_schema: Optional[dict] = None

    def render(self, **kwargs) -> dict:
        """Render the prompt with variables."""
        return {
            "system": self.system_prompt,
            "user": Template(self.user_template).safe_substitute(**kwargs)
        }


# Example templates
CODE_REVIEW_TEMPLATE = PromptTemplate(
    name="code_review",
    version="1.2.0",
    system_prompt="""You are an expert code reviewer. Provide constructive,
specific feedback focusing on bugs, security issues, and improvements.
Be direct but respectful.""",
    user_template="""Review this $language code:

```$language
$code
```

Focus areas: $focus_areas

Provide your review with specific line references and suggested fixes.""",
    output_schema={
        "issues": [{"line": "int", "severity": "str", "description": "str", "fix": "str"}],
        "summary": "str",
        "overall_rating": "int"  # 1-5
    }
)

SUMMARIZATION_TEMPLATE = PromptTemplate(
    name="summarize",
    version="1.0.0",
    system_prompt="""You are a precise summarizer. Create concise summaries
that capture the key points without losing important details.""",
    user_template="""Summarize the following $content_type in $length:

$content

Key requirements:
- Maintain factual accuracy
- Preserve important numbers and dates
- Use clear, simple language"""
)
```

### Prompt Registry

```python
class PromptRegistry:
    """Manage and version prompts."""

    def __init__(self):
        self.prompts = {}

    def register(self, template: PromptTemplate):
        """Register a prompt template."""
        key = f"{template.name}:{template.version}"
        self.prompts[key] = template

    def get(self, name: str, version: str = "latest") -> PromptTemplate:
        """Retrieve a prompt template."""
        if version == "latest":
            # Find latest version
            versions = [k for k in self.prompts if k.startswith(f"{name}:")]
            if not versions:
                raise KeyError(f"No prompt found: {name}")
            key = sorted(versions)[-1]
        else:
            key = f"{name}:{version}"

        return self.prompts[key]

    def list_versions(self, name: str) -> list[str]:
        """List all versions of a prompt."""
        return [k.split(":")[1] for k in self.prompts if k.startswith(f"{name}:")]


# Usage
registry = PromptRegistry()
registry.register(CODE_REVIEW_TEMPLATE)
registry.register(SUMMARIZATION_TEMPLATE)

# Get and render
template = registry.get("code_review", version="1.2.0")
prompt = template.render(
    language="python",
    code="def foo(): pass",
    focus_areas="security, performance"
)
```

---

## Prompt Optimization

### Token Efficiency

```python
# VERBOSE (expensive)
verbose_prompt = """
I would like you to please analyze the following piece of Python code
and provide me with a detailed explanation of what it does. Please make
sure to cover all the important aspects including the function's purpose,
its parameters, return values, and any potential issues you might notice.

Here is the code I would like you to analyze:
{code}
"""

# CONCISE (efficient)
concise_prompt = """Analyze this Python code. Cover: purpose, params, returns, issues.

```python
{code}
```"""

# Token savings: ~60%
```

### Compression Techniques

```python
def compress_context(documents: list[str], max_tokens: int) -> str:
    """Compress documents to fit token budget."""

    # Strategy 1: Summarize each document
    summaries = [summarize(doc, max_length=100) for doc in documents]

    # Strategy 2: Extract key sentences
    key_sentences = extract_key_sentences(documents, n=10)

    # Strategy 3: Remove redundancy
    unique_content = remove_redundant_info(summaries)

    # Combine within token budget
    return truncate_to_tokens(unique_content, max_tokens)
```

---

## Testing Prompts

### Prompt Evaluation Framework

```python
from dataclasses import dataclass
from typing import Callable

@dataclass
class PromptTestCase:
    """Test case for prompt evaluation."""
    input_vars: dict
    expected_output: str  # or pattern/schema
    description: str

@dataclass
class PromptEvalResult:
    passed: bool
    actual_output: str
    expected: str
    metrics: dict

class PromptEvaluator:
    """Evaluate prompt quality."""

    def __init__(self, llm_client):
        self.llm = llm_client

    async def evaluate(
        self,
        template: PromptTemplate,
        test_cases: list[PromptTestCase],
        evaluators: list[Callable] = None
    ) -> list[PromptEvalResult]:
        """Run evaluation suite."""

        results = []

        for case in test_cases:
            prompt = template.render(**case.input_vars)
            response = await self.llm.complete(prompt)

            # Default evaluators
            metrics = {
                "exact_match": response.strip() == case.expected_output.strip(),
                "contains_expected": case.expected_output in response,
                "response_length": len(response),
            }

            # Custom evaluators
            if evaluators:
                for eval_fn in evaluators:
                    metric_name, value = eval_fn(response, case.expected_output)
                    metrics[metric_name] = value

            passed = metrics.get("exact_match") or metrics.get("semantic_match", False)

            results.append(PromptEvalResult(
                passed=passed,
                actual_output=response,
                expected=case.expected_output,
                metrics=metrics
            ))

        return results

# Custom evaluator example
def semantic_similarity_evaluator(actual: str, expected: str) -> tuple:
    """Check semantic similarity using embeddings."""
    similarity = compute_cosine_similarity(
        get_embedding(actual),
        get_embedding(expected)
    )
    return ("semantic_match", similarity > 0.85)
```

### A/B Testing Prompts

```python
import random
from dataclasses import dataclass

@dataclass
class PromptVariant:
    name: str
    template: PromptTemplate
    weight: float = 0.5

class PromptABTest:
    """A/B test prompt variants."""

    def __init__(self, variants: list[PromptVariant]):
        self.variants = variants
        self.results = {v.name: [] for v in variants}

    def select_variant(self, user_id: str = None) -> PromptVariant:
        """Select variant (deterministic if user_id provided)."""
        if user_id:
            # Consistent assignment per user
            random.seed(hash(user_id))

        r = random.random()
        cumulative = 0

        for variant in self.variants:
            cumulative += variant.weight
            if r <= cumulative:
                return variant

        return self.variants[-1]

    def record_result(
        self,
        variant_name: str,
        success: bool,
        latency_ms: float,
        user_rating: int = None
    ):
        """Record result for analysis."""
        self.results[variant_name].append({
            "success": success,
            "latency_ms": latency_ms,
            "user_rating": user_rating
        })

    def get_stats(self) -> dict:
        """Get A/B test statistics."""
        stats = {}

        for name, results in self.results.items():
            if not results:
                continue

            stats[name] = {
                "n": len(results),
                "success_rate": sum(r["success"] for r in results) / len(results),
                "avg_latency": sum(r["latency_ms"] for r in results) / len(results),
                "avg_rating": (
                    sum(r["user_rating"] for r in results if r["user_rating"])
                    / len([r for r in results if r["user_rating"]])
                ) if any(r["user_rating"] for r in results) else None
            }

        return stats
```

---

## Good Examples

### Example 1: Well-Structured Classification Prompt

```python
CLASSIFICATION_PROMPT = PromptTemplate(
    name="intent_classification",
    version="2.0.0",
    system_prompt="""You are an intent classifier for a customer service system.
Classify user messages into exactly one of these categories:
- BILLING: Payment, invoices, refunds, charges
- TECHNICAL: Product issues, bugs, how-to questions
- ACCOUNT: Login, password, profile, settings
- SHIPPING: Delivery, tracking, address changes
- OTHER: Anything that doesn't fit above

Respond with ONLY the category name, nothing else.""",

    user_template="""Classify this customer message:

"$message"

Category:"""
)

# Clear role, constrained output, explicit categories
```

### Example 2: Robust Data Extraction

```python
EXTRACTION_PROMPT = """Extract structured data from this invoice.

Invoice Text:
$invoice_text

Return a JSON object with these fields (use null if not found):
{
    "invoice_number": "string",
    "date": "YYYY-MM-DD",
    "vendor_name": "string",
    "total_amount": number,
    "currency": "string (3-letter code)",
    "line_items": [
        {
            "description": "string",
            "quantity": number,
            "unit_price": number,
            "total": number
        }
    ]
}

Important:
- Dates must be in YYYY-MM-DD format
- Amounts must be numbers without currency symbols
- If a field is ambiguous, use your best judgment and note uncertainty

JSON:"""

# Clear schema, handling edge cases, explicit formatting rules
```

---

## Bad Examples (Anti-Patterns)

### Anti-Pattern 1: Vague Instructions

```python
# BAD - Vague, no structure
bad_prompt = "Analyze this text and tell me what you think: {text}"

# GOOD - Specific, structured
good_prompt = """Analyze this text for:
1. Main topic (1 sentence)
2. Key arguments (bullet points)
3. Tone (formal/informal/neutral)
4. Target audience

Text: {text}

Analysis:"""
```

### Anti-Pattern 2: No Output Format

```python
# BAD - Unpredictable output format
bad_prompt = "List the issues in this code: {code}"

# GOOD - Explicit format
good_prompt = """List issues in this code using this format:

Line [number]: [SEVERITY] - [description]
Fix: [suggested fix]

Severity levels: CRITICAL, HIGH, MEDIUM, LOW

Code:
{code}

Issues:"""
```

### Anti-Pattern 3: No Examples for Complex Tasks

```python
# BAD - Complex task with no examples
bad_prompt = "Convert this natural language query to SQL: {query}"

# GOOD - Few-shot with examples
good_prompt = """Convert natural language to SQL.

Database schema:
- users(id, name, email, created_at)
- orders(id, user_id, total, status, created_at)

Examples:
Q: "How many users signed up last month?"
SQL: SELECT COUNT(*) FROM users WHERE created_at >= DATE_SUB(NOW(), INTERVAL 1 MONTH)

Q: "What's the total revenue from completed orders?"
SQL: SELECT SUM(total) FROM orders WHERE status = 'completed'

Q: "{query}"
SQL:"""
```

---

## Quality Checklist

Before deploying a prompt:

### Design
- [ ] Clear role/persona defined
- [ ] Task explicitly stated
- [ ] Output format specified
- [ ] Edge cases handled
- [ ] Examples included (if complex task)

### Testing
- [ ] Test cases cover common inputs
- [ ] Edge cases tested
- [ ] Output format validated
- [ ] Consistency verified (run multiple times)

### Safety
- [ ] Guardrails against harmful outputs
- [ ] PII handling considered
- [ ] Failure modes graceful

### Operations
- [ ] Prompt versioned
- [ ] Token usage measured
- [ ] Latency acceptable
- [ ] Cost estimated

---

## Skill Interactions

### Preceded By
- **03-Executable Spec** - Requirements inform prompt design

### Followed By
- **22-RAG Architecture** - Prompts incorporate retrieved context
- **23-AI Agents** - Prompts drive agent behavior

### Related Skills
- **24-AI Safety** - Safe prompt design
- **06-Atomic TDD** - Test-driven prompt development

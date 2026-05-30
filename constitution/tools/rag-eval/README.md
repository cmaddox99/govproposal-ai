# RAG Evaluation Harness

Standalone evaluation framework for the Hangar AI Constitution's RAG quality.

## Overview

The harness scores how well the constitution's content supports retrieval-augmented generation across **5 dimensions**:

| Dimension | Weight | Threshold | Description |
|-----------|--------|-----------|-------------|
| `law_retrieval` | 35% | 85% | % of test questions that retrieve expected laws in top-k results |
| `skill_routing` | 25% | 80% | % of test questions routed to the correct skill via trigger phrase matching |
| `avatar_selection` | 20% | 80% | % of avatar queries resolved to the correct avatar |
| `index_integrity` | 10% | 95% | % of index entries (laws, skills, AVATAR-RAG-INDEX) that resolve to real files |
| `cross_ref_consistency` | 10% | 95% | % of law citations in skill/avatar files that are valid registered law IDs |

**Overall weighted score threshold: 85%**

## Usage

```bash
# Console output (default)
python tools/rag-eval/evaluate.py --constitution /path/to/constitution

# JSON output
python tools/rag-eval/evaluate.py --constitution /path/to/constitution --format json

# GitHub Actions annotations
python tools/rag-eval/evaluate.py --constitution /path/to/constitution --format github-actions

# Exit 1 if any threshold is breached (for CI gating)
python tools/rag-eval/evaluate.py --constitution /path/to/constitution --threshold-check

# Override top-k
python tools/rag-eval/evaluate.py --constitution /path/to/constitution --top-k 5
```

## Files

```
tools/rag-eval/
├── evaluate.py          CLI entry point (argparse, stdlib + PyYAML only)
├── retriever.py         Deterministic keyword + law ID retriever
├── scorer.py            5-dimension scoring model
├── config.yaml          Configurable thresholds and settings
├── README.md            This file
├── test-cases/
│   ├── engineering.yaml  20 test cases — ENG laws
│   ├── product.yaml      20 test cases — PRD laws
│   ├── business.yaml     15 test cases — BUS laws
│   ├── skills.yaml       15 test cases — skill trigger routing
│   └── avatars.yaml      15 test cases — avatar selection
└── reports/             Generated reports (not committed — see .gitignore)
    └── latest.json
```

## Retrieval Model

The retriever (`retriever.py`) uses three scoring signals — no embeddings, no LLM calls:

| Signal | Weight | Method |
|--------|--------|--------|
| Exact law ID match | 3.0 | Regex `[A-Z]{2,5}-\d+\.\d+` against indexed law IDs |
| Trigger phrase match | 2.0 | Substring match against skill/avatar trigger phrases |
| Keyword overlap | 1.0 | Token intersection / sqrt(vocab size) (TF-IDF-style) |

## Configuration

Edit `tools/rag-eval/config.yaml` to adjust thresholds:

```yaml
thresholds:
  law_retrieval: 0.85
  skill_routing: 0.80
  avatar_selection: 0.80
  index_integrity: 0.95
  cross_reference_consistency: 0.95
  overall: 0.85
```

## Adding Test Cases

Add YAML files to `tools/rag-eval/test-cases/` following the schema:

```yaml
test_cases:
  - id: tc-eng-001
    question: "How do I implement TDD in my project?"
    expected_laws: [ENG-4.1]
    expected_skills: [06-atomic-tdd.md]
    expected_avatars: []
    category: engineering
```

## CI Integration

The `rag-eval.yml` workflow runs this harness on every PR and push to `main`:

```yaml
- run: python tools/rag-eval/evaluate.py --format github-actions --threshold-check
```

Reports are uploaded as workflow artifacts (BUS-7.1 audit trail requirement).

## Dependencies

- Python 3.9+
- PyYAML (`pip install pyyaml`)
- No other dependencies (stdlib only for everything else)

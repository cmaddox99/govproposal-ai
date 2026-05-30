# Proposal: LLM Skill Behavioral Testing Infrastructure

**Status:** 📋 PROPOSE
**Spec ID:** `llm-skill-behavioral-testing`
**Laws:** ENG-4.1, ENG-4.2, ENG-12.1
**Motivated by:** Inability to write meaningful behavioral tests for skill routing
decisions (gateway paths, Trust Ramp branching) using the existing structural
test infrastructure. Identified during implementation of the
`pragmatic-adoption-full-workflow-gateway` proposal.

---

## Problem Statement

The constitution's skills (`.md` files under `agent-skills/`) define AI-executable
procedures with branching logic, routing decisions, and structured outputs. The
existing test suite validates:

- Law registry consistency (governance)
- RAG law-ID extraction (tooling)
- Avatar structural schema (markdown/YAML)

None of these test **whether an AI agent actually follows the skill's decision
logic correctly**. For example, given:

- User says: "I want to adopt the constitution"
- Repo has an active pragmatic adoption in `hangar-ai-specs/changes/`

Does the agent resume the in-progress adoption (Priority 1 in the gateway decision
table) or present the two-path gateway dialog? There is no test for this today.

This gap means:
1. Skill regressions are invisible until a human runs a real session and notices
2. Refactoring skill prose risks silently breaking routing behavior
3. New contributors cannot verify their skill edits without running a live AI session

---

## Solution

### Overview

Introduce a new test category: **LLM Skill Behavioral Tests** (`tests/skill-behavioral/`).

Each test:
1. Loads a skill file's prose
2. Constructs a **scenario** (simulated repo state + user utterance)
3. Sends both to a lightweight LLM (Claude Haiku or GPT-4o-mini) with a
   structured-output prompt asking: "Given this skill and this scenario, what
   would the agent do?"
4. Asserts the LLM's structured response matches the expected routing decision

Tests run as an optional CI job (`skill-behavioral` label) — not part of the
mandatory unit/governance gate. They require API credentials and are skipped
(`pytest.skip`) when `LLM_TEST_API_KEY` is not set.

---

### Scenario Definition Format

Each scenario is a YAML file:

```yaml
# tests/skill-behavioral/scenarios/pragmatic-adoption-gateway/resume-active-adoption.yaml
scenario_id: resume-active-adoption
skill: agent-skills/skills-by-domain/development-practices/02-constitutional-companion.md
description: >
  User says "I want to adopt the constitution" but an active pragmatic adoption
  proposal already exists in hangar-ai-specs/changes/. Agent should resume, not
  re-present the gateway.
user_utterance: "I want to adopt the constitution"
repo_state:
  files_present:
    - AGENTS.md
    - hangar-ai-specs/changes/adoption-iteration-1/PROPOSAL.md
    - hangar-ai-specs/changes/adoption-iteration-1/tasks.md
  files_absent:
    - hangar-ai-specs/archive/adoption-iteration-1/
expected:
  path_taken: resume_active_adoption        # matches Priority 1 in decision table
  gateway_presented: false
  rationale_contains: "active pragmatic adoption"
```

---

### Test Runner Architecture

```
tests/skill-behavioral/
├── conftest.py                   ← LLM client fixture; skip if no API key
├── scenarios/
│   ├── pragmatic-adoption-gateway/
│   │   ├── resume-active-adoption.yaml
│   │   ├── already-adopted-skip-gateway.yaml
│   │   ├── no-artifacts-present-full-gateway.yaml
│   │   ├── user-chooses-path-a.yaml
│   │   └── user-chooses-path-b.yaml
│   └── [other-skill-scenarios]/
├── test_skill_routing.py         ← parametrized test over all scenario files
└── evaluator_prompt.md           ← the structured-output prompt sent to the LLM
```

### Evaluator Prompt Strategy

The LLM is asked to act as an **evaluator**, not as the agent itself. It is given:

1. The full skill prose (without the YAML frontmatter, to avoid meta-confusion)
2. The simulated repo state as a structured context block
3. The user utterance
4. A JSON schema it must respond with

```
Given the following AI skill procedure and the described scenario, determine
which decision branch the skill's Step 0a logic would take. Respond ONLY with
valid JSON matching this schema:

{
  "path_taken": "<string: one of resume_active_adoption | skip_gateway_already_adopted | update_context | full_gateway>",
  "gateway_presented": <boolean>,
  "confidence": <float 0.0–1.0>,
  "rationale": "<string: 1–2 sentence explanation>"
}
```

### Assertion Strategy

```python
@pytest.mark.parametrize("scenario", load_scenarios("pragmatic-adoption-gateway"))
def test_skill_routing(scenario, llm_evaluator):
    result = llm_evaluator.evaluate(scenario)
    assert result["path_taken"] == scenario["expected"]["path_taken"], (
        f"Wrong path for scenario '{scenario['scenario_id']}': "
        f"expected {scenario['expected']['path_taken']}, got {result['path_taken']}. "
        f"Rationale: {result['rationale']}"
    )
    assert result["gateway_presented"] == scenario["expected"]["gateway_presented"]
    if "rationale_contains" in scenario["expected"]:
        assert scenario["expected"]["rationale_contains"].lower() in result["rationale"].lower()
```

---

### LLM Selection

| Model | Rationale |
|---|---|
| **Claude Haiku (primary)** | Fast, cheap, good at structured JSON output, same family as Copilot backend |
| **GPT-4o-mini (secondary)** | Cross-model validation; detects skill prose that only works with one LLM's interpretation |
| **Ollama (local, optional)** | Zero-cost local run; useful for dev loop; lower accuracy acceptable for smoke tests |

Model is selected via `LLM_TEST_MODEL` env var; defaults to `claude-haiku`.

---

### CI Integration

```yaml
# .github/workflows/skill-behavioral-tests.yml
name: Skill Behavioral Tests
on:
  pull_request:
    paths:
      - 'agent-skills/**/*.md'
      - 'tests/skill-behavioral/**'
jobs:
  skill-behavioral:
    runs-on: ubuntu-latest
    if: vars.RUN_SKILL_BEHAVIORAL_TESTS == 'true'   # opt-in org variable
    env:
      LLM_TEST_API_KEY: ${{ secrets.LLM_TEST_API_KEY }}
      LLM_TEST_MODEL: claude-haiku
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install pytest pyyaml anthropic openai
      - run: pytest tests/skill-behavioral/ -m skill_behavioral -v
```

Tests are **opt-in** at the org level via `vars.RUN_SKILL_BEHAVIORAL_TESTS`. This
prevents unintended API spend on forks and draft PRs.

---

## Relationship to Existing Tests

| Existing test category | Tests | Relationship |
|---|---|---|
| Governance (`tests/unit/laws/`) | Law registry, domain YAML | Unchanged |
| Constitution lint (`tests/unit/test_constitution_lint/`) | Structural lint rules | Unchanged |
| RAG eval (`tests/unit/test_rag_eval/`) | Law ID extraction | Unchanged |
| **Skill behavioral (new)** | AI routing decisions, path branching | New category; opt-in CI |

---

## What This Enables

1. **Regression protection for skills** — refactoring skill prose does not silently break routing
2. **Scenario-driven skill development** — write the scenario before writing the skill section (TDD for AI behavior)
3. **Cross-model consistency** — detect skill prose that is LLM-family-specific
4. **Contribution confidence** — contributors can verify skill edits without a live AI session

---

## Changes

| Artifact | Change |
|----------|--------|
| `tests/skill-behavioral/` | New directory with conftest, scenarios, evaluator prompt |
| `tests/skill-behavioral/test_skill_routing.py` | Parametrized test runner |
| `.github/workflows/skill-behavioral-tests.yml` | Opt-in CI job |
| `pyproject.toml` | Add `skill-behavioral` pytest marker and optional dependencies |
| `tests/skill-behavioral/scenarios/pragmatic-adoption-gateway/` | 5 gateway scenarios as first consumer |

---

## Open Questions for Review

1. Should the evaluator ask the LLM to **simulate the agent** (first-person, "I would resume...") or **evaluate the skill** (third-person, "the skill would resume...")? Third-person evaluator is more reliable for structured output but tests a different thing.

2. Should failing skill behavioral tests **block merges** or only **warn**? Given LLM non-determinism, blocking may cause flaky CI.

3. Should scenario YAML files live next to the skills they test (`agent-skills/skills-by-domain/.../scenarios/`) or centrally in `tests/skill-behavioral/scenarios/`? Central is easier to find; co-located is easier to maintain with the skill.

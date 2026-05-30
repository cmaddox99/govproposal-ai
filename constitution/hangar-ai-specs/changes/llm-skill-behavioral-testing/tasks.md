# Tasks — LLM Skill Behavioral Testing Infrastructure

**Spec ID:** `llm-skill-behavioral-testing`
**Status:** PROPOSE — awaiting review

## Task List

- [ ] LLM-TEST-01 — Review proposal and resolve Open Questions (human)
- [ ] LLM-TEST-02 — Add `skill-behavioral` pytest marker to `pyproject.toml`
- [ ] LLM-TEST-03 — Create `tests/skill-behavioral/conftest.py` with LLM client fixture and skip logic
- [ ] LLM-TEST-04 — Create `tests/skill-behavioral/evaluator_prompt.md`
- [ ] LLM-TEST-05 — Create `tests/skill-behavioral/test_skill_routing.py` (parametrized runner)
- [ ] LLM-TEST-06 — Write 5 gateway scenarios under `tests/skill-behavioral/scenarios/pragmatic-adoption-gateway/`
- [ ] LLM-TEST-07 — Create `.github/workflows/skill-behavioral-tests.yml`
- [ ] LLM-TEST-08 — Run tests locally with real API key to verify green
- [ ] LLM-TEST-09 — Commit and open PR

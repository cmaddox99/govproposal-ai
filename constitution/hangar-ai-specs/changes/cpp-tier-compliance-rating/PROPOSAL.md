# Proposal: C++ Tier System and Compliance Evaluation Framework

**Status:** PROPOSED
**Spec ID:** `cpp-tier-compliance-rating`
**Triggered by:** Amendment O (V6/V8) — `compliance-rating-system.md` removed as shadow governance from avatar directory; content requires a formal spec proposal per ENG-11.1
**Scope:** `avatars/technology/cpp/` (manifest tier system), `agent-skills/skills-by-domain/platform-engineering/` (compliance skill), new constitutional amendment
**Parent PR:** #14 (c-plus-plus-avatar-enrichment)
**Companion to:** `cpp-extended-reference-docs`, `product-avatar-bus-enrichment`

---

## Problem

The C++ avatar contains a `standard_tiers:` block in `manifest.yaml` (T1–T5, representing C++ standard version ranges from C++98/03 to C++20/23) and a `skill-cpp-compliance-rating.md` that implements a 10-dimension evaluation formula with tier multipliers. These two systems are **architecturally inseparable**:

1. **Tier is a pre-condition for scoring** — the CMakeLists.txt is inspected to determine `CMAKE_CXX_STANDARD`, which maps to a tier (T1–T5). No score without tier.
2. **Dimension 9 IS the tier evaluation** — one of the 10 scoring dimensions is specifically the tier assessment itself.
3. **Tier multiplier adjusts composite score** — `composite = raw_score × tier_multiplier` (T1=0.85, T2=0.90, T3=0.95, T4/T5=1.00). The evaluation formula has no meaning without the tier definition.

The original `compliance-rating-system.md` was removed from the avatar directory by Amendment O because it was shadow governance embedded in an avatar directory (V6 violation). However, the underlying framework is valid constitutional content — it simply needs to be formalized as a proper spec proposal with law citations, governance review, and a dedicated change directory.

### Why This Must Be a Single Proposal (Not Two)

Splitting tier taxonomy from evaluation formula would create an incomplete spec. A tier definition without the evaluation formula has no application; an evaluation formula without tier definitions has no taxonomy to reference. They must be proposed, reviewed, and implemented together.

---

## Solution

Formalize the C++ tier taxonomy and evaluation framework as a constitutional amendment:

1. **Tier Taxonomy** (`standard_tiers:` in manifest.yaml) — already in place; formalize via this proposal
2. **Evaluation Formula** — 10 dimensions, tier multiplier, composite scoring; govern as a spec
3. **Skill** — `skill-cpp-compliance-rating.md` updated to reference this proposal
4. **Governance** — How teams use tier/evaluation results; what authority they carry; escalation path

---

## Tier Taxonomy (T1–T5)

| Tier | Standard | Policy |
|------|----------|--------|
| T1 (legacy_frozen) | C++98/C++03 | Legacy — frozen, no new features; RAII migration required on touched code |
| T2 (legacy_supported) | C++11 | Active maintenance; gradual modernization via phased migration |
| T3 (active_brownfield) | C++14/C++17 | Greenfield OK; brownfield modernization active |
| T4 (required_minimum) | C++20 | Minimum for new projects; required for all non-brownfield code |
| T5 (recommended) | C++23 | Recommended for new services; full modern C++ capabilities |

---

## Evaluation Framework (10 Dimensions)

| Dim | Name | Weight | Description |
|-----|------|--------|-------------|
| 1 | Test Coverage | 15% | GoogleTest unit coverage %, mutation score (Mull) |
| 2 | Memory Safety | 20% | ASAN/MSAN/UBSAN pass rates, raw pointer usage |
| 3 | Static Analysis | 15% | clang-tidy warnings/errors, SAST gate status |
| 4 | Build Determinism | 10% | Reproducible build compliance, CMake best practices |
| 5 | Dependency Governance | 10% | License compliance, version pinning, supply chain |
| 6 | Observability | 10% | OpenTelemetry instrumentation, structured logging |
| 7 | CI/CD Compliance | 10% | Pipeline coverage, gate enforcement, deployment safety |
| 8 | Security Posture | 5% | DAST, secrets management, binary hardening |
| 9 | Standard Tier | 5% | Tier assessment (T1–T5 per CMakeLists.txt inspection) |
| 10 | Documentation | 0% | Informational only; no score impact |

**Composite Score:** `composite = raw_score × tier_multiplier`

Tier multipliers: T1=0.85, T2=0.90, T3=0.95, T4/T5=1.00

Score bands: A (≥90%), B (75–89%), C (60–74%), D (45–59%), F (<45%)

---

## Deliverables

| Artifact | Description |
|----------|-------------|
| This PROPOSAL.md | Formal spec for tier taxonomy + evaluation formula |
| `tasks.md` | Atomic TDD implementation tasks |
| `agent-skills/…/skill-cpp-compliance-rating.md` | Updated to cite this proposal as governing spec |
| `avatars/technology/cpp/manifest.yaml` | `standard_tiers:` block already in place — add spec reference |
| Amendment to constitution | Add `cpp-tier-compliance-rating` to `hangar-ai-specs/README.md` spec index |

---

## Success Criteria

| Criterion | Verification |
|-----------|--------------|
| Tier taxonomy formally documented | This PROPOSAL.md approved by governance |
| Evaluation formula formally documented | 10-dimension table + scoring formula in this spec |
| Skill law references ENG-* only | `test_skill_cpp_compliance_rating_has_no_bus_law_refs()` PASSES |
| `manifest.yaml standard_tiers:` references this spec | Manual review |
| No shadow governance documents in avatar dir | `test_no_shadow_governance_docs_in_avatar_dir()` PASSES |

---

## Laws Cited

| Law | Relevance |
|-----|-----------|
| [ENG-11.1](laws/engineering/spec-driven-development.md) | Spec-Driven Development — governance frameworks require formal proposals |
| [ENG-11.2](laws/engineering/spec-driven-development.md) | Proposal Completeness — law citations, success criteria, deliverables |
| [ENG-4.1](laws/engineering/testing.md) | Atomic TDD — evaluation formula implementations require tests |
| [ENG-6.7](laws/engineering/security.md) | Compliance Reporting — evaluation framework produces compliance reports |

---

## Out of Scope

- **Product avatar adoption** — tier/evaluation applies only to `avatars/technology/cpp/`; product avatars have different evaluation concerns
- **Automated enforcement** — this proposal governs the framework definition only; tooling to automate evaluation is a future proposal
- **Cross-avatar standardization** — other technology avatars may adopt similar tier systems via separate proposals

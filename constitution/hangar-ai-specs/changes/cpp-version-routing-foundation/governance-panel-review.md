# Multi-Persona Governance Panel Review
# cpp-version-routing-foundation — Schema Extension Decisions

**Panel convened:** 2026-04-25  
**Record reviewed:** `governance-decision-record.md` (GDR-cpp-version-routing-foundation)  
**Prompt:** See [governance-review-prompt.md](governance-review-prompt.md)

---

## PANEL ROSTER

| # | Name | Role | Domain |
|---|------|------|--------|
| 1 | Dr. Anjali Mehta | Principal C++ Language Engineer, ISO C++ WG observer | C++ Technical Correctness |
| 2 | Marcus Webb | Hangar AI Constitution Governance Lead | Constitution Governance |
| 3 | Dmitri Volkov | Senior Staff Engineer — C++98 Legacy / CWR Project | Legacy/Brownfield C++ |
| 4 | Dr. Priya Sundaram | AI Agent Architecture & RAG Systems Researcher | AI Agent Architecture |
| 5 | Sofia Chen | Developer Experience Lead — C++ Onboarding | Developer Experience |
| 6 | Col. James Okonkwo (ret.) | DO-178C / MISRA C++ Safety Systems Consultant | Safety-Critical Systems |
| 7 | Cameron Ross | AA Platform Engineering — Consuming Repo Owner | Consuming Repo Perspective |
| 8 | Dr. Yuki Tanaka | Information Architecture & YAML Schema Design | Information Architecture |
| 9 | Dr. Thomas Hart | Testing Correctness Lead — AI-Assisted Code Review | Test Correctness |
| 10 | Owen Bradley | Build System Detection Specialist | Build-System Detection |
| 11 | Patricia Osei | Change Management & Organizational Risk | Security/Audit |
| 12 | Richard Callahan | Portfolio Risk & Rollout Management | Portfolio/Change Mgmt |

---

## PANEL VERDICTS

### Persona 1 — Dr. Anjali Mehta (C++ Technical Correctness)

**Scope:** Check whether the schema correctly models real C++ standard/toolchain boundaries.

- 🟢 D1.1 is correct: min-only is safer than min/max for evolving C++ guidance
- 🔴 `cpp_version_min: 98` cannot mean "safe for all versions" while D3 also defines a pre-C++98 legacy tier — the floor is lower than 98
- 🔴 Some proposed version tags are not source-validated. Example: `ENG-6.7-audit-trail.md` uses designated initializers (`.booking_id = id`), which is C++20, not C++17

**OQ resolutions:**
- OQ-1.2: Keep `cpp_version_min` (scoped, explicit, consistent)
- OQ-1.3: Yes — surface warnings for C++11 content shown to C++98/03/pre-98 projects

**Verdict: 🔴 BLOCKED**

---

### Persona 2 — Marcus Webb (Constitution Governance)

**Scope:** Check ENG-11.x compliance, schema clarity, and decision completeness.

- 🟢 Decision framing is clear and within ENG-11 scope
- 🟡 D2.2 is internally inconsistent: calls `idiom_level` "mandatory" then "optional"
- 🔴 Proposal, GDR, and tasks use inconsistent vocabulary for tiers — undermines governance traceability

**OQ resolutions:**
- OQ-3.3: Canonical routing policy in `AVATAR-RAG-INDEX.yaml`; `guidance.md` should summarize, not redefine

**Verdict: ⚠️ CONDITIONAL PASS**

---

### Persona 3 — Dmitri Volkov (Legacy/Brownfield C++)

**Scope:** Check fit for C++98/03, MSVC 6.0, CWR, herc-odyssey, SPEClient.

- 🟢 Conservative fallback default is the right strategic move
- 🔴 D2 schema cannot represent pre-C++98 projects — SPEClient cannot declare its actual state
- 🔴 D1.3 leaves a silent-failure gap: C++11 files still return uncompilable advice for ~35% of the portfolio

**OQ resolutions:**
- OQ-1.3: Yes — provide warnings for all C++11+ content shown to C++98/03/pre-98 projects
- OQ-2.2: Do not add `borland` unless the C++ avatar explicitly supports that tier

**Verdict: 🔴 BLOCKED**

---

### Persona 4 — Dr. Priya Sundaram (AI Agent Architecture)

**Scope:** Check fit with agent-as-router architecture and token constraints.

- 🟢 Putting routing data in the index is architecturally correct
- 🔴 D3 block references filenames that do **not exist** in the repo (`ref-core-language.md`, `ref-safety-memory.md`, `ref-advanced-cpp.md`, `ref-brownfield-config.md`) — the routing block cannot be implemented as written
- 🔴 Routing semantics have already drifted between `guidance.md`, GDR, proposal, and tasks

**OQ resolutions:**
- OQ-3.1: Hybrid — file paths for refs; optional `law_id` alias for example files
- OQ-3.3: Canonical data in index; execution protocol in guidance (summary only)

**Verdict: 🔴 BLOCKED**

---

### Persona 5 — Sofia Chen (Developer Experience)

**Scope:** Check adoption friction and usability of the project.yaml declaration.

- 🟢 `.copilot/project.yaml` is a reasonable, discoverable location
- 🟡 `compiler` and `toolset` fields are too strict for early adoption; teams may not know exact values
- 🟡 No `schema_version` field means copied templates can drift silently

**OQ resolutions:**
- OQ-2.1: Keep `.copilot/project.yaml` with language sections (not `cpp-context.yaml`)
- OQ-2.3: `.copilot/` is acceptable; document as canonical AI config root

**Verdict: ⚠️ CONDITIONAL PASS**

---

### Persona 6 — Col. James Okonkwo (Safety-Critical Systems)

**Scope:** Check safety for regulated and legacy operational environments.

- 🟢 Conservative default is appropriate for safety-sensitive repos
- 🔴 "Unknown → C++14 baseline" wording is unsafe for MSVC6/C++03 estates — must read "legacy-safe" uniformly
- 🟡 Advisory-only avoid lists are acceptable only if version-mismatch warnings are reliable

**OQ resolutions:**
- OQ-1.3: Yes — warning required whenever content version exceeds detected project tier
- OQ-3.2: No tier split yet — use file-level gating via `cpp_version_min`

**Verdict: ⚠️ CONDITIONAL PASS**

---

### Persona 7 — Cameron Ross (Consuming Repo Perspective)

**Scope:** Check minimum viable adoption path for AA teams.

- 🟢 Opt-in project file plus fallback detection is the right rollout model
- 🟡 Required vs optional fields are unclear — `idiom_level` and `compiler` should not block adoption
- 🔴 No way to declare "pre-C++98 / legacy" even though SPEClient is in the stated scope

**OQ resolutions:**
- OQ-2.1: Keep `.copilot/project.yaml`
- OQ-2.3: `.copilot/` fine — document it

**Verdict: ⚠️ CONDITIONAL PASS**

---

### Persona 8 — Dr. Yuki Tanaka (Information Architecture)

**Scope:** Check schema shape, naming, and cross-avatar consistency.

- 🟢 `cpp_version_min` is better than `min_cpp_standard`: scoped, explicit, consistent with existing snake_case frontmatter
- 🔴 D3 `detection_order` list includes `"*.dsp / *.dsw"` as an ambiguous string, not structured input
- 🟡 D2 and D3 must share one canonical enum set and one canonical tier vocabulary

**OQ resolutions:**
- OQ-1.2: `cpp_version_min` (confirmed)
- OQ-3.1: Prefer structured path keys, not law_id-only references

**Verdict: ⚠️ CONDITIONAL PASS**

---

### Persona 9 — Dr. Thomas Hart (Test Correctness)

**Scope:** Check whether acceptance criteria can actually validate the schema decisions.

- 🔴 Current test plan (AC-1 through AC-9) tests presence/existence only — does not validate precedence, fallback, `idiom_level` override, untagged-file default, or mismatch warning behavior
- 🔴 Tasks use tier names that differ from the GDR — tests will pass against wrong behavior
- 🟡 `cpp_version_note` should have a tested character limit

**OQ resolutions:**
- OQ-1.1: Add a hard max (240 chars) with a validated test
- OQ-3.3: Add consistency test: guidance.md tier names must match AVATAR-RAG-INDEX.yaml tier names

**Verdict: 🔴 BLOCKED**

---

### Persona 10 — Owen Bradley (Build-System Detection)

**Scope:** Check CMake/vcxproj/Makefile/.dsp detection design.

- 🟢 Detection order is sensible
- 🟡 `.dsp/.dsw` presence heuristic can false-positive on archived/stale project files
- 🟡 Detection items should be structured as typed match rules, not prose strings

**OQ resolutions:**
- OQ-2.3: `.copilot/` is fine location

**Verdict: ⚠️ CONDITIONAL PASS**

---

### Persona 11 — Patricia Osei (Security/Audit)

**Scope:** Check auditability and safe failure modes.

- 🟢 D3 improves traceability over current implicit routing
- 🟡 Advisory avoid lists need explicit override-logging semantics in a future phase
- 🟡 `cpp_version_note` length should be bounded to keep prompts predictable

**OQ resolutions:**
- OQ-1.1: Yes, add a hard limit
- OQ-3.1: Path-based references are more auditable

**Verdict: ⚠️ CONDITIONAL PASS**

---

### Persona 12 — Richard Callahan (Portfolio/Change Management)

**Scope:** Check rollout feasibility across the AA C++ repo estate.

- 🟢 Proposal is well-targeted at the real portfolio skew (95% LOC below C++20)
- 🔴 Legacy representation gap blocks the highest-risk estate (SPEClient at 24% LOC) from declaring its actual state
- 🟡 Adoption improves if the project file is permissive — mostly optional fields

**OQ resolutions:**
- OQ-2.2: Keep out-of-scope toolchains out unless explicitly supported
- OQ-3.2: No extra tier yet

**Verdict: ⚠️ CONDITIONAL PASS**

---

## OVERALL PANEL VERDICT

**🔴 BLOCKED FOR IMPLEMENTATION**

The design direction is sound. Three panels (Anjali, Dmitri, Priya, Thomas) issued hard blocks.
The remainder issued conditional passes with shared concerns. Implementation cannot begin
until the five blocking issues below are resolved in the GDR and proposal.

---

## OPEN QUESTION RESOLUTIONS

| OQ | Question | Recommended Resolution |
|----|----------|----------------------|
| OQ-1.1 | Should `cpp_version_note` have a character limit? | **Yes. Max 240 chars, prose only, no code blocks. Add a tested acceptance criterion.** |
| OQ-1.2 | `cpp_version_min` vs `min_cpp_standard`? | **`cpp_version_min` — scoped, consistent with existing snake_case frontmatter style.** |
| OQ-1.3 | Should C++11 files receive `cpp_version_note` for C++98/03 projects? | **Yes. Surface a warning whenever `cpp_version_min` exceeds the detected project tier, regardless of tier.** |
| OQ-2.1 | `cpp-context.yaml` vs `.copilot/project.yaml`? | **Keep `.copilot/project.yaml` with language sections (`cpp:`). Language-specific names create per-language sprawl.** |
| OQ-2.2 | Should `borland` be in the compiler enum? | **No. Use `other` or `unknown` in Phase 1. Borland/VCL is explicitly out of scope for the C++ avatar.** |
| OQ-2.3 | Is `.copilot/` the right directory? | **Yes. Document it as the canonical agent config root in guidance.md.** |
| OQ-3.1 | `avoid` lists per filename vs per law_id? | **Hybrid: file paths for reference files; optional `law_id` for example files. Avoid pure law_id — too brittle to renames.** |
| OQ-3.2 | Is C++11 different enough from C++14 to warrant a split? | **No — not in Phase 1. Use file-level `cpp_version_min` for fine gating. Add a tier only when differentiated content exists.** |
| OQ-3.3 | Routing policy in AVATAR-RAG-INDEX.yaml or guidance.md? | **Canonical data in `AVATAR-RAG-INDEX.yaml`. `guidance.md` references tier names but does not redefine them. Add a consistency test.** |

---

## BLOCKING ISSUES (Must Resolve Before Implementation)

| # | Issue | Severity | Required Fix |
|---|-------|----------|-------------|
| B1 | D3 references non-existent/non-canonical filenames (`ref-core-language.md`, etc.) and tier names | 🔴 Blocking | Replace with real repo paths; establish one canonical tier vocabulary across all documents |
| B2 | Legacy/pre-C++98 is not representable in D2 project.yaml schema | 🔴 Blocking | Add `legacy`/`pre98` to the `standard` enum; update D1.4 semantics so `cpp_version_min: 98` does NOT claim "safe for all versions" |
| B3 | Unknown fallback wording is inconsistent (`legacy-safe` in D3 vs "C++14 baseline" in `unknown.agent_prompt`) | 🔴 Blocking | Remove "C++14 baseline" wording everywhere; all unknown/fallback messaging must say "legacy-safe" |
| B4 | AC plan does not validate core behavior (only tests presence/existence) | 🔴 Blocking | Add scenario tests for: detection precedence, `idiom_level` override, untagged-file default, version-mismatch warning |
| B5 | Some proposed `cpp_version_min` assignments are wrong (`ENG-6.7-audit-trail.md` uses C++20 designated initializers, not C++17) | 🔴 Blocking | Audit all proposed version assignments against actual file syntax before tagging |

---

## HIGH-PRIORITY IMPROVEMENTS (Before Phase 1)

| Priority | Improvement |
|----------|-------------|
| P1 | Add `legacy` / `pre98` to `.copilot/project.yaml` `standard` enum |
| P2 | Fix D3 `prefer`/`avoid` lists to reference real existing file paths |
| P3 | Make D3 `detection_order` structured data (typed rules, not prose strings) |
| P4 | Add `schema_version` field to `.copilot/project.yaml` template |
| P5 | Clarify field requiredness: `standard` = required; `idiom_level`, `compiler`, `toolset` = optional |
| P6 | Audit all 29 proposed `cpp_version_min` assignments against actual file content before tagging |

---

## ADVISORY IMPROVEMENTS (Future Phases)

- Auto-generate a generic warning when file `cpp_version_min > project tier` and no `cpp_version_note` exists
- Add a constitution-lint rule that validates every D3 `prefer`/`avoid` reference actually exists
- Add scenario-level test fixtures for canonical repos: CWR, herc-odyssey, SPEClient
- Consider C++11/C++14 tier split only after differentiated content (Phase 2) exists

---

## GOVERNANCE VERDICTS

| Decision | Verdict | Key Conditions |
|----------|---------|---------------|
| D1 — `cpp_version_min` / `cpp_version_note` frontmatter | ⚠️ **APPROVED WITH CONDITIONS** | Fix legacy semantics; add 240-char note limit; validate all version assignments |
| D2 — `.copilot/project.yaml` declaration mechanism | ⚠️ **APPROVED WITH CONDITIONS** | Add `legacy`/`pre98` to `standard` enum; clarify field requiredness; add `schema_version` |
| D3 — `version_routing_policy` block | ⚠️ **APPROVED WITH CONDITIONS** | Replace non-existent file refs; unify tier vocabulary; fix unknown fallback wording |

*Implementation is BLOCKED until all 5 blocking issues (B1–B5) are resolved.*

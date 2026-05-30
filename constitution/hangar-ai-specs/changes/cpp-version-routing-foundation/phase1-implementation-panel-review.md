# Phase 1 Implementation Panel Review
# cpp-version-routing-foundation

**Panel convened:** 2026-04-25  
**Scope:** Phase 1 implementation review (commits `6ed40dd` → `be5829b`)  
**Prior review:** `governance-panel-review.md` (original governance design)  
**Prompt:** Same 12-persona panel, reconvened to assess implementation

---

## PANEL ROSTER (unchanged from governance review)

| # | Name | Role | Domain |
|---|------|------|--------|
| 1 | Dr. Anjali Mehta | Principal C++ Language Engineer | C++ Technical Correctness |
| 2 | Marcus Webb | Hangar AI Constitution Governance Lead | Constitution Governance |
| 3 | Dmitri Volkov | Senior Staff Engineer — C++98 Legacy / CWR Project | Legacy/Brownfield C++ |
| 4 | Dr. Priya Sundaram | AI Agent Architecture & RAG Systems Researcher | AI Agent Architecture |
| 5 | Sofia Chen | Developer Experience Lead — C++ Onboarding | Developer Experience |
| 6 | Col. James Okonkwo (ret.) | DO-178C / MISRA C++ Safety Systems Consultant | Safety-Critical Systems |
| 7 | Cameron Ross | AA Platform Engineering — Consuming Repo Owner | Consuming Repo Perspective |
| 8 | Dr. Yuki Tanaka | Information Architecture & YAML Schema Design | Information Architecture |
| 9 | Dr. Thomas Hart | Testing Correctness Lead | Test Correctness |
| 10 | Owen Bradley | Build System Detection Specialist | Build-System Detection |
| 11 | Patricia Osei | Change Management & Organizational Risk | Security/Audit |
| 12 | Richard Callahan | Portfolio Risk & Rollout Management | Portfolio/Change Mgmt |

---

## ORIGINAL BLOCKING ISSUES — RESOLUTION STATUS

| # | Issue | Status |
|---|-------|--------|
| B1 | D3 non-existent filenames; inconsistent tier vocabulary | ✅ RESOLVED |
| B2 | Legacy/pre-C++98 not representable in project.yaml | ✅ RESOLVED |
| B3 | Unknown fallback wording inconsistent (C++14 baseline) | ✅ RESOLVED |
| B4 | AC plan only tested presence, not behavior | ✅ RESOLVED |
| B5 | Wrong cpp_version_min assignments (ENG-6.7 etc.) | ✅ RESOLVED |

---

## PANEL VERDICTS

### Persona 1 — Dr. Anjali Mehta (C++ Technical Correctness)

**B-issue resolution**
| Issue | Status |
|---|---|
| B2 `pre98` enum | ✅ RESOLVED |
| B3 legacy-safe fallback | ✅ RESOLVED |
| B5 version assignments audited | ✅ RESOLVED |

**P-improvement status** P1 ✅, P6 ✅

**New findings**
- 🟢 `ENG-6.7-audit-trail.md → 20` and `std::expected → 23` directly address prior technical correctness concerns
- 🟡 Policy is tier-based but correctness sometimes depends on exact standard (11 vs 14, 20 vs 23); same-tier exact-version mismatch is not explicitly tested
- 🟡 `cpp-project.yaml` uses string values (`"14"`) while `AVATAR-RAG-INDEX.yaml` uses numeric scalars (`[17]`, `[20, 23]`); routing can misclassify if comparison logic is not normalized

**Verdict: ⚠️ CONDITIONAL PASS**

---

### Persona 2 — Marcus Webb (Constitution Governance)

**B-issue resolution** B1 ✅, B3 ✅, B4 ✅

**P-improvement status** P2 ✅, P3 ⚠️ PARTIAL, P4 ✅, P5 ✅

**New findings**
- 🟢 Canonical vocabulary is coherent: `legacy-safe` is consistent, D3 path references are real paths
- 🟡 `detection_order` was requested as structured data; it exists in `guidance.md` prose but not as machine-readable data in `AVATAR-RAG-INDEX.yaml`

**Verdict: ⚠️ CONDITIONAL PASS**

---

### Persona 3 — Dmitri Volkov (Legacy/Brownfield C++)

**B-issue resolution** B2 ✅, B3 ✅, B5 ✅

**P-improvement status** P1 ✅, P6 ✅

**New findings**
- 🟢 Semantic version ordering explicitly fixes the `11 < 98` integer comparison trap
- 🟢 `.dsp` → `legacy` and SPEClient walkthrough show pre98 path is representable and exercised
- 🟡 `brownfield` groups `98` and `03`; fine for tier routing, but exact `03`-minimum examples still require standard-level checks beyond tier selection

**Verdict: ⚠️ CONDITIONAL PASS**

---

### Persona 4 — Dr. Priya Sundaram (AI Agent Architecture)

**B-issue resolution** B1 ✅, B3 ✅, B4 ✅

**P-improvement status** P2 ✅, P3 ⚠️ PARTIAL, P5 ✅

**New findings**
- 🟢 `unknown_fallback: legacy-safe` is explicit and conservative
- 🟡 Detection precedence lives in markdown, not structured policy data — weakens determinism for automated consumers
- 🟡 Mixed scalar types in YAML are a real architecture risk if any consumer performs strict equality instead of normalization

**Verdict: ⚠️ CONDITIONAL PASS**

---

### Persona 5 — Sofia Chen (Developer Experience)

**B-issue resolution** B1 ✅, B3 ✅

**P-improvement status** P2 ✅, P4 ✅, P5 ✅

**New findings**
- 🟢 Template is much clearer: required vs optional explicit, examples concrete, `pre98` now onboardable
- 🟡 Quoted strings in template vs numeric values in policy increases user/tool confusion and copy-paste inconsistency risk

**Verdict: ⚠️ CONDITIONAL PASS**

---

### Persona 6 — Col. James Okonkwo (Safety-Critical Systems)

**B-issue resolution** B3 ✅, B4 ✅, B5 ✅

**P-improvement status** P6 ✅

**New findings**
- 🟢 "Warn — never silently serve wrong-version patterns" is the correct conservative behavior for safety-critical estates
- 🟡 Scenario coverage added, but summary does not explicitly show same-tier mismatch tests (`11` project vs `14` example, `20` vs `23`)

**Verdict: ⚠️ CONDITIONAL PASS**

---

### Persona 7 — Cameron Ross (Consuming Repo Perspective)

**B-issue resolution** B1 ✅, B2 ✅, B3 ✅, B4 ✅

**P-improvement status** P1 ✅, P4 ✅, P5 ✅

**New findings**
- 🟢 Now actually consumable: `.copilot/project.yaml` documented, examples annotated, fallback behavior explicit
- 🟡 Consumption depends on detection logic partly encoded in prose, not a single machine-readable source of truth

**Verdict: ⚠️ CONDITIONAL PASS**

---

### Persona 8 — Dr. Yuki Tanaka (Information Architecture)

**B-issue resolution** B1 ✅, B2 ✅

**P-improvement status** P1 ✅, P3 ⚠️ PARTIAL, P4 ✅, P5 ✅

**New findings**
- 🟡 Schema is not type-consistent: template `standard: "14"` (string) vs policy `standards: [17]` / `[20, 23]` (integers)
- 🟡 `"03"` is quoted in the policy while `98`, `11`, `14`, `17`, `20`, `23` are not — increases coercion ambiguity
- 🟡 `detection_order` is still not structured YAML data

**Verdict: ⚠️ CONDITIONAL PASS**

---

### Persona 9 — Dr. Thomas Hart (Test Correctness)

**B-issue resolution** B4 ✅, B5 ✅

**P-improvement status** P6 ✅

**New findings**
- 🟢 Acceptance strategy materially stronger: 24 AC tests plus walkthrough validation across transitional, brownfield, and legacy repos
- 🟡 No explicit tests for YAML string/int normalization
- 🟡 No explicit tests for exact-version mismatch inside a shared tier (`11` vs `14`, `20` vs `23`)

**Verdict: ⚠️ CONDITIONAL PASS**

---

### Persona 10 — Owen Bradley (Build System Detection)

**B-issue resolution** B1 ✅, B4 ✅

**P-improvement status** P2 ✅, P3 ⚠️ PARTIAL

**New findings**
- 🟢 Detection precedence is sensible: explicit project declaration first, build-system heuristics second
- 🟡 Slight source-of-truth drift: `guidance.md` includes `*.props` and `.dsw`; `AVATAR-RAG-INDEX.yaml` comment mentions `.vcxproj` and `.dsp` but omits those two
- 🟡 Presence-only `.dsp/.dsw → legacy` rules can misfire in mixed repos unless scoping is explicit

**Verdict: ⚠️ CONDITIONAL PASS**

---

### Persona 11 — Patricia Osei (Security/Audit)

**B-issue resolution** B1 ✅, B4 ✅

**P-improvement status** P4 ✅, P5 ✅

**New findings**
- 🟢 `schema_version` and explicit requiredness improve auditability and rollout hygiene
- 🟡 If `schema_version` is meant for drift detection, enforcement expectations are not stated; currently reads as convention rather than contract

**Verdict: ⚠️ CONDITIONAL PASS**

---

### Persona 12 — Richard Callahan (Portfolio/Change Management)

**B-issue resolution** B1 ✅, B2 ✅, B3 ✅, B4 ✅, B5 ✅

**P-improvement status** P1 ✅, P2 ✅, P3 ⚠️ PARTIAL, P4 ✅, P5 ✅, P6 ✅

**New findings**
- 🟢 Original blockers appear closed on evidence presented
- 🟡 Residual rollout risk concentrated in two implementation-quality gaps: type consistency and lack of structured detection-order data

**Verdict: ⚠️ CONDITIONAL PASS**

---

## OVERALL PANEL VERDICT

**⚠️ MERGE WITH CONDITIONS**

All 5 original blocking issues (B1–B5) are resolved. 12/12 personas returned CONDITIONAL PASS — a significant improvement over the original review (4 BLOCKED). Implementation materially improves correctness, introduces conservative fallback behavior, audits version minima, and adds scenario-based testing.

Three new non-blocking issues identified during implementation review:

---

## NEW ISSUES TABLE

| # | Issue | Severity | Required Fix |
|---|-------|----------|-------------|
| N1 | YAML standard type inconsistency: template uses strings (`"14"`), policy uses integers (`17`, `[20, 23]`) | Non-blocking / High Priority | Normalize all standard values to strings everywhere, or define explicit coercion rules and test them |
| N2 | `detection_order` not structured in `AVATAR-RAG-INDEX.yaml` — lives only in `guidance.md` prose | Non-blocking / High Priority | Add machine-readable `detection_order` data to index YAML (P3 partial completion) |
| N3 | Minor drift: `guidance.md` mentions `*.props` and `.dsw`; RAG index comment mentions only `.vcxproj` and `.dsp` | Suggestion | Align comments/source-of-truth text across artifacts |

---

## REMAINING HIGH-PRIORITY IMPROVEMENTS

| Priority | Improvement | Phase |
|----------|-------------|-------|
| P3 (partial) | Encode `detection_order` as structured YAML, not only prose | Phase 2+ |
| N1 | Standardize scalar type for standards: use strings everywhere (`"14"`, `"17"`, `"20"`) | Phase 2+ or hotfix |
| Testing gap | Add tests for string/int normalization and same-tier exact-version mismatch (`11` vs `14`, `20` vs `23`) | Phase 2+ |

---

## ADVISORY ITEMS (Future Phases)

- Make drift-detection behavior around `schema_version` explicit and enforceable
- Clarify whether exact standard comparison is separate from tier routing in the implementation contract
- Add mixed-repo detection tests for archival `.dsp/.dsw` presence in repos not actually at pre-C++98
- Add constitution-lint rule enforcing that all D3 prefer/avoid refs continue to exist on disk (advisory from P11)

---

## MERGE READINESS

**⚠️ MERGE WITH CONDITIONS**

Conditions before merge to main:
1. Normalize standard scalar types across all YAML artifacts (N1)
2. Add targeted tests for exact-version mismatch within shared tiers (Thomas Hart / James Okonkwo finding)

N2 and N3 are acceptable to defer to Phase 2+ (they do not affect correctness of the agent routing).

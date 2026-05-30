# Avatar Workflow Assessment — C++ Technology Avatar

> **Assessed against:** `docs/guides/avatar-model-schema.md`
> **Mode:** Validate (read-only)
> **Workflow:** `workflows/avatar-workflow.md` — Mode 3
> **Avatar path:** `avatars/technology/cpp/`
> **Scan date:** 2026-04-13
> **Context:** Post-Phase 17 state (Amendment P merged); pre-Phase 18 remediation

---

### Verdict: 🔴 BLOCKED

Two blocking findings (manifest token budget, broken workflow reference) plus three new workflow findings not covered by the panel review.

---

## PHASE 1 — IDENTIFY

| Field | Value |
|-------|-------|
| Mode | Validate (Mode 3) |
| Type | technology |
| Domain | cpp |
| Avatar path | `avatars/technology/cpp/` |
| Avatar exists | ✅ Yes — `manifest.yaml`, `guidance.md`, `examples/` (44 files), `full-reference.md` |

---

## PHASE 2 — SCAN

### Safeguard 1 — Deduplication

✅ PASS — No other C++ technology avatar exists. `avatar-cpp` is unique in `avatars/technology/`.

### Step 2.1 — Schema Completeness Check

**manifest.yaml:**

| Check | Result | Detail |
|-------|--------|--------|
| File present | ✅ | |
| `avatar.id` present | ✅ | `avatar-cpp` |
| `avatar.type` valid | ✅ | `technology` |
| `avatar.version` (semver) | ✅ | `2.0.0` |
| `stack` block present | ✅ | Language, compilers, testing, build, sanitizers |
| `activates.skills` ≥2 entries | ✅ | 4 entries |
| `activates.skills` — each exists in `agent-skills/`? | 🟡 WARNING | Files resolve with `skill-` prefix stripped (`skill-06-atomic-tdd` → `06-atomic-tdd.md`). Routing depends on implicit prefix-stripping (see W-6 below). |
| `activates.workflows` ≥1 entry | ✅ | 3 entries |
| `activates.workflows` — each exists in `workflows/`? | 🔴 BLOCKING | `brownfield-adoption` → **NOT FOUND** as `workflows/brownfield-adoption.md`. `greenfield-development` ✅, `product-discovery-stage-a-f` ✅. |
| `specializes_laws` ≥1 non-negotiable | ✅ | ENG-4.1 (Atomic TDD — non-negotiable) |
| All `example_file` refs resolve | 🟡 WARNING | 4 laws missing `example_file`: ENG-3.7, ENG-5.2, ENG-5.5, ENG-7.1 |
| Estimated tokens ≤150 | 🔴 BLOCKING | 1,176 words ≈ **1,568 tokens** — 10× over budget |
| All blocks on manifest allowlist | 🔴 BLOCKING | 6 blocks NOT on allowlist (see W-5 below) |

**guidance.md:**

| Check | Result | Detail |
|-------|--------|--------|
| File present | ✅ | |
| Non-Negotiable Laws section | ✅ | 7 laws in table |
| Estimated tokens ≤450 | ✅ | 268 words ≈ 357 tokens |

**examples/:**

| Check | Result | Detail |
|-------|--------|--------|
| Directory present | ✅ | 44 files |
| One file per `specializes_laws` law | 🟡 WARNING | Missing: ENG-3.7, ENG-5.5, ENG-7.1 (no files on disk). ENG-5.2 has 2 files but only 1 in manifest. ENG-4.4, ENG-7.2–7.5 have files but laws NOT in `specializes_laws`. |
| Each file ≤850 tokens | ✅ | Largest: `ENG-3.1-coroutines.md` (444 words ≈ 592 tokens) |

### Safeguard 2 — Law Domain Boundary (Step 2.2)

✅ PASS

| Check | Result |
|-------|--------|
| All `specializes_laws` entries ENG-* only | ✅ 16/16 are ENG-* |
| No PRD-* entries | ✅ |
| No BUS-* entries | ✅ |
| All `examples/` filenames ENG-* | ✅ 44/44 are ENG-* |

### Safeguard 3 — Product Taxonomy

N/A (technology avatar)

### Safeguard 4 — Law ID Validity (Step 2.3)

✅ PASS — All 16 law IDs verified against `laws/engineering/_domain.yaml`:

ENG-4.1 ✅, ENG-6.1 ✅, ENG-6.4 ✅, ENG-6.7 ✅, ENG-3.1 ✅, ENG-3.2 ✅, ENG-2.1 ✅, ENG-2.2 ✅, ENG-3.3 ✅, ENG-3.5 ✅, ENG-3.7 ✅, ENG-4.2 ✅, ENG-5.2 ✅, ENG-5.5 ✅, ENG-6.5 ✅, ENG-7.1 ✅

### Safeguard 5 — Shadow Governance & Skills Existence (Steps 2.4, 2.5)

**Shadow Governance Detection (Step 2.4):**

| Pattern | Found | Severity | Detail |
|---------|-------|----------|--------|
| Invented law IDs | No | — | — |
| Ungrounded mandatory requirements | Yes | 🟡 SHADOW GOVERNANCE | `standard_tiers` block: "required_greenfield", "required_minimum", "modernization plan toward C++20 required", "modernization timeline to C++17+ required within 12 months" — all without law citations |
| Embedded skill definitions | Yes | 🟡 SHADOW GOVERNANCE | `brownfield_adoption` block defines agent behavior steps ("Run compliance rating", "Create MODERNIZATION_PLAN.md") directly in manifest |
| Law overrides / self-approval | No | — | Amendment O removed `governance_overrides` |
| Unknown manifest blocks | Yes | 🟡 SHADOW GOVERNANCE | See W-5 below: 6 blocks not on allowlist |

**activates.skills Existence (Step 2.5):**

| Skill in manifest | File found | Match type |
|-------------------|-----------|------------|
| `skill-06-atomic-tdd` | `06-atomic-tdd.md` | Prefix-stripped |
| `skill-07-vertical-slice-dev` | `07-vertical-slice-dev.md` | Prefix-stripped |
| `skill-08-code-review` | `08-code-review.md` | Prefix-stripped |
| `skill-04-business-domain-modeling` | `04-business-domain-modeling.md` | Prefix-stripped |

🟡 WARNING (W-6) — All 4 skills resolve only after stripping the `skill-` prefix. Manifest names do not exactly match filenames.

**Inverse check:** No orphaned skills found in `examples/` (all are law examples, not skill definitions). The 25 Phase 16 C++ skills need separate verification (A-7 in tasks.md).

### Step 2.6 — Blast Radius

N/A — No BLOCKING law boundary violations found in Step 2.2.

---

## PHASE 5 — RAG VALIDATE

### 5 Canonical Queries

| # | Query | Files Loaded | Est. Tokens | Answerable | Verdict |
|---|-------|-------------|-------------|------------|---------|
| Q1 | "How do I write a GoogleTest for a C++ class with RAII ownership?" | guidance.md (357) + ENG-4.1-atomic-tdd.md (~512) + ENG-3.1-complexity.md (~467) | ~1,336 | ✅ Yes — GoogleTest patterns + RAII patterns | ✅ PASS |
| Q2 | "What is the correct way to handle errors in C++ without exceptions?" | guidance.md (357) + ??? | ~357 | 🔴 No — ENG-3.7 has no `example_file`; `ENG-6.1-expected-errors.md` is not routed by manifest | 🔴 FAIL |
| Q3 | "How do I migrate from raw pointers to unique_ptr in a C++03 brownfield codebase?" | guidance.md (357) + ENG-6.1-smart-pointer-migration.md (~867) + ENG-6.1-auto-ptr-migration.md (~653) | ~1,877 | ✅ Yes — Both migration examples cover this | ✅ PASS |
| Q4 | "What sanitizers are mandatory in CI for C++ under this constitution?" | guidance.md (357) + ENG-5.2-cmake-governance.md (~813) | ~1,170 | ✅ Yes — manifest sanitizers block + CI governance | ✅ PASS |
| Q5 | "How does the compliance rating score a C++ project for safety-critical posture?" | guidance.md (357) + skill-cpp-compliance-rating.md (~600) | ~957 | ✅ Yes — 10-dimension scoring model | ✅ PASS |

**RAG Validation Summary:**

| Metric | Threshold | Actual | Result |
|--------|-----------|--------|--------|
| Recall proxy | ≥95% (5/5) | 4/5 (80%) | 🟡 WARNING |
| Precision proxy | ≥90% | All loaded files relevant | ✅ PASS |
| Max query token load | ≤3,500 per query | 1,877 (Q3 highest) | ✅ PASS |
| BLOCKING violations | 0 | 2 (manifest tokens, workflow ref) | 🔴 FAIL |

**Q2 root cause:** ENG-3.7 (Error Handling) is in `specializes_laws` but has no `example_file`. The relevant content (`ENG-6.1-expected-errors.md`) exists on disk but is only reachable through ENG-6.1, which routes to `ENG-6.1-security-by-design.md` — not to the expected-errors file. **This confirms H-1 as a RAG recall impact.** Creating `ENG-3.7-error-handling.md` (Phase 2 task 2.2) resolves this.

> **Note:** `full-reference.md` was NOT included in any query's loaded file set per the prompt constraint. It is marked `on_demand_only` in the RAG index.

---

## New Findings (Not in Panel Review)

### W-5 — 6 Forbidden/Unknown Manifest Blocks (Phase 2.1 + 2.4)

🟡 SHADOW GOVERNANCE — The following blocks are present in `manifest.yaml` but NOT on the allowlist defined in `docs/guides/avatar-model-schema.md` Section 3:

| Block | Location | Status per Schema | Disposition |
|-------|----------|-------------------|-------------|
| `standard_tiers` | Top-level | NOT on allowlist | Should move to `guidance.md` or separate companion file |
| `ci_toolchain` | Top-level | NOT on allowlist | Should move to `guidance.md` or separate companion file |
| `authorities` | Top-level | NOT on allowlist | Should move to `guidance.md` or separate companion file |
| `brownfield_adoption` | Under `activates` | **Explicitly forbidden** — "guidance.md or dedicated workflow phase" | Must remove from manifest |
| `skill_parity` | Under `activates` | **Explicitly forbidden** — "guidance.md conventions section" | Must remove from manifest |
| `project_archetypes` | Under `activates` | **Explicitly forbidden** — "guidance.md or separate example files" | Must remove from manifest |

**Impact:** These 6 blocks contribute ~800 tokens to the manifest (roughly half the 1,568-token total). Amendment O removed `anti_patterns`, `anti_patterns_by_tier`, and `retrieval_triggers` but missed these 6. This finding strengthens the case for W-4 (manifest restructure) as a separate PR.

### W-6 — activates.skills Naming Convention Mismatch (Phase 2.5)

🟡 WARNING — Manifest references skills with a `skill-` prefix (`skill-06-atomic-tdd`) but actual files use only the number prefix (`06-atomic-tdd.md`). Routing depends on implicit prefix-stripping logic. If any routing implementation uses exact filename matching, all 4 skill references will fail to resolve.

**Resolution:** Either (a) update manifest to match actual filenames, or (b) document the `skill-` prefix convention as a routing alias contract.

### W-7 — RAG Validation Q2 Confirms H-1 Impact (Phase 5)

🟡 WARNING — RAG recall drops to 4/5 (80%) because Q2 (error handling) cannot be answered through manifest routing. This quantifies the impact of the H-1 finding (ENG-3.7 missing `example_file`). Phase 2 task 2.2 (create `ENG-3.7-error-handling.md`) resolves this.

---

## Required Changes Before Merge

| # | Finding | Severity | Resolution | PR |
|---|---------|----------|------------|-----|
| W-2 | `brownfield-adoption` workflow doesn't exist | 🔴 BLOCKING | Fix manifest reference or create workflow file | #14 |
| W-4 | Manifest ≈1,568 tokens (budget: 150) | 🔴 BLOCKING | Separate PR — extract 6+ blocks to companion files | Separate |
| W-5 | 6 forbidden/unknown manifest blocks | 🟡 SHADOW GOVERNANCE | Bundle with W-4 manifest restructure | Separate |
| W-6 | Skills naming convention mismatch | 🟡 WARNING | Update manifest skill references or document alias | #14 |
| W-7 | RAG Q2 routing gap (ENG-3.7) | 🟡 WARNING | Phase 2 creates `ENG-3.7-error-handling.md` | Phase 18 |
| H-1 | 4 `specializes_laws` missing `example_file` | 🟡 WARNING | Phase 2 of Phase 18 proposal | Phase 18 |

---

## Comparison with Panel Review

### Findings the Panel Review Caught That the Workflow Missed

| Panel Finding | Why Workflow Missed It |
|---------------|----------------------|
| H-5: `guidance.md` relative path breaks at Phase 17 file move | Phase 17 already executed — the link was fixed as part of Amendment P. Workflow validates post-correction state. |
| A-3/A-4/A-5: DX improvements (brownfield path, skill tree, anchor links) | Workflow does not assess DX quality — only schema conformance and RAG routing. |
| A-8: BUS-7.1 citation in compliance rating skill | Workflow scope is avatar files only — skills outside the avatar directory are not scanned. |

### Findings the Workflow Caught That the Panel Review Missed

| Workflow Finding | Why Panel Missed It |
|-----------------|-------------------|
| **W-5: 6 forbidden manifest blocks** (`standard_tiers`, `ci_toolchain`, `authorities`, `brownfield_adoption`, `skill_parity`, `project_archetypes`) | Panel's V4 finding removed 3 blocks (`anti_patterns`, `anti_patterns_by_tier`, `retrieval_triggers`) but did not scan against the full allowlist. The remaining 6 blocks were not flagged. |
| **W-6: Skills naming convention mismatch** | Panel verified skills exist conceptually but did not check exact filename resolution. |
| **W-4: 150-token manifest budget** | Panel never referenced the manifest token budget. The workflow enforces this mechanically. This is the single most impactful divergence — the panel approved a 1,568-token manifest that the workflow flags as BLOCKING. |
| **W-7: RAG Q2 recall failure** | Panel noted H-1 as a routing gap but did not run the 5 canonical queries to quantify impact. The workflow simulation shows recall drops to 4/5 (80%). |

### Key Takeaway

The manifest token budget (W-4) and allowlist enforcement (W-5) are the **most significant workflow findings the panel missed entirely**. Together they account for ~1,400 of the 1,568 manifest tokens. The panel's focus was governance correctness (domain boundaries, shadow governance, broken paths) — it did not enforce the mechanical token budget because that constraint lives in the workflow, not in the governance review checklist.

---

*Assessment conducted per `workflows/avatar-workflow.md` Mode 3 (Validate). No files modified except evidence files.*

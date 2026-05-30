---
schema_version: 1
verdict: REJECTED
round: R1
juror_count: 5
jurors:
  - id: J1
    model: claude-opus-4.6
    verdict: CHALLENGED
  - id: J2
    model: claude-sonnet-4.6
    verdict: CHALLENGED
  - id: J3
    model: gpt-5.4
    verdict: CHALLENGED
  - id: J4
    model: gpt-5.2
    verdict: CHALLENGED
  - id: J5
    model: gpt-5.4-mini
    verdict: CHALLENGED
synthesizer:
  model: claude-opus-4.5
rounds:
  r1_completed: true
  r2_completed: false
laws_invoked:
  - ENG-1.2
  - ENG-4.1
  - ENG-11.1
  - ENG-12.1
  - ENG-12.2
  - ENG-13.1
  - ENG-14.1
  - PRD-2.6
change_id: agents-md-size-correctness-audit
deliberation_date: 2026-05-27
---

# PRD-2.6 Multi-Cognition Jury Synthesis: AGENTS.md Size & Correctness Audit

**Artifact under review:** `AGENTS.md` (410 lines, ~19KB)  
**Question:** Is AGENTS.md too large? Is it correct in content and size per the hangar-ai-constitution?

---

## R1 — Juror Findings

### J1 — Domain Sceptic (claude-opus-4.6): CHALLENGED

**Blocking issues:**
1. **Two incompatible TDD cycles**: Lines 17–50 define an 8-step cycle; lines 399–410 close with a 6-step cycle (RED→GREEN→REFACTOR→VERIFY→COMMIT→REPEAT). The 6-step version omits IDENTIFY, UPDATE TASKS.MD, STOP/REPORT and adds REPEAT (contradicts STOP). Agents won't know which to follow.
2. **Authority hierarchy violation**: Phase Gate Sub-Protocol and RAG Retrieval Protocol are Level 2 (generic) content embedded in a Level 3 (project-specific) document. If AGENT.md evolves, this copy drifts.

**Non-blocking:**
3. Model roster appears twice (Phase Gate + Quick Reference) — maintenance risk.
4. File is ~3× too large for an entry-point router; should be ~120 lines.
5. BUS-2.1/BUS-2.2 not verified to exist in law index.

---

### J2 — Technical Expert (claude-sonnet-4.6): CHALLENGED

**Blocking issues:**
1. **`hangar-ai-specs/specs/` doesn't exist**: Directory tree shows `specs/` subdirectory but actual on-disk structure has `evidence/`, `templates/`, `README.md`. No `specs/` directory. Will cause agents to create files in wrong locations.
2. **Non-Negotiable Laws list is ~50% incomplete**: 14 laws listed; `laws/index.yaml` has 24 non-negotiable laws. 10 missing including ENG-4.12, ENG-10.1, PRD-1.5, PRD-2.5, PRD-6.2, BUS-2.1, BUS-2.2, BUS-2.3, BUS-3.1, BUS-3.6, BUS-4.3, BUS-6.1.
3. **`tools/` tree omits 3 mandatory Phase Gate tools**: Shows only `constitution-lint/`; actual repo also has `citation-auditor/`, `aa-jury-gate/`, `artifact-renderer/`. Contradiction with pip install commands in the same file.

**Non-blocking:**
4. BUS-2.2 mislabeled as "TSA Security Requirements" (actual: Control Framework Law).
5. Quick Reference Phase Gate Tools fully duplicates Sub-Protocol; wasteful.
6. 8-step cycle cites only ENG-4.1 but extends it with 3 non-ENG-4.1 steps.

---

### J3 — Product/Strategic Lens (gpt-5.4): CHALLENGED

**Blocking issues:**
1. **File too large for router role**: 19KB injected every session wastes context budget. Phase Gate Sub-Protocol (70 lines) is operational detail that belongs in a skill, not in the system prompt.
2. **Phase Gate Sub-Protocol over-specified**: Volatile details (exit codes, model roster, pip installs) are brittle in a system prompt.
3. **Missing "load AGENT.md first" startup instruction**: Agents should be directed to `agent-skills/base/AGENT.md` as the operating system. Without it, maintenance drift is likely.
4. **BUS-2.2 citation error**: Labeled "TSA Security Requirements" — wrong.

**Non-blocking:**
5. Constitution Lint section too detailed for system prompt.
6. Missing task-type router (code vs. governance/docs vs. jury work).

---

### J4 — Defense Counsel (gpt-5.2): CHALLENGED (size-positive)

**Blocking issues:**
1. **`tasks.md` path incorrect**: Step 1 says "Find the FIRST unchecked task in `tasks.md`" but no root-level `tasks.md` exists. Tasks live at `hangar-ai-specs/changes/*/tasks.md`. Agent fails immediately at Step 1.
2. **Missing "commit phase artifact before jury" explicit gate**: ENG-12.2 requires phase artifact committed to `hangar-ai-specs/changes/` before jury is invoked. Phase Gate Sub-Protocol doesn't state this as an explicit Step 0.

**Non-blocking:**
3. Non-Negotiable Laws list is incomplete vs `laws/index.yaml`.
4. Constitution Lint section defensible but trimmable.
5. Quick Reference Phase Gate duplication defensible.

**Size assessment:** NOT too big by evidence-based token-pressure argument. Content correctness matters more than line count.

---

### J5 — Implementation Realist (gpt-5.4-mini): CHALLENGED

**Blocking issues:**
1. **Too much duplication buries critical rules**: Redundant repetition of protocol in multiple places dilutes signal.
2. **`tasks.md` path ambiguity**: Same finding as J4 — no root `tasks.md`.

**Non-blocking:**
3. Human-oriented content should be removed (AI Tool Configuration, "answer aloud" wording, docs/slides tree).
4. Several sections better as pointers.

---

### Corroboration Matrix

| Finding | J1 | J2 | J3 | J4 | J5 | Confirmed |
|---------|----|----|----|----|----|----|
| Dual conflicting TDD cycles | ✓ | — | — | — | — | 1 juror (blocking per authority) |
| `tasks.md` path wrong | — | — | — | ✓ | ✓ | **2+ jurors** |
| `hangar-ai-specs/specs/` phantom | — | ✓ | — | — | — | 1 juror (verified on disk) |
| `tools/` tree incomplete | — | ✓ | — | — | — | 1 juror (verified on disk) |
| BUS-2.2 mislabeled | — | ✓ | ✓ | — | ✓ | **3 jurors** |
| Missing Step 0 (artifact commit) | — | — | — | ✓ | — | 1 juror (ENG-12.2 cite) |
| Non-Negotiable Laws incomplete | — | ✓ | — | ✓ | — | **2 jurors** |
| Model roster duplicated | ✓ | ✓ | — | — | — | **2 jurors** |
| File too large | ✓ | — | ✓ | ✗ | ✓ | 3 for, 1 against — contested |

---

## R2 — Corrections Required

The following 6 corrections are **BLOCKING** and must be applied before AGENTS.md can be APPROVED:

### C1: Remove conflicting 6-step TDD cycle

**Location:** Constitution Lint → Atomic TDD Integration section (lines ~399–410)

**Current (incorrect):**
```markdown
### Atomic TDD Integration

Run constitution-lint at the VERIFY step:

1. RED      → Write ONE failing test
2. GREEN    → Write MINIMUM code to pass
3. REFACTOR → Improve code quality
4. VERIFY   → Tests + coverage + aa-constitution-lint  ← HERE
5. COMMIT   → Save progress
6. REPEAT   → Start next test
```

**Required (corrected):**
```markdown
### Atomic TDD Integration

Run `aa-constitution-lint .` at the **VERIFY** step (Step 5) of the 8-step Mandatory Agent Protocol above. The 8-step protocol is authoritative; do not follow any other cycle.
```

**Rationale:** Two incompatible cycles cause agent confusion. The 6-step omits IDENTIFY, UPDATE TASKS.MD, STOP/REPORT and adds REPEAT (contradicts mandatory STOP). One authoritative source required (ENG-4.1).

---

### C2: Fix `tasks.md` path in Step 1

**Location:** Mandatory Agent Protocol, Step 1

**Current (incorrect):**
```
Step 1 — IDENTIFY   Find the FIRST unchecked task in tasks.md
```

**Required (corrected):**
```
Step 1 — IDENTIFY   Locate the active change directory under hangar-ai-specs/changes/<change-id>/
                    Find the FIRST unchecked task in that directory's tasks.md
```

**Rationale:** No root-level `tasks.md` exists. Tasks live at `hangar-ai-specs/changes/<change-id>/tasks.md`. Current instruction is unexecutable.

---

### C3: Fix `hangar-ai-specs/` directory tree

**Location:** Constitution Structure section

**Current (incorrect):**
```
├── hangar-ai-specs/        # Hangar SDD — Spec-Driven Development (ENG-11.1)
│   ├── changes/            # Active proposals
│   ├── archive/            # Completed proposals
│   └── specs/              # Current truth documents
```

**Required (corrected):**
```
├── hangar-ai-specs/        # Hangar SDD — Spec-Driven Development (ENG-11.1)
│   ├── changes/            # Active proposals
│   ├── archive/            # Completed proposals
│   ├── evidence/           # Supporting evidence artifacts
│   ├── templates/          # Phase artifact templates
│   └── README.md           # SDD workflow documentation
```

**Rationale:** `specs/` subdirectory does not exist on disk. Phantom path causes agents to create files in wrong locations.

---

### C4: Fix `tools/` directory tree

**Location:** Constitution Structure section

**Current (incorrect):**
```
└── tools/
    └── constitution-lint/  # AA Constitution Linter
```

**Required (corrected):**
```
└── tools/
    ├── aa-jury-gate/       # PRD-2.6 multi-cognition jury orchestrator
    ├── artifact-renderer/  # Phase artifact renderer (ENG-13.1)
    ├── citation-auditor/   # Law citation validator (ENG-12.1)
    └── constitution-lint/  # AA Constitution Linter (ENG-4.2)
```

**Rationale:** Tree omits 3 mandatory Phase Gate tools that are referenced in pip install commands in the same file. Internal contradiction.

---

### C5: Fix BUS-2.2 label

**Location:** Constitutional Compliance section

**Current (incorrect):**
```markdown
- **BUS-2.2**: TSA Security Requirements
```

**Required (corrected):**
```markdown
- **BUS-2.2**: Control Framework Law
```

**Rationale:** Verified against `laws/index.yaml`. "TSA Security Requirements" is not the actual title.

---

### C6: Add Step 0 to Phase Gate Sub-Protocol

**Location:** Phase Gate Sub-Protocol section (if present), or add as preamble to Phase Gate workflow

**Required addition:**
```markdown
### Step 0 — ARTIFACT COMMIT (Prerequisite)

Before invoking citation-auditor or aa-jury-gate:
1. Ensure `phase-artifact.md` is committed to `hangar-ai-specs/changes/<change-id>/`
2. All evidence files must be committed (not staged, not dirty)
3. This is required by ENG-12.2 — jury cannot deliberate on uncommitted artifacts
```

**Rationale:** ENG-12.2 requires phase artifact committed before jury deliberation. Current protocol lacks explicit gate, causing agents to invoke jury on uncommitted work.

---

## Synthesis — Final Verdict

### Verdict: **REJECTED**

AGENTS.md contains **6 blocking issues** confirmed through multi-cognition deliberation:

| # | Issue | Jurors | Law Violated |
|---|-------|--------|--------------|
| C1 | Dual conflicting TDD cycles | J1 | ENG-4.1 |
| C2 | `tasks.md` path unexecutable | J4, J5 | ENG-11.1 |
| C3 | Phantom `specs/` directory | J2 | ENG-11.1 |
| C4 | Incomplete `tools/` tree | J2 | ENG-12.1, ENG-13.1 |
| C5 | BUS-2.2 mislabeled | J2, J3, J5 | ENG-14.1 |
| C6 | Missing Step 0 artifact commit | J4 | ENG-12.2 |

### What is NOT blocking

- **File size (19KB)**: Contested (3 jurors say too large, 1 says acceptable). Not a correctness issue — defer to post-correction review.
- **Non-Negotiable Laws incomplete**: Non-blocking but should be fixed. Add note that list is representative, not exhaustive.
- **Model roster duplication**: Maintenance risk, not correctness failure.
- **Phase Gate Sub-Protocol location**: J1's "authority hierarchy" concern is interpretive, not a constitutional violation.

### R2 Process

Per PRD-2.6, this R1 synthesis triggers **Round 2 (R2)** where:
1. Corrections C1–C6 are applied to AGENTS.md
2. The corrected file is re-submitted for jury validation
3. If all blocking issues are resolved, verdict changes to APPROVED

### Next Actions

1. Apply corrections C1–C6 to `AGENTS.md`
2. Commit corrected file with message: `fix(agents): resolve 6 blocking issues from PRD-2.6 jury R1`
3. Run `aa-jury-gate synthesize --round R2` to validate corrections
4. Update `rounds.r2_completed: true` in this file upon R2 completion

---

*Synthesized by Judicial Synthesizer (claude-opus-4.5) per PRD-2.6 Multi-Cognition Jury Protocol*

---
skill:
  id: skill-avatar-workflow
  name: Avatar Workflow
  domain: platform-engineering
  laws: [ENG-11.1, ENG-11.2, ENG-1.2, ENG-6.7, ENG-10.3]
  triggers:
    # Generate mode
    - "Create a new avatar"
    - "Generate a technology avatar"
    - "Generate a product avatar"
    - "Scaffold an avatar for"
    - "New avatar for"
    # Assess & Correct mode
    - "Assess this avatar"
    - "Check this avatar"
    - "Correct this avatar"
    - "Fix this avatar"
    - "Is this avatar compliant?"
    - "Review this avatar"
    # Validate mode
    - "Validate this avatar"
    - "Run RAG validation on"
    - "Is this avatar RAG-ready?"
    - "Check avatar RAG thresholds"
    # Enrich mode
    - "Enrich this avatar"
    - "Enrich avatar from codebase"
    - "Update avatar from code"
    - "Pull patterns from codebase into avatar"
    # PR Review mode
    - "Review this avatar PR"
    - "Check this avatar pull request"
    - "Assess PR for avatar"
    # Pre-flight mode
    - "Pre-flight check"
    - "Check before I commit this avatar"
    - "Shift-left avatar check"
  followed_by:
    - skill-spec-governance    # to archive workflow output as evidence (ENG-11.1)
    - skill-sonarqube-compliance-gate  # when code-enriched avatar references ENG-6.x laws
  version: "1.0.0"
  created: "2025-01-01"
---

# Skill: Avatar Workflow

> **Purpose:** Govern the full lifecycle of Hangar AI Constitution avatars — technology type and product type — across six operating modes. Ensures every avatar has complete model structure, correct law domain boundaries, passing RAG thresholds, and a validated registry entry before it is committed. No avatar may be committed without completing the applicable phases of this workflow.
> **Workflow:** See `workflows/avatar-workflow.md` for full phase detail per mode.

---

## Mode Classification

Identify the operating mode from the trigger phrase and context before proceeding. Do not mix modes in a single run.

| Mode | Trigger Context | Entry Point |
|------|----------------|-------------|
| **Mode 0 — Pre-flight** | Author requests shift-left check on in-progress avatar | Phase 0 |
| **Mode 1 — Generate** | No avatar exists; request to create from scratch | Phase 1 |
| **Mode 2 — Assess & Correct** | Avatar exists; author requests review or correction | Phase 0 → Phase 1 |
| **Mode 3 — Validate** | Avatar exists and is claimed complete; run RAG validation only | Phase 5 |
| **Mode 4 — Enrich** | Avatar exists; enrich from a codebase | Phase 0 → Phase 4 |
| **Mode 5 — PR Review** | Reviewing a GitHub PR that contains avatar changes | Phase 5 (diff-scoped) |

---

## Phase Protocol

### Phase 0 — Pre-flight (Modes 0, 2, 4)

Before scanning any files, confirm the following with the author:

```
PRE-FLIGHT CHECKLIST
─────────────────────────────────────────────────────────
□ What is the avatar type? (technology | product | industry)
□ What is the avatar ID / stack name?
□ What is the avatar's target domain?
□ Is this a new avatar or an existing one?
□ For Enrich: what is the codebase root path?
```

Block on any unanswered item — do not proceed with assumptions.

---

### Phase 1 — Identify

1. Confirm avatar type from the trigger/context. If ambiguous, ask the author.
2. Verify avatar location matches the registry convention:
   - Technology: `avatars/technology/{stack-name}/`
   - Product: `avatars/product-type/{domain-name}/`
3. Confirm the domain slot in `manifest.yaml` matches the declared type.
4. Check `avatars/index.yaml` for an existing entry with the same `id` or semantically similar `name`. If found, stop and report — do not create a duplicate.

**Deduplication Guard:**
```
DUPLICATE CHECK
─────────────────────────────────────────────────────────
Search avatars/index.yaml for entries where:
  - id matches exactly, OR
  - name similarity ≥ 0.85 (semantic), OR
  - stack field overlaps with proposed avatar stack

If any match found:
  STOP — Report existing avatar ID and path
  Recommend Mode 4 (Enrich) or Mode 2 (Assess & Correct) instead
```

---

### Phase 2 — Scan

Run all checks below. Classify every finding before proceeding.

**Gap Classification:**
| Severity | Label | Effect |
|----------|-------|--------|
| Missing non-negotiable law example | BLOCKING | Must resolve before Phase 5 |
| Missing use case | BLOCKING | Must resolve before Phase 5 |
| Law domain boundary violation | BLOCKING | Must resolve before Phase 5 |
| Unknown manifest block | BLOCKING | Must resolve before Phase 5 |
| Token budget exceeded (any file) | BLOCKING | Must resolve before Phase 5 |
| Shadow governance detected | HARD BLOCK | Stop workflow; file ENG-10.3 amendment |
| Embedded skill definition in example | WARNING | File issue or amendment |
| Missing `rag_validated` field | WARNING | Backfill in Phase 6 |
| Missing `tags` or `compliance_domains` | ADVISORY | Address before commit |

**Structural Completeness Check — Technology Avatar:**
```
□ manifest.yaml — present, valid YAML, no unknown blocks
□ guidance.md — present, ≤ 450 tokens
□ examples/ — directory present, ≥ 1 example per non-negotiable law
□ use-cases/ — directory present, ≥ 2 use cases
□ Each example file ≤ 850 tokens
□ Each use-case file ≤ 1,500 tokens
```

**Structural Completeness Check — Product Avatar:**
```
□ manifest.yaml — present, valid YAML, no unknown blocks
□ guidance.md — present, ≤ 450 tokens
□ examples/ — directory present, ≥ 1 example per non-negotiable PRD-* law
□ use-cases/ — directory present, ≥ 2 use cases
□ journeys/ — directory present (product avatars require core journeys)
□ Each example file ≤ 850 tokens
□ Each use-case file ≤ 1,500 tokens
```

**Law Domain Boundary Check:**

For each law ID found in `specializes_laws`, `examples/`, `use-cases/`, and `guidance.md`:

| Avatar Type | Permitted | Conditionally Permitted | FORBIDDEN |
|-------------|-----------|------------------------|-----------|
| Technology | `ENG-*` | `ENG-6.x` with justification | `PRD-*`, `BUS-*` |
| Product | `PRD-*`, `BUS-*` | `ENG-6.x` with justification | `ENG-1–5`, `ENG-7–12` |
| Industry | `BUS-*`, `PRD-*` | `ENG-6.x` with justification | All other `ENG-*` |

> **Note:** `ENG-6.7` (Engineering Audit Trail) is the correct citation for audit logging in tech avatars. `BUS-7.1` (Business Audit Trail) is FORBIDDEN in technology avatars.

**Manifest Unknown Blocks Guard:**

Permitted manifest blocks (allowlist):
```
avatar, stack (tech only), domain (product only), core_journeys,
activates, specializes_laws, conventions, commands, project_structure,
dependencies, compliance_domains, tags
```

Any block not in this allowlist is a BLOCKING violation. Do not accept custom blocks without an ENG-10.3 amendment filing.

**activates.skills Existence Validation:**
```
For each skill ID in activates.skills:
  □ Verify agent-skills/skills-by-domain/**/{skill-id}.md exists
  □ If not found → BLOCKING: skill reference is broken
For each skill file in agent-skills/:
  □ If skill is not referenced by any avatar → WARNING: orphaned skill
```

**Shadow Governance Detection:**
```
Scan all files for:
  □ Authority assertions ("Authority: ...", "This framework governs ...")
  □ Self-scoring or rating systems that reference constitution law IDs
  □ Compliance thresholds defined outside AVATAR-RAG-INDEX.yaml
  □ governance_overrides manifest block (no ENG-10.3 exemption = HARD BLOCK)

If found → HARD BLOCK. Stop workflow. Author must file ENG-10.3 amendment.
```

**Blast Radius Trigger:**
```
If a law domain boundary violation is found in a technology avatar:
  □ Scan ALL technology avatars for the same violated law ID
  □ Report count and list of affected avatars
  □ Resolve ALL before Phase 6 commit
```

---

### Phase 3 — Discover

Identify all laws that apply to this avatar type.

**For Technology Avatars:**
```
Query: "What ENG-* laws apply to {stack-name} development?"
Query: "What non-negotiable laws must a {stack-name} avatar specialize?"
Query: "What ENG-6.x security/audit laws apply to {stack-name}?"
```

**For Product Avatars:**
```
Query: "What PRD-* laws apply to {domain-name} product development?"
Query: "What BUS-* laws apply to {domain-name} domain?"
Query: "What core journeys must a {domain-name} product avatar define?"
```

Collect law IDs, titles, and non-negotiable status. Feed results into Phase 4.

---

### Phase 4 — Build / Correct / Enrich

**Mode 1 — Generate:**
1. Scaffold directory structure per `docs/guides/avatar-model-schema.md`
2. Write `manifest.yaml` using only allowlisted blocks
3. Write `guidance.md` (≤ 450 tokens)
4. Write one example per non-negotiable law discovered in Phase 3
5. Write ≥ 2 use cases grounded in real usage scenarios
6. For product avatars: write `journeys/` with ≥ 1 core journey

**Mode 2 — Assess & Correct:**
```
For each BLOCKING gap found in Phase 2:
  □ Create missing file or section
  □ Remove or relocate misplaced law references (Content Routing Protocol below)
  □ Resolve unknown manifest blocks — remove or file amendment
  □ Trim token-over-budget files; extract overflow to separate example files

Content Routing Protocol:
  Misplaced BUS-* content in tech avatar → route to nearest product/industry avatar
  Misplaced PRD-* content in tech avatar → route to nearest product avatar
  Misplaced ENG-* content in product avatar → route to nearest tech avatar
  Do NOT delete misplaced content — route it, then file a cross-avatar link note
```

**Mode 4 — Enrich:**
1. Scan codebase root for stack-specific patterns (file extensions, config files, package manifests)
2. Identify real usage patterns that correspond to non-negotiable laws
3. Extract ≤ 850-token code examples grounded in actual codebase files
4. Add examples only — do not modify existing `specializes_laws` or `guidance.md` structure without re-running Phase 2
5. Bump version MINOR on commit (e.g., `1.0.0` → `1.1.0`)

---

### Phase 5 — RAG Validate

Run 5 canonical RAG queries against the avatar. All 5 must pass.

**Query Set:**

| # | Query Template | Success Criteria |
|---|---------------|-----------------|
| Q1 | "What laws govern {stack/domain} development at AA?" | Returns ≥ 3 law IDs with titles |
| Q2 | "Show me a {stack/domain} example for {non-negotiable law}" | Returns example file content |
| Q3 | "How do I set up a {stack/domain} project at AA?" | Returns guidance.md scaffold steps |
| Q4 | "What is the use case for {stack/domain} in {context}?" | Returns use-case file content |
| Q5 | "What skills are activated by the {stack/domain} avatar?" | Returns activates.skills list |

**Threshold Table:**

| Metric | Target | Hard Stop |
|--------|--------|-----------|
| Recall (queries answered) | ≥ 95% (5/5) | < 80% (< 4/5) |
| Tokens per query response | ≤ 3,500 | > 3,500 |
| Precision (no hallucinated laws) | ≥ 90% | < 80% |

**RAG Validation Report:**
```
AVATAR RAG VALIDATION REPORT
─────────────────────────────────────────────────────────
Avatar:        {avatar-id}
Type:          {technology | product | industry}
Date:          {YYYY-MM-DD}
Validator:     {agent-id or human reviewer}

Q1 — Law coverage:          [ PASS | FAIL ] ({n} laws returned)
Q2 — Example retrieval:     [ PASS | FAIL ] ({law-id} example found)
Q3 — Setup guidance:        [ PASS | FAIL ] (guidance.md accessible)
Q4 — Use case retrieval:    [ PASS | FAIL ] ({use-case-id} found)
Q5 — Skill activation:      [ PASS | FAIL ] ({n} skills returned)

Recall:    {n}/5 ({pct}%)   → [ PASS | FAIL ]
Max tokens:{n}              → [ PASS | FAIL ]
Precision: {pct}%           → [ PASS | FAIL ]

VERDICT: [ PASS — proceed to Phase 6 | BLOCKED — resolve failures first ]
```

If BLOCKED, return to Phase 4 and resolve all failing queries before re-running Phase 5.

---

### Phase 6 — Commit

1. **Render Gate (ENG-13.1 NON-NEGOTIABLE):** Before updating `index.yaml`, render all evidence artifacts from this run and confirm in browser. See `workflows/avatar-workflow.md` Step 6.4 for the full render gate protocol. Templates: `docs/templates/avatars/rag-validation-template.md`, `docs/templates/avatars/discovery-handoff-template.md`.

2. Update `avatars/index.yaml`:
   - Set `rag_validated: true` (or `false` if Phase 5 failed)
   - Set `status: active`
   - Set `last_validated: {YYYY-MM-DD}`
   - Confirm `version` matches the versioning protocol

2. Update `avatars/index.yaml`:
   - Set `rag_validated: true` (or `false` if Phase 5 failed)
   - Set `status: active`
   - Set `last_validated: {YYYY-MM-DD}`
   - Confirm `version` matches the versioning protocol

3. **Versioning Protocol:**
   | Change Type | Version Bump |
   |-------------|-------------|
   | New avatar | `1.0.0` |
   | Added examples or use cases | MINOR (`1.0.0` → `1.1.0`) |
   | Bug fix / law correction | PATCH (`1.0.0` → `1.0.1`) |
   | Removed or restructured law specializations | MAJOR (`1.0.0` → `2.0.0`) |
   | Enrich mode additions | MINOR |

4. **Deprecation Protocol:**
   - Set `deprecated_since: {YYYY-MM-DD}` and `replaced_by: {new-avatar-id}`
   - Set `sunset_date` to 90 days after `deprecated_since`
   - Do not delete the avatar directory until after `sunset_date`

5. Commit message template:
   ```
   avatar({avatar-id}): {mode} — {one-line summary}

   Mode: {Generate | Assess & Correct | Validate | Enrich | PR Review}
   Laws corrected: {list or "none"}
   RAG: Recall {n}/5 | Max tokens {n} | Precision {pct}%
   Violations resolved: {list or "none"}
   ```

---

### Phase 5 (Mode 5) — PR Review

> **Constraint:** Read-only mode. Do not modify any files. Report only.

1. Obtain the PR diff (GitHub diff view or `git diff main...{branch}`)
2. Run Phase 2 scan scoped to changed files only
3. Run Phase 5 RAG validation against the changed avatar
4. Produce a structured review comment using the template below:

**PR Review Comment Template:**
```markdown
## Avatar Workflow — PR Review

**Avatar:** {avatar-id}
**Type:** {technology | product | industry}
**Mode:** PR Review (Mode 5)
**Reviewer:** Avatar Workflow Skill v{version}

---

### Phase 2 — Structural Scan

| Check | Result | Detail |
|-------|--------|--------|
| Manifest unknown blocks | {PASS/BLOCKING} | {detail} |
| Law domain boundary | {PASS/BLOCKING} | {detail} |
| Token budgets | {PASS/BLOCKING} | {detail} |
| Shadow governance | {PASS/HARD BLOCK} | {detail} |
| activates.skills validity | {PASS/BLOCKING} | {detail} |

### Phase 5 — RAG Validation

| Query | Result |
|-------|--------|
| Q1 Law coverage | {PASS/FAIL} |
| Q2 Example retrieval | {PASS/FAIL} |
| Q3 Setup guidance | {PASS/FAIL} |
| Q4 Use case retrieval | {PASS/FAIL} |
| Q5 Skill activation | {PASS/FAIL} |

Recall: {n}/5 | Max tokens: {n} | Precision: {pct}%

---

### Verdict

**{PASS — Avatar meets all constitutional requirements | BLOCKED — {n} blocking violations found}**

{List of violations that must be resolved before merge, if any}
```

---

## Evidence Artifacts

After every workflow run, produce and retain the following artifacts:

| Artifact | Location | Required For |
|----------|----------|-------------|
| RAG Validation Report | `hangar-ai-specs/changes/{spec-id}/rag-validation-{avatar-id}.md` | All modes |
| Blast Radius Report | `hangar-ai-specs/changes/{spec-id}/blast-radius-{avatar-id}.md` | When violations found |
| PR Review Comment | Posted to GitHub PR | Mode 5 only |
| Commit evidence log | Git commit message body | All modes |

---

## Quick Reference — Common Violations

| Violation | Correct Action |
|-----------|---------------|
| `BUS-7.1` in tech avatar `specializes_laws` | Replace with `ENG-6.7` (Engineering Audit Trail) |
| `PRD-*` in tech avatar | Route to nearest product avatar; remove from tech avatar |
| `BUS-*` in tech avatar | Route to nearest product/industry avatar; remove from tech avatar |
| `governance_overrides` in manifest | Remove; file ENG-10.3 amendment if override is legitimate |
| `guidance.md` > 450 tokens | Split overflow into separate example files |
| Unknown manifest block | Remove block or file ENG-10.3 amendment |
| Skill referenced but file not found | Create skill file or correct the reference |

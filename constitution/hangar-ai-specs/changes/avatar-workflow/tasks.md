# Tasks: avatar-workflow

> Atomic tasks following the Hangar AI Constitution strictly.
> Update status after each task completes.
> Laws enforced: ENG-11.1 (NON-NEGOTIABLE), ENG-1.2, ENG-11.2, ENG-11.3

---

## Workstream 1 — Avatar Model Schema

- [x] **1-01** Create `docs/guides/avatar-model-schema.md` — explicit lintable schema: required manifest fields by avatar type, guidance.md structure, examples requirements, use-cases requirements, token budgets per document, known manifest block allowlist
- [ ] **1-02** Add schema cross-references to `AVATAR-RAG-INDEX.yaml` header (link to schema doc)

---

## Workstream 2 — Avatar Workflow

- [x] **2-01** Create `workflows/avatar-workflow.md` — frontmatter (id, name, laws, skills, modes), mode table, phase table, Phase 0 Pre-flight detail
- [x] **2-02** Add Phase 1 (Identify) — mode classification table, domain slot confirmation, avatar location check
- [x] **2-03** Add Phase 2 (Scan) — structural completeness check, gap classification (BLOCKING / WARNING / ADVISORY), manifest unknown blocks guard, activates.skills existence validation, blast radius trigger
- [x] **2-04** Add Phase 3 (Discover) — law discovery by avatar type, 5 canonical RAG query pattern definition
- [x] **2-05** Add Phase 4 (Build / Correct / Enrich) — Generate scaffold steps, Assess & Correct gap resolution table, Enrich codebase discovery steps, content routing protocol
- [x] **2-06** Add Phase 5 (RAG Validate) — 5-query simulation, threshold table (recall ≥95%, ≤3500 tokens), RAG validation report template, hard-stop gate
- [x] **2-07** Add Phase 6 (Commit) — registry update steps, versioning protocol (semver rules), deprecation model, commit message template
- [x] **2-08** Add Phase 5 (PR Review mode) — diff-scoped scan, read-only constraint, review comment template, PASS/BLOCKED verdict

---

## Workstream 3 — Agent Skill

- [x] **3-01** Create `agent-skills/skill-avatar-workflow.md` — frontmatter (id, name, laws, version), trigger phrases for all 6 modes, phase protocol per mode, RAG simulation procedure, evidence artifact list

---

## Workstream 4 — Registry Updates

- [x] **4-01** Update `workflows/README.md` — add avatar-workflow row to the workflow registry table with laws (ENG-11.1, ENG-1.2) and skills (skill-avatar-workflow, skill-spec-governance)

---

## Workstream 5 — Avatar Index Schema Update

- [x] **5-01** Update `avatars/index.yaml` schema — add `rag_validated` (boolean), `status` (active / deprecated), `last_validated` (date), `deprecated_since`, `replaced_by`, `sunset_date` fields to the index entry schema
- [x] **5-02** Backfill all existing avatar entries in `avatars/index.yaml` with `rag_validated: unknown` and `status: active`

---

## Workstream 6 — Backfill Live Law Boundary Violations

> These are the 6 confirmed violations found in the existing avatar corpus.
> Each is an Assess & Correct run targeting only the law boundary violation — no other changes.

- [x] **6-01** Correct `avatars/technology/react-typescript/manifest.yaml` — remove `PRD-3.4` from `specializes_laws`; remove `examples/PRD-3.4-accessibility.md` reference; update manifest version to next MAJOR (boundary removal = MAJOR bump)
- [x] **6-02** Correct `avatars/technology/databricks-pyspark/manifest.yaml` — remove `BUS-7.1`; replace with `ENG-6.7` if not already present; update version
- [x] **6-03** Correct `avatars/technology/postgresql-sqlalchemy/manifest.yaml` — remove `BUS-7.1`; replace with `ENG-6.7` if not already present; update version
- [x] **6-04** Correct `avatars/technology/azure-openai/manifest.yaml` — remove `BUS-7.1`; replace with `ENG-6.7` if not already present; update version
- [x] **6-05** Correct `avatars/technology/opentelemetry-python/manifest.yaml` — remove `BUS-7.1`; replace with `ENG-6.7` if not already present; update version
- [x] **6-06** Correct `avatars/technology/operations-research-optimizer/manifest.yaml` — remove `BUS-2.1`; update version; add routing note in evidence pointing `BUS-2.1` patterns to the appropriate product avatar
- [x] **6-07** Commit all 6 corrections in a single constitutional correction commit with blast-radius evidence file at `hangar-ai-specs/evidence/avatar-law-boundary-blast-radius.md`

---

## Final

- [x] **F-01** Verify `workflows/README.md` accurately reflects all 6 workflows including avatar-workflow
- [x] **F-02** Verify `avatars/index.yaml` schema is valid YAML and all existing entries parse correctly
- [x] **F-03** Commit proposal and tasks to `hangar-ai-specs/changes/avatar-workflow/` and open PR against main following ENG-11.1

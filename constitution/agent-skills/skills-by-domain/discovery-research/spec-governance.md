---
skill:
  id: skill-spec-governance
  name: "Hangar SDD: Spec Governance"
  category: orchestration
  version: "1.0.0"

laws:
  implements:
    - id: ENG-11.1
      title: Hangar SDD Law
    - id: ENG-11.2
      title: Proposal Completeness Law
    - id: BUS-7.1
      title: Audit Trail Law
  references:
    - id: ENG-4.1
      title: Atomic TDD Law
    - id: ENG-10.1
      title: Constitution Metrics Collection Law
    - id: PRD-2.1
      title: Problem Validation Law

triggers:
  phrases:
    - "Let's create a new feature"
    - "Start a new change"
    - "What's the next step?"
    - "Check compliance for this work"
    - "Scaffold a proposal"
    - "Archive this work"

followed_by:
  - skill-01-roadmapping
  - skill-02-user-journey-mapping
  - skill-03-executable-spec
  - skill-06-atomic-tdd
---

# Skill: Hangar SDD — Spec Governance

> **Purpose:** Govern the `hangar-ai-specs/` lifecycle for spec-driven development with constitutional compliance. This skill is tool-independent — no external CLI required. Per ENG-11.1 (NON-NEGOTIABLE).

---

## Purpose

The Hangar SDD (Spec-Driven Development) process ensures human-AI alignment before implementation. Every project adopting the constitution MUST have a `hangar-ai-specs/` folder (ENG-11.1).

**Three-stage lifecycle:**
```
PROPOSE → IMPLEMENT → ARCHIVE
```

---

## `hangar-ai-specs/` Folder Contract

```
hangar-ai-specs/
  changes/                    ← active proposals (in-flight work)
    [verb-noun-id]/
      PROPOSAL.md             ← problem, solution, deliverables, success criteria (ENG-11.2)
      tasks.md                ← work breakdown with checkbox status
      design.md               ← (optional) architecture and design decisions
      SPEC.md                 ← (optional) detailed technical specification
      PROGRESS.md             ← implementation tracking (phases, blockers)
  archive/                    ← completed proposals
    YYYY-MM-DD-[id]/          ← renamed on archive with all files
  specs/                      ← current truth documents (living specs)
    [domain]/
```

---

## When to Invoke

- Starting any new work item of significant scope
- Creating or updating a proposal
- Planning implementation for a vertical slice
- Reviewing work for constitutional compliance
- Archiving completed work

---

## Procedure

### 1. PROPOSE — Create a new changeset

```bash
mkdir -p hangar-ai-specs/changes/[verb-noun-id]
```

Create `PROPOSAL.md` with:
- Problem (what is broken/missing)
- Solution (what we will do)
- Deliverables (concrete outputs)
- Success Criteria (measurable)
- References (law IDs — required per ENG-11.2)

Create `tasks.md` with checkbox list of all implementation tasks.

**Validation:** `PROPOSAL.md` MUST cite at least one law ID. Per ENG-11.2: proposals without law citations SHALL be rejected.

### 2. IMPLEMENT — Execute the changeset

- Find FIRST unchecked task in `tasks.md`
- Implement following applicable skill (ENG-4.1 for code tasks)
- Mark `[x]` in `tasks.md` after each task completes
- Update `PROGRESS.md` with phase status and any blockers

### 3. ARCHIVE — Complete the changeset

Move completed folder:
```bash
mv hangar-ai-specs/changes/[id] hangar-ai-specs/archive/$(date +%Y-%m-%d)-[id]
```

Update `PROGRESS.md` status to COMPLETE before archiving.

---

## Quality Checklist

- [ ] `PROPOSAL.md` cites ≥1 law ID (ENG-11.2)
- [ ] `tasks.md` has checkbox list
- [ ] All tasks `[x]` before archiving
- [ ] `PROGRESS.md` reflects current state
- [ ] Archived proposals dated (YYYY-MM-DD prefix)
- [ ] Audit trail maintained (BUS-7.1)

# SPEC: Adoption Guide Constitutional Alignment

## Constitutional Authority

This proposal ensures the adoption guides themselves comply with constitutional requirements:

| Law ID | Title | How It Applies |
|--------|-------|----------------|
| **ENG-1.2** | AI-Engineer Pairing Law | "Every decision references the constitutional principle behind it" - Guides must cite laws |
| **ENG-6.4** | Decision Documentation Law | "Architecture decisions documented" - Adoption guides ARE architecture decisions |
| **ENG-6.1** | Self-Documenting Code Law | Guides should be self-documenting with clear law references |
| **PRD-3.1** | Acceptance Criteria Law | Guides need clear success criteria tied to law compliance |

---

## Problem Statement

### Current State

The adoption guides in `docs/guides/adoption/` describe **WHAT** to do but not **WHY** constitutionally:

| Guide | Lines | Law Citations | Status |
|-------|-------|---------------|--------|
| brownfield-adoption.md | 668 | 0 | ❌ No constitutional authority |
| greenfield-adoption.md | ~400 | 0 | ❌ No constitutional authority |

### Impact

Per **ENG-1.2 (AI-Engineer Pairing Law)**: "Every decision references the constitutional principle behind it."

Without law citations:
- AI agents don't know which laws mandate each practice
- Engineers can't verify adoption compliance
- Inconsistent adoption across projects
- No authority hierarchy established

### Laws Not Referenced in Any Adoption Guide

| Category | Laws Missing | Impact |
|----------|--------------|--------|
| Principles | ENG-1.1, ENG-1.3, ENG-1.4 | No foundation |
| Architecture | ENG-2.1, ENG-2.2, ENG-2.3 | No structure guidance |
| Complexity | ENG-3.1, ENG-3.2, ENG-3.4 | No quality gates |
| Testing | ENG-4.1, ENG-4.2, ENG-4.4, ENG-4.5, ENG-4.6, ENG-4.7 | No test standards |
| Security | ENG-6.1, ENG-6.4, ENG-6.5, ENG-6.7 | No security guidance |
| Product | PRD-5.1 | No OpenSpec authority |

---

## Proposed Solution

Update adoption guides to cite constitutional laws for every instruction, add compliance checklists, and provide standardized templates.

---

## Slices

### Slice 1: Brownfield Adoption Guide Updates

**File:** `docs/guides/adoption/brownfield-adoption.md`

**Changes:**

1. **Add Constitutional Authority section** at top:
```markdown
## Constitutional Authority

This guide implements the following laws:

| Law ID | Title | Section |
|--------|-------|---------|
| ENG-4.1 | Atomic TDD Law | Phase 1: Characterization Tests |
| ENG-1.3 | Continuous Refactoring Law | Phase 1: Safety Net |
| ENG-4.6 | Coverage Requirements | Phase 1: Critical Paths |
| ENG-4.4 | Test Structure Law | Phase 1: Test Format |
| ENG-4.5 | Test Naming Convention | Phase 1: Test Names |
| ENG-2.3 | Vertical Slice Law | Phase 2: New Features |
| ENG-1.4 | Incremental Improvement Law | Phase 3: Strangler Fig |
| ENG-6.7 | Audit Trail Law | Phase 1: Document Behavior |
| PRD-5.1 | OpenSpec Protocol | Phase 2: Proposals |
```

2. **Add law citations inline** throughout:
   - Phase 1: "Per **ENG-4.1**, write characterization tests before ANY refactoring"
   - Phase 1: "Per **ENG-1.3**, NEVER refactor without tests"
   - Phase 1: "Per **ENG-4.6**, critical paths require 100% coverage"
   - Phase 2: "Per **ENG-2.3**, deliver features as vertical slices"
   - Phase 3: "Per **ENG-1.4**, break large changes into incremental slices"

3. **Add Security section**:
```markdown
## Security Considerations

Per **ENG-6.1 (Security by Design)** and **ENG-6.5 (Input Validation Law)**:

- [ ] Review existing input validation
- [ ] Document security debt in project-rules.md
- [ ] Prioritize security fixes in Phase 2
```

4. **Add Compliance Checklist** at end:
```markdown
## Adoption Compliance Checklist

### Phase 1 Complete When:
- [ ] AGENTS.md created (ENG-1.2)
- [ ] openspec/ structure created (PRD-5.1)
- [ ] project-rules.md documents adaptations (ENG-1.2)
- [ ] Characterization tests exist (ENG-4.1, ENG-1.3)
- [ ] Tests follow Given-When-Then (ENG-4.4)
- [ ] Tests follow naming convention (ENG-4.5)
- [ ] Critical paths have 100% coverage (ENG-4.6)
```

---

### Slice 2: Greenfield Adoption Guide Updates

**File:** `docs/guides/adoption/greenfield-adoption.md`

**Changes:**

1. **Add Constitutional Authority section** at top (similar to brownfield)

2. **Add law citations inline**:
   - Setup: "Per **ENG-1.2**, create AGENTS.md as AI entry point"
   - Architecture: "Per **ENG-2.2 (Layered Architecture)**, maintain clear layer separation"
   - Architecture: "Per **ENG-2.3 (Vertical Slice)**, deliver complete slices"
   - TDD: "Per **ENG-4.1**, practice Atomic TDD - ONE test at a time"
   - Quality: "Per **ENG-3.1**, cyclomatic complexity ≤10"
   - Quality: "Per **ENG-3.2**, cognitive complexity ≤7"

3. **Add Quality Gates section**:
```markdown
## Quality Gates

Per Constitution laws, all code MUST pass:

| Gate | Law | Threshold |
|------|-----|-----------|
| Cyclomatic Complexity | ENG-3.1 | ≤10 per method |
| Cognitive Complexity | ENG-3.2 | ≤7 per method |
| Method Length | ENG-3.4 | ≤50 lines |
| Test Coverage (new code) | ENG-4.6 | ≥90% |
| Test Coverage (critical) | ENG-4.6 | 100% |
```

4. **Add Compliance Checklist** at end

---

### Slice 3: AGENTS.md Template

**File:** `docs/templates/AGENTS.md` (NEW)

**Content:**
```markdown
# AGENTS.md - AI Entry Point

> **READ THIS FIRST** before making any changes to this codebase.
> Per **ENG-1.2 (AI-Engineer Pairing Law)**: AI assistants SHALL follow the Constitution strictly.

## Constitutional Authority

This project is governed by the **hangar-ai-constitution**.

## Authority Hierarchy

Per **ENG-1.1 (Priority Hierarchy)**:

```
┌─────────────────────────────────────────────────────────┐
│                  AUTHORITY PRECEDENCE                   │
├─────────────────────────────────────────────────────────┤
│  1. hangar-ai-constitution                           │
│     └── Engineering Laws are NON-NEGOTIABLE             │
│                                                         │
│  2. openspec/project-rules.md                           │
│     └── Project-specific adaptations WITHIN law bounds  │
│                                                         │
│  3. This file (AGENTS.md)                               │
│     └── Quick reference and entry point                 │
│                                                         │
│  4. openspec/changes/*/SPEC.md                          │
│     └── Current work specifications                     │
└─────────────────────────────────────────────────────────┘
```

## Technology Stack

| Layer | Technology | Version |
|-------|------------|---------|
| Language | {{LANGUAGE}} | {{VERSION}} |
| Framework | {{FRAMEWORK}} | {{VERSION}} |
| Database | {{DATABASE}} | {{VERSION}} |
| Build | {{BUILD_TOOL}} | {{VERSION}} |

## Domain Context

{{DOMAIN_DESCRIPTION}}

## Non-Negotiable Laws

| Law ID | Title | Summary |
|--------|-------|---------|
| **ENG-4.1** | Atomic TDD Law | TDD in atomic cycles - ONE test at a time |
| **ENG-6.1** | Security by Design | Security built in, not bolted on |
| **ENG-6.4** | Data Protection | All sensitive data protected |
| **ENG-6.7** | Audit Trail | All sensitive operations logged |

## Before You Code

1. **Read** `openspec/project-rules.md`
2. **Check** `openspec/changes/` for active work
3. **Follow** the Constitution laws
4. **Test First** - Per **ENG-4.1**, no exceptions
```

---

### Slice 4: project-rules.md Template

**File:** `docs/templates/project-rules.md` (NEW)

**Content:**
```markdown
# Project Rules - {{PROJECT_NAME}}

> Project-specific adaptations within Constitutional law boundaries.
> Per **ENG-1.2**: Every decision references the constitutional principle behind it.

## Constitution Reference

- **Source:** `{{PATH_TO_CONSTITUTION}}`
- **Compliance Status:** {{STATUS}}

## Technology Decisions

### {{TECHNOLOGY}} Version: {{VERSION}}
- **Constraint:** {{CONSTRAINT_DESCRIPTION}}
- **Impact per {{LAW_ID}}:** {{IMPACT}}
- **Adaptation:** {{ADAPTATION}}

## Law Adaptations

### {{LAW_ID}} ({{LAW_NAME}}) - ADAPTED

| Standard Requirement | Project Adaptation | Rationale |
|---------------------|-------------------|-----------|
| {{STANDARD}} | {{ADAPTATION}} | {{RATIONALE}} |

## Domain Rules (Business Critical)

Per **ENG-1.1 (Priority Hierarchy)** - Correctness is #2 priority.

### {{DOMAIN_RULE_NAME}}
{{DOMAIN_RULE_DESCRIPTION}}

## Known Technical Debt

Per **ENG-3.4 (Single Responsibility)** - documented for future remediation:

| Debt Item | Violates | Impact | Remediation Phase |
|-----------|----------|--------|-------------------|
| {{DEBT}} | {{LAW}} | {{IMPACT}} | {{PHASE}} |

## Adoption Phases

### Phase 1: {{PHASE_1_NAME}} (CURRENT)
- [ ] {{TASK}} ({{LAW_ID}})

### Phase 2: {{PHASE_2_NAME}} (NEXT)
- [ ] {{TASK}} ({{LAW_ID}})
```

---

### Slice 5: Adoption Compliance Checklist

**File:** `docs/guides/adoption/adoption-compliance-checklist.md` (NEW)

**Content:**
```markdown
# Adoption Compliance Checklist

> Use this checklist to verify your project's constitutional adoption is complete.

## Governance Files

| Item | Law | Required | Verified |
|------|-----|----------|----------|
| AGENTS.md at project root | ENG-1.2 | ✓ | [ ] |
| openspec/ directory | PRD-5.1 | ✓ | [ ] |
| openspec/project-rules.md | ENG-1.2 | ✓ | [ ] |
| openspec/CONSTITUTION.md | ENG-6.4 | ✓ | [ ] |
| openspec/changes/ directory | PRD-5.1 | ✓ | [ ] |
| openspec/specs/ directory | PRD-5.1 | ✓ | [ ] |
| openspec/archive/ directory | PRD-5.1 | ✓ | [ ] |

## AGENTS.md Content

| Item | Law | Required | Verified |
|------|-----|----------|----------|
| Authority hierarchy documented | ENG-1.1 | ✓ | [ ] |
| Technology stack listed | ENG-6.4 | ✓ | [ ] |
| Domain context explained | ENG-2.1 | ✓ | [ ] |
| Non-negotiable laws listed | ENG-4.1, ENG-6.x | ✓ | [ ] |
| "Before You Code" checklist | ENG-1.2 | ✓ | [ ] |

## project-rules.md Content

| Item | Law | Required | Verified |
|------|-----|----------|----------|
| Constitution reference path | ENG-1.2 | ✓ | [ ] |
| Technology constraints documented | ENG-6.4 | ✓ | [ ] |
| Law adaptations with rationale | ENG-1.2 | ✓ | [ ] |
| Domain rules documented | ENG-2.1 | ✓ | [ ] |
| Technical debt catalogued | ENG-1.3 | ✓ | [ ] |
| Adoption phases defined | ENG-1.4 | ✓ | [ ] |

## Testing (Brownfield)

| Item | Law | Required | Verified |
|------|-----|----------|----------|
| Characterization tests exist | ENG-4.1 | ✓ | [ ] |
| Tests follow Given-When-Then | ENG-4.4 | ✓ | [ ] |
| Tests follow naming convention | ENG-4.5 | ✓ | [ ] |
| Critical paths 100% covered | ENG-4.6 | ✓ | [ ] |
| Tests are isolated | ENG-4.7 | ✓ | [ ] |

## Testing (Greenfield)

| Item | Law | Required | Verified |
|------|-----|----------|----------|
| TDD practiced (test first) | ENG-4.1 | ✓ | [ ] |
| Test pyramid maintained | ENG-4.2 | ✓ | [ ] |
| Tests follow Given-When-Then | ENG-4.4 | ✓ | [ ] |
| Tests follow naming convention | ENG-4.5 | ✓ | [ ] |
| New code ≥90% coverage | ENG-4.6 | ✓ | [ ] |
| Critical paths 100% coverage | ENG-4.6 | ✓ | [ ] |

## Quality Gates

| Item | Law | Threshold | Verified |
|------|-----|-----------|----------|
| Cyclomatic complexity | ENG-3.1 | ≤10 | [ ] |
| Cognitive complexity | ENG-3.2 | ≤7 | [ ] |
| Method length | ENG-3.4 | ≤50 lines | [ ] |
| Class length | ENG-3.4 | ≤300 lines | [ ] |

## Security

| Item | Law | Required | Verified |
|------|-----|----------|----------|
| Input validation reviewed | ENG-6.5 | ✓ | [ ] |
| Security debt documented | ENG-6.1 | ✓ | [ ] |
| Sensitive data protected | ENG-6.4 | ✓ | [ ] |
| Audit logging in place | ENG-6.7 | ✓ | [ ] |
```

---

## Out of Scope

- Updating practice guides (separate proposal)
- Updating law definitions
- Adding new laws
- Tooling changes

---

## Success Criteria

| Metric | Target |
|--------|--------|
| Laws cited in brownfield guide | ≥15 |
| Laws cited in greenfield guide | ≥12 |
| Compliance checklist items | ≥30 with law IDs |
| Templates created | 2 (AGENTS.md, project-rules.md) |

---

## Estimated Effort

| Slice | Effort | Priority |
|-------|--------|----------|
| Slice 1: Brownfield guide | Medium | High |
| Slice 2: Greenfield guide | Medium | High |
| Slice 3: AGENTS.md template | Low | High |
| Slice 4: project-rules.md template | Low | High |
| Slice 5: Compliance checklist | Medium | High |

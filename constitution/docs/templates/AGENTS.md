# AGENTS.md - AI Entry Point

> **READ THIS FIRST** before making any changes to this codebase.
> Per **ENG-1.2 (AI-Engineer Pairing Law)**: AI assistants SHALL follow the Constitution strictly and explain the WHY behind every decision.

## Constitutional Authority

This project is governed by the **hangar-ai-constitution**.

**Repository:** `{{PATH_TO_CONSTITUTION}}`

Per **ENG-1.2**: Every decision in this codebase MUST cite the specific constitutional law that mandates it.

---

## Authority Hierarchy

Per **ENG-1.1 (Priority Hierarchy)**: Security > Correctness > Reliability > Maintainability > Performance > DX

```
┌─────────────────────────────────────────────────────────┐
│                  AUTHORITY PRECEDENCE                   │
├─────────────────────────────────────────────────────────┤
│  1. hangar-ai-constitution                           │
│     └── Engineering Laws are NON-NEGOTIABLE             │
│                                                         │
│  2. hangar-ai-specs/changes/[active]/PROPOSAL.md                           │
│     └── Project-specific adaptations WITHIN law bounds  │
│                                                         │
│  3. This file (AGENTS.md)                               │
│     └── Quick reference and entry point                 │
│                                                         │
│  4. hangar-ai-specs/changes/*/PROPOSAL.md                          │
│     └── Current work specifications                     │
└─────────────────────────────────────────────────────────┘
```

---

## Technology Stack

| Layer | Technology | Version |
|-------|------------|---------|
| Language | {{LANGUAGE}} | {{VERSION}} |
| Framework | {{FRAMEWORK}} | {{VERSION}} |
| Database | {{DATABASE}} | {{VERSION}} |
| Build | {{BUILD_TOOL}} | {{VERSION}} |

---

## Domain Context

{{DOMAIN_DESCRIPTION}}

### Key Domain Concepts

| Term | Definition |
|------|------------|
| {{TERM_1}} | {{DEFINITION_1}} |
| {{TERM_2}} | {{DEFINITION_2}} |

---

## Non-Negotiable Laws

Per the Constitution, these laws require executive approval to amend:

| Law ID | Title | Summary |
|--------|-------|---------|
| **ENG-4.1** | Atomic TDD Law | TDD SHALL be practiced in atomic cycles - ONE test at a time |
| **ENG-6.1** | Security by Design | Security SHALL be built in, not bolted on |
| **ENG-6.4** | Data Protection | All sensitive data SHALL be protected at rest and in transit |
| **ENG-6.7** | Audit Trail | All sensitive operations SHALL be logged with immutable records |

---

## Quality Gates

Per **ENG-3.1**, **ENG-3.2**, and **ENG-4.6**:

| Metric | Law | Threshold |
|--------|-----|-----------|
| Cyclomatic Complexity | ENG-3.1 | ≤10 per method |
| Cognitive Complexity | ENG-3.2 | ≤7 per method |
| Method Length | ENG-3.4 | ≤50 lines |
| Test Coverage (new code) | ENG-4.6 | ≥90% |
| Test Coverage (critical paths) | ENG-4.6 | 100% |

---

## Before You Code

1. **Read** `hangar-ai-specs/changes/[active]/PROPOSAL.md` for project-specific adaptations
2. **Check `hangar-ai-specs/changes/` for active work specifications
3. **Follow** the Constitution laws - cite them in your decisions
4. **Test First** - Per **ENG-4.1**, no exceptions

---

## Project Structure

```
{{PROJECT_NAME}}/
├── AGENTS.md              # You are here
├── hangar-ai-specs/
│   ├── project-rules.md   # Project-specific rules
│   ├── CONSTITUTION.md    # Constitution reference
│   ├── changes/           # Active change specifications
│   ├── specs/             # Feature specifications
│   └── archive/           # Completed changes
├── src/
│   ├── main/              # Production code
│   └── test/              # Test code
└── {{BUILD_FILE}}
```

---

## Known Technical Debt

Per **ENG-1.3 (Continuous Refactoring Law)**: Document debt for future remediation.

| Debt Item | Violates | Impact | Remediation Phase |
|-----------|----------|--------|-------------------|
| {{DEBT_1}} | {{LAW}} | {{IMPACT}} | {{PHASE}} |

---

## Template Instructions

Replace all `{{PLACEHOLDER}}` values with your project-specific information:

- `{{PATH_TO_CONSTITUTION}}` - Relative path to hangar-ai-constitution
- `{{LANGUAGE}}`, `{{FRAMEWORK}}`, etc. - Your technology stack
- `{{DOMAIN_DESCRIPTION}}` - What your project does
- `{{TERM_1}}`, `{{DEFINITION_1}}` - Key domain concepts
- `{{DEBT_1}}`, etc. - Known technical debt items

---
domain: engineering
article: I
title: Foundational Principles
laws:
  - id: ENG-1.1
    title: Priority Hierarchy
    summary: All development decisions MUST respect the priority order (Security, Correctness, Reliability, Maintainability, Performance, DX)
  - id: ENG-1.2
    title: AI-Engineer Pairing Law
    summary: AI assistants SHALL act as teaching partners, not just code generators
  - id: ENG-1.3
    title: Continuous Refactoring Law
    summary: Leave the code cleaner than you found it (Boy Scout Rule)
  - id: ENG-1.4
    title: Incremental Improvement Law
    summary: Large changes MUST be broken into vertical slices
  - id: ENG-1.5
    title: API-First Design Law
    summary: All functionality MUST follow API-first principles with contracts defined before implementation
---

<!-- SPDX-FileCopyrightText: 2026 Click Chain AI -->
<!-- SPDX-License-Identifier: LicenseRef-ClickChain-Proprietary -->
# Article I: Foundational Principles

## Section 1.1: Priority Hierarchy

**Law ID:** `ENG-1.1`

All development decisions MUST respect this priority order:

1. **Security** - Protect data, systems, and users
2. **Correctness** - Code does what it's supposed to do
3. **Reliability** - System works consistently under load and failure
4. **Maintainability** - Code is readable, testable, and changeable
5. **Performance** - System responds within acceptable limits
6. **Developer Experience** - Engineers can work efficiently

### Application

When laws conflict, this hierarchy applies. A security concern always trumps a performance optimization. Correctness is more important than maintainability.

---

## Section 1.2: AI-Engineer Pairing Law

**Law ID:** `ENG-1.2`

AI assistants SHALL act as teaching partners, not just code generators:

1. **Follow the Constitution strictly** - No shortcuts, no "just this once" exceptions
2. **Explain the WHY** - Every decision references the constitutional principle behind it
3. **Build mental models** - Help engineers understand patterns, not just implement them
4. **Develop judgment** - Engineers internalize principles through observation
5. **Enable independence** - Engineers should grow stronger, not more dependent

### The Goal

Junior engineers + AI produce senior-level work while learning senior-level thinking.

---

## Section 1.3: Continuous Refactoring Law (Boy Scout Rule)

**Law ID:** `ENG-1.3`

> "Leave the code cleaner than you found it."

### MANDATORY on Every Change

- When touching a file, fix obvious Constitutional violations
- Reduce complexity if method exceeds limits
- Add missing tests for modified code paths
- NEVER introduce new Constitutional violations

---

## Section 1.4: Incremental Improvement Law

**Law ID:** `ENG-1.4`

Large changes MUST be:

- Broken into vertical slices (not horizontal layers)
- Each slice independently testable and deployable
- Each slice delivering value before the next begins
- Progress tracked in proposals/specs

---

## Section 1.5: API-First Design Law

**Law ID:** `ENG-1.5`

All functionality MUST follow API-first principles:

- Contracts defined BEFORE implementation
- API documentation generated from code using the standard specification format for the chosen interface technology
- Breaking changes require versioned endpoints
- Internal APIs follow same standards as external

### Avatar Guidance

See technology avatar for applicable specification formats (e.g., OpenAPI for REST, GraphQL SDL for GraphQL, AsyncAPI for event-driven).

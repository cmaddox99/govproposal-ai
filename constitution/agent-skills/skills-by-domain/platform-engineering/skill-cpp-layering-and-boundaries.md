---
skill:
  id: skill-cpp-layering-and-boundaries
  name: "C++ Layering and Boundaries"
  category: platform-engineering
  version: "1.0.0"
  avatar: cpp

laws:
  implements:
    - id: ENG-2.2
      title: Layered Architecture Law
    - id: ENG-2.1
      title: DDD Aggregate Root Law
  references:
    - id: ENG-3.1
      title: Complexity Limits Law

triggers:
  phrases:
    - "C++ layer separation"
    - "C++ header organization"
    - "C++ include boundaries"
    - "C++ domain model structure"

followed_by:
  - skill-08-code-review
  - skill-27-constitution-compliance
---

# Skill: C++ Layering and Boundaries

## Purpose

Enforce layered architecture in C++ projects so that domain logic, application use-cases, and infrastructure adapters remain in separate directories with unidirectional dependency flow.

## Procedure

1. **Verify directory structure** — `include/project/domain/`, `include/project/application/`, `include/project/infrastructure/` must exist
2. **Check include direction** — domain headers must NOT include application or infrastructure headers
3. **Validate aggregate boundaries** — each aggregate root owns its children via `std::vector<>` or `std::unique_ptr<>`; no cross-aggregate direct references
4. **Review namespace usage** — each layer uses its own namespace (`project::domain`, `project::application`, `project::infrastructure`)

## Governance Gate

Per [ENG-2.2](laws/engineering/eng-2-architecture.md), any `#include` from domain/ that references infrastructure/ or application/ is a **blocking violation**.

## C++ Specific Patterns

- Forward-declare across layers to minimize compile-time coupling
- Use abstract interfaces (pure virtual classes) at layer boundaries
- Domain types must be header-only or compiled into a separate static library

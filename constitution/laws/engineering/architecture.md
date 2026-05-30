---
domain: engineering
article: II
title: Architecture & Design Laws
laws:
  - id: ENG-2.1
    title: Domain-Driven Design Law
    summary: ALL projects SHALL apply DDD tactical patterns (Entities, Value Objects, Aggregates, Domain Services, Domain Events)
  - id: ENG-2.2
    title: Layered Architecture Law
    summary: All projects SHALL maintain clear layer separation (Presentation, Application, Domain, Infrastructure)
  - id: ENG-2.3
    title: Vertical Slice Architecture Law
    summary: Features SHALL be delivered as complete vertical slices
  - id: ENG-2.4
    title: Bounded Context Law
    summary: Systems SHALL be decomposed into bounded contexts with well-defined interfaces
  - id: ENG-2.5
    title: Dependency Inversion Law
    summary: High-level modules SHALL NOT depend on low-level modules; both depend on abstractions
---

<!-- SPDX-FileCopyrightText: 2026 Click Chain AI -->
<!-- SPDX-License-Identifier: LicenseRef-ClickChain-Proprietary -->
# Article II: Architecture & Design Laws

## Section 2.1: Domain-Driven Design Law

**Law ID:** `ENG-2.1`

ALL projects SHALL apply DDD tactical patterns:

### Entities

- Have identity that persists through state changes
- Primary keys are UUIDs (not auto-increment integers)
- Track creation/modification metadata
- Encapsulate behavior with their data

### Value Objects

- MUST be immutable (see ENG-3.2). Equality based on attributes, not identity
- Examples: Money, Address, EmailAddress, DateRange

### Aggregates

- Clear boundaries with single aggregate root
- External references by ID only (no object navigation)
- One repository per aggregate root
- Transactions don't span aggregates

### Domain Services

- Business logic that doesn't belong to single entity
- Stateless operations
- Named with ubiquitous language

### Domain Events

- Capture significant domain occurrences
- Immutable records of what happened
- Enable loose coupling between bounded contexts

---

## Section 2.2: Layered Architecture Law

**Law ID:** `ENG-2.2`

All projects SHALL maintain clear layer separation:

```
┌─────────────────────────────────────────┐
│  Presentation Layer (Controllers/UI)    │ ← Request/Response handling ONLY
├─────────────────────────────────────────┤
│  Application Layer (Services/Handlers)  │ ← Use case orchestration
├─────────────────────────────────────────┤
│  Domain Layer (Entities/Value Objects)  │ ← Business rules and logic
├─────────────────────────────────────────┤
│  Infrastructure Layer (Repos/Clients)   │ ← External system integration
└─────────────────────────────────────────┘
```

### Layer Rules

- **Presentation:** Request validation, response formatting, authentication checks ONLY
- **Application:** Orchestrates domain objects, transaction boundaries, no business logic
- **Domain:** Business rules, invariants, calculations - NO infrastructure dependencies
- **Infrastructure:** Database access, external APIs, messaging - implements domain interfaces

### Violations

- Business logic in controllers/handlers
- Domain objects importing infrastructure
- Cross-layer object sharing (use DTOs at boundaries)

---

## Section 2.3: Vertical Slice Architecture Law

**Law ID:** `ENG-2.3`

Features SHALL be delivered as complete vertical slices:

```
Feature A:        Feature B:        Feature C:
┌─────────┐       ┌─────────┐       ┌─────────┐
│   UI    │       │   UI    │       │   UI    │
├─────────┤       ├─────────┤       ├─────────┤
│   API   │       │   API   │       │   API   │
├─────────┤       ├─────────┤       ├─────────┤
│ Service │       │ Service │       │ Service │
├─────────┤       ├─────────┤       ├─────────┤
│  Repo   │       │  Repo   │       │  Repo   │
├─────────┤       ├─────────┤       ├─────────┤
│  Tests  │       │  Tests  │       │  Tests  │
└─────────┘       └─────────┘       └─────────┘
```

### Rules

- Complete one slice before starting the next
- Each slice independently deployable
- Horizontal layer-by-layer development PROHIBITED
- Each slice includes tests at all levels

---

## Section 2.4: Bounded Context Law

**Law ID:** `ENG-2.4`

Systems SHALL be decomposed into bounded contexts:

- Each context has its own ubiquitous language
- Contexts communicate via well-defined interfaces (APIs, events)
- No shared databases between contexts
- Context mapping documents relationships (Customer/Supplier, Conformist, etc.)

---

## Section 2.5: Dependency Inversion Law

**Law ID:** `ENG-2.5`

High-level modules SHALL NOT depend on low-level modules:

- Both depend on abstractions (interfaces)
- Abstractions defined in the layer that uses them
- Implementations provided by infrastructure layer
- Enables testing without real infrastructure

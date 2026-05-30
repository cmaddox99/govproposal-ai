---
laws: [ENG-2.1]
avatar: [java-spring]
title: Domain-Driven Design — Java/Spring
---

# ENG-2.1: Domain-Driven Design — java-spring

Organise code around bounded contexts. Booking, Loyalty, and Operations are separate bounded contexts with explicit interfaces.

## Bounded Context Example (Java/Spring)

Domain entities must not reference infrastructure concerns. Aggregates enforce invariants.

**Rule**: Cross-context communication via domain events or anti-corruption layers — never direct object references.

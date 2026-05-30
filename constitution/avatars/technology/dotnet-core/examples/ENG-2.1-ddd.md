---
laws: [ENG-2.1]
avatar: [dotnet-core]
title: Domain-Driven Design — C#/.NET
---

# ENG-2.1: Domain-Driven Design — dotnet-core

Organise code around bounded contexts. Booking, Loyalty, and Operations are separate bounded contexts with explicit interfaces.

## Bounded Context Example (C#/.NET)

Domain entities must not reference infrastructure concerns. Aggregates enforce invariants.

**Rule**: Cross-context communication via domain events or anti-corruption layers — never direct object references.

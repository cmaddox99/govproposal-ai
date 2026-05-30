---
laws: [ENG-2.2]
avatar: [java-spring]
title: Layered Architecture — java-spring
---

# ENG-2.2: Layered Architecture — java-spring

Organise code into domain, application, and infrastructure layers with inward-only dependencies.

## Layer Responsibilities

- **Domain**: Business entities, aggregates, value objects — zero framework dependencies
- **Application**: Use cases, orchestration — depends only on domain interfaces
- **Infrastructure**: HTTP clients, DB repos, event publishers — implements domain interfaces

**Rule**: Domain layer must compile and test without any Spring/NUnit/framework annotations.

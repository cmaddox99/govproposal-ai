---
laws: [ENG-4.1]
avatar: [java-spring]
title: Atomic TDD — java-spring
---

# ENG-4.1: Atomic TDD — java-spring

Every production behaviour must have a corresponding unit test written before the implementation.
Tests must run without database, network, or file-system dependencies.

## Pattern

Write the test first (RED), make it pass with minimal code (GREEN), then refactor (REFACTOR).
Each test covers exactly one behaviour. Use dependency injection and mocks for external systems.

**Rule**: SonarQube gate enforces ≥ 90% line coverage and mutation score ≥ 70%.

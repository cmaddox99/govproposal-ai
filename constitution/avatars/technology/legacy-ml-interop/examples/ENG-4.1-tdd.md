---
laws: [ENG-4.1]
avatar: [legacy-ml-interop]
title: Atomic TDD — legacy-ml-interop
---

# ENG-4.1: Atomic TDD

Every pipeline stage and model transformation must have an atomic unit test.
Use mock data fixtures — no live ML services, no S3, no GPU in unit tests.

Each test validates one transformation. Mock all external systems with `unittest.mock`.

**Rule**: SonarQube gate enforces >= 90% coverage; mutation score >= 70%.

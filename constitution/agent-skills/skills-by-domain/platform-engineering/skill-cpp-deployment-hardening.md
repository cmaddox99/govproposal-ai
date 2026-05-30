---
skill:
  id: skill-cpp-deployment-hardening
  name: "C++ Deployment & Operational Hardening"
  category: platform-engineering
  version: "1.0.0"
  avatar: cpp

laws:
  implements:
    - id: ENG-5.2
      title: Build & Deploy Law
    - id: ENG-6.1
      title: Security by Design Law (NON-NEGOTIABLE)
  references:
    - id: ENG-5.1
      title: Infrastructure as Code Law
    - id: ENG-5.3
      title: Environment Parity Law

triggers:
  phrases:
    - "C++ deployment"
    - "C++ linking policy"
    - "C++ binary hardening"
    - "C++ container image"
    - "C++ feature flags"
    - "C++ rollback"

followed_by:
  - skill-cpp-portable-build-governance
  - skill-27-constitution-compliance
---

# Skill: C++ Deployment & Operational Hardening

## Purpose

Govern how C++ binaries are built, hardened, containerized, and deployed. Per [ENG-5.2](laws/engineering/eng-5-devops.md), build and deployment must be reproducible; per [ENG-6.1](laws/engineering/eng-6-security.md), binaries must be hardened against exploitation.

## Procedure

1. **Define linking policy** — prefer static linking for self-contained microservices (single binary, no runtime deps); use dynamic linking only for shared libraries consumed by multiple services
2. **Mandate compilation hardening flags** — release builds must include `-fstack-protector-strong`, `-fPIE`, `-pie`, `-Wl,-z,relro,-z,now` (full RELRO), and `-D_FORTIFY_SOURCE=2` for ASLR, stack canaries, and buffer overflow protection
3. **Strip symbols for release** — use `-s` or `strip --strip-all` on release binaries; archive split debug info (`.debug` files) for crash symbolization
4. **Govern container images** — use multi-stage Dockerfiles with a builder stage (full toolchain) and a minimal runtime stage (distroless or Alpine); final image must not contain compilers or build tools
5. **Implement feature flags** — use compile-time `#ifdef` for permanent platform variants; use a runtime flag service (LaunchDarkly, AA internal) for experiments with dynamic toggle
6. **Define rollback procedures** — maintain N-1 binary artifacts in the registry; rollback must complete within the SLA window without data migration

## Governance Gate

Per [ENG-6.1](laws/engineering/eng-6-security.md), a release binary missing any hardening flag is a **blocking violation**. Per [ENG-5.2](laws/engineering/eng-5-devops.md), a container image containing build tools in the runtime stage fails the deployment gate.

## Blue-Green Deployment Pattern

- Deploy new version to the idle environment; run smoke tests against it
- Switch traffic only after health checks pass on the new environment
- Keep the previous environment live for instant rollback during the bake period

---
skill:
  id: skill-cpp-dependency-governance
  name: "C++ Dependency & License Governance"
  category: platform-engineering
  version: "1.0.0"
  avatar: cpp

laws:
  implements:
    - id: ENG-6.6
      title: Dependency Management Law
    - id: ENG-6.1
      title: Security by Design Law (NON-NEGOTIABLE)
  references:
    - id: ENG-5.2
      title: Build & Deploy Law

triggers:
  phrases:
    - "C++ dependency management"
    - "C++ license compliance"
    - "C++ third party"
    - "C++ Boost policy"
    - "C++ vendoring"
    - "C++ SBOM"

followed_by:
  - skill-cpp-portable-build-governance
  - skill-27-constitution-compliance
---

# Skill: C++ Dependency & License Governance

## Purpose

Govern third-party C++ dependencies for license compliance, security, and supply-chain integrity. Per [ENG-6.6](laws/engineering/eng-6-security.md), dependencies must be managed; per [ENG-6.1](laws/engineering/eng-6-security.md), untrusted code is a security risk.

## Procedure

1. **Scan licenses in CI** — run scancode-toolkit or FOSSA on every PR that adds or updates a dependency; fail the build on unapproved licenses
2. **Maintain an approved license allowlist** — permitted licenses: MIT, BSD-2-Clause, BSD-3-Clause, Apache-2.0, `BSL-1.0`, Zlib. All others require legal review
3. **Review GPL/LGPL carefully** — static linking against GPL/LGPL code creates a distribution obligation; prefer dynamic linking or find an alternative. LGPL with dynamic linking is conditionally approved
4. **Apply Boost module policy** — for C++20 and later, prefer `std::` equivalents (`optional`, `variant`, `filesystem`, `any`). Approved Boost modules: Asio, Beast, Serialization. All other Boost usage requires justification
5. **Define header-only vs compiled policy** — compiled libraries are preferred when a dependency is included in more than 3 translation units to reduce compile times and binary bloat
6. **Govern vendoring** — vendor only when AA-specific patches are required; place vendored code in `third_party/<lib>-<version>/` with the upstream LICENSE file. Prefer Conan/vcpkg for unpatched dependencies
7. **Generate SBOM for deployed binaries** — produce a CycloneDX or SPDX SBOM at build time; attach it to the release artifact and store in the artifact registry

## Governance Gate

Per [ENG-6.6](laws/engineering/eng-6-security.md), a dependency without a license scan result is a **blocking violation**.

## Transitive Dependency Audit

- Run `conan info --graph` or `vcpkg x-ci-verify-versions` to enumerate the full transitive closure
- Verify every transitive dependency appears in the license scan output
- Flag any transitive dependency pulling in a restrictive license not on the allowlist

---
law_id: ENG-10.1
avatar: ios-swift
---

# ENG-10.1: Constitution Governance — iOS Projects

> **Law:** Every AI-governed project must include a `hangar-ai-specs/` directory. The avatar manifest is the authoritative reference for which laws, patterns, and skills apply to the codebase. Agents must read the manifest before proposing changes.

---

## Required Project Structure

```
BookingApp/               ← Xcode project root
  hangar-ai-specs/
    manifest-ref.yaml     ← points to the governing avatar manifest
    changes/              ← per-sprint enrichment changelogs
    overrides/            ← justified deviations (require human sign-off)
  BookingApp.xcodeproj
  Sources/
  Tests/
  fastlane/
```

## `manifest-ref.yaml`

```yaml
# hangar-ai-specs/manifest-ref.yaml
avatar: ios-swift
constitution: hangar-ai-constitution
governing_laws:
  - ENG-4.1   # Atomic TDD — non-negotiable
  - ENG-10.1  # Constitution Governance — non-negotiable
  - ENG-11.1  # Spec-Driven Development — non-negotiable
  - ENG-3.1   # Complexity Limits
  - ENG-3.2   # Immutability
  - ENG-6.1   # Security by Design
  - ENG-6.4   # Data Protection
last_validated: 2025-07-17
validator: hangar-ai-constitution avatar-workflow Phase 5 (RAG Validate)
```

## What Agents Do with This

Before proposing any code change in an iOS repo:
1. Check for `hangar-ai-specs/manifest-ref.yaml`
2. Read the governing avatar manifest (ios-swift)
3. Confirm the proposed change is compliant with all listed laws
4. If a deviation is required, log it in `hangar-ai-specs/overrides/` with justification before proceeding

## What Agents Must NOT Do

- Do not bypass the manifest lookup by assuming defaults
- Do not add a new library or architectural pattern that conflicts with the manifest's technology stack
- Do not mark a change as compliant without having read the applicable law file

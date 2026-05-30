---
title: "Gate Management — Avatar Handoff for Discovery Stage A"
spec_id: "test-avatar-run-gate-mgmt"
type: avatar
workflow: "avatar-workflow"
phase: "phase-6-commit"
status: "READY"
author: "Amaya (Technical Coach)"
created: "2026-04-18"
scope: "Avatar workflow Phase 6 output — authoritative input for Discovery Stage A"
triggered_by: "Avatar workflow Phase 6 commit — java-spring (Enrich, gate-management)"
affects: "Discovery Stage A frontmatter — avatars[], avatar_path"
laws_applied:
  - ENG-13.1
  - ENG-11.1
exit_checklist:
  - item: "Technology avatar (java-spring) RAG-validated and committed"
    status: "pass"
  - item: "Product avatar RAG-validated and committed (if applicable)"
    status: "na"
  - item: "avatar_path resolves to an existing directory"
    status: "pass"
  - item: "rag_validation_date populated — handoff is not stale"
    status: "pass"
  - item: "ready_for_discovery: true confirmed by human"
    status: "pend"
  - item: "Rendered HTML reviewed in browser (ENG-13.1)"
    status: "pend"
stakeholder:
  name: "Adeel Ali"
  role: "Architect & Co-founder"
  affirm: false
  note: "Set affirm: true and ready_for_discovery: true after reviewing RAG validation HTML and this handoff HTML"
audit_log:
  - date: "2026-04-18"
    actor: "Amaya (Technical Coach)"
    action: "Discovery handoff produced — avatar RAG validation passed 5/5"
    outcome: "READY"
  - date: "2026-04-18"
    actor: "Amaya (Technical Coach)"
    action: "Artifact rendered to HTML for human review"
    outcome: "RENDERED"
avatars:
  - "avatar-technology-java-spring"
spec_artifacts:
  - path: "avatars/technology/java-spring/manifest.yaml"
    type: "manifest"
    status: "DONE"
  - path: "hangar-ai-specs/changes/test-avatar-run-gate-mgmt/rag-validation-java-spring.md"
    type: "validation"
    status: "DONE"
template_version: "1.0.0"
template_path: "docs/templates/avatars/discovery-handoff-template.md"
avatar_path: "avatars/technology/java-spring/"
---

# Gate Management — Avatar Handoff for Discovery Stage A

This document is the **authoritative source** for the `avatars[]` and `avatar_path` fields
in Discovery Stage A frontmatter for the Gate Management codebase. Copy from here — do not fill manually from `index.yaml`.

---

## Handoff Summary

| Field | Value |
|-------|-------|
| **Technology avatar** | `avatar-technology-java-spring` |
| **Product avatar** | N/A (technology enrichment only) |
| **Avatar path** | `avatars/technology/java-spring/` |
| **RAG validated** | Yes |
| **RAG validation date** | `2026-04-18` |
| **Ready for discovery** | ⏳ Awaiting human confirmation |

---

## Copy into Discovery Stage A Frontmatter

```yaml
avatars:
  - "avatar-technology-java-spring"
avatar_path: "avatars/technology/java-spring/"
```

---

## RAG Validation Reference

| Avatar | Recall | Max tokens | Precision | Report |
|--------|--------|-----------|-----------|--------|
| avatar-technology-java-spring | 5/5 | 1,840 | 100% | `hangar-ai-specs/changes/test-avatar-run-gate-mgmt/rag-validation-java-spring.html` |

---

## Constraints

- This handoff is valid until the avatar's `last_validated` date is > 90 days old.
  After 90 days, re-run Phase 5 (RAG Validate) before starting a new discovery.
- If `ready_for_discovery: false`, **do not start Discovery Stage A** — resolve the
  blocking RAG failures in the avatar workflow first.

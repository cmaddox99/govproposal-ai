---
title: "{Domain} — Avatar Handoff for Discovery Stage A"
spec_id: "{spec-id}"
type: avatar
workflow: "avatar-workflow"
phase: "phase-6-commit"
author: "{Agent or Human}"
created: "{YYYY-MM-DD}"
scope: "Avatar workflow Phase 6 output — authoritative input for Discovery Stage A"
triggered_by: "Avatar workflow Phase 6 commit — {avatar-id}"
affects: "Discovery Stage A frontmatter — avatars[], avatar_path"
laws_applied:
  - ENG-13.1
  - ENG-11.1
exit_checklist:
  - item: "Technology avatar RAG-validated and committed"
    status: "pend"
  - item: "Product avatar RAG-validated and committed (if applicable)"
    status: "pend"
  - item: "avatar_path resolves to an existing directory"
    status: "pend"
  - item: "rag_validation_date populated — handoff is not stale"
    status: "pend"
  - item: "ready_for_discovery: true confirmed by human"
    status: "pend"
  - item: "Rendered HTML reviewed in browser (ENG-13.1)"
    status: "pend"
stakeholder:
  name: "{Reviewer Name}"
  role: "{Role}"
  affirm: false
  note: "Confirm avatar is RAG-validated and ready before starting discovery"
audit_log:
  - date: "{YYYY-MM-DD}"
    actor: "{Agent or Human}"
    action: "Discovery handoff produced — avatar workflow Phase 6 complete"
    outcome: "DRAFTED"
avatars:
  - "{technology-avatar-id}"
  - "{product-avatar-id}"
spec_artifacts:
  - path: "avatars/{type}/{domain}/manifest.yaml"
    type: "manifest"
    status: "DONE"
  - path: "hangar-ai-specs/changes/{spec-id}/rag-validation-{avatar-id}.md"
    type: "validation"
    status: "DONE"
template_version: "1.0.0"
template_path: "docs/templates/avatars/discovery-handoff-template.md"
avatar_path: "avatars/{type}/{domain}/"
---

# {Domain} — Avatar Handoff for Discovery Stage A

This document is the **authoritative source** for the `avatars[]` and `avatar_path` fields
in Discovery Stage A frontmatter. Copy from here — do not fill manually from `index.yaml`.

---

## Handoff Summary

| Field | Value |
|-------|-------|
| **Technology avatar** | `{technology-avatar-id}` |
| **Product avatar** | `{product-avatar-id}` (or N/A) |
| **Avatar path** | `avatars/{type}/{domain}/` |
| **RAG validated** | Yes |
| **RAG validation date** | `{YYYY-MM-DD}` |
| **Ready for discovery** | ✅ Yes |

---

## Copy into Discovery Stage A Frontmatter

```yaml
avatars:
  - "{technology-avatar-id}"
  - "{product-avatar-id}"
avatar_path: "avatars/{type}/{domain}/"
```

---

## RAG Validation Reference

| Avatar | Recall | Max tokens | Precision | Report |
|--------|--------|-----------|-----------|--------|
| {technology-avatar-id} | {n}/5 | {n} | {pct}% | `hangar-ai-specs/changes/{spec-id}/rag-validation-{avatar-id}.html` |
| {product-avatar-id} | {n}/5 | {n} | {pct}% | `hangar-ai-specs/changes/{spec-id}/rag-validation-{avatar-id}.html` |

---

## Constraints

- This handoff is valid until the avatar's `last_validated` date is > 90 days ago.
  After 90 days, re-run Phase 5 (RAG Validate) before starting a new discovery.
- If `ready_for_discovery: false`, **do not start Discovery Stage A** — resolve the
  blocking RAG failures in the avatar workflow first.

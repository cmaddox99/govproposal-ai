---
law_id: ENG-13.1
avatar: android-kotlin
non_negotiable: true
---

# ENG-13.1: Artifact Rendering Standard — Android (Kotlin)

> **Law:** All human-facing governance artifacts SHALL be rendered as self-contained HTML using `aa-artifact-render` before ensemble deliberation, gate review, or stakeholder presentation.

---

## Android Context

For the `androidapps` monorepo, ENG-13.1 applies to: feature PROPOSAL.md files in `hangar-ai-specs/` (once created per ENG-11.1 gap), phase gate evidence artifacts, and any ADR produced during architecture decisions (e.g., Dagger 2 → Hilt migration plan, RxJava → Coroutines migration).

---

## COMPLIANT: Render Gate Before Feature PR

```bash
# When hangar-ai-specs/changes/{spec-id}/PROPOSAL.md is ready for review:
export PATH="$PATH:/Users/{dev}/Library/Python/3.9/bin"

# Render proposal for ensemble review
aa-artifact-render hangar-ai-specs/changes/android-network-abc/PROPOSAL.md \
  --output hangar-ai-specs/changes/android-network-abc/PROPOSAL.html

# Open in browser — verify law citation tooltips and AA design system
open hangar-ai-specs/changes/android-network-abc/PROPOSAL.html
```

---

## COMPLIANT: Artifact Frontmatter (Required Fields)

```markdown
---
artifact_type: proposal
law_citations: [ENG-4.1, ENG-2.2, ENG-6.1]
spec_id: android-network-abc
date: "2026-04-30"
render_gate:
  rendered: true
  date: "2026-04-30"
  rendered_by: aa-artifact-render v1.2.0
---
```

`render_gate.rendered: true` is the evidence field confirming compliance. An artifact without it is non-compliant per ENG-13.1.

---

## COMPLIANT: CI Gate — Render Check in PR

```yaml
# .github/workflows/hangar-spec-check.yml
- name: Render gate check (ENG-13.1)
  run: |
    PROPOSAL="hangar-ai-specs/changes/${{ env.SPEC_ID }}/PROPOSAL.md"
    if ! grep -q "rendered: true" "$PROPOSAL"; then
      echo "ENG-13.1 VIOLATION: render_gate.rendered not true in PROPOSAL.md"
      exit 1
    fi
    aa-artifact-render "$PROPOSAL" --validate-only
```

---

## VIOLATION: Unrendered Proposal Submitted for Review

```markdown
<!-- ❌ VIOLATION: PROPOSAL.md for god-class decomposition has no render_gate -->
---
artifact_type: proposal
spec_id: android-checkinmanager-decomp
---

# CheckInManagerV2 Decomposition

(No render_gate block — non-compliant)
(No HTML artifact — reviewers see raw Markdown)
```

**Why ENG-13.1 non-negotiable:** Unrendered PROPOSAL.md lacks inline law tooltips. Engineers reviewing god-class decomposition plans cannot see which ENG-3.1 or ENG-2.2 provisions apply at the point of citation without navigating elsewhere.

---

## Phase Gate for Android Module Changes

| Phase | ENG-13.1 Requirement |
|---|---|
| Spec (feature) | Render PROPOSAL.md → PROPOSAL.html before team review |
| Phase 4 (Build) | Render phase gate evidence → {phase}-evidence.html |
| Phase 6 (Commit) | Include rendered HTML in commit; link in PR description |
| God-class decomposition | ADR rendered before architecture review session |

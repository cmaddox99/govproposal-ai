---
law_id: ENG-13.1
avatar: ios-swift
non_negotiable: true
---

# ENG-13.1: Artifact Rendering Standard — iOS (Swift)

> **Law:** All human-facing governance artifacts SHALL be rendered as self-contained HTML using `aa-artifact-render` before ensemble deliberation, gate review, or stakeholder presentation.

---

## iOS Context

For iOS framework repos, ENG-13.1 applies to: feature PROPOSAL.md files in `hangar-ai-specs/`, phase gate evidence, and any ADR produced during architecture decisions affecting a module.

---

## COMPLIANT: Render Gate Before Feature PR

```bash
# When a hangar-ai-specs/changes/{spec-id}/PROPOSAL.md is ready for review:
export PATH="$PATH:/Users/{dev}/Library/Python/3.9/bin"

# Render proposal for ensemble review
aa-artifact-render hangar-ai-specs/changes/ios-checkin-abc/PROPOSAL.md \
  --output hangar-ai-specs/changes/ios-checkin-abc/PROPOSAL.html

# Verify: open in browser — check law tooltips, AA design system applied
open hangar-ai-specs/changes/ios-checkin-abc/PROPOSAL.html
```

---

## COMPLIANT: Artifact Frontmatter (Required Fields)

```markdown
---
artifact_type: proposal          # proposal | evidence | adr | rag-validation
law_citations: [ENG-4.1, ENG-6.4]
spec_id: ios-checkin-abc
date: "2026-04-30"
render_gate:
  rendered: true
  date: "2026-04-30"
  rendered_by: aa-artifact-render v1.2.0
---
```

The `render_gate` field confirms the artifact was rendered before review. An artifact without `render_gate.rendered: true` is non-compliant.

---

## COMPLIANT: CI Gate — Render Check in PR

```yaml
# .github/workflows/hangar-spec-check.yml
- name: Render gate check (ENG-13.1)
  run: |
    PROPOSAL="hangar-ai-specs/changes/${{ env.SPEC_ID }}/PROPOSAL.md"
    if ! grep -q "rendered: true" "$PROPOSAL"; then
      echo "ENG-13.1 VIOLATION: PROPOSAL.md render_gate.rendered is not true"
      exit 1
    fi
    aa-artifact-render "$PROPOSAL" --validate-only
```

---

## VIOLATION: Unrendered Proposal Submitted for Review

```markdown
<!-- ❌ VIOLATION: PROPOSAL.md submitted to PR without render_gate block -->
---
artifact_type: proposal
spec_id: ios-checkin-abc
---

# Feature Proposal: Check-In Flow Refactor

(No render_gate: block)
(No HTML artifact produced)
```

**Why ENG-13.1 non-negotiable:** Unrendered Markdown proposals lack law citation tooltips and AA design system styling. Reviewers cannot see law compliance context inline. Governance quality degrades when reviewers must navigate separately to understand cited laws.

---

## Phase Gate for iOS Module Changes

| Phase | ENG-13.1 Requirement |
|---|---|
| Phase 1 (Spec) | Render PROPOSAL.md → PROPOSAL.html before team review |
| Phase 4 (Build) | Render phase gate evidence → {phase}-evidence.html |
| Phase 6 (Commit) | Include rendered HTML in commit; link in PR description |
| Framework release | RAG validation report rendered before index.yaml update |

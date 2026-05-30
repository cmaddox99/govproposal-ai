# Hangar SDD Changes

This directory contains Hangar SDD (Spec-Driven Development) proposals for changes to the hangar-ai-constitution. Governed by ENG-11.1 (NON-NEGOTIABLE).

## Creating a Proposal

```bash
mkdir -p hangar-ai-specs/changes/<verb-noun-id>
```

1. Create `changes/<verb-noun-id>/PROPOSAL.md` — problem, solution, deliverables, success criteria, law citations (required per ENG-11.2)
2. Create `changes/<verb-noun-id>/tasks.md` — checkbox list of all implementation tasks
3. Implement following the PROPOSE → IMPLEMENT → ARCHIVE lifecycle
4. Archive on completion: `mv changes/<id> archive/$(date +%Y-%m-%d)-<id>`

## Active Proposals

| Proposal | Status | PR |
|----------|--------|-----|
| [avatar-id-schema-clarification](changes/avatar-id-schema-clarification/) | 🟡 ACTIVE | #32 |
| [cpp-tier-compliance-rating](changes/cpp-tier-compliance-rating/) | 🔵 IN PROGRESS | PR #19 (stacked on #14) |
| [cpp-extended-reference-docs](changes/cpp-extended-reference-docs/) | ✅ COMPLETE | PR #18 (stacked on #14) |
| [product-avatar-bus-enrichment](changes/product-avatar-bus-enrichment/) | 🔵 IN PROGRESS — 13/14 files unblocked | — |
| [product-avatar-accessibility-governance](changes/product-avatar-accessibility-governance/) | 🔴 BLOCKED — PRD-3.4 domain boundary ruling pending | — |

## Reference

See `agent-skills/skills-by-domain/discovery-research/spec-governance.md` (`skill-spec-governance`) for full lifecycle guidance.

---
skill:
  id: skill-30-taxonomy-governed-avatar-enrichment
  name: Taxonomy-Governed Avatar Enrichment
  category: discovery
  version: "1.0.0"

laws:
  implements:
    - id: PRD-3.1
      title: Journey Mapping Law
    - id: PRD-5.1
      title: MVP Law
    - id: BUS-1.1
      title: Priority Hierarchy Law
    - id: BUS-7.1
      title: Audit Trail Law
    - id: ENG-10.1
      title: Constitution Compliance
  references:
    - id: ENG-1.3
      title: Maintainability Law
    - id: ENG-5.1
      title: Infrastructure as Code Law

triggers:
  phrases:
    - "enrich product avatar"
    - "product taxonomy"
    - "taxonomy governance"
    - "brownfield enrichment"
    - "reject wrong taxonomy"

followed_by:
  - skill-spec-governance
  - skill-04-business-domain-modeling
  - skill-05-business-rules
---

# Skill: Taxonomy-Governed Avatar Enrichment

## Purpose

Enrich avatars while preserving a healthy product taxonomy. This skill prevents anti-patterns such as modeling organizational groups (for example, ORAA or Data Engineering) as product types.

## When To Invoke

Use this skill when teams need to:

1. Add or update product avatars.
2. Map brownfield team-owned services into constitutional taxonomy.
3. Reject incorrect product taxons before enrichment proceeds.
4. Establish repeatable governance so future enrichments are consistent.

## Method

1. Classify incoming label into one of three buckets:
   - Product capability
   - Technology/runtime capability
   - Team/org ownership label
2. Run taxonomy gates before creating/updating any product avatar:
   - Domain test (durable business capability)
   - User journey test (distinct users and flows)
   - Boundary test (no overlap with existing avatars)
   - Stability test (independent of org chart changes)
   - Retrieval test (improves RAG precision)
3. Reject team/org labels as product taxons; remap them to canonical domains.
4. Create or update artifacts in the correct layer:
   - Product domain in product-type avatar
   - Runtime patterns in technology avatar
   - Repeatable procedures in skills
5. Record decisions and rejected aliases for auditability.

## Required Outputs

1. Taxonomy decision table (input label, decision, rationale).
2. Canonical mapping table (anti-pattern alias -> approved taxon).
3. Enrichment plan split by avatar vs skill vs guide updates.
4. Brownfield safety gates (no-rewrite default and migration approval criteria).

## Guardrails

1. Never create product-type avatars named after teams, orgs, or platforms.
2. Never proceed with enrichment if taxonomy gates fail.
3. Never allow language migration by default in brownfield adoption.
4. Require explicit parity evidence before approving any stack rewrite.

## Retrieval Notes

For enrichment prompts, route in this order:

1. `agent-skills/skills-by-domain/discovery-research/index.yaml`
2. `agent-skills/skills-by-domain/discovery-research/30-taxonomy-governed-avatar-enrichment.md`
3. `docs/guides/avatars/product-taxonomy-governance.md`
4. `docs/guides/adoption/taxonomy-aligned-avatar-enrichment-workflow.md`

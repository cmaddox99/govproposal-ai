# Product Taxonomy Governance Guide

This guide defines how product-type avatars are approved, rejected, and maintained to keep taxonomy healthy and retrieval quality high.

## Objective

Keep product taxonomy capability-based, stable, and composable across teams.

## Core Principle

Product-type avatars represent durable business capabilities, not organizational ownership.

Valid:

- Network Planning Optimization
- Passenger Booking
- Customer Service

Invalid:

- ORAA
- Data Engineering Team
- Platform Group Alpha

## Taxonomy Validation Gates

A proposed product taxon must pass all gates.

1. Domain gate: can this be described as a business capability independent of team names?
2. User journey gate: does it have distinct end-user or operator journeys?
3. Boundary gate: does it avoid overlap with an existing product avatar?
4. Stability gate: would it remain valid if org structure changed?
5. Retrieval gate: does it improve RAG routing precision versus adding ambiguity?

## Automatic Rejection Rules

Reject proposal if any condition is true:

1. Taxon name is a team, org unit, or cost-center label.
2. Scope is purely technology/runtime concern without product journeys.
3. Scope duplicates existing product avatar with renamed wording.

## Canonical Remapping Rules

When anti-pattern labels are provided, remap:

1. Team/org label -> business capability product avatar
2. Runtime/platform label -> technology avatar
3. Reusable process requirement -> skill

Example:

- Input label: ORAA
- Product mapping: Network Planning Optimization
- Technology mapping: Legacy ML Interop, Python Streamlit
- Skill mapping: Taxonomy-Governed Avatar Enrichment, Spec Governance

## Required Artifacts for Approved Product Taxons

1. `manifest.yaml`
2. `guidance.md`
3. `examples/` with PRD law applications
4. At least one `use-cases/.../README.md`
5. Registry and RAG index updates

## Governance Workflow

1. Intake taxonomy request.
2. Run validation gates.
3. Approve or reject with rationale.
4. If rejected, provide canonical remap decision.
5. Execute enrichment in correct layer.
6. Record decision in Hangar SDD proposal and progress artifacts.

## Compliance Checklist

- [ ] Taxon is capability-based and not org-based
- [ ] Distinct user journeys exist
- [ ] No overlap with existing product avatar
- [ ] Technology concerns moved to technology avatar
- [ ] Skills remain domain-general and reusable
- [ ] Decision rationale recorded for audit

## RAG Routing Hook

For avatar enrichment requests, retrieval SHOULD include:

1. Discovery-research index
2. Skill `skill-30-taxonomy-governed-avatar-enrichment`
3. This guide
4. Taxonomy-aligned enrichment workflow guide

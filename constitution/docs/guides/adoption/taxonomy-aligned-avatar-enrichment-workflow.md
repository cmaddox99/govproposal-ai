# Taxonomy-Aligned Avatar Enrichment Workflow

This workflow operationalizes taxonomy governance for all future avatar enrichments.

## Workflow Intent

Ensure enrichment runs are consistent, auditable, and RAG-retrievable.

## Step 1: Intake and Classification

Capture inputs:

1. Requested label
2. Problem statement
3. Target repositories/services
4. Brownfield constraints

Classify request into:

- Product capability
- Technology/runtime capability
- Org/team label

## Step 2: Taxonomy Gate Review

Run product taxonomy gates from `product-taxonomy-governance.md`.

Outcome:

1. Approved product taxon
2. Rejected with canonical remap

## Step 3: Hangar SDD Change Initialization

Create Hangar SDD change under `hangar-ai-specs/changes/<change-id>/` with:

1. `PROPOSAL.md`
2. `PROGRESS.md`

Required proposal sections:

1. Taxonomy decision and rationale
2. Canonical mapping table
3. Brownfield non-rewrite safeguards
4. Deliverables split by product avatar, technology avatar, and guide/skill updates

## Step 4: Enrichment Execution

Apply updates in correct layer:

1. Product capability -> `avatars/product-type/...`
2. Runtime stack -> `avatars/technology/...`
3. Reusable process -> `agent-skills/skills-by-domain/...`
4. Governance and procedures -> `docs/guides/...`

## Step 5: Registry and RAG Wiring

Update routing artifacts:

1. `avatars/index.yaml`
2. `avatars/product-type/index.yaml`
3. `avatars/AVATAR-RAG-INDEX.yaml`
4. relevant skill domain `index.yaml`
5. `AGENTS.md` if retrieval protocol needs update

## Step 6: Brownfield Safety Validation

Before adoption recommendations are finalized:

1. Confirm no language rewrite is proposed by default.
2. If migration is requested, verify approval and parity evidence gates.
3. Document preserved behavior and test equivalence strategy.

## Step 7: Review and Sign-off

Minimum sign-offs:

1. Constitution steward (taxonomy compliance)
2. Domain/product representative (journey validity)
3. Engineering representative (brownfield safety)

## Exit Criteria

- Taxonomy decision recorded and auditable
- Required avatar artifacts created and indexed
- RAG routing points to governance skill and guides
- Brownfield recommendation defaults to preserve-stack behavior

## RAG Retrieval Contract

For enrichment prompts, retrieval SHOULD load:

1. `agent-skills/skills-by-domain/discovery-research/index.yaml`
2. `agent-skills/skills-by-domain/discovery-research/30-taxonomy-governed-avatar-enrichment.md`
3. `docs/guides/avatars/product-taxonomy-governance.md`
4. this workflow guide

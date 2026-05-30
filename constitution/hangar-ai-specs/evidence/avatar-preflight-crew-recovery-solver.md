# Avatar Pre-flight Evidence — crew-recovery-solver
timestamp: 2026-04-23T03:53:49Z
mode: Generate  # Mode 1
avatar_type: product
domain_slug: crew-recovery-solver
intent_classification: "Create new product-type avatar for Crew Recovery Solver (CWR) IROP domain"

deduplication_tier1:
  path_checked: avatars/product-type/crew-recovery-solver/
  exists: false
  result: PROCEED

deduplication_tier2:
  nearest_neighbor: schedule-change-self-serve
  overlap_score: 28%  # different domain: crew (labor/FAR117) vs passenger (rebooking)
  result: PROCEED — below 40% threshold; distinct regulatory domain (BUS-2.1 FAR 117)

law_boundary_acknowledgement:
  avatar_type: product
  permitted_primary: "PRD-*, BUS-*"
  conditionally_permitted: "ENG-6.x with inline justification"
  forbidden: "ENG-1.x–ENG-5.x, ENG-7.x–ENG-12.x"
  acknowledged: true

rag_query_patterns:
  Q1: "How do we discover crew recovery user needs?"
  Q2: "What is the crew recovery core journey?"
  Q3: "What are the success metrics for crew recovery?"
  Q4: "What are the non-negotiable rules for crew recovery?"
  Q5: "Walk me through a crew reassignment during IROP"

taxonomy_check:
  proposed_category: "Product (Service Recovery)"
  basis: "IROP crew recovery is a service recovery domain — restoring service after disruption"
  nearest_existing: schedule-change-self-serve (Product Service Recovery, passenger-facing)
  boundary: "CWR is crew-labor-facing with FAR 117 regulatory obligations; distinct from passenger self-serve rebooking"
  verdict: VALID — taxonomically distinct domain

verdict: PROCEED to Phase 1 → Mode 1 Generate

# Avatar Pre-flight Evidence — network-automation
timestamp: 2026-04-28T18:43:40Z
mode: Generate  # Mode 1
avatar_type: product
domain_slug: network-automation
intent_classification: "Create new product-type avatar for IT Network Automation (Nautobot, DNS, firewall, device management, API gateway)"

deduplication_tier1:
  path_checked: avatars/product-type/network-automation/
  exists: false
  result: PROCEED

deduplication_tier2:
  nearest_neighbor: network-planning-optimization
  overlap_score: "<10%"
  rationale: |
    "network-planning-optimization" governs airline route/capacity planning (flight networks,
    revenue management, operations research). "network-automation" governs IT network
    infrastructure automation (Nautobot, DNS, firewall rules, device configuration,
    network monitoring via Apigee). Completely distinct domains — "network" word overlap only.
    Laws in network-planning-optimization (PRD-1.1, PRD-2.1, PRD-4.1, ENG-4.1) do not
    reflect meaningful shared governance scope.
  result: PROCEED — below 40% threshold; entirely distinct domain

law_boundary_acknowledgement:
  avatar_type: product
  permitted_primary: "PRD-*, BUS-*"
  conditionally_permitted: "ENG-6.x with inline justification"
  forbidden: "ENG-1.x–ENG-5.x, ENG-7.x–ENG-12.x"
  acknowledged: true

rag_query_patterns:
  Q1: "How do we discover network automation user needs?"
  Q2: "What is the network automation core journey for an operator?"
  Q3: "What are the success metrics for network automation?"
  Q4: "What are the non-negotiable rules for network automation?"
  Q5: "Walk me through a network change automation workflow"

taxonomy_check:
  proposed_category: "Product (Internal Operations)"
  basis: |
    Network automation is an internal IT infrastructure toolchain serving network engineers,
    NOC operators, and platform teams — not customer-facing. Aligns with "Product (Internal
    Operations)" as it automates internal operational processes (network change management,
    device provisioning, DNS management, firewall rule lifecycle).
  nearest_existing: "internal-productivity (Product (Internal Operations))"
  boundary: |
    network-automation is IT infrastructure-focused (Nautobot, Apigee, network devices) with
    distinct personas (network engineers, NOC) and journeys (network change automation, device
    provisioning) not covered by the internal-productivity avatar (employee productivity tooling).
  verdict: VALID — maps to established taxonomy category "Product (Internal Operations)"

verdict: PROCEED to Phase 1 → Mode 1 Generate

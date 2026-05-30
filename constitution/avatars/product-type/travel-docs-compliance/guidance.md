# TravelDocs Readiness Guidance

## Scope

Use this avatar when working on services that determine passenger travel-document readiness before check-in or boarding. This avatar is intended for API-first products that combine regulatory constraints and operational decisions in near real time.

## Law Application

### PRD-1.1 Continuous Discovery

Discovery should prioritize friction in these decision points:

1. Passenger asks what documents are needed for itinerary.
2. Passenger receives not-ready status near departure.
3. Agent needs precise reason and next action.
4. Operations team needs route-level readiness visibility.

### PRD-2.1 Journey Mapping

Track both external and internal journeys:

1. Passenger journey: pre-trip question to ready-to-board.
2. Agent journey: exception diagnosis to remediation.
3. Compliance journey: rule update to policy validation.
4. Ops journey: readiness monitoring to intervention.

### PRD-3.1 Roadmap Planning

Prioritize in this order unless evidence suggests otherwise:

1. Correctness and compliance accuracy.
2. Explainability of decision output.
3. Latency and reliability for high-volume windows.
4. Automation of common remediation paths.

### PRD-4.1 MVP Validation

For each change, define:

1. Hypothesis: which readiness outcome improves.
2. Risk controls: false-ready and false-block guardrails.
3. Experimental cohort: route/client subset.
4. Exit criteria: measurable error reduction or faster recovery.

### PRD-5.1 Metrics (Experimental Baselines)

When production measurements are unavailable, start with explicit baselines:

| Metric | Baseline Type | Initial Baseline | 90-Day Target |
|---|---|---:|---:|
| Document decision latency p95 | Experimental | 2500 ms | 1800 ms |
| External dependency timeout rate | Experimental | 2.5% | 1.2% |
| Manual intervention rate per 1k requests | Experimental | 45 | 25 |
| Passenger-ready rate at D-1 | Experimental | 78% | 86% |
| False block rate | Experimental | 1.8% | 0.8% |
| Exception explainability score | Experimental | 3.1/5 | 4.2/5 |

Mark all values as hypotheses until replaced by measured telemetry.

## Engineering Expectations

1. Emit decision and reason codes for every readiness result.
2. Keep external call latency and error telemetry per provider.
3. Preserve immutable audit trails for compliance-sensitive decisions.
4. Add contract tests whenever request/response models change.
5. Define fallback behavior for each upstream dependency.

## Skill Pairings

Use these skills together for this domain:

1. `skill-04-business-domain-modeling` to map entities and rule ownership.
2. `skill-05-business-rules` for explicit rule catalogs and edge-case handling.
3. `skill-12-api-design` for stable, explainable response contracts.
4. `skill-13-observability` for readiness decision telemetry.

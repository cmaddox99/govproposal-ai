# Use Case: Pre-Departure Document Readiness

## Objective

Determine if each passenger is document-ready for travel and provide a reasoned, actionable response when not ready.

## Trigger

Passenger or check-in channel invokes readiness check at itinerary, segment, or passenger scope.

## Core Flow

1. Validate request shape and identity context.
2. Resolve itinerary segments and passenger attributes via Retrieve Reservation Service.
3. Query policy dependencies: `TravelDocsRequirement` (BFF orchestrator) calls Timatic4 via `TravelDocsStatusRequestBuilder`, Sherpa via `HealthDocsStatusRequestBuilder`, and VeriFly.
4. Evaluate business rules and aggregate status per segment: `DocsStatusEnum` (SUFFICIENT / INSUFFICIENT / NOT_APPLICABLE) and `TravelAuthorizationStatusEnum`.
5. Return readiness decision with reason codes and suggested actions via `TravelDocsStatusResponse` / `PassengerTravelDocsResponse`.
6. Persist telemetry and audit metadata (decision, rule version, timestamp).

## Exception Flow

1. Upstream timeout: return partial decision with clear degraded mode flag.
2. Missing passenger context: fail with explicit remediation instructions.
3. Conflicting provider outputs: prefer conservative rule and log review event.

## Success Metrics

1. p95 response latency under target.
2. Reduced manual intervention per 1k requests.
3. Lower false-block rate while maintaining compliance coverage.

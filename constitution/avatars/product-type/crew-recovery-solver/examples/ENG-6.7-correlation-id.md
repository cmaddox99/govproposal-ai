---
avatar: avatar-product-crew-recovery-solver
law: ENG-6.7
title: "Audit Trail Law (Engineering)"
---

# ENG-6.7 — Audit Trail Law (Engineering): Correlation ID in Crew Recovery

> **Justification for ENG-6.7 in a product-type avatar:** CWR has a direct BUS-7.1 regulatory audit obligation. Implementing that obligation requires a specific engineering pattern — correlation ID propagation from IROP event to every downstream audit record. This example defines the implementation requirement, not the law itself.

## What This Law Requires
Every log entry, audit record, and downstream service call in a crew recovery workflow must carry the originating IROP event's correlation ID, enabling full end-to-end audit trail reconstruction for regulatory review.

## Compliant Example

**Correlation ID Propagation in IROP Recovery Flow**

```python
# 1. IROP event published with correlation ID
@dataclass
class IROPEvent:
    correlation_id: str  # format: "cwr-event-{uuid4}"
    event_type: str      # "FLIGHT_CANCELLED" | "FLIGHT_DELAYED"
    flight_id: str
    affected_crew: list[str]

# 2. Propagated through all service calls
class CrewRecoveryOrchestrator:
    def handle_irop(self, event: IROPEvent) -> RecoveryResult:
        with LogContext(correlation_id=event.correlation_id):
            options = self.option_builder.build(
                event, correlation_id=event.correlation_id
            )
            selection = self.scheduler_interface.present(
                options, correlation_id=event.correlation_id
            )
            audit_record = CrewAssignmentAuditRecord(
                correlation_id=event.correlation_id,  # ← BUS-7.1 traceability
                ...
            )
            self.audit_store.append(audit_record)

# 3. Every log line carries correlation_id
# structlog / JSON logging pattern:
logger.info("far_117_eligibility_check",
    correlation_id=event.correlation_id,
    crew_id=crew_id,
    eligible=result.eligible,
    rest_hours=result.actual_rest_hours,
)
```

**Why this matters for regulatory audit:** When the FAA requests an audit trail for a specific IROP event, the correlation ID is the join key across all services — eligibility service, assignment service, notification service, and audit store. Without it, the audit trail cannot be reconstructed.

## Violation Example
```
❌ Correlation ID generated fresh in each microservice.
   → Audit trail cannot be joined; multiple records for same event have different IDs.
   → Fix: correlation_id originates at the IROP event; every downstream call receives it as a parameter.
```

## Edge Cases & Warnings
- The correlation ID must survive async handoffs — include in message headers (Kafka/SQS), not just in-process context
- Do not use request IDs (HTTP) as correlation IDs — they are per-request, not per-IROP-event

---
laws: [ENG-6.1, ENG-6.4, ENG-6.7]
avatar: [r-shiny]
title: Security Laws — R/Shiny
---

# Security Laws: ENG-6.1, ENG-6.4, ENG-6.7 — r-shiny

## ENG-6.1: Security by Design

Every data pipeline and service endpoint handling passenger PII must enforce authentication and authorisation before processing.

```
if (!is_authenticated(session)) { showModal(authModal()); return() }  # ENG-6.1
```

## ENG-6.4: Data Encryption

Encrypt PII at rest (AES-256/CMK) and in transit (TLS 1.3). Never log raw PAN, passport, or loyalty numbers.

## ENG-6.7: Audit Trail with Correlation ID

Every operation must emit a structured audit event with `correlation_id` traceable from API gateway to data sink.

```
session$userData$correlation_id <- generateCorrelationId()
log_audit(event='dashboard_access', user=session$user, cid=session$userData$correlation_id)
```

**Rule**: `X-Correlation-ID` must be propagated from the initiating HTTP request through all downstream calls and log entries.

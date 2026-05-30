---
laws: [ENG-6.1, ENG-6.4, ENG-6.7]
avatar: [langchain]
title: Security Laws — Python/LangChain
---

# Security Laws: ENG-6.1, ENG-6.4, ENG-6.7 — langchain

## ENG-6.1: Security by Design

Every data pipeline and service endpoint handling passenger PII must enforce authentication and authorisation before processing.

```
if any(pii_detector.detect(msg) for msg in messages): raise PiiViolation('PII in prompt — redact before LLM call')
```

## ENG-6.4: Data Encryption

Encrypt PII at rest (AES-256/CMK) and in transit (TLS 1.3). Never log raw PAN, passport, or loyalty numbers.

## ENG-6.7: Audit Trail with Correlation ID

Every operation must emit a structured audit event with `correlation_id` traceable from API gateway to data sink.

```
chain = LLMChain(llm=llm, prompt=prompt, callbacks=[AuditCallback(correlation_id=ctx.correlation_id)])
```

**Rule**: `X-Correlation-ID` must be propagated from the initiating HTTP request through all downstream calls and log entries.

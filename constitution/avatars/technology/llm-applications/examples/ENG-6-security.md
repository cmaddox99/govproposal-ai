---
laws: [ENG-6.1, ENG-6.4, ENG-6.7]
avatar: [llm-applications]
title: Security Laws — Python/LLM Apps
---

# Security Laws: ENG-6.1, ENG-6.4, ENG-6.7 — llm-applications

## ENG-6.1: Security by Design

Every data pipeline and service endpoint handling passenger PII must enforce authentication and authorisation before processing.

```
audit_log.record(correlation_id=ctx.id, model=model, tokens_in=usage.prompt_tokens, tokens_out=usage.completion_tokens)
```

## ENG-6.4: Data Encryption

Encrypt PII at rest (AES-256/CMK) and in transit (TLS 1.3). Never log raw PAN, passport, or loyalty numbers.

## ENG-6.7: Audit Trail with Correlation ID

Every operation must emit a structured audit event with `correlation_id` traceable from API gateway to data sink.

```
response = client.chat.completions.create(model='gpt-4o', messages=sanitized_messages, user=masked_user_id)
```

**Rule**: `X-Correlation-ID` must be propagated from the initiating HTTP request through all downstream calls and log entries.

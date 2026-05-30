---
laws: [ENG-6.1, ENG-6.4, ENG-6.7]
avatar: [streaming-ml]
title: Security Laws — Python/Kafka/Flink
---

# Security Laws: ENG-6.1, ENG-6.4, ENG-6.7 — streaming-ml

## ENG-6.1: Security by Design

Every data pipeline and service endpoint handling passenger PII must enforce authentication and authorisation before processing.

```
consumer_group.subscribe(['pax-events'], on_assign=lambda c,p: log.info('Assigned', partitions=p, correlation_id=ctx.id))
```

## ENG-6.4: Data Encryption

Encrypt PII at rest (AES-256/CMK) and in transit (TLS 1.3). Never log raw PAN, passport, or loyalty numbers.

## ENG-6.7: Audit Trail with Correlation ID

Every operation must emit a structured audit event with `correlation_id` traceable from API gateway to data sink.

```
producer.produce(topic, value=encrypt(payload, DATA_KEY), headers=[('x-correlation-id', correlation_id)])
```

**Rule**: `X-Correlation-ID` must be propagated from the initiating HTTP request through all downstream calls and log entries.

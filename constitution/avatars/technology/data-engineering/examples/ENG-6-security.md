---
laws: [ENG-6.1, ENG-6.4, ENG-6.7]
avatar: [data-engineering]
title: Security Laws — Python/Spark/dbt
---

# Security Laws: ENG-6.1, ENG-6.4, ENG-6.7 — data-engineering

## ENG-6.1: Security by Design

Every data pipeline and service endpoint handling passenger PII must enforce authentication and authorisation before processing.

```
spark = SparkSession.builder.config('spark.sql.legacy.allowNonEmptyLocationInCTAS','false').getOrCreate()
```

## ENG-6.4: Data Encryption

Encrypt PII at rest (AES-256/CMK) and in transit (TLS 1.3). Never log raw PAN, passport, or loyalty numbers.

## ENG-6.7: Audit Trail with Correlation ID

Every operation must emit a structured audit event with `correlation_id` traceable from API gateway to data sink.

```
df = df.withColumn('_ingested_at', current_timestamp()).withColumn('_correlation_id', lit(correlation_id))
```

**Rule**: `X-Correlation-ID` must be propagated from the initiating HTTP request through all downstream calls and log entries.

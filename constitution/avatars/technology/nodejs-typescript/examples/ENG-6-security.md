---
laws: [ENG-6.1, ENG-6.4, ENG-6.7]
avatar: [nodejs-typescript]
title: Security Laws — Node.js/TypeScript
---

# Security Laws: ENG-6.1, ENG-6.4, ENG-6.7 — nodejs-typescript

## ENG-6.1: Security by Design

Every data pipeline and service endpoint handling passenger PII must enforce authentication and authorisation before processing.

```
jwt.verify(token, SECRET, (err,payload)=>{ if(err) return res.status(401).json({error:'Unauthorized'}); req.user=payload; next(); });
```

## ENG-6.4: Data Encryption

Encrypt PII at rest (AES-256/CMK) and in transit (TLS 1.3). Never log raw PAN, passport, or loyalty numbers.

## ENG-6.7: Audit Trail with Correlation ID

Every operation must emit a structured audit event with `correlation_id` traceable from API gateway to data sink.

```
app.use((req,res,next)=>{ req.correlationId=req.headers['x-correlation-id']||uuidv4(); res.setHeader('X-Correlation-ID',req.correlationId); next(); });
```

**Rule**: `X-Correlation-ID` must be propagated from the initiating HTTP request through all downstream calls and log entries.

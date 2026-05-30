---
laws: [ENG-6.1, ENG-6.4, ENG-6.7]
avatar: [vector-databases]
title: Security Laws — Vector Databases
---

# Security Laws: ENG-6.1, ENG-6.4, ENG-6.7 — Vector Databases

## ENG-6.1: Security by Design

API keys from env vars. Namespace/index-level access controls per data sensitivity. Validate embedding input before encoding.

```python
import os
from pinecone import Pinecone

# ✅ API key from environment
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
# ❌ NEVER: pc = Pinecone(api_key="abc-123-def-456")

# Use separate namespaces per classification level
NAMESPACE_PUBLIC    = "public-faq"           # airport/flight FAQs
NAMESPACE_INTERNAL  = "internal-procedures"  # agent SOPs
NAMESPACE_SENSITIVE = "booking-policies"     # fare rules (internal only)
# ❌ NEVER mix sensitivity levels in a single namespace

index = pc.Index("aa-knowledge-base")
```

Weaviate/Qdrant — server-side collection-level auth:

```python
import weaviate

client = weaviate.Client(
    url=os.environ["WEAVIATE_URL"],
    auth_client_secret=weaviate.AuthBearerToken(os.environ["WEAVIATE_TOKEN"]),
    additional_headers={"X-OpenAI-Api-Key": os.environ["OPENAI_API_KEY"]},
)
```

Validate and length-limit text before embedding:

```python
import re

MAX_EMBED_CHARS = 8000   # ~2000 tokens — model limit buffer

def validate_embed_input(text: str) -> str:
    if len(text) > MAX_EMBED_CHARS:
        raise ValueError(f"Input exceeds max embed length ({len(text)} chars)")
    # Basic PII pre-check — block obvious raw PII from embedding
    if re.search(r'\b[A-Z]{6}\b', text):          # 6-char PNR pattern
        raise ValueError("Possible PNR detected in embed input — anonymize first")
    if re.search(r'[\w.+-]+@[\w-]+\.[a-z]{2,}', text, re.I):
        raise ValueError("Email address detected in embed input — anonymize first")
    return text
```

## ENG-6.4: Data Protection

Never embed raw PII. Use anonymized or pseudonymized text. Treat embeddings as sensitive data.

```python
import hashlib

def anonymize_for_embedding(text: str, salt: str) -> str:
    """Replace PII tokens with pseudonymous placeholders before embedding."""
    import re
    # Replace emails with pseudonym
    text = re.sub(r'[\w.+-]+@[\w-]+\.[a-z]{2,}',
        lambda m: "PASSENGER_" + hashlib.sha256((salt + m.group()).encode()).hexdigest()[:8],
        text, flags=re.I)
    # Replace PNR patterns
    text = re.sub(r'\b[A-Z]{6}\b',
        lambda m: "PNR_" + hashlib.sha256((salt + m.group()).encode()).hexdigest()[:6],
        text)
    return text

# Vector DB metadata: store IDs and content hashes — not reconstructable PII
def index_document(doc_id: str, content: str, namespace: str) -> None:
    safe_content = anonymize_for_embedding(content, os.environ["ANON_SALT"])
    embedding    = embed_model.encode(safe_content)
    content_hash = hashlib.sha256(content.encode()).hexdigest()[:16]

    index.upsert(
        vectors=[{
            "id":       doc_id,
            "values":   embedding.tolist(),
            "metadata": {
                "doc_id":       doc_id,
                "content_hash": content_hash,   # ✅ hash only — not raw content
                "namespace":    namespace,
                # ❌ NEVER: "passenger_name": name, "email": email
            },
        }],
        namespace=namespace,
    )
```

Vector embeddings leak information — treat as sensitive:

```
Note: Embedding vectors can be reversed via nearest-neighbour attacks to approximate
the original text. Store embeddings with the same access controls as the source data.
Encrypt at rest (S3 SSE-KMS or Weaviate encryption-at-rest config).
```

## ENG-6.7: Audit Trail

Log every query and index operation with correlation ID, query hash (not raw text), and result IDs.

```python
import hashlib, time, structlog

log = structlog.get_logger()

def query_index(query_text: str, namespace: str,
                top_k: int, correlation_id: str) -> list[dict]:
    safe_query = validate_embed_input(query_text)  # raises if PII detected
    query_hash = hashlib.sha256(safe_query.encode()).hexdigest()[:16]
    query_vec  = embed_model.encode(safe_query)

    start = time.monotonic()
    results = index.query(
        vector=query_vec.tolist(),
        top_k=top_k,
        namespace=namespace,
        include_metadata=True,
    )
    latency_ms = (time.monotonic() - start) * 1000

    result_ids = [m["id"] for m in results["matches"]]

    log.info("vector_query",
             correlation_id=correlation_id,
             query_hash=query_hash,           # ✅ hash — not raw query text
             namespace=namespace,
             top_k=top_k,
             result_ids=result_ids,           # ✅ IDs only — not content
             latency_ms=round(latency_ms, 2))
    # ❌ NEVER: log.info("query: %s results: %s", query_text, results)

    return results["matches"]

def log_index_operation(doc_id: str, version: str, correlation_id: str) -> None:
    log.info("vector_index_upsert",
             doc_id=doc_id,
             version=version,
             correlation_id=correlation_id,
             timestamp=time.time())
```

Append-only audit table for vector DB operations:

```sql
CREATE TABLE vector_audit (
    id             BIGSERIAL PRIMARY KEY,
    recorded_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    operation      TEXT NOT NULL,     -- QUERY or UPSERT
    namespace      TEXT NOT NULL,
    doc_id         TEXT,              -- for UPSERT
    query_hash     TEXT,              -- for QUERY
    result_ids     TEXT[],            -- for QUERY
    correlation_id TEXT NOT NULL
);
REVOKE UPDATE, DELETE ON vector_audit FROM app_role;
```

## Anti-Patterns

1. **Raw PII text as embedding input** — embedding `"Passenger John Doe PNR ABC123 email john@example.com"` stores passenger-identifiable vectors; anonymize before encoding.
2. **API keys in application code** — `api_key="pinecone-abc-123"` is committed to Git; use env vars and never log the key value.
3. **No namespace separation for different data classifications** — mixing public FAQ content with internal agent procedures or sensitive fare rules in a single namespace means a public-facing query can surface internal documents.
4. **Logging full query text when it may contain PII** — a support agent pasting a passenger complaint into a semantic search box sends PII to log aggregators; log the query hash only.
5. **No access logging on vector DB queries** — vector databases are often queried by LLM pipelines without audit trails; every query must be logged with correlation ID for traceability.

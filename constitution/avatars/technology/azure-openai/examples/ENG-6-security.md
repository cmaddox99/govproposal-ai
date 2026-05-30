---
laws: [ENG-6.1, ENG-6.4, ENG-6.7]
avatar: [azure-openai]
title: Security Laws — Azure OpenAI
---

# Security Laws: ENG-6.1, ENG-6.4, ENG-6.7 — Azure OpenAI

## ENG-6.1: Security by Design

API credentials must come from the environment or Managed Identity — never from source code.

```python
import os
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

# ✅ Production: Managed Identity (no key at all)
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)
client = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    azure_ad_token_provider=token_provider,
    api_version="2024-02-01",
)

# ✅ Local dev only: key from env var
# client = AzureOpenAI(api_key=os.environ["AZURE_OPENAI_KEY"], ...)

# ❌ NEVER
# client = AzureOpenAI(api_key="sk-abc123...")
```

Validate all inputs before dispatch; check content filter results:

```python
def call_llm(prompt: str, correlation_id: str) -> str:
    _validate_prompt(prompt)          # length, no injection patterns
    response = client.chat.completions.create(
        model=os.environ["AZURE_OPENAI_DEPLOYMENT"],   # deployment name, not model name
        messages=[{"role": "user", "content": prompt}],
        extra_headers={"X-Correlation-ID": correlation_id},
    )
    _check_content_filter(response)   # raise if filtered
    return response.choices[0].message.content

def _check_content_filter(response) -> None:
    for choice in response.choices:
        cf = getattr(choice, "content_filter_results", None)
        if cf and any(getattr(cf, cat, None) and getattr(cf, cat).filtered
                      for cat in ["hate", "self_harm", "sexual", "violence"]):
            raise ContentFilterError("Response blocked by content filter")
```

## ENG-6.4: Data Protection

PII — passenger names, PNR numbers, email addresses, seat assignments — must be redacted before the prompt reaches Azure OpenAI. Responses may echo back PII; redact before logging.

```python
import re

PII_PATTERNS = {
    "pnr":   re.compile(r'\b[A-Z]{6}\b'),
    "email": re.compile(r'[\w.+-]+@[\w-]+\.[a-z]{2,}', re.IGNORECASE),
}

def redact_pii(text: str) -> str:
    for label, pattern in PII_PATTERNS.items():
        text = pattern.sub(f"[{label.upper()}_REDACTED]", text)
    return text

async def generate_response(raw_prompt: str, correlation_id: str) -> str:
    safe_prompt = redact_pii(raw_prompt)
    response_text = call_llm(safe_prompt, correlation_id)
    safe_response = redact_pii(response_text)   # response may echo PII

    # ✅ Log safe metadata only
    logger.info("llm_call_complete",
                correlation_id=correlation_id,
                deployment=os.environ["AZURE_OPENAI_DEPLOYMENT"],
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens)
    # ❌ NEVER: logger.info("prompt: %s", raw_prompt)
    return safe_response
```

## ENG-6.7: Audit Trail

Every LLM call must produce an append-only audit record. Correlation ID (TID) ties the call to the originating booking/service request.

```python
from datetime import datetime, timezone

async def _write_audit(correlation_id: str, deployment: str,
                       prompt_tokens: int, completion_tokens: int,
                       latency_ms: float, filtered: bool) -> None:
    # INSERT only — no UPDATE/DELETE on llm_audit
    await db.execute(
        """INSERT INTO llm_audit
           (correlation_id, deployment, prompt_tokens, completion_tokens,
            latency_ms, content_filtered, recorded_at)
           VALUES (:cid, :dep, :pt, :ct, :lat, :filt, :ts)""",
        {"cid": correlation_id, "dep": deployment,
         "pt": prompt_tokens, "ct": completion_tokens,
         "lat": latency_ms, "filt": filtered,
         "ts": datetime.now(timezone.utc)},
    )
```

Use deployment name (not model alias) so audit records capture the exact model version:

```python
# ✅ Auditable — deployment name scopes the model version
deployment = os.environ["AZURE_OPENAI_DEPLOYMENT"]  # e.g. "gpt-4o-2024-05-13"

# ❌ Not auditable — model name can resolve to different versions over time
model = "gpt-4o"
```

## Anti-Patterns

1. **`print(api_key)` or logging the Authorization header** — any debug `print` of the env var or the SDK `api_key` attribute leaks credentials to stdout and log aggregators.
2. **PNR or customer email in the prompt** — Azure OpenAI logs prompts server-side (for abuse monitoring); sending `"Rebook passenger john.doe@aa.com PNR ABC123"` exports PII to Microsoft infrastructure.
3. **Not checking `content_filter_results`** — a filtered response still returns HTTP 200 with `finish_reason="content_filter"`; ignoring it causes silent data quality failures.
4. **Using model name instead of deployment name** — `model="gpt-4o"` bypasses AA's deployment-specific content filter configuration and breaks audit scoping.
5. **Hardcoding the OTLP / API endpoint** — endpoint URLs may encode tenant or region; treat them as secrets and load from env vars.

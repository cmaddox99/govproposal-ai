# Azure OpenAI Service Guidance

> **Purpose:** Stack-specific patterns for Python services integrating with Azure OpenAI Service. Covers endpoint construction, deployment routing, authentication, custom wrapper conventions, retry, and test patterns.

---

## Overview

Azure OpenAI Service has a distinct API surface from the public OpenAI API. Key differences that must be encoded in avatars and guidance:

| Concern | Public OpenAI SDK | Azure OpenAI |
|---------|------------------|--------------|
| Endpoint | `https://api.openai.com` | `https://{service}.openai.azure.com` |
| Routing | Model name (e.g., `gpt-4o`) | **Deployment name** (e.g., `gpt-4o-aa-prod`) |
| Auth header | `Authorization: Bearer {key}` | `api-key: {key}` |
| API versioning | Implicit (latest) | **Explicit** — `api-version=2024-12-01-preview` required |
| Content filtering | Optional | **Built-in** — `content_filter_results` in every response |

Using the wrong avatar (`azure-ml`) or the generic `llm-applications` avatar will produce guidance that misses all four of these differences.

---

## Endpoint and Auth Pattern

### Endpoint Construction

> **Per `ENG-6.5` (Input Validation):** Construct the endpoint in code from the service name — do not accept a full URL as an environment variable. This prevents misconfiguration from malformed URLs, trailing slashes, or wrong subdomains.

```python
# CORRECT — construct from service name
class Settings:
    def __init__(self):
        self.azure_openai_service = os.getenv("AZURE_OPENAI_SERVICE")
        self.azure_openai_endpoint = f"https://{self.azure_openai_service}.openai.azure.com"
        self.azure_openai_api_key = os.getenv("AZURE_OPENAI_KEY")
        self.azure_openai_model = os.getenv("AZURE_OPENAI_MODEL")   # deployment name
        self.azure_api_version = os.getenv("AZURE_OPENAI_VERSION")  # e.g. "2024-12-01-preview"

# INCORRECT — fragile, accepts malformed env var values
self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")   # no validation, allows trailing slash
```

### API Key Security

> **Per `ENG-6.1` (Security):** API key must never appear in logs, traces, or error messages. Always load from environment variables; never hardcode or commit.

```python
# CORRECT — key loaded from env, never logged
logging.info(f"TID {tid} - Calling Azure OpenAI deployment: {self.azure_openai_model}")
# INCORRECT — logs secret
logging.info(f"Using key: {self.azure_openai_api_key}")
```

---

## Deployment Routing vs. Model Name

Azure OpenAI routes requests by **deployment name**, not model name. A deployment named `gpt-4o-aa-prod` may run `gpt-4o` or `gpt-4.1` depending on what was deployed. The `AZURE_OPENAI_MODEL` env var must hold the **deployment name**, not the model family name.

```yaml
# Correct env var values
AZURE_OPENAI_MODEL=gpt-4o            # if deployment name = gpt-4o
AZURE_OPENAI_MODEL=gpt-4o-aa-east    # if deployment name = gpt-4o-aa-east
AZURE_OPENAI_VERSION=2024-12-01-preview

# Incorrect
AZURE_OPENAI_MODEL=GPT-4-Turbo       # this is a display name, not a deployment name
```

---

## API Version Governance

Azure OpenAI introduces breaking changes between `api-version` values. Always pin the version explicitly and review Azure OpenAI changelog before updating.

```python
# Pinned in the URL query string for direct REST calls
url = (
    f"{self.azure_openai_endpoint}/openai/deployments/"
    f"{self.azure_openai_model}/chat/completions"
    f"?api-version={self.azure_api_version}"
)
```

For `langchain-openai` integration:

```python
from langchain_openai import AzureChatOpenAI

llm = AzureChatOpenAI(
    azure_endpoint=settings.azure_openai_endpoint,
    azure_deployment=settings.azure_openai_model,    # deployment name
    api_version=settings.azure_api_version,          # pinned version
    api_key=settings.azure_openai_api_key,
)
```

---

## Custom LLM Wrapper Pattern

> **Per `BUS-7.1` (Audit Trail):** Every LLM call must carry a Transaction ID (TID) for end-to-end traceability. The TID must be the first parameter of every call method.

### Recommended Structure

```python
class AzureLLMWrapper:
    """Per BUS-7.1: TID propagates through all calls for audit traceability."""

    def __init__(self):
        self._endpoint = (
            f"{settings.azure_openai_endpoint}/openai/deployments/"
            f"{settings.azure_openai_model}/chat/completions"
            f"?api-version={settings.azure_api_version}"
        )
        self._headers = {
            "Content-Type": "application/json",
            "api-key": settings.azure_openai_api_key,   # never logged
        }

    def _call_llm(self, tid: str, payload: dict) -> str:
        """Per ENG-6.5: Validate payload before calling. Per BUS-7.1: TID required."""
        if not payload.get("messages"):
            raise ValueError(f"TID {tid}: payload missing 'messages' field")

        response = requests.post(self._endpoint, headers=self._headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()

        # Log usage — but NOT the prompt content (may contain PII after restoration)
        usage = data.get("usage", {})
        logging.info(
            f"TID {tid} - Azure OpenAI call complete. "
            f"model={settings.azure_openai_model}, "
            f"prompt_tokens={usage.get('prompt_tokens')}, "
            f"completion_tokens={usage.get('completion_tokens')}, "
            f"finish_reason={data['choices'][0].get('finish_reason')}"
        )

        return data["choices"][0]["message"]["content"]

    def generate(self, tid: str, user_prompt: str, system_prompt: str) -> str:
        payload = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]
        }
        return self._call_llm(tid, payload)
```

---

## Retry Pattern

Azure OpenAI returns `429 Too Many Requests` and transient `5xx` errors. Use `tenacity` for retry:

```python
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import requests

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(requests.exceptions.HTTPError),
)
def _call_llm_with_retry(self, tid: str, payload: dict) -> str:
    return self._call_llm(tid, payload)
```

---

## Content Filter Response Handling

Azure OpenAI includes `content_filter_results` in every response. Check and log this for audit compliance:

```python
choice = data["choices"][0]
filter_results = choice.get("content_filter_results", {})
if any(v.get("filtered") for v in filter_results.values()):
    logging.warning(f"TID {tid} - Content filtered: {filter_results}")
    raise ContentFilterException(f"TID {tid}: Response content was filtered by Azure OpenAI")
```

---

## Testing Pattern

> **Per `ENG-4.1` (Atomic TDD):** LLM wrapper methods must be unit-testable with mocked HTTP responses. No live Azure credentials required in unit tests.

See `examples/ENG-4.1-wrapper-tdd.md` for the full TDD cycle with `responses` library.

### Anti-Patterns to Avoid

| Anti-Pattern | Correct Pattern |
|-------------|----------------|
| Live Azure call in unit test | Mock with `responses` or `unittest.mock` |
| `AZURE_OPENAI_KEY` hardcoded in test | Inject via `monkeypatch.setenv` |
| No TID parameter in `_call_llm` | TID is first parameter — non-negotiable per `BUS-7.1` |
| Full URL in env var | Service name in env var; endpoint constructed in code |
| Model name (not deployment name) in `AZURE_OPENAI_MODEL` | Deployment name only |
| Logging `api-key` header value | Never log credentials; log TID and model name only |

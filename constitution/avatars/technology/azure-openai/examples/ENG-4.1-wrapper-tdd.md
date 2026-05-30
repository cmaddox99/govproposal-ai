---
law_id: ENG-4.1
avatar: azure-openai
---

# ENG-4.1: Atomic TDD Examples for Azure OpenAI Custom LLM Wrapper

## COMPLIANT: Full TDD Cycle with Mocked HTTP

```python
# tests/unit/test_llm_wrapper.py
import pytest
import responses as responses_lib
from unittest.mock import patch
from app.status.models.Custom_LLMWrapper_new import AzureLLMWrapper


# ─────────────────────────────────────────────────────────────
# Step 1: RED — Write failing test FIRST, before any implementation
# ─────────────────────────────────────────────────────────────

@responses_lib.activate
def test_generate_returns_llm_content_on_success():
    """LLM wrapper returns the message content from Azure OpenAI response."""
    # GIVEN
    responses_lib.add(
        responses_lib.POST,
        "https://test-service.openai.azure.com/openai/deployments/gpt-4o/chat/completions",
        json={
            "choices": [{
                "message": {"role": "assistant", "content": "Dear Passenger, ..."},
                "finish_reason": "stop",
                "content_filter_results": {}
            }],
            "usage": {"prompt_tokens": 120, "completion_tokens": 80}
        },
        status=200,
    )
    wrapper = AzureLLMWrapper()

    # WHEN
    result = wrapper.generate(
        tid="test-001",
        user_prompt="Generate a response for complaint category: INFLIGHT",
        system_prompt="You are a compliance-driven response generator."
    )

    # THEN
    assert result == "Dear Passenger, ..."


# ─────────────────────────────────────────────────────────────
# Step 2: GREEN — Implement minimal code in AzureLLMWrapper
# ─────────────────────────────────────────────────────────────

# class AzureLLMWrapper:
#     def generate(self, tid, user_prompt, system_prompt) -> str:
#         payload = {"messages": [
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": user_prompt},
#         ]}
#         return self._call_llm(tid, payload)
#
#     def _call_llm(self, tid, payload) -> str:
#         response = requests.post(self._endpoint, headers=self._headers, json=payload)
#         return response.json()["choices"][0]["message"]["content"]


# ─────────────────────────────────────────────────────────────
# Step 3: Next RED — TID is required; missing TID must raise
# ─────────────────────────────────────────────────────────────

def test_call_llm_raises_when_payload_missing_messages():
    """Per ENG-6.5: payload must be validated before the HTTP call."""
    # GIVEN
    wrapper = AzureLLMWrapper()

    # WHEN / THEN
    with pytest.raises(ValueError, match="missing 'messages'"):
        wrapper._call_llm(tid="test-002", payload={})


# Step 4: GREEN — add validation guard in _call_llm


# ─────────────────────────────────────────────────────────────
# Step 5: Next RED — 429 retry behavior
# ─────────────────────────────────────────────────────────────

@responses_lib.activate
def test_generate_retries_on_429_and_succeeds():
    """Wrapper retries up to 3 times on 429 Too Many Requests."""
    # GIVEN — first call 429, second call succeeds
    responses_lib.add(
        responses_lib.POST,
        "https://test-service.openai.azure.com/openai/deployments/gpt-4o/chat/completions",
        status=429,
    )
    responses_lib.add(
        responses_lib.POST,
        "https://test-service.openai.azure.com/openai/deployments/gpt-4o/chat/completions",
        json={
            "choices": [{"message": {"content": "Retry succeeded"}, "finish_reason": "stop", "content_filter_results": {}}],
            "usage": {}
        },
        status=200,
    )
    wrapper = AzureLLMWrapper()

    # WHEN
    result = wrapper.generate(tid="test-003", user_prompt="Test", system_prompt="Test")

    # THEN
    assert result == "Retry succeeded"


# Step 6: GREEN — wrap _call_llm with tenacity retry decorator


# ─────────────────────────────────────────────────────────────
# Step 7: Security RED — API key must never appear in logs
# ─────────────────────────────────────────────────────────────

@responses_lib.activate
def test_api_key_does_not_appear_in_log_output(caplog):
    """Per ENG-6.1: API key must never be logged at any level."""
    import logging
    responses_lib.add(
        responses_lib.POST,
        "https://test-service.openai.azure.com/openai/deployments/gpt-4o/chat/completions",
        json={
            "choices": [{"message": {"content": "ok"}, "finish_reason": "stop", "content_filter_results": {}}],
            "usage": {}
        },
        status=200,
    )
    with patch.dict("os.environ", {"AZURE_OPENAI_KEY": "secret-key-abc123"}):
        wrapper = AzureLLMWrapper()
        with caplog.at_level(logging.DEBUG):
            wrapper.generate(tid="test-004", user_prompt="Test", system_prompt="Test")

    # THEN — key must not appear anywhere in captured logs
    assert "secret-key-abc123" not in caplog.text


# Step 8: GREEN — confirm logging statements never reference self._headers or api_key value
```

## VIOLATION: Untestable Wrapper (No TID, Hardcoded Credentials)

```python
# BAD — multiple violations
class AzureLLMWrapper:
    def generate(self, prompt: str) -> str:  # no TID — untraceable per BUS-7.1
        headers = {"api-key": "hardcoded-key-abc"}   # violates ENG-6.1
        print(f"Calling with key: hardcoded-key-abc")  # logs secret — critical violation
        response = requests.post(ENDPOINT, headers=headers, json={"messages": prompt})
        return response.json()["choices"][0]["message"]["content"]
```

**Why non-compliant:** Missing TID breaks `BUS-7.1` audit trail. Hardcoded key violates `ENG-6.1`. Logging the key is a critical security violation. `prompt` as a bare string bypasses `ENG-6.5` input validation.

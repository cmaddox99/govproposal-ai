# LLM Applications Guidance

> **Purpose:** Stack-specific agent behaviors for building applications with LLM APIs (OpenAI, Anthropic, Google, etc.).

---

## Overview

This guidance provides patterns for AI agents working directly with LLM APIs to build AI-powered applications without heavy frameworks. Covers prompt management, API best practices, and production patterns.

---

## Testing Framework

**Primary Framework:** pytest + pytest-asyncio + responses/httpx-mock

### Test Structure

```python
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import json
from myproject.llm.client import LLMClient
from myproject.llm.prompts import PromptTemplate
from myproject.services.completion import CompletionService


class TestLLMClient:
    """Tests for LLM client wrapper."""

    @pytest.fixture
    def mock_openai_response(self):
        """Mock OpenAI API response."""
        return {
            "id": "chatcmpl-123",
            "object": "chat.completion",
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "Test response"
                },
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 5,
                "total_tokens": 15
            }
        }

    @pytest.fixture
    def client(self):
        """LLM client instance."""
        return LLMClient(api_key="test-key", model="gpt-4")

    @patch('openai.ChatCompletion.create')
    def test_client_sends_request(self, mock_create, client, mock_openai_response):
        """Client should send properly formatted request."""
        # Arrange
        mock_create.return_value = mock_openai_response

        # Act
        response = client.complete("Hello")

        # Assert
        mock_create.assert_called_once()
        call_args = mock_create.call_args
        assert call_args.kwargs["model"] == "gpt-4"
        assert len(call_args.kwargs["messages"]) > 0

    @patch('openai.ChatCompletion.create')
    def test_client_returns_content(self, mock_create, client, mock_openai_response):
        """Client should extract content from response."""
        # Arrange
        mock_create.return_value = mock_openai_response

        # Act
        response = client.complete("Hello")

        # Assert
        assert response.content == "Test response"
        assert response.usage.total_tokens == 15


class TestPromptTemplate:
    """Tests for prompt templates."""

    def test_template_renders_variables(self):
        """Template should render variables correctly."""
        # Arrange
        template = PromptTemplate(
            "Hello {name}, you asked about {topic}."
        )

        # Act
        result = template.render(name="Alice", topic="Python")

        # Assert
        assert result == "Hello Alice, you asked about Python."

    def test_template_validates_required_vars(self):
        """Template should validate required variables."""
        # Arrange
        template = PromptTemplate(
            "Hello {name}",
            required_vars=["name"]
        )

        # Act & Assert
        with pytest.raises(ValueError, match="Missing required variable"):
            template.render()

    def test_template_escapes_special_chars(self):
        """Template should handle special characters safely."""
        # Arrange
        template = PromptTemplate("User said: {message}")

        # Act
        result = template.render(message="Hello {world}")

        # Assert
        assert "{world}" in result  # Not treated as variable


class TestCompletionService:
    """Tests for the completion service."""

    @pytest.fixture
    def mock_client(self):
        """Mock LLM client."""
        mock = MagicMock(spec=LLMClient)
        mock.complete.return_value = MagicMock(content="Generated response")
        return mock

    @pytest.fixture
    def service(self, mock_client):
        """Completion service with mock."""
        return CompletionService(client=mock_client)

    def test_service_applies_system_prompt(self, service, mock_client):
        """Service should include system prompt."""
        # Act
        service.complete("User message", system_prompt="Be helpful")

        # Assert
        call_args = mock_client.complete.call_args
        messages = call_args.kwargs.get("messages", call_args.args[0])
        assert any(m["role"] == "system" for m in messages)

    def test_service_tracks_conversation(self, service):
        """Service should maintain conversation history."""
        # Act
        service.complete("First message")
        service.complete("Second message")

        # Assert
        assert len(service.history) == 4  # 2 user + 2 assistant

    def test_service_respects_max_tokens(self, service, mock_client):
        """Service should pass max_tokens to client."""
        # Act
        service.complete("Message", max_tokens=100)

        # Assert
        call_args = mock_client.complete.call_args
        assert call_args.kwargs.get("max_tokens") == 100
```

---

## Common Patterns

### Good Patterns

**LLM Client Wrapper:**

```python
from dataclasses import dataclass
from typing import Optional, List
import openai
import time
from tenacity import retry, stop_after_attempt, wait_exponential

@dataclass
class LLMResponse:
    """Structured LLM response."""
    content: str
    model: str
    usage: dict
    finish_reason: str
    raw_response: dict

@dataclass
class Message:
    """Chat message."""
    role: str  # system, user, assistant
    content: str

class LLMClient:
    """Wrapper for LLM API calls."""

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4",
        default_temperature: float = 0.7,
        default_max_tokens: int = 1000,
        timeout: int = 30
    ):
        self.api_key = api_key
        self.model = model
        self.default_temperature = default_temperature
        self.default_max_tokens = default_max_tokens
        self.timeout = timeout

        openai.api_key = api_key

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=60)
    )
    def complete(
        self,
        messages: List[Message],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        """Send completion request."""

        formatted_messages = [
            {"role": m.role, "content": m.content}
            for m in messages
        ]

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=formatted_messages,
            temperature=temperature or self.default_temperature,
            max_tokens=max_tokens or self.default_max_tokens,
            timeout=self.timeout,
            **kwargs
        )

        return LLMResponse(
            content=response.choices[0].message.content,
            model=response.model,
            usage=response.usage,
            finish_reason=response.choices[0].finish_reason,
            raw_response=response
        )

    async def acomplete(self, messages: List[Message], **kwargs) -> LLMResponse:
        """Async completion."""
        # Similar implementation with async client
        pass
```

**Prompt Template System:**

```python
from string import Template
from typing import Dict, List, Optional
import yaml

class PromptTemplate:
    """Versioned, validated prompt template."""

    def __init__(
        self,
        template: str,
        name: str = None,
        version: str = "1.0.0",
        required_vars: List[str] = None,
        description: str = None
    ):
        self.template = template
        self.name = name
        self.version = version
        self.required_vars = required_vars or self._extract_vars()
        self.description = description

    def _extract_vars(self) -> List[str]:
        """Extract variable names from template."""
        import re
        return re.findall(r'\{(\w+)\}', self.template)

    def render(self, **kwargs) -> str:
        """Render template with variables."""
        # Validate required variables
        missing = set(self.required_vars) - set(kwargs.keys())
        if missing:
            raise ValueError(f"Missing required variables: {missing}")

        return self.template.format(**kwargs)

    def to_dict(self) -> dict:
        """Serialize template."""
        return {
            "name": self.name,
            "version": self.version,
            "template": self.template,
            "required_vars": self.required_vars,
            "description": self.description
        }


class PromptRegistry:
    """Registry for prompt templates."""

    def __init__(self):
        self._prompts: Dict[str, PromptTemplate] = {}

    def register(self, prompt: PromptTemplate):
        """Register a prompt template."""
        key = f"{prompt.name}:{prompt.version}"
        self._prompts[key] = prompt

    def get(self, name: str, version: str = None) -> PromptTemplate:
        """Get prompt by name and optional version."""
        if version:
            return self._prompts[f"{name}:{version}"]

        # Get latest version
        matching = [k for k in self._prompts if k.startswith(f"{name}:")]
        if not matching:
            raise KeyError(f"Prompt not found: {name}")
        latest = sorted(matching)[-1]
        return self._prompts[latest]

    def load_from_yaml(self, path: str):
        """Load prompts from YAML file."""
        with open(path) as f:
            data = yaml.safe_load(f)

        for prompt_data in data.get("prompts", []):
            self.register(PromptTemplate(**prompt_data))


# Pre-defined prompts
SUMMARIZATION_PROMPT = PromptTemplate(
    name="summarization",
    version="1.0.0",
    template="""Summarize the following text in {length} sentences.

Text:
{text}

Summary:""",
    description="General text summarization"
)

CLASSIFICATION_PROMPT = PromptTemplate(
    name="classification",
    version="1.0.0",
    template="""Classify the following text into one of these categories: {categories}

Text: {text}

Respond with only the category name.""",
    description="Text classification"
)
```

**Response Caching:**

```python
import hashlib
import json
from typing import Optional
from datetime import datetime, timedelta

class ResponseCache:
    """Cache LLM responses to reduce costs."""

    def __init__(self, backend, ttl_seconds: int = 3600):
        self.backend = backend  # Redis, file, memory, etc.
        self.ttl = timedelta(seconds=ttl_seconds)

    def _cache_key(self, messages: list, model: str, **kwargs) -> str:
        """Generate cache key from request."""
        key_data = {
            "messages": messages,
            "model": model,
            **kwargs
        }
        key_str = json.dumps(key_data, sort_keys=True)
        return hashlib.sha256(key_str.encode()).hexdigest()

    def get(self, messages: list, model: str, **kwargs) -> Optional[dict]:
        """Get cached response."""
        key = self._cache_key(messages, model, **kwargs)
        cached = self.backend.get(key)

        if cached:
            data = json.loads(cached)
            if datetime.fromisoformat(data["expires_at"]) > datetime.utcnow():
                return data["response"]

        return None

    def set(self, messages: list, model: str, response: dict, **kwargs):
        """Cache a response."""
        key = self._cache_key(messages, model, **kwargs)
        data = {
            "response": response,
            "cached_at": datetime.utcnow().isoformat(),
            "expires_at": (datetime.utcnow() + self.ttl).isoformat()
        }
        self.backend.set(key, json.dumps(data))


class CachedLLMClient:
    """LLM client with caching."""

    def __init__(self, client: LLMClient, cache: ResponseCache):
        self.client = client
        self.cache = cache

    def complete(self, messages: list, use_cache: bool = True, **kwargs):
        """Complete with optional caching."""
        if use_cache:
            cached = self.cache.get(messages, self.client.model, **kwargs)
            if cached:
                return cached

        response = self.client.complete(messages, **kwargs)

        if use_cache:
            self.cache.set(messages, self.client.model, response, **kwargs)

        return response
```

**Cost Tracking:**

```python
from dataclasses import dataclass
from typing import Dict
from datetime import datetime

# Pricing per 1K tokens (example, update with actual pricing)
PRICING = {
    "gpt-4": {"input": 0.03, "output": 0.06},
    "gpt-4-turbo": {"input": 0.01, "output": 0.03},
    "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
    "claude-3-opus": {"input": 0.015, "output": 0.075},
    "claude-3-sonnet": {"input": 0.003, "output": 0.015},
}

@dataclass
class UsageRecord:
    timestamp: datetime
    model: str
    input_tokens: int
    output_tokens: int
    cost: float

class CostTracker:
    """Track LLM API costs."""

    def __init__(self):
        self.records: list[UsageRecord] = []

    def record(self, model: str, usage: dict):
        """Record usage from API response."""
        input_tokens = usage.get("prompt_tokens", 0)
        output_tokens = usage.get("completion_tokens", 0)

        pricing = PRICING.get(model, {"input": 0, "output": 0})
        cost = (
            (input_tokens / 1000) * pricing["input"] +
            (output_tokens / 1000) * pricing["output"]
        )

        self.records.append(UsageRecord(
            timestamp=datetime.utcnow(),
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost=cost
        ))

    def get_total_cost(self, since: datetime = None) -> float:
        """Get total cost, optionally since a date."""
        records = self.records
        if since:
            records = [r for r in records if r.timestamp >= since]
        return sum(r.cost for r in records)

    def get_summary(self) -> Dict:
        """Get usage summary by model."""
        summary = {}
        for record in self.records:
            if record.model not in summary:
                summary[record.model] = {
                    "calls": 0,
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "cost": 0
                }
            summary[record.model]["calls"] += 1
            summary[record.model]["input_tokens"] += record.input_tokens
            summary[record.model]["output_tokens"] += record.output_tokens
            summary[record.model]["cost"] += record.cost
        return summary
```

---

## Anti-Patterns to Avoid

### No Retry Logic

```python
# BAD - No handling for transient failures
response = openai.ChatCompletion.create(...)  # May fail randomly

# GOOD - Retry with backoff
@retry(stop=stop_after_attempt(3), wait=wait_exponential())
def complete_with_retry(messages):
    return openai.ChatCompletion.create(...)
```

### Ignoring Token Limits

```python
# BAD - May exceed context window
response = client.complete(very_long_text)

# GOOD - Check and truncate
def safe_complete(text: str, max_input_tokens: int = 3000):
    token_count = count_tokens(text)
    if token_count > max_input_tokens:
        text = truncate_to_tokens(text, max_input_tokens)
    return client.complete(text)
```

### Hardcoded API Keys

```python
# BAD - Key in code
client = OpenAI(api_key="sk-...")

# GOOD - Environment variable
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
```

---

## Tools and Commands

### Development

```bash
# Install dependencies
pip install openai anthropic tiktoken

# Set up environment
export OPENAI_API_KEY=xxx
export ANTHROPIC_API_KEY=xxx

# Run interactive testing
python -c "from src.llm import LLMClient; ..."
```

### Testing

```bash
# Run unit tests (mocked)
pytest tests/ -m "not integration"

# Run integration tests
pytest tests/integration/ -m integration

# Run with verbose
pytest -v -s
```

### Token Counting

```bash
# Count tokens in a file
python -c "
import tiktoken
enc = tiktoken.encoding_for_model('gpt-4')
text = open('input.txt').read()
print(f'Tokens: {len(enc.encode(text))}')
"
```

---

## LLM Application Guidance

### Testing Strategy

1. **Unit Tests** - Mock API calls
   - Client behavior
   - Prompt rendering
   - Response parsing

2. **Integration Tests** - Real API calls (sparingly)
   - End-to-end flows
   - Error handling
   - Rate limiting

3. **Prompt Tests** - Evaluate prompt quality
   - Output format
   - Edge cases
   - Consistency

### Production Checklist

```markdown
## LLM Application Production Checklist

### API Integration
- [ ] Retry logic with exponential backoff
- [ ] Timeout handling
- [ ] Rate limit handling
- [ ] Error logging

### Cost Management
- [ ] Token counting before requests
- [ ] Cost tracking
- [ ] Budget alerts
- [ ] Caching for repeated queries

### Security
- [ ] API keys in environment/secrets manager
- [ ] Input validation
- [ ] Output filtering
- [ ] PII detection

### Observability
- [ ] Request/response logging
- [ ] Latency metrics
- [ ] Token usage metrics
- [ ] Error rate tracking

### Reliability
- [ ] Fallback models configured
- [ ] Graceful degradation
- [ ] Circuit breaker for API failures
```

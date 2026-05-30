---
law_id: ENG-4.1
avatar: llm-applications
---

# ENG-4.1: Atomic TDD Examples for LLM Applications

## COMPLIANT: Unit Testing LLM Integration with Mocked Responses

```python
import pytest
from unittest.mock import Mock, patch, AsyncMock
from typing import List, Dict, Any
import json

from llm_client import LLMClient, LLMResponse
from llm_handlers import (
    ResponseParser,
    ConversationManager,
    PromptBuilder,
    RetryHandler
)


class TestResponseParser:
    """Atomic tests for LLM response parsing."""

    @pytest.fixture
    def parser(self):
        """Provide response parser instance."""
        return ResponseParser()

    def test_parse_json_response_extracts_valid_json(self, parser):
        """Test parsing JSON from LLM response."""
        response_text = """Here's the analysis:
        ```json
        {"sentiment": "positive", "confidence": 0.95}
        ```
        """

        result = parser.parse_json_response(response_text)

        assert result == {"sentiment": "positive", "confidence": 0.95}

    def test_parse_json_response_handles_no_code_block(self, parser):
        """Test parsing when JSON is not in code block."""
        response_text = '{"key": "value"}'

        result = parser.parse_json_response(response_text)

        assert result == {"key": "value"}

    def test_parse_json_response_returns_none_for_invalid_json(self, parser):
        """Test graceful handling of invalid JSON."""
        response_text = "This is not JSON at all"

        result = parser.parse_json_response(response_text)

        assert result is None

    def test_parse_list_response_splits_numbered_items(self, parser):
        """Test parsing numbered list from response."""
        response_text = """1. First item
        2. Second item
        3. Third item"""

        result = parser.parse_list_response(response_text)

        assert result == ["First item", "Second item", "Third item"]

    def test_parse_list_response_handles_bullet_points(self, parser):
        """Test parsing bullet point list."""
        response_text = """- Item A
        - Item B
        - Item C"""

        result = parser.parse_list_response(response_text)

        assert result == ["Item A", "Item B", "Item C"]


class TestConversationManager:
    """Atomic tests for conversation history management."""

    @pytest.fixture
    def manager(self):
        """Provide conversation manager."""
        return ConversationManager(max_history=5)

    def test_add_message_stores_in_history(self, manager):
        """Test that messages are added to history."""
        manager.add_message("user", "Hello")

        history = manager.get_history()

        assert len(history) == 1
        assert history[0]["role"] == "user"
        assert history[0]["content"] == "Hello"

    def test_history_respects_max_length(self, manager):
        """Test that history is trimmed to max length."""
        for i in range(10):
            manager.add_message("user", f"Message {i}")

        history = manager.get_history()

        assert len(history) == 5
        # Should keep most recent messages
        assert history[-1]["content"] == "Message 9"

    def test_clear_history_removes_all_messages(self, manager):
        """Test clearing conversation history."""
        manager.add_message("user", "Hello")
        manager.add_message("assistant", "Hi!")

        manager.clear_history()

        assert len(manager.get_history()) == 0

    def test_get_context_window_returns_recent_messages(self, manager):
        """Test getting limited context window."""
        for i in range(5):
            manager.add_message("user", f"Message {i}")

        context = manager.get_context_window(limit=3)

        assert len(context) == 3
        assert context[-1]["content"] == "Message 4"


class TestPromptBuilder:
    """Atomic tests for prompt construction."""

    @pytest.fixture
    def builder(self):
        """Provide prompt builder."""
        return PromptBuilder(
            system_template="You are a {role} assistant.",
            user_template="User request: {request}"
        )

    def test_build_system_prompt_formats_template(self, builder):
        """Test system prompt template formatting."""
        result = builder.build_system_prompt(role="helpful")

        assert result == "You are a helpful assistant."

    def test_build_user_prompt_formats_template(self, builder):
        """Test user prompt template formatting."""
        result = builder.build_user_prompt(request="Summarize this text")

        assert result == "User request: Summarize this text"

    def test_build_messages_creates_correct_structure(self, builder):
        """Test building complete message structure."""
        messages = builder.build_messages(
            system_vars={"role": "coding"},
            user_vars={"request": "Write a function"},
            history=[{"role": "user", "content": "Previous message"}]
        )

        assert len(messages) == 3
        assert messages[0]["role"] == "system"
        assert messages[1]["role"] == "user"  # History
        assert messages[2]["role"] == "user"  # Current

    def test_build_prompt_escapes_special_characters(self, builder):
        """Test that special characters in input are handled."""
        builder = PromptBuilder(
            system_template="Process: {input}",
            user_template="{query}"
        )

        # Input with braces that shouldn't be interpreted as templates
        result = builder.build_system_prompt(input="dict = {key: value}")

        assert "dict = {key: value}" in result


class TestRetryHandler:
    """Atomic tests for LLM request retry logic."""

    @pytest.fixture
    def handler(self):
        """Provide retry handler."""
        return RetryHandler(
            max_retries=3,
            base_delay=0.1,
            max_delay=1.0
        )

    def test_successful_request_returns_immediately(self, handler):
        """Test that successful requests don't retry."""
        mock_func = Mock(return_value="Success")

        result = handler.execute_with_retry(mock_func)

        assert result == "Success"
        assert mock_func.call_count == 1

    def test_retries_on_rate_limit_error(self, handler):
        """Test retry on rate limit errors."""
        mock_func = Mock(side_effect=[
            RateLimitError("Rate limited"),
            RateLimitError("Rate limited"),
            "Success"
        ])

        result = handler.execute_with_retry(mock_func)

        assert result == "Success"
        assert mock_func.call_count == 3

    def test_raises_after_max_retries(self, handler):
        """Test that error is raised after max retries."""
        mock_func = Mock(side_effect=RateLimitError("Rate limited"))

        with pytest.raises(RateLimitError):
            handler.execute_with_retry(mock_func)

        assert mock_func.call_count == 3

    def test_exponential_backoff_increases_delay(self, handler):
        """Test that delays increase exponentially."""
        delays = handler.calculate_delays()

        assert delays[0] == 0.1
        assert delays[1] == 0.2
        assert delays[2] == 0.4

    def test_delay_respects_max_limit(self, handler):
        """Test that delay doesn't exceed maximum."""
        handler = RetryHandler(max_retries=10, base_delay=0.5, max_delay=1.0)

        delays = handler.calculate_delays()

        assert all(d <= 1.0 for d in delays)


class TestLLMClient:
    """Atomic tests for LLM client functionality."""

    @pytest.fixture
    def mock_http_client(self):
        """Provide mock HTTP client."""
        return Mock()

    @pytest.fixture
    def client(self, mock_http_client):
        """Provide LLM client with mocked HTTP."""
        return LLMClient(
            api_key="test-key",
            http_client=mock_http_client
        )

    def test_format_request_creates_valid_payload(self, client):
        """Test request payload formatting."""
        messages = [{"role": "user", "content": "Hello"}]

        payload = client.format_request(
            messages=messages,
            model="gpt-4",
            temperature=0.7
        )

        assert payload["model"] == "gpt-4"
        assert payload["messages"] == messages
        assert payload["temperature"] == 0.7

    def test_parse_response_extracts_content(self, client):
        """Test response parsing."""
        raw_response = {
            "choices": [{
                "message": {"content": "Response text"},
                "finish_reason": "stop"
            }],
            "usage": {"total_tokens": 100}
        }

        result = client.parse_response(raw_response)

        assert result.content == "Response text"
        assert result.finish_reason == "stop"
        assert result.total_tokens == 100

    def test_handles_api_error_response(self, client):
        """Test handling of API error responses."""
        error_response = {
            "error": {
                "message": "Invalid API key",
                "type": "authentication_error"
            }
        }

        with pytest.raises(APIError) as exc_info:
            client.parse_response(error_response)

        assert "Invalid API key" in str(exc_info.value)
```

**Why compliant:** Each test verifies a single behavior of an LLM integration component. No actual API calls are made - all responses are mocked. Tests focus on parsing, formatting, and error handling logic. Fixtures provide consistent test setup. Edge cases (invalid JSON, rate limits, errors) are tested separately.

---

## VIOLATION: Testing LLM Integration with Real API Calls

```python
import openai


def test_llm_summarization():
    """Test summarization with real API - not atomic."""
    # Real API call - slow, costly, non-deterministic
    client = openai.OpenAI()

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{
            "role": "user",
            "content": "Summarize: " + "Long text..." * 100
        }]
    )

    # Vague assertions - output varies
    assert len(response.choices[0].message.content) > 0
    assert len(response.choices[0].message.content) < 500


def test_conversation_flow():
    """Test multi-turn conversation - too many concerns."""
    client = openai.OpenAI()

    # First turn
    response1 = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "My name is Alice"}]
    )

    # Second turn - depends on first response
    response2 = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": "My name is Alice"},
            {"role": "assistant", "content": response1.choices[0].message.content},
            {"role": "user", "content": "What is my name?"}
        ]
    )

    # Assertion depends on LLM remembering context
    assert "Alice" in response2.choices[0].message.content


def test_error_handling():
    """Test error handling with real errors."""
    client = openai.OpenAI(api_key="invalid-key")

    # Will make real API call with invalid key
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello"}]
        )
    except openai.AuthenticationError:
        pass  # Expected

    # No actual verification of error handling logic
```

**Why violates ENG-4.1:** Tests make real API calls which are slow, costly, and non-deterministic. Output quality varies between runs, making assertions unreliable. Error testing requires invalid credentials to hit real API. Multiple API calls in single test increase cost and flakiness. Tests don't isolate specific parsing or formatting logic.

---

## COMPLIANT: Testing Streaming Response Handling

```python
import pytest
from unittest.mock import Mock, AsyncMock
import asyncio
from typing import AsyncIterator

from llm_client import StreamingLLMClient
from llm_handlers import StreamProcessor, TokenCounter


class TestStreamProcessor:
    """Atomic tests for streaming response processing."""

    @pytest.fixture
    def processor(self):
        """Provide stream processor."""
        return StreamProcessor()

    @pytest.fixture
    def mock_stream(self):
        """Provide mock streaming response."""
        async def generate_chunks():
            chunks = [
                {"choices": [{"delta": {"content": "Hello"}}]},
                {"choices": [{"delta": {"content": " world"}}]},
                {"choices": [{"delta": {"content": "!"}}]},
                {"choices": [{"delta": {}, "finish_reason": "stop"}]}
            ]
            for chunk in chunks:
                yield chunk

        return generate_chunks()

    @pytest.mark.asyncio
    async def test_process_stream_concatenates_chunks(
        self, processor, mock_stream
    ):
        """Test that stream chunks are concatenated correctly."""
        result = await processor.process_stream(mock_stream)

        assert result.content == "Hello world!"

    @pytest.mark.asyncio
    async def test_stream_callback_called_for_each_chunk(self, processor):
        """Test that callback is invoked for each chunk."""
        callback = Mock()

        async def mock_stream():
            yield {"choices": [{"delta": {"content": "A"}}]}
            yield {"choices": [{"delta": {"content": "B"}}]}

        await processor.process_stream(mock_stream(), on_chunk=callback)

        assert callback.call_count == 2
        callback.assert_any_call("A")
        callback.assert_any_call("B")

    @pytest.mark.asyncio
    async def test_handles_empty_delta_gracefully(self, processor):
        """Test handling of empty delta in stream."""
        async def mock_stream():
            yield {"choices": [{"delta": {"content": "Start"}}]}
            yield {"choices": [{"delta": {}}]}  # Empty delta
            yield {"choices": [{"delta": {"content": "End"}}]}

        result = await processor.process_stream(mock_stream())

        assert result.content == "StartEnd"


class TestTokenCounter:
    """Atomic tests for token counting functionality."""

    @pytest.fixture
    def counter(self):
        """Provide token counter."""
        return TokenCounter(model="gpt-4")

    def test_count_tokens_for_simple_text(self, counter):
        """Test token counting for simple text."""
        text = "Hello, world!"

        count = counter.count_tokens(text)

        # Approximate - exact count depends on tokenizer
        assert 2 <= count <= 5

    def test_count_tokens_for_messages(self, counter):
        """Test token counting for message array."""
        messages = [
            {"role": "system", "content": "You are helpful."},
            {"role": "user", "content": "Hello!"}
        ]

        count = counter.count_message_tokens(messages)

        # Should include message overhead tokens
        assert count > counter.count_tokens("You are helpful.Hello!")

    def test_estimate_cost_calculates_correctly(self, counter):
        """Test cost estimation calculation."""
        # Known token counts for deterministic test
        input_tokens = 1000
        output_tokens = 500

        cost = counter.estimate_cost(
            input_tokens=input_tokens,
            output_tokens=output_tokens
        )

        # GPT-4 pricing: $0.03/1K input, $0.06/1K output
        expected = (1000 * 0.03 / 1000) + (500 * 0.06 / 1000)
        assert cost == pytest.approx(expected, rel=0.01)

    def test_will_fit_in_context_returns_correct_boolean(self, counter):
        """Test context window size checking."""
        # Short text should fit
        assert counter.will_fit_in_context("Hello", max_tokens=8192)

        # Very long text should not fit
        long_text = "word " * 100000
        assert not counter.will_fit_in_context(long_text, max_tokens=8192)
```

**Why compliant:** Each test verifies a single streaming behavior. Mock streams provide deterministic test data. Async handling is tested with proper pytest-asyncio fixtures. Token counting and cost estimation are tested independently. Edge cases (empty deltas, context limits) are tested separately.

---

## VIOLATION: Testing Streaming Without Isolation

```python
import openai


async def test_streaming_response():
    """Test streaming with real API - not atomic."""
    client = openai.OpenAI()

    # Real streaming API call
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Count from 1 to 10"}],
        stream=True
    )

    chunks = []
    for chunk in stream:
        if chunk.choices[0].delta.content:
            chunks.append(chunk.choices[0].delta.content)

    full_response = "".join(chunks)

    # Vague assertion - content varies
    assert len(full_response) > 0
    assert any(str(i) in full_response for i in range(1, 11))


async def test_streaming_with_timeout():
    """Test streaming timeout - depends on network."""
    import asyncio

    client = openai.OpenAI()

    # Real API call with artificial timeout
    try:
        async with asyncio.timeout(0.001):  # Unrealistic timeout
            stream = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": "Hello"}],
                stream=True
            )
            async for chunk in stream:
                pass
    except asyncio.TimeoutError:
        pass  # Expected but not really testing our timeout logic
```

**Why violates ENG-4.1:** Real API calls make tests slow and costly. Stream content is non-deterministic. Network conditions affect test reliability. No isolation of streaming logic from API communication. Timeout testing depends on network latency.

---

## TDD Cycle Commands

```bash
# RED: Run specific test, see it fail
pytest tests/llm/test_client.py::test_client_returns_completion -v

# GREEN: Write code, run test again
pytest tests/llm/test_client.py::test_client_returns_completion -v

# REFACTOR: Run all unit tests
pytest tests/ -m "not integration"

# VERIFY: Check coverage and constitutional compliance
pytest --cov=src --cov-fail-under=80
constitution-lint .

# Commit when green and compliant
git add -A && git commit -m "Add LLM client completion method"
```

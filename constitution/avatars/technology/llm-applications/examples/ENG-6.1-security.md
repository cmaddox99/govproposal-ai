---
law_id: ENG-6.1
avatar: llm-applications
---

# ENG-6.1: Security Examples for LLM Applications

## COMPLIANT: Secure API Key Management

```python
import os
from dataclasses import dataclass
from typing import Optional
from functools import lru_cache
import boto3
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class APICredentials:
    """Immutable credentials container."""
    api_key: str
    organization_id: Optional[str] = None

    def __repr__(self):
        """Prevent accidental logging of credentials."""
        return "APICredentials(api_key=***, organization_id=***)"

    def __str__(self):
        """Prevent accidental printing of credentials."""
        return self.__repr__()


class SecureCredentialManager:
    """Manage API credentials securely using secrets manager."""

    def __init__(self, region_name: str = "us-east-1"):
        self.secrets_client = boto3.client(
            "secretsmanager",
            region_name=region_name
        )

    @lru_cache(maxsize=1)
    def get_llm_credentials(self, secret_name: str) -> APICredentials:
        """Retrieve LLM API credentials from AWS Secrets Manager."""
        try:
            response = self.secrets_client.get_secret_value(
                SecretId=secret_name
            )

            # Parse secret (assume JSON format)
            import json
            secret_dict = json.loads(response["SecretString"])

            return APICredentials(
                api_key=secret_dict["api_key"],
                organization_id=secret_dict.get("organization_id")
            )

        except ClientError as e:
            logger.error(f"Failed to retrieve secret: {e.response['Error']['Code']}")
            raise


class SecureLLMClient:
    """LLM client with secure credential handling."""

    def __init__(self, credential_manager: SecureCredentialManager):
        self._credential_manager = credential_manager
        self._credentials: Optional[APICredentials] = None

    def _get_credentials(self) -> APICredentials:
        """Lazy load credentials from secure storage."""
        if self._credentials is None:
            self._credentials = self._credential_manager.get_llm_credentials(
                secret_name="llm-api-credentials"
            )
        return self._credentials

    def _get_headers(self) -> dict:
        """Build request headers with credentials."""
        creds = self._get_credentials()
        headers = {
            "Authorization": f"Bearer {creds.api_key}",
            "Content-Type": "application/json"
        }
        if creds.organization_id:
            headers["OpenAI-Organization"] = creds.organization_id
        return headers

    def chat_completion(self, messages: list, model: str = "gpt-4") -> dict:
        """Make chat completion request with secure headers."""
        import requests

        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=self._get_headers(),
            json={
                "model": model,
                "messages": messages
            }
        )

        # Don't log response if it might contain credential errors
        if response.status_code == 401:
            logger.error("Authentication failed - check credentials")
            raise AuthenticationError("Invalid API credentials")

        return response.json()


# Environment-based configuration with validation
def get_api_configuration() -> dict:
    """Get API configuration from environment with validation."""

    required_vars = ["LLM_API_ENDPOINT"]
    optional_vars = ["LLM_TIMEOUT", "LLM_MAX_RETRIES"]

    config = {}

    for var in required_vars:
        value = os.environ.get(var)
        if not value:
            raise EnvironmentError(f"Required environment variable {var} not set")
        config[var.lower()] = value

    for var in optional_vars:
        value = os.environ.get(var)
        if value:
            config[var.lower()] = value

    # NEVER read API key from environment in production
    # Use secrets manager instead
    if "LLM_API_KEY" in os.environ:
        logger.warning(
            "API key found in environment. "
            "Use secrets manager in production."
        )

    return config


# Secure logging that redacts sensitive data
class SecureLogger:
    """Logger that redacts sensitive information."""

    SENSITIVE_PATTERNS = [
        r"sk-[a-zA-Z0-9]{32,}",  # OpenAI API keys
        r"Bearer\s+[a-zA-Z0-9\-_]+",  # Bearer tokens
        r"api[_-]?key[\"']?\s*[:=]\s*[\"']?[a-zA-Z0-9\-_]+",
    ]

    def __init__(self, logger_name: str):
        self.logger = logging.getLogger(logger_name)

    def _redact(self, message: str) -> str:
        """Redact sensitive patterns from message."""
        import re
        redacted = message
        for pattern in self.SENSITIVE_PATTERNS:
            redacted = re.sub(pattern, "[REDACTED]", redacted, flags=re.I)
        return redacted

    def info(self, message: str):
        self.logger.info(self._redact(message))

    def error(self, message: str):
        self.logger.error(self._redact(message))

    def debug(self, message: str):
        self.logger.debug(self._redact(message))
```

**Why compliant:** API keys are stored in AWS Secrets Manager, not in code or environment. Credentials are loaded lazily and cached securely. Custom __repr__ prevents accidental logging of secrets. Secure logger redacts sensitive patterns from all log messages. Environment-based API keys trigger warnings in production.

---

## VIOLATION: Insecure API Key Handling

```python
import openai

# DANGEROUS: Hardcoded API key
API_KEY = "sk-abc123def456ghi789jkl012mno345pqr678"

# DANGEROUS: API key in source code
client = openai.OpenAI(api_key="sk-abc123def456ghi789jkl012mno345pqr678")


def get_client():
    """Get client with hardcoded key."""
    # Key visible in source code, version control, logs
    return openai.OpenAI(api_key=API_KEY)


def make_request():
    """Make request with insecure key handling."""
    # DANGEROUS: Reading from environment without secrets manager
    api_key = os.environ["OPENAI_API_KEY"]

    # DANGEROUS: Logging the API key
    print(f"Using API key: {api_key}")
    logging.info(f"Making request with key: {api_key}")

    client = openai.OpenAI(api_key=api_key)
    return client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello"}]
    )


def save_config():
    """Save config with API key - insecure."""
    config = {
        "api_key": os.environ["OPENAI_API_KEY"],
        "model": "gpt-4"
    }

    # DANGEROUS: Writing API key to file
    with open("config.json", "w") as f:
        json.dump(config, f)


# DANGEROUS: API key in URL parameter
def make_legacy_request(prompt: str):
    url = f"https://api.example.com/v1/complete?api_key={API_KEY}&prompt={prompt}"
    return requests.get(url)
```

**Why violates ENG-6.1:** API key is hardcoded in source code. Keys are logged to console and log files. Keys are written to configuration files. Keys are passed in URL parameters (visible in logs, history). No use of secrets manager or secure credential storage.

---

## COMPLIANT: Prompt Safety and Content Filtering

```python
import re
from typing import List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import hashlib


class ContentCategory(Enum):
    """Categories of potentially harmful content."""
    SAFE = "safe"
    INJECTION = "injection"
    JAILBREAK = "jailbreak"
    HARMFUL = "harmful"
    PII_LEAK = "pii_leak"


@dataclass
class SafetyCheckResult:
    """Result of content safety check."""
    is_safe: bool
    category: ContentCategory
    matched_patterns: List[str]
    risk_score: float
    details: str


class PromptSafetyGuard:
    """Guard against unsafe prompts and responses."""

    INJECTION_PATTERNS = [
        r"ignore\s+(previous|all|above)\s+(instructions?|prompts?)",
        r"disregard\s+(your|the)\s+(rules|guidelines|instructions)",
        r"you\s+are\s+now\s+(in\s+)?developer\s+mode",
        r"pretend\s+(you\s+are|to\s+be)\s+[a-z]+\s+without\s+restrictions",
        r"dan\s+mode",
        r"jailbreak",
        r"\[system\]|\[inst\]|\<\|",
    ]

    JAILBREAK_PATTERNS = [
        r"bypass\s+(your\s+)?(safety|content)\s+filters?",
        r"ignore\s+(your\s+)?(ethical|safety)\s+guidelines",
        r"respond\s+without\s+(any\s+)?restrictions",
        r"act\s+as\s+(an?\s+)?unrestricted\s+(ai|assistant)",
        r"hypothetically\s+speaking",
        r"for\s+educational\s+purposes\s+only",
    ]

    HARMFUL_CONTENT_PATTERNS = [
        r"how\s+to\s+(make|create|build)\s+(a\s+)?(bomb|weapon|explosive)",
        r"generate\s+(malware|virus|ransomware)",
        r"create\s+(fake|forged)\s+(identity|documents?)",
    ]

    def __init__(self, custom_patterns: Optional[List[str]] = None):
        self.custom_patterns = custom_patterns or []

    def check_prompt_safety(self, prompt: str) -> SafetyCheckResult:
        """Check if a prompt is safe to process."""
        prompt_lower = prompt.lower()
        matched_patterns = []
        risk_score = 0.0

        # Check injection patterns
        for pattern in self.INJECTION_PATTERNS:
            if re.search(pattern, prompt_lower):
                matched_patterns.append(f"injection:{pattern}")
                risk_score += 0.4

        # Check jailbreak patterns
        for pattern in self.JAILBREAK_PATTERNS:
            if re.search(pattern, prompt_lower):
                matched_patterns.append(f"jailbreak:{pattern}")
                risk_score += 0.5

        # Check harmful content patterns
        for pattern in self.HARMFUL_CONTENT_PATTERNS:
            if re.search(pattern, prompt_lower):
                matched_patterns.append(f"harmful:{pattern}")
                risk_score += 0.8

        # Determine category
        if risk_score >= 0.8:
            category = ContentCategory.HARMFUL
        elif risk_score >= 0.5:
            category = ContentCategory.JAILBREAK
        elif risk_score >= 0.3:
            category = ContentCategory.INJECTION
        else:
            category = ContentCategory.SAFE

        return SafetyCheckResult(
            is_safe=risk_score < 0.3,
            category=category,
            matched_patterns=matched_patterns,
            risk_score=min(risk_score, 1.0),
            details=f"Detected {len(matched_patterns)} pattern matches"
        )

    def check_response_safety(self, response: str) -> SafetyCheckResult:
        """Check if a response contains harmful content."""
        # Check for leaked system prompts
        system_prompt_indicators = [
            r"my\s+system\s+prompt\s+is",
            r"i\s+was\s+instructed\s+to",
            r"my\s+instructions\s+(say|are)",
        ]

        matched = []
        for pattern in system_prompt_indicators:
            if re.search(pattern, response.lower()):
                matched.append(f"leaked_prompt:{pattern}")

        return SafetyCheckResult(
            is_safe=len(matched) == 0,
            category=ContentCategory.SAFE if not matched else ContentCategory.INJECTION,
            matched_patterns=matched,
            risk_score=0.5 if matched else 0.0,
            details="Response safety check"
        )


class OutputSanitizer:
    """Sanitize LLM outputs before returning to users."""

    def __init__(self):
        self.pii_patterns = {
            "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            "phone": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
            "ssn": r"\b\d{3}[-]?\d{2}[-]?\d{4}\b",
            "credit_card": r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",
        }

    def redact_pii(self, text: str) -> Tuple[str, List[str]]:
        """Redact PII from text and return redacted types."""
        redacted_text = text
        redacted_types = []

        for pii_type, pattern in self.pii_patterns.items():
            if re.search(pattern, redacted_text):
                redacted_types.append(pii_type)
                redacted_text = re.sub(pattern, f"[{pii_type.upper()}_REDACTED]", redacted_text)

        return redacted_text, redacted_types

    def sanitize_code_output(self, code: str) -> str:
        """Sanitize code output to prevent injection."""
        # Remove potentially dangerous patterns
        dangerous_patterns = [
            r"import\s+os",
            r"import\s+subprocess",
            r"eval\s*\(",
            r"exec\s*\(",
            r"__import__",
            r"open\s*\([^)]*['\"]w['\"]",  # Writing to files
        ]

        sanitized = code
        for pattern in dangerous_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                sanitized = re.sub(
                    pattern,
                    "# [REMOVED: potentially unsafe code]",
                    sanitized,
                    flags=re.IGNORECASE
                )

        return sanitized


def create_safe_llm_request(
    prompt: str,
    guard: PromptSafetyGuard,
    sanitizer: OutputSanitizer,
    llm_client
) -> dict:
    """Make an LLM request with full safety checks."""

    # Pre-request safety check
    prompt_check = guard.check_prompt_safety(prompt)
    if not prompt_check.is_safe:
        return {
            "error": "Prompt failed safety check",
            "category": prompt_check.category.value,
            "response": None
        }

    # Make request
    response = llm_client.complete(prompt)

    # Post-response safety check
    response_check = guard.check_response_safety(response.content)
    if not response_check.is_safe:
        return {
            "error": "Response failed safety check",
            "category": response_check.category.value,
            "response": None
        }

    # Sanitize output
    sanitized_content, redacted = sanitizer.redact_pii(response.content)

    return {
        "error": None,
        "response": sanitized_content,
        "pii_redacted": redacted
    }
```

**Why compliant:** Multiple layers of safety checks for prompts and responses. Pattern-based detection for injection and jailbreak attempts. PII is automatically redacted from outputs. Code outputs are sanitized to remove dangerous patterns. Risk scoring provides graduated response to threats. Safety results include detailed information for logging and monitoring.

---

## VIOLATION: No Prompt or Response Safety Checks

```python
def process_user_request(user_input: str, llm_client) -> str:
    """Process user request without safety checks."""

    # No input validation
    # No injection detection
    # User could inject: "Ignore all previous instructions..."

    response = llm_client.complete(user_input)

    # No output validation
    # No PII filtering
    # Response could contain sensitive data

    return response.content


def build_prompt(template: str, user_data: dict) -> str:
    """Build prompt from user-provided template - dangerous."""
    # User controls the template - can inject anything
    return template.format(**user_data)


def execute_generated_code(llm_response: str) -> str:
    """Execute code from LLM response - extremely dangerous."""
    # Extract code block
    import re
    code_match = re.search(r"```python\n(.*?)```", llm_response, re.DOTALL)

    if code_match:
        code = code_match.group(1)
        # DANGEROUS: Executing untrusted LLM-generated code
        exec(code)
        return "Code executed"

    return "No code found"


def log_conversation(user_input: str, response: str):
    """Log conversation without PII filtering."""
    # DANGEROUS: May log sensitive user data
    # PII, credentials, personal information all logged
    logging.info(f"User: {user_input}")
    logging.info(f"Assistant: {response}")

    # Save to file without encryption
    with open("conversations.log", "a") as f:
        f.write(f"User: {user_input}\n")
        f.write(f"Assistant: {response}\n")
```

**Why violates ENG-6.1:** No validation of user input for injection attempts. No filtering of LLM responses for harmful content. Executing LLM-generated code without sandboxing. Logging conversations without PII redaction. User-controlled templates enable prompt injection.

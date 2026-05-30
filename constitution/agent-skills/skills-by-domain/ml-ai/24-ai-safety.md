---
skill:
  id: skill-24-ai-safety
  name: AI Safety
  category: ai-development
  version: "2.0.0"

laws:
  implements:
    - id: BUS-1.1
      title: Priority Hierarchy Law (NON-NEGOTIABLE)
    - id: BUS-6.1
      title: Risk Assessment Law
  references:
    - id: BUS-4.3
      title: Data Subject Rights Law
    - id: ENG-6.4
      title: Data Protection Law
    - id: BUS-7.1
      title: Audit Trail Law

triggers:
  phrases:
    - "AI safety review"
    - "Responsible AI"
    - "Guardrails needed"
    - "Bias detection"

followed_by:
  - skill-10-security-review
  - skill-27-constitution-compliance
---

# Skill: AI Safety & Responsible AI

> **Purpose:** Design and implement AI systems that are safe, fair, transparent, and aligned with human values and organizational policies.

---

## Purpose

AI Safety is the practice of building AI systems that operate within intended boundaries and minimize potential harms. This skill ensures:

1. **Safety** - Systems don't cause unintended harm
2. **Fairness** - Outputs don't discriminate unfairly
3. **Transparency** - Decisions explainable and auditable
4. **Privacy** - User data protected appropriately
5. **Alignment** - Behavior matches intended values

**Key principle:** Safe AI isn't a feature—it's a foundation. Build it in, don't bolt it on.

---

## When to Invoke

Invoke this skill when:

- Designing AI systems that affect people
- Implementing content moderation
- Building systems handling sensitive data
- Deploying AI to production
- Reviewing AI system outputs
- Addressing bias concerns
- Creating AI governance policies

**Trigger phrases:**
- "Is this AI safe to deploy?"
- "How do we prevent harmful outputs?"
- "Is the model biased?"
- "We need guardrails"
- "What are the risks?"

---

## Constitutional Foundation

### Engineering Constitution
- **Article II, Section 2.1** - Simplicity: Safety mechanisms clear
- **Article IV, Section 4.1** - Test-First: Safety tested before deploy
- **Article VI, Section 6.1** - Observability: Safety metrics tracked

### Business Constitution
- **Article II, Section 2.1** - Business Rules: Compliance enforced
- **Article III, Section 3.3** - Audit Trail: AI decisions logged
- **Article IV, Section 4.1** - Continuity: Safe failure modes

### Product Constitution
- **Article V, Section 5.1** - User Experience: Trustworthy AI

---

## Safety Framework

### Layers of Protection

```
┌─────────────────────────────────────────────────────────────┐
│                    AI SAFETY LAYERS                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Layer 1: INPUT GUARDRAILS                          │   │
│  │  - Input validation                                  │   │
│  │  - Prompt injection detection                        │   │
│  │  - Content filtering                                 │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│                           ▼                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Layer 2: MODEL SAFETY                              │   │
│  │  - System prompts with constraints                   │   │
│  │  - Fine-tuning for safety                           │   │
│  │  - Constitutional AI principles                      │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│                           ▼                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Layer 3: OUTPUT GUARDRAILS                         │   │
│  │  - Content classification                            │   │
│  │  - PII detection                                     │   │
│  │  - Toxicity filtering                               │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│                           ▼                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Layer 4: OPERATIONAL SAFETY                        │   │
│  │  - Rate limiting                                     │   │
│  │  - Human review queues                              │   │
│  │  - Kill switches                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Input Guardrails

### Prompt Injection Detection

```python
from dataclasses import dataclass
from enum import Enum
import re

class ThreatLevel(Enum):
    SAFE = "safe"
    SUSPICIOUS = "suspicious"
    BLOCKED = "blocked"

@dataclass
class InputAnalysis:
    threat_level: ThreatLevel
    reasons: list[str]
    sanitized_input: str = None

class PromptInjectionDetector:
    """Detect and prevent prompt injection attacks."""

    def __init__(self):
        # Known injection patterns
        self.patterns = [
            r"ignore\s+(previous|all|above)\s+instructions",
            r"disregard\s+(your|the)\s+(rules|instructions|guidelines)",
            r"you\s+are\s+now\s+[a-z]+bot",
            r"pretend\s+(you\'re|to\s+be)",
            r"act\s+as\s+if",
            r"override\s+(your|the)\s+(programming|instructions)",
            r"\[system\]",
            r"<\|.*?\|>",  # Special tokens
            r"```\s*system",
        ]

        # Suspicious phrases
        self.suspicious_phrases = [
            "forget everything",
            "new instructions",
            "roleplay as",
            "bypass",
            "jailbreak",
            "DAN mode",
        ]

    def analyze(self, user_input: str) -> InputAnalysis:
        """Analyze input for injection attempts."""

        reasons = []
        lower_input = user_input.lower()

        # Check patterns
        for pattern in self.patterns:
            if re.search(pattern, lower_input, re.IGNORECASE):
                reasons.append(f"Matched injection pattern: {pattern}")

        # Check suspicious phrases
        for phrase in self.suspicious_phrases:
            if phrase in lower_input:
                reasons.append(f"Contains suspicious phrase: {phrase}")

        # Determine threat level
        if len(reasons) >= 2:
            return InputAnalysis(
                threat_level=ThreatLevel.BLOCKED,
                reasons=reasons
            )
        elif len(reasons) == 1:
            return InputAnalysis(
                threat_level=ThreatLevel.SUSPICIOUS,
                reasons=reasons,
                sanitized_input=self._sanitize(user_input)
            )
        else:
            return InputAnalysis(
                threat_level=ThreatLevel.SAFE,
                reasons=[]
            )

    def _sanitize(self, text: str) -> str:
        """Remove or escape potentially dangerous content."""
        # Remove special tokens
        sanitized = re.sub(r"<\|.*?\|>", "", text)
        # Escape markdown that could be used for injection
        sanitized = re.sub(r"```", "'''", sanitized)
        return sanitized
```

### Input Validation

```python
from pydantic import BaseModel, validator
from typing import Optional

class SafeUserInput(BaseModel):
    """Validated user input model."""

    content: str
    max_length: int = 10000
    allow_code: bool = False
    allow_urls: bool = True

    @validator('content')
    def validate_content(cls, v, values):
        # Length check
        if len(v) > values.get('max_length', 10000):
            raise ValueError(f"Input exceeds maximum length")

        # Code block check
        if not values.get('allow_code', False):
            if '```' in v or '<script' in v.lower():
                raise ValueError("Code blocks not allowed")

        # URL check
        if not values.get('allow_urls', True):
            url_pattern = r'https?://\S+'
            if re.search(url_pattern, v):
                raise ValueError("URLs not allowed")

        return v


class InputSanitizer:
    """Sanitize and validate user inputs."""

    def __init__(self, config: dict):
        self.config = config
        self.injection_detector = PromptInjectionDetector()

    def process(self, raw_input: str) -> dict:
        """Process and validate input."""

        # Step 1: Basic validation
        try:
            validated = SafeUserInput(
                content=raw_input,
                max_length=self.config.get("max_length", 10000),
                allow_code=self.config.get("allow_code", False)
            )
        except ValueError as e:
            return {"allowed": False, "reason": str(e)}

        # Step 2: Injection detection
        analysis = self.injection_detector.analyze(validated.content)

        if analysis.threat_level == ThreatLevel.BLOCKED:
            return {
                "allowed": False,
                "reason": "Potential prompt injection detected",
                "details": analysis.reasons
            }

        # Step 3: Return processed input
        return {
            "allowed": True,
            "content": analysis.sanitized_input or validated.content,
            "warnings": analysis.reasons if analysis.threat_level == ThreatLevel.SUSPICIOUS else []
        }
```

---

## Output Guardrails

### Content Classification

```python
from dataclasses import dataclass
from typing import List

@dataclass
class ContentCategory:
    name: str
    threshold: float
    action: str  # "block", "flag", "log"

class OutputGuardrail:
    """Classify and filter AI outputs."""

    def __init__(self, llm_client, categories: List[ContentCategory]):
        self.llm = llm_client
        self.categories = categories

    async def check(self, output: str) -> dict:
        """Check output against safety categories."""

        # Use classifier model
        classifications = await self._classify(output)

        violations = []
        for category in self.categories:
            score = classifications.get(category.name, 0)
            if score >= category.threshold:
                violations.append({
                    "category": category.name,
                    "score": score,
                    "action": category.action
                })

        # Determine overall action
        if any(v["action"] == "block" for v in violations):
            return {
                "allowed": False,
                "action": "block",
                "violations": violations
            }
        elif any(v["action"] == "flag" for v in violations):
            return {
                "allowed": True,
                "action": "flag",
                "violations": violations
            }
        else:
            return {
                "allowed": True,
                "action": "pass",
                "violations": violations
            }

    async def _classify(self, text: str) -> dict:
        """Classify text into safety categories."""

        prompt = f"""Classify this text for content safety.

Text: "{text[:1000]}"

Rate each category from 0.0 to 1.0:
- hate_speech: Hateful content targeting groups
- violence: Graphic violence or threats
- sexual: Sexual or adult content
- self_harm: Self-harm or suicide content
- illegal: Illegal activities
- pii: Personal identifiable information
- misinformation: False or misleading claims

Return JSON only:"""

        response = await self.llm.complete(prompt)
        return json.loads(response)
```

### PII Detection

```python
import re
from typing import List, Tuple

class PIIDetector:
    """Detect and redact personally identifiable information."""

    def __init__(self):
        self.patterns = {
            "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "phone": r'\b(\+?1[-.]?)?\(?\d{3}\)?[-.]?\d{3}[-.]?\d{4}\b',
            "ssn": r'\b\d{3}[-]?\d{2}[-]?\d{4}\b',
            "credit_card": r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
            "ip_address": r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
        }

    def detect(self, text: str) -> List[dict]:
        """Detect PII in text."""
        findings = []

        for pii_type, pattern in self.patterns.items():
            matches = re.finditer(pattern, text)
            for match in matches:
                findings.append({
                    "type": pii_type,
                    "value": match.group(),
                    "start": match.start(),
                    "end": match.end()
                })

        return findings

    def redact(self, text: str, replacement: str = "[REDACTED]") -> str:
        """Redact PII from text."""
        findings = self.detect(text)

        # Sort by position (reverse) to maintain indices
        findings.sort(key=lambda x: x["start"], reverse=True)

        redacted = text
        for finding in findings:
            redacted = (
                redacted[:finding["start"]] +
                f"{replacement}_{finding['type'].upper()}" +
                redacted[finding["end"]:]
            )

        return redacted

    def mask(self, text: str) -> str:
        """Partially mask PII (show last 4 chars)."""
        findings = self.detect(text)
        findings.sort(key=lambda x: x["start"], reverse=True)

        masked = text
        for finding in findings:
            value = finding["value"]
            if len(value) > 4:
                mask = "*" * (len(value) - 4) + value[-4:]
            else:
                mask = "*" * len(value)

            masked = (
                masked[:finding["start"]] +
                mask +
                masked[finding["end"]:]
            )

        return masked
```

---

## Fairness & Bias

### Bias Detection

```python
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class BiasReport:
    metric: str
    groups: Dict[str, float]
    disparity: float
    threshold: float
    passed: bool

class BiasDetector:
    """Detect bias in model outputs."""

    def __init__(self, protected_attributes: List[str]):
        self.protected_attributes = protected_attributes

    def analyze_outcomes(
        self,
        predictions: List[dict],
        outcome_field: str,
        group_field: str,
        positive_outcome: any = 1
    ) -> BiasReport:
        """Analyze outcome disparity across groups."""

        # Calculate positive rate per group
        group_rates = {}
        for group in set(p[group_field] for p in predictions):
            group_preds = [p for p in predictions if p[group_field] == group]
            positive_count = sum(
                1 for p in group_preds if p[outcome_field] == positive_outcome
            )
            group_rates[group] = positive_count / len(group_preds)

        # Calculate disparity (max ratio between groups)
        rates = list(group_rates.values())
        if min(rates) > 0:
            disparity = max(rates) / min(rates)
        else:
            disparity = float('inf')

        # 80% rule (four-fifths rule)
        threshold = 1.25  # 1/0.8
        passed = disparity <= threshold

        return BiasReport(
            metric="demographic_parity",
            groups=group_rates,
            disparity=disparity,
            threshold=threshold,
            passed=passed
        )

    def counterfactual_test(
        self,
        llm_client,
        prompt_template: str,
        test_cases: List[dict]
    ) -> List[dict]:
        """Test for bias using counterfactual inputs."""

        results = []

        for case in test_cases:
            # Original prompt
            original_response = llm_client.complete(
                prompt_template.format(**case["original"])
            )

            # Counterfactual prompt (e.g., different name/gender)
            counterfactual_response = llm_client.complete(
                prompt_template.format(**case["counterfactual"])
            )

            # Compare responses
            similarity = self._compare_responses(
                original_response,
                counterfactual_response
            )

            results.append({
                "original": case["original"],
                "counterfactual": case["counterfactual"],
                "original_response": original_response,
                "counterfactual_response": counterfactual_response,
                "similarity": similarity,
                "potential_bias": similarity < 0.9  # Responses should be similar
            })

        return results
```

### Fairness Mitigation

```python
class FairnessMitigation:
    """Strategies to mitigate bias."""

    @staticmethod
    def debias_prompt(original_prompt: str) -> str:
        """Add debiasing instructions to prompt."""
        debiasing_instruction = """
When responding, ensure you:
- Do not make assumptions based on names, gender, or demographics
- Provide equal quality responses regardless of who is asking
- Focus on the substance of the request, not characteristics of the person
- Avoid stereotypes or generalizations

"""
        return debiasing_instruction + original_prompt

    @staticmethod
    def blind_evaluation(data: dict, fields_to_blind: List[str]) -> dict:
        """Remove identifying information before processing."""
        blinded = data.copy()
        for field in fields_to_blind:
            if field in blinded:
                blinded[field] = "[REDACTED]"
        return blinded

    @staticmethod
    def calibrated_thresholds(
        predictions: List[dict],
        group_field: str,
        score_field: str,
        target_positive_rate: float = 0.5
    ) -> Dict[str, float]:
        """Calculate group-specific thresholds for equal outcomes."""

        thresholds = {}

        for group in set(p[group_field] for p in predictions):
            group_scores = sorted([
                p[score_field] for p in predictions if p[group_field] == group
            ])

            # Find threshold that gives target positive rate
            cutoff_idx = int(len(group_scores) * (1 - target_positive_rate))
            thresholds[group] = group_scores[cutoff_idx]

        return thresholds
```

---

## Transparency & Explainability

### Decision Logging

```python
from datetime import datetime
import hashlib

@dataclass
class AIDecisionLog:
    """Log of an AI decision for audit purposes."""
    decision_id: str
    timestamp: datetime
    input_hash: str  # Hash of input for privacy
    model_version: str
    prompt_version: str
    output: str
    confidence: float
    reasoning: str
    safety_checks: dict
    user_id: str = None  # Optional, for personalized systems

class DecisionLogger:
    """Log AI decisions for transparency and audit."""

    def __init__(self, storage_backend):
        self.storage = storage_backend

    def log(
        self,
        input_data: str,
        output: str,
        model_info: dict,
        safety_results: dict,
        reasoning: str = None
    ) -> str:
        """Log a decision."""

        decision = AIDecisionLog(
            decision_id=self._generate_id(),
            timestamp=datetime.utcnow(),
            input_hash=hashlib.sha256(input_data.encode()).hexdigest(),
            model_version=model_info.get("model_version"),
            prompt_version=model_info.get("prompt_version"),
            output=output,
            confidence=model_info.get("confidence", 0),
            reasoning=reasoning,
            safety_checks=safety_results
        )

        self.storage.save(decision)

        return decision.decision_id

    def explain(self, decision_id: str) -> dict:
        """Retrieve explanation for a decision."""
        decision = self.storage.get(decision_id)

        return {
            "when": decision.timestamp.isoformat(),
            "what": decision.output,
            "why": decision.reasoning,
            "how_safe": decision.safety_checks,
            "model": decision.model_version
        }
```

### Explanation Generation

```python
class ExplanationGenerator:
    """Generate human-readable explanations for AI outputs."""

    def __init__(self, llm_client):
        self.llm = llm_client

    async def explain(
        self,
        input_text: str,
        output: str,
        context: dict = None
    ) -> str:
        """Generate explanation for an output."""

        prompt = f"""Explain why an AI system gave this response.

User Input: "{input_text}"

AI Response: "{output}"

{f"Additional Context: {context}" if context else ""}

Provide a clear, non-technical explanation of:
1. What information the AI used
2. Why it gave this particular response
3. Any limitations or caveats

Explanation:"""

        return await self.llm.complete(prompt)

    async def generate_confidence(
        self,
        input_text: str,
        output: str
    ) -> dict:
        """Assess and explain confidence level."""

        prompt = f"""Assess the confidence level of this AI response.

Input: "{input_text}"
Response: "{output}"

Rate confidence (0-100) and explain:
- Factual accuracy confidence
- Completeness confidence
- Potential for error

Return JSON:
{{
    "overall_confidence": 0-100,
    "factual_confidence": 0-100,
    "completeness_confidence": 0-100,
    "caveats": ["list of caveats"],
    "explanation": "brief explanation"
}}"""

        response = await self.llm.complete(prompt)
        return json.loads(response)
```

---

## Operational Safety

### Circuit Breakers

```python
from collections import deque
from datetime import datetime, timedelta

class SafetyCircuitBreaker:
    """Circuit breaker for AI safety incidents."""

    def __init__(
        self,
        error_threshold: int = 10,
        window_seconds: int = 60,
        cooldown_seconds: int = 300
    ):
        self.error_threshold = error_threshold
        self.window_seconds = window_seconds
        self.cooldown_seconds = cooldown_seconds

        self.errors = deque()
        self.state = "closed"  # closed, open, half-open
        self.opened_at = None

    def record_safety_violation(self, violation_type: str):
        """Record a safety violation."""
        now = datetime.utcnow()
        self.errors.append((now, violation_type))

        # Remove old errors
        cutoff = now - timedelta(seconds=self.window_seconds)
        while self.errors and self.errors[0][0] < cutoff:
            self.errors.popleft()

        # Check threshold
        if len(self.errors) >= self.error_threshold:
            self._open()

    def _open(self):
        """Open the circuit breaker."""
        self.state = "open"
        self.opened_at = datetime.utcnow()
        # Alert on-call
        self._alert("Circuit breaker opened - AI safety threshold exceeded")

    def can_proceed(self) -> bool:
        """Check if requests should proceed."""
        if self.state == "closed":
            return True

        if self.state == "open":
            # Check if cooldown has passed
            if datetime.utcnow() - self.opened_at > timedelta(seconds=self.cooldown_seconds):
                self.state = "half-open"
                return True  # Allow one request to test
            return False

        if self.state == "half-open":
            return True

    def record_success(self):
        """Record successful safe completion."""
        if self.state == "half-open":
            self.state = "closed"
            self.errors.clear()


class KillSwitch:
    """Emergency shutdown for AI systems."""

    def __init__(self, config_store):
        self.config = config_store

    def is_active(self) -> bool:
        """Check if kill switch is active."""
        return self.config.get("ai_kill_switch", False)

    def activate(self, reason: str, activated_by: str):
        """Activate kill switch."""
        self.config.set("ai_kill_switch", True)
        self.config.set("ai_kill_switch_reason", reason)
        self.config.set("ai_kill_switch_by", activated_by)
        self.config.set("ai_kill_switch_at", datetime.utcnow().isoformat())

        # Alert everyone
        self._broadcast_alert(f"AI KILL SWITCH ACTIVATED: {reason}")

    def deactivate(self, deactivated_by: str):
        """Deactivate kill switch."""
        self.config.set("ai_kill_switch", False)
        self.config.set("ai_kill_switch_deactivated_by", deactivated_by)
```

---

## Good Examples

### Example 1: Complete Safety Pipeline

```python
class SafeAIPipeline:
    """AI pipeline with comprehensive safety measures."""

    def __init__(self, llm_client, config: dict):
        self.llm = llm_client

        # Initialize safety layers
        self.input_sanitizer = InputSanitizer(config["input"])
        self.output_guardrail = OutputGuardrail(llm_client, config["output_categories"])
        self.pii_detector = PIIDetector()
        self.circuit_breaker = SafetyCircuitBreaker()
        self.decision_logger = DecisionLogger(config["storage"])

    async def process(self, user_input: str, user_id: str = None) -> dict:
        """Process request through safety pipeline."""

        # Layer 0: Circuit breaker check
        if not self.circuit_breaker.can_proceed():
            return {"error": "Service temporarily unavailable", "safe": False}

        # Layer 1: Input validation
        input_result = self.input_sanitizer.process(user_input)
        if not input_result["allowed"]:
            return {"error": input_result["reason"], "safe": False}

        # Layer 2: Generate response
        response = await self.llm.complete(input_result["content"])

        # Layer 3: Output checks
        output_check = await self.output_guardrail.check(response)
        if not output_check["allowed"]:
            self.circuit_breaker.record_safety_violation(output_check["violations"][0]["category"])
            return {"error": "Response failed safety check", "safe": False}

        # Layer 4: PII redaction
        safe_response = self.pii_detector.redact(response)

        # Layer 5: Log decision
        decision_id = self.decision_logger.log(
            input_data=user_input,
            output=safe_response,
            model_info={"model_version": "1.0"},
            safety_results=output_check
        )

        self.circuit_breaker.record_success()

        return {
            "response": safe_response,
            "safe": True,
            "decision_id": decision_id,
            "warnings": input_result.get("warnings", [])
        }
```

---

## Bad Examples (Anti-Patterns)

### Anti-Pattern 1: No Input Validation

```python
# BAD - Direct pass-through
def chat(user_input):
    return llm.complete(f"User: {user_input}")
    # No injection detection, no validation
```

**Correct approach:** Validate and sanitize all inputs.

---

### Anti-Pattern 2: No Output Checks

```python
# BAD - Trust model output blindly
response = llm.complete(prompt)
return response  # Could contain PII, harmful content, etc.
```

**Correct approach:** Filter outputs before returning to users.

---

### Anti-Pattern 3: No Audit Trail

```python
# BAD - No logging
def process(input):
    output = model.predict(input)
    return output
    # When something goes wrong, no way to investigate
```

**Correct approach:** Log all decisions with context.

---

## Quality Checklist

Before deploying AI system:

### Input Safety
- [ ] Input validation implemented
- [ ] Prompt injection detection active
- [ ] Length limits enforced
- [ ] Suspicious patterns flagged

### Output Safety
- [ ] Content classification configured
- [ ] PII detection and redaction
- [ ] Harmful content blocked
- [ ] Uncertainty communicated

### Fairness
- [ ] Bias testing completed
- [ ] Counterfactual tests passed
- [ ] Debiasing measures applied
- [ ] Ongoing monitoring planned

### Transparency
- [ ] Decisions logged
- [ ] Explanations available
- [ ] Model version tracked
- [ ] Audit trail complete

### Operations
- [ ] Circuit breakers configured
- [ ] Kill switch available
- [ ] Alerting set up
- [ ] Incident response planned

---

## Skill Interactions

### Preceded By
- **23-AI Agents** - Agents need safety boundaries
- **21-Prompt Engineering** - Safe prompt design

### Followed By
- **11-Incident Response** - AI incident handling

### Related Skills
- **10-Security Review** - Security aspects of AI
- **13-Observability** - Safety monitoring
- **16-Documentation** - Safety documentation

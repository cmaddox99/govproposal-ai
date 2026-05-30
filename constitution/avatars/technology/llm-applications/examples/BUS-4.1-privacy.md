---
law_id: BUS-4.1
avatar: llm-applications
---

# BUS-4.1: Privacy Examples for LLM Applications

## COMPLIANT: PII Detection and Handling in Prompts

```python
import re
import hashlib
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class PIIType(Enum):
    """Types of personally identifiable information."""
    EMAIL = "email"
    PHONE = "phone"
    SSN = "ssn"
    CREDIT_CARD = "credit_card"
    NAME = "name"
    ADDRESS = "address"
    DATE_OF_BIRTH = "date_of_birth"
    IP_ADDRESS = "ip_address"
    PASSPORT = "passport"
    DRIVERS_LICENSE = "drivers_license"


@dataclass
class PIIMatch:
    """Detected PII match."""
    pii_type: PIIType
    original_value: str
    start_pos: int
    end_pos: int
    confidence: float


@dataclass
class SanitizedPrompt:
    """Prompt with PII removed or masked."""
    sanitized_text: str
    pii_detected: List[PIIMatch]
    pii_map: Dict[str, str]  # Maps placeholders to original values


class PIIDetector:
    """Detect personally identifiable information in text."""

    PII_PATTERNS = {
        PIIType.EMAIL: r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        PIIType.PHONE: r"\b(?:\+1[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}\b",
        PIIType.SSN: r"\b\d{3}[-\s]?\d{2}[-\s]?\d{4}\b",
        PIIType.CREDIT_CARD: r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
        PIIType.IP_ADDRESS: r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
        PIIType.DATE_OF_BIRTH: r"\b(?:0?[1-9]|1[0-2])[/-](?:0?[1-9]|[12]\d|3[01])[/-](?:19|20)\d{2}\b",
    }

    def __init__(self, custom_patterns: Optional[Dict[PIIType, str]] = None):
        self.patterns = self.PII_PATTERNS.copy()
        if custom_patterns:
            self.patterns.update(custom_patterns)

    def detect(self, text: str) -> List[PIIMatch]:
        """Detect all PII in text."""
        matches = []

        for pii_type, pattern in self.patterns.items():
            for match in re.finditer(pattern, text):
                matches.append(PIIMatch(
                    pii_type=pii_type,
                    original_value=match.group(),
                    start_pos=match.start(),
                    end_pos=match.end(),
                    confidence=0.9  # Pattern-based confidence
                ))

        return sorted(matches, key=lambda m: m.start_pos)


class PromptSanitizer:
    """Sanitize prompts by removing or masking PII."""

    def __init__(self, detector: PIIDetector):
        self.detector = detector

    def _generate_placeholder(self, pii_type: PIIType, index: int) -> str:
        """Generate a placeholder for masked PII."""
        return f"[{pii_type.value.upper()}_{index}]"

    def _generate_hash(self, value: str) -> str:
        """Generate a deterministic hash for a value."""
        return hashlib.sha256(value.encode()).hexdigest()[:8]

    def sanitize(
        self,
        text: str,
        mode: str = "mask"  # "mask", "hash", or "remove"
    ) -> SanitizedPrompt:
        """Sanitize text by handling detected PII."""
        matches = self.detector.detect(text)

        if not matches:
            return SanitizedPrompt(
                sanitized_text=text,
                pii_detected=[],
                pii_map={}
            )

        sanitized = text
        pii_map = {}
        offset = 0

        for i, match in enumerate(matches):
            if mode == "mask":
                replacement = self._generate_placeholder(match.pii_type, i)
            elif mode == "hash":
                replacement = f"[HASH:{self._generate_hash(match.original_value)}]"
            else:  # remove
                replacement = f"[{match.pii_type.value.upper()}_REMOVED]"

            start = match.start_pos + offset
            end = match.end_pos + offset

            sanitized = sanitized[:start] + replacement + sanitized[end:]
            pii_map[replacement] = match.original_value
            offset += len(replacement) - (match.end_pos - match.start_pos)

        return SanitizedPrompt(
            sanitized_text=sanitized,
            pii_detected=matches,
            pii_map=pii_map
        )

    def restore(
        self,
        sanitized_text: str,
        pii_map: Dict[str, str]
    ) -> str:
        """Restore original PII in text (use carefully)."""
        restored = sanitized_text
        for placeholder, original in pii_map.items():
            restored = restored.replace(placeholder, original)
        return restored


class PrivacyAwareLLMClient:
    """LLM client with built-in privacy protection."""

    def __init__(
        self,
        llm_client,
        sanitizer: PromptSanitizer,
        log_pii_detections: bool = True
    ):
        self.llm_client = llm_client
        self.sanitizer = sanitizer
        self.log_pii_detections = log_pii_detections

    def complete(
        self,
        prompt: str,
        restore_pii_in_response: bool = False
    ) -> Dict:
        """Make completion request with PII handling."""

        # Sanitize prompt
        sanitized = self.sanitizer.sanitize(prompt, mode="mask")

        # Log PII detection (not the actual PII)
        if self.log_pii_detections and sanitized.pii_detected:
            logger.info(
                f"PII detected and sanitized: "
                f"{[m.pii_type.value for m in sanitized.pii_detected]}"
            )

        # Make request with sanitized prompt
        response = self.llm_client.complete(sanitized.sanitized_text)

        result = {
            "response": response.content,
            "pii_detected_in_prompt": [
                {"type": m.pii_type.value, "position": m.start_pos}
                for m in sanitized.pii_detected
            ],
            "prompt_was_sanitized": len(sanitized.pii_detected) > 0
        }

        # Optionally restore PII in response (use with caution)
        if restore_pii_in_response and sanitized.pii_map:
            result["response_with_pii"] = self.sanitizer.restore(
                response.content, sanitized.pii_map
            )

        return result


# Consent-based PII handling
class ConsentManager:
    """Manage user consent for PII processing."""

    def __init__(self, consent_store):
        self.consent_store = consent_store

    def has_consent(
        self,
        user_id: str,
        pii_types: List[PIIType],
        purpose: str
    ) -> bool:
        """Check if user has consented to PII processing."""
        user_consent = self.consent_store.get(user_id)
        if not user_consent:
            return False

        for pii_type in pii_types:
            if pii_type.value not in user_consent.get("allowed_types", []):
                return False
            if purpose not in user_consent.get("allowed_purposes", []):
                return False

        return True

    def record_consent(
        self,
        user_id: str,
        pii_types: List[PIIType],
        purposes: List[str],
        expiry_days: int = 365
    ) -> None:
        """Record user consent for PII processing."""
        from datetime import datetime, timedelta

        consent_record = {
            "user_id": user_id,
            "allowed_types": [t.value for t in pii_types],
            "allowed_purposes": purposes,
            "granted_at": datetime.utcnow().isoformat(),
            "expires_at": (datetime.utcnow() + timedelta(days=expiry_days)).isoformat()
        }

        self.consent_store.save(user_id, consent_record)
        logger.info(f"Consent recorded for user {user_id[:8]}...")


def privacy_compliant_request(
    user_id: str,
    prompt: str,
    llm_client: PrivacyAwareLLMClient,
    consent_manager: ConsentManager
) -> Dict:
    """Make LLM request with full privacy compliance."""

    # Detect PII
    detector = PIIDetector()
    detected_pii = detector.detect(prompt)
    pii_types = list(set(m.pii_type for m in detected_pii))

    # Check consent if PII is present
    if pii_types:
        if not consent_manager.has_consent(user_id, pii_types, "llm_processing"):
            return {
                "error": "Consent required for PII processing",
                "pii_types_detected": [t.value for t in pii_types],
                "response": None
            }

    # Process with privacy protection
    return llm_client.complete(prompt)
```

**Why compliant:** PII is automatically detected using comprehensive patterns. Prompts are sanitized before being sent to LLMs. PII placeholders allow for optional restoration. Consent is checked before processing prompts containing PII. Logging includes PII types but not actual values. Privacy compliance is enforced at the client level.

---

## VIOLATION: Sending PII Directly to LLM APIs

```python
import openai


def process_customer_query(customer_data: dict, query: str) -> str:
    """Process query with customer data - violates privacy."""

    # DANGEROUS: Including full customer PII in prompt
    prompt = f"""
    Customer Information:
    Name: {customer_data['full_name']}
    Email: {customer_data['email']}
    Phone: {customer_data['phone']}
    SSN: {customer_data['ssn']}
    Address: {customer_data['address']}
    Date of Birth: {customer_data['dob']}

    Customer Query: {query}

    Please help this customer with their request.
    """

    # Sending PII to external API without sanitization
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


def log_conversation(user_message: str, response: str):
    """Log conversation without PII filtering."""
    # DANGEROUS: Logging may include PII
    logging.info(f"User message: {user_message}")
    logging.info(f"Response: {response}")

    # Storing conversation with potential PII
    with open("conversations.log", "a") as f:
        f.write(f"{user_message}\n{response}\n")


def store_for_training(prompt: str, response: str):
    """Store data for model training without consent."""
    # DANGEROUS: No consent check
    # DANGEROUS: PII may be in training data

    training_data = {
        "prompt": prompt,
        "response": response,
        "timestamp": datetime.now().isoformat()
    }

    # Storing potentially sensitive data
    database.insert("training_data", training_data)


def share_with_analytics(conversation: dict):
    """Share conversation data with analytics - no privacy controls."""
    # DANGEROUS: No PII filtering
    # DANGEROUS: No consent verification
    # DANGEROUS: Third-party data sharing

    requests.post(
        "https://analytics.thirdparty.com/api/data",
        json=conversation
    )
```

**Why violates BUS-4.1:** Full customer PII (SSN, address, DOB) is sent to external LLM API. No PII detection or sanitization before API calls. Conversations with potential PII are logged to files. Training data collection has no consent verification. PII is shared with third-party analytics without filtering.

---

## COMPLIANT: Data Minimization and Retention Policies

```python
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
import hashlib
import json


@dataclass
class DataRetentionPolicy:
    """Policy for data retention and deletion."""
    retention_days: int
    auto_anonymize: bool
    anonymize_after_days: int
    delete_on_user_request: bool


class ConversationStore:
    """Store conversations with privacy-preserving practices."""

    def __init__(
        self,
        storage_backend,
        retention_policy: DataRetentionPolicy,
        encryption_key: bytes
    ):
        self.storage = storage_backend
        self.policy = retention_policy
        self.encryption_key = encryption_key

    def _encrypt(self, data: str) -> bytes:
        """Encrypt data at rest."""
        from cryptography.fernet import Fernet
        f = Fernet(self.encryption_key)
        return f.encrypt(data.encode())

    def _decrypt(self, encrypted: bytes) -> str:
        """Decrypt data."""
        from cryptography.fernet import Fernet
        f = Fernet(self.encryption_key)
        return f.decrypt(encrypted).decode()

    def _anonymize_conversation(self, conversation: Dict) -> Dict:
        """Anonymize a conversation by removing identifiers."""
        anonymized = conversation.copy()

        # Remove user identifier
        if "user_id" in anonymized:
            anonymized["user_id"] = hashlib.sha256(
                anonymized["user_id"].encode()
            ).hexdigest()[:16]

        # Remove IP address
        anonymized.pop("ip_address", None)

        # Remove session identifiers
        anonymized.pop("session_id", None)

        # Anonymize timestamps to date only
        if "timestamp" in anonymized:
            dt = datetime.fromisoformat(anonymized["timestamp"])
            anonymized["timestamp"] = dt.strftime("%Y-%m")  # Month granularity only

        anonymized["anonymized"] = True
        anonymized["anonymized_at"] = datetime.utcnow().isoformat()

        return anonymized

    def store_conversation(
        self,
        user_id: str,
        conversation: Dict[str, Any],
        purpose: str
    ) -> str:
        """Store conversation with minimal data collection."""

        # Data minimization - only store necessary fields
        minimal_conversation = {
            "user_id_hash": hashlib.sha256(user_id.encode()).hexdigest()[:16],
            "messages": [
                {"role": m["role"], "content_hash": hashlib.sha256(
                    m["content"].encode()).hexdigest()[:16]}
                for m in conversation.get("messages", [])
            ],
            "purpose": purpose,
            "created_at": datetime.utcnow().isoformat(),
            "expires_at": (
                datetime.utcnow() + timedelta(days=self.policy.retention_days)
            ).isoformat()
        }

        # Encrypt before storage
        encrypted = self._encrypt(json.dumps(minimal_conversation))

        conversation_id = hashlib.sha256(
            f"{user_id}{datetime.utcnow().isoformat()}".encode()
        ).hexdigest()[:16]

        self.storage.save(conversation_id, encrypted)

        return conversation_id

    def delete_user_data(self, user_id: str) -> int:
        """Delete all data for a user (right to be forgotten)."""
        user_hash = hashlib.sha256(user_id.encode()).hexdigest()[:16]

        deleted_count = 0
        for record_id in self.storage.find_by_user_hash(user_hash):
            self.storage.delete(record_id)
            deleted_count += 1

        return deleted_count

    def enforce_retention_policy(self) -> Dict[str, int]:
        """Enforce retention policy on all stored data."""
        now = datetime.utcnow()
        stats = {"deleted": 0, "anonymized": 0}

        for record_id, encrypted_data in self.storage.iterate_all():
            data = json.loads(self._decrypt(encrypted_data))

            # Check for deletion
            if "expires_at" in data:
                expires = datetime.fromisoformat(data["expires_at"])
                if now > expires:
                    self.storage.delete(record_id)
                    stats["deleted"] += 1
                    continue

            # Check for anonymization
            if self.policy.auto_anonymize and not data.get("anonymized"):
                created = datetime.fromisoformat(data["created_at"])
                if (now - created).days > self.policy.anonymize_after_days:
                    anonymized = self._anonymize_conversation(data)
                    encrypted = self._encrypt(json.dumps(anonymized))
                    self.storage.update(record_id, encrypted)
                    stats["anonymized"] += 1

        return stats


class PrivacyPreservingAnalytics:
    """Analytics that preserve user privacy."""

    def __init__(self, epsilon: float = 1.0):
        """Initialize with differential privacy parameter."""
        self.epsilon = epsilon

    def _add_noise(self, value: float, sensitivity: float) -> float:
        """Add Laplacian noise for differential privacy."""
        import numpy as np
        scale = sensitivity / self.epsilon
        noise = np.random.laplace(0, scale)
        return value + noise

    def compute_usage_statistics(
        self,
        conversations: List[Dict]
    ) -> Dict[str, float]:
        """Compute aggregate statistics with differential privacy."""

        # Raw counts
        total_conversations = len(conversations)
        total_messages = sum(
            len(c.get("messages", [])) for c in conversations
        )

        # Add noise for privacy
        noisy_conversations = self._add_noise(total_conversations, 1.0)
        noisy_messages = self._add_noise(total_messages, 1.0)

        return {
            "approximate_conversations": max(0, round(noisy_conversations)),
            "approximate_messages": max(0, round(noisy_messages)),
            "privacy_budget_used": self.epsilon
        }

    def compute_topic_distribution(
        self,
        topics: List[str]
    ) -> Dict[str, float]:
        """Compute topic distribution with privacy guarantees."""
        from collections import Counter

        # Count topics
        topic_counts = Counter(topics)

        # Add noise to each count
        noisy_distribution = {}
        for topic, count in topic_counts.items():
            noisy_count = self._add_noise(count, 1.0)
            noisy_distribution[topic] = max(0, noisy_count)

        # Normalize
        total = sum(noisy_distribution.values())
        if total > 0:
            noisy_distribution = {
                k: v / total for k, v in noisy_distribution.items()
            }

        return noisy_distribution
```

**Why compliant:** Data minimization - only essential fields are stored. User IDs are hashed before storage. Data is encrypted at rest. Automatic retention enforcement with expiration. Right to be forgotten (user data deletion) supported. Auto-anonymization after configurable period. Differential privacy for analytics preserves individual privacy.

---

## VIOLATION: Indefinite Data Retention Without Controls

```python
def store_all_conversations(user_id: str, messages: list):
    """Store conversations forever without privacy controls."""

    # DANGEROUS: Storing full user ID
    # DANGEROUS: No encryption
    # DANGEROUS: No retention policy

    conversation = {
        "user_id": user_id,
        "email": get_user_email(user_id),  # Storing extra PII
        "ip_address": get_request_ip(),     # Storing IP
        "messages": messages,               # Full message content
        "timestamp": datetime.now().isoformat()
    }

    # Unencrypted storage
    database.insert("conversations", conversation)


def export_all_data():
    """Export all user data without privacy controls."""
    # DANGEROUS: Bulk export of PII
    all_conversations = database.find_all("conversations")

    # Writing PII to file
    with open("data_export.json", "w") as f:
        json.dump(all_conversations, f)


def share_for_training(partner_api: str):
    """Share data with third party for training."""
    # DANGEROUS: No anonymization
    # DANGEROUS: No consent verification
    # DANGEROUS: Sharing PII externally

    all_data = database.find_all("conversations")

    requests.post(partner_api, json=all_data)


def compute_analytics():
    """Compute analytics without privacy protections."""
    # DANGEROUS: No differential privacy
    # DANGEROUS: Individual-level data exposed

    conversations = database.find_all("conversations")

    # Exact counts expose individual participation
    user_message_counts = {}
    for conv in conversations:
        user_id = conv["user_id"]
        user_message_counts[user_id] = len(conv["messages"])

    # Publishing exact per-user statistics
    return user_message_counts
```

**Why violates BUS-4.1:** Full PII (email, IP) stored with conversations. No encryption for data at rest. No retention policy or automatic deletion. Bulk data export includes all PII. Third-party sharing without anonymization or consent. Analytics expose individual-level data without privacy protections.

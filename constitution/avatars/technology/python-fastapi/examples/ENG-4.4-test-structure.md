---
law_id: ENG-4.4
avatar: python-fastapi
---

# ENG-4.4: Test Structure (Given-When-Then) Examples for Python/FastAPI

## COMPLIANT: Clear Structure with pytest

```python
import pytest
from unittest.mock import Mock, patch


class TestGradAuditService:

    def test_publish_with_all_credits_earned_creates_published_record(self):
        # GIVEN - Setup preconditions
        learner = LearnerFixture.with_completed_credits()
        grad_audit = GradAuditFixture.for_learner(learner)
        repository = Mock(spec=GradAuditRepository)
        repository.find_by_id.return_value = grad_audit
        service = GradAuditService(repository=repository)

        # WHEN - Execute the action
        result = service.publish(grad_audit.id)

        # THEN - Verify outcomes
        assert result.status == AuditStatus.PUBLISHED
        assert result.published_at is not None
        repository.save.assert_called_once()
        saved_audit = repository.save.call_args[0][0]
        assert saved_audit.status == AuditStatus.PUBLISHED


    def test_publish_with_missing_credits_raises_error(self):
        # GIVEN
        grad_audit = GradAuditFixture.with_incomplete_credits()
        repository = Mock(spec=GradAuditRepository)
        repository.find_by_id.return_value = grad_audit
        service = GradAuditService(repository=repository)

        # WHEN / THEN - Expect exception
        with pytest.raises(IncompleteCreditError) as exc_info:
            service.publish(grad_audit.id)

        assert "Cannot publish audit with incomplete credits" in str(exc_info.value)
```

**Why compliant:** Clear separation of setup, action, and verification. Each section is visually distinct with comments.

---

## VIOLATION: Unclear Structure

```python
def test_publish():
    # Mixed setup and assertions, no clear structure
    audit = GradAudit()
    audit.id = uuid4()
    audit.status = "DRAFT"
    service.publish(audit.id)
    assert audit is not None
    assert audit.status is not None
    # What is being tested? Hard to tell.
```

**Why violates ENG-4.4:**
- No clear sections
- Assertions are vague
- Hard to understand what behavior is being tested

---

## Test Naming Convention

### COMPLIANT Names

```python
def test_calculate_credits_with_completed_courses_returns_sum_of_credits(): ...
def test_validate_email_with_invalid_format_raises_validation_error(): ...
def test_sync_learner_when_powerschool_unavailable_returns_failure_result(): ...
def test_create_order_with_insufficient_inventory_returns_backorder_status(): ...
```

**Pattern:** `test_[action]_with_[condition]_[expected_outcome]()`

### VIOLATION Names

```python
def test_calculate(): ...           # What does it test?
def test_1(): ...                    # Meaningless
def test_should_work(): ...          # Vague
def test_it_works(): ...             # Even more vague
def test_create_order_happy_path(): ... # "Happy path" isn't specific
```

---

## Async Test Structure

```python
@pytest.mark.asyncio
class TestOrderAPI:

    async def test_create_order_with_valid_items_returns_201(self, client: AsyncClient):
        # GIVEN
        payload = {
            "customer_id": str(uuid4()),
            "items": [
                {"product_id": str(uuid4()), "quantity": 2}
            ]
        }

        # WHEN
        response = await client.post("/orders", json=payload)

        # THEN
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["status"] == "DRAFT"
```

---
law_id: ENG-4.1
avatar: streaming-ml
---

# ENG-4.1: Atomic TDD Examples for Streaming ML

## COMPLIANT: TDD Cycle with pytest for Stream Processing

```python
# test_stream_processor.py

# Step 1: RED - Write failing test
def test_processor_enriches_event_with_features():
    # GIVEN
    feature_store = InMemoryFeatureStore({
        "user:123": {"avg_order_value": 45.50, "order_count": 12}
    })
    processor = StreamProcessor(feature_store=feature_store)
    event = PurchaseEvent(user_id="user:123", amount=50.00)

    # WHEN
    enriched = processor.enrich(event)

    # THEN
    assert enriched.features["avg_order_value"] == 45.50
    assert enriched.features["order_count"] == 12


# Step 2: GREEN - Write minimum code (in stream_processor.py)
@dataclass
class EnrichedEvent:
    event: PurchaseEvent
    features: dict

class StreamProcessor:
    def __init__(self, feature_store: FeatureStore):
        self._features = feature_store

    def enrich(self, event: PurchaseEvent) -> EnrichedEvent:
        features = self._features.get_online_features(event.user_id)
        return EnrichedEvent(event=event, features=features)


# Step 3: REFACTOR - Add feature vector abstraction
@dataclass(frozen=True)
class FeatureVector:
    user_id: str
    features: dict
    retrieved_at: datetime

class StreamProcessor:
    def enrich(self, event: PurchaseEvent) -> EnrichedEvent:
        vector = self._features.get_feature_vector(
            entity_id=event.user_id,
            feature_names=["avg_order_value", "order_count"]
        )
        return EnrichedEvent(event=event, features=vector.features)


# Step 4: Commit, then write NEXT test
def test_processor_handles_missing_features_gracefully():
    # Next TDD cycle for missing feature handling...
    pass
```

**Why compliant:** One test at a time, minimal code to pass, refactor continuously.

---

## VIOLATION: Testing with Live Kafka/Redis

```python
# BAD: Tests that require running infrastructure
import pytest
from kafka import KafkaProducer, KafkaConsumer

def test_full_streaming_pipeline():
    # VIOLATION: Requires running Kafka cluster
    producer = KafkaProducer(bootstrap_servers="localhost:9092")
    consumer = KafkaConsumer("predictions", bootstrap_servers="localhost:9092")

    # VIOLATION: Requires running Redis for features
    redis = Redis(host="localhost", port=6379)
    redis.hset("user:123", mapping={"score": "0.85"})

    # VIOLATION: Tests multiple components at once
    producer.send("events", value=b'{"user_id": "123", "action": "click"}')

    # VIOLATION: Flaky timing-dependent assertion
    time.sleep(2)  # Wait for processing

    # VIOLATION: Depends on external state
    messages = list(consumer)
    assert len(messages) == 1
    assert json.loads(messages[0].value)["prediction"] > 0.8


# BAD: Integration test without isolation
@pytest.mark.asyncio
async def test_feature_materialization():
    # VIOLATION: Runs actual Flink job
    flink_env = StreamExecutionEnvironment.get_execution_environment()

    # VIOLATION: Writes to actual feature store
    feast_client = FeatureStore(repo_path="./feast_repo")

    # VIOLATION: Non-deterministic batch processing
    await materialize_features(
        flink_env,
        feast_client,
        start_date=datetime.now() - timedelta(days=1)
    )

    # Assertions depend on actual data
    features = feast_client.get_online_features(...)
```

**Why violates ENG-4.1:** Tests multiple components together, requires live infrastructure, timing-dependent, non-deterministic results.

---

## TDD Cycle Commands for Streaming ML

```bash
# RED: Run test, see it fail
pytest tests/streaming/test_processor.py::test_processor_enriches_event -v

# GREEN: Write code, run test again
pytest tests/streaming/test_processor.py::test_processor_enriches_event -v

# REFACTOR: Run all unit tests
pytest tests/ -m "not integration" -v

# Integration tests (separate from TDD, with infrastructure)
docker-compose up -d kafka redis
pytest tests/integration/ --run-kafka -v

# VERIFY: Check coverage and constitutional compliance
pytest --cov=src --cov-fail-under=80
constitution-lint .

# Commit when green and compliant
git add -A && git commit -m "Add feature enrichment to StreamProcessor"
```

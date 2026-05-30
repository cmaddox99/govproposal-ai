# Streaming ML Guidance

> **Purpose:** Stack-specific agent behaviors for real-time ML with streaming data (Kafka, Flink, Feature Stores).

---

## Overview

This guidance provides patterns for AI agents working with real-time ML systems including streaming inference, online feature stores, and event-driven ML pipelines.

---

## Testing Framework

**Primary Framework:** pytest + pytest-kafka + feast (feature store testing)

### Test Structure

```python
import pytest
from unittest.mock import MagicMock, AsyncMock
from datetime import datetime, timedelta
from myproject.streaming.processor import StreamProcessor
from myproject.features.online_store import OnlineFeatureStore
from myproject.inference.realtime import RealtimePredictor


class TestStreamProcessor:
    """Tests for stream processing."""

    @pytest.fixture
    def mock_consumer(self):
        """Mock Kafka consumer."""
        mock = MagicMock()
        mock.__iter__ = lambda self: iter([
            MagicMock(value=b'{"user_id": "123", "event": "click"}'),
            MagicMock(value=b'{"user_id": "456", "event": "purchase"}'),
        ])
        return mock

    @pytest.fixture
    def mock_producer(self):
        """Mock Kafka producer."""
        return MagicMock()

    @pytest.fixture
    def processor(self, mock_consumer, mock_producer):
        """Stream processor with mocks."""
        return StreamProcessor(
            consumer=mock_consumer,
            producer=mock_producer
        )

    def test_processor_consumes_events(self, processor, mock_consumer):
        """Processor should consume events from Kafka."""
        # Act
        events = list(processor.consume(max_messages=2))

        # Assert
        assert len(events) == 2

    def test_processor_transforms_events(self, processor):
        """Processor should transform events correctly."""
        # Arrange
        event = {"user_id": "123", "event": "click", "timestamp": "2024-01-15T10:00:00"}

        # Act
        transformed = processor.transform(event)

        # Assert
        assert "features" in transformed
        assert "user_id" in transformed

    def test_processor_produces_results(self, processor, mock_producer):
        """Processor should produce results to output topic."""
        # Arrange
        result = {"user_id": "123", "prediction": 0.85}

        # Act
        processor.produce(result, topic="predictions")

        # Assert
        mock_producer.send.assert_called_once()


class TestOnlineFeatureStore:
    """Tests for online feature store."""

    @pytest.fixture
    def mock_redis(self):
        """Mock Redis client."""
        mock = MagicMock()
        mock.hgetall.return_value = {
            b"total_purchases": b"5",
            b"avg_order_value": b"99.50",
            b"last_activity_days": b"3"
        }
        return mock

    @pytest.fixture
    def feature_store(self, mock_redis):
        """Online feature store with mock."""
        return OnlineFeatureStore(redis_client=mock_redis)

    def test_store_retrieves_features(self, feature_store, mock_redis):
        """Feature store should retrieve user features."""
        # Act
        features = feature_store.get_features(
            entity_id="user_123",
            feature_names=["total_purchases", "avg_order_value"]
        )

        # Assert
        assert features["total_purchases"] == 5
        assert features["avg_order_value"] == 99.50

    def test_store_handles_missing_features(self, feature_store, mock_redis):
        """Feature store should handle missing features."""
        # Arrange
        mock_redis.hgetall.return_value = {}

        # Act
        features = feature_store.get_features(
            entity_id="unknown_user",
            feature_names=["total_purchases"]
        )

        # Assert
        assert features.get("total_purchases") is None or features.get("total_purchases") == 0

    def test_store_writes_features(self, feature_store, mock_redis):
        """Feature store should write features."""
        # Arrange
        features = {"total_purchases": 6, "last_activity_days": 0}

        # Act
        feature_store.set_features(entity_id="user_123", features=features)

        # Assert
        mock_redis.hset.assert_called()


class TestRealtimePredictor:
    """Tests for real-time inference."""

    @pytest.fixture
    def mock_model(self):
        """Mock ML model."""
        mock = MagicMock()
        mock.predict.return_value = [[0.85, 0.15]]
        return mock

    @pytest.fixture
    def mock_feature_store(self):
        """Mock feature store."""
        mock = MagicMock()
        mock.get_features.return_value = {
            "total_purchases": 5,
            "avg_order_value": 99.50
        }
        return mock

    @pytest.fixture
    def predictor(self, mock_model, mock_feature_store):
        """Real-time predictor with mocks."""
        return RealtimePredictor(
            model=mock_model,
            feature_store=mock_feature_store
        )

    def test_predictor_fetches_features(self, predictor, mock_feature_store):
        """Predictor should fetch features from store."""
        # Act
        predictor.predict(entity_id="user_123")

        # Assert
        mock_feature_store.get_features.assert_called_with(
            entity_id="user_123",
            feature_names=predictor.feature_names
        )

    def test_predictor_returns_prediction(self, predictor):
        """Predictor should return prediction."""
        # Act
        result = predictor.predict(entity_id="user_123")

        # Assert
        assert "prediction" in result
        assert "probability" in result
        assert result["probability"] == 0.85

    def test_predictor_meets_latency_slo(self, predictor):
        """Predictor should meet latency SLO."""
        import time

        # Act
        start = time.time()
        predictor.predict(entity_id="user_123")
        latency_ms = (time.time() - start) * 1000

        # Assert (50ms SLO for mocked test)
        assert latency_ms < 50
```

---

## Common Patterns

### Good Patterns

**Stream Processor:**

```python
from kafka import KafkaConsumer, KafkaProducer
from typing import Iterator, Dict, Any, Callable
import json
from dataclasses import dataclass

@dataclass
class StreamConfig:
    bootstrap_servers: str
    input_topic: str
    output_topic: str
    group_id: str
    auto_offset_reset: str = "latest"

class StreamProcessor:
    """Kafka stream processor for ML events."""

    def __init__(
        self,
        config: StreamConfig,
        transform_fn: Callable[[Dict], Dict] = None,
        feature_store = None,
        predictor = None
    ):
        self.config = config
        self.transform_fn = transform_fn
        self.feature_store = feature_store
        self.predictor = predictor

        self.consumer = KafkaConsumer(
            config.input_topic,
            bootstrap_servers=config.bootstrap_servers,
            group_id=config.group_id,
            auto_offset_reset=config.auto_offset_reset,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

        self.producer = KafkaProducer(
            bootstrap_servers=config.bootstrap_servers,
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )

    def process(self):
        """Main processing loop."""
        for message in self.consumer:
            try:
                event = message.value

                # Transform event
                if self.transform_fn:
                    event = self.transform_fn(event)

                # Enrich with features
                if self.feature_store:
                    features = self.feature_store.get_features(
                        entity_id=event.get("entity_id"),
                        feature_names=self.feature_names
                    )
                    event["features"] = features

                # Generate prediction
                if self.predictor:
                    prediction = self.predictor.predict(event["features"])
                    event["prediction"] = prediction

                # Produce result
                self.producer.send(
                    self.config.output_topic,
                    value=event
                )

            except Exception as e:
                self._handle_error(message, e)

    def _handle_error(self, message, error):
        """Handle processing errors."""
        # Log error
        logger.error(f"Error processing message: {error}")

        # Send to dead letter queue
        self.producer.send(
            f"{self.config.output_topic}-dlq",
            value={
                "original_message": message.value,
                "error": str(error),
                "timestamp": datetime.utcnow().isoformat()
            }
        )
```

**Online Feature Store (Feast):**

```python
from feast import FeatureStore
import pandas as pd
from typing import List, Dict
import redis

class OnlineFeatureStore:
    """Online feature store with Feast and Redis."""

    def __init__(
        self,
        feast_repo_path: str = None,
        redis_host: str = "localhost",
        redis_port: int = 6379,
        feature_ttl_seconds: int = 3600
    ):
        if feast_repo_path:
            self.feast_store = FeatureStore(repo_path=feast_repo_path)
        else:
            self.feast_store = None

        self.redis = redis.Redis(
            host=redis_host,
            port=redis_port,
            decode_responses=True
        )
        self.ttl = feature_ttl_seconds

    def get_online_features(
        self,
        entity_rows: List[Dict],
        feature_refs: List[str]
    ) -> pd.DataFrame:
        """Get features from Feast online store."""
        if self.feast_store:
            return self.feast_store.get_online_features(
                entity_rows=entity_rows,
                features=feature_refs
            ).to_df()

        # Fallback to direct Redis lookup
        results = []
        for entity in entity_rows:
            entity_id = list(entity.values())[0]
            features = self._get_from_redis(entity_id, feature_refs)
            results.append({**entity, **features})

        return pd.DataFrame(results)

    def _get_from_redis(
        self,
        entity_id: str,
        feature_names: List[str]
    ) -> Dict:
        """Get features directly from Redis."""
        key = f"features:{entity_id}"
        values = self.redis.hmget(key, feature_names)

        return {
            name: self._parse_value(value)
            for name, value in zip(feature_names, values)
        }

    def _parse_value(self, value):
        """Parse Redis value to appropriate type."""
        if value is None:
            return None
        try:
            return float(value)
        except ValueError:
            return value

    def write_features(
        self,
        entity_id: str,
        features: Dict[str, Any]
    ):
        """Write features to online store."""
        key = f"features:{entity_id}"
        self.redis.hset(key, mapping=features)
        self.redis.expire(key, self.ttl)
```

**Real-time Predictor:**

```python
from typing import Dict, List, Any
import numpy as np
from dataclasses import dataclass
import time

@dataclass
class PredictionResult:
    entity_id: str
    prediction: int
    probability: float
    features_used: Dict
    latency_ms: float
    timestamp: str

class RealtimePredictor:
    """Real-time ML prediction with online features."""

    def __init__(
        self,
        model,
        feature_store: OnlineFeatureStore,
        feature_names: List[str],
        latency_slo_ms: float = 100
    ):
        self.model = model
        self.feature_store = feature_store
        self.feature_names = feature_names
        self.latency_slo_ms = latency_slo_ms

    def predict(
        self,
        entity_id: str,
        additional_features: Dict = None
    ) -> PredictionResult:
        """Generate real-time prediction."""
        start_time = time.time()

        # Fetch online features
        entity_rows = [{"entity_id": entity_id}]
        features_df = self.feature_store.get_online_features(
            entity_rows=entity_rows,
            feature_refs=self.feature_names
        )

        features = features_df.iloc[0].to_dict()

        # Add additional features
        if additional_features:
            features.update(additional_features)

        # Prepare feature vector
        feature_vector = self._prepare_features(features)

        # Generate prediction
        probabilities = self.model.predict_proba([feature_vector])[0]
        prediction = int(np.argmax(probabilities))
        probability = float(probabilities[prediction])

        # Calculate latency
        latency_ms = (time.time() - start_time) * 1000

        # Log if SLO breached
        if latency_ms > self.latency_slo_ms:
            logger.warning(f"Latency SLO breached: {latency_ms:.2f}ms > {self.latency_slo_ms}ms")

        return PredictionResult(
            entity_id=entity_id,
            prediction=prediction,
            probability=probability,
            features_used=features,
            latency_ms=latency_ms,
            timestamp=datetime.utcnow().isoformat()
        )

    def _prepare_features(self, features: Dict) -> List[float]:
        """Prepare feature vector in correct order."""
        return [
            float(features.get(name, 0))
            for name in self.feature_names
        ]
```

**Feature Definition (Feast):**

```python
# feast/feature_repo/features.py
from datetime import timedelta
from feast import Entity, Feature, FeatureView, FileSource, ValueType
from feast.types import Float32, Int64

# Entity definition
user = Entity(
    name="user_id",
    value_type=ValueType.STRING,
    description="User identifier"
)

# Feature source
user_stats_source = FileSource(
    path="data/user_stats.parquet",
    timestamp_field="event_timestamp"
)

# Feature view
user_features = FeatureView(
    name="user_features",
    entities=["user_id"],
    ttl=timedelta(days=1),
    features=[
        Feature(name="total_purchases", dtype=Int64),
        Feature(name="avg_order_value", dtype=Float32),
        Feature(name="days_since_last_order", dtype=Int64),
        Feature(name="total_spend", dtype=Float32),
    ],
    source=user_stats_source,
    online=True,  # Enable online serving
    tags={"team": "ml", "category": "user"}
)
```

---

## Tools and Commands

### Development

```bash
# Install dependencies
pip install kafka-python feast redis apache-flink

# Start local Kafka
docker-compose up -d kafka zookeeper

# Start local Redis
docker run -d -p 6379:6379 redis

# Initialize Feast
cd feast/feature_repo && feast apply
```

### Testing

```bash
# Run unit tests
pytest tests/ -m "not integration"

# Run with Kafka testcontainers
pytest tests/streaming/ --run-kafka
```

### Operations

```bash
# Materialize features
feast materialize $(date -d "1 day ago" +%Y-%m-%dT%H:%M:%S) $(date +%Y-%m-%dT%H:%M:%S)

# Monitor consumer lag
kafka-consumer-groups --bootstrap-server localhost:9092 --describe --group ml-processor
```

---

## Production Checklist

```markdown
## Streaming ML Production Checklist

### Streaming
- [ ] Consumer groups configured
- [ ] Partitioning strategy defined
- [ ] Dead letter queues configured
- [ ] Exactly-once semantics (if required)

### Features
- [ ] Online/offline consistency validated
- [ ] Feature freshness monitored
- [ ] TTL configured appropriately
- [ ] Materialization scheduled

### Inference
- [ ] Latency SLOs defined
- [ ] Model loading optimized
- [ ] Batch inference available
- [ ] Fallback strategy defined

### Reliability
- [ ] Checkpointing enabled
- [ ] Replay capability
- [ ] Backpressure handling
- [ ] Auto-scaling configured
```

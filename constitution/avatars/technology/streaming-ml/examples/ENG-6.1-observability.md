---
law_id: ENG-6.1
avatar: streaming-ml
---

# ENG-6.1: Observability Examples for Streaming ML

## COMPLIANT: Comprehensive Stream Processing Observability

```python
"""
Streaming ML observability with latency tracking, consumer lag monitoring,
and feature freshness metrics.
"""
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional
from prometheus_client import Histogram, Gauge, Counter
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
import structlog

logger = structlog.get_logger()
tracer = trace.get_tracer(__name__)

# Stream processing metrics
EVENT_PROCESSING_LATENCY = Histogram(
    "stream_event_processing_seconds",
    "Time to process a single event",
    ["event_type", "processor"],
    buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0]
)

CONSUMER_LAG = Gauge(
    "stream_consumer_lag_messages",
    "Number of messages behind in consumer group",
    ["topic", "partition", "consumer_group"]
)

FEATURE_FRESHNESS = Gauge(
    "feature_store_freshness_seconds",
    "Age of features since last materialization",
    ["feature_view"]
)

PREDICTION_LATENCY = Histogram(
    "ml_prediction_latency_ms",
    "End-to-end prediction latency in milliseconds",
    ["model_name", "model_version"],
    buckets=[1, 5, 10, 25, 50, 100, 250, 500]
)

EVENTS_PROCESSED = Counter(
    "stream_events_processed_total",
    "Total events processed",
    ["event_type", "status"]
)


@dataclass(frozen=True)
class ProcessingContext:
    """Immutable context for event processing observability."""
    event_id: str
    event_type: str
    kafka_timestamp: datetime
    received_at: datetime


class ObservableStreamProcessor:
    """Stream processor with comprehensive observability."""

    def __init__(self, feature_store, predictor, logger):
        self._features = feature_store
        self._predictor = predictor
        self._logger = logger

    async def process_event(self, event: dict) -> dict:
        """Process event with full observability."""
        context = ProcessingContext(
            event_id=event["id"],
            event_type=event["type"],
            kafka_timestamp=datetime.fromisoformat(event["timestamp"]),
            received_at=datetime.now(timezone.utc)
        )

        with tracer.start_as_current_span("stream.process_event") as span:
            span.set_attribute("event.id", context.event_id)
            span.set_attribute("event.type", context.event_type)

            # Track kafka-to-processing latency
            kafka_lag = (context.received_at - context.kafka_timestamp).total_seconds()
            span.set_attribute("event.kafka_lag_seconds", kafka_lag)

            self._logger.info(
                "Processing event",
                event_id=context.event_id,
                event_type=context.event_type,
                kafka_lag_seconds=kafka_lag
            )

            try:
                # Enrich with features (tracked separately)
                features = await self._enrich_with_features(event, span)

                # Run prediction (tracked separately)
                prediction = await self._run_prediction(event, features, span)

                # Record success metrics
                processing_time = (datetime.now(timezone.utc) - context.received_at).total_seconds()
                EVENT_PROCESSING_LATENCY.labels(
                    event_type=context.event_type,
                    processor="realtime"
                ).observe(processing_time)

                EVENTS_PROCESSED.labels(
                    event_type=context.event_type,
                    status="success"
                ).inc()

                span.set_status(Status(StatusCode.OK))
                self._logger.info(
                    "Event processed successfully",
                    event_id=context.event_id,
                    processing_time_seconds=processing_time,
                    prediction=prediction["score"]
                )

                return {"event_id": context.event_id, "prediction": prediction}

            except Exception as e:
                EVENTS_PROCESSED.labels(
                    event_type=context.event_type,
                    status="error"
                ).inc()

                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.record_exception(e)

                self._logger.error(
                    "Event processing failed",
                    event_id=context.event_id,
                    error=str(e),
                    error_type=type(e).__name__
                )
                raise

    async def _enrich_with_features(self, event: dict, parent_span) -> dict:
        """Enrich event with features, tracking latency and freshness."""
        with tracer.start_as_current_span("stream.feature_enrichment", parent=parent_span) as span:
            start = datetime.now(timezone.utc)

            features = await self._features.get_online_features(
                entity_id=event["user_id"],
                feature_views=["user_features", "product_features"]
            )

            # Track feature retrieval latency
            latency_ms = (datetime.now(timezone.utc) - start).total_seconds() * 1000
            span.set_attribute("feature.latency_ms", latency_ms)

            # Track feature freshness
            if features.metadata:
                freshness = (datetime.now(timezone.utc) - features.metadata.last_updated).total_seconds()
                FEATURE_FRESHNESS.labels(feature_view="user_features").set(freshness)
                span.set_attribute("feature.freshness_seconds", freshness)

            return features.to_dict()

    async def _run_prediction(self, event: dict, features: dict, parent_span) -> dict:
        """Run ML prediction with latency tracking."""
        with tracer.start_as_current_span("stream.prediction", parent=parent_span) as span:
            start = datetime.now(timezone.utc)

            prediction = await self._predictor.predict(
                features=features,
                context={"event_type": event["type"]}
            )

            latency_ms = (datetime.now(timezone.utc) - start).total_seconds() * 1000
            PREDICTION_LATENCY.labels(
                model_name=prediction.model_name,
                model_version=prediction.model_version
            ).observe(latency_ms)

            span.set_attribute("prediction.score", prediction.score)
            span.set_attribute("prediction.latency_ms", latency_ms)

            return {"score": prediction.score, "model": prediction.model_name}


class ConsumerLagMonitor:
    """Monitor Kafka consumer lag for alerting."""

    def __init__(self, admin_client, consumer_group: str):
        self._admin = admin_client
        self._group = consumer_group

    async def update_lag_metrics(self):
        """Update consumer lag metrics for all partitions."""
        offsets = await self._admin.list_consumer_group_offsets(self._group)

        for tp, offset_metadata in offsets.items():
            end_offset = await self._admin.list_offsets({tp: "latest"})
            lag = end_offset[tp].offset - offset_metadata.offset

            CONSUMER_LAG.labels(
                topic=tp.topic,
                partition=tp.partition,
                consumer_group=self._group
            ).set(lag)

            if lag > 10000:  # Alert threshold
                logger.warning(
                    "High consumer lag detected",
                    topic=tp.topic,
                    partition=tp.partition,
                    lag=lag
                )
```

**Why compliant:** Tracks end-to-end latency, consumer lag, feature freshness, prediction latency. Uses structured logging with correlation. Implements distributed tracing across stream processing stages.

---

## VIOLATION: No Observability in Stream Processing

```python
# BAD: Stream processor with no observability
class StreamProcessor:
    def __init__(self, feature_store, predictor):
        self.features = feature_store
        self.predictor = predictor

    async def process(self, event):
        # VIOLATION: No logging of event receipt
        # VIOLATION: No tracing context

        # VIOLATION: No latency tracking for feature retrieval
        features = await self.features.get(event["user_id"])

        # VIOLATION: No prediction latency tracking
        prediction = await self.predictor.predict(features)

        # VIOLATION: No success/failure metrics
        # VIOLATION: No consumer lag monitoring
        return prediction

    async def consume_loop(self):
        # VIOLATION: Silent consumption with no visibility
        async for message in self.consumer:
            try:
                await self.process(message.value)
            except Exception:
                # VIOLATION: Swallowed exception with no logging
                pass
```

**Why violates ENG-6.1:** No structured logging, missing latency metrics, no consumer lag monitoring, no distributed tracing, impossible to debug streaming issues or detect data staleness.

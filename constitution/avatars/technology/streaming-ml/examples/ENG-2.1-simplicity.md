---
law_id: ENG-2.1
avatar: streaming-ml
---

# ENG-2.1: Simplicity Examples for Streaming ML

## COMPLIANT: Clean, Focused Stream Processing Components

```python
"""
Simple, focused streaming ML components with single responsibilities.
Each component does one thing well.
"""
from dataclasses import dataclass
from typing import Protocol, AsyncIterator
from datetime import datetime


# Simple, focused value objects
@dataclass(frozen=True)
class StreamEvent:
    """Immutable event from stream."""
    event_id: str
    user_id: str
    event_type: str
    payload: dict
    timestamp: datetime


@dataclass(frozen=True)
class FeatureVector:
    """Immutable feature vector for prediction."""
    entity_id: str
    features: dict
    retrieved_at: datetime


@dataclass(frozen=True)
class Prediction:
    """Immutable prediction result."""
    event_id: str
    score: float
    model_version: str


# Clean protocols for abstractions
class FeatureStore(Protocol):
    """Simple interface for feature retrieval."""
    async def get_features(self, entity_id: str) -> FeatureVector:
        ...


class Predictor(Protocol):
    """Simple interface for predictions."""
    async def predict(self, features: FeatureVector) -> Prediction:
        ...


class EventSink(Protocol):
    """Simple interface for writing predictions."""
    async def write(self, prediction: Prediction) -> None:
        ...


# Focused implementations
class StreamProcessor:
    """Single-purpose processor: enrich and predict."""

    def __init__(
        self,
        feature_store: FeatureStore,
        predictor: Predictor,
        sink: EventSink
    ):
        self._features = feature_store
        self._predictor = predictor
        self._sink = sink

    async def process(self, event: StreamEvent) -> Prediction:
        """Process single event through the pipeline."""
        features = await self._features.get_features(event.user_id)
        prediction = await self._predictor.predict(features)
        await self._sink.write(prediction)
        return prediction


class FeastFeatureStore:
    """Simple Feast wrapper for online features."""

    def __init__(self, feast_client):
        self._client = feast_client

    async def get_features(self, entity_id: str) -> FeatureVector:
        """Get features for a single entity."""
        response = self._client.get_online_features(
            features=["user_features:avg_spend", "user_features:visit_count"],
            entity_rows=[{"user_id": entity_id}]
        )
        return FeatureVector(
            entity_id=entity_id,
            features=response.to_dict(),
            retrieved_at=datetime.utcnow()
        )


class KafkaEventSource:
    """Simple Kafka consumer as event source."""

    def __init__(self, consumer):
        self._consumer = consumer

    async def events(self) -> AsyncIterator[StreamEvent]:
        """Yield events from Kafka."""
        async for message in self._consumer:
            yield StreamEvent(
                event_id=message.key,
                user_id=message.value["user_id"],
                event_type=message.value["type"],
                payload=message.value,
                timestamp=datetime.fromtimestamp(message.timestamp / 1000)
            )


# Simple composition
async def run_pipeline(source: KafkaEventSource, processor: StreamProcessor):
    """Run the streaming pipeline."""
    async for event in source.events():
        await processor.process(event)
```

**Why compliant:** Each component has single responsibility, clean interfaces using Protocol, simple composition, no unnecessary abstraction layers.

---

## VIOLATION: Over-Engineered Streaming Framework

```python
# BAD: Unnecessary complexity for simple stream processing
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Callable

T = TypeVar('T')
E = TypeVar('E')
F = TypeVar('F')
P = TypeVar('P')


# VIOLATION: Unnecessary abstract base classes
class AbstractStreamSourceAdapter(ABC, Generic[T]):
    @abstractmethod
    def create_consumer_factory(self) -> 'ConsumerFactory[T]':
        pass

    @abstractmethod
    def get_deserializer_chain(self) -> 'DeserializerChain[T]':
        pass


# VIOLATION: Pipeline builder with too many options
class StreamPipelineBuilder(Generic[E, F, P]):
    def __init__(self):
        self._stages = []
        self._error_handlers = []
        self._interceptors = []
        self._transformers = []
        self._validators = []
        self._enrichers = []
        self._filters = []
        self._routers = []

    def with_source_adapter(self, adapter: AbstractStreamSourceAdapter) -> 'StreamPipelineBuilder':
        pass

    def with_feature_enrichment_strategy(
        self,
        strategy: 'FeatureEnrichmentStrategy',
        fallback_strategy: 'FeatureEnrichmentStrategy',
        cache_strategy: 'CacheStrategy',
        retry_strategy: 'RetryStrategy'
    ) -> 'StreamPipelineBuilder':
        pass

    def with_prediction_orchestrator(
        self,
        orchestrator: 'PredictionOrchestrator',
        model_selector: 'ModelSelector',
        ab_test_router: 'ABTestRouter',
        shadow_mode_handler: 'ShadowModeHandler'
    ) -> 'StreamPipelineBuilder':
        pass

    def with_error_handling_chain(
        self,
        handlers: list['ErrorHandler'],
        dead_letter_strategy: 'DeadLetterStrategy',
        circuit_breaker: 'CircuitBreaker',
        bulkhead: 'Bulkhead'
    ) -> 'StreamPipelineBuilder':
        pass

    # ... 20 more configuration methods


# VIOLATION: Factory for creating factories
class StreamProcessorFactoryFactory:
    def __init__(
        self,
        adapter_factory_registry: 'AdapterFactoryRegistry',
        enricher_factory_provider: 'EnricherFactoryProvider',
        predictor_factory_builder: 'PredictorFactoryBuilder'
    ):
        pass

    def create_processor_factory(
        self,
        config: 'ProcessorFactoryConfig'
    ) -> 'StreamProcessorFactory':
        pass


# Result: Simple event processing requires 500 lines of setup
def process_events():
    factory_factory = StreamProcessorFactoryFactory(
        AdapterFactoryRegistry.get_default(),
        EnricherFactoryProvider.with_feast(),
        PredictorFactoryBuilder().with_defaults()
    )

    processor_factory = factory_factory.create_processor_factory(
        ProcessorFactoryConfig.from_yaml("config.yaml")
    )

    pipeline = StreamPipelineBuilder() \
        .with_source_adapter(KafkaSourceAdapterFactory().create()) \
        .with_feature_enrichment_strategy(...) \
        .with_prediction_orchestrator(...) \
        .with_error_handling_chain(...) \
        .build()

    # 50 lines later, finally process an event
```

**Why violates ENG-2.1:** Factory factories, excessive generic parameters, builder with 20+ methods, simple operation requires navigating many classes. Processing a stream event should not require 500 lines of framework setup.

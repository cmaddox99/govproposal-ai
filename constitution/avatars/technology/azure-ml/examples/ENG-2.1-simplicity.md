---
law_id: ENG-2.1
avatar: azure-ml
---

# ENG-2.1: Simplicity Examples for Azure Machine Learning

## COMPLIANT: Clean Separation of Training Components

```python
"""
Simple, focused Azure ML components with single responsibilities.
Each component does one thing well.
"""
from dataclasses import dataclass
from typing import Protocol
from azure.ai.ml import command, Input, Output
from azure.ai.ml.entities import Environment


# Simple, focused value objects
@dataclass(frozen=True)
class TrainingConfig:
    """Immutable training configuration."""
    compute_target: str
    environment_name: str
    max_epochs: int = 100
    learning_rate: float = 0.001


@dataclass(frozen=True)
class ModelArtifact:
    """Immutable model reference."""
    name: str
    version: str
    path: str


# Clean protocol for trainer abstraction
class ModelTrainer(Protocol):
    """Simple interface for model training."""

    def train(self, data_path: str, config: TrainingConfig) -> ModelArtifact:
        """Train a model and return the artifact."""
        ...


# Focused implementation
class AzureMLTrainer:
    """Single-purpose trainer for Azure ML jobs."""

    def __init__(self, ml_client, experiment_name: str):
        self._client = ml_client
        self._experiment = experiment_name

    def train(self, data_path: str, config: TrainingConfig) -> ModelArtifact:
        """Submit training job and return model artifact."""
        job = self._submit_job(data_path, config)
        return self._wait_and_get_model(job)

    def _submit_job(self, data_path: str, config: TrainingConfig):
        """Submit a command job to Azure ML."""
        return self._client.jobs.create_or_update(
            command(
                code="./src/training",
                command=f"python train.py --data ${{inputs.data}} --epochs {config.max_epochs}",
                inputs={"data": Input(path=data_path)},
                outputs={"model": Output(type="mlflow_model")},
                compute=config.compute_target,
                environment=config.environment_name
            ),
            experiment_name=self._experiment
        )

    def _wait_and_get_model(self, job) -> ModelArtifact:
        """Wait for job and extract model artifact."""
        completed_job = self._client.jobs.stream(job.name)
        return ModelArtifact(
            name=f"{self._experiment}-model",
            version=completed_job.name,
            path=completed_job.outputs["model"].path
        )


# Simple pipeline composition
class TrainingPipeline:
    """Compose training steps simply."""

    def __init__(self, trainer: ModelTrainer, registry):
        self._trainer = trainer
        self._registry = registry

    def run(self, data_path: str, config: TrainingConfig) -> str:
        """Run training and register model."""
        artifact = self._trainer.train(data_path, config)
        return self._registry.register(artifact)
```

**Why compliant:** Each component has a single responsibility, uses simple immutable data structures, and composes cleanly. No unnecessary abstractions or indirection.

---

## VIOLATION: Over-Engineered Training Framework

```python
# BAD: Unnecessary complexity and abstraction layers
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Callable

T = TypeVar('T')
M = TypeVar('M')
C = TypeVar('C')


# VIOLATION: Unnecessary generic abstraction
class AbstractMLPlatformAdapter(ABC, Generic[T, M, C]):
    """Base adapter for any ML platform - way too abstract."""

    @abstractmethod
    def get_platform_client(self) -> T:
        pass

    @abstractmethod
    def create_model_wrapper(self, model: M) -> 'ModelWrapper[M]':
        pass

    @abstractmethod
    def get_config_parser(self) -> 'ConfigParser[C]':
        pass


# VIOLATION: Wrapper around wrapper
class ModelWrapper(Generic[M]):
    def __init__(self, model: M, metadata_factory: 'MetadataFactory'):
        self._model = model
        self._metadata = metadata_factory.create()

    def get_model(self) -> M:
        return self._model


# VIOLATION: Factory for factory
class TrainerFactoryFactory:
    """Factory that creates trainer factories."""

    def __init__(self, config_parser_factory, adapter_factory):
        self._config_factory = config_parser_factory
        self._adapter_factory = adapter_factory

    def create_trainer_factory(self, platform: str) -> 'TrainerFactory':
        adapter = self._adapter_factory.create(platform)
        config_parser = self._config_factory.create(platform)
        return TrainerFactory(adapter, config_parser)


# VIOLATION: Unnecessary strategy pattern
class TrainingStrategyResolver:
    """Resolves training strategy based on 10 different factors."""

    def __init__(
        self,
        compute_strategy_selector: 'ComputeStrategySelector',
        environment_strategy_selector: 'EnvironmentStrategySelector',
        data_strategy_selector: 'DataStrategySelector',
        model_strategy_selector: 'ModelStrategySelector',
        # ... 6 more strategy selectors
    ):
        pass

    def resolve(self, context: 'TrainingContext') -> 'TrainingStrategy':
        # 200 lines of strategy resolution logic
        pass


# Result: Simple training requires navigating 15 classes
def train_model():
    factory_factory = TrainerFactoryFactory(
        ConfigParserFactoryBuilder().build(),
        AdapterFactoryBuilder().with_defaults().build()
    )
    trainer_factory = factory_factory.create_trainer_factory("azure")
    trainer = trainer_factory.create(
        strategy_resolver=TrainingStrategyResolver(...),
        wrapper_factory=ModelWrapperFactory(MetadataFactoryBuilder().build())
    )
    # Finally can train, 50 lines later...
```

**Why violates ENG-2.1:** Unnecessary abstraction layers (factory factories), premature generalization (Generic types for single use case), excessive indirection that makes simple operations complex. A training job should not require navigating 15+ classes.

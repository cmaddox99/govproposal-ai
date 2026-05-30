---
law_id: ENG-2.1
avatar: vertex-ai
---

# ENG-2.1: Simplicity Examples for Google Vertex AI

## COMPLIANT: Clean Separation of Vertex AI Components

```python
"""
Simple, focused Vertex AI components with single responsibilities.
Each component does one thing well.
"""
from dataclasses import dataclass
from typing import Protocol
import google.cloud.aiplatform as aiplatform


# Simple, focused value objects
@dataclass(frozen=True)
class TrainingConfig:
    """Immutable training configuration."""
    machine_type: str
    accelerator_type: str = None
    accelerator_count: int = 0
    container_uri: str = "gcr.io/cloud-aiplatform/training/pytorch-gpu.1-13:latest"


@dataclass(frozen=True)
class ModelArtifact:
    """Immutable model reference."""
    display_name: str
    artifact_uri: str
    model_id: str


# Clean protocol for abstractions
class Trainer(Protocol):
    """Simple interface for model training."""

    def train(self, script_path: str, config: TrainingConfig) -> ModelArtifact:
        """Train a model and return the artifact."""
        ...


# Focused implementation
class VertexTrainer:
    """Single-purpose trainer for Vertex AI custom jobs."""

    def __init__(self, project: str, location: str, staging_bucket: str):
        aiplatform.init(
            project=project,
            location=location,
            staging_bucket=staging_bucket
        )

    def train(self, script_path: str, config: TrainingConfig) -> ModelArtifact:
        """Submit training job and return model artifact."""
        job = self._create_job(script_path, config)
        job.run(sync=True)
        return self._extract_artifact(job)

    def _create_job(self, script_path: str, config: TrainingConfig) -> aiplatform.CustomJob:
        """Create a custom training job."""
        return aiplatform.CustomJob.from_local_script(
            display_name="training-job",
            script_path=script_path,
            container_uri=config.container_uri,
            machine_type=config.machine_type,
            accelerator_type=config.accelerator_type,
            accelerator_count=config.accelerator_count
        )

    def _extract_artifact(self, job: aiplatform.CustomJob) -> ModelArtifact:
        """Extract model artifact from completed job."""
        return ModelArtifact(
            display_name=job.display_name,
            artifact_uri=job.job_spec.base_output_directory.output_uri_prefix,
            model_id=job.resource_name
        )


class ModelDeployer:
    """Single-purpose deployer for Vertex AI endpoints."""

    def __init__(self, project: str, location: str):
        aiplatform.init(project=project, location=location)

    def deploy(self, artifact: ModelArtifact, endpoint_name: str) -> str:
        """Deploy model to endpoint, return endpoint ID."""
        model = aiplatform.Model.upload(
            display_name=artifact.display_name,
            artifact_uri=artifact.artifact_uri
        )

        endpoint = aiplatform.Endpoint.create(display_name=endpoint_name)
        model.deploy(endpoint=endpoint, machine_type="n1-standard-2")

        return endpoint.resource_name


# Simple pipeline composition
class TrainingPipeline:
    """Compose training and deployment simply."""

    def __init__(self, trainer: Trainer, deployer: ModelDeployer):
        self._trainer = trainer
        self._deployer = deployer

    def run(
        self,
        script_path: str,
        config: TrainingConfig,
        endpoint_name: str
    ) -> str:
        """Train and deploy model."""
        artifact = self._trainer.train(script_path, config)
        return self._deployer.deploy(artifact, endpoint_name)
```

**Why compliant:** Each component has a single responsibility, uses simple immutable data structures, and composes cleanly. No unnecessary abstractions or indirection.

---

## VIOLATION: Over-Engineered Vertex AI Framework

```python
# BAD: Unnecessary complexity and abstraction layers
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Callable

T = TypeVar('T')
M = TypeVar('M')


# VIOLATION: Unnecessary abstract factory
class AbstractCloudProviderAdapter(ABC, Generic[T]):
    """Base adapter for any cloud ML platform."""

    @abstractmethod
    def get_platform_client(self) -> T:
        pass

    @abstractmethod
    def create_resource_manager(self) -> 'ResourceManager':
        pass

    @abstractmethod
    def get_cost_estimator(self) -> 'CostEstimator':
        pass


# VIOLATION: Strategy pattern overkill
class TrainingStrategySelector:
    """Selects training strategy based on many factors."""

    def __init__(
        self,
        machine_type_selector: 'MachineTypeSelector',
        accelerator_selector: 'AcceleratorSelector',
        distributed_strategy_selector: 'DistributedStrategySelector',
        container_selector: 'ContainerSelector',
        preemptible_selector: 'PreemptibleSelector',
        region_selector: 'RegionSelector'
    ):
        pass

    def select(self, context: 'TrainingContext') -> 'TrainingStrategy':
        # 100 lines of strategy selection logic
        pass


# VIOLATION: Builder with too many options
class VertexJobBuilder:
    def __init__(self):
        self._config = {}

    def with_machine_type(self, mt) -> 'VertexJobBuilder':
        self._config["machine_type"] = mt
        return self

    def with_accelerator(self, acc_type, count) -> 'VertexJobBuilder':
        self._config["accelerator_type"] = acc_type
        self._config["accelerator_count"] = count
        return self

    def with_container(self, uri) -> 'VertexJobBuilder':
        self._config["container_uri"] = uri
        return self

    def with_distributed_training(self, strategy) -> 'VertexJobBuilder':
        return self

    def with_hyperparameter_tuning(self, config) -> 'VertexJobBuilder':
        return self

    def with_custom_service_account(self, sa) -> 'VertexJobBuilder':
        return self

    def with_vpc_network(self, network) -> 'VertexJobBuilder':
        return self

    def with_kms_key(self, key) -> 'VertexJobBuilder':
        return self

    # ... 15 more builder methods

    def build(self) -> 'VertexJob':
        pass


# VIOLATION: Factory factory
class VertexTrainerFactoryFactory:
    def __init__(
        self,
        adapter_factory: 'CloudAdapterFactory',
        strategy_factory: 'StrategyFactory',
        builder_factory: 'BuilderFactory'
    ):
        pass

    def create_trainer_factory(self, platform: str) -> 'TrainerFactory':
        pass


# Result: Simple training requires 200 lines of setup
def train_model():
    factory_factory = VertexTrainerFactoryFactory(
        GCPAdapterFactoryBuilder().build(),
        StrategyFactoryProvider.get_default(),
        BuilderFactoryRegistry.create()
    )

    trainer_factory = factory_factory.create_trainer_factory("vertex")
    trainer = trainer_factory.create(
        strategy_selector=TrainingStrategySelector(...),
        job_builder=VertexJobBuilder()
    )

    # Finally can train...
```

**Why violates ENG-2.1:** Factory factories, excessive strategy patterns, builders with 20+ methods. A simple training job should not require navigating 10+ classes. The Vertex AI SDK already provides good abstractions - wrapping it in more abstraction adds no value.

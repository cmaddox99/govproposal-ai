---
law_id: BUS-3.1
avatar: pytorch
---

# BUS-3.1: Data Governance Examples for PyTorch

## COMPLIANT: Model Versioning with Comprehensive Metadata

```python
import torch
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
import torch.nn as nn


@dataclass
class ModelCheckpointMetadata:
    """Metadata for model checkpoint governance."""

    model_id: str
    version: str
    checkpoint_hash: str
    created_at: str
    created_by: str
    training_data_version: str
    hyperparameters: Dict[str, Any]
    architecture: str
    framework_version: str
    metrics: Dict[str, float]
    parent_checkpoint: Optional[str]
    tags: List[str]


class ModelRegistry:
    """PyTorch model registry with versioning and lineage tracking."""

    def __init__(self, registry_path: str):
        self.registry_path = Path(registry_path)
        self.registry_path.mkdir(parents=True, exist_ok=True)
        self.metadata_path = self.registry_path / 'metadata'
        self.metadata_path.mkdir(exist_ok=True)

    def compute_model_hash(self, model: nn.Module) -> str:
        """Compute deterministic hash of model state."""
        state_dict = model.state_dict()

        # Serialize state dict deterministically
        buffer = []
        for key in sorted(state_dict.keys()):
            buffer.append(key.encode())
            buffer.append(state_dict[key].cpu().numpy().tobytes())

        return hashlib.sha256(b''.join(buffer)).hexdigest()[:16]

    def get_architecture_string(self, model: nn.Module) -> str:
        """Get string representation of model architecture."""
        return str(model)

    def register_model(
        self,
        model: nn.Module,
        model_id: str,
        version: str,
        training_data_version: str,
        hyperparameters: Dict[str, Any],
        metrics: Dict[str, float],
        created_by: str,
        parent_checkpoint: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> ModelCheckpointMetadata:
        """Register a model checkpoint with full governance metadata."""

        checkpoint_hash = self.compute_model_hash(model)

        metadata = ModelCheckpointMetadata(
            model_id=model_id,
            version=version,
            checkpoint_hash=checkpoint_hash,
            created_at=datetime.utcnow().isoformat(),
            created_by=created_by,
            training_data_version=training_data_version,
            hyperparameters=hyperparameters,
            architecture=self.get_architecture_string(model),
            framework_version=torch.__version__,
            metrics=metrics,
            parent_checkpoint=parent_checkpoint,
            tags=tags or []
        )

        # Save model checkpoint
        checkpoint_path = self.registry_path / f"{model_id}_{version}.pt"
        torch.save({
            'model_state_dict': model.state_dict(),
            'metadata': asdict(metadata)
        }, checkpoint_path)

        # Save metadata separately for querying
        metadata_file = self.metadata_path / f"{model_id}_{version}.json"
        with open(metadata_file, 'w') as f:
            json.dump(asdict(metadata), f, indent=2)

        return metadata

    def load_model(
        self,
        model: nn.Module,
        model_id: str,
        version: str
    ) -> ModelCheckpointMetadata:
        """Load a model checkpoint with metadata verification."""
        checkpoint_path = self.registry_path / f"{model_id}_{version}.pt"

        checkpoint = torch.load(checkpoint_path, map_location='cpu')
        model.load_state_dict(checkpoint['model_state_dict'])

        # Verify integrity
        current_hash = self.compute_model_hash(model)
        stored_hash = checkpoint['metadata']['checkpoint_hash']

        if current_hash != stored_hash:
            raise ValueError(
                f"Model integrity check failed. "
                f"Expected hash {stored_hash}, got {current_hash}"
            )

        return ModelCheckpointMetadata(**checkpoint['metadata'])

    def get_model_lineage(self, model_id: str, version: str) -> List[Dict]:
        """Trace the training lineage of a model."""
        lineage = []
        current_version = version

        while current_version:
            metadata_file = self.metadata_path / f"{model_id}_{current_version}.json"

            with open(metadata_file) as f:
                metadata = json.load(f)

            lineage.append(metadata)
            current_version = metadata.get('parent_checkpoint')

        return lineage

    def list_models(
        self,
        model_id: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> List[Dict]:
        """List registered models with optional filtering."""
        models = []

        for metadata_file in self.metadata_path.glob('*.json'):
            with open(metadata_file) as f:
                metadata = json.load(f)

            if model_id and metadata['model_id'] != model_id:
                continue

            if tags and not all(t in metadata['tags'] for t in tags):
                continue

            models.append(metadata)

        return sorted(models, key=lambda x: x['created_at'], reverse=True)


# Usage example
def train_and_register_model(
    model: nn.Module,
    train_loader: torch.utils.data.DataLoader,
    registry: ModelRegistry,
    data_version: str,
    user_id: str
) -> ModelCheckpointMetadata:
    """Train model and register with governance metadata."""

    hyperparameters = {
        'learning_rate': 0.001,
        'batch_size': 32,
        'epochs': 10,
        'optimizer': 'Adam',
        'weight_decay': 1e-5
    }

    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=hyperparameters['learning_rate'],
        weight_decay=hyperparameters['weight_decay']
    )

    # Training loop
    for epoch in range(hyperparameters['epochs']):
        train_epoch(model, train_loader, optimizer)

    # Evaluate and compute metrics
    metrics = evaluate_model(model, val_loader)

    # Register with full governance metadata
    metadata = registry.register_model(
        model=model,
        model_id='transformer_classifier',
        version=f'v1.0.{datetime.now().strftime("%Y%m%d%H%M%S")}',
        training_data_version=data_version,
        hyperparameters=hyperparameters,
        metrics=metrics,
        created_by=user_id,
        tags=['production-candidate', 'classification']
    )

    return metadata
```

**Why compliant:** Every model checkpoint includes comprehensive metadata. Training data version is linked to model version. Hyperparameters are captured for reproducibility. Model integrity is verified through hash comparison. Parent checkpoint tracking enables lineage tracing.

---

## VIOLATION: Saving Models Without Versioning or Metadata

```python
import torch
import torch.nn as nn


def save_model(model: nn.Module, path: str) -> None:
    """Save model without any governance information."""
    # Only save model weights - no metadata
    torch.save(model.state_dict(), path)


def load_model(model: nn.Module, path: str) -> None:
    """Load model without verification."""
    # No integrity check
    # No version information
    # No provenance data
    model.load_state_dict(torch.load(path))


def train_and_save():
    """Train model and save without governance."""
    model = create_model()

    # Train model
    for epoch in range(10):
        train_epoch(model, train_loader, optimizer)

    # Save without any metadata
    save_model(model, 'model.pt')

    # No record of:
    # - Which data was used for training
    # - What hyperparameters were used
    # - Who trained the model
    # - What metrics were achieved
    # - Framework version
```

**Why violates BUS-3.1:** Model is saved without any metadata or versioning. No record of training data used. Hyperparameters are not captured. No integrity verification on load. Cannot trace model lineage or provenance. Overwrites previous model without history.

---

## COMPLIANT: Experiment Tracking with MLflow Integration

```python
import torch
import torch.nn as nn
import mlflow
import mlflow.pytorch
from typing import Dict, Any, Optional
from datetime import datetime
import json
import tempfile


class ExperimentTracker:
    """Track PyTorch experiments with full governance compliance."""

    def __init__(self, experiment_name: str, tracking_uri: str):
        mlflow.set_tracking_uri(tracking_uri)
        mlflow.set_experiment(experiment_name)
        self.experiment_name = experiment_name

    def start_run(
        self,
        run_name: str,
        data_version: str,
        user_id: str,
        tags: Optional[Dict[str, str]] = None
    ) -> str:
        """Start a new tracked training run."""
        run_tags = {
            'data_version': data_version,
            'user_id': user_id,
            'framework': 'pytorch',
            'framework_version': torch.__version__,
            'started_at': datetime.utcnow().isoformat()
        }
        if tags:
            run_tags.update(tags)

        run = mlflow.start_run(run_name=run_name, tags=run_tags)
        return run.info.run_id

    def log_hyperparameters(self, params: Dict[str, Any]) -> None:
        """Log training hyperparameters."""
        mlflow.log_params(params)

    def log_metrics(
        self,
        metrics: Dict[str, float],
        step: Optional[int] = None
    ) -> None:
        """Log training metrics."""
        mlflow.log_metrics(metrics, step=step)

    def log_model_architecture(self, model: nn.Module) -> None:
        """Log model architecture for governance."""
        architecture = {
            'repr': str(model),
            'num_parameters': sum(p.numel() for p in model.parameters()),
            'trainable_parameters': sum(
                p.numel() for p in model.parameters() if p.requires_grad
            )
        }

        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.json', delete=False
        ) as f:
            json.dump(architecture, f, indent=2)
            mlflow.log_artifact(f.name, 'model_architecture')

    def log_model(
        self,
        model: nn.Module,
        artifact_path: str = 'model',
        registered_model_name: Optional[str] = None
    ) -> None:
        """Log model with MLflow model registry."""
        mlflow.pytorch.log_model(
            model,
            artifact_path,
            registered_model_name=registered_model_name
        )

    def log_data_sample(
        self,
        sample_data: torch.Tensor,
        sample_name: str
    ) -> None:
        """Log sample of training data for reproducibility."""
        with tempfile.NamedTemporaryFile(suffix='.pt', delete=False) as f:
            torch.save(sample_data, f.name)
            mlflow.log_artifact(f.name, f'data_samples/{sample_name}')

    def end_run(self) -> None:
        """End the current run."""
        mlflow.end_run()


def governed_training_pipeline(
    model: nn.Module,
    train_loader: torch.utils.data.DataLoader,
    val_loader: torch.utils.data.DataLoader,
    tracker: ExperimentTracker,
    data_version: str,
    user_id: str
) -> str:
    """Training pipeline with full governance tracking."""

    hyperparameters = {
        'learning_rate': 0.001,
        'batch_size': 32,
        'epochs': 10,
        'optimizer': 'AdamW',
        'weight_decay': 0.01,
        'scheduler': 'cosine'
    }

    # Start tracked run
    run_id = tracker.start_run(
        run_name=f'training_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
        data_version=data_version,
        user_id=user_id,
        tags={'model_type': 'transformer', 'task': 'classification'}
    )

    # Log configuration
    tracker.log_hyperparameters(hyperparameters)
    tracker.log_model_architecture(model)

    # Log data sample for reproducibility
    sample_batch = next(iter(train_loader))
    tracker.log_data_sample(sample_batch[0][:5], 'training_sample')

    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=hyperparameters['learning_rate'],
        weight_decay=hyperparameters['weight_decay']
    )

    # Training loop with metric logging
    for epoch in range(hyperparameters['epochs']):
        train_loss = train_epoch(model, train_loader, optimizer)
        val_metrics = evaluate(model, val_loader)

        tracker.log_metrics({
            'train_loss': train_loss,
            'val_loss': val_metrics['loss'],
            'val_accuracy': val_metrics['accuracy']
        }, step=epoch)

    # Log final model
    tracker.log_model(
        model,
        artifact_path='model',
        registered_model_name='transformer_classifier'
    )

    tracker.end_run()

    return run_id
```

**Why compliant:** Full experiment tracking with MLflow integration. Data version is recorded with each training run. Hyperparameters and metrics are logged systematically. Model architecture is captured for reproducibility. Model registry provides versioning and deployment tracking. Audit trail supports compliance requirements.

---

## VIOLATION: Training Without Experiment Tracking

```python
import torch


def train_model(model, train_loader, epochs=10):
    """Train model without any tracking."""
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    for epoch in range(epochs):
        for batch in train_loader:
            optimizer.zero_grad()
            loss = model(batch)
            loss.backward()
            optimizer.step()

        # Print metrics but don't save them
        print(f"Epoch {epoch}, Loss: {loss.item()}")

    # No record of final metrics
    # No hyperparameters logged
    # No data version tracked

    torch.save(model.state_dict(), 'model.pt')


def compare_models():
    """Try to compare models without experiment tracking."""
    # Cannot compare because there's no record of:
    # - What hyperparameters were used for each model
    # - What data version was used
    # - What metrics were achieved
    # - When each model was trained

    model1 = torch.load('model_v1.pt')
    model2 = torch.load('model_v2.pt')

    # No way to know which is better or why
    return "Unknown - no tracking data available"
```

**Why violates BUS-3.1:** No experiment tracking or logging. Metrics are printed but not persisted. Cannot compare experiments or reproduce results. No hyperparameter or data version tracking. Training history is lost when script ends.

# MLflow + Kubeflow Guidance

> **Purpose:** Stack-specific agent behaviors for MLOps using MLflow for experiment tracking and Kubeflow for pipeline orchestration.

---

## Overview

This guidance provides patterns for AI agents working with the MLflow + Kubeflow stack for production MLOps including experiment tracking, model registry, and Kubernetes-native ML pipelines.

---

## Testing Framework

**Primary Framework:** pytest + kfp.testing + mlflow tracking

### Test Structure

```python
import pytest
from unittest.mock import MagicMock, patch
import mlflow
from kfp import dsl
from kfp.testing import run_pipeline_locally
from myproject.pipelines.training_pipeline import training_pipeline
from myproject.components.train import train_component
from myproject.tracking.experiment import ExperimentTracker


class TestMLflowTracking:
    """Tests for MLflow experiment tracking."""

    @pytest.fixture
    def tracker(self, tmp_path):
        """Experiment tracker with local backend."""
        mlflow.set_tracking_uri(f"file://{tmp_path}/mlruns")
        return ExperimentTracker(experiment_name="test-experiment")

    def test_tracker_logs_params(self, tracker):
        """Tracker should log parameters."""
        # Arrange
        params = {"learning_rate": 0.001, "epochs": 10}

        # Act
        with tracker.start_run():
            tracker.log_params(params)

        # Assert
        run = mlflow.get_run(tracker.run_id)
        assert run.data.params["learning_rate"] == "0.001"

    def test_tracker_logs_metrics(self, tracker):
        """Tracker should log metrics."""
        # Act
        with tracker.start_run():
            tracker.log_metrics({"accuracy": 0.95, "loss": 0.1})

        # Assert
        run = mlflow.get_run(tracker.run_id)
        assert run.data.metrics["accuracy"] == 0.95

    def test_tracker_logs_model(self, tracker, tmp_path):
        """Tracker should log model artifacts."""
        # Arrange
        import joblib
        model = {"type": "test"}
        model_path = tmp_path / "model.pkl"
        joblib.dump(model, model_path)

        # Act
        with tracker.start_run():
            tracker.log_model(str(model_path), "model")

        # Assert
        run = mlflow.get_run(tracker.run_id)
        assert "model" in [a.path for a in mlflow.tracking.MlflowClient().list_artifacts(run.info.run_id)]


class TestKubeflowPipeline:
    """Tests for Kubeflow pipeline."""

    def test_pipeline_compiles(self):
        """Pipeline should compile successfully."""
        from kfp import compiler

        # Act
        compiler.Compiler().compile(
            pipeline_func=training_pipeline,
            package_path="pipeline.yaml"
        )

        # Assert
        import os
        assert os.path.exists("pipeline.yaml")

    def test_pipeline_runs_locally(self):
        """Pipeline should run in local mode."""
        # Act
        result = run_pipeline_locally(
            training_pipeline,
            arguments={
                "input_data": "/tmp/data",
                "epochs": 1
            }
        )

        # Assert
        assert result.status == "Succeeded"


class TestTrainComponent:
    """Tests for training component."""

    def test_component_trains_model(self, tmp_path):
        """Training component should produce model."""
        # Arrange
        train_data = tmp_path / "train.csv"
        train_data.write_text("feature,label\n1,0\n2,1\n")
        output_dir = tmp_path / "model"

        # Act
        train_component.python_func(
            train_data=str(train_data),
            model_output=str(output_dir),
            epochs=1
        )

        # Assert
        assert (output_dir / "model.pt").exists()

    def test_component_logs_to_mlflow(self, tmp_path):
        """Training component should log to MLflow."""
        # Setup MLflow
        mlflow.set_tracking_uri(f"file://{tmp_path}/mlruns")

        # Act
        train_component.python_func(
            train_data="...",
            model_output="...",
            epochs=1,
            mlflow_tracking_uri=f"file://{tmp_path}/mlruns"
        )

        # Assert
        experiment = mlflow.get_experiment_by_name("training")
        assert experiment is not None
```

---

## Common Patterns

### Good Patterns

**MLflow Experiment Tracking:**

```python
import mlflow
from mlflow.tracking import MlflowClient
from typing import Dict, Any, Optional
import os

class ExperimentTracker:
    """MLflow experiment tracking wrapper."""

    def __init__(
        self,
        tracking_uri: str = None,
        experiment_name: str = "default",
        artifact_location: str = None
    ):
        self.tracking_uri = tracking_uri or os.environ.get(
            "MLFLOW_TRACKING_URI",
            "http://mlflow:5000"
        )
        mlflow.set_tracking_uri(self.tracking_uri)

        self.experiment_name = experiment_name
        self.client = MlflowClient()

        # Get or create experiment
        experiment = mlflow.get_experiment_by_name(experiment_name)
        if experiment is None:
            self.experiment_id = mlflow.create_experiment(
                experiment_name,
                artifact_location=artifact_location
            )
        else:
            self.experiment_id = experiment.experiment_id

        self.run_id = None

    def start_run(self, run_name: str = None, tags: Dict = None):
        """Start a new MLflow run."""
        self.run = mlflow.start_run(
            experiment_id=self.experiment_id,
            run_name=run_name,
            tags=tags
        )
        self.run_id = self.run.info.run_id
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_run()

    def log_params(self, params: Dict[str, Any]):
        """Log parameters."""
        mlflow.log_params(params)

    def log_metrics(self, metrics: Dict[str, float], step: int = None):
        """Log metrics."""
        for key, value in metrics.items():
            mlflow.log_metric(key, value, step=step)

    def log_model(
        self,
        model,
        artifact_path: str,
        registered_model_name: str = None,
        **kwargs
    ):
        """Log model artifact."""
        # Determine model flavor
        if hasattr(model, 'state_dict'):  # PyTorch
            mlflow.pytorch.log_model(
                model,
                artifact_path,
                registered_model_name=registered_model_name,
                **kwargs
            )
        elif hasattr(model, 'get_params'):  # Sklearn
            mlflow.sklearn.log_model(
                model,
                artifact_path,
                registered_model_name=registered_model_name,
                **kwargs
            )
        else:
            mlflow.log_artifact(model, artifact_path)

    def log_artifact(self, local_path: str, artifact_path: str = None):
        """Log arbitrary artifact."""
        mlflow.log_artifact(local_path, artifact_path)

    def set_tags(self, tags: Dict[str, str]):
        """Set run tags."""
        mlflow.set_tags(tags)

    def end_run(self):
        """End the current run."""
        if self.run:
            mlflow.end_run()
            self.run = None
```

**Kubeflow Pipeline:**

```python
from kfp import dsl
from kfp.dsl import component, pipeline, Input, Output, Dataset, Model, Metrics
from typing import NamedTuple

# Component definitions
@component(
    base_image="python:3.10",
    packages_to_install=["pandas", "scikit-learn", "mlflow"]
)
def preprocess_data(
    input_data: Input[Dataset],
    train_output: Output[Dataset],
    test_output: Output[Dataset],
    test_size: float = 0.2,
    mlflow_tracking_uri: str = ""
):
    """Preprocess and split data with MLflow tracking."""
    import pandas as pd
    from sklearn.model_selection import train_test_split
    import mlflow

    if mlflow_tracking_uri:
        mlflow.set_tracking_uri(mlflow_tracking_uri)

    with mlflow.start_run(nested=True):
        mlflow.log_param("test_size", test_size)

        df = pd.read_csv(input_data.path)
        mlflow.log_metric("input_rows", len(df))

        train_df, test_df = train_test_split(df, test_size=test_size)

        train_df.to_csv(train_output.path, index=False)
        test_df.to_csv(test_output.path, index=False)

        mlflow.log_metric("train_rows", len(train_df))
        mlflow.log_metric("test_rows", len(test_df))


@component(
    base_image="pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime",
    packages_to_install=["mlflow"]
)
def train_model(
    train_data: Input[Dataset],
    model_output: Output[Model],
    metrics_output: Output[Metrics],
    epochs: int = 10,
    learning_rate: float = 0.001,
    mlflow_tracking_uri: str = "",
    mlflow_experiment: str = "training"
):
    """Train model with MLflow tracking."""
    import torch
    import mlflow
    import json

    if mlflow_tracking_uri:
        mlflow.set_tracking_uri(mlflow_tracking_uri)
        mlflow.set_experiment(mlflow_experiment)

    with mlflow.start_run():
        # Log parameters
        mlflow.log_params({
            "epochs": epochs,
            "learning_rate": learning_rate
        })

        # Training loop
        model = create_model()
        optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

        for epoch in range(epochs):
            loss = train_epoch(model, train_data, optimizer)
            mlflow.log_metric("loss", loss, step=epoch)

        # Evaluate
        accuracy = evaluate(model, train_data)
        mlflow.log_metric("accuracy", accuracy)

        # Save model
        torch.save(model.state_dict(), f"{model_output.path}/model.pt")

        # Log to MLflow
        mlflow.pytorch.log_model(model, "model")

        # Output metrics
        metrics_output.log_metric("accuracy", accuracy)
        metrics_output.log_metric("final_loss", loss)


@component
def evaluate_model(
    model: Input[Model],
    test_data: Input[Dataset],
    metrics: Output[Metrics],
    threshold: float = 0.8
) -> NamedTuple("Outputs", [("deploy", bool)]):
    """Evaluate model and decide on deployment."""
    from collections import namedtuple

    # Load and evaluate
    accuracy = run_evaluation(model.path, test_data.path)

    metrics.log_metric("test_accuracy", accuracy)

    Outputs = namedtuple("Outputs", ["deploy"])
    return Outputs(deploy=accuracy >= threshold)


@pipeline(name="ml-training-pipeline")
def training_pipeline(
    input_data: str,
    epochs: int = 10,
    learning_rate: float = 0.001,
    accuracy_threshold: float = 0.8,
    mlflow_tracking_uri: str = "http://mlflow:5000",
    mlflow_experiment: str = "training",
    model_name: str = "classifier"
):
    """Complete ML training pipeline with MLflow integration."""

    # Preprocess
    preprocess_task = preprocess_data(
        input_data=input_data,
        mlflow_tracking_uri=mlflow_tracking_uri
    )

    # Train
    train_task = train_model(
        train_data=preprocess_task.outputs["train_output"],
        epochs=epochs,
        learning_rate=learning_rate,
        mlflow_tracking_uri=mlflow_tracking_uri,
        mlflow_experiment=mlflow_experiment
    )

    # Evaluate
    eval_task = evaluate_model(
        model=train_task.outputs["model_output"],
        test_data=preprocess_task.outputs["test_output"],
        threshold=accuracy_threshold
    )

    # Conditional registration
    with dsl.If(eval_task.outputs["deploy"] == True):
        register_model(
            model=train_task.outputs["model_output"],
            model_name=model_name,
            mlflow_tracking_uri=mlflow_tracking_uri
        )
```

**Model Registry Operations:**

```python
from mlflow.tracking import MlflowClient
from mlflow.entities.model_registry import ModelVersionStatus

class ModelRegistry:
    """MLflow Model Registry operations."""

    def __init__(self, tracking_uri: str):
        self.client = MlflowClient(tracking_uri)

    def get_latest_version(
        self,
        model_name: str,
        stages: list = None
    ) -> str:
        """Get latest model version."""
        stages = stages or ["Production", "Staging", "None"]

        versions = self.client.get_latest_versions(model_name, stages)
        if not versions:
            return None

        return max(versions, key=lambda v: int(v.version))

    def promote_to_production(
        self,
        model_name: str,
        version: str,
        archive_existing: bool = True
    ):
        """Promote model version to production."""

        # Archive existing production models
        if archive_existing:
            existing = self.client.get_latest_versions(model_name, ["Production"])
            for model in existing:
                self.client.transition_model_version_stage(
                    name=model_name,
                    version=model.version,
                    stage="Archived"
                )

        # Promote new version
        self.client.transition_model_version_stage(
            name=model_name,
            version=version,
            stage="Production"
        )

    def get_production_model_uri(self, model_name: str) -> str:
        """Get URI for production model."""
        return f"models:/{model_name}/Production"

    def load_production_model(self, model_name: str):
        """Load the production model."""
        import mlflow

        uri = self.get_production_model_uri(model_name)
        return mlflow.pyfunc.load_model(uri)
```

---

## Tools and Commands

### Development

```bash
# Install dependencies
pip install mlflow kfp kubernetes

# Start local MLflow server
mlflow server --host 0.0.0.0 --port 5000

# Compile pipeline
python -c "from kfp import compiler; from pipelines import training_pipeline; compiler.Compiler().compile(training_pipeline, 'pipeline.yaml')"
```

### Testing

```bash
# Run unit tests
pytest tests/ -m "not integration"

# Run pipeline locally
python -c "from kfp.testing import run_pipeline_locally; ..."
```

### Pipeline Operations

```bash
# Submit to Kubeflow
kfp pipeline upload -p my-pipeline pipeline.yaml

# Create run
kfp run submit -e experiment -p my-pipeline

# View runs
kfp run list
```

---

## Production Checklist

```markdown
## MLflow + Kubeflow Production Checklist

### MLflow
- [ ] Tracking server deployed (HA)
- [ ] Artifact storage configured (S3/GCS)
- [ ] Model registry governance defined
- [ ] Experiments organized

### Kubeflow
- [ ] Pipeline versioned
- [ ] Resource limits set
- [ ] Retry policies configured
- [ ] Caching enabled

### Operations
- [ ] CI/CD for pipeline updates
- [ ] Monitoring dashboards
- [ ] Alerting configured
- [ ] Backup procedures
```

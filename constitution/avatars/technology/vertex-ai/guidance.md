# Google Cloud Vertex AI Guidance

> **Purpose:** Stack-specific agent behaviors for ML projects using Google Cloud Vertex AI.

---

## Overview

This guidance provides patterns for AI agents working with Vertex AI for end-to-end machine learning including AutoML, custom training, pipelines, and model deployment.

---

## Testing Framework

**Primary Framework:** pytest + google-cloud-aiplatform

### Test Structure

```python
import pytest
from unittest.mock import MagicMock, patch
from google.cloud import aiplatform
from myproject.training.trainer import VertexTrainer
from myproject.inference.predictor import VertexPredictor
from myproject.pipelines.training_pipeline import TrainingPipeline


class TestVertexTrainer:
    """Tests for Vertex AI training."""

    @pytest.fixture
    def mock_aiplatform(self):
        """Mock aiplatform module."""
        with patch('google.cloud.aiplatform') as mock:
            yield mock

    @pytest.fixture
    def trainer(self):
        """Vertex trainer instance."""
        return VertexTrainer(
            project_id="test-project",
            location="us-central1",
            staging_bucket="gs://test-bucket"
        )

    def test_trainer_creates_custom_job(self, trainer, mock_aiplatform):
        """Trainer should create custom training job."""
        # Arrange
        mock_job = MagicMock()
        mock_aiplatform.CustomJob.return_value = mock_job

        # Act
        trainer.train(
            display_name="test-job",
            script_path="train.py",
            args=["--epochs", "10"]
        )

        # Assert
        mock_aiplatform.CustomJob.assert_called_once()
        mock_job.run.assert_called_once()

    def test_trainer_configures_machine_spec(self, trainer, mock_aiplatform):
        """Trainer should configure machine correctly."""
        # Act
        trainer.train(
            display_name="test-job",
            script_path="train.py",
            machine_type="n1-standard-4",
            accelerator_type="NVIDIA_TESLA_T4",
            accelerator_count=1
        )

        # Assert
        call_args = mock_aiplatform.CustomJob.call_args
        worker_pool = call_args.kwargs["worker_pool_specs"][0]
        assert worker_pool["machine_spec"]["machine_type"] == "n1-standard-4"


class TestVertexPredictor:
    """Tests for Vertex AI prediction."""

    @pytest.fixture
    def mock_endpoint(self):
        """Mock Vertex endpoint."""
        mock = MagicMock()
        mock.predict.return_value = MagicMock(
            predictions=[[0.9, 0.1]]
        )
        return mock

    @pytest.fixture
    def predictor(self, mock_endpoint):
        """Predictor with mock endpoint."""
        return VertexPredictor(endpoint=mock_endpoint)

    def test_predictor_invokes_endpoint(self, predictor, mock_endpoint):
        """Predictor should invoke Vertex endpoint."""
        # Arrange
        instances = [{"feature1": 1.0, "feature2": 2.0}]

        # Act
        result = predictor.predict(instances)

        # Assert
        mock_endpoint.predict.assert_called_once_with(instances=instances)
        assert result.predictions is not None

    def test_predictor_handles_batch(self, predictor):
        """Predictor should handle batch predictions."""
        # Arrange
        instances = [{"features": [1, 2]}, {"features": [3, 4]}]

        # Act
        results = predictor.predict(instances)

        # Assert
        assert len(results.predictions) > 0


class TestTrainingPipeline:
    """Tests for Vertex AI Pipeline."""

    @pytest.fixture
    def pipeline(self):
        """Training pipeline instance."""
        return TrainingPipeline(
            project_id="test-project",
            location="us-central1"
        )

    def test_pipeline_compiles(self, pipeline):
        """Pipeline should compile successfully."""
        # Act
        compiled = pipeline.compile()

        # Assert
        assert compiled is not None

    def test_pipeline_has_required_components(self, pipeline):
        """Pipeline should have all required components."""
        # Act
        pipeline_spec = pipeline.build()

        # Assert
        component_names = [c.name for c in pipeline_spec.components]
        assert "preprocess" in component_names
        assert "train" in component_names
        assert "evaluate" in component_names
```

---

## Common Patterns

### Good Patterns

**Vertex AI Training:**

```python
from google.cloud import aiplatform
from typing import Dict, List, Optional

class VertexTrainer:
    """Wrapper for Vertex AI custom training."""

    def __init__(
        self,
        project_id: str,
        location: str,
        staging_bucket: str
    ):
        aiplatform.init(
            project=project_id,
            location=location,
            staging_bucket=staging_bucket
        )
        self.project_id = project_id
        self.location = location

    def train(
        self,
        display_name: str,
        script_path: str,
        args: List[str] = None,
        requirements: List[str] = None,
        machine_type: str = "n1-standard-4",
        accelerator_type: str = None,
        accelerator_count: int = 0,
        replica_count: int = 1,
        base_image: str = "gcr.io/deeplearning-platform-release/pytorch-gpu.1-13",
        tensorboard: str = None
    ) -> aiplatform.CustomJob:
        """Run custom training job."""

        # Define worker pool
        worker_pool_specs = [{
            "machine_spec": {
                "machine_type": machine_type,
            },
            "replica_count": replica_count,
            "python_package_spec": {
                "executor_image_uri": base_image,
                "package_uris": [],
                "python_module": script_path.replace("/", ".").replace(".py", ""),
                "args": args or [],
            }
        }]

        # Add accelerator if specified
        if accelerator_type:
            worker_pool_specs[0]["machine_spec"]["accelerator_type"] = accelerator_type
            worker_pool_specs[0]["machine_spec"]["accelerator_count"] = accelerator_count

        # Create and run job
        job = aiplatform.CustomJob(
            display_name=display_name,
            worker_pool_specs=worker_pool_specs,
        )

        job.run(
            sync=True,
            tensorboard=tensorboard
        )

        return job

    def hyperparameter_tuning(
        self,
        display_name: str,
        script_path: str,
        metric_id: str,
        parameter_spec: Dict,
        max_trial_count: int = 10,
        parallel_trial_count: int = 3
    ) -> aiplatform.HyperparameterTuningJob:
        """Run hyperparameter tuning job."""

        job = aiplatform.HyperparameterTuningJob(
            display_name=display_name,
            optimization_prediction_type="classification",
            metric_spec={metric_id: "maximize"},
            parameter_spec=parameter_spec,
            max_trial_count=max_trial_count,
            parallel_trial_count=parallel_trial_count,
            custom_job=self._create_custom_job_spec(script_path)
        )

        job.run(sync=True)
        return job
```

**Vertex AI Pipeline (KFP v2):**

```python
from kfp import dsl
from kfp.dsl import component, pipeline, Input, Output, Dataset, Model, Metrics
from google.cloud import aiplatform

@component(
    base_image="python:3.10",
    packages_to_install=["pandas", "scikit-learn"]
)
def preprocess_data(
    input_data: Input[Dataset],
    output_train: Output[Dataset],
    output_test: Output[Dataset],
    test_size: float = 0.2
):
    """Preprocess and split data."""
    import pandas as pd
    from sklearn.model_selection import train_test_split

    df = pd.read_csv(input_data.path)

    train_df, test_df = train_test_split(df, test_size=test_size)

    train_df.to_csv(output_train.path, index=False)
    test_df.to_csv(output_test.path, index=False)


@component(
    base_image="gcr.io/deeplearning-platform-release/pytorch-gpu.1-13"
)
def train_model(
    train_data: Input[Dataset],
    model_output: Output[Model],
    metrics_output: Output[Metrics],
    epochs: int = 10,
    learning_rate: float = 0.001
):
    """Train the model."""
    import torch
    import json

    # Training logic...

    # Log metrics
    metrics_output.log_metric("accuracy", accuracy)
    metrics_output.log_metric("loss", final_loss)

    # Save model
    torch.save(model.state_dict(), model_output.path + "/model.pt")


@component
def evaluate_model(
    model: Input[Model],
    test_data: Input[Dataset],
    metrics: Output[Metrics],
    threshold: float = 0.8
) -> bool:
    """Evaluate model and return if it passes threshold."""
    # Evaluation logic...

    metrics.log_metric("test_accuracy", test_accuracy)

    return test_accuracy >= threshold


@component
def deploy_model(
    model: Input[Model],
    project_id: str,
    endpoint_name: str
):
    """Deploy model to Vertex AI endpoint."""
    from google.cloud import aiplatform

    aiplatform.init(project=project_id)

    # Upload model
    uploaded_model = aiplatform.Model.upload(
        display_name="model",
        artifact_uri=model.uri,
        serving_container_image_uri="us-docker.pkg.dev/vertex-ai/prediction/pytorch-gpu.1-13:latest"
    )

    # Deploy to endpoint
    endpoint = aiplatform.Endpoint.create(display_name=endpoint_name)
    endpoint.deploy(model=uploaded_model)


@pipeline(name="training-pipeline")
def training_pipeline(
    input_data_uri: str,
    project_id: str,
    epochs: int = 10,
    learning_rate: float = 0.001,
    accuracy_threshold: float = 0.8
):
    """Complete training pipeline."""

    # Preprocess
    preprocess_task = preprocess_data(
        input_data=input_data_uri
    )

    # Train
    train_task = train_model(
        train_data=preprocess_task.outputs["output_train"],
        epochs=epochs,
        learning_rate=learning_rate
    )

    # Evaluate
    eval_task = evaluate_model(
        model=train_task.outputs["model_output"],
        test_data=preprocess_task.outputs["output_test"],
        threshold=accuracy_threshold
    )

    # Conditional deploy
    with dsl.If(eval_task.output == True):
        deploy_model(
            model=train_task.outputs["model_output"],
            project_id=project_id,
            endpoint_name="production-endpoint"
        )
```

**Vertex AI Experiments:**

```python
from google.cloud import aiplatform
from typing import Dict, Any

class ExperimentTracker:
    """Track experiments with Vertex AI Experiments."""

    def __init__(
        self,
        project_id: str,
        location: str,
        experiment_name: str
    ):
        aiplatform.init(project=project_id, location=location)

        self.experiment = aiplatform.Experiment.create(
            experiment_name,
            description="ML experiment"
        )

    def start_run(self, run_name: str):
        """Start a new experiment run."""
        self.run = aiplatform.ExperimentRun.create(
            run_name,
            experiment=self.experiment
        )

    def log_params(self, params: Dict[str, Any]):
        """Log hyperparameters."""
        self.run.log_params(params)

    def log_metrics(self, metrics: Dict[str, float]):
        """Log metrics."""
        self.run.log_metrics(metrics)

    def log_model(self, model_uri: str):
        """Log model artifact."""
        # Associate model with run
        pass

    def end_run(self):
        """End the current run."""
        self.run.end_run()
```

---

## Tools and Commands

### Development

```bash
# Install Vertex AI SDK
pip install google-cloud-aiplatform kfp

# Authenticate
gcloud auth application-default login

# Set project
gcloud config set project PROJECT_ID
```

### Testing

```bash
# Run unit tests
pytest tests/ -m "not integration"

# Run integration tests
pytest tests/integration/ --run-gcp
```

### Pipeline Operations

```bash
# Compile pipeline
python -c "from pipelines import training_pipeline; ..."

# Submit pipeline
python scripts/submit_pipeline.py

# Monitor pipeline
gcloud ai pipelines describe PIPELINE_ID
```

---

## Production Checklist

```markdown
## Vertex AI Production Checklist

### Training
- [ ] Experiments logged
- [ ] Checkpointing enabled
- [ ] Preemptible VMs used where appropriate
- [ ] Data in regional buckets

### Deployment
- [ ] Traffic splitting configured
- [ ] Auto-scaling enabled
- [ ] Model monitoring active
- [ ] Explainability configured

### Security
- [ ] VPC-SC configured
- [ ] IAM roles scoped
- [ ] CMEK encryption
- [ ] Private endpoints
```

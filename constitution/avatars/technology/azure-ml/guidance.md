# Azure Machine Learning Guidance

> **Purpose:** Stack-specific agent behaviors for ML projects using Azure Machine Learning.

---

## Overview

This guidance provides patterns for AI agents working with Azure Machine Learning for end-to-end ML workflows including training, deployment, MLOps, and responsible AI.

---

## Testing Framework

**Primary Framework:** pytest + azure-ai-ml SDK

### Test Structure

```python
import pytest
from unittest.mock import MagicMock, patch
from azure.ai.ml import MLClient
from azure.ai.ml.entities import Model, Environment
from myproject.training.trainer import AzureMLTrainer
from myproject.inference.predictor import AzureMLPredictor


class TestAzureMLTrainer:
    """Tests for Azure ML training."""

    @pytest.fixture
    def mock_ml_client(self):
        """Mock ML client."""
        mock = MagicMock(spec=MLClient)
        mock.jobs.create_or_update.return_value = MagicMock(
            name="test-job",
            status="Completed"
        )
        return mock

    @pytest.fixture
    def trainer(self, mock_ml_client):
        """Azure ML trainer instance."""
        return AzureMLTrainer(
            ml_client=mock_ml_client,
            compute_name="gpu-cluster"
        )

    def test_trainer_submits_job(self, trainer, mock_ml_client):
        """Trainer should submit job to Azure ML."""
        # Arrange
        config = {
            "script": "train.py",
            "environment": "pytorch-env",
            "inputs": {"data": "azureml://datastores/data/paths/train"}
        }

        # Act
        job = trainer.train(config)

        # Assert
        mock_ml_client.jobs.create_or_update.assert_called_once()

    def test_trainer_configures_compute(self, trainer, mock_ml_client):
        """Trainer should configure compute correctly."""
        # Act
        trainer.train(
            config={"script": "train.py"},
            instance_type="Standard_NC6",
            instance_count=2
        )

        # Assert
        call_args = mock_ml_client.jobs.create_or_update.call_args
        job = call_args[0][0]
        assert job.compute == "gpu-cluster"


class TestAzureMLPredictor:
    """Tests for Azure ML inference."""

    @pytest.fixture
    def mock_endpoint(self):
        """Mock online endpoint."""
        mock = MagicMock()
        mock.invoke.return_value = '{"predictions": [0.9]}'
        return mock

    @pytest.fixture
    def predictor(self, mock_endpoint):
        """Predictor with mock."""
        return AzureMLPredictor(endpoint=mock_endpoint)

    def test_predictor_invokes_endpoint(self, predictor, mock_endpoint):
        """Predictor should invoke Azure ML endpoint."""
        # Arrange
        data = {"features": [1.0, 2.0, 3.0]}

        # Act
        result = predictor.predict(data)

        # Assert
        mock_endpoint.invoke.assert_called_once()
        assert "predictions" in result
```

---

## Common Patterns

### Good Patterns

**Azure ML Training:**

```python
from azure.ai.ml import MLClient, command, Input, Output
from azure.ai.ml.entities import (
    AmlCompute, Environment, Model
)
from azure.identity import DefaultAzureCredential
from typing import Dict, Optional

class AzureMLTrainer:
    """Wrapper for Azure ML training."""

    def __init__(
        self,
        subscription_id: str,
        resource_group: str,
        workspace_name: str,
        compute_name: str = "cpu-cluster"
    ):
        self.ml_client = MLClient(
            credential=DefaultAzureCredential(),
            subscription_id=subscription_id,
            resource_group_name=resource_group,
            workspace_name=workspace_name
        )
        self.compute_name = compute_name

    def train(
        self,
        display_name: str,
        script_path: str,
        source_directory: str,
        environment: str,
        inputs: Dict[str, str] = None,
        outputs: Dict[str, str] = None,
        instance_type: str = "Standard_DS3_v2",
        instance_count: int = 1,
        distributed: bool = False,
        experiment_name: str = None
    ):
        """Submit training job."""

        # Build inputs
        job_inputs = {}
        if inputs:
            for name, path in inputs.items():
                job_inputs[name] = Input(type="uri_folder", path=path)

        # Build outputs
        job_outputs = {}
        if outputs:
            for name, path in outputs.items():
                job_outputs[name] = Output(type="uri_folder", path=path)

        # Create command job
        job = command(
            display_name=display_name,
            code=source_directory,
            command=f"python {script_path} ${{{{inputs.data}}}}",
            inputs=job_inputs,
            outputs=job_outputs,
            environment=environment,
            compute=self.compute_name,
            instance_count=instance_count,
            experiment_name=experiment_name
        )

        # Submit job
        returned_job = self.ml_client.jobs.create_or_update(job)

        return returned_job

    def create_environment(
        self,
        name: str,
        conda_file: str = None,
        dockerfile: str = None,
        base_image: str = None
    ) -> Environment:
        """Create or update environment."""

        if dockerfile:
            env = Environment(
                name=name,
                build={"path": dockerfile}
            )
        elif conda_file:
            env = Environment(
                name=name,
                conda_file=conda_file,
                image=base_image or "mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu20.04"
            )

        return self.ml_client.environments.create_or_update(env)
```

**Azure ML Pipeline:**

```python
from azure.ai.ml import dsl, Input, Output
from azure.ai.ml.entities import Pipeline

@dsl.pipeline(
    name="training-pipeline",
    description="End-to-end training pipeline"
)
def training_pipeline(
    input_data: Input,
    learning_rate: float = 0.001,
    epochs: int = 10
):
    """Azure ML Pipeline definition."""

    # Preprocess step
    preprocess_step = preprocess_component(
        input_data=input_data
    )

    # Training step
    train_step = train_component(
        train_data=preprocess_step.outputs.output_train,
        val_data=preprocess_step.outputs.output_val,
        learning_rate=learning_rate,
        epochs=epochs
    )

    # Evaluation step
    eval_step = evaluate_component(
        model=train_step.outputs.model,
        test_data=preprocess_step.outputs.output_test
    )

    # Register model (conditional)
    register_step = register_model_component(
        model=train_step.outputs.model,
        metrics=eval_step.outputs.metrics
    )

    return {
        "trained_model": train_step.outputs.model,
        "metrics": eval_step.outputs.metrics
    }


# Component definition
from azure.ai.ml import command

preprocess_component = command(
    name="preprocess",
    display_name="Preprocess Data",
    inputs={
        "input_data": Input(type="uri_folder")
    },
    outputs={
        "output_train": Output(type="uri_folder"),
        "output_val": Output(type="uri_folder"),
        "output_test": Output(type="uri_folder")
    },
    code="./src/pipelines/components",
    command="python preprocess.py --input ${{inputs.input_data}} --output-train ${{outputs.output_train}}",
    environment="azureml:AzureML-sklearn-1.0-ubuntu20.04-py38-cpu@latest"
)
```

**Model Deployment:**

```python
from azure.ai.ml.entities import (
    ManagedOnlineEndpoint,
    ManagedOnlineDeployment,
    Model,
    CodeConfiguration
)

class ModelDeployer:
    """Deploy models to Azure ML endpoints."""

    def __init__(self, ml_client: MLClient):
        self.ml_client = ml_client

    def deploy(
        self,
        model_name: str,
        model_version: str,
        endpoint_name: str,
        deployment_name: str = "default",
        instance_type: str = "Standard_DS3_v2",
        instance_count: int = 1,
        scoring_script: str = "score.py",
        environment: str = None
    ):
        """Deploy model to managed endpoint."""

        # Create endpoint
        endpoint = ManagedOnlineEndpoint(
            name=endpoint_name,
            auth_mode="key"
        )
        self.ml_client.online_endpoints.begin_create_or_update(endpoint).result()

        # Get model
        model = self.ml_client.models.get(model_name, model_version)

        # Create deployment
        deployment = ManagedOnlineDeployment(
            name=deployment_name,
            endpoint_name=endpoint_name,
            model=model,
            code_configuration=CodeConfiguration(
                code="./src/inference",
                scoring_script=scoring_script
            ),
            environment=environment,
            instance_type=instance_type,
            instance_count=instance_count
        )

        self.ml_client.online_deployments.begin_create_or_update(deployment).result()

        # Set traffic
        endpoint.traffic = {deployment_name: 100}
        self.ml_client.online_endpoints.begin_create_or_update(endpoint).result()

        return endpoint

    def blue_green_deploy(
        self,
        endpoint_name: str,
        new_deployment_name: str,
        model: Model,
        traffic_percent: int = 10
    ):
        """Blue-green deployment with traffic splitting."""

        # Create new deployment
        deployment = ManagedOnlineDeployment(
            name=new_deployment_name,
            endpoint_name=endpoint_name,
            model=model,
            # ... other config
        )
        self.ml_client.online_deployments.begin_create_or_update(deployment).result()

        # Update traffic split
        endpoint = self.ml_client.online_endpoints.get(endpoint_name)
        endpoint.traffic = {
            "production": 100 - traffic_percent,
            new_deployment_name: traffic_percent
        }
        self.ml_client.online_endpoints.begin_create_or_update(endpoint).result()
```

---

## Tools and Commands

### Development

```bash
# Install Azure ML SDK
pip install azure-ai-ml azure-identity

# Authenticate
az login

# Set workspace context
az ml workspace show --name <workspace> --resource-group <rg>
```

### Testing

```bash
# Run unit tests
pytest tests/ -m "not integration"

# Run integration tests
pytest tests/integration/ --run-azure
```

### Job Operations

```bash
# Submit job
az ml job create --file job.yaml

# Monitor job
az ml job show --name <job-name>

# Stream logs
az ml job stream --name <job-name>
```

---

## Production Checklist

```markdown
## Azure ML Production Checklist

### Training
- [ ] Environments versioned
- [ ] Compute auto-scaling configured
- [ ] Spot VMs used where appropriate
- [ ] Data assets registered

### Deployment
- [ ] Blue-green deployment ready
- [ ] Auto-scaling configured
- [ ] Health probes configured
- [ ] Model monitoring enabled

### Security
- [ ] Private endpoints configured
- [ ] Managed identity used
- [ ] Key Vault for secrets
- [ ] Network isolation
```

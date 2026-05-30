# AWS SageMaker Guidance

> **Purpose:** Stack-specific agent behaviors for ML projects using AWS SageMaker ecosystem.

---

## Overview

This guidance provides patterns for AI agents working with AWS SageMaker for end-to-end machine learning workflows including training, deployment, and MLOps.

---

## Testing Framework

**Primary Framework:** pytest + moto (AWS mocking) + localstack

### Test Structure

```python
import pytest
from unittest.mock import MagicMock, patch
import boto3
from moto import mock_s3, mock_sagemaker
from myproject.training.trainer import SageMakerTrainer
from myproject.inference.predictor import SageMakerPredictor
from myproject.pipelines.training_pipeline import TrainingPipeline


@mock_s3
class TestSageMakerTrainer:
    """Tests for SageMaker training."""

    @pytest.fixture
    def s3_bucket(self):
        """Create mock S3 bucket."""
        conn = boto3.resource('s3', region_name='us-east-1')
        conn.create_bucket(Bucket='ml-bucket')
        return 'ml-bucket'

    @pytest.fixture
    def trainer(self, s3_bucket):
        """SageMaker trainer instance."""
        return SageMakerTrainer(
            role_arn="arn:aws:iam::123456789:role/SageMakerRole",
            bucket=s3_bucket,
            instance_type="ml.m5.large"
        )

    def test_trainer_uploads_data(self, trainer, s3_bucket):
        """Trainer should upload training data to S3."""
        # Arrange
        train_data = {"features": [[1, 2], [3, 4]], "labels": [0, 1]}

        # Act
        s3_uri = trainer.upload_data(train_data, prefix="train")

        # Assert
        assert s3_uri.startswith(f"s3://{s3_bucket}/train")

    def test_trainer_configures_estimator(self, trainer):
        """Trainer should configure estimator correctly."""
        # Act
        estimator = trainer._create_estimator(
            entry_point="train.py",
            hyperparameters={"epochs": 10}
        )

        # Assert
        assert estimator.instance_type == "ml.m5.large"
        assert estimator.hyperparameters["epochs"] == 10

    @patch('sagemaker.estimator.Estimator.fit')
    def test_trainer_starts_training_job(self, mock_fit, trainer):
        """Trainer should start SageMaker training job."""
        # Act
        trainer.train(
            entry_point="train.py",
            train_data="s3://bucket/train",
            hyperparameters={"epochs": 10}
        )

        # Assert
        mock_fit.assert_called_once()


class TestSageMakerPredictor:
    """Tests for SageMaker inference."""

    @pytest.fixture
    def mock_runtime(self):
        """Mock SageMaker runtime."""
        mock = MagicMock()
        mock.invoke_endpoint.return_value = {
            'Body': MagicMock(read=lambda: b'{"prediction": [0.9]}')
        }
        return mock

    @pytest.fixture
    def predictor(self, mock_runtime):
        """Predictor with mock runtime."""
        return SageMakerPredictor(
            endpoint_name="my-endpoint",
            runtime_client=mock_runtime
        )

    def test_predictor_invokes_endpoint(self, predictor, mock_runtime):
        """Predictor should invoke SageMaker endpoint."""
        # Arrange
        input_data = {"features": [1.0, 2.0, 3.0]}

        # Act
        result = predictor.predict(input_data)

        # Assert
        mock_runtime.invoke_endpoint.assert_called_once()
        assert "prediction" in result

    def test_predictor_handles_batch(self, predictor):
        """Predictor should handle batch predictions."""
        # Arrange
        inputs = [{"features": [1, 2]}, {"features": [3, 4]}]

        # Act
        results = predictor.predict_batch(inputs)

        # Assert
        assert len(results) == 2


class TestTrainingPipeline:
    """Tests for SageMaker Pipeline."""

    @pytest.fixture
    def pipeline(self):
        """Training pipeline instance."""
        return TrainingPipeline(
            pipeline_name="test-pipeline",
            role_arn="arn:aws:iam::123456789:role/SageMakerRole"
        )

    def test_pipeline_has_required_steps(self, pipeline):
        """Pipeline should have all required steps."""
        # Act
        definition = pipeline.build()

        # Assert
        step_names = [s.name for s in definition.steps]
        assert "Preprocess" in step_names
        assert "Train" in step_names
        assert "Evaluate" in step_names
        assert "RegisterModel" in step_names

    def test_pipeline_parameters_configurable(self, pipeline):
        """Pipeline parameters should be configurable."""
        # Assert
        param_names = [p.name for p in pipeline.parameters]
        assert "InstanceType" in param_names
        assert "TrainingData" in param_names
```

---

## Common Patterns

### Good Patterns

**SageMaker Estimator Wrapper:**

```python
from sagemaker.estimator import Estimator
from sagemaker.inputs import TrainingInput
from sagemaker import Session
import boto3
from typing import Dict, Optional

class SageMakerTrainer:
    """Wrapper for SageMaker training jobs."""

    def __init__(
        self,
        role_arn: str,
        bucket: str,
        instance_type: str = "ml.m5.large",
        instance_count: int = 1,
        framework: str = "pytorch",
        framework_version: str = "2.0",
        py_version: str = "py310",
        region: str = "us-east-1"
    ):
        self.role = role_arn
        self.bucket = bucket
        self.instance_type = instance_type
        self.instance_count = instance_count
        self.framework = framework
        self.framework_version = framework_version
        self.py_version = py_version

        self.session = Session(boto_session=boto3.Session(region_name=region))

    def train(
        self,
        entry_point: str,
        source_dir: str,
        train_data: str,
        validation_data: str = None,
        hyperparameters: Dict = None,
        job_name: str = None,
        tags: Dict = None,
        wait: bool = True
    ) -> str:
        """Start training job."""

        # Create estimator
        if self.framework == "pytorch":
            from sagemaker.pytorch import PyTorch
            estimator = PyTorch(
                entry_point=entry_point,
                source_dir=source_dir,
                role=self.role,
                instance_type=self.instance_type,
                instance_count=self.instance_count,
                framework_version=self.framework_version,
                py_version=self.py_version,
                hyperparameters=hyperparameters or {},
                sagemaker_session=self.session,
                tags=self._format_tags(tags)
            )
        elif self.framework == "sklearn":
            from sagemaker.sklearn import SKLearn
            estimator = SKLearn(
                entry_point=entry_point,
                source_dir=source_dir,
                role=self.role,
                instance_type=self.instance_type,
                instance_count=self.instance_count,
                framework_version="1.2-1",
                hyperparameters=hyperparameters or {},
                sagemaker_session=self.session
            )

        # Prepare inputs
        inputs = {"train": TrainingInput(train_data)}
        if validation_data:
            inputs["validation"] = TrainingInput(validation_data)

        # Start training
        estimator.fit(inputs, job_name=job_name, wait=wait)

        return estimator.latest_training_job.name

    def _format_tags(self, tags: Dict) -> list:
        """Format tags for SageMaker."""
        if not tags:
            return []
        return [{"Key": k, "Value": v} for k, v in tags.items()]
```

**SageMaker Pipeline:**

```python
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.steps import ProcessingStep, TrainingStep, CreateModelStep
from sagemaker.workflow.parameters import ParameterString, ParameterInteger
from sagemaker.workflow.conditions import ConditionGreaterThanOrEqualTo
from sagemaker.workflow.condition_step import ConditionStep
from sagemaker.workflow.model_step import ModelStep
from sagemaker.processing import ScriptProcessor
from sagemaker.estimator import Estimator

class TrainingPipeline:
    """SageMaker Pipeline for model training."""

    def __init__(
        self,
        pipeline_name: str,
        role_arn: str,
        bucket: str,
        region: str = "us-east-1"
    ):
        self.pipeline_name = pipeline_name
        self.role = role_arn
        self.bucket = bucket
        self.region = region

        # Define parameters
        self.parameters = self._define_parameters()

    def _define_parameters(self) -> list:
        """Define pipeline parameters."""
        return [
            ParameterString(name="TrainingData", default_value=f"s3://{self.bucket}/data/train"),
            ParameterString(name="ValidationData", default_value=f"s3://{self.bucket}/data/val"),
            ParameterString(name="InstanceType", default_value="ml.m5.large"),
            ParameterInteger(name="Epochs", default_value=10),
            ParameterString(name="ModelApprovalStatus", default_value="PendingManualApproval"),
        ]

    def build(self) -> Pipeline:
        """Build the pipeline."""

        # Step 1: Preprocessing
        preprocess_step = self._create_preprocess_step()

        # Step 2: Training
        training_step = self._create_training_step(preprocess_step)

        # Step 3: Evaluation
        eval_step = self._create_evaluation_step(training_step)

        # Step 4: Conditional registration
        condition_step = self._create_condition_step(eval_step, training_step)

        # Create pipeline
        pipeline = Pipeline(
            name=self.pipeline_name,
            parameters=self.parameters,
            steps=[preprocess_step, training_step, eval_step, condition_step]
        )

        return pipeline
```

**Model Registry:**

```python
from sagemaker.model_registry import ModelPackageGroup
import boto3

class ModelRegistry:
    """Manage models in SageMaker Model Registry."""

    def __init__(self, region: str = "us-east-1"):
        self.sm_client = boto3.client("sagemaker", region_name=region)

    def register_model(
        self,
        model_package_group_name: str,
        model_url: str,
        image_uri: str,
        approval_status: str = "PendingManualApproval",
        description: str = None,
        metrics: dict = None
    ) -> str:
        """Register a model version."""

        model_metrics = None
        if metrics:
            model_metrics = {
                "ModelQuality": {
                    "Statistics": {
                        "ContentType": "application/json",
                        "S3Uri": metrics.get("statistics_uri")
                    }
                }
            }

        response = self.sm_client.create_model_package(
            ModelPackageGroupName=model_package_group_name,
            ModelPackageDescription=description,
            InferenceSpecification={
                "Containers": [{
                    "Image": image_uri,
                    "ModelDataUrl": model_url,
                    "Framework": "PYTORCH"
                }],
                "SupportedTransformInstanceTypes": ["ml.m5.large"],
                "SupportedRealtimeInferenceInstanceTypes": ["ml.m5.large"],
                "SupportedContentTypes": ["application/json"],
                "SupportedResponseMIMETypes": ["application/json"]
            },
            ModelApprovalStatus=approval_status,
            ModelMetrics=model_metrics
        )

        return response["ModelPackageArn"]

    def approve_model(self, model_package_arn: str):
        """Approve a model for deployment."""
        self.sm_client.update_model_package(
            ModelPackageArn=model_package_arn,
            ModelApprovalStatus="Approved"
        )

    def get_latest_approved(self, model_package_group_name: str) -> str:
        """Get latest approved model version."""
        response = self.sm_client.list_model_packages(
            ModelPackageGroupName=model_package_group_name,
            ModelApprovalStatus="Approved",
            SortBy="CreationTime",
            SortOrder="Descending",
            MaxResults=1
        )

        if response["ModelPackageSummaryList"]:
            return response["ModelPackageSummaryList"][0]["ModelPackageArn"]
        return None
```

---

## Tools and Commands

### Development

```bash
# Install SageMaker SDK
pip install sagemaker boto3

# Configure AWS credentials
aws configure

# Local mode testing
python -c "from sagemaker.local import LocalSession; ..."
```

### Testing

```bash
# Run unit tests with moto
pytest tests/ -m "not integration"

# Run integration tests (requires AWS)
pytest tests/integration/ --run-aws
```

### Pipeline Operations

```bash
# Create/update pipeline
python scripts/create_pipeline.py

# Start pipeline execution
aws sagemaker start-pipeline-execution --pipeline-name my-pipeline

# Monitor execution
aws sagemaker describe-pipeline-execution --pipeline-execution-arn <arn>
```

---

## Production Checklist

```markdown
## SageMaker Production Checklist

### Training
- [ ] Hyperparameters logged
- [ ] Checkpointing enabled
- [ ] Spot instances considered
- [ ] Data versioned in S3

### Deployment
- [ ] Auto-scaling configured
- [ ] Multi-AZ deployment
- [ ] Endpoint monitoring enabled
- [ ] Rollback strategy defined

### Security
- [ ] VPC configuration
- [ ] IAM roles scoped
- [ ] Encryption at rest/transit
- [ ] Network isolation
```

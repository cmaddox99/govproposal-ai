---
law_id: ENG-4.1
avatar: mlflow-kubeflow
---

# ENG-4.1: Atomic TDD Examples for MLflow/Kubeflow

## COMPLIANT: Unit Testing ML Pipeline Components

```python
import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch
from sklearn.datasets import make_classification
from components.data_preprocessing import preprocess_features
from components.model_training import train_model
from components.evaluation import evaluate_model


@pytest.fixture
def sample_training_data():
    """Generate synthetic classification data for testing."""
    X, y = make_classification(
        n_samples=100,
        n_features=10,
        n_informative=5,
        n_redundant=2,
        random_state=42
    )
    return pd.DataFrame(X, columns=[f"feature_{i}" for i in range(10)]), pd.Series(y)


@pytest.fixture
def sample_raw_data():
    """Create sample raw data with known issues."""
    return pd.DataFrame({
        "feature_0": [1.0, 2.0, None, 4.0, 5.0],
        "feature_1": [10.0, 20.0, 30.0, 40.0, 50.0],
        "feature_2": ["a", "b", "a", "c", "b"],  # Categorical
        "target": [0, 1, 0, 1, 0]
    })


class TestDataPreprocessing:
    """Tests for data preprocessing component."""

    def test_handles_missing_values(self, sample_raw_data):
        """Verify missing values are imputed correctly."""
        # Arrange
        expected_null_count = 0

        # Act
        processed = preprocess_features(sample_raw_data.drop("target", axis=1))

        # Assert
        assert processed.isnull().sum().sum() == expected_null_count

    def test_encodes_categorical_features(self, sample_raw_data):
        """Verify categorical columns are encoded."""
        # Arrange
        raw_features = sample_raw_data.drop("target", axis=1)

        # Act
        processed = preprocess_features(raw_features)

        # Assert
        assert processed["feature_2"].dtype in [np.int64, np.float64]

    def test_preserves_feature_count(self, sample_raw_data):
        """Verify preprocessing doesn't lose features."""
        # Arrange
        raw_features = sample_raw_data.drop("target", axis=1)

        # Act
        processed = preprocess_features(raw_features)

        # Assert
        assert len(processed.columns) >= len(raw_features.columns)


class TestModelTraining:
    """Tests for model training component."""

    def test_returns_trained_model(self, sample_training_data):
        """Verify training returns a model object."""
        X, y = sample_training_data

        model = train_model(X, y, model_type="random_forest")

        assert hasattr(model, "predict")
        assert hasattr(model, "predict_proba")

    def test_model_can_predict(self, sample_training_data):
        """Verify trained model can make predictions."""
        X, y = sample_training_data

        model = train_model(X, y, model_type="random_forest")
        predictions = model.predict(X)

        assert len(predictions) == len(y)
        assert set(predictions).issubset({0, 1})

    def test_respects_hyperparameters(self, sample_training_data):
        """Verify hyperparameters are applied."""
        X, y = sample_training_data

        model = train_model(
            X, y,
            model_type="random_forest",
            hyperparams={"n_estimators": 50, "max_depth": 5}
        )

        assert model.n_estimators == 50
        assert model.max_depth == 5


class TestEvaluation:
    """Tests for model evaluation component."""

    def test_returns_required_metrics(self, sample_training_data):
        """Verify evaluation returns all required metrics."""
        X, y = sample_training_data
        model = train_model(X, y, model_type="random_forest")

        metrics = evaluate_model(model, X, y)

        required_metrics = ["accuracy", "precision", "recall", "f1", "auc"]
        for metric in required_metrics:
            assert metric in metrics
            assert 0 <= metrics[metric] <= 1

    def test_metrics_are_reproducible(self, sample_training_data):
        """Verify same inputs produce same metrics."""
        X, y = sample_training_data
        model = train_model(X, y, model_type="random_forest", random_state=42)

        metrics_1 = evaluate_model(model, X, y)
        metrics_2 = evaluate_model(model, X, y)

        assert metrics_1 == metrics_2
```

**Why compliant:** Each test focuses on a single behavior, uses descriptive names, follows Arrange-Act-Assert pattern, uses fixtures for data setup, and tests components in isolation without external dependencies.

---

## COMPLIANT: Testing Kubeflow Pipeline Components

```python
import pytest
from kfp import dsl
from kfp.components import create_component_from_func
from unittest.mock import Mock, patch
import json


def preprocess_op(
    input_path: str,
    output_path: str,
    config: dict
) -> str:
    """Preprocess data component."""
    import pandas as pd

    df = pd.read_parquet(input_path)
    # Preprocessing logic
    df_processed = df.dropna().reset_index(drop=True)
    df_processed.to_parquet(output_path)

    return output_path


class TestKubeflowComponents:
    """Test Kubeflow pipeline components."""

    @pytest.fixture
    def mock_input_data(self, tmp_path):
        """Create temporary input data."""
        import pandas as pd

        df = pd.DataFrame({
            "feature_1": [1.0, 2.0, None, 4.0],
            "feature_2": [10.0, 20.0, 30.0, 40.0],
            "label": [0, 1, 0, 1]
        })
        input_path = tmp_path / "input.parquet"
        df.to_parquet(input_path)
        return str(input_path)

    def test_preprocess_removes_nulls(self, mock_input_data, tmp_path):
        """Verify preprocessing removes null values."""
        import pandas as pd

        output_path = str(tmp_path / "output.parquet")

        result_path = preprocess_op(
            input_path=mock_input_data,
            output_path=output_path,
            config={"strategy": "drop"}
        )

        result_df = pd.read_parquet(result_path)
        assert result_df.isnull().sum().sum() == 0
        assert len(result_df) == 3  # One row dropped

    def test_preprocess_returns_valid_path(self, mock_input_data, tmp_path):
        """Verify component returns valid output path."""
        import os

        output_path = str(tmp_path / "output.parquet")

        result_path = preprocess_op(
            input_path=mock_input_data,
            output_path=output_path,
            config={}
        )

        assert os.path.exists(result_path)
        assert result_path == output_path


class TestPipelineDefinition:
    """Test pipeline structure and configuration."""

    def test_pipeline_has_required_components(self):
        """Verify pipeline includes all required steps."""
        @dsl.pipeline(name="test-pipeline")
        def ml_pipeline(input_data: str):
            preprocess = preprocess_component(input_path=input_data)
            train = train_component(data_path=preprocess.output)
            evaluate = evaluate_component(model_path=train.output)
            return evaluate.output

        # Compile and verify structure
        pipeline_spec = ml_pipeline.pipeline_spec

        assert len(pipeline_spec.components) >= 3
        component_names = [c for c in pipeline_spec.components.keys()]
        assert "preprocess" in str(component_names).lower()
        assert "train" in str(component_names).lower()
        assert "evaluate" in str(component_names).lower()

    def test_pipeline_parameter_validation(self):
        """Verify pipeline validates required parameters."""
        @dsl.pipeline(name="parameterized-pipeline")
        def ml_pipeline(
            input_data: str,
            learning_rate: float = 0.01,
            epochs: int = 10
        ):
            pass

        # Verify parameters are defined
        params = ml_pipeline.pipeline_spec.root.input_definitions.parameters
        assert "input_data" in params
        assert "learning_rate" in params
        assert "epochs" in params
```

**Why compliant:** Tests pipeline components in isolation using temporary files, verifies component outputs, tests pipeline structure separately from execution, and uses mocks to avoid external dependencies.

---

## VIOLATION: Testing Entire Pipeline as Single Unit

```python
import mlflow
from pipelines.full_pipeline import run_full_pipeline


def test_pipeline():
    """Test the entire ML pipeline."""
    # This test does everything at once
    result = run_full_pipeline(
        data_source="s3://production/raw-data/",
        model_registry="production",
        deploy_to="staging"
    )

    # Vague assertions
    assert result is not None
    assert result["status"] == "success"


def test_model_training():
    """Test model training with production data."""
    # Uses production data - non-deterministic
    mlflow.set_tracking_uri("http://production-mlflow:5000")

    with mlflow.start_run():
        # Train on actual production data
        model = train_on_production_data()

        # Log to production MLflow - side effect!
        mlflow.sklearn.log_model(model, "model")

        # Assert model exists
        assert model is not None
```

**Why violates ENG-4.1:** This test violates atomic TDD by: (1) testing the entire pipeline instead of individual components, (2) using production data making tests non-deterministic, (3) having side effects by logging to production MLflow, (4) having vague assertions that don't verify specific behaviors, and (5) not isolating components for independent testing.

---

## VIOLATION: No Mocking of External Dependencies

```python
from components.data_loader import load_from_s3
from components.model_registry import register_model


def test_data_loading():
    """Test data loading from S3."""
    # Directly calls S3 - requires credentials, network
    data = load_from_s3("s3://my-bucket/data/training.parquet")

    assert len(data) > 0


def test_model_registration():
    """Test model registration to MLflow."""
    # Directly calls MLflow server
    model = train_simple_model()

    # Registers to actual MLflow - permanent side effect
    model_uri = register_model(
        model=model,
        name="test-model",
        registry_uri="http://mlflow:5000"
    )

    assert "models:/" in model_uri


def test_kubeflow_submission():
    """Test pipeline submission to Kubeflow."""
    from kfp import Client

    # Connects to actual Kubeflow cluster
    client = Client(host="http://kubeflow.company.com")

    # Submits actual pipeline run
    run = client.create_run_from_pipeline_func(
        my_pipeline,
        arguments={"data": "s3://bucket/data"}
    )

    # Waits for actual execution
    client.wait_for_run_completion(run.run_id, timeout=3600)

    assert run.run.status == "Succeeded"
```

**Why violates ENG-4.1:** This violates atomic TDD by: (1) not mocking external services (S3, MLflow, Kubeflow), (2) requiring network access and credentials to run tests, (3) creating permanent side effects in external systems, (4) making tests slow and flaky due to external dependencies, and (5) not being isolated or reproducible.

---

## COMPLIANT: Testing MLflow Experiment Tracking

```python
import pytest
import mlflow
from unittest.mock import Mock, patch, MagicMock
import tempfile
import os


@pytest.fixture
def mock_mlflow_client():
    """Create mock MLflow client."""
    with patch("mlflow.tracking.MlflowClient") as mock:
        yield mock.return_value


@pytest.fixture
def local_mlflow_tracking(tmp_path):
    """Set up local MLflow tracking for tests."""
    tracking_uri = f"file://{tmp_path}/mlruns"
    mlflow.set_tracking_uri(tracking_uri)
    yield tracking_uri
    mlflow.set_tracking_uri("")


class TestExperimentTracking:
    """Test MLflow experiment tracking functionality."""

    def test_logs_hyperparameters(self, local_mlflow_tracking):
        """Verify hyperparameters are logged correctly."""
        hyperparams = {
            "learning_rate": 0.01,
            "batch_size": 32,
            "epochs": 10
        }

        with mlflow.start_run() as run:
            for key, value in hyperparams.items():
                mlflow.log_param(key, value)
            run_id = run.info.run_id

        # Verify params were logged
        logged_run = mlflow.get_run(run_id)
        for key, value in hyperparams.items():
            assert logged_run.data.params[key] == str(value)

    def test_logs_metrics_over_epochs(self, local_mlflow_tracking):
        """Verify metrics are logged with steps."""
        with mlflow.start_run() as run:
            for epoch in range(5):
                mlflow.log_metric("loss", 1.0 / (epoch + 1), step=epoch)
                mlflow.log_metric("accuracy", 0.5 + epoch * 0.1, step=epoch)
            run_id = run.info.run_id

        # Verify metric history
        client = mlflow.tracking.MlflowClient()
        loss_history = client.get_metric_history(run_id, "loss")

        assert len(loss_history) == 5
        assert loss_history[0].value == 1.0
        assert loss_history[4].value == 0.2

    def test_logs_artifacts(self, local_mlflow_tracking, tmp_path):
        """Verify artifacts are logged correctly."""
        # Create test artifact
        artifact_path = tmp_path / "test_artifact.json"
        artifact_path.write_text('{"key": "value"}')

        with mlflow.start_run() as run:
            mlflow.log_artifact(str(artifact_path))
            run_id = run.info.run_id

        # Verify artifact exists
        client = mlflow.tracking.MlflowClient()
        artifacts = client.list_artifacts(run_id)

        assert len(artifacts) == 1
        assert artifacts[0].path == "test_artifact.json"


class TestModelRegistry:
    """Test MLflow model registry operations."""

    def test_registers_model_version(self, mock_mlflow_client):
        """Verify model registration creates version."""
        mock_mlflow_client.create_registered_model.return_value = Mock(name="test-model")
        mock_mlflow_client.create_model_version.return_value = Mock(version="1")

        from components.model_registry import register_new_model

        version = register_new_model(
            client=mock_mlflow_client,
            model_name="test-model",
            run_id="abc123",
            artifact_path="model"
        )

        mock_mlflow_client.create_model_version.assert_called_once()
        assert version == "1"

    def test_transitions_model_stage(self, mock_mlflow_client):
        """Verify model stage transitions work."""
        mock_mlflow_client.transition_model_version_stage.return_value = None

        from components.model_registry import promote_model

        promote_model(
            client=mock_mlflow_client,
            model_name="test-model",
            version="1",
            stage="Production"
        )

        mock_mlflow_client.transition_model_version_stage.assert_called_once_with(
            name="test-model",
            version="1",
            stage="Production"
        )
```

**Why compliant:** Uses local file-based MLflow tracking for isolation, mocks external MLflow client calls, tests specific behaviors (parameter logging, metric history, artifacts), and avoids any production side effects.

---

## TDD Cycle Commands

```bash
# RED: Run specific test, see it fail
pytest tests/tracking/test_experiment.py::test_logs_parameters -v

# GREEN: Write code, run test again
pytest tests/tracking/test_experiment.py::test_logs_parameters -v

# REFACTOR: Run all unit tests
pytest tests/ -m "not integration"

# VERIFY: Check coverage and constitutional compliance
pytest --cov=src --cov-fail-under=80
constitution-lint .

# Commit when green and compliant
git add -A && git commit -m "Add parameter logging to ExperimentTracker"
```

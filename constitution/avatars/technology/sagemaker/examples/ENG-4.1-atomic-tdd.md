---
law_id: ENG-4.1
avatar: sagemaker
---

# ENG-4.1: Atomic TDD Examples for Amazon SageMaker

## COMPLIANT: Unit Testing SageMaker Training Scripts

```python
import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
import json
import os
import tempfile


# Training script module
# scripts/train.py
def parse_args():
    """Parse training arguments."""
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-dir", type=str, default=os.environ.get("SM_MODEL_DIR", "/opt/ml/model"))
    parser.add_argument("--train", type=str, default=os.environ.get("SM_CHANNEL_TRAIN", "/opt/ml/input/data/train"))
    parser.add_argument("--n-estimators", type=int, default=100)
    parser.add_argument("--max-depth", type=int, default=10)
    return parser.parse_args()


def load_data(train_path):
    """Load training data from SageMaker channel."""
    import pandas as pd
    return pd.read_csv(os.path.join(train_path, "train.csv"))


def train_model(X, y, n_estimators, max_depth):
    """Train the model."""
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth)
    model.fit(X, y)
    return model


# Test file: tests/test_train.py
class TestSageMakerTrainingScript:
    """Unit tests for SageMaker training script."""

    @pytest.fixture
    def sample_training_data(self, tmp_path):
        """Create sample training data in SageMaker format."""
        df = pd.DataFrame({
            "feature_1": np.random.randn(100),
            "feature_2": np.random.randn(100),
            "feature_3": np.random.randn(100),
            "target": np.random.randint(0, 2, 100)
        })
        train_dir = tmp_path / "train"
        train_dir.mkdir()
        df.to_csv(train_dir / "train.csv", index=False)
        return str(train_dir)

    @pytest.fixture
    def model_dir(self, tmp_path):
        """Create temporary model directory."""
        model_dir = tmp_path / "model"
        model_dir.mkdir()
        return str(model_dir)

    def test_load_data_reads_csv(self, sample_training_data):
        """Verify data loading from SageMaker channel."""
        from scripts.train import load_data

        df = load_data(sample_training_data)

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 100
        assert "target" in df.columns

    def test_train_model_returns_fitted_model(self):
        """Verify training returns a fitted model."""
        from scripts.train import train_model

        X = np.random.randn(50, 3)
        y = np.random.randint(0, 2, 50)

        model = train_model(X, y, n_estimators=10, max_depth=5)

        assert hasattr(model, "predict")
        assert model.n_estimators == 10
        assert model.max_depth == 5

    def test_train_model_can_predict(self):
        """Verify trained model can make predictions."""
        from scripts.train import train_model

        X_train = np.random.randn(50, 3)
        y_train = np.random.randint(0, 2, 50)
        X_test = np.random.randn(10, 3)

        model = train_model(X_train, y_train, n_estimators=10, max_depth=5)
        predictions = model.predict(X_test)

        assert len(predictions) == 10
        assert all(p in [0, 1] for p in predictions)

    def test_parse_args_uses_environment_defaults(self, monkeypatch):
        """Verify argument parsing respects SageMaker environment."""
        from scripts.train import parse_args

        monkeypatch.setenv("SM_MODEL_DIR", "/opt/ml/model")
        monkeypatch.setenv("SM_CHANNEL_TRAIN", "/opt/ml/input/data/train")

        with patch("sys.argv", ["train.py"]):
            args = parse_args()

        assert args.model_dir == "/opt/ml/model"
        assert args.train == "/opt/ml/input/data/train"


class TestSageMakerInferenceScript:
    """Unit tests for SageMaker inference script."""

    @pytest.fixture
    def mock_model(self):
        """Create a mock model for testing."""
        model = Mock()
        model.predict.return_value = np.array([0, 1, 0])
        model.predict_proba.return_value = np.array([
            [0.8, 0.2],
            [0.3, 0.7],
            [0.9, 0.1]
        ])
        return model

    def test_model_fn_loads_model(self, tmp_path):
        """Verify model_fn loads serialized model."""
        from scripts.inference import model_fn
        import joblib
        from sklearn.ensemble import RandomForestClassifier

        # Save a model
        model = RandomForestClassifier(n_estimators=5)
        model.fit([[1, 2], [3, 4]], [0, 1])
        model_path = tmp_path / "model.joblib"
        joblib.dump(model, model_path)

        # Load it
        loaded_model = model_fn(str(tmp_path))

        assert hasattr(loaded_model, "predict")

    def test_input_fn_parses_json(self):
        """Verify input_fn parses JSON request body."""
        from scripts.inference import input_fn

        request_body = json.dumps({
            "instances": [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
        })

        data = input_fn(request_body, "application/json")

        assert isinstance(data, np.ndarray)
        assert data.shape == (2, 3)

    def test_predict_fn_returns_predictions(self, mock_model):
        """Verify predict_fn returns model predictions."""
        from scripts.inference import predict_fn

        input_data = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]])

        predictions = predict_fn(input_data, mock_model)

        mock_model.predict.assert_called_once()
        assert len(predictions) == 3

    def test_output_fn_formats_json(self):
        """Verify output_fn formats predictions as JSON."""
        from scripts.inference import output_fn

        predictions = np.array([0, 1, 0])

        response_body, content_type = output_fn(predictions, "application/json")

        assert content_type == "application/json"
        parsed = json.loads(response_body)
        assert "predictions" in parsed
```

**Why compliant:** Tests each function in the training/inference scripts independently, uses fixtures for data setup, mocks external dependencies, follows SageMaker's expected function signatures (model_fn, input_fn, predict_fn, output_fn), and tests edge cases.

---

## COMPLIANT: Testing SageMaker Processing Jobs

```python
import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch
import tempfile
import os


class TestPreprocessingScript:
    """Tests for SageMaker Processing script."""

    @pytest.fixture
    def raw_data(self, tmp_path):
        """Create raw input data."""
        df = pd.DataFrame({
            "customer_id": ["C001", "C002", "C003", "C004"],
            "age": [25, None, 35, 45],
            "income": [50000.0, 75000.0, None, 100000.0],
            "category": ["A", "B", "A", "C"],
            "target": [0, 1, 0, 1]
        })
        input_dir = tmp_path / "input"
        input_dir.mkdir()
        df.to_csv(input_dir / "raw_data.csv", index=False)
        return str(input_dir)

    @pytest.fixture
    def output_dirs(self, tmp_path):
        """Create output directories."""
        train_dir = tmp_path / "output" / "train"
        test_dir = tmp_path / "output" / "test"
        train_dir.mkdir(parents=True)
        test_dir.mkdir(parents=True)
        return str(train_dir), str(test_dir)

    def test_imputes_missing_values(self, raw_data):
        """Verify missing values are imputed."""
        from scripts.preprocess import impute_missing_values

        df = pd.read_csv(os.path.join(raw_data, "raw_data.csv"))

        result = impute_missing_values(df, numeric_strategy="median")

        assert result["age"].isnull().sum() == 0
        assert result["income"].isnull().sum() == 0

    def test_encodes_categorical_columns(self, raw_data):
        """Verify categorical columns are encoded."""
        from scripts.preprocess import encode_categoricals

        df = pd.read_csv(os.path.join(raw_data, "raw_data.csv"))

        result, encoder = encode_categoricals(df, columns=["category"])

        assert "category" not in result.columns or result["category"].dtype in [np.int64, np.float64]
        assert encoder is not None

    def test_splits_data_correctly(self, raw_data):
        """Verify train/test split ratios."""
        from scripts.preprocess import split_data

        df = pd.read_csv(os.path.join(raw_data, "raw_data.csv"))

        train_df, test_df = split_data(df, test_size=0.25, random_state=42)

        assert len(train_df) == 3
        assert len(test_df) == 1

    def test_preserves_column_order(self, raw_data):
        """Verify preprocessing preserves expected column order."""
        from scripts.preprocess import preprocess_pipeline

        df = pd.read_csv(os.path.join(raw_data, "raw_data.csv"))
        expected_columns = ["age", "income", "category_encoded", "target"]

        result = preprocess_pipeline(df)

        # Target should be last column for SageMaker
        assert result.columns[-1] == "target"

    def test_saves_artifacts(self, raw_data, output_dirs, tmp_path):
        """Verify preprocessing saves required artifacts."""
        from scripts.preprocess import run_preprocessing

        train_dir, test_dir = output_dirs
        artifacts_dir = tmp_path / "artifacts"
        artifacts_dir.mkdir()

        run_preprocessing(
            input_path=raw_data,
            train_output=train_dir,
            test_output=test_dir,
            artifacts_output=str(artifacts_dir)
        )

        # Check outputs exist
        assert os.path.exists(os.path.join(train_dir, "train.csv"))
        assert os.path.exists(os.path.join(test_dir, "test.csv"))
        assert os.path.exists(os.path.join(str(artifacts_dir), "encoder.joblib"))


class TestSageMakerPipelineSteps:
    """Tests for SageMaker Pipeline step definitions."""

    @pytest.fixture
    def mock_sagemaker_session(self):
        """Create mock SageMaker session."""
        session = Mock()
        session.default_bucket.return_value = "test-bucket"
        session.boto_region_name = "us-east-1"
        return session

    def test_processing_step_configuration(self, mock_sagemaker_session):
        """Verify processing step is configured correctly."""
        from pipelines.training_pipeline import create_processing_step

        step = create_processing_step(
            session=mock_sagemaker_session,
            instance_type="ml.m5.xlarge",
            input_data="s3://bucket/data/"
        )

        assert step.name == "PreprocessingStep"
        assert "ml.m5.xlarge" in str(step.processor.instance_type)

    def test_training_step_uses_correct_estimator(self, mock_sagemaker_session):
        """Verify training step uses correct estimator configuration."""
        from pipelines.training_pipeline import create_training_step

        step = create_training_step(
            session=mock_sagemaker_session,
            instance_type="ml.m5.xlarge",
            hyperparameters={"n_estimators": 100}
        )

        assert step.name == "TrainingStep"
        assert step.estimator.hyperparameters()["n_estimators"] == 100
```

**Why compliant:** Tests preprocessing functions in isolation, verifies SageMaker-specific requirements (column ordering, artifact saving), uses fixtures for test data, mocks SageMaker session for pipeline step tests, and tests both data transformations and pipeline configuration.

---

## VIOLATION: Testing Against Live SageMaker Infrastructure

```python
import sagemaker
from sagemaker.sklearn import SKLearn


def test_training_job():
    """Test by running actual SageMaker training job."""
    # Creates actual AWS resources!
    session = sagemaker.Session()

    sklearn_estimator = SKLearn(
        entry_point="train.py",
        role="arn:aws:iam::123456789:role/SageMakerRole",
        instance_count=1,
        instance_type="ml.m5.xlarge",
        framework_version="1.0-1",
        sagemaker_session=session
    )

    # Runs actual training job - costs money, takes time
    sklearn_estimator.fit({
        "train": "s3://my-bucket/train-data/"
    })

    # Vague assertion
    assert sklearn_estimator.latest_training_job is not None


def test_endpoint_deployment():
    """Test by deploying actual endpoint."""
    session = sagemaker.Session()

    # Deploy actual endpoint - costs money, creates resources
    predictor = sagemaker.predictor.Predictor(
        endpoint_name="test-endpoint",
        sagemaker_session=session
    )

    # Make actual prediction
    result = predictor.predict([[1, 2, 3]])

    assert result is not None
```

**Why violates ENG-4.1:** This violates atomic TDD by: (1) creating actual AWS resources costing money, (2) requiring live AWS credentials and network, (3) taking minutes/hours instead of milliseconds, (4) not testing specific logic but infrastructure, (5) having vague assertions that don't verify business logic, and (6) being non-deterministic due to external dependencies.

---

## VIOLATION: Untestable Training Script

```python
# scripts/train.py - Untestable monolithic script

import argparse
import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import boto3


if __name__ == "__main__":
    # All logic in main block - cannot be imported for testing

    parser = argparse.ArgumentParser()
    parser.add_argument("--train", type=str)
    parser.add_argument("--model-dir", type=str)
    args = parser.parse_args()

    # Direct file reads - no abstraction
    df = pd.read_csv(os.path.join(args.train, "train.csv"))

    # Hardcoded preprocessing - not testable
    df = df.fillna(0)
    X = df.drop("target", axis=1).values
    y = df["target"].values

    # Hardcoded hyperparameters
    model = RandomForestClassifier(n_estimators=100, max_depth=10)
    model.fit(X, y)

    # Direct AWS calls - not mockable
    s3 = boto3.client("s3")
    s3.put_object(
        Bucket="my-bucket",
        Key="models/latest.joblib",
        Body=joblib.dumps(model)
    )

    joblib.dump(model, os.path.join(args.model_dir, "model.joblib"))
    print("Done!")
```

**Why violates ENG-4.1:** This script violates atomic TDD by: (1) putting all logic in `if __name__ == "__main__"` making functions not importable for testing, (2) hardcoding dependencies like boto3 without abstraction, (3) mixing data loading, preprocessing, training, and saving in one block, (4) no separation of concerns allowing unit testing, and (5) direct AWS calls that cannot be mocked without modifying the script.

---

## COMPLIANT: Testing SageMaker Feature Store Integration

```python
import pytest
from unittest.mock import Mock, patch, MagicMock
import pandas as pd
import numpy as np
from datetime import datetime


class TestFeatureStoreIntegration:
    """Tests for SageMaker Feature Store operations."""

    @pytest.fixture
    def mock_feature_store_session(self):
        """Create mock Feature Store session."""
        session = Mock()
        session.boto_region_name = "us-east-1"
        return session

    @pytest.fixture
    def sample_features(self):
        """Create sample feature data."""
        return pd.DataFrame({
            "customer_id": ["C001", "C002", "C003"],
            "avg_order_value": [100.0, 150.0, 200.0],
            "order_count": [5, 10, 15],
            "days_since_last_order": [7, 14, 21],
            "event_time": [datetime.now()] * 3
        })

    def test_feature_definitions_match_schema(self, sample_features):
        """Verify feature definitions match DataFrame schema."""
        from features.customer_features import get_feature_definitions

        definitions = get_feature_definitions()

        # Check all DataFrame columns have definitions
        for col in sample_features.columns:
            if col != "event_time":  # event_time is handled separately
                assert any(d.feature_name == col for d in definitions), \
                    f"Missing definition for {col}"

    def test_feature_transformation_is_deterministic(self):
        """Verify feature transformations produce consistent results."""
        from features.customer_features import compute_features

        raw_data = pd.DataFrame({
            "customer_id": ["C001"],
            "orders": [{"amount": 100}, {"amount": 200}]
        })

        result1 = compute_features(raw_data)
        result2 = compute_features(raw_data)

        pd.testing.assert_frame_equal(result1, result2)

    def test_validates_feature_types(self, sample_features):
        """Verify feature types are validated before ingestion."""
        from features.customer_features import validate_features

        # Valid data should pass
        assert validate_features(sample_features) is True

        # Invalid types should fail
        invalid_features = sample_features.copy()
        invalid_features["avg_order_value"] = "not a number"

        with pytest.raises(ValueError, match="type mismatch"):
            validate_features(invalid_features)

    @patch("sagemaker.feature_store.feature_group.FeatureGroup")
    def test_ingestion_batches_large_datasets(
        self,
        mock_feature_group,
        sample_features
    ):
        """Verify large datasets are batched for ingestion."""
        from features.customer_features import ingest_features

        # Create large dataset
        large_features = pd.concat([sample_features] * 1000, ignore_index=True)

        mock_fg = Mock()
        mock_feature_group.return_value = mock_fg

        ingest_features(
            feature_group=mock_fg,
            features=large_features,
            batch_size=500
        )

        # Should be called multiple times for batching
        assert mock_fg.ingest.call_count >= 2
```

**Why compliant:** Mocks SageMaker Feature Store classes, tests feature transformation logic independently, verifies type validation, tests batching behavior without actual AWS calls, and uses fixtures for consistent test data.

---

## TDD Cycle Commands

```bash
# RED: Run specific test, see it fail
pytest tests/training/test_estimator.py::test_creates_training_job -v

# GREEN: Write code, run test again
pytest tests/training/test_estimator.py::test_creates_training_job -v

# REFACTOR: Run all unit tests
pytest tests/ -m "not integration"

# VERIFY: Check coverage and constitutional compliance
pytest --cov=src --cov-fail-under=80
constitution-lint .

# Commit when green and compliant
git add -A && git commit -m "Add training job creation to SageMakerEstimator"
```

# ML/Analytics Guidance

> **Purpose:** Stack-specific agent behaviors for Machine Learning and Data Analytics projects.

---

## Overview

This guidance provides patterns for AI agents working with Machine Learning and Analytics projects. It covers testing patterns for ML code, experiment tracking, data validation, and reproducibility concerns.

---

## Testing Framework

**Primary Framework:** pytest + pytest-cov + great_expectations (data validation)

### Test Structure

```python
import pytest
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from myproject.models.classifier import OrderClassifier
from myproject.features.transformers import OrderFeatureTransformer

class TestOrderClassifier:
    """Tests for the OrderClassifier model."""

    @pytest.fixture
    def sample_data(self):
        """Fixture providing sample training data."""
        return pd.DataFrame({
            'total': [100, 200, 50, 500, 75],
            'item_count': [2, 5, 1, 10, 3],
            'customer_age_days': [30, 365, 7, 1000, 60],
            'is_returning': [0, 1, 0, 1, 0],
            'label': [0, 1, 0, 1, 0]  # 0=low_risk, 1=high_value
        })

    @pytest.fixture
    def trained_model(self, sample_data):
        """Fixture providing a trained model."""
        X = sample_data.drop('label', axis=1)
        y = sample_data['label']
        model = OrderClassifier()
        model.fit(X, y)
        return model

    def test_model_can_be_trained(self, sample_data):
        """Model training should complete without errors."""
        # Arrange
        X = sample_data.drop('label', axis=1)
        y = sample_data['label']
        model = OrderClassifier()

        # Act
        model.fit(X, y)

        # Assert
        assert model.is_fitted

    def test_model_predictions_are_valid(self, trained_model, sample_data):
        """Model predictions should be valid class labels."""
        # Arrange
        X = sample_data.drop('label', axis=1)

        # Act
        predictions = trained_model.predict(X)

        # Assert
        assert len(predictions) == len(X)
        assert all(p in [0, 1] for p in predictions)

    def test_model_accuracy_above_threshold(self, sample_data):
        """Model should achieve minimum accuracy threshold."""
        # Arrange
        X = sample_data.drop('label', axis=1)
        y = sample_data['label']
        model = OrderClassifier()

        # Act
        model.fit(X, y)
        predictions = model.predict(X)
        accuracy = accuracy_score(y, predictions)

        # Assert
        assert accuracy >= 0.6, f"Accuracy {accuracy} below threshold 0.6"


class TestOrderFeatureTransformer:
    """Tests for feature transformation."""

    def test_transformer_creates_expected_features(self):
        """Transformer should create all expected features."""
        # Arrange
        raw_data = pd.DataFrame({
            'order_total': [100.0],
            'order_date': ['2024-01-15'],
            'customer_id': ['cust-123']
        })
        transformer = OrderFeatureTransformer()

        # Act
        features = transformer.transform(raw_data)

        # Assert
        expected_columns = ['total_normalized', 'day_of_week', 'is_weekend']
        for col in expected_columns:
            assert col in features.columns, f"Missing feature: {col}"

    def test_transformer_handles_missing_values(self):
        """Transformer should handle missing values gracefully."""
        # Arrange
        raw_data = pd.DataFrame({
            'order_total': [100.0, None, 200.0],
            'order_date': ['2024-01-15', '2024-01-16', None]
        })
        transformer = OrderFeatureTransformer()

        # Act
        features = transformer.transform(raw_data)

        # Assert
        assert not features.isnull().any().any(), "Features contain null values"
```

### Data Validation Tests

```python
import great_expectations as gx
import pytest

class TestDataQuality:
    """Tests for data quality validation."""

    @pytest.fixture
    def orders_data(self):
        """Load orders dataset."""
        return pd.read_parquet("data/raw/orders.parquet")

    def test_orders_schema(self, orders_data):
        """Orders data should have expected schema."""
        expected_columns = ['order_id', 'customer_id', 'total', 'created_at']
        assert all(col in orders_data.columns for col in expected_columns)

    def test_orders_no_duplicate_ids(self, orders_data):
        """Order IDs should be unique."""
        assert orders_data['order_id'].is_unique

    def test_orders_total_positive(self, orders_data):
        """Order totals should be positive."""
        assert (orders_data['total'] >= 0).all()

    def test_orders_data_expectations(self, orders_data):
        """Validate data with Great Expectations."""
        context = gx.get_context()
        validator = context.sources.pandas_default.read_dataframe(orders_data)

        validator.expect_column_values_to_not_be_null("order_id")
        validator.expect_column_values_to_be_unique("order_id")
        validator.expect_column_values_to_be_between("total", min_value=0)

        results = validator.validate()
        assert results.success, f"Data validation failed: {results}"
```

---

## Common Patterns

### Good Patterns

**Reproducibility:**

```python
import random
import numpy as np
import torch

def set_seed(seed: int = 42):
    """Set random seeds for reproducibility."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

# Configuration-driven experiments
import yaml

def load_config(config_path: str) -> dict:
    with open(config_path) as f:
        return yaml.safe_load(f)

# configs/model_config.yaml
# model:
#   type: "random_forest"
#   n_estimators: 100
#   max_depth: 10
#   random_state: 42
```

**Experiment Tracking:**

```python
import mlflow
from mlflow.tracking import MlflowClient

class ExperimentTracker:
    """Wrapper for experiment tracking."""

    def __init__(self, experiment_name: str):
        mlflow.set_experiment(experiment_name)
        self.client = MlflowClient()

    def log_params(self, params: dict):
        for key, value in params.items():
            mlflow.log_param(key, value)

    def log_metrics(self, metrics: dict, step: int = None):
        for key, value in metrics.items():
            mlflow.log_metric(key, value, step=step)

    def log_model(self, model, artifact_path: str):
        mlflow.sklearn.log_model(model, artifact_path)

    def log_artifact(self, local_path: str):
        mlflow.log_artifact(local_path)


# Usage in training
def train_model(config: dict):
    with mlflow.start_run():
        tracker = ExperimentTracker("order-classification")

        # Log configuration
        tracker.log_params(config['model'])

        # Train model
        model = OrderClassifier(**config['model'])
        model.fit(X_train, y_train)

        # Log metrics
        metrics = evaluate_model(model, X_test, y_test)
        tracker.log_metrics(metrics)

        # Log model
        tracker.log_model(model, "model")

        return model, metrics
```

**Data Pipeline:**

```python
from abc import ABC, abstractmethod
import pandas as pd

class DataTransformer(ABC):
    """Base class for data transformers."""

    @abstractmethod
    def fit(self, data: pd.DataFrame) -> "DataTransformer":
        """Fit transformer to data."""
        pass

    @abstractmethod
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """Transform data."""
        pass

    def fit_transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """Fit and transform data."""
        return self.fit(data).transform(data)


class OrderFeatureTransformer(DataTransformer):
    """Transform raw order data into features."""

    def __init__(self):
        self._total_mean = None
        self._total_std = None

    def fit(self, data: pd.DataFrame) -> "OrderFeatureTransformer":
        self._total_mean = data['order_total'].mean()
        self._total_std = data['order_total'].std()
        return self

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        features = pd.DataFrame()

        # Normalize total
        features['total_normalized'] = (
            (data['order_total'] - self._total_mean) / self._total_std
        )

        # Extract date features
        dates = pd.to_datetime(data['order_date'])
        features['day_of_week'] = dates.dt.dayofweek
        features['is_weekend'] = features['day_of_week'].isin([5, 6]).astype(int)

        return features
```

---

## Anti-Patterns to Avoid

### Data Leakage

```python
# BAD - Fitting transformer on all data before split
transformer = StandardScaler()
X_scaled = transformer.fit_transform(X)  # Uses all data!
X_train, X_test = train_test_split(X_scaled, y)

# GOOD - Fit only on training data
X_train, X_test, y_train, y_test = train_test_split(X, y)
transformer = StandardScaler()
X_train_scaled = transformer.fit_transform(X_train)
X_test_scaled = transformer.transform(X_test)  # Transform only
```

### Hardcoded Magic Numbers

```python
# BAD - Magic numbers in code
if accuracy > 0.85:  # Why 0.85?
    deploy_model(model)

# GOOD - Configuration-driven thresholds
config = {
    'deployment': {
        'min_accuracy': 0.85,
        'max_latency_ms': 100
    }
}

if accuracy > config['deployment']['min_accuracy']:
    deploy_model(model)
```

### No Versioning

```python
# BAD - Overwriting models without versioning
model.save("model.pkl")  # Previous version lost!

# GOOD - Versioned model artifacts
import datetime

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
model_path = f"models/trained/classifier_{timestamp}.pkl"
model.save(model_path)

# Log with MLflow for tracking
mlflow.log_artifact(model_path)
```

---

## Tools and Commands

### Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run Jupyter for exploration
jupyter lab

# Start MLflow UI
mlflow ui
```

### Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=src --cov-report=html

# Run specific tests
pytest tests/models/

# Run with markers
pytest -m "not slow"
```

### Data Pipeline

```bash
# DVC commands
dvc init
dvc add data/raw/orders.csv
dvc run -n preprocess -d src/data/preprocess.py -o data/processed python src/data/preprocess.py
dvc repro  # Reproduce pipeline

# Data validation
great_expectations init
great_expectations checkpoint run orders_checkpoint
```

---

## ML-Specific Guidance

### Model Testing Hierarchy

1. **Unit Tests** - Test individual components
   - Feature transformers
   - Data validators
   - Utility functions

2. **Integration Tests** - Test pipelines
   - Training pipeline end-to-end
   - Inference pipeline
   - Data loading + transformation

3. **Model Performance Tests** - Test model quality
   - Accuracy/precision/recall thresholds
   - Latency requirements
   - Memory constraints

4. **Data Quality Tests** - Test data assumptions
   - Schema validation
   - Distribution checks
   - Missing value handling

### Production Readiness Checklist

```markdown
## Model Production Checklist

### Code Quality
- [ ] All tests pass
- [ ] Coverage > 80%
- [ ] No linting errors
- [ ] Code reviewed

### Model Quality
- [ ] Performance metrics meet thresholds
- [ ] No data leakage in pipeline
- [ ] Validated on holdout set
- [ ] Bias analysis complete

### Reproducibility
- [ ] Random seeds fixed
- [ ] Dependencies pinned
- [ ] Training data versioned (DVC)
- [ ] Model artifact logged (MLflow)

### Monitoring
- [ ] Input data validation
- [ ] Prediction logging
- [ ] Drift detection configured
- [ ] Alerting set up
```

---
skill:
  id: skill-17-ml-pipeline
  name: ML Pipeline
  category: mlops
  version: "2.0.0"

laws:
  implements:
    - id: ENG-5.2
      title: CI/CD Pipeline Law
    - id: BUS-3.3
      title: Data Lineage Law
  references:
    - id: BUS-7.1
      title: Audit Trail Law
    - id: ENG-5.1
      title: Infrastructure as Code Law

triggers:
  phrases:
    - "Build ML pipeline"
    - "Automate training"
    - "MLOps setup"
    - "Data pipeline design"

followed_by:
  - skill-18-experiment-tracking
  - skill-19-model-serving
---

# Skill: ML Pipeline Design

> **Purpose:** Design and implement end-to-end machine learning pipelines that are reproducible, automated, and production-ready.

---

## Purpose

ML Pipeline Design is the practice of orchestrating the complete machine learning workflow from data ingestion to model deployment. This skill ensures:

1. **Reproducibility** - Any experiment can be exactly recreated
2. **Automation** - Manual steps eliminated, human error reduced
3. **Scalability** - Pipelines handle growing data and model complexity
4. **Traceability** - Every artifact linked to its lineage
5. **Reliability** - Failures are detected, handled, and recoverable

**Key principle:** ML is software engineering. Pipelines are products, not notebooks.

---

## When to Invoke

Invoke this skill when:

- Starting a new ML project
- Transitioning from notebooks to production
- Scaling existing ML workflows
- Debugging training or data issues
- Establishing MLOps practices for a team

**Trigger phrases:**
- "How do we productionize this model?"
- "Our training isn't reproducible"
- "We need to automate the ML workflow"
- "Data scientists keep breaking each other's work"
- "Set up our ML infrastructure"

---

## Constitutional Foundation

### Engineering Constitution
- **Article II, Section 2.1** - Simplicity: Pipelines should be as simple as possible
- **Article IV, Section 4.1** - Test-First: Pipeline components tested
- **Article VI, Section 6.1** - Observability: Pipeline metrics and logging

### Business Constitution
- **Article III, Section 3.3** - Audit Trail: Model lineage tracked
- **Article IV, Section 4.1** - Continuity: Pipelines recoverable

---

## ML Pipeline Architecture

### Pipeline Stages

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Data      │────▶│  Feature    │────▶│  Training   │
│  Ingestion  │     │ Engineering │     │             │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                               │
┌─────────────┐     ┌─────────────┐     ┌──────▼──────┐
│   Deploy    │◀────│  Validate   │◀────│  Evaluate   │
│             │     │             │     │             │
└─────────────┘     └─────────────┘     └─────────────┘
```

### Stage 1: Data Ingestion

**Purpose:** Collect, validate, and version raw data.

```python
# Example: Data ingestion component
from dataclasses import dataclass
from datetime import datetime
import great_expectations as ge

@dataclass
class DataIngestionConfig:
    source_path: str
    destination_path: str
    schema_path: str
    timestamp: datetime = None

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config
        self.config.timestamp = datetime.utcnow()

    def ingest(self) -> str:
        """Ingest and validate raw data."""
        # Load data
        df = self._load_from_source()

        # Validate schema
        self._validate_schema(df)

        # Validate data quality
        self._validate_quality(df)

        # Version and store
        versioned_path = self._store_versioned(df)

        return versioned_path

    def _validate_schema(self, df):
        """Ensure data matches expected schema."""
        expected_schema = self._load_schema()
        for col, dtype in expected_schema.items():
            if col not in df.columns:
                raise ValueError(f"Missing column: {col}")
            if df[col].dtype != dtype:
                raise TypeError(f"Column {col} expected {dtype}, got {df[col].dtype}")

    def _validate_quality(self, df):
        """Run data quality checks."""
        ge_df = ge.from_pandas(df)

        # Example expectations
        ge_df.expect_column_values_to_not_be_null("user_id")
        ge_df.expect_column_values_to_be_between("age", 0, 120)
        ge_df.expect_column_values_to_be_unique("transaction_id")

        results = ge_df.validate()
        if not results.success:
            raise ValueError(f"Data quality check failed: {results}")
```

---

### Stage 2: Feature Engineering

**Purpose:** Transform raw data into ML-ready features.

```python
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

class FeatureEngineer(BaseEstimator, TransformerMixin):
    """Feature engineering pipeline component."""

    def __init__(self, config: dict):
        self.config = config
        self.fitted_values_ = {}

    def fit(self, X: pd.DataFrame, y=None):
        """Learn feature statistics from training data."""
        # Store statistics for reproducibility
        for col in self.config.get("normalize_cols", []):
            self.fitted_values_[f"{col}_mean"] = X[col].mean()
            self.fitted_values_[f"{col}_std"] = X[col].std()

        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Apply feature transformations."""
        X = X.copy()

        # Normalize numerical columns
        for col in self.config.get("normalize_cols", []):
            mean = self.fitted_values_[f"{col}_mean"]
            std = self.fitted_values_[f"{col}_std"]
            X[col] = (X[col] - mean) / std

        # One-hot encode categorical columns
        for col in self.config.get("categorical_cols", []):
            dummies = pd.get_dummies(X[col], prefix=col)
            X = pd.concat([X, dummies], axis=1)
            X = X.drop(col, axis=1)

        # Create interaction features
        for col1, col2 in self.config.get("interactions", []):
            X[f"{col1}_{col2}_interaction"] = X[col1] * X[col2]

        return X
```

**Feature Store Integration:**

```python
from feast import FeatureStore

class FeatureStoreManager:
    """Manage features in a feature store."""

    def __init__(self, repo_path: str):
        self.store = FeatureStore(repo_path=repo_path)

    def get_training_features(
        self,
        entity_df: pd.DataFrame,
        feature_refs: list[str]
    ) -> pd.DataFrame:
        """Retrieve features for training."""
        return self.store.get_historical_features(
            entity_df=entity_df,
            features=feature_refs
        ).to_df()

    def get_online_features(
        self,
        entity_rows: list[dict],
        feature_refs: list[str]
    ) -> dict:
        """Retrieve features for inference."""
        return self.store.get_online_features(
            entity_rows=entity_rows,
            features=feature_refs
        ).to_dict()
```

---

### Stage 3: Training

**Purpose:** Train models with tracked experiments.

```python
import mlflow
from sklearn.model_selection import cross_val_score

class ModelTrainer:
    """Train and track ML models."""

    def __init__(self, experiment_name: str):
        mlflow.set_experiment(experiment_name)

    def train(
        self,
        model,
        X_train,
        y_train,
        params: dict,
        tags: dict = None
    ) -> str:
        """Train model with full tracking."""

        with mlflow.start_run() as run:
            # Log parameters
            mlflow.log_params(params)

            # Log tags (data version, git commit, etc.)
            if tags:
                mlflow.set_tags(tags)

            # Train model
            model.set_params(**params)
            model.fit(X_train, y_train)

            # Cross-validation scores
            cv_scores = cross_val_score(model, X_train, y_train, cv=5)

            # Log metrics
            mlflow.log_metric("cv_mean", cv_scores.mean())
            mlflow.log_metric("cv_std", cv_scores.std())

            # Log model
            mlflow.sklearn.log_model(
                model,
                "model",
                registered_model_name=f"{model.__class__.__name__}"
            )

            # Log artifacts (feature importance, etc.)
            self._log_artifacts(model, X_train)

            return run.info.run_id

    def _log_artifacts(self, model, X_train):
        """Log additional artifacts."""
        if hasattr(model, "feature_importances_"):
            importance_df = pd.DataFrame({
                "feature": X_train.columns,
                "importance": model.feature_importances_
            }).sort_values("importance", ascending=False)

            importance_df.to_csv("feature_importance.csv", index=False)
            mlflow.log_artifact("feature_importance.csv")
```

---

### Stage 4: Evaluation

**Purpose:** Assess model quality against business requirements.

```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix
)
import matplotlib.pyplot as plt

class ModelEvaluator:
    """Evaluate models against multiple criteria."""

    def __init__(self, thresholds: dict):
        self.thresholds = thresholds

    def evaluate(
        self,
        model,
        X_test,
        y_test,
        model_type: str = "classification"
    ) -> dict:
        """Run comprehensive evaluation."""

        y_pred = model.predict(X_test)

        if model_type == "classification":
            metrics = self._evaluate_classification(y_test, y_pred, model, X_test)
        else:
            metrics = self._evaluate_regression(y_test, y_pred)

        # Check against thresholds
        metrics["passed"] = self._check_thresholds(metrics)

        return metrics

    def _evaluate_classification(self, y_true, y_pred, model, X_test):
        """Classification-specific metrics."""
        metrics = {
            "accuracy": accuracy_score(y_true, y_pred),
            "precision": precision_score(y_true, y_pred, average="weighted"),
            "recall": recall_score(y_true, y_pred, average="weighted"),
            "f1": f1_score(y_true, y_pred, average="weighted"),
        }

        # ROC-AUC if binary and has predict_proba
        if hasattr(model, "predict_proba") and len(set(y_true)) == 2:
            y_prob = model.predict_proba(X_test)[:, 1]
            metrics["roc_auc"] = roc_auc_score(y_true, y_prob)

        return metrics

    def _check_thresholds(self, metrics: dict) -> bool:
        """Check if metrics meet minimum thresholds."""
        for metric, threshold in self.thresholds.items():
            if metric in metrics and metrics[metric] < threshold:
                return False
        return True
```

---

### Stage 5: Validation

**Purpose:** Ensure model is safe for production deployment.

```python
class ModelValidator:
    """Validate model before deployment."""

    def __init__(self, baseline_metrics: dict):
        self.baseline_metrics = baseline_metrics

    def validate(
        self,
        new_metrics: dict,
        model,
        validation_data
    ) -> dict:
        """Run validation checks."""

        results = {
            "performance_check": self._check_performance(new_metrics),
            "regression_check": self._check_no_regression(new_metrics),
            "bias_check": self._check_fairness(model, validation_data),
            "latency_check": self._check_latency(model, validation_data),
        }

        results["approved"] = all(results.values())

        return results

    def _check_performance(self, metrics: dict) -> bool:
        """Check absolute performance thresholds."""
        return metrics.get("passed", False)

    def _check_no_regression(self, new_metrics: dict) -> bool:
        """Ensure new model isn't worse than baseline."""
        for metric, baseline_value in self.baseline_metrics.items():
            if metric in new_metrics:
                # Allow 2% degradation tolerance
                if new_metrics[metric] < baseline_value * 0.98:
                    return False
        return True

    def _check_fairness(self, model, data) -> bool:
        """Check for bias across protected groups."""
        # Implementation depends on fairness requirements
        # Example: Check equal opportunity across groups
        return True

    def _check_latency(self, model, data, max_latency_ms: float = 100) -> bool:
        """Check inference latency."""
        import time

        sample = data.sample(n=100)
        start = time.time()
        model.predict(sample)
        latency_ms = (time.time() - start) / 100 * 1000

        return latency_ms <= max_latency_ms
```

---

### Stage 6: Deployment

**Purpose:** Deploy validated models to production.

```python
class ModelDeployer:
    """Deploy models to serving infrastructure."""

    def __init__(self, registry_uri: str):
        self.registry_uri = registry_uri

    def deploy(
        self,
        model_name: str,
        model_version: str,
        deployment_config: dict
    ) -> dict:
        """Deploy model to production."""

        # Transition model stage in registry
        self._transition_stage(model_name, model_version, "Production")

        # Deploy based on strategy
        strategy = deployment_config.get("strategy", "rolling")

        if strategy == "canary":
            return self._deploy_canary(model_name, model_version, deployment_config)
        elif strategy == "blue_green":
            return self._deploy_blue_green(model_name, model_version, deployment_config)
        else:
            return self._deploy_rolling(model_name, model_version, deployment_config)

    def _deploy_canary(self, model_name, version, config) -> dict:
        """Canary deployment with gradual traffic shift."""
        return {
            "strategy": "canary",
            "initial_traffic_percent": config.get("canary_percent", 10),
            "model": model_name,
            "version": version,
            "status": "deployed"
        }
```

---

## Pipeline Orchestration

### Using Orchestration Frameworks

**Kubeflow Pipelines:**

```python
from kfp import dsl
from kfp.dsl import component, pipeline

@component
def ingest_data(source_path: str) -> str:
    """Data ingestion component."""
    # Implementation
    return versioned_data_path

@component
def engineer_features(data_path: str, config: dict) -> str:
    """Feature engineering component."""
    # Implementation
    return features_path

@component
def train_model(features_path: str, params: dict) -> str:
    """Training component."""
    # Implementation
    return model_uri

@component
def evaluate_model(model_uri: str, test_data_path: str) -> dict:
    """Evaluation component."""
    # Implementation
    return metrics

@pipeline(name="ml-training-pipeline")
def training_pipeline(
    source_path: str,
    feature_config: dict,
    training_params: dict
):
    """End-to-end training pipeline."""

    # Stage 1: Ingest
    ingest_task = ingest_data(source_path=source_path)

    # Stage 2: Features
    feature_task = engineer_features(
        data_path=ingest_task.output,
        config=feature_config
    )

    # Stage 3: Train
    train_task = train_model(
        features_path=feature_task.output,
        params=training_params
    )

    # Stage 4: Evaluate
    eval_task = evaluate_model(
        model_uri=train_task.output,
        test_data_path=feature_task.output
    )
```

**Airflow DAG:**

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "ml-team",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "ml_training_pipeline",
    default_args=default_args,
    schedule_interval="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["ml", "training"]
) as dag:

    ingest = PythonOperator(
        task_id="ingest_data",
        python_callable=ingest_data_fn,
    )

    features = PythonOperator(
        task_id="engineer_features",
        python_callable=engineer_features_fn,
    )

    train = PythonOperator(
        task_id="train_model",
        python_callable=train_model_fn,
    )

    evaluate = PythonOperator(
        task_id="evaluate_model",
        python_callable=evaluate_model_fn,
    )

    validate = PythonOperator(
        task_id="validate_model",
        python_callable=validate_model_fn,
    )

    deploy = PythonOperator(
        task_id="deploy_model",
        python_callable=deploy_model_fn,
    )

    ingest >> features >> train >> evaluate >> validate >> deploy
```

---

## Good Examples

### Example 1: Reproducible Training Config

```yaml
# pipeline_config.yaml
pipeline:
  name: customer-churn-prediction
  version: 1.2.0

data:
  source: s3://data-lake/customers/
  schema: schemas/customer_v2.json
  validation:
    - column: customer_id
      expectation: unique
    - column: tenure_months
      expectation: between
      min: 0
      max: 240

features:
  normalize:
    - tenure_months
    - monthly_charges
  categorical:
    - contract_type
    - payment_method
  interactions:
    - [tenure_months, monthly_charges]

training:
  model: xgboost.XGBClassifier
  params:
    max_depth: 6
    learning_rate: 0.1
    n_estimators: 100
  cv_folds: 5

evaluation:
  thresholds:
    accuracy: 0.85
    precision: 0.80
    recall: 0.75
    roc_auc: 0.90

deployment:
  strategy: canary
  canary_percent: 10
  promotion_threshold: 0.95
```

---

## Bad Examples (Anti-Patterns)

### Anti-Pattern 1: Notebook-Driven Pipeline

```python
# BAD - "Pipeline" as a series of notebook cells

# Cell 1
df = pd.read_csv("data.csv")  # Hardcoded path

# Cell 2
df = df.dropna()  # No validation

# Cell 3 - Run this twice if it fails
model.fit(X, y)  # No tracking

# Cell 4
model.predict(test)  # Where does test come from?

# Cell 5 - Copy model to server manually
```

**Correct approach:** Modular, tested pipeline components with full tracking.

---

### Anti-Pattern 2: No Data Versioning

```python
# BAD - Training on "latest" data
def train():
    data = load_data("s3://bucket/data/")  # Which version?
    model = train_model(data)
    save_model(model, "model.pkl")  # Which data was this trained on?
```

**Correct approach:** Version data and link to model artifacts.

---

## Quality Checklist

Before considering ML pipeline complete:

### Reproducibility
- [ ] All data versioned
- [ ] All code versioned
- [ ] All parameters logged
- [ ] Random seeds set
- [ ] Environment captured (requirements.txt/conda.yaml)

### Automation
- [ ] No manual steps required
- [ ] Pipeline triggered automatically
- [ ] Failures alert and retry appropriately

### Testing
- [ ] Data validation tests
- [ ] Feature engineering tests
- [ ] Model training smoke tests
- [ ] Integration tests for pipeline

### Observability
- [ ] Pipeline metrics tracked
- [ ] Alerts on failures
- [ ] Experiment tracking in place

---

## Skill Interactions

### Preceded By
- **15-Data Modeling** - Data schemas inform feature engineering
- **04-Business Domain Modeling** - Domain knowledge guides features

### Followed By
- **18-Experiment Tracking** - Track experiments within pipeline
- **19-Model Serving** - Deploy trained models

### Related Skills
- **13-Observability** - Pipeline monitoring
- **14-Technical Debt** - Pipeline debt management

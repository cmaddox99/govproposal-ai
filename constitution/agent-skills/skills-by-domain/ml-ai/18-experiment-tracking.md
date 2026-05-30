---
skill:
  id: skill-18-experiment-tracking
  name: Experiment Tracking
  category: mlops
  version: "2.0.0"

laws:
  implements:
    - id: PRD-5.3
      title: Experiment Design Law
    - id: BUS-7.1
      title: Audit Trail Law
  references:
    - id: BUS-3.3
      title: Data Lineage Law
    - id: PRD-5.2
      title: Hypothesis-Driven Law

triggers:
  phrases:
    - "Track experiments"
    - "Compare models"
    - "MLflow setup"
    - "Experiment reproducibility"

followed_by:
  - skill-19-model-serving
  - skill-20-ml-monitoring
---

# Skill: Experiment Tracking

> **Purpose:** Systematically track, compare, and reproduce machine learning experiments to accelerate model development and ensure scientific rigor.

---

## Purpose

Experiment Tracking is the practice of recording all aspects of ML experiments to enable comparison, reproduction, and collaboration. This skill ensures:

1. **Reproducibility** - Any experiment can be exactly recreated
2. **Comparison** - Models compared fairly on same data splits
3. **Collaboration** - Team shares experiments and learns from each other
4. **Lineage** - Models traced back to data, code, and parameters
5. **Governance** - Audit trail for model decisions

**Key principle:** If you can't reproduce it, you can't trust it. Track everything.

---

## When to Invoke

Invoke this skill when:

- Starting any ML experimentation
- Comparing multiple model approaches
- Debugging model performance issues
- Preparing models for production
- Onboarding new team members to ML projects
- Conducting model audits

**Trigger phrases:**
- "Which model performed best?"
- "Can you reproduce that result?"
- "What parameters did we use?"
- "Show me the experiment history"
- "Why did we choose this model?"

---

## Constitutional Foundation

### Engineering Constitution
- **Article IV, Section 4.1** - Test-First: Experiments have clear hypotheses
- **Article VI, Section 6.1** - Observability: Experiment metrics visible

### Business Constitution
- **Article III, Section 3.3** - Audit Trail: Model decisions traceable
- **Article IV, Section 4.1** - Continuity: Knowledge preserved

---

## Experiment Tracking Fundamentals

### What to Track

```
┌─────────────────────────────────────────────────────────────┐
│                    EXPERIMENT RECORD                         │
├─────────────────────────────────────────────────────────────┤
│  Metadata                                                    │
│  ├── Experiment name & ID                                   │
│  ├── Author & timestamp                                     │
│  ├── Git commit SHA                                         │
│  └── Hypothesis / goal                                      │
├─────────────────────────────────────────────────────────────┤
│  Inputs                                                      │
│  ├── Data version / path                                    │
│  ├── Data split (train/val/test)                           │
│  ├── Feature set version                                    │
│  └── Environment (dependencies)                             │
├─────────────────────────────────────────────────────────────┤
│  Configuration                                               │
│  ├── Model type & architecture                              │
│  ├── Hyperparameters                                        │
│  ├── Training config (epochs, batch size)                   │
│  └── Random seeds                                           │
├─────────────────────────────────────────────────────────────┤
│  Outputs                                                     │
│  ├── Metrics (accuracy, loss, etc.)                        │
│  ├── Model artifacts                                        │
│  ├── Visualizations (learning curves, confusion matrix)    │
│  └── Predictions on test set                                │
└─────────────────────────────────────────────────────────────┘
```

---

## MLflow Implementation

### Basic Experiment Tracking

```python
import mlflow
from mlflow.tracking import MlflowClient

class ExperimentTracker:
    """Track ML experiments with MLflow."""

    def __init__(self, experiment_name: str, tracking_uri: str = None):
        if tracking_uri:
            mlflow.set_tracking_uri(tracking_uri)

        self.experiment = mlflow.set_experiment(experiment_name)
        self.client = MlflowClient()

    def start_run(
        self,
        run_name: str,
        tags: dict = None,
        description: str = None
    ):
        """Start a new experiment run."""
        return mlflow.start_run(
            run_name=run_name,
            tags=tags,
            description=description
        )

    def log_params(self, params: dict):
        """Log hyperparameters."""
        mlflow.log_params(params)

    def log_metrics(self, metrics: dict, step: int = None):
        """Log metrics."""
        for key, value in metrics.items():
            mlflow.log_metric(key, value, step=step)

    def log_model(
        self,
        model,
        artifact_path: str,
        registered_name: str = None
    ):
        """Log model artifact."""
        mlflow.sklearn.log_model(
            model,
            artifact_path,
            registered_model_name=registered_name
        )

    def log_artifact(self, local_path: str, artifact_path: str = None):
        """Log arbitrary artifact."""
        mlflow.log_artifact(local_path, artifact_path)

    def log_figure(self, figure, artifact_file: str):
        """Log matplotlib figure."""
        mlflow.log_figure(figure, artifact_file)
```

### Complete Training Example

```python
import mlflow
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt

def train_with_tracking(
    model_class,
    params: dict,
    X_train, y_train,
    X_test, y_test,
    experiment_name: str,
    run_name: str,
    data_version: str,
    git_commit: str
):
    """Train model with comprehensive tracking."""

    mlflow.set_experiment(experiment_name)

    with mlflow.start_run(run_name=run_name) as run:
        # 1. Log metadata
        mlflow.set_tags({
            "data_version": data_version,
            "git_commit": git_commit,
            "model_type": model_class.__name__,
            "author": "ml-team",
        })

        # 2. Log parameters
        mlflow.log_params(params)
        mlflow.log_param("n_features", X_train.shape[1])
        mlflow.log_param("n_train_samples", X_train.shape[0])
        mlflow.log_param("n_test_samples", X_test.shape[0])

        # 3. Train model
        model = model_class(**params)
        model.fit(X_train, y_train)

        # 4. Evaluate and log metrics
        # Training metrics
        train_score = model.score(X_train, y_train)
        mlflow.log_metric("train_accuracy", train_score)

        # Test metrics
        test_score = model.score(X_test, y_test)
        mlflow.log_metric("test_accuracy", test_score)

        # Cross-validation
        cv_scores = cross_val_score(model, X_train, y_train, cv=5)
        mlflow.log_metric("cv_mean", cv_scores.mean())
        mlflow.log_metric("cv_std", cv_scores.std())

        # Detailed classification metrics
        y_pred = model.predict(X_test)
        report = classification_report(y_test, y_pred, output_dict=True)
        mlflow.log_metric("precision_macro", report["macro avg"]["precision"])
        mlflow.log_metric("recall_macro", report["macro avg"]["recall"])
        mlflow.log_metric("f1_macro", report["macro avg"]["f1-score"])

        # 5. Log artifacts
        # Classification report
        report_text = classification_report(y_test, y_pred)
        with open("classification_report.txt", "w") as f:
            f.write(report_text)
        mlflow.log_artifact("classification_report.txt")

        # Confusion matrix plot
        fig = plot_confusion_matrix(y_test, y_pred)
        mlflow.log_figure(fig, "confusion_matrix.png")
        plt.close(fig)

        # Feature importance (if available)
        if hasattr(model, "feature_importances_"):
            fig = plot_feature_importance(model, X_train.columns)
            mlflow.log_figure(fig, "feature_importance.png")
            plt.close(fig)

        # 6. Log model
        mlflow.sklearn.log_model(
            model,
            "model",
            registered_model_name=f"{experiment_name}_{model_class.__name__}"
        )

        return run.info.run_id, model
```

---

## Experiment Organization

### Naming Conventions

```python
# Experiment naming
EXPERIMENT_NAME_PATTERN = "{project}/{task}/{approach}"

# Examples:
# - "churn-prediction/classification/xgboost"
# - "fraud-detection/anomaly/isolation-forest"
# - "recommendations/collaborative-filtering/als"

# Run naming
RUN_NAME_PATTERN = "{model}_{date}_{description}"

# Examples:
# - "xgb_20240115_baseline"
# - "xgb_20240116_tuned_depth"
# - "xgb_20240117_feature_selection"
```

### Tagging Strategy

```python
STANDARD_TAGS = {
    # Data lineage
    "data_version": "v2.1.0",
    "data_split_seed": "42",
    "feature_set": "v3",

    # Code lineage
    "git_commit": "abc123",
    "git_branch": "feature/new-model",
    "code_version": "1.2.0",

    # Context
    "author": "alice@company.com",
    "team": "ml-platform",
    "environment": "development",

    # Experiment metadata
    "hypothesis": "deeper trees improve recall",
    "experiment_type": "hyperparameter_tuning",
    "baseline_run_id": "xyz789",
}
```

---

## Hyperparameter Optimization

### Grid Search with Tracking

```python
from sklearn.model_selection import GridSearchCV
import mlflow

def hyperparameter_search(
    model_class,
    param_grid: dict,
    X_train, y_train,
    experiment_name: str,
    cv: int = 5
):
    """Hyperparameter search with individual run tracking."""

    mlflow.set_experiment(experiment_name)

    # Parent run for the search
    with mlflow.start_run(run_name="hyperparam_search") as parent_run:
        mlflow.log_params({"search_type": "grid", "cv_folds": cv})
        mlflow.log_param("param_grid", str(param_grid))

        best_score = -float("inf")
        best_params = None
        best_run_id = None

        # Iterate through parameter combinations
        from itertools import product
        param_names = list(param_grid.keys())
        param_values = list(param_grid.values())

        for values in product(*param_values):
            params = dict(zip(param_names, values))

            # Child run for each combination
            with mlflow.start_run(
                run_name=f"params_{hash(str(params)) % 10000}",
                nested=True
            ) as child_run:
                mlflow.log_params(params)

                # Train and evaluate
                model = model_class(**params)
                scores = cross_val_score(model, X_train, y_train, cv=cv)

                mlflow.log_metric("cv_mean", scores.mean())
                mlflow.log_metric("cv_std", scores.std())

                if scores.mean() > best_score:
                    best_score = scores.mean()
                    best_params = params
                    best_run_id = child_run.info.run_id

        # Log best results to parent
        mlflow.log_params({f"best_{k}": v for k, v in best_params.items()})
        mlflow.log_metric("best_cv_score", best_score)
        mlflow.set_tag("best_child_run", best_run_id)

        return best_params, best_score
```

### Optuna Integration

```python
import optuna
from optuna.integration.mlflow import MLflowCallback

def optuna_search(
    objective_fn,
    n_trials: int,
    experiment_name: str
):
    """Bayesian optimization with Optuna and MLflow tracking."""

    mlflow.set_experiment(experiment_name)

    # Create Optuna study
    study = optuna.create_study(
        direction="maximize",
        study_name=experiment_name
    )

    # MLflow callback for automatic tracking
    mlflow_callback = MLflowCallback(
        tracking_uri=mlflow.get_tracking_uri(),
        metric_name="objective_value"
    )

    # Run optimization
    study.optimize(
        objective_fn,
        n_trials=n_trials,
        callbacks=[mlflow_callback]
    )

    return study.best_params, study.best_value


# Example objective function
def objective(trial):
    params = {
        "max_depth": trial.suggest_int("max_depth", 2, 10),
        "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3),
        "n_estimators": trial.suggest_int("n_estimators", 50, 300),
        "min_child_weight": trial.suggest_int("min_child_weight", 1, 10),
    }

    model = XGBClassifier(**params)
    scores = cross_val_score(model, X_train, y_train, cv=5)

    return scores.mean()
```

---

## Model Registry

### Registering Models

```python
from mlflow.tracking import MlflowClient

class ModelRegistry:
    """Manage model lifecycle in registry."""

    def __init__(self):
        self.client = MlflowClient()

    def register_model(
        self,
        run_id: str,
        model_name: str,
        description: str = None
    ) -> str:
        """Register a model from a run."""
        model_uri = f"runs:/{run_id}/model"

        result = mlflow.register_model(model_uri, model_name)

        if description:
            self.client.update_model_version(
                name=model_name,
                version=result.version,
                description=description
            )

        return result.version

    def transition_stage(
        self,
        model_name: str,
        version: str,
        stage: str,  # "Staging", "Production", "Archived"
        archive_existing: bool = True
    ):
        """Transition model to new stage."""
        self.client.transition_model_version_stage(
            name=model_name,
            version=version,
            stage=stage,
            archive_existing_versions=archive_existing
        )

    def get_production_model(self, model_name: str):
        """Load the production model."""
        return mlflow.pyfunc.load_model(
            model_uri=f"models:/{model_name}/Production"
        )

    def compare_versions(
        self,
        model_name: str,
        version_a: str,
        version_b: str
    ) -> dict:
        """Compare two model versions."""
        run_a = self.client.get_model_version(model_name, version_a)
        run_b = self.client.get_model_version(model_name, version_b)

        metrics_a = self.client.get_run(run_a.run_id).data.metrics
        metrics_b = self.client.get_run(run_b.run_id).data.metrics

        comparison = {}
        all_metrics = set(metrics_a.keys()) | set(metrics_b.keys())

        for metric in all_metrics:
            comparison[metric] = {
                "version_a": metrics_a.get(metric),
                "version_b": metrics_b.get(metric),
                "diff": (metrics_b.get(metric, 0) - metrics_a.get(metric, 0))
            }

        return comparison
```

---

## Experiment Comparison

### Comparing Runs

```python
def compare_experiments(experiment_name: str, metric: str = "test_accuracy"):
    """Compare all runs in an experiment."""

    client = MlflowClient()
    experiment = client.get_experiment_by_name(experiment_name)

    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=[f"metrics.{metric} DESC"]
    )

    comparison = []
    for run in runs:
        comparison.append({
            "run_id": run.info.run_id,
            "run_name": run.info.run_name,
            "status": run.info.status,
            metric: run.data.metrics.get(metric),
            "params": run.data.params,
            "tags": run.data.tags,
        })

    return pd.DataFrame(comparison)
```

### Visualization

```python
def plot_experiment_history(experiment_name: str, metrics: list[str]):
    """Plot metric progression over experiment runs."""

    df = compare_experiments(experiment_name)
    df = df.sort_values("start_time")

    fig, axes = plt.subplots(len(metrics), 1, figsize=(12, 4*len(metrics)))

    for i, metric in enumerate(metrics):
        ax = axes[i] if len(metrics) > 1 else axes
        ax.plot(df.index, df[metric], marker='o')
        ax.set_xlabel("Run Number")
        ax.set_ylabel(metric)
        ax.set_title(f"{metric} Over Time")
        ax.grid(True)

    plt.tight_layout()
    return fig
```

---

## Good Examples

### Example 1: Well-Structured Experiment

```python
# Comprehensive experiment with full tracking
def run_experiment():
    with mlflow.start_run(run_name="xgb_v2_tuned"):
        # Clear hypothesis documented
        mlflow.set_tag("hypothesis", "Reducing max_depth will improve generalization")
        mlflow.set_tag("baseline_comparison", "run_abc123")

        # Full lineage
        mlflow.set_tag("data_version", "customers_v2.1")
        mlflow.set_tag("git_commit", get_git_commit())
        mlflow.set_tag("feature_set", "standard_v3")

        # Parameters
        params = {
            "max_depth": 4,  # Reduced from 6
            "learning_rate": 0.1,
            "n_estimators": 100
        }
        mlflow.log_params(params)

        # Train
        model = XGBClassifier(**params)
        model.fit(X_train, y_train)

        # Comprehensive metrics
        mlflow.log_metric("train_accuracy", model.score(X_train, y_train))
        mlflow.log_metric("test_accuracy", model.score(X_test, y_test))
        mlflow.log_metric("cv_mean", cross_val_score(model, X_train, y_train).mean())

        # Conclusion documented
        mlflow.set_tag("conclusion", "Hypothesis confirmed: test acc improved 2%")
        mlflow.set_tag("next_steps", "Try further reduction to max_depth=3")
```

---

## Bad Examples (Anti-Patterns)

### Anti-Pattern 1: No Tracking

```python
# BAD - No experiment tracking
model = XGBClassifier(max_depth=6)
model.fit(X_train, y_train)
print(f"Score: {model.score(X_test, y_test)}")
# What were the parameters? Which data version? Can't reproduce.
```

**Correct approach:** Track all experiments, even quick tests.

---

### Anti-Pattern 2: Overwriting Experiments

```python
# BAD - Reusing same run name, losing history
for params in param_grid:
    with mlflow.start_run(run_name="experiment"):  # Same name every time!
        mlflow.log_params(params)
        # Previous runs are hidden, can't compare
```

**Correct approach:** Unique run names or let MLflow auto-generate.

---

### Anti-Pattern 3: Missing Lineage

```python
# BAD - No connection to data or code
with mlflow.start_run():
    mlflow.log_params({"depth": 6})
    mlflow.log_metric("accuracy", 0.95)
    # Which data? Which code version? Which features?
```

**Correct approach:** Always log data version, git commit, and feature set.

---

## Quality Checklist

Before considering experiment tracking complete:

### Tracking Coverage
- [ ] All experiments tracked (no notebooks without logging)
- [ ] Parameters fully logged
- [ ] Metrics comprehensively captured
- [ ] Artifacts stored (plots, reports, models)

### Lineage
- [ ] Data version linked
- [ ] Code version (git commit) logged
- [ ] Environment captured
- [ ] Random seeds recorded

### Organization
- [ ] Consistent naming conventions
- [ ] Meaningful tags applied
- [ ] Experiments logically grouped
- [ ] Clear documentation/hypotheses

### Collaboration
- [ ] Team can access experiments
- [ ] Comparison dashboards available
- [ ] Best practices documented

---

## Skill Interactions

### Preceded By
- **17-ML Pipeline** - Pipeline generates experiments to track

### Followed By
- **19-Model Serving** - Best experiments become production models
- **20-ML Monitoring** - Production metrics continue tracking

### Related Skills
- **13-Observability** - Experiment visibility
- **16-Documentation** - Experiment documentation practices

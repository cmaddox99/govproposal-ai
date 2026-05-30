---
law_id: BUS-3.1
avatar: mlflow-kubeflow
---

# BUS-3.1: Data Governance Examples for MLflow/Kubeflow

## COMPLIANT: Comprehensive Experiment Tracking with MLflow

```python
import mlflow
from mlflow.tracking import MlflowClient
from datetime import datetime
import hashlib
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class ExperimentMetadata:
    """Comprehensive experiment metadata for governance."""
    experiment_name: str
    run_name: str
    data_source: str
    data_version: str
    data_hash: str
    model_type: str
    owner: str
    purpose: str
    compliance_tags: list[str]


class GovernedExperimentTracker:
    """MLflow experiment tracking with full governance compliance."""

    def __init__(self, tracking_uri: str, experiment_name: str):
        mlflow.set_tracking_uri(tracking_uri)
        self.client = MlflowClient()
        self.experiment_name = experiment_name

        # Create or get experiment with governance tags
        experiment = mlflow.get_experiment_by_name(experiment_name)
        if experiment is None:
            self.experiment_id = mlflow.create_experiment(
                experiment_name,
                tags={
                    "governance.created_at": datetime.utcnow().isoformat(),
                    "governance.compliance_level": "standard"
                }
            )
        else:
            self.experiment_id = experiment.experiment_id

    def start_governed_run(
        self,
        metadata: ExperimentMetadata,
        hyperparameters: Dict[str, Any]
    ) -> str:
        """Start a run with full governance tracking."""

        with mlflow.start_run(
            experiment_id=self.experiment_id,
            run_name=metadata.run_name
        ) as run:
            # Log governance metadata as tags
            mlflow.set_tags({
                "governance.data_source": metadata.data_source,
                "governance.data_version": metadata.data_version,
                "governance.data_hash": metadata.data_hash,
                "governance.owner": metadata.owner,
                "governance.purpose": metadata.purpose,
                "governance.timestamp": datetime.utcnow().isoformat(),
                "governance.model_type": metadata.model_type,
            })

            # Log compliance tags
            for i, tag in enumerate(metadata.compliance_tags):
                mlflow.set_tag(f"compliance.tag_{i}", tag)

            # Log all hyperparameters
            mlflow.log_params(hyperparameters)

            # Log metadata as artifact for complete audit trail
            metadata_path = "/tmp/experiment_metadata.json"
            with open(metadata_path, "w") as f:
                json.dump(asdict(metadata), f, indent=2)
            mlflow.log_artifact(metadata_path, "governance")

            return run.info.run_id

    def log_data_lineage(
        self,
        run_id: str,
        input_datasets: list[Dict[str, str]],
        output_datasets: list[Dict[str, str]],
        transformations: list[str]
    ):
        """Log data lineage information for a run."""

        lineage = {
            "inputs": input_datasets,
            "outputs": output_datasets,
            "transformations": transformations,
            "logged_at": datetime.utcnow().isoformat()
        }

        with mlflow.start_run(run_id=run_id):
            lineage_path = "/tmp/data_lineage.json"
            with open(lineage_path, "w") as f:
                json.dump(lineage, f, indent=2)
            mlflow.log_artifact(lineage_path, "governance")

    def log_model_with_governance(
        self,
        run_id: str,
        model: Any,
        model_name: str,
        signature: Any,
        input_example: Any
    ):
        """Log model with complete governance metadata."""

        with mlflow.start_run(run_id=run_id):
            # Log model with signature for schema validation
            mlflow.sklearn.log_model(
                model,
                artifact_path="model",
                signature=signature,
                input_example=input_example,
                registered_model_name=model_name
            )

            # Add governance tags to registered model
            self.client.set_registered_model_tag(
                model_name,
                "governance.registered_at",
                datetime.utcnow().isoformat()
            )


# Usage Example
tracker = GovernedExperimentTracker(
    tracking_uri="http://mlflow:5000",
    experiment_name="customer-churn-prediction"
)

metadata = ExperimentMetadata(
    experiment_name="customer-churn-prediction",
    run_name="rf-baseline-v1",
    data_source="s3://data-lake/curated/customers/",
    data_version="2024-01-15",
    data_hash="sha256:abc123...",
    model_type="RandomForestClassifier",
    owner="ml-team@company.com",
    purpose="Predict customer churn for retention campaigns",
    compliance_tags=["GDPR-compliant", "no-PII-in-features"]
)

run_id = tracker.start_governed_run(
    metadata=metadata,
    hyperparameters={
        "n_estimators": 100,
        "max_depth": 10,
        "min_samples_split": 5
    }
)
```

**Why compliant:** Tracks comprehensive experiment metadata including data lineage, captures data versions and hashes for reproducibility, logs owner and purpose for accountability, includes compliance tags, and creates a complete audit trail as artifacts.

---

## COMPLIANT: Model Registry Governance with MLflow

```python
from mlflow.tracking import MlflowClient
from datetime import datetime
from typing import Optional, List
from dataclasses import dataclass
import json


@dataclass
class ModelApproval:
    """Model approval record for governance."""
    model_name: str
    version: str
    approver: str
    approval_type: str  # "data_quality", "model_performance", "security", "final"
    approved: bool
    comments: str
    timestamp: str


class ModelRegistryGovernance:
    """Enforces governance policies on MLflow Model Registry."""

    def __init__(self, client: MlflowClient):
        self.client = client
        self.required_approvals = ["data_quality", "model_performance", "security"]

    def request_approval(
        self,
        model_name: str,
        version: str,
        requester: str,
        target_stage: str
    ):
        """Request approval for model stage transition."""

        # Set request metadata
        self.client.set_model_version_tag(
            model_name, version,
            "approval.requested_by", requester
        )
        self.client.set_model_version_tag(
            model_name, version,
            "approval.requested_at", datetime.utcnow().isoformat()
        )
        self.client.set_model_version_tag(
            model_name, version,
            "approval.target_stage", target_stage
        )
        self.client.set_model_version_tag(
            model_name, version,
            "approval.status", "pending"
        )

    def record_approval(self, approval: ModelApproval):
        """Record an approval decision."""

        prefix = f"approval.{approval.approval_type}"

        self.client.set_model_version_tag(
            approval.model_name, approval.version,
            f"{prefix}.approver", approval.approver
        )
        self.client.set_model_version_tag(
            approval.model_name, approval.version,
            f"{prefix}.approved", str(approval.approved).lower()
        )
        self.client.set_model_version_tag(
            approval.model_name, approval.version,
            f"{prefix}.comments", approval.comments
        )
        self.client.set_model_version_tag(
            approval.model_name, approval.version,
            f"{prefix}.timestamp", approval.timestamp
        )

    def check_all_approvals(
        self,
        model_name: str,
        version: str
    ) -> tuple[bool, List[str]]:
        """Check if all required approvals are granted."""

        model_version = self.client.get_model_version(model_name, version)
        tags = model_version.tags

        missing = []
        for approval_type in self.required_approvals:
            prefix = f"approval.{approval_type}"
            if tags.get(f"{prefix}.approved") != "true":
                missing.append(approval_type)

        return len(missing) == 0, missing

    def promote_with_governance(
        self,
        model_name: str,
        version: str,
        target_stage: str
    ) -> bool:
        """Promote model only if all governance requirements are met."""

        all_approved, missing = self.check_all_approvals(model_name, version)

        if not all_approved:
            raise ValueError(
                f"Cannot promote model. Missing approvals: {missing}"
            )

        # Record promotion
        self.client.set_model_version_tag(
            model_name, version,
            "governance.promoted_to", target_stage
        )
        self.client.set_model_version_tag(
            model_name, version,
            "governance.promoted_at", datetime.utcnow().isoformat()
        )

        # Perform transition
        self.client.transition_model_version_stage(
            name=model_name,
            version=version,
            stage=target_stage,
            archive_existing_versions=True
        )

        self.client.set_model_version_tag(
            model_name, version,
            "approval.status", "completed"
        )

        return True

    def get_audit_trail(
        self,
        model_name: str,
        version: str
    ) -> dict:
        """Get complete audit trail for a model version."""

        model_version = self.client.get_model_version(model_name, version)
        run = self.client.get_run(model_version.run_id)

        return {
            "model_name": model_name,
            "version": version,
            "run_id": model_version.run_id,
            "created_at": model_version.creation_timestamp,
            "current_stage": model_version.current_stage,
            "tags": model_version.tags,
            "run_tags": run.data.tags,
            "metrics": run.data.metrics,
            "params": run.data.params
        }
```

**Why compliant:** Implements multi-stage approval workflow, tracks all approval decisions with approvers and timestamps, enforces required approvals before promotion, maintains complete audit trail, and enables governance queries on model history.

---

## VIOLATION: No Experiment Tracking

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import pickle


def train_model(data_path, output_path):
    """Train model with no experiment tracking."""
    # Load data - no tracking of source or version
    df = pd.read_csv(data_path)
    X = df.drop("target", axis=1)
    y = df["target"]

    # Split data - no tracking of split parameters
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Train model - no logging of hyperparameters
    model = RandomForestClassifier(n_estimators=100, max_depth=10)
    model.fit(X_train, y_train)

    # Evaluate - no logging of metrics
    accuracy = model.score(X_test, y_test)
    print(f"Accuracy: {accuracy}")

    # Save model - no versioning or registry
    with open(output_path, "wb") as f:
        pickle.dump(model, f)

    print("Model saved!")


if __name__ == "__main__":
    train_model("data.csv", "model.pkl")
```

**Why violates BUS-3.1:** This code violates data governance by: (1) no tracking of data source or version, (2) no logging of hyperparameters for reproducibility, (3) no metrics tracking for comparison, (4) no model versioning or registry, (5) using pickle with no schema validation, and (6) no audit trail of training runs.

---

## VIOLATION: Ungoverned Model Promotion

```python
from mlflow.tracking import MlflowClient


def promote_model_fast(model_name):
    """Promote model to production without governance."""
    client = MlflowClient()

    # Get latest version
    versions = client.search_model_versions(f"name='{model_name}'")
    latest = max(versions, key=lambda v: int(v.version))

    # Skip all validation and approval
    # Just push to production
    client.transition_model_version_stage(
        name=model_name,
        version=latest.version,
        stage="Production",
        archive_existing_versions=True
    )

    print(f"Model {model_name} v{latest.version} is now in Production!")


def cleanup_old_models(model_name):
    """Delete old model versions without audit."""
    client = MlflowClient()

    versions = client.search_model_versions(f"name='{model_name}'")

    for version in versions:
        if version.current_stage == "Archived":
            # Delete without any record
            client.delete_model_version(model_name, version.version)

    print("Cleanup complete - old versions deleted")
```

**Why violates BUS-3.1:** This violates data governance by: (1) promoting models without any approval process, (2) no validation of model quality before production, (3) no record of who promoted the model or why, (4) deleting model versions without audit trail, and (5) losing historical data needed for compliance.

---

## COMPLIANT: Kubeflow Pipeline Governance

```python
from kfp import dsl
from kfp.dsl import Dataset, Model, Metrics, Output, Input
from datetime import datetime
import json


@dsl.component(
    base_image="python:3.10",
    packages_to_install=["pandas", "great-expectations"]
)
def data_quality_gate(
    input_data: Input[Dataset],
    quality_report: Output[Metrics],
    approved: Output[str]
) -> str:
    """Data quality gate component with governance tracking."""
    import pandas as pd
    import great_expectations as gx
    from datetime import datetime

    # Load data
    df = pd.read_parquet(input_data.path)

    # Run quality checks
    context = gx.get_context()
    results = context.run_checkpoint(
        checkpoint_name="data_quality_checkpoint",
        batch_request={
            "runtime_parameters": {"batch_data": df},
            "batch_identifiers": {"run_id": datetime.utcnow().isoformat()}
        }
    )

    # Log quality metrics
    quality_report.log_metric("rows_validated", len(df))
    quality_report.log_metric("expectations_passed", results.statistics["successful_expectations"])
    quality_report.log_metric("expectations_failed", results.statistics["unsuccessful_expectations"])
    quality_report.log_metric("success_rate", results.statistics["success_percent"])

    # Record governance decision
    if results.success:
        approved.set("approved")
        return "approved"
    else:
        approved.set("rejected")
        return "rejected"


@dsl.component(
    base_image="python:3.10",
    packages_to_install=["mlflow", "scikit-learn"]
)
def train_with_lineage(
    training_data: Input[Dataset],
    model_output: Output[Model],
    lineage_record: Output[Metrics],
    experiment_name: str,
    hyperparameters: dict
):
    """Training component with full lineage tracking."""
    import mlflow
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier
    import hashlib
    from datetime import datetime

    # Calculate data hash for lineage
    df = pd.read_parquet(training_data.path)
    data_hash = hashlib.sha256(
        pd.util.hash_pandas_object(df).values.tobytes()
    ).hexdigest()

    # Log lineage metadata
    lineage_record.log_metric("input_rows", len(df))
    lineage_record.log_metric("input_columns", len(df.columns))

    with mlflow.start_run(experiment_id=experiment_name):
        # Log data lineage
        mlflow.set_tags({
            "lineage.input_path": training_data.path,
            "lineage.input_hash": data_hash,
            "lineage.training_timestamp": datetime.utcnow().isoformat(),
            "lineage.pipeline_run_id": "{{workflow.uid}}"
        })

        # Log hyperparameters
        mlflow.log_params(hyperparameters)

        # Train model
        X = df.drop("target", axis=1)
        y = df["target"]
        model = RandomForestClassifier(**hyperparameters)
        model.fit(X, y)

        # Log model with signature
        from mlflow.models import infer_signature
        signature = infer_signature(X, model.predict(X))
        mlflow.sklearn.log_model(model, "model", signature=signature)

        # Save model output
        import joblib
        joblib.dump(model, model_output.path)


@dsl.pipeline(name="governed-ml-pipeline")
def governed_training_pipeline(
    data_source: str,
    experiment_name: str,
    hyperparameters: dict
):
    """ML pipeline with built-in governance controls."""

    # Data loading with versioning
    load_data_task = load_versioned_data(data_source=data_source)

    # Mandatory data quality gate
    quality_gate_task = data_quality_gate(
        input_data=load_data_task.outputs["output_data"]
    )

    # Training only proceeds if data quality passes
    with dsl.Condition(
        quality_gate_task.outputs["approved"] == "approved",
        name="data-quality-passed"
    ):
        train_task = train_with_lineage(
            training_data=load_data_task.outputs["output_data"],
            experiment_name=experiment_name,
            hyperparameters=hyperparameters
        )

        # Model validation gate
        validation_task = validate_model(
            model=train_task.outputs["model_output"]
        )

        # Register only if validation passes
        with dsl.Condition(
            validation_task.outputs["passed"] == "true",
            name="model-validation-passed"
        ):
            register_task = register_governed_model(
                model=train_task.outputs["model_output"],
                validation_report=validation_task.outputs["report"]
            )
```

**Why compliant:** Implements mandatory quality gates in the pipeline, tracks data lineage at each step, logs governance metadata to MLflow, uses conditional execution based on quality checks, and creates audit trail through metrics outputs.

---

## COMPLIANT: ML Metadata Tracking for Reproducibility

```python
import mlflow
from mlflow.tracking import MlflowClient
from datetime import datetime
import subprocess
import platform
import pkg_resources
from typing import Dict, Any


class ReproducibilityTracker:
    """Tracks all information needed to reproduce an ML experiment."""

    def __init__(self):
        self.client = MlflowClient()

    def capture_environment(self) -> Dict[str, Any]:
        """Capture complete environment information."""

        # Get git info
        try:
            git_commit = subprocess.check_output(
                ["git", "rev-parse", "HEAD"]
            ).decode().strip()
            git_branch = subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"]
            ).decode().strip()
            git_dirty = bool(subprocess.check_output(
                ["git", "status", "--porcelain"]
            ).decode().strip())
        except subprocess.CalledProcessError:
            git_commit = "unknown"
            git_branch = "unknown"
            git_dirty = False

        # Get Python packages
        packages = {
            pkg.key: pkg.version
            for pkg in pkg_resources.working_set
        }

        return {
            "git": {
                "commit": git_commit,
                "branch": git_branch,
                "dirty": git_dirty
            },
            "python_version": platform.python_version(),
            "platform": platform.platform(),
            "packages": packages,
            "captured_at": datetime.utcnow().isoformat()
        }

    def log_reproducibility_info(self, run_id: str):
        """Log all reproducibility information to MLflow run."""

        env_info = self.capture_environment()

        with mlflow.start_run(run_id=run_id):
            # Log git info as tags
            mlflow.set_tags({
                "reproducibility.git_commit": env_info["git"]["commit"],
                "reproducibility.git_branch": env_info["git"]["branch"],
                "reproducibility.git_dirty": str(env_info["git"]["dirty"]),
                "reproducibility.python_version": env_info["python_version"],
                "reproducibility.platform": env_info["platform"],
                "reproducibility.captured_at": env_info["captured_at"]
            })

            # Log full environment as artifact
            import json
            env_path = "/tmp/environment.json"
            with open(env_path, "w") as f:
                json.dump(env_info, f, indent=2)
            mlflow.log_artifact(env_path, "reproducibility")

            # Log requirements.txt style package list
            req_path = "/tmp/requirements.txt"
            with open(req_path, "w") as f:
                for pkg, version in env_info["packages"].items():
                    f.write(f"{pkg}=={version}\n")
            mlflow.log_artifact(req_path, "reproducibility")

    def verify_reproducibility(
        self,
        run_id: str
    ) -> tuple[bool, list[str]]:
        """Verify current environment matches logged run."""

        current_env = self.capture_environment()

        run = self.client.get_run(run_id)
        tags = run.data.tags

        issues = []

        # Check git commit
        if tags.get("reproducibility.git_commit") != current_env["git"]["commit"]:
            issues.append(
                f"Git commit mismatch: logged={tags.get('reproducibility.git_commit')}, "
                f"current={current_env['git']['commit']}"
            )

        # Check Python version
        if tags.get("reproducibility.python_version") != current_env["python_version"]:
            issues.append(
                f"Python version mismatch: logged={tags.get('reproducibility.python_version')}, "
                f"current={current_env['python_version']}"
            )

        return len(issues) == 0, issues
```

**Why compliant:** Captures complete environment state including git commit, Python version, and package versions; logs all information to MLflow for audit trail; provides verification capability to ensure reproducibility; and stores detailed artifacts for complete recreation of training environment.

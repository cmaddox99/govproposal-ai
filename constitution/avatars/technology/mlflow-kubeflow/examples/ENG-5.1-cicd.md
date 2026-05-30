---
law_id: ENG-5.1
avatar: mlflow-kubeflow
---

# ENG-5.1: CI/CD Examples for MLflow/Kubeflow

## COMPLIANT: ML Pipeline CI/CD with GitHub Actions

```yaml
# .github/workflows/ml-pipeline-ci.yml
name: ML Pipeline CI/CD

on:
  push:
    branches: [main, develop]
    paths:
      - 'pipelines/**'
      - 'components/**'
      - 'models/**'
  pull_request:
    branches: [main]

env:
  MLFLOW_TRACKING_URI: ${{ secrets.MLFLOW_TRACKING_URI }}
  KUBEFLOW_HOST: ${{ secrets.KUBEFLOW_HOST }}
  PYTHON_VERSION: '3.10'

jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: 'pip'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Lint code
        run: |
          ruff check pipelines/ components/ models/
          mypy pipelines/ components/ --ignore-missing-imports

      - name: Run unit tests
        run: |
          pytest tests/unit/ -v --cov=components --cov=pipelines \
            --cov-report=xml --cov-fail-under=80

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage.xml

  integration-tests:
    needs: lint-and-test
    runs-on: ubuntu-latest
    services:
      mlflow:
        image: ghcr.io/mlflow/mlflow:v2.10.0
        ports:
          - 5000:5000
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install dependencies
        run: pip install -r requirements.txt -r requirements-dev.txt

      - name: Run integration tests
        env:
          MLFLOW_TRACKING_URI: http://localhost:5000
        run: |
          pytest tests/integration/ -v --timeout=300

  compile-pipeline:
    needs: integration-tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install KFP SDK
        run: pip install kfp==2.5.0

      - name: Compile pipeline
        run: |
          python -c "from pipelines.training_pipeline import pipeline; \
            from kfp import compiler; \
            compiler.Compiler().compile(pipeline, 'pipeline.yaml')"

      - name: Validate pipeline YAML
        run: |
          python scripts/validate_pipeline.py pipeline.yaml

      - name: Upload pipeline artifact
        uses: actions/upload-artifact@v4
        with:
          name: compiled-pipeline
          path: pipeline.yaml

  deploy-staging:
    needs: compile-pipeline
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v4

      - name: Download pipeline artifact
        uses: actions/download-artifact@v4
        with:
          name: compiled-pipeline

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install KFP SDK
        run: pip install kfp==2.5.0

      - name: Deploy to staging Kubeflow
        env:
          KUBEFLOW_HOST: ${{ secrets.STAGING_KUBEFLOW_HOST }}
          KUBEFLOW_TOKEN: ${{ secrets.STAGING_KUBEFLOW_TOKEN }}
        run: |
          python scripts/deploy_pipeline.py \
            --pipeline-file pipeline.yaml \
            --environment staging \
            --version ${{ github.sha }}

  deploy-production:
    needs: compile-pipeline
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4

      - name: Download pipeline artifact
        uses: actions/download-artifact@v4
        with:
          name: compiled-pipeline

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Deploy to production Kubeflow
        env:
          KUBEFLOW_HOST: ${{ secrets.PROD_KUBEFLOW_HOST }}
          KUBEFLOW_TOKEN: ${{ secrets.PROD_KUBEFLOW_TOKEN }}
        run: |
          python scripts/deploy_pipeline.py \
            --pipeline-file pipeline.yaml \
            --environment production \
            --version ${{ github.sha }} \
            --require-approval
```

**Why compliant:** Implements a complete CI/CD pipeline with stages (lint, test, compile, deploy), uses GitHub environments for deployment approvals, runs integration tests with containerized MLflow, separates staging and production deployments, and requires approval for production.

---

## COMPLIANT: Automated Model Validation Gate

```python
# scripts/model_validation_gate.py
"""
Model validation gate for CI/CD pipeline.
Ensures models meet quality thresholds before deployment.
"""

import mlflow
from mlflow.tracking import MlflowClient
import json
import sys
from dataclasses import dataclass
from typing import Optional


@dataclass
class ValidationThresholds:
    """Minimum thresholds for model promotion."""
    min_accuracy: float = 0.85
    min_f1_score: float = 0.80
    max_inference_time_ms: float = 100.0
    min_test_coverage: float = 0.80
    required_tests_passed: bool = True


@dataclass
class ValidationResult:
    """Result of model validation."""
    passed: bool
    model_name: str
    model_version: str
    metrics: dict
    failures: list[str]


class ModelValidationGate:
    """Validates models before promotion to production."""

    def __init__(self, client: MlflowClient, thresholds: ValidationThresholds):
        self.client = client
        self.thresholds = thresholds

    def validate_model(
        self,
        model_name: str,
        model_version: str
    ) -> ValidationResult:
        """Validate model against all thresholds."""
        failures = []

        # Get model version details
        model_version_info = self.client.get_model_version(
            name=model_name,
            version=model_version
        )

        # Get run metrics
        run = self.client.get_run(model_version_info.run_id)
        metrics = run.data.metrics

        # Validate accuracy
        if metrics.get("accuracy", 0) < self.thresholds.min_accuracy:
            failures.append(
                f"Accuracy {metrics.get('accuracy', 0):.3f} < "
                f"threshold {self.thresholds.min_accuracy}"
            )

        # Validate F1 score
        if metrics.get("f1_score", 0) < self.thresholds.min_f1_score:
            failures.append(
                f"F1 score {metrics.get('f1_score', 0):.3f} < "
                f"threshold {self.thresholds.min_f1_score}"
            )

        # Validate inference time
        if metrics.get("inference_time_ms", float("inf")) > self.thresholds.max_inference_time_ms:
            failures.append(
                f"Inference time {metrics.get('inference_time_ms'):.1f}ms > "
                f"threshold {self.thresholds.max_inference_time_ms}ms"
            )

        # Validate test coverage from tags
        tags = run.data.tags
        if float(tags.get("test_coverage", 0)) < self.thresholds.min_test_coverage:
            failures.append(
                f"Test coverage {tags.get('test_coverage', 0)} < "
                f"threshold {self.thresholds.min_test_coverage}"
            )

        # Validate tests passed
        if tags.get("tests_passed") != "true":
            failures.append("Model tests did not pass")

        return ValidationResult(
            passed=len(failures) == 0,
            model_name=model_name,
            model_version=model_version,
            metrics=metrics,
            failures=failures
        )

    def promote_if_valid(
        self,
        model_name: str,
        model_version: str,
        target_stage: str = "Production"
    ) -> bool:
        """Promote model to target stage if validation passes."""
        result = self.validate_model(model_name, model_version)

        if result.passed:
            self.client.transition_model_version_stage(
                name=model_name,
                version=model_version,
                stage=target_stage,
                archive_existing_versions=True
            )
            print(f"Model {model_name} v{model_version} promoted to {target_stage}")
            return True
        else:
            print(f"Model validation failed:")
            for failure in result.failures:
                print(f"  - {failure}")
            return False


def main():
    """CLI entry point for CI/CD integration."""
    import argparse

    parser = argparse.ArgumentParser(description="Model validation gate")
    parser.add_argument("--model-name", required=True)
    parser.add_argument("--model-version", required=True)
    parser.add_argument("--target-stage", default="Production")
    parser.add_argument("--min-accuracy", type=float, default=0.85)
    parser.add_argument("--min-f1", type=float, default=0.80)
    args = parser.parse_args()

    client = MlflowClient()
    thresholds = ValidationThresholds(
        min_accuracy=args.min_accuracy,
        min_f1_score=args.min_f1
    )

    gate = ModelValidationGate(client, thresholds)
    success = gate.promote_if_valid(
        args.model_name,
        args.model_version,
        args.target_stage
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
```

**Why compliant:** Implements automated quality gates for model promotion, validates against configurable thresholds, provides clear failure messages, returns proper exit codes for CI/CD integration, and ensures only validated models reach production.

---

## VIOLATION: No Automated Testing in Pipeline

```yaml
# .github/workflows/deploy.yml
name: Deploy ML Pipeline

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to production
        run: |
          # Skip tests - takes too long
          # Skip validation - we tested locally
          kfp pipeline upload pipeline.py --name production-pipeline

          # Deploy model directly
          mlflow models serve -m models:/my-model/Production -p 8000
```

**Why violates ENG-5.1:** This violates CI/CD best practices by: (1) having no automated tests in the pipeline, (2) deploying directly to production without staging, (3) skipping validation steps, (4) no quality gates or approval processes, and (5) no environment separation.

---

## VIOLATION: Manual Deployment Process

```python
# deploy_model.py
"""Manual deployment script - run from laptop."""

import mlflow
from mlflow.tracking import MlflowClient


def deploy_to_production():
    """Manually deploy model to production."""
    client = MlflowClient()

    # Find latest model version
    versions = client.search_model_versions("name='my-model'")
    latest = max(versions, key=lambda v: int(v.version))

    # Skip validation - we're in a hurry
    print(f"Deploying version {latest.version} to production...")

    # Promote directly to production
    client.transition_model_version_stage(
        name="my-model",
        version=latest.version,
        stage="Production",
        archive_existing_versions=True
    )

    print("Done! Model is now in production.")
    print("Remember to test it manually later...")


if __name__ == "__main__":
    # Run from developer laptop
    deploy_to_production()
```

**Why violates ENG-5.1:** This violates CI/CD by: (1) using manual deployment from a developer laptop, (2) no validation before production promotion, (3) no audit trail or version tracking, (4) no rollback mechanism, (5) depending on developer machine state, and (6) encouraging "deploy first, test later" anti-pattern.

---

## COMPLIANT: Kubeflow Pipeline Deployment Automation

```python
# scripts/deploy_pipeline.py
"""Automated Kubeflow pipeline deployment with validation."""

import kfp
from kfp import Client
from kfp.compiler import Compiler
import yaml
import hashlib
import logging
from datetime import datetime
from typing import Optional
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PipelineDeployer:
    """Manages Kubeflow pipeline deployments with safety checks."""

    def __init__(
        self,
        kubeflow_host: str,
        namespace: str = "kubeflow",
        token: Optional[str] = None
    ):
        self.client = Client(
            host=kubeflow_host,
            namespace=namespace,
            existing_token=token
        )
        self.namespace = namespace

    def validate_pipeline(self, pipeline_path: str) -> bool:
        """Validate pipeline YAML before deployment."""
        logger.info(f"Validating pipeline: {pipeline_path}")

        with open(pipeline_path, "r") as f:
            pipeline_spec = yaml.safe_load(f)

        # Check required fields
        if "pipelineSpec" not in pipeline_spec:
            logger.error("Missing pipelineSpec in pipeline YAML")
            return False

        # Check for components
        components = pipeline_spec.get("pipelineSpec", {}).get("components", {})
        if not components:
            logger.error("Pipeline has no components defined")
            return False

        # Validate resource limits are set
        for name, component in components.items():
            executor = component.get("executorLabel", "")
            if not self._has_resource_limits(pipeline_spec, executor):
                logger.warning(f"Component {name} missing resource limits")

        logger.info("Pipeline validation passed")
        return True

    def _has_resource_limits(self, spec: dict, executor_label: str) -> bool:
        """Check if executor has resource limits defined."""
        executors = spec.get("deploymentSpec", {}).get("executors", {})
        executor = executors.get(executor_label, {})
        container = executor.get("container", {})
        resources = container.get("resources", {})
        return bool(resources.get("limits"))

    def deploy_pipeline(
        self,
        pipeline_path: str,
        pipeline_name: str,
        version: str,
        environment: str,
        dry_run: bool = False
    ) -> Optional[str]:
        """Deploy pipeline with version tracking."""

        # Validate first
        if not self.validate_pipeline(pipeline_path):
            raise ValueError("Pipeline validation failed")

        # Calculate pipeline hash for dedup
        with open(pipeline_path, "rb") as f:
            pipeline_hash = hashlib.sha256(f.read()).hexdigest()[:12]

        versioned_name = f"{pipeline_name}-{environment}-{version[:8]}"

        if dry_run:
            logger.info(f"DRY RUN: Would deploy {versioned_name}")
            return None

        # Check if version already exists
        existing = self.client.list_pipelines(
            filter=f'name="{versioned_name}"'
        )
        if existing.pipelines:
            logger.info(f"Pipeline version {versioned_name} already exists")
            return existing.pipelines[0].pipeline_id

        # Upload pipeline
        logger.info(f"Deploying pipeline: {versioned_name}")
        result = self.client.upload_pipeline(
            pipeline_package_path=pipeline_path,
            pipeline_name=versioned_name,
            description=f"Deployed at {datetime.utcnow().isoformat()} from {version}"
        )

        logger.info(f"Pipeline deployed with ID: {result.pipeline_id}")
        return result.pipeline_id

    def create_recurring_run(
        self,
        pipeline_id: str,
        experiment_name: str,
        cron_schedule: str,
        parameters: dict
    ) -> str:
        """Create recurring run for scheduled training."""

        # Get or create experiment
        experiment = self.client.create_experiment(
            name=experiment_name,
            namespace=self.namespace
        )

        # Create recurring run
        job = self.client.create_recurring_run(
            experiment_id=experiment.experiment_id,
            job_name=f"{experiment_name}-scheduled",
            pipeline_id=pipeline_id,
            cron_expression=cron_schedule,
            params=parameters,
            enabled=True
        )

        logger.info(f"Created recurring run: {job.id}")
        return job.id


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--pipeline-file", required=True)
    parser.add_argument("--pipeline-name", default="ml-training-pipeline")
    parser.add_argument("--environment", required=True, choices=["staging", "production"])
    parser.add_argument("--version", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--require-approval", action="store_true")
    args = parser.parse_args()

    if args.require_approval and args.environment == "production":
        approval = os.environ.get("DEPLOYMENT_APPROVED", "false")
        if approval.lower() != "true":
            logger.error("Production deployment requires approval")
            exit(1)

    deployer = PipelineDeployer(
        kubeflow_host=os.environ["KUBEFLOW_HOST"],
        token=os.environ.get("KUBEFLOW_TOKEN")
    )

    pipeline_id = deployer.deploy_pipeline(
        pipeline_path=args.pipeline_file,
        pipeline_name=args.pipeline_name,
        version=args.version,
        environment=args.environment,
        dry_run=args.dry_run
    )

    if pipeline_id:
        print(f"::set-output name=pipeline_id::{pipeline_id}")


if __name__ == "__main__":
    main()
```

**Why compliant:** Validates pipelines before deployment, tracks versions with commit hashes, supports dry-run mode, requires approval for production, creates audit trail with timestamps, and handles idempotent deployments.

---

## COMPLIANT: Model Rollback Automation

```python
# scripts/rollback_model.py
"""Automated model rollback with safety checks."""

import mlflow
from mlflow.tracking import MlflowClient
import logging
from datetime import datetime
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelRollbackManager:
    """Manages safe model rollbacks with audit trail."""

    def __init__(self, client: MlflowClient):
        self.client = client

    def get_previous_production_version(
        self,
        model_name: str
    ) -> Optional[str]:
        """Find the previous production version for rollback."""
        versions = self.client.search_model_versions(
            f"name='{model_name}'",
            order_by=["version_number DESC"]
        )

        production_versions = [
            v for v in versions
            if v.current_stage == "Archived"
            and v.tags.get("previous_stage") == "Production"
        ]

        if not production_versions:
            logger.warning("No previous production version found")
            return None

        return production_versions[0].version

    def rollback(
        self,
        model_name: str,
        target_version: Optional[str] = None,
        reason: str = "Manual rollback"
    ) -> bool:
        """Rollback to previous or specified version."""

        # Get current production version
        current_versions = self.client.get_latest_versions(
            model_name, stages=["Production"]
        )

        if not current_versions:
            logger.error("No current production version to rollback from")
            return False

        current_version = current_versions[0]

        # Determine target version
        if target_version is None:
            target_version = self.get_previous_production_version(model_name)
            if target_version is None:
                logger.error("Cannot determine rollback target")
                return False

        logger.info(
            f"Rolling back {model_name} from v{current_version.version} "
            f"to v{target_version}"
        )

        # Archive current version with rollback metadata
        self.client.set_model_version_tag(
            model_name,
            current_version.version,
            "rollback_reason",
            reason
        )
        self.client.set_model_version_tag(
            model_name,
            current_version.version,
            "rollback_timestamp",
            datetime.utcnow().isoformat()
        )

        # Promote target version back to production
        self.client.transition_model_version_stage(
            name=model_name,
            version=target_version,
            stage="Production",
            archive_existing_versions=True
        )

        logger.info(f"Rollback complete. v{target_version} is now in Production")
        return True


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--model-name", required=True)
    parser.add_argument("--target-version", help="Specific version to rollback to")
    parser.add_argument("--reason", default="CI/CD triggered rollback")
    args = parser.parse_args()

    client = MlflowClient()
    manager = ModelRollbackManager(client)

    success = manager.rollback(
        model_name=args.model_name,
        target_version=args.target_version,
        reason=args.reason
    )

    exit(0 if success else 1)


if __name__ == "__main__":
    main()
```

**Why compliant:** Provides automated rollback capability, maintains audit trail with reasons and timestamps, safely archives current version before rollback, finds previous production version automatically, and integrates with CI/CD through exit codes.

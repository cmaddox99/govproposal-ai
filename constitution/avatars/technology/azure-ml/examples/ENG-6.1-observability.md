---
law_id: ENG-6.1
avatar: azure-ml
---

# ENG-6.1: Observability Examples for Azure Machine Learning

## COMPLIANT: Comprehensive ML Observability with Azure Monitor

```python
"""
Azure ML observability implementation with structured logging,
metrics tracking, and distributed tracing for ML pipelines.
"""
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace, metrics
from opentelemetry.trace import Status, StatusCode
import mlflow
import logging
import json

# Configure Azure Monitor for distributed tracing
configure_azure_monitor(
    connection_string="InstrumentationKey=xxx"
)

tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)

# Custom metrics for ML operations
training_duration = meter.create_histogram(
    "ml.training.duration_seconds",
    description="Duration of training jobs"
)
prediction_latency = meter.create_histogram(
    "ml.inference.latency_ms",
    description="Inference latency in milliseconds"
)
model_accuracy = meter.create_gauge(
    "ml.model.accuracy",
    description="Model accuracy metric"
)


@dataclass(frozen=True)
class TrainingContext:
    """Immutable context for training observability."""
    experiment_name: str
    run_id: str
    compute_target: str
    model_name: str
    started_at: datetime


class ObservableAzureMLTrainer:
    """Azure ML trainer with comprehensive observability."""

    def __init__(self, ml_client, logger: logging.Logger):
        self._ml_client = ml_client
        self._logger = logger

    def train_model(
        self,
        experiment_name: str,
        training_config: Dict[str, Any]
    ) -> str:
        """Train model with full observability."""

        with tracer.start_as_current_span("ml.training.job") as span:
            run_id = self._generate_run_id()
            context = TrainingContext(
                experiment_name=experiment_name,
                run_id=run_id,
                compute_target=training_config["compute"],
                model_name=training_config["model_name"],
                started_at=datetime.now(timezone.utc)
            )

            # Add trace attributes for correlation
            span.set_attribute("ml.experiment", experiment_name)
            span.set_attribute("ml.run_id", run_id)
            span.set_attribute("ml.compute", training_config["compute"])

            self._logger.info(
                "Training job started",
                extra={
                    "event": "training.started",
                    "experiment": experiment_name,
                    "run_id": run_id,
                    "compute_target": training_config["compute"],
                    "hyperparameters": json.dumps(training_config.get("hyperparameters", {}))
                }
            )

            try:
                # Submit and monitor job
                job = self._submit_job(training_config, context)
                self._monitor_job(job, context, span)

                # Record metrics
                duration = (datetime.now(timezone.utc) - context.started_at).total_seconds()
                training_duration.record(
                    duration,
                    {"experiment": experiment_name, "status": "success"}
                )

                # Log model metrics to MLflow
                with mlflow.start_run(run_id=run_id):
                    mlflow.log_metrics(job.metrics)
                    mlflow.log_param("compute_target", training_config["compute"])

                span.set_status(Status(StatusCode.OK))
                self._logger.info(
                    "Training job completed",
                    extra={
                        "event": "training.completed",
                        "run_id": run_id,
                        "duration_seconds": duration,
                        "metrics": job.metrics
                    }
                )

                return run_id

            except Exception as e:
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.record_exception(e)
                training_duration.record(
                    (datetime.now(timezone.utc) - context.started_at).total_seconds(),
                    {"experiment": experiment_name, "status": "failed"}
                )
                self._logger.error(
                    "Training job failed",
                    extra={
                        "event": "training.failed",
                        "run_id": run_id,
                        "error": str(e),
                        "error_type": type(e).__name__
                    },
                    exc_info=True
                )
                raise

    def _monitor_job(self, job, context: TrainingContext, span) -> None:
        """Monitor job progress with periodic logging."""
        with tracer.start_as_current_span("ml.training.monitor", parent=span):
            while job.status not in ["Completed", "Failed", "Canceled"]:
                self._logger.debug(
                    "Training job progress",
                    extra={
                        "event": "training.progress",
                        "run_id": context.run_id,
                        "status": job.status,
                        "current_epoch": job.current_epoch
                    }
                )
                job.refresh()
```

**Why compliant:** Implements structured logging, distributed tracing with OpenTelemetry, custom metrics for ML operations, and correlates all observability data with run IDs.

---

## VIOLATION: Missing Observability in ML Pipeline

```python
# BAD: No logging, metrics, or tracing
class AzureMLTrainer:
    def __init__(self, ml_client):
        self.ml_client = ml_client

    def train(self, config):
        # VIOLATION: No logging of job start
        # VIOLATION: No tracing context
        job = self.ml_client.jobs.create_or_update(config)

        # VIOLATION: Silent waiting with no progress indication
        while job.status not in ["Completed", "Failed"]:
            job = self.ml_client.jobs.get(job.name)

        # VIOLATION: No metrics recorded
        # VIOLATION: No duration tracking
        # VIOLATION: No error context on failure
        if job.status == "Failed":
            raise Exception("Training failed")

        return job

    def deploy(self, model_name, endpoint_name):
        # VIOLATION: No deployment observability
        # VIOLATION: No correlation with training run
        endpoint = self.ml_client.online_endpoints.begin_create_or_update(
            OnlineEndpoint(name=endpoint_name)
        ).result()

        # VIOLATION: No latency tracking
        # VIOLATION: No health metrics
        return endpoint
```

**Why violates ENG-6.1:** No structured logging, missing distributed tracing, no custom metrics for ML operations, impossible to debug production issues or correlate training with inference.

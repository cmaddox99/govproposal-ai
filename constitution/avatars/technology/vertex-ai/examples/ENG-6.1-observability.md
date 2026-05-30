---
law_id: ENG-6.1
avatar: vertex-ai
---

# ENG-6.1: Observability Examples for Google Vertex AI

## COMPLIANT: Comprehensive Vertex AI Observability with Cloud Monitoring

```python
"""
Vertex AI observability with Cloud Monitoring, Cloud Trace,
and structured logging for ML pipelines.
"""
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional
from google.cloud import monitoring_v3, logging as cloud_logging
from opentelemetry import trace
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
import google.cloud.aiplatform as aiplatform
import structlog

# Configure Cloud Trace exporter
trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(CloudTraceSpanExporter())
)

tracer = trace.get_tracer(__name__)
logger = structlog.get_logger()


@dataclass(frozen=True)
class TrainingContext:
    """Immutable context for training observability."""
    experiment_name: str
    run_id: str
    job_name: str
    started_at: datetime


class ObservableVertexTrainer:
    """Vertex AI trainer with comprehensive observability."""

    def __init__(
        self,
        project: str,
        location: str,
        metrics_client: monitoring_v3.MetricServiceClient,
        log_client: cloud_logging.Client
    ):
        self._project = project
        self._location = location
        self._metrics = metrics_client
        self._logger = log_client.logger("vertex-training")
        aiplatform.init(project=project, location=location)

    def train_model(
        self,
        experiment_name: str,
        training_config: dict
    ) -> str:
        """Train model with full observability."""

        with tracer.start_as_current_span("vertex.training.job") as span:
            run_id = self._generate_run_id()
            context = TrainingContext(
                experiment_name=experiment_name,
                run_id=run_id,
                job_name=f"{experiment_name}-{run_id}",
                started_at=datetime.now(timezone.utc)
            )

            # Add trace attributes for correlation
            span.set_attribute("vertex.experiment", experiment_name)
            span.set_attribute("vertex.run_id", run_id)
            span.set_attribute("vertex.machine_type", training_config["machine_type"])

            # Structured log entry
            self._logger.log_struct({
                "event": "training.started",
                "experiment": experiment_name,
                "run_id": run_id,
                "machine_type": training_config["machine_type"],
                "accelerator": training_config.get("accelerator_type"),
                "severity": "INFO"
            })

            try:
                # Create and run job with monitoring
                job = self._create_custom_job(training_config, context)
                self._monitor_job(job, context, span)

                # Record custom metrics
                duration = (datetime.now(timezone.utc) - context.started_at).total_seconds()
                self._write_metric(
                    "custom.googleapis.com/vertex/training/duration_seconds",
                    duration,
                    {"experiment": experiment_name, "status": "success"}
                )

                span.set_status(trace.Status(trace.StatusCode.OK))

                self._logger.log_struct({
                    "event": "training.completed",
                    "run_id": run_id,
                    "duration_seconds": duration,
                    "metrics": job.gca_resource.training_task_metadata,
                    "severity": "INFO"
                })

                return run_id

            except Exception as e:
                span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
                span.record_exception(e)

                self._write_metric(
                    "custom.googleapis.com/vertex/training/duration_seconds",
                    (datetime.now(timezone.utc) - context.started_at).total_seconds(),
                    {"experiment": experiment_name, "status": "failed"}
                )

                self._logger.log_struct({
                    "event": "training.failed",
                    "run_id": run_id,
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "severity": "ERROR"
                })
                raise

    def _monitor_job(
        self,
        job: aiplatform.CustomJob,
        context: TrainingContext,
        span
    ) -> None:
        """Monitor job progress with periodic logging."""
        with tracer.start_as_current_span("vertex.training.monitor", parent=span):
            while job.state not in ["JOB_STATE_SUCCEEDED", "JOB_STATE_FAILED", "JOB_STATE_CANCELLED"]:
                self._logger.log_struct({
                    "event": "training.progress",
                    "run_id": context.run_id,
                    "state": str(job.state),
                    "severity": "DEBUG"
                })
                job._sync_gca_resource()

    def _write_metric(self, metric_type: str, value: float, labels: dict) -> None:
        """Write custom metric to Cloud Monitoring."""
        series = monitoring_v3.TimeSeries()
        series.metric.type = metric_type
        series.metric.labels.update(labels)
        series.resource.type = "global"

        point = monitoring_v3.Point()
        point.value.double_value = value
        now = datetime.now(timezone.utc)
        point.interval.end_time.seconds = int(now.timestamp())
        series.points.append(point)

        self._metrics.create_time_series(
            name=f"projects/{self._project}",
            time_series=[series]
        )


class VertexEndpointMonitor:
    """Monitor Vertex AI endpoints for prediction latency and errors."""

    def __init__(self, project: str, endpoint_id: str):
        self._project = project
        self._endpoint_id = endpoint_id

    async def get_endpoint_metrics(self) -> dict:
        """Get prediction latency and error metrics."""
        # Query Cloud Monitoring for endpoint metrics
        return {
            "prediction_count": await self._query_metric(
                "aiplatform.googleapis.com/prediction/count"
            ),
            "prediction_latency_p50": await self._query_metric(
                "aiplatform.googleapis.com/prediction/latencies",
                percentile=50
            ),
            "prediction_latency_p99": await self._query_metric(
                "aiplatform.googleapis.com/prediction/latencies",
                percentile=99
            ),
            "error_count": await self._query_metric(
                "aiplatform.googleapis.com/prediction/error_count"
            )
        }
```

**Why compliant:** Uses Cloud Trace for distributed tracing, Cloud Monitoring for custom metrics, Cloud Logging for structured logs. All observability data is correlated via run IDs and trace context.

---

## VIOLATION: No Observability in Vertex AI Pipeline

```python
# BAD: Vertex AI training with no observability
class VertexTrainer:
    def __init__(self, project, location):
        aiplatform.init(project=project, location=location)

    def train(self, config):
        # VIOLATION: No logging of job start
        # VIOLATION: No tracing context
        job = aiplatform.CustomJob(
            display_name="training",
            worker_pool_specs=[config]
        )

        # VIOLATION: Silent execution with no progress indication
        job.run(sync=True)

        # VIOLATION: No metrics recorded
        # VIOLATION: No duration tracking
        # VIOLATION: No error context on failure
        if job.state != "JOB_STATE_SUCCEEDED":
            raise Exception("Training failed")

        return job

    def deploy(self, model_uri, endpoint_name):
        # VIOLATION: No deployment observability
        model = aiplatform.Model.upload(artifact_uri=model_uri)
        endpoint = aiplatform.Endpoint.create(display_name=endpoint_name)

        # VIOLATION: No latency tracking
        # VIOLATION: No health monitoring
        model.deploy(endpoint=endpoint)
        return endpoint
```

**Why violates ENG-6.1:** No structured logging, missing distributed tracing, no custom metrics for training duration or model performance, impossible to debug production issues or track ML experiments.

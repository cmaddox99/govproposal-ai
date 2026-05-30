---
laws: [ENG-6.1, ENG-6.4, ENG-6.7]
avatar: [tensorflow]
title: Security Laws — TensorFlow
---

# Security Laws: ENG-6.1, ENG-6.4, ENG-6.7 — TensorFlow

## ENG-6.1: Security by Design

No credentials in notebooks or `SavedModel` artifacts. Validate input tensors at inference. Restrict TensorFlow Serving access.

```python
import os, tensorflow as tf

# ✅ Cloud credentials from environment / IAM role — never in notebooks
MODEL_BUCKET = os.environ["MODEL_ARTIFACT_BUCKET"]
# boto3 / google-cloud-storage uses IAM role automatically when key is absent

# ❌ NEVER in .ipynb or TFX pipeline config
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/key.json"  # baked in
```

Validate input tensors with a custom Keras validation layer:

```python
import tensorflow as tf

class InputValidationLayer(tf.keras.layers.Layer):
    def __init__(self, expected_shape, value_range, **kwargs):
        super().__init__(**kwargs)
        self.expected_shape = expected_shape
        self.value_range    = value_range

    def call(self, inputs):
        tf.debugging.assert_rank(inputs, len(self.expected_shape) + 1,
            message="Unexpected input rank")
        tf.debugging.assert_greater_equal(inputs, tf.cast(self.value_range[0], inputs.dtype),
            message="Input values below minimum")
        tf.debugging.assert_less_equal(inputs, tf.cast(self.value_range[1], inputs.dtype),
            message="Input values above maximum")
        return inputs

# Add as first layer in inference model
inference_model = tf.keras.Sequential([
    InputValidationLayer(expected_shape=(64,), value_range=(0.0, 1.0)),
    saved_model_layer,
])
```

TensorFlow Serving — restrict to internal callers via nginx auth proxy; do not expose port 8501 publicly.

## ENG-6.4: Data Protection

Remove PII from TFRecord files. Use TFDV for schema validation that detects unexpected PII columns.

```python
import tensorflow as tf
import hashlib

PII_FEATURE_KEYS = {"passenger_name", "email", "loyalty_number"}

def write_tfrecord(records: list[dict], output_path: str) -> None:
    with tf.io.TFRecordWriter(output_path) as writer:
        for record in records:
            present_pii = PII_FEATURE_KEYS & set(record.keys())
            if present_pii:
                raise ValueError(f"PII features must not appear in TFRecord: {present_pii}")
            example = tf.train.Example(features=tf.train.Features(feature={
                k: tf.train.Feature(float_list=tf.train.FloatList(value=[v]))
                for k, v in record.items()
            }))
            writer.write(example.SerializeToString())
```

TFDV schema validation to detect unexpected PII columns:

```python
import tensorflow_data_validation as tfdv

schema = tfdv.load_schema_text("schema/demand_schema.pbtxt")
# Enforce no unexpected features (catches accidental PII columns)
tfdv.validate_statistics(
    statistics=tfdv.generate_statistics_from_csv("data/features.csv"),
    schema=schema,
)
```

Keras callbacks must not log raw batch data:

```python
class AuditCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        # ✅ Log metrics only — not batch samples
        safe_logs = {k: float(v) for k, v in (logs or {}).items()}
        logger.info("epoch_end", epoch=epoch, metrics=safe_logs)
        # ❌ NEVER: logger.info("batch: %s", self.model.inputs)
```

## ENG-6.7: Audit Trail

Use TFX MLMD for artifact provenance. Log prediction requests with `request_id` (correlation ID) and input shape — never raw input data.

```python
import mlflow, os, hashlib, pathlib

def log_training_run(dataset_path: str, config: dict, metrics: dict) -> str:
    dataset_hash = hashlib.sha256(
        pathlib.Path(dataset_path).read_bytes()
    ).hexdigest()[:16]

    with mlflow.start_run() as run:
        mlflow.log_params({
            "dataset_hash":   dataset_hash,
            "code_commit":    os.environ.get("GIT_COMMIT_SHA", "unknown"),
            "tf_version":     tf.__version__,
            "model_arch":     config.get("architecture"),
        })
        mlflow.log_metrics(metrics)
        mlflow.tensorflow.log_model(model, artifact_path="model")
        # ❌ NEVER delete: mlflow.delete_run(run.info.run_id)
        return run.info.run_id
```

TF Serving prediction log — safe fields only:

```python
import structlog, time, hashlib

log = structlog.get_logger()

def serve_predict(input_tensor, request_id: str):
    input_hash = hashlib.sha256(input_tensor.numpy().tobytes()).hexdigest()[:16]
    start = time.monotonic()
    result = model(input_tensor)
    latency_ms = (time.monotonic() - start) * 1000

    log.info("tf_serving_predict",
             request_id=request_id,           # correlation ID from API gateway
             input_shape=list(input_tensor.shape),
             input_hash=input_hash,           # ✅ not raw input
             confidence_max=float(result.numpy().max()),
             latency_ms=round(latency_ms, 2))
    # ❌ NEVER: tf.print(inputs) in production serving code
    return result
```

Model approval workflow logged to append-only audit store:

```python
await db.execute(
    "INSERT INTO model_deployment_audit (run_id, deployed_by, approved_by, deployed_at, serving_endpoint) "
    "VALUES (:r, :d, :a, now(), :e)",
    {"r": run_id, "d": deployer_id, "a": approver_id, "e": endpoint_name},
)
```

## Anti-Patterns

1. **Credentials in TFX pipeline config YAML** — service account keys in `pipeline.yaml` or `runner_config.json` are committed to Git; use Workload Identity or environment injection.
2. **PII columns in TFRecord features** — `passenger_name` or `email` as TFRecord string features are stored in plaintext; strip before writing with schema validation.
3. **`tf.print(inputs)` in production** — TF print ops execute during graph evaluation and write tensor values to stdout; remove before deploying to serving infrastructure.
4. **No model versioning** — deploying a `SavedModel` without recording the MLflow run ID means there is no way to tie a production prediction to a training dataset or code commit.
5. **TensorBoard logging raw data batches with PII** — `tf.summary.image` or `tf.summary.text` callbacks that log raw batch samples expose passenger data to anyone with TensorBoard access.

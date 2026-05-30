---
laws: [ENG-6.1, ENG-6.4, ENG-6.7]
avatar: [pytorch]
title: Security Laws — PyTorch
---

# Security Laws: ENG-6.1, ENG-6.4, ENG-6.7 — PyTorch

## ENG-6.1: Security by Design

No credentials in notebook cells or checkpoint files. Validate model inputs before inference. Use environment variables for all cloud access.

```python
import os, torch
from torch import Tensor

# ✅ Cloud credentials from environment only
S3_BUCKET   = os.environ["MODEL_ARTIFACT_BUCKET"]
AWS_PROFILE = os.environ.get("AWS_PROFILE", "default")  # or IAM role

# ❌ NEVER in a notebook cell
# S3_BUCKET = "aa-ml-models"
# boto3.client("s3", aws_access_key_id="AKIAIOSFODNN7EXAMPLE", ...)
```

Validate input tensors before inference:

```python
def validate_input(tensor: Tensor, expected_shape: tuple,
                   value_range: tuple[float, float]) -> None:
    if tensor.shape[1:] != expected_shape:
        raise ValueError(f"Expected shape {expected_shape}, got {tensor.shape[1:]}")
    if tensor.dtype not in (torch.float32, torch.float16):
        raise TypeError(f"Unexpected dtype: {tensor.dtype}")
    if not (tensor >= value_range[0]).all() or not (tensor <= value_range[1]).all():
        raise ValueError(f"Tensor values outside expected range {value_range}")

# Usage before model inference
validate_input(input_tensor, expected_shape=(64,), value_range=(0.0, 1.0))
predictions = model(input_tensor)
```

Checkpoint files must not contain training data or credentials:

```python
# ✅ Save model weights + metadata dict only
torch.save({
    "model_state_dict": model.state_dict(),
    "run_id":           run_id,
    "model_version":    "demand-forecast-v3",
    "epoch":            epoch,
    # ❌ NEVER include: "training_data": dataset, "api_key": key
}, checkpoint_path)
```

## ENG-6.4: Data Protection

Strip PII identifiers from datasets before `torch.save`. Use Opacus for differential privacy when training on personal data.

```python
import pandas as pd, hashlib

PII_COLUMNS = {"passenger_name", "email", "loyalty_number", "pnr"}

def strip_pii(df: pd.DataFrame) -> pd.DataFrame:
    present_pii = PII_COLUMNS & set(df.columns)
    if present_pii:
        raise ValueError(f"PII columns must be removed before tensor conversion: {present_pii}")
    return df

# Build dataset from clean DataFrame only
clean_df = strip_pii(raw_df)
tensors  = torch.tensor(clean_df.values, dtype=torch.float32)
# ✅ Safe to save
torch.save(tensors, "data/demand_features.pt")

# ❌ NEVER
# torch.save(raw_df_with_passenger_names, "data/passengers.pt")
```

Differential privacy for models trained on personal data (Opacus):

```python
from opacus import PrivacyEngine

privacy_engine = PrivacyEngine()
model, optimizer, train_loader = privacy_engine.make_private_with_epsilon(
    module=model,
    optimizer=optimizer,
    data_loader=train_loader,
    epochs=10,
    target_epsilon=8.0,   # ε — lower = more private
    target_delta=1e-5,
    max_grad_norm=1.0,
)
```

Model cards must document PII handling — note in `README.md` alongside the model:

```markdown
## Data Lineage
- Training data: anonymized flight demand features (no passenger PII)
- PII handling: passenger identifiers removed via `strip_pii()` before featurization
- Dataset hash: sha256:abc123...
```

## ENG-6.7: Audit Trail

Log every training run with MLflow. Log model serving predictions using input hash, not raw input.

```python
import mlflow, hashlib, pathlib

def hash_file(path: str) -> str:
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()[:16]

with mlflow.start_run() as run:
    mlflow.log_params({
        "architecture":   "ResNet18",
        "batch_size":     128,
        "learning_rate":  1e-3,
        "dataset_hash":   hash_file("data/demand_features.pt"),
        "git_commit":     os.environ.get("GIT_COMMIT_SHA", "unknown"),
    })
    # ... training loop ...
    mlflow.log_metrics({"val_loss": val_loss, "val_mae": val_mae})
    mlflow.pytorch.log_model(model, artifact_path="model")
    # ❌ NEVER delete: mlflow.delete_run(run.info.run_id)
    print(f"MLflow Run ID: {run.info.run_id}")
```

Log serving predictions safely (input hash, not raw data):

```python
import hashlib, structlog, time

log = structlog.get_logger()

def predict(tensor: Tensor, correlation_id: str) -> Tensor:
    input_hash = hashlib.sha256(tensor.numpy().tobytes()).hexdigest()[:16]
    start = time.monotonic()
    with torch.no_grad():
        output = model(tensor)
    latency_ms = (time.monotonic() - start) * 1000

    log.info("model_prediction",
             input_hash=input_hash,      # ✅ hash only — not raw tensor data
             output_shape=list(output.shape),
             latency_ms=round(latency_ms, 2),
             correlation_id=correlation_id)
    return output
```

## Anti-Patterns

1. **Credentials in `.ipynb` notebook cells (visible in JSON)** — Jupyter stores cell outputs in JSON; any `print(api_key)` or variable assignment with a secret is committed and visible in Git diff.
2. **`torch.save(dataset_with_pii, "data.pt")`** — saves raw passenger tensors that include PII identifiers to disk; strip PII before converting to tensors.
3. **No input validation before `model(tensor)`** — unexpected tensor shapes or out-of-range values cause silent incorrect predictions or CUDA errors; validate before every inference call.
4. **Logging raw prediction inputs when they contain PII** — a serving log line like `logger.info("input: %s", tensor.tolist())` writes flight-passenger association data to log aggregators.
5. **Sharing checkpoints without data lineage documentation** — a checkpoint file without a corresponding model card leaves no record of what data was used or whether PII was present during training.

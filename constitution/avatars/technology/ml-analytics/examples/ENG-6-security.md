---
laws: [ENG-6.1, ENG-6.4, ENG-6.7]
avatar: [ml-analytics]
title: Security Laws — ML Analytics
---

# Security Laws: ENG-6.1, ENG-6.4, ENG-6.7 — ML Analytics

## ENG-6.1: Security by Design

Never embed credentials in notebook cells. Load all secrets via environment variables or a secrets manager. Validate DataFrames before inference.

```python
# ✅ Load credentials from environment — never hardcode
import os
from dotenv import load_dotenv

load_dotenv()                                    # reads .env (gitignored)
ADLS_ACCOUNT_KEY = os.environ["ADLS_ACCOUNT_KEY"]
DB_URL           = os.environ["DATABASE_URL"]

# ❌ NEVER in a notebook cell
# ADLS_ACCOUNT_KEY = "aBcDeFgH1234..."
```

Validate input DataFrames before model inference:

```python
import pandas as pd
from typing import List

REQUIRED_COLUMNS = {"flight_id", "day_of_week", "historical_load_factor", "route_code"}
EXPECTED_DTYPES  = {"historical_load_factor": float, "day_of_week": int}

def validate_inference_input(df: pd.DataFrame) -> None:
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    if df["historical_load_factor"].between(0.0, 1.0).sum() != len(df):
        raise ValueError("historical_load_factor must be in [0, 1]")
    pii_cols = {"passenger_name", "email", "loyalty_number"} & set(df.columns)
    if pii_cols:
        raise ValueError(f"PII columns must not reach inference: {pii_cols}")

validate_inference_input(df)
predictions = model.predict(df[REQUIRED_COLUMNS])
```

## ENG-6.4: Data Protection

Pseudonymize PII before storing training data. Never commit raw PII to Git or save it to CSV.

```python
import hashlib

def pseudonymize(df: pd.DataFrame, pii_cols: List[str]) -> pd.DataFrame:
    """Replace PII with one-way hash. Irreversible without salt."""
    salt = os.environ["PSEUDONYM_SALT"]
    for col in pii_cols:
        if col in df.columns:
            df[col] = df[col].apply(
                lambda v: hashlib.sha256(f"{salt}{v}".encode()).hexdigest()[:12]
            )
    return df

# ✅ Strip PII before saving any artifact
clean_df = pseudonymize(raw_df, pii_cols=["passenger_name", "email", "loyalty_number"])
clean_df.to_parquet("s3://aa-ml-data/demand/v3/features.parquet")  # SSE-KMS on bucket

# ❌ NEVER
# raw_df.to_csv("passengers_train.csv")  # PII committed to Git
```

Cloud storage encryption — enforce SSE-KMS at bucket/container level:

```python
import boto3

s3 = boto3.client("s3")
s3.put_object(
    Bucket="aa-ml-data",
    Key="demand/v3/features.parquet",
    Body=parquet_bytes,
    ServerSideEncryption="aws:kms",
    SSEKMSKeyId=os.environ["KMS_KEY_ARN"],
)
```

## ENG-6.7: Audit Trail

Log every training run with MLflow — immutable experiment records.

```python
import mlflow, hashlib

def hash_dataset(path: str) -> str:
    import hashlib, pathlib
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()[:16]

with mlflow.start_run(run_name="demand-forecast-v3") as run:
    mlflow.log_params({
        "model_type":          "GradientBoostingRegressor",
        "n_estimators":        300,
        "dataset_hash":        hash_dataset("data/features.parquet"),
        "feature_columns":     ",".join(REQUIRED_COLUMNS),
    })
    mlflow.log_metrics({"rmse": rmse, "mae": mae, "r2": r2})
    mlflow.sklearn.log_model(model, artifact_path="model")
    # MLflow run records are immutable — do not delete runs post-analysis
    print(f"Run ID: {run.info.run_id}")  # store for deployment audit
```

Record model deployment approval in audit store:

```python
# Append-only deployment log
await db.execute(
    "INSERT INTO model_deployment_audit "
    "(run_id, deployed_by, approved_by, deployed_at, endpoint) "
    "VALUES (:run_id, :by, :approved, now(), :ep)",
    {"run_id": run_id, "by": deployer_id, "approved": approver_id, "ep": endpoint},
)
```

## Anti-Patterns

1. **Credentials in Jupyter notebook cells** — `.ipynb` files store cell outputs in JSON; a key printed or assigned in a cell is committed and visible in Git history.
2. **Raw PII in training CSV committed to Git** — passenger names, loyalty numbers, and emails in a committed `data/passengers.csv` are never truly deletable from Git history.
3. **`df.to_csv("data.csv")` with PII columns** — saves PII to disk in plaintext; always pseudonymize and use encrypted cloud storage.
4. **No input validation before `model.predict()`** — unexpected columns or out-of-range values cause silent incorrect predictions or exceptions; validate schema and value ranges first.
5. **Deleting MLflow experiment runs** — removing runs destroys the audit chain for model lineage and compliance reviews; treat MLflow runs as immutable records.

---
laws: [ENG-6.1, ENG-6.4, ENG-6.7]
avatar: [legacy-ml-interop]
title: Security Laws — Legacy ML Interop
---

# Security Laws: ENG-6.1, ENG-6.4, ENG-6.7 — Legacy ML Interop

## ENG-6.1: Security by Design

The FastAPI wrapper is the security boundary. Validate all inputs before they reach the legacy subprocess. Run the subprocess as non-root with no shell expansion.

```python
# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
import subprocess, shlex, os

app = FastAPI()

class PredictRequest(BaseModel):
    flight_id: str
    passenger_count: int

    @field_validator("flight_id")
    @classmethod
    def validate_flight_id(cls, v: str) -> str:
        if not v.isalnum() or len(v) > 12:
            raise ValueError("Invalid flight_id")
        return v

    @field_validator("passenger_count")
    @classmethod
    def validate_count(cls, v: int) -> int:
        if not (1 <= v <= 500):
            raise ValueError("passenger_count out of range")
        return v

MODEL_SCRIPT = "/app/models/demand_forecast.R"

@app.post("/predict")
def predict(req: PredictRequest, correlation_id: str = Header(alias="X-Correlation-ID")):
    # ✅ List form — no shell=True, no injection possible
    result = subprocess.run(
        ["Rscript", MODEL_SCRIPT, req.flight_id, str(req.passenger_count)],
        capture_output=True, text=True, timeout=30,
        # subprocess runs as non-root via Docker USER directive
    )
    if result.returncode != 0:
        raise HTTPException(status_code=500, detail="Model execution failed")
    return {"prediction": result.stdout.strip(), "correlation_id": correlation_id}
```

Dockerfile enforces non-root execution:

```dockerfile
FROM python:3.11-slim
RUN adduser --disabled-password --gecos "" mluser
USER mluser           # ✅ non-root
COPY --chown=mluser:mluser . /app
```

Secrets reach the container via Docker Secrets, not baked-in ENV:

```yaml
# docker-compose.yml
services:
  legacy-ml:
    secrets:
      - db_password
    environment:
      DB_PASSWORD_FILE: /run/secrets/db_password
secrets:
  db_password:
    file: ./secrets/db_password.txt
```

## ENG-6.4: Data Protection

Legacy R/PySpark models may expect raw data files. Mask PII before passing to subprocess.

```python
import hashlib, pandas as pd

def prepare_model_input(df: pd.DataFrame) -> pd.DataFrame:
    """Remove PII columns before writing model input file."""
    pii_cols = {"passenger_name", "email", "loyalty_number"}
    present_pii = pii_cols & set(df.columns)
    if present_pii:
        raise ValueError(f"PII columns detected in model input: {present_pii}")
    return df

def hash_record_id(raw_id: str) -> str:
    """Replace reconstructable IDs with one-way hash for model input."""
    return hashlib.sha256(raw_id.encode()).hexdigest()[:16]
```

Never bake PII into the container image:

```dockerfile
# ❌ NEVER — PII-containing CSV baked into image layer
# COPY training_passengers.csv /app/data/

# ✅ Mount at runtime from encrypted volume
VOLUME ["/app/data"]
```

## ENG-6.7: Audit Trail

Log every model invocation using input hash (not raw input), model version, and correlation ID.

```python
import hashlib, time, structlog

log = structlog.get_logger()

def invoke_model(req: PredictRequest, correlation_id: str) -> str:
    input_hash = hashlib.sha256(
        f"{req.flight_id}:{req.passenger_count}".encode()
    ).hexdigest()

    model_version = os.environ.get("MODEL_VERSION", "unknown")
    start = time.monotonic()

    result = subprocess.run(
        ["Rscript", MODEL_SCRIPT, req.flight_id, str(req.passenger_count)],
        capture_output=True, text=True, timeout=30,
    )
    latency_ms = (time.monotonic() - start) * 1000

    log.info("model_invocation",
             correlation_id=correlation_id,
             model_version=model_version,
             input_hash=input_hash,          # ✅ hash only — not raw values
             latency_ms=round(latency_ms, 2),
             success=result.returncode == 0)
    # ❌ NEVER: log.info("input: %s", raw_dataframe)
    return result.stdout.strip()
```

Audit records written to an append-only store:

```sql
-- No UPDATE or DELETE permitted on model_audit
CREATE TABLE model_audit (
    id          BIGSERIAL PRIMARY KEY,
    recorded_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    correlation_id TEXT NOT NULL,
    model_version  TEXT NOT NULL,
    input_hash     TEXT NOT NULL,
    latency_ms     NUMERIC,
    success        BOOLEAN NOT NULL
);
REVOKE UPDATE, DELETE ON model_audit FROM app_role;
```

## Anti-Patterns

1. **`subprocess.run(command, shell=True)`** — any unsanitized string in `command` becomes a shell injection vector; always use list form with explicit argument separation.
2. **PII in model input CSV files** — a passenger list with names and emails committed to the repo or mounted into the container exposes PII to everyone with image access.
3. **Hardcoded paths to model artifacts** — `/home/developer/models/v2/demand.pkl` breaks between environments and reveals internal directory structure; use env-var-configured volume mounts.
4. **No input validation before subprocess call** — passing unsanitized API input directly to an R or PySpark script enables argument injection and crashes the model runtime.
5. **Legacy model logs containing raw PII** — R `print()` and PySpark `show()` default to printing full DataFrames; wrap legacy code output parsing and suppress or redact before forwarding to log aggregator.

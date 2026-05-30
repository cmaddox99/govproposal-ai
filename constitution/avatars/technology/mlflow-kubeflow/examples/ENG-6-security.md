---
laws: [ENG-6.1, ENG-6.4, ENG-6.7]
avatar: [mlflow-kubeflow]
title: Security Laws — MLflow / Kubeflow
---

# Security Laws: ENG-6.1, ENG-6.4, ENG-6.7 — MLflow / Kubeflow

## ENG-6.1: Security by Design

Kubeflow pipeline components run under least-privilege ServiceAccounts. MLflow Tracking Server requires authentication. No component runs as root.

```yaml
# pipeline-component.yaml — non-root, dedicated ServiceAccount
apiVersion: v1
kind: ServiceAccount
metadata:
  name: demand-forecast-sa
  namespace: ml-pipelines
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: demand-forecast-role
rules:
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get", "list"]    # least privilege — no create/delete
---
# Pipeline container spec
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
serviceAccountName: demand-forecast-sa
```

Secrets via Kubernetes Secrets (not hardcoded in pipeline YAML):

```python
# component.py — read secret from mounted volume
import pathlib

def get_db_password() -> str:
    secret_path = pathlib.Path("/var/run/secrets/db-password/password")
    return secret_path.read_text().strip()

# ❌ NEVER in pipeline YAML
# env:
#   - name: DB_PASSWORD
#     value: "SuperSecret123"
```

MLflow Tracking Server behind OIDC:

```bash
mlflow server \
  --backend-store-uri postgresql://... \
  --default-artifact-root s3://aa-ml-artifacts/ \
  --app-name basic-auth          # or deploy behind OAuth2 proxy
```

## ENG-6.4: Data Protection

Training data must be anonymized before pipeline ingestion. No PII in MLflow metadata.

```python
import mlflow

# ✅ Safe MLflow metadata — identifiers and hashes only
with mlflow.start_run() as run:
    mlflow.set_tags({
        "dataset.version":  "v3.2",
        "dataset.hash":     dataset_hash,      # SHA-256 of the anonymized dataset
        "pipeline.commit":  git_commit_sha,
        # ❌ NEVER: "passenger.sample": "John Doe, ABC123"
        # ❌ NEVER: "data.source": "s3://aa-raw/passengers_with_names.csv"
    })
```

S3 artifact store with SSE-KMS:

```python
import boto3

s3 = boto3.client("s3")
s3.put_bucket_encryption(
    Bucket="aa-ml-artifacts",
    ServerSideEncryptionConfiguration={
        "Rules": [{"ApplyServerSideEncryptionByDefault": {
            "SSEAlgorithm": "aws:kms",
            "KMSMasterKeyID": os.environ["ML_KMS_KEY_ARN"],
        }}]
    },
)
```

## ENG-6.7: Audit Trail

Every pipeline run produces an immutable MLflow record linking dataset version, code commit, and evaluation metrics. Pipeline run IDs are stored in downstream deployment systems for traceability.

```python
import mlflow, os, hashlib, pathlib

def log_pipeline_run(dataset_path: str, metrics: dict) -> str:
    dataset_hash = hashlib.sha256(
        pathlib.Path(dataset_path).read_bytes()
    ).hexdigest()

    with mlflow.start_run() as run:
        mlflow.log_params({
            "dataset_hash":    dataset_hash,
            "code_commit_sha": os.environ.get("GIT_COMMIT_SHA", "unknown"),
            "pipeline_name":   "demand-forecast",
            "kubeflow_run_id": os.environ.get("KFP_RUN_ID", ""),
        })
        mlflow.log_metrics(metrics)
        # ❌ NEVER delete this run: mlflow.delete_run(run.info.run_id)
        return run.info.run_id

# Store run_id in deployment record for traceability
run_id = log_pipeline_run(dataset_path, metrics={"rmse": 4.2, "mae": 3.1})
await db.execute(
    "INSERT INTO pipeline_audit (run_id, triggered_by, completed_at) VALUES (:r, :u, now())",
    {"r": run_id, "u": service_account_name},
)
```

Kubeflow pipeline completion/failure logged via exit handler:

```python
@dsl.pipeline(name="demand-forecast")
def demand_forecast_pipeline(dataset_version: str):
    train_op = train_model(dataset_version=dataset_version)
    with dsl.ExitHandler(exit_task=log_completion_op()):
        evaluate_op = evaluate_model(model=train_op.output)
```

## Anti-Patterns

1. **Hardcoding cloud credentials in pipeline YAML** — `env: [{name: AWS_SECRET_ACCESS_KEY, value: "..."}]` in a KFP YAML file exposes credentials to anyone with cluster read access.
2. **PII in MLflow run tags** — tags like `"passenger_sample": "J. Smith / PNR ABC123"` are stored in plaintext in the MLflow tracking DB and accessible to all project members.
3. **Running pipeline components as root** — `runAsNonRoot: false` violates least-privilege; a compromised component gains full node access.
4. **Deleting MLflow runs post-analysis** — removing runs breaks model lineage for audit, compliance, and incident investigation.
5. **No dataset versioning** — training a model without recording which exact dataset version was used makes it impossible to reproduce results or investigate data-quality incidents.

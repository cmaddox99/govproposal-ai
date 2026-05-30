---
laws: [ENG-6.1, ENG-6.4, ENG-6.7]
avatar: [sagemaker]
title: Security Laws — AWS SageMaker
---

# Security Laws: ENG-6.1, ENG-6.4, ENG-6.7 — AWS SageMaker

## ENG-6.1: Security by Design

SageMaker execution roles follow least privilege. Notebooks run in VPC-only mode. No credentials in notebook cells.

```python
# ✅ Credentials come from the IAM role attached to the SageMaker instance
import boto3, sagemaker

role   = sagemaker.get_execution_role()    # resolves attached IAM role — no keys needed
sess   = sagemaker.Session()

# ❌ NEVER in a notebook cell
# boto3.client("s3", aws_access_key_id="AKIA...", aws_secret_access_key="...")
```

IAM policy for SageMaker execution role — least privilege:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject", "s3:ListBucket"],
      "Resource": [
        "arn:aws:s3:::aa-ml-training-data/*",
        "arn:aws:s3:::aa-ml-artifacts/*"
      ]
      // ❌ NEVER: "Resource": "*"   or   "Action": "s3:*"
    }
  ]
}
```

VPC-only notebook instance configuration:

```python
import boto3

sm = boto3.client("sagemaker")
sm.create_notebook_instance(
    NotebookInstanceName="demand-forecast-nb",
    InstanceType="ml.t3.medium",
    RoleArn=role_arn,
    SubnetId="subnet-0abc1234",                     # private subnet
    SecurityGroupIds=["sg-0abc5678"],
    DirectInternetAccess="Disabled",                # ✅ VPC only — no public internet
    KmsKeyId=os.environ["NOTEBOOK_KMS_KEY_ARN"],    # encrypt EBS volume
)
```

SageMaker endpoints behind API Gateway with auth:

```python
# Deploy endpoint — no public access without API Gateway auth
predictor = model.deploy(
    instance_type="ml.m5.xlarge",
    initial_instance_count=1,
    data_capture_config=DataCaptureConfig(
        enable_capture=True,
        sampling_percentage=100,
        destination_s3_uri=f"s3://{S3_BUCKET}/data-capture/",
    ),
)
```

## ENG-6.4: Data Protection

Training data in S3 with SSE-KMS. No PII in experiment tags or parameter names. Log dataset path and schema hash — not raw data rows.

```python
from sagemaker.inputs import TrainingInput
import hashlib, boto3

# ✅ SSE-KMS on training data bucket (enforce via S3 bucket policy)
training_input = TrainingInput(
    s3_data=f"s3://aa-ml-training-data/demand/v3/",
    content_type="text/csv",
    s3_data_type="S3Prefix",
)

# ✅ Log dataset path + row count + schema hash — not row values
def safe_dataset_metadata(s3_uri: str, schema: list[str]) -> dict:
    return {
        "dataset_s3_uri":  s3_uri,
        "schema_hash":     hashlib.sha256(",".join(sorted(schema)).encode()).hexdigest()[:12],
        # ❌ NEVER: "sample_row": df.iloc[0].to_dict()  — may contain PII
    }
```

MLflow/SageMaker Experiments — no PII in tags:

```python
import mlflow

with mlflow.start_run(run_name="demand-v3") as run:
    mlflow.set_tags({
        "dataset.version": "v3",
        "dataset.hash":    dataset_hash,
        "iam.role":        role_arn,
        # ❌ NEVER: "passenger.sample": "J. Doe / PNR ABC123"
    })
```

## ENG-6.7: Audit Trail

Every training job logged with IAM role, dataset URI, code commit, and metrics. Model deployments logged with approver and timestamp.

```python
import mlflow, os, datetime

def log_training_job(dataset_s3_uri: str, hyperparameters: dict,
                     metrics: dict, sm_job_name: str) -> str:
    with mlflow.start_run(run_name=sm_job_name) as run:
        mlflow.log_params({
            "sagemaker_job_name":  sm_job_name,
            "dataset_s3_uri":      dataset_s3_uri,
            "code_commit_sha":     os.environ.get("GIT_COMMIT_SHA", "unknown"),
            "iam_role":            sagemaker.get_execution_role(),
            **hyperparameters,
        })
        mlflow.log_metrics(metrics)
        # ❌ NEVER delete: mlflow.delete_run(run.info.run_id)
        return run.info.run_id

# Log deployment event — append-only
async def log_deployment(run_id: str, endpoint_name: str,
                          model_version: str, approver_id: str) -> None:
    await db.execute(
        "INSERT INTO sagemaker_deployment_audit "
        "(run_id, endpoint_name, model_version, deployed_by, approved_by, deployed_at) "
        "VALUES (:r, :e, :mv, :by, :ap, :ts)",
        {"r": run_id, "e": endpoint_name, "mv": model_version,
         "by": os.environ.get("DEPLOYER_ID"), "ap": approver_id,
         "ts": datetime.datetime.utcnow()},
    )
```

SageMaker Pipeline execution history is immutable by design — preserve it:

```python
# ❌ NEVER delete pipeline execution history
# sm.delete_pipeline_execution(PipelineExecutionArn=arn)

# ✅ Query execution history for audit
response = sm.list_pipeline_executions(
    PipelineName="demand-forecast-pipeline",
    SortBy="CreationTime",
    SortOrder="Descending",
)
```

## Anti-Patterns

1. **IAM role with `s3:*` on all buckets** — overly broad permissions mean a compromised training job can read or overwrite any S3 bucket in the account, including production data.
2. **AWS credentials in notebook cells** — `aws_access_key_id="AKIA..."` in a cell is committed to `.ipynb` JSON and visible in Git history; use IAM role attached to the instance.
3. **PII in SageMaker experiment tags** — tags are stored in plaintext in the AWS console and accessible to anyone with `sagemaker:DescribeExperiment` permission.
4. **Training on non-encrypted S3 data** — omitting SSE-KMS on the training data bucket means passenger demand data is stored in plaintext; enforce encryption via bucket policy requiring `aws:kms`.
5. **No VPC config for notebook instance** — `DirectInternetAccess: Enabled` allows the notebook to exfiltrate data or credentials via the public internet; always use VPC-only mode.

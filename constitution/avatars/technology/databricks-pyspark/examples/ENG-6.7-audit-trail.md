---
law_id: ENG-6.7
avatar: databricks-pyspark
---

# ENG-6.7: Audit Trail Examples for Databricks / PySpark

---

## COMPLIANT

### 1. Append-only Delta audit log table with full lineage schema

The audit log captures every offer decision with enough information to reconstruct who received what, which model made the decision, and what run produced it.

```sql
CREATE TABLE main.marketing.offer_audit_log (
  customer_id_hash  STRING    NOT NULL COMMENT 'SHA-256 hash of AA customer ID — no raw PII',
  offer_id          STRING    NOT NULL COMMENT 'Offer catalogue identifier (e.g., offer-2024-plat-upgrade)',
  model_version     STRING             COMMENT 'Unity Catalog model version used for scoring',
  mlflow_run_id     STRING             COMMENT 'MLflow run that produced this score — links to full params/metrics',
  score             DOUBLE             COMMENT 'Raw propensity score [0.0, 1.0]',
  channel           STRING             COMMENT 'Delivery channel: EMAIL | PUSH | SMS | WEB',
  created_at        TIMESTAMP NOT NULL COMMENT 'UTC timestamp of the offer decision'
)
USING DELTA
PARTITIONED BY (DATE(created_at))
TBLPROPERTIES (
  'delta.enableChangeDataFeed'       = 'true',
  'delta.logRetentionDuration'       = 'interval 7 years',
  'delta.deletedFileRetentionDuration' = 'interval 7 years',
  'pipelines.autoOptimize.managed'   = 'true'
);

-- No UPDATE or DELETE granted on this table — append-only by access control
GRANT INSERT ON TABLE main.marketing.offer_audit_log
  TO `topml-scoring-sp@aa.com`;
-- Revoke all non-SELECT grants from all other principals
```

---

### 2. Delta transaction log as immutable lineage record

Delta's transaction log records every write operation, making the history of the audit table tamper-evident without additional infrastructure:

```sql
-- View the full transaction history of the audit log table
DESCRIBE HISTORY main.marketing.offer_audit_log;

-- Inspect a specific version to see exactly what was written and by whom
DESCRIBE HISTORY main.marketing.offer_audit_log
  LIMIT 1 OFFSET 0;

-- Time-travel query: read audit log as of a specific date
SELECT *
FROM main.marketing.offer_audit_log
TIMESTAMP AS OF '2024-06-01T00:00:00Z'
WHERE offer_id = 'offer-2024-plat-upgrade';
```

Delta's transaction log (`_delta_log/`) is immutable — each JSON commit file is append-only and content-addressed. An attacker cannot silently overwrite or delete past records.

---

### 3. MLflow run ID linking each prediction to its model version

Every offer decision written to the audit log includes the `mlflow_run_id` that produced the score. This links each individual decision back to the exact model version, hyperparameters, and training metrics.

```python
# src/topml/audit/offer_audit.py
from datetime import datetime, timezone
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType


AUDIT_LOG_TABLE = "main.marketing.offer_audit_log"

AUDIT_SCHEMA = StructType([
    StructField("customer_id_hash", StringType(), nullable=False),
    StructField("offer_id",         StringType(), nullable=False),
    StructField("model_version",    StringType(), nullable=True),
    StructField("mlflow_run_id",    StringType(), nullable=True),
    StructField("score",            DoubleType(), nullable=True),
    StructField("channel",          StringType(), nullable=True),
    StructField("created_at",       TimestampType(), nullable=False),
])


def write_offer_audit_records(
    spark: SparkSession,
    scored_decisions: DataFrame,
    mlflow_run_id: str,
    model_version: str,
) -> None:
    """Append offer decisions to the immutable audit log.

    Each row links a customer decision to the exact MLflow run and model version
    that produced it, satisfying ENG-6.7 and BUS-7.1 traceability requirements.
    """
    audit_df = (
        scored_decisions
        .withColumn("mlflow_run_id",  F.lit(mlflow_run_id))
        .withColumn("model_version",  F.lit(model_version))
        .withColumn("created_at",     F.current_timestamp())
        .select(
            "customer_id_hash",
            "offer_id",
            "model_version",
            "mlflow_run_id",
            "score",
            "channel",
            "created_at",
        )
    )

    (
        audit_df.write
        .format("delta")
        .mode("append")
        .option("mergeSchema", "false")
        .saveAsTable(AUDIT_LOG_TABLE)
    )
```

Calling code passes `run.info.run_id` from the active MLflow context:

```python
import mlflow

with mlflow.start_run() as run:
    scores_df = score_customers(customers_df, model)
    mlflow.log_metric("customers_scored", scores_df.count())

    write_offer_audit_records(
        spark=spark,
        scored_decisions=scores_df,
        mlflow_run_id=run.info.run_id,
        model_version=champion_version,
    )
```

---

## VIOLATION

### Overwriting the Delta table — no history retained

```python
# VIOLATION — overwrites audit table; all prior records are gone
(
    new_decisions_df.write
    .format("delta")
    .mode("overwrite")   # destroys audit history
    .saveAsTable("main.marketing.offer_audit_log")
)
```

### Logging offer decisions to driver stdout only

```python
# VIOLATION — stdout is not durable; logs disappear when the cluster terminates
for row in decisions_df.collect():
    print(f"Offered {row['offer_id']} to {row['customer_id_hash']}")
# No queryable record, no retention, no linkage to model version
```

### No model version recorded with predictions

```python
# VIOLATION — audit record exists but cannot be traced back to a model
(
    decisions_df
    .select("customer_id_hash", "offer_id", "score", "channel")
    .write.format("delta").mode("append")
    .saveAsTable("main.marketing.offer_audit_log")
)
# If the model produces bad scores, there is no way to identify which version
# was responsible or replay decisions under the correct model
```

All three patterns violate ENG-6.7. Audit records must be append-only, durable, and linked to the model artefact that produced them.

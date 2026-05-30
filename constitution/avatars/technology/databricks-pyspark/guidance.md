# Databricks / PySpark / Delta Lake Guidance

> **Purpose:** Stack-specific agent behaviors and patterns for Databricks, PySpark, and Delta Lake pipelines in the AA TopML (Top Marketing Layer) platform.

---

## Overview

This guidance covers how AI agents should write, test, and deploy PySpark pipelines on Databricks for the American Airlines marketing and offer-scoring platform (TopML). It covers Delta Lake conventions, MLflow experiment tracking, Unity Catalog access patterns, Databricks Asset Bundle deployment, and secret management.

---

## Workspace Structure

Databricks environments are managed via **Databricks Asset Bundles (DAB)** with three target environments defined in `databricks.yml`:

```yaml
# databricks.yml
bundle:
  name: topml-offer-scoring

targets:
  dev:
    mode: development
    workspace:
      host: https://adb-dev.azuredatabricks.net
  stage:
    workspace:
      host: https://adb-stage.azuredatabricks.net
  prod:
    workspace:
      host: https://adb-prod.azuredatabricks.net
    run_as:
      service_principal_name: topml-scoring-sp@aa.com
```

- **dev** → personal workspace; `mode: development` prefixes all resources with the developer's username automatically.
- **stage** → integration environment; CI deploys here on every merge to `main`.
- **prod** → production; requires manual approval gate in CI.

---

## Delta Lake Table Conventions

### Naming

All tables use the `catalog.schema.table` three-part Unity Catalog naming:

```
main.marketing.customer_segments
main.marketing.offer_decisions
main.marketing.offer_audit_log
main.feature_store.customer_features_daily
```

- Schema names: `snake_case`, prefixed by domain (e.g., `marketing`, `feature_store`).
- Table names: `snake_case`, descriptive noun phrases.

### Partitioning & ZORDER

```sql
-- Partition large fact tables by date; ZORDER on high-cardinality lookup keys
CREATE TABLE main.marketing.offer_decisions (
  decision_date DATE NOT NULL,
  customer_id_hash STRING NOT NULL,
  offer_id STRING NOT NULL,
  channel STRING NOT NULL,
  score DOUBLE,
  mlflow_run_id STRING,
  model_version STRING,
  created_at TIMESTAMP NOT NULL
)
USING DELTA
PARTITIONED BY (decision_date)
TBLPROPERTIES (
  'delta.enableChangeDataFeed' = 'true',
  'delta.logRetentionDuration' = 'interval 7 years',
  'delta.dataSkippingNumIndexedCols' = '4'
);

-- After initial load, ZORDER on most-queried non-partition keys
OPTIMIZE main.marketing.offer_decisions
ZORDER BY (customer_id_hash, offer_id);
```

### Reading and Writing

Always use `spark.table()` for Unity Catalog tables — never construct JDBC URLs manually:

```python
from pyspark.sql import DataFrame, SparkSession

def read_customer_segments(spark: SparkSession) -> DataFrame:
    return spark.table("main.marketing.customer_segments")

def write_offer_decisions(df: DataFrame, mode: str = "append") -> None:
    (
        df.write
        .format("delta")
        .mode(mode)
        .option("mergeSchema", "false")
        .saveAsTable("main.marketing.offer_decisions")
    )
```

---

## PySpark Transformation Patterns

### Pure Functions

Every transformation must be a **pure function**: accepts a `DataFrame`, returns a `DataFrame`, with no side effects (no reads, writes, or external calls inside the function body).

```python
# src/topml/transformations/offer_filter.py
from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def apply_customer_offer_filter(
    customers: DataFrame,
    offer_tier: str,
    opt_out_flag: str = "Y",
) -> DataFrame:
    """Filter customers eligible for an offer by tier and opt-out status."""
    return (
        customers
        .filter(F.col("loyalty_tier") == offer_tier)
        .filter(F.col("marketing_opt_out") != opt_out_flag)
        .filter(F.col("account_status") == "ACTIVE")
    )
```

### Immutable DataFrame Chains

Never mutate a `DataFrame` variable. Assign each transformation step to a new name or chain directly:

```python
# GOOD — chained pure functions, each step is named
eligible = apply_customer_offer_filter(customers, offer_tier="PLATINUM")
scored   = apply_propensity_score(eligible, scores_df)
ranked   = rank_offers(scored, top_n=3)

# BAD — reassigning the same variable, obscures lineage
df = customers
df = df.filter(...)
df = df.join(...)
```

### Schema Enforcement

Declare expected schemas as constants and validate on read:

```python
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType

CUSTOMER_SEGMENT_SCHEMA = StructType([
    StructField("customer_id_hash", StringType(), nullable=False),
    StructField("loyalty_tier", StringType(), nullable=False),
    StructField("marketing_opt_out", StringType(), nullable=False),
    StructField("account_status", StringType(), nullable=False),
])
```

---

## MLflow Experiment Tracking

### Experiment Naming Convention

```
/Users/<service-principal-email>/topml/<pipeline_name>
# e.g.
/Users/topml-scoring-sp@aa.com/topml/offer_propensity_scoring
```

### Logging Pattern

```python
import mlflow
from mlflow.models import infer_signature

def train_propensity_model(
    train_df: DataFrame,
    params: dict,
    experiment_path: str,
) -> str:
    mlflow.set_experiment(experiment_path)

    with mlflow.start_run() as run:
        mlflow.log_params(params)

        model = _fit_model(train_df, params)
        metrics = _evaluate_model(model, train_df)
        mlflow.log_metrics(metrics)

        signature = infer_signature(
            train_df.toPandas(),
            model.predict(train_df.toPandas()),
        )
        mlflow.sklearn.log_model(
            model,
            artifact_path="propensity_model",
            signature=signature,
            registered_model_name="main.marketing.propensity_model",
        )

        return run.info.run_id
```

### Unity Catalog Model Registry

Register all models in Unity Catalog (three-part name):

```python
client = mlflow.tracking.MlflowClient()
client.set_registered_model_alias(
    name="main.marketing.propensity_model",
    alias="champion",
    version=latest_version,
)
```

---

## Unity Catalog Access Patterns

### Least-Privilege Grants

```sql
-- Grant only SELECT on specific tables to the scoring service principal
GRANT SELECT ON TABLE main.marketing.customer_segments
  TO `topml-scoring-sp@aa.com`;

GRANT SELECT ON TABLE main.feature_store.customer_features_daily
  TO `topml-scoring-sp@aa.com`;

-- Write access only to output tables
GRANT INSERT ON TABLE main.marketing.offer_decisions
  TO `topml-scoring-sp@aa.com`;
```

### Column Masking (PII)

```sql
CREATE FUNCTION main.marketing.mask_customer_id(customer_id STRING)
  RETURNS STRING
  RETURN CASE
    WHEN is_account_group_member('topml_pii_viewers') THEN customer_id
    ELSE sha2(customer_id, 256)
  END;

ALTER TABLE main.marketing.offer_decisions
  ALTER COLUMN customer_id_hash
  SET MASK main.marketing.mask_customer_id;
```

### Row Filters

```sql
CREATE FUNCTION main.marketing.filter_by_channel(channel STRING)
  RETURNS BOOLEAN
  RETURN is_account_group_member('topml_all_channels')
      OR current_user() LIKE CONCAT('%-', channel, '@aa.com');

ALTER TABLE main.marketing.offer_decisions
  SET ROW FILTER main.marketing.filter_by_channel ON (channel);
```

---

## Secret Management

**All credentials must come from Databricks Secrets.** Never use `.env` files in notebooks, never hardcode tokens, never use notebook widgets for secrets.

```python
# CORRECT — always use dbutils.secrets.get()
def get_jdbc_connection_string(dbutils) -> str:
    return dbutils.secrets.get(scope="topml-kv", key="jdbc-connection-string")

def get_sendgrid_api_key(dbutils) -> str:
    return dbutils.secrets.get(scope="topml-kv", key="sendgrid-api-key")
```

Secret scopes follow the environment pattern:
- `topml-kv-dev` → dev secrets
- `topml-kv-stage` → stage secrets
- `topml-kv-prod` → prod secrets

The target-specific scope name should be passed in via a DAB job parameter, not hardcoded.

---

## Testing Strategy

### SparkSession Fixture (conftest.py)

```python
# tests/conftest.py
import pytest
from delta import configure_spark_with_delta_pip
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def spark() -> SparkSession:
    builder = (
        SparkSession.builder
        .master("local[2]")
        .appName("topml-tests")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config(
            "spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        )
        .config("spark.sql.shuffle.partitions", "4")
    )
    return configure_spark_with_delta_pip(builder).getOrCreate()
```

### Delta Table Fixtures

Use `tmp_path` (pytest built-in) for ephemeral Delta tables — never write to production paths in tests:

```python
# tests/conftest.py (continued)
import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType


@pytest.fixture()
def customer_segments_table(spark: SparkSession, tmp_path):
    path = str(tmp_path / "customer_segments")
    schema = StructType([
        StructField("customer_id_hash", StringType(), False),
        StructField("loyalty_tier", StringType(), False),
        StructField("marketing_opt_out", StringType(), False),
        StructField("account_status", StringType(), False),
    ])
    df = spark.createDataFrame([], schema)
    df.write.format("delta").save(path)
    return spark.read.format("delta").load(path), path
```

### Test Naming

```
tests/
  test_offer_filter.py          # unit: pure transformation functions
  test_feature_eng.py           # unit: feature engineering functions
  test_scoring_pipeline.py      # integration: full pipeline with Delta fixtures
```

---

## Databricks Asset Bundle Deployment

```
# Validate bundle syntax
databricks bundle validate

# Deploy to stage (CI does this on merge to main)
databricks bundle deploy --target stage

# Run a job on stage to smoke-test
databricks bundle run topml_offer_scoring_daily --target stage

# Deploy to prod (requires manual approval in CI)
databricks bundle deploy --target prod
```

The `databricks.yml` defines all cluster configs, job schedules, and library dependencies. No manual cluster configuration through the Databricks UI.

---

## CI/CD Pipeline

See `examples/ENG-5.1-cicd.md` for the full GitHub Actions workflow. Key stages:

1. **validate** — `databricks bundle validate`
2. **test** — `pytest tests/ --cov=src`
3. **deploy-stage** — `databricks bundle deploy --target stage`
4. **smoke-test** — trigger the DAB job via REST API and poll for completion
5. **approve** — manual gate (GitHub Environment protection rule)
6. **deploy-prod** — `databricks bundle deploy --target prod`

---

## Notebooks

Notebooks in `notebooks/` are **orchestration only**. They call functions from `src/topml/` and contain no business logic themselves:

```python
# notebooks/run_scoring_pipeline.py
# Databricks notebook source

# COMMAND ----------
# %pip install -e /Workspace/Repos/topml-offer-scoring

# COMMAND ----------
from topml.pipelines.scoring_pipeline import run_offer_scoring_pipeline

run_offer_scoring_pipeline(
    spark=spark,
    dbutils=dbutils,
    target_date=dbutils.widgets.get("target_date"),
)
```

Logic tested in `tests/` against `src/topml/` — notebooks themselves are not unit-tested.

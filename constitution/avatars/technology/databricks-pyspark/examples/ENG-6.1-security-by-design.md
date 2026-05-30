---
law_id: ENG-6.1
avatar: databricks-pyspark
---

# ENG-6.1: Security by Design Examples for Databricks / PySpark

---

## COMPLIANT

### 1. All credentials retrieved from Databricks Secrets

Never read credentials from environment variables, `.env` files, notebook widgets, or any file stored in the repo. Use `dbutils.secrets.get()` exclusively.

```python
# src/topml/pipelines/scoring_pipeline.py
from pyspark.sql import SparkSession


def run_offer_scoring_pipeline(
    spark: SparkSession,
    dbutils,  # injected by Databricks runtime; mocked in tests
    target_date: str,
) -> None:
    jdbc_url = dbutils.secrets.get(scope="topml-kv-prod", key="jdbc-connection-string")
    sendgrid_key = dbutils.secrets.get(scope="topml-kv-prod", key="sendgrid-api-key")
    model_endpoint = dbutils.secrets.get(scope="topml-kv-prod", key="model-serving-endpoint")

    customers = _read_customers(spark, jdbc_url)
    scores = _call_model_endpoint(customers, model_endpoint)
    _deliver_offers(scores, sendgrid_key)
```

Secret scope names follow the environment pattern:
- `topml-kv-dev` — dev workspace secrets (non-sensitive test values only)
- `topml-kv-stage` — stage workspace secrets
- `topml-kv-prod` — prod workspace secrets (accessed only by the scoring service principal)

The correct scope name is injected as a DAB job parameter at deploy time — not hardcoded in source:

```yaml
# resources/jobs.yml
jobs:
  - name: topml_offer_scoring_daily
    parameters:
      - name: secret_scope
        default: topml-kv-prod
```

---

### 2. Least-privilege Unity Catalog grants

Grant the minimum permissions required for the scoring service principal to operate. Never use broad grants.

```sql
-- Grant SELECT only on the tables the scoring SP reads
GRANT SELECT ON TABLE main.marketing.customer_segments
  TO `topml-scoring-sp@aa.com`;

GRANT SELECT ON TABLE main.feature_store.customer_features_daily
  TO `topml-scoring-sp@aa.com`;

-- Grant INSERT only on the output table; no UPDATE or DELETE
GRANT INSERT ON TABLE main.marketing.offer_decisions
  TO `topml-scoring-sp@aa.com`;

-- Grant EXECUTE on the model serving endpoint
GRANT EXECUTE ON FUNCTION main.marketing.propensity_model
  TO `topml-scoring-sp@aa.com`;

-- Verify effective permissions before deploying
SHOW GRANTS ON TABLE main.marketing.customer_segments;
```

---

### 3. Service principal authentication via Azure AD managed identity

Cluster configuration uses managed identity — no client secret is stored in source code or cluster environment variables:

```yaml
# resources/jobs.yml  — cluster config for the scoring job
jobs:
  - name: topml_offer_scoring_daily
    job_clusters:
      - job_cluster_key: scoring_cluster
        new_cluster:
          spark_version: "15.4.x-scala2.12"
          node_type_id: Standard_DS3_v2
          num_workers: 4
          azure_attributes:
            # Managed identity attached to the cluster — no client secret
            msi_resource_id: /subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.ManagedIdentity/userAssignedIdentities/topml-scoring-mi
```

The service principal is configured once at the Azure AD level; Databricks inherits the identity automatically.

---

### 4. Workspace isolation per environment

Each environment is a **separate** Databricks workspace with its own secrets scope and Unity Catalog metastore. Cross-workspace access is not permitted.

```yaml
# databricks.yml
targets:
  dev:
    workspace:
      host: https://adb-dev.azuredatabricks.net    # dev metastore, dev secrets
  stage:
    workspace:
      host: https://adb-stage.azuredatabricks.net  # stage metastore, stage secrets
  prod:
    workspace:
      host: https://adb-prod.azuredatabricks.net   # prod metastore, prod secrets
```

Production credentials **never** exist in dev or stage workspaces. CI uses workspace-scoped service principals with tokens stored in GitHub Secrets, rotated quarterly.

---

## VIOLATION

### 1. Hardcoded connection string in a notebook cell

```python
# VIOLATION — notebook cell
jdbc_url = "jdbc:sqlserver://EXAMPLE-SERVER:1433;database=marketing;user=sa;password=EXAMPLE-PASSWORD"
df = spark.read.format("jdbc").option("url", jdbc_url).load()
# ❌ Credential is hardcoded — visible in notebook revision history, Git history, and Databricks audit logs
```

### 2. Overly broad Unity Catalog grant

```sql
-- VIOLATION — grants all privileges on the entire schema to all users
GRANT ALL PRIVILEGES ON SCHEMA main.marketing TO GROUP all_users;
-- Any Databricks user can now read, write, or delete any marketing table
```

### 3. Client secret stored in a notebook widget

```python
# VIOLATION — notebook cell
dbutils.widgets.text("client_secret", "")
client_secret = dbutils.widgets.get("client_secret")
# Widget value appears in notebook state, is loggable, and requires a human to paste the secret at runtime
```

These patterns violate ENG-6.1 because they expose credentials in version control, audit logs, or human-readable surfaces. Use `dbutils.secrets.get()` and managed identity in all cases.

# Azure Data Factory Avatar Guidance

This guidance specializes the AA Hangar AI Constitution laws for Azure Data Factory pipelines
on the topml platform. Follow all naming conventions and security patterns defined in
`manifest.yaml`.

---

## 1. Pipeline Naming Conventions

Every pipeline name **must** follow the pattern: `pl_{env}_{campaign_or_domain}_{frequency}`

The environment prefix is **mandatory** — a pipeline without it cannot be deployed via the
automated promotion workflow and will be rejected in code review.

### topml Platform Examples

| Pipeline Name | Purpose |
|---------------|---------|
| `pl_dev_anp_daily` | Dev: American Now Plus daily batch |
| `pl_stage_anp_daily` | Stage: American Now Plus daily batch |
| `pl_prod_anp_daily` | Prod: American Now Plus daily batch |
| `pl_stage_model_retrain` | Stage: model retraining pipeline |
| `pl_prod_offer_delivery_hourly` | Prod: hourly offer delivery |
| `pl_stage_customer_segment_refresh` | Stage: daily customer segment rebuild |
| `pl_prod_anp_historical_backfill` | Prod: historical backfill (TumblingWindow) |

### Why Environment Prefix is Mandatory

ADF Git integration stores all pipelines in the same repository branch. Without environment
encoding in the name, it is impossible to distinguish which resources belong to which
environment during ARM template deployment, log queries, and incident response.

### Anti-Pattern

```
# WRONG — no environment context, ambiguous in shared ADF instance
pl_campaign_daily
pipeline_model_retrain
anp_offer_pipeline
```

---

## 2. Linked Service Patterns

### Preferred: Managed Identity (No Credentials Block)

Managed Identity authentication eliminates secrets entirely. The ADF managed identity is
granted the minimum necessary RBAC role on the target resource.

**ADF JSON — Databricks Linked Service with MSI**

```json
{
  "name": "ls_databricks_prod",
  "type": "Microsoft.DataFactory/factories/linkedservices",
  "properties": {
    "type": "AzureDatabricks",
    "typeProperties": {
      "domain": {
        "value": "@{linkedService().databricksWorkspaceUrl}",
        "type": "Expression"
      },
      "authentication": "MSI",
      "workspaceResourceId": {
        "value": "@{linkedService().workspaceResourceId}",
        "type": "Expression"
      },
      "newClusterNodeType": "Standard_DS3_v2",
      "newClusterNumOfWorker": "2:8",
      "newClusterSparkConf": {
        "spark.databricks.delta.preview.enabled": "true"
      }
    },
    "parameters": {
      "databricksWorkspaceUrl": { "type": "String" },
      "workspaceResourceId":    { "type": "String" }
    }
  }
}
```

There is **no** `credential`, `accessToken`, or `password` field. ADF authenticates using
the factory's system-assigned managed identity.

**RBAC assignment required on the Databricks workspace:**

```bash
az role assignment create \
  --assignee <adf-managed-identity-object-id> \
  --role "Contributor" \
  --scope /subscriptions/<sub-id>/resourceGroups/topml-rg/providers/Microsoft.Databricks/workspaces/topml-dbx-prod
```

---

### When MSI Is Not Available: Key Vault Reference

For connection strings that require a secret (e.g., a JDBC connection string for a legacy
SQL Server), use an Azure Key Vault reference. The secret value is **never** stored in ADF
or in source code.

```json
{
  "name": "ls_sqlserver_prod",
  "properties": {
    "type": "SqlServer",
    "typeProperties": {
      "connectionString": {
        "type": "AzureKeyVaultSecret",
        "store": {
          "referenceName": "ls_keyvault_prod",
          "type": "LinkedServiceReference"
        },
        "secretName": "topml-sqlserver-jdbc-conn"
      }
    }
  }
}
```

Inline Key Vault reference syntax (in pipeline expressions):

```
@Microsoft.KeyVault(SecretUri=https://topml-kv.vault.azure.net/secrets/jdbc-conn/)
```

---

## 3. Trigger Types: When to Use Each

### Schedule Trigger — Daily / Weekly Batch

Use for fixed-time batch operations that do not need backfill support.

```json
{
  "name": "tr_pl_prod_anp_daily_0300",
  "properties": {
    "type": "ScheduleTrigger",
    "typeProperties": {
      "recurrence": {
        "frequency": "Day",
        "interval": 1,
        "startTime": "2025-01-01T03:00:00Z",
        "timeZone": "UTC"
      }
    },
    "pipelines": [
      {
        "pipelineReference": { "referenceName": "pl_prod_anp_daily", "type": "PipelineReference" },
        "parameters": { "runDate": "@trigger().scheduledTime" }
      }
    ]
  }
}
```

**Use for:** daily offer email generation (03:00 UTC), weekly model scoring, monthly reporting.

---

### TumblingWindow Trigger — Backfill-Capable Historical Processing

Use when you need exactly-once, ordered processing of time windows with full backfill support.
TumblingWindow triggers retry failed windows automatically and support dependency chaining.

```json
{
  "name": "tr_pl_prod_anp_historical_backfill_daily",
  "properties": {
    "type": "TumblingWindowTrigger",
    "typeProperties": {
      "frequency": "Hour",
      "interval": 24,
      "startTime": "2024-01-01T00:00:00Z",
      "endTime": "2025-12-31T00:00:00Z",
      "delay": "00:10:00",
      "maxConcurrency": 4,
      "retryPolicy": { "count": 3, "intervalInSeconds": 30 }
    },
    "pipeline": {
      "pipelineReference": {
        "referenceName": "pl_prod_anp_historical_backfill",
        "type": "PipelineReference"
      },
      "parameters": {
        "windowStart": "@trigger().outputs.windowStartTime",
        "windowEnd":   "@trigger().outputs.windowEndTime"
      }
    }
  }
}
```

**Use for:** reprocessing 12 months of ANP campaign data, model retraining on historical
segments, correcting data quality issues across a date range.

---

### Event-Based Trigger — File Arrival in ADLS

Use when processing should start immediately upon file arrival in Azure Data Lake Storage,
not on a schedule.

```json
{
  "name": "tr_pl_prod_customer_segment_on_file",
  "properties": {
    "type": "BlobEventsTrigger",
    "typeProperties": {
      "blobPathBeginsWith": "/topml-segments/blobs/inbound/customer_segments/",
      "blobPathEndsWith": ".parquet",
      "events": [ "Microsoft.Storage.BlobCreated" ],
      "scope": "/subscriptions/<sub-id>/resourceGroups/topml-rg/providers/Microsoft.Storage/storageAccounts/topmlprodsa"
    },
    "pipelines": [
      {
        "pipelineReference": {
          "referenceName": "pl_prod_customer_segment_refresh",
          "type": "PipelineReference"
        },
        "parameters": {
          "blobName": "@triggerBody().fileName",
          "blobPath": "@triggerBody().folderPath"
        }
      }
    ]
  }
}
```

**Use for:** processing a new customer segment file uploaded by the data science team,
triggering offer scoring when a model output file lands in ADLS.

---

## 4. Environment Promotion Workflow

Promotion follows a strict one-way path: **dev → stage → prod**, enforced by GitHub Actions.

```
feature branch → PR → main → deploy to stage (automated) → deploy to prod (manual approval)
```

### Parameter File Pattern

Each environment has its own parameter file. Only the parameter values differ — the ARM
template is identical across all environments.

```
adf/
├── adf-arm-template.json          # single source-of-truth ARM template (from ADF Git)
├── adf-parameters-dev.json
├── adf-parameters-stage.json
└── adf-parameters-prod.json
```

**adf-parameters-stage.json**

```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "factoryName": { "value": "topml-adf-stage" },
    "ls_adls_stage_accountKey": {
      "value": "@Microsoft.KeyVault(SecretUri=https://topml-kv.vault.azure.net/secrets/adls-stage-key/)"
    },
    "ls_databricks_stage_workspaceUrl": {
      "value": "https://adb-1234567890.12.azuredatabricks.net"
    },
    "ls_databricks_stage_workspaceResourceId": {
      "value": "/subscriptions/<sub-id>/resourceGroups/topml-rg/providers/Microsoft.Databricks/workspaces/topml-dbx-stage"
    }
  }
}
```

See `examples/ENG-5.1-cicd.md` for the full GitHub Actions workflow.

---

## 5. Parameterization

**Every** environment-specific value — storage account names, workspace URLs, Delta table
names, Key Vault URIs — must be a **pipeline parameter**. Hardcoded values cause silent
cross-environment contamination and make promotion unsafe.

### Pipeline JSON With Parameters Block

```json
{
  "name": "pl_stage_anp_daily",
  "properties": {
    "parameters": {
      "storageAccountName": { "type": "string", "defaultValue": "" },
      "deltaTablePath":     { "type": "string", "defaultValue": "" },
      "runDate":            { "type": "string", "defaultValue": "@utcNow('yyyy-MM-dd')" },
      "environment":        { "type": "string", "defaultValue": "stage" }
    },
    "activities": [
      {
        "name": "CopyCustomerSegments",
        "type": "Copy",
        "typeProperties": {
          "source": {
            "type": "ParquetSource",
            "storeSettings": {
              "type": "AzureBlobFSReadSettings",
              "recursive": false
            }
          },
          "sink": {
            "type": "DeltalakeSink",
            "storeSettings": {
              "type": "AzureBlobFSWriteSettings"
            }
          }
        },
        "inputs": [
          {
            "referenceName": "ds_adls_customer_segments",
            "type": "DatasetReference",
            "parameters": {
              "storageAccountName": { "value": "@pipeline().parameters.storageAccountName", "type": "Expression" },
              "folderPath": { "value": "@concat('segments/', pipeline().parameters.runDate)", "type": "Expression" }
            }
          }
        ]
      }
    ]
  }
}
```

**Rule:** `defaultValue` for environment-specific parameters must be `""` (empty string).
This forces the trigger or deployment to supply the correct value rather than silently using
a dev value in production.

---

## 6. Never Use ADF Studio Publish

The **Publish** button in ADF Studio bypasses Git entirely. Clicking it:

1. Writes directly to the `adf_publish` branch, skipping all pull request review
2. Deploys changes to the live ADF instance without any CI validation
3. Creates a divergence between the Git-tracked state and the deployed state that is extremely
   difficult to reconcile
4. Leaves no GitHub Actions audit trail of what was deployed, when, and by whom

### Enforcement

- ADF Git integration is configured with **collaboration branch = `main`**
- The ADF managed identity used by the GitHub Actions deployer is the **only** identity with
  `Data Factory Contributor` role on the prod factory
- Developer identities have `Data Factory Contributor` on dev only — they cannot publish to
  stage or prod even if they click the button

### Allowed Workflow

```
# Development
git checkout -b feature/add-offer-delivery-pipeline
# ... edit pipeline JSON in VS Code with ADF extension ...
git commit -m "feat: add pl_dev_offer_delivery_hourly pipeline"
git push origin feature/add-offer-delivery-pipeline
# Open PR → code review → merge to main → GitHub Actions deploys to stage automatically
```

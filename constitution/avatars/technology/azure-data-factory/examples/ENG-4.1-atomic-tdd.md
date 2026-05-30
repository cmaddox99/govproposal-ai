---
law_id: ENG-4.1
avatar: azure-data-factory
---

# ENG-4.1 Atomic TDD — Azure Data Factory

Atomic TDD in ADF means testing **one activity** in **one isolated pipeline** before
composing it into a larger orchestration. Use ADF debug runs to validate each activity in
isolation, and the ADF REST API or `az cli` to validate schema and configuration before
promotion.

---

## COMPLIANT

### Step 1 — Create an Isolated Test Pipeline for a Single Copy Activity

Rather than building a full 20-activity orchestration pipeline upfront, create a minimal
test pipeline containing **only** the Copy Activity under test.

**`pl_stage_test_copy_customer_segments.json`**

```json
{
  "name": "pl_stage_test_copy_customer_segments",
  "properties": {
    "description": "Isolated test pipeline — validates single Copy Activity in isolation before use in pl_stage_anp_daily",
    "parameters": {
      "storageAccountName": { "type": "string" },
      "sourceContainer":    { "type": "string" },
      "sourceFolderPath":   { "type": "string" },
      "sinkTablePath":      { "type": "string" },
      "runDate":            { "type": "string" }
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
              "recursive": false,
              "enablePartitionDiscovery": false
            }
          },
          "sink": {
            "type": "DeltalakeSink",
            "preCopyScript": "TRUNCATE TABLE stage_customer_segments"
          },
          "enableStaging": false,
          "validateDataConsistency": true
        },
        "inputs":  [{ "referenceName": "ds_adls_customer_segments", "type": "DatasetReference" }],
        "outputs": [{ "referenceName": "ds_delta_stage_customer_segments", "type": "DatasetReference" }]
      }
    ]
  }
}
```

---

### Step 2 — Run via ADF Debug and Validate Output

```bash
# Trigger a debug run of the isolated test pipeline
az datafactory pipeline create-run \
  --factory-name topml-adf-stage \
  --resource-group topml-rg \
  --name pl_stage_test_copy_customer_segments \
  --parameters '{
    "storageAccountName": "topmlstagesa",
    "sourceContainer":    "topml-segments",
    "sourceFolderPath":   "inbound/customer_segments/2025-01-15",
    "sinkTablePath":      "/delta/stage/customer_segments",
    "runDate":            "2025-01-15"
  }'
```

```bash
# Poll for completion and check the activity run result
RUN_ID=$(az datafactory pipeline create-run ... --query runId -o tsv)

az datafactory pipeline-run show \
  --factory-name topml-adf-stage \
  --resource-group topml-rg \
  --run-id "$RUN_ID" \
  --query "{status: status, rowsCopied: output.rowsCopied, errors: output.errors}"
```

Expected output (passing):

```json
{
  "status": "Succeeded",
  "rowsCopied": 142837,
  "errors": []
}
```

---

### Step 3 — Validate Output Schema via REST API

Before composing into the parent pipeline, validate the sink schema matches expectations:

```bash
# Validate the ARM/ADF resource schema (catches JSON structure errors before deployment)
az deployment group validate \
  --resource-group topml-rg \
  --template-file adf-arm-template.json \
  --parameters @adf-parameters-stage.json

# If using ADF REST API — validate pipeline definition
az datafactory pipeline create \
  --validate \
  --factory-name topml-adf-stage \
  --resource-group topml-rg \
  --name pl_stage_test_copy_customer_segments \
  --pipeline @pl_stage_test_copy_customer_segments.json
```

A passing `--validate` run confirms:
- All linked service references resolve
- All dataset schema definitions are consistent with the activity's expected input/output
- Parameter references are type-safe

---

### Step 4 — Compose Into Parent Pipeline Only After Isolated Test Passes

Once `pl_stage_test_copy_customer_segments` succeeds in isolation, add the Copy Activity
as a single node in `pl_stage_anp_daily`:

```json
{
  "name": "pl_stage_anp_daily",
  "properties": {
    "activities": [
      {
        "name": "CopyCustomerSegments",
        "type": "ExecutePipeline",
        "typeProperties": {
          "pipeline": {
            "referenceName": "pl_stage_test_copy_customer_segments",
            "type": "PipelineReference"
          },
          "waitOnCompletion": true,
          "parameters": {
            "storageAccountName": "@pipeline().parameters.storageAccountName",
            "runDate":            "@pipeline().parameters.runDate"
          }
        },
        "dependsOn": []
      }
    ]
  }
}
```

Each activity is validated independently before being wired into the orchestration pipeline.

---

## VIOLATION

### Anti-Pattern: 20-Activity Orchestration Pipeline as the First and Only Test

```json
{
  "name": "pl_prod_anp_full_pipeline",
  "properties": {
    "activities": [
      { "name": "LoadCustomerSegments",    "type": "Copy",           "dependsOn": [] },
      { "name": "EnrichWithLoyaltyData",   "type": "DatabricksNotebook", "dependsOn": [{"activity": "LoadCustomerSegments"}] },
      { "name": "RunScoringModel",         "type": "DatabricksNotebook", "dependsOn": [{"activity": "EnrichWithLoyaltyData"}] },
      { "name": "FilterEligibleMembers",   "type": "DataFlow",       "dependsOn": [{"activity": "RunScoringModel"}] },
      { "name": "GenerateOfferPayloads",   "type": "DatabricksNotebook", "dependsOn": [{"activity": "FilterEligibleMembers"}] },
      { "name": "WriteToOfferQueue",       "type": "Copy",           "dependsOn": [{"activity": "GenerateOfferPayloads"}] },
      { "name": "TriggerEmailDelivery",    "type": "WebActivity",    "dependsOn": [{"activity": "WriteToOfferQueue"}] }
    ]
  }
}
```

**Deployed directly to production as the first run. No debug runs. No schema validation.**

**Why this violates ENG-4.1:**
- A failure at activity 4 (`FilterEligibleMembers`) leaves no indication of whether activities
  1–3 are correct — the entire run must be retried
- No isolated validation means a JSON schema error in a dataset definition is only caught
  after 40 minutes of Databricks cluster startup time
- If the pipeline runs in production and fails at `WriteToOfferQueue`, partial data may have
  been written to Delta tables with no rollback mechanism
- Zero schema validation steps — linked service misconfigurations are discovered in production

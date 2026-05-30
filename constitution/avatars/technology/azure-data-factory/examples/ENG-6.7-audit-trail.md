---
law_id: ENG-6.7
avatar: azure-data-factory
---

# ENG-6.7 Audit Trail Law — Azure Data Factory

Every ADF pipeline run must produce a durable, queryable audit record. ADF Monitor UI alone
is insufficient — logs must be exported to Log Analytics with a minimum 90-day retention
policy. Structured activity outputs must capture row counts and run metadata.

---

## COMPLIANT

### 1. Diagnostic Settings — Pipeline Run Logs Sent to Log Analytics

**ARM Template / ADF Diagnostic Settings JSON**

```json
{
  "type": "Microsoft.DataFactory/factories/providers/diagnosticSettings",
  "name": "topml-adf-prod/Microsoft.Insights/topml-adf-diag",
  "properties": {
    "workspaceId": "/subscriptions/<sub-id>/resourceGroups/topml-rg/providers/Microsoft.OperationalInsights/workspaces/topml-law-prod",
    "logs": [
      {
        "category": "PipelineRuns",
        "enabled": true,
        "retentionPolicy": { "enabled": true, "days": 90 }
      },
      {
        "category": "ActivityRuns",
        "enabled": true,
        "retentionPolicy": { "enabled": true, "days": 90 }
      },
      {
        "category": "TriggerRuns",
        "enabled": true,
        "retentionPolicy": { "enabled": true, "days": 90 }
      }
    ],
    "metrics": [
      {
        "category": "AllMetrics",
        "enabled": true,
        "retentionPolicy": { "enabled": true, "days": 90 }
      }
    ]
  }
}
```

**Enable via az CLI:**

```bash
az monitor diagnostic-settings create \
  --name topml-adf-diag \
  --resource "/subscriptions/<sub-id>/resourceGroups/topml-rg/providers/Microsoft.DataFactory/factories/topml-adf-prod" \
  --workspace "/subscriptions/<sub-id>/resourceGroups/topml-rg/providers/Microsoft.OperationalInsights/workspaces/topml-law-prod" \
  --logs '[
    {"category": "PipelineRuns",  "enabled": true},
    {"category": "ActivityRuns",  "enabled": true},
    {"category": "TriggerRuns",   "enabled": true}
  ]'
```

---

### 2. Structured Activity Output Log Schema

Each Copy Activity and Databricks activity in the topml pipeline must write a structured
outcome record to the pipeline's run output. Use a **Web Activity** or **Set Variable** at
the end of each pipeline to emit a structured audit event.

**Structured Audit Event Schema**

```json
{
  "pipeline_name":   "pl_prod_anp_daily",
  "run_id":          "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "trigger_type":    "ScheduleTrigger",
  "trigger_name":    "tr_pl_prod_anp_daily_0300",
  "activity_name":   "CopyCustomerSegments",
  "environment":     "prod",
  "run_date":        "2025-01-15",
  "start_time":      "2025-01-15T03:00:12.345Z",
  "end_time":        "2025-01-15T03:08:47.901Z",
  "duration_seconds": 515,
  "status":          "Succeeded",
  "rows_read":       142837,
  "rows_written":    142837,
  "rows_skipped":    0,
  "source_path":     "topmlprodsa/topml-segments/inbound/customer_segments/2025-01-15",
  "sink_path":       "/delta/prod/customer_segments",
  "initiated_by":    "tr_pl_prod_anp_daily_0300"
}
```

**Pipeline: Emit Audit Event via Web Activity After Each Critical Activity**

```json
{
  "name": "EmitAuditEvent",
  "type": "WebActivity",
  "dependsOn": [
    { "activity": "CopyCustomerSegments", "dependencyConditions": ["Succeeded", "Failed"] }
  ],
  "typeProperties": {
    "url": "https://topml-law-prod.ods.opinsights.azure.com/api/logs?api-version=2016-04-01",
    "method": "POST",
    "headers": {
      "Log-Type": "TopMLADFAudit",
      "Content-Type": "application/json"
    },
    "body": {
      "value": "@json(concat('{\"pipeline_name\":\"', pipeline().Pipeline, '\",\"run_id\":\"', pipeline().RunId, '\",\"activity_name\":\"CopyCustomerSegments\",\"status\":\"', activity('CopyCustomerSegments').Status, '\",\"rows_read\":', string(activity('CopyCustomerSegments').output.rowsRead), ',\"rows_written\":', string(activity('CopyCustomerSegments').output.rowsCopied), ',\"run_date\":\"', pipeline().parameters.runDate, '\"}'))",
      "type": "Expression"
    }
  }
}
```

---

### 3. KQL Query to Audit Pipeline Runs

Use the following KQL query in the Log Analytics workspace to audit pipeline execution history:

```kql
// All pipeline runs for pl_prod_anp_daily in the last 30 days
AzureDiagnostics
| where ResourceProvider == "MICROSOFT.DATAFACTORY"
| where Category == "PipelineRuns"
| where pipelineName_s == "pl_prod_anp_daily"
| where TimeGenerated >= ago(30d)
| project
    TimeGenerated,
    pipelineName_s,
    runId_g,
    status_s,
    start_t,
    end_t,
    durationInMs_d,
    triggeredBy_name_s
| order by TimeGenerated desc
```

```kql
// Failed activity runs with row counts — for data reconciliation audit
AzureDiagnostics
| where ResourceProvider == "MICROSOFT.DATAFACTORY"
| where Category == "ActivityRuns"
| where status_s == "Failed"
| where TimeGenerated >= ago(7d)
| project
    TimeGenerated,
    pipelineName_s,
    activityName_s,
    activityType_s,
    status_s,
    errorCode_s,
    errorMessage_s,
    rowsRead_d,
    rowsCopied_d,
    runId_g
| order by TimeGenerated desc
```

```kql
// Custom audit table — structured events from Web Activity
TopMLADFAudit_CL
| where TimeGenerated >= ago(90d)
| where status_s == "Succeeded"
| summarize
    total_rows_written = sum(rows_written_d),
    run_count          = count(),
    avg_duration_sec   = avg(duration_seconds_d)
  by pipeline_name_s, bin(TimeGenerated, 1d)
| order by TimeGenerated desc
```

---

### 4. Log Analytics Workspace Retention Policy (≥ 90 Days)

```bash
# Set retention to 90 days on the Log Analytics workspace
az monitor log-analytics workspace update \
  --resource-group topml-rg \
  --workspace-name topml-law-prod \
  --retention-time 90
```

**Verify the retention setting:**

```bash
az monitor log-analytics workspace show \
  --resource-group topml-rg \
  --workspace-name topml-law-prod \
  --query "retentionInDays" -o tsv
# Expected output: 90
```

---

## VIOLATION

### Anti-Pattern 1: Relying Solely on ADF Monitor UI

```
Developer checks pipeline run status via:
  ADF Studio → Monitor → Pipeline Runs → select run → view activity output
```

**Why this violates ENG-6.7:**
- ADF Monitor UI retains run history for **45 days** only (non-configurable)
- There is no way to programmatically query historical runs beyond 45 days
- No export mechanism — data is inaccessible during ADF service outages
- Compliance audits requiring >45 days of history cannot be satisfied
- No KQL queries possible — no integration with Security Center or Sentinel

---

### Anti-Pattern 2: No Structured Outcome Recording

```json
{
  "name": "pl_prod_anp_daily",
  "properties": {
    "activities": [
      { "name": "CopyCustomerSegments", "type": "Copy" },
      { "name": "RunScoringModel",       "type": "DatabricksNotebook" },
      { "name": "WriteOfferQueue",       "type": "Copy" }
    ]
  }
}
```

Pipeline completes with status `Succeeded` — but no audit record captures:
- How many rows were processed
- What source path was read
- Whether any rows were skipped due to data quality issues
- What the trigger run ID was for correlation

**Why this violates ENG-6.7:** Without structured outcome recording, a data quality incident
(e.g., 50,000 rows silently skipped due to a schema mismatch) is undetectable after the fact.
Row counts in the audit log are the primary mechanism for data reconciliation.

---

### Anti-Pattern 3: No Retention Policy (Default 30 Days)

```bash
# WRONG — workspace created with default retention (30 days), never updated
az monitor log-analytics workspace create \
  --resource-group topml-rg \
  --workspace-name topml-law-prod \
  --location eastus
# retention-time defaults to 30 days
```

**Why this violates ENG-6.7:** American Airlines data governance policy requires a minimum
90-day audit trail for all data pipeline operations. At 30 days, the default retention
fails to meet this requirement, and logs are silently deleted before any compliance review
period ends.

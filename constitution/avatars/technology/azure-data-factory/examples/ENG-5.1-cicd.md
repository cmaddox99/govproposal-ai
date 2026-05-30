---
law_id: ENG-5.1
avatar: azure-data-factory
---

# ENG-5.1 CI/CD Law — Azure Data Factory

All ADF changes must flow through Git + GitHub Actions. The ADF Studio **Publish** button is
prohibited. Every deployment must be validated before promotion, and production requires a
manual approval gate.

---

## COMPLIANT

### GitHub Actions Workflow — `adf-deploy.yml`

```yaml
# .github/workflows/adf-deploy.yml
name: ADF Deploy

on:
  push:
    branches: [main]
    paths:
      - 'adf/**'

permissions:
  id-token: write   # Required for OIDC / federated credential login
  contents: read

env:
  RESOURCE_GROUP: topml-rg
  ADF_STAGE: topml-adf-stage
  ADF_PROD: topml-adf-prod

jobs:
  validate:
    name: Validate ARM Template
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Azure Login (OIDC)
        uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - name: Validate ADF ARM Template (Stage Parameters)
        run: |
          az deployment group validate \
            --resource-group ${{ env.RESOURCE_GROUP }} \
            --template-file adf/adf-arm-template.json \
            --parameters @adf/adf-parameters-stage.json

  deploy-stage:
    name: Deploy to Stage
    needs: validate
    runs-on: ubuntu-latest
    environment: stage
    steps:
      - uses: actions/checkout@v4

      - name: Azure Login (OIDC)
        uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - name: Deploy to Stage
        run: |
          az deployment group create \
            --resource-group ${{ env.RESOURCE_GROUP }} \
            --template-file adf/adf-arm-template.json \
            --parameters @adf/adf-parameters-stage.json \
            --name "adf-deploy-stage-${{ github.sha }}"

      - name: Run Integration Test Pipeline
        id: run-integration-test
        run: |
          RUN_ID=$(az datafactory pipeline create-run \
            --factory-name ${{ env.ADF_STAGE }} \
            --resource-group ${{ env.RESOURCE_GROUP }} \
            --name pl_stage_integration_test \
            --parameters '{"runDate": "'"$(date -u +%Y-%m-%d)"'"}' \
            --query runId -o tsv)
          echo "run_id=$RUN_ID" >> "$GITHUB_OUTPUT"

      - name: Wait for Integration Test Pipeline Completion
        run: |
          RUN_ID="${{ steps.run-integration-test.outputs.run_id }}"
          for i in $(seq 1 30); do
            STATUS=$(az datafactory pipeline-run show \
              --factory-name ${{ env.ADF_STAGE }} \
              --resource-group ${{ env.RESOURCE_GROUP }} \
              --run-id "$RUN_ID" \
              --query status -o tsv)
            echo "Status: $STATUS (attempt $i/30)"
            if [ "$STATUS" = "Succeeded" ]; then exit 0; fi
            if [ "$STATUS" = "Failed" ] || [ "$STATUS" = "Cancelled" ]; then
              echo "Integration test pipeline failed with status: $STATUS"
              exit 1
            fi
            sleep 60
          done
          echo "Timed out waiting for pipeline completion"
          exit 1

  deploy-prod:
    name: Deploy to Production
    needs: deploy-stage
    runs-on: ubuntu-latest
    environment: production   # Requires manual approval in GitHub Environments settings
    steps:
      - uses: actions/checkout@v4

      - name: Azure Login (OIDC)
        uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID_PROD }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - name: Validate ADF ARM Template (Prod Parameters)
        run: |
          az deployment group validate \
            --resource-group ${{ env.RESOURCE_GROUP }} \
            --template-file adf/adf-arm-template.json \
            --parameters @adf/adf-parameters-prod.json

      - name: Deploy to Production
        run: |
          az deployment group create \
            --resource-group ${{ env.RESOURCE_GROUP }} \
            --template-file adf/adf-arm-template.json \
            --parameters @adf/adf-parameters-prod.json \
            --name "adf-deploy-prod-${{ github.sha }}"

      - name: Verify Production ADF Factory Is Running
        run: |
          az datafactory show \
            --name ${{ env.ADF_PROD }} \
            --resource-group ${{ env.RESOURCE_GROUP }} \
            --query "provisioningState" -o tsv | grep -q "Succeeded"
```

### Key Properties of This Workflow

| Property | Implementation |
|----------|----------------|
| ARM validation before deploy | `az deployment group validate` in both stage and prod jobs |
| Stage gate before prod | `needs: deploy-stage` on the `deploy-prod` job |
| Manual approval gate | `environment: production` with required reviewers in GitHub settings |
| OIDC authentication | No stored secrets — federated credential via `azure/login@v2` |
| Audit trail | Every deployment tagged with `${{ github.sha }}` in ARM deployment name |
| Integration test | `pl_stage_integration_test` must succeed before `deploy-prod` runs |

### Parameter Files Structure

```
adf/
├── adf-arm-template.json            # Generated by ADF Git integration (adf_publish branch)
├── adf-arm-template-parameters.json # Default parameter file from ADF Git (not used directly)
├── adf-parameters-dev.json          # Dev-specific overrides
├── adf-parameters-stage.json        # Stage-specific overrides
└── adf-parameters-prod.json         # Prod-specific overrides
```

**`adf-parameters-stage.json`**

```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "factoryName": {
      "value": "topml-adf-stage"
    },
    "ls_adls_stage_properties_typeProperties_url": {
      "value": "https://topmlstagesa.dfs.core.windows.net"
    },
    "ls_databricks_stage_properties_typeProperties_domain": {
      "value": "https://adb-1234567890.12.azuredatabricks.net"
    },
    "ls_databricks_stage_properties_typeProperties_workspaceResourceId": {
      "value": "/subscriptions/<sub-id>/resourceGroups/topml-rg/providers/Microsoft.Databricks/workspaces/topml-dbx-stage"
    }
  }
}
```

---

## VIOLATION

### Anti-Pattern 1: Clicking "Publish" in ADF Studio

```
Developer opens ADF Studio → edits pl_prod_anp_daily → clicks "Publish" button
```

**What happens:**
1. ADF Studio writes the change directly to the `adf_publish` branch, bypassing GitHub PRs
2. The change is immediately live in the production ADF instance — no validation, no review
3. No GitHub Actions run is triggered — no audit trail in Actions history
4. The Git-tracked state (`main` branch) diverges from the deployed state
5. The next legitimate GitHub Actions deploy may overwrite or conflict with the Studio-published
   change in unpredictable ways

---

### Anti-Pattern 2: No Stage Gate — Direct Deployment to Production

```yaml
# WRONG — deploys directly to prod with no stage validation
name: ADF Deploy (Unsafe)
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Production
        run: |
          az deployment group create \
            --resource-group topml-rg \
            --template-file adf/adf-arm-template.json \
            --parameters @adf/adf-parameters-prod.json
```

**Why this violates ENG-5.1:**
- No `validate` step — a malformed ARM template reaches production
- No integration test — a broken data flow that fails on real data only surfaces in production
- No manual approval gate — any merge to `main` immediately deploys to production
- No stage environment validation — cross-environment parameter errors are discovered in prod

---

### Anti-Pattern 3: Untested Changes Deployed Directly to Production

```bash
# Developer runs this directly from their laptop — no CI, no tests
az deployment group create \
  --resource-group topml-rg \
  --template-file /tmp/my-updated-adf.json \
  --parameters factoryName=topml-adf-prod
```

**Why this violates ENG-5.1:** Manual deployments from developer machines bypass all
pipeline controls, produce no audit trail, and cannot be reproduced or rolled back safely.

---
law_id: ENG-5.1
avatar: databricks-pyspark
---

# ENG-5.1: CI/CD Law Examples for Databricks / PySpark

---

## COMPLIANT

### GitHub Actions workflow: validate → test → deploy-stage → smoke-test → approve → deploy-prod

```yaml
# .github/workflows/topml-offer-scoring.yml
name: TopML Offer Scoring — CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  PYTHON_VERSION: "3.10"

jobs:
  # ── 1. Validate bundle syntax ──────────────────────────────────────────────
  validate:
    name: Validate DAB Bundle
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Databricks CLI
        uses: databricks/setup-cli@main

      - name: Validate bundle
        run: databricks bundle validate
        env:
          DATABRICKS_HOST: ${{ secrets.DATABRICKS_STAGE_HOST }}
          DATABRICKS_TOKEN: ${{ secrets.DATABRICKS_STAGE_TOKEN }}

  # ── 2. Unit & integration tests ────────────────────────────────────────────
  test:
    name: pytest (local Spark)
    runs-on: ubuntu-latest
    needs: validate
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ env.PYTHON_VERSION }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install dependencies
        run: |
          pip install --upgrade pip
          pip install -e ".[dev]"

      - name: Lint
        run: |
          ruff format src/ tests/ --check
          ruff check src/ tests/

      - name: Type check
        run: mypy src/ --strict

      - name: Run tests with coverage
        run: pytest tests/ --cov=src --cov-report=xml --cov-fail-under=90

      - name: Upload coverage report
        uses: codecov/codecov-action@v4
        with:
          files: coverage.xml

  # ── 3. Deploy to stage ─────────────────────────────────────────────────────
  deploy-stage:
    name: Deploy → Stage
    runs-on: ubuntu-latest
    needs: test
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4

      - name: Set up Databricks CLI
        uses: databricks/setup-cli@main

      - name: Deploy bundle to stage
        run: databricks bundle deploy --target stage
        env:
          DATABRICKS_HOST: ${{ secrets.DATABRICKS_STAGE_HOST }}
          DATABRICKS_TOKEN: ${{ secrets.DATABRICKS_STAGE_TOKEN }}

  # ── 4. Smoke test on stage ─────────────────────────────────────────────────
  smoke-test:
    name: Smoke Test on Stage
    runs-on: ubuntu-latest
    needs: deploy-stage
    steps:
      - uses: actions/checkout@v4

      - name: Set up Databricks CLI
        uses: databricks/setup-cli@main

      - name: Trigger smoke-test job and wait for completion
        run: |
          RUN_ID=$(databricks jobs run-now \
            --job-name topml_offer_scoring_smoke_test \
            --output json | jq -r '.run_id')

          echo "Smoke test run ID: $RUN_ID"

          # Poll until the run reaches a terminal state
          for i in $(seq 1 30); do
            STATE=$(databricks runs get --run-id "$RUN_ID" | jq -r '.state.life_cycle_state')
            echo "  [attempt $i] state: $STATE"
            if [[ "$STATE" == "TERMINATED" ]]; then
              RESULT=$(databricks runs get --run-id "$RUN_ID" | jq -r '.state.result_state')
              echo "Result: $RESULT"
              [[ "$RESULT" == "SUCCESS" ]] && exit 0 || exit 1
            fi
            sleep 20
          done
          echo "Timed out waiting for smoke test" && exit 1
        env:
          DATABRICKS_HOST: ${{ secrets.DATABRICKS_STAGE_HOST }}
          DATABRICKS_TOKEN: ${{ secrets.DATABRICKS_STAGE_TOKEN }}

  # ── 5. Manual approval gate ────────────────────────────────────────────────
  approve-prod:
    name: Approve Production Deploy
    runs-on: ubuntu-latest
    needs: smoke-test
    # GitHub Environment "production" has required reviewers configured
    environment: production
    steps:
      - name: Approval granted
        run: echo "Production deployment approved by required reviewer."

  # ── 6. Deploy to prod ──────────────────────────────────────────────────────
  deploy-prod:
    name: Deploy → Prod
    runs-on: ubuntu-latest
    needs: approve-prod
    steps:
      - uses: actions/checkout@v4

      - name: Set up Databricks CLI
        uses: databricks/setup-cli@main

      - name: Deploy bundle to prod
        run: databricks bundle deploy --target prod
        env:
          DATABRICKS_HOST: ${{ secrets.DATABRICKS_PROD_HOST }}
          DATABRICKS_TOKEN: ${{ secrets.DATABRICKS_PROD_TOKEN }}
```

**GitHub Secrets required:**

| Secret | Description |
|---|---|
| `DATABRICKS_STAGE_HOST` | Stage workspace URL |
| `DATABRICKS_STAGE_TOKEN` | Service principal PAT for stage |
| `DATABRICKS_PROD_HOST` | Prod workspace URL |
| `DATABRICKS_PROD_TOKEN` | Service principal PAT for prod (restricted to CI only) |

Tokens are rotated quarterly and scoped to the minimum permissions required (deploy + run jobs). The `production` GitHub Environment requires at least one named reviewer before `deploy-prod` runs.

---

## VIOLATION

### Manual notebook uploads via the Databricks UI

```
# VIOLATION — deployment process:
1. Developer edits notebook in Databricks UI on stage workspace
2. Downloads notebook as .ipynb
3. Uploads manually to prod workspace via "Import notebook"
4. No version control, no review, no rollback path

# Problems:
# - No validation step; broken notebooks go straight to prod
# - No environment promotion gating; stage and prod diverge silently
# - No audit trail of what changed between deployments
# - Cannot be rolled back — overwrite deletes the previous version
```

### No environment promotion, no validation step

```python
# VIOLATION — "deploy" script used in CI
# deploy.sh
databricks workspace import --path /Production/topml_scoring src/notebooks/scoring.py --overwrite
echo "Deployed!"
# - No `databricks bundle validate` — syntax errors reach prod
# - Writes directly to prod; stage is never tested
# - No smoke test; first indication of failure is a production alert
# - No approval gate; any push to main deploys immediately to prod
```

Both patterns violate ENG-5.1. Every change must pass validation, automated tests, and a smoke test on a non-production environment before reaching production. Manual UI operations are not repeatable, reviewable, or rollback-safe.

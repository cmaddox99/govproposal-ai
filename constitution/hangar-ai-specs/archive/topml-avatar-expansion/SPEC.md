# Spec: topml Avatar Expansion

## Overview

Create 4 new Hangar AI Constitution avatars to support the Targeted Offer Platform (topml) codebase adoption. Each avatar must follow the standard structure defined in `docs/guides/avatars/` and include examples for all relevant non-negotiable laws.

---

## Avatar 1: `avatars/technology/databricks-pyspark/`

### Required Files

```
avatars/technology/databricks-pyspark/
├── manifest.yaml
├── guidance.md
└── examples/
    ├── ENG-4.1-atomic-tdd.md
    ├── ENG-6.1-security-by-design.md
    ├── ENG-6.4-data-protection.md
    ├── ENG-6.7-audit-trail.md
    ├── ENG-3.1-complexity.md
    ├── ENG-5.1-cicd.md
    └── BUS-7.1-audit-trail.md
```

### manifest.yaml Requirements

```yaml
avatar:
  id: avatar-technology-databricks-pyspark
  type: technology
  name: "Databricks / PySpark / Delta Lake"
  version: "1.0.0"

stack:
  language: Python 3.10+
  platform: Databricks (Azure)
  frameworks:
    - PySpark
    - Delta Lake
    - MLflow
    - Databricks SDK (databricks-sdk >= 0.76.0)
    - Unity Catalog
  testing:
    - pytest >= 8.0.0
    - pytest-cov
    - databricks-connect (for local unit testing)
  tools:
    formatter: ruff
    linter: ruff
    type_checker: mypy
    bundle: databricks-asset-bundles

dependencies:
  required:
    - databricks-sdk>=0.76.0
    - databricks-sql-connector>=4.2.0
    - pyarrow>=22.0.0
    - pyspark (via Databricks runtime)
    - delta (via Databricks runtime)
    - mlflow (via Databricks runtime)
  dev:
    - pytest>=8.3.0
    - pytest-cov>=6.0.0
    - ruff>=0.1.0
    - mypy>=1.8.0

activates:
  skills:
    - skill-06-atomic-tdd
    - skill-07-vertical-slice-dev
    - skill-08-code-review
    - skill-04-business-domain-modeling
  workflows:
    - workflow-discovery-to-delivery
    - workflow-sdd-lifecycle

specializes_laws:
  - id: ENG-4.1
    title: Atomic TDD Law
    example_file: examples/ENG-4.1-atomic-tdd.md
  - id: ENG-6.1
    title: Security by Design Law
    example_file: examples/ENG-6.1-security-by-design.md
  - id: ENG-6.4
    title: Data Protection Law
    example_file: examples/ENG-6.4-data-protection.md
  - id: ENG-6.7
    title: Audit Trail Law
    example_file: examples/ENG-6.7-audit-trail.md
  - id: ENG-3.1
    title: Complexity Limits
    example_file: examples/ENG-3.1-complexity.md
  - id: ENG-5.1
    title: CI/CD Law
    example_file: examples/ENG-5.1-cicd.md
  - id: BUS-7.1
    title: Business Audit Trail Law
    example_file: examples/BUS-7.1-audit-trail.md
```

### guidance.md Requirements

Cover:
- Databricks workspace structure (dev/stage/prod)
- Delta Lake table conventions (schema, naming, partitioning)
- PySpark transformation patterns (immutable DataFrames, functional style)
- MLflow experiment tracking patterns
- Unity Catalog table access patterns
- Databricks Asset Bundle deployment
- Testing strategy: pytest with Delta table fixtures, mocking Spark sessions
- Secret management via Databricks Secrets API (never `.env` files in notebooks)

### Example File Requirements

**ENG-4.1-atomic-tdd.md** — Show:
- Compliant: ONE pytest test for a single PySpark transformation function, using a Delta table fixture, RED-GREEN-REFACTOR cycle
- Violation: Writing multiple transformation tests before implementation

**ENG-6.1-security-by-design.md** — Show:
- Compliant: Unity Catalog RBAC grants, Databricks Secrets API usage (not hardcoded credentials), service principal authentication pattern
- Violation: Hardcoded connection strings in notebooks, overly permissive catalog grants

**ENG-6.4-data-protection.md** — Show:
- Compliant: Delta Lake column masking for PII fields (customer_id, email, loyalty_id), Fernet encryption for tokens, row-level security via Unity Catalog
- Violation: Writing raw PII to unencrypted Delta tables without column masking

**ENG-6.7-audit-trail.md** — Show:
- Compliant: `DESCRIBE HISTORY` on Delta tables, MLflow run metadata as provenance, dedicated audit log Delta table (append-only), recording which model version scored which customer
- Violation: Overwriting Delta tables without history, not tracking model predictions to run IDs

**ENG-3.1-complexity.md** — Show:
- Compliant: Breaking a complex PySpark pipeline into single-responsibility transformation functions (cyclomatic complexity ≤ 10)
- Violation: One massive `transform()` function with 15+ branches

**ENG-5.1-cicd.md** — Show:
- Compliant: GitHub Actions workflow using Databricks Asset Bundles (`databricks bundle deploy`), environment promotion gates (dev → stage → prod), smoke test job before prod deploy
- Violation: Manual notebook uploads, no environment promotion

**BUS-7.1-audit-trail.md** — Show:
- Compliant: Offer decision audit log (customer_id, offer_id, model_version, score, timestamp, channel) written to append-only Delta table with TTL archival policy
- Violation: Logging offer decisions to ephemeral Spark driver stdout

---

## Avatar 2: `avatars/technology/r-shiny/`

### Required Files

```
avatars/technology/r-shiny/
├── manifest.yaml
├── guidance.md
└── examples/
    ├── ENG-4.1-atomic-tdd.md
    ├── ENG-6.1-security-by-design.md
    ├── ENG-3.1-complexity.md
    └── ENG-6.5-validation.md
```

### manifest.yaml Requirements

```yaml
avatar:
  id: avatar-technology-r-shiny
  type: technology
  name: "R / Shiny"
  version: "1.0.0"

stack:
  language: R 4.x
  framework: Shiny
  packages:
    - shiny
    - shinydashboard
    - testthat
    - shinytest2
    - AzureStor
    - data.table
    - config
  testing:
    - testthat >= 3.0.0
    - shinytest2

specializes_laws:
  - id: ENG-4.1
    title: Atomic TDD Law
    example_file: examples/ENG-4.1-atomic-tdd.md
  - id: ENG-6.1
    title: Security by Design Law
    example_file: examples/ENG-6.1-security-by-design.md
  - id: ENG-3.1
    title: Complexity Limits
    example_file: examples/ENG-3.1-complexity.md
  - id: ENG-6.5
    title: Input Validation Law
    example_file: examples/ENG-6.5-validation.md
```

### Example File Requirements

**ENG-4.1-atomic-tdd.md** — Show:
- Compliant: testthat test for a single reactive computation function extracted from Shiny server, shinytest2 test for a single UI interaction
- Violation: Testing entire server.R in one test, no tests for reactive logic

**ENG-6.1-security-by-design.md** — Show:
- Compliant: Azure AD authentication check before rendering any dashboard content, config-based secret loading (never hardcoded storage keys), session timeout enforcement
- Violation: Hardcoded Azure Blob Storage keys in global.R

**ENG-3.1-complexity.md** — Show:
- Compliant: Reactive chains broken into named functions with single responsibility
- Violation: Single `observe()` block with 20+ reactive dependencies

**ENG-6.5-validation.md** — Show:
- Compliant: `validate(need(...))` for all user inputs before data queries
- Violation: Passing raw UI inputs directly to data queries

### guidance.md Requirements

Cover:
- Separating business logic from Shiny reactive glue (testability)
- Azure Blob Storage integration via AzureStor
- Config-based environment management (`config` package)
- Module pattern for scalable Shiny apps
- Dashboard KPI refresh patterns

---

## Avatar 3: `avatars/technology/azure-data-factory/`

### Required Files

```
avatars/technology/azure-data-factory/
├── manifest.yaml
├── guidance.md
└── examples/
    ├── ENG-4.1-atomic-tdd.md
    ├── ENG-5.1-cicd.md
    ├── ENG-6.1-security-by-design.md
    └── ENG-6.7-audit-trail.md
```

### manifest.yaml Requirements

```yaml
avatar:
  id: avatar-technology-azure-data-factory
  type: technology
  name: "Azure Data Factory"
  version: "1.0.0"

stack:
  platform: Azure Data Factory
  authoring: JSON (ARM templates)
  orchestration:
    - Pipelines
    - Triggers
    - Linked Services
    - Datasets
  security:
    - Azure Managed Identity
    - Azure Key Vault parameter references
  cicd:
    - GitHub Actions
    - ARM template deployment
  testing:
    - ADF REST API (pipeline validation)
    - Integration test pipelines

specializes_laws:
  - id: ENG-4.1
    title: Atomic TDD Law
    example_file: examples/ENG-4.1-atomic-tdd.md
  - id: ENG-5.1
    title: CI/CD Law
    example_file: examples/ENG-5.1-cicd.md
  - id: ENG-6.1
    title: Security by Design Law
    example_file: examples/ENG-6.1-security-by-design.md
  - id: ENG-6.7
    title: Audit Trail Law
    example_file: examples/ENG-6.7-audit-trail.md
```

### Example File Requirements

**ENG-4.1-atomic-tdd.md** — Show:
- Compliant: Test a single pipeline activity in isolation using ADF debug mode + REST API validation before composing into a parent pipeline
- Violation: Building a 20-activity pipeline before running any tests

**ENG-5.1-cicd.md** — Show:
- Compliant: GitHub Actions deploying ADF ARM templates per environment (dev/stage/prod), pull-request validation via ADF REST API, no manual publish button
- Violation: Using ADF Studio "Publish" button as the deployment mechanism

**ENG-6.1-security-by-design.md** — Show:
- Compliant: Linked Service using Managed Identity (no credentials), Key Vault parameter reference for all secrets (`@Microsoft.KeyVault(...)`), no passwords in JSON pipeline definitions
- Violation: Inline connection strings or passwords in linked service JSON

**ENG-6.7-audit-trail.md** — Show:
- Compliant: ADF Monitor activity run history retention policy, Diagnostic Settings sending run logs to Log Analytics, structured log of pipeline outcomes (pipeline_name, run_id, start_time, end_time, status, rows_processed)
- Violation: Relying solely on ADF Studio monitor with no log export/retention

### guidance.md Requirements

Cover:
- Pipeline naming conventions (matches topml pattern: `_stage_<campaign>_daily`)
- Linked Service patterns (Managed Identity vs. Key Vault ref)
- Trigger types (schedule, tumbling window, event-based)
- Environment promotion workflow (dev → stage → prod ARM deploy)
- Parameterization best practices

---

## Avatar 4: `avatars/product-type/marketing-personalization/`

### Required Files

```
avatars/product-type/marketing-personalization/
├── manifest.yaml
├── guidance.md
├── examples/
│   ├── personas.md
│   ├── PRD-1.1-discovery.md
│   ├── PRD-1.2-problem-first.md
│   ├── PRD-1.5-evidence-based.md
│   ├── PRD-2.1-journey.md
│   ├── PRD-3.1-roadmap.md
│   ├── PRD-5.1-mvp.md
│   ├── PRD-6.2-retention.md
│   ├── BUS-4.3-data-subject-rights.md
│   ├── BUS-7.1-audit-trail.md
│   └── BUS-9.3-breach-notification.md
└── use-cases/
    ├── offer-experiment-design/
    ├── customer-segmentation/
    └── campaign-attribution/
```

### manifest.yaml Requirements

```yaml
avatar:
  id: avatar-product-marketing-personalization
  type: product
  name: "Marketing Personalization & Targeted Offers"
  version: "1.0.0"

domain:
  category: "Customer Offer Targeting & Campaign Management"
  description: |
    The Marketing Personalization domain powers American Airlines' ability to deliver
    the right offer, to the right customer, at the right time — across email, app,
    web, and loyalty channels. It encompasses offer selection and ranking, propensity
    scoring, customer segmentation, campaign experiment design, and offer attribution.
    Governed by customer data privacy laws and retention-first business strategy.

  personas:
    - Campaign Manager
    - Data Scientist
    - CRM Analyst
    - Marketing Strategist
    - Customer (Traveler)
  personas_file: "examples/personas.md"

core_journeys:
  - "Offer Selection & Ranking"
  - "Campaign Experiment Design (A/B Testing)"
  - "Customer Segmentation & Targeting"
  - "Offer Delivery & Attribution"
  - "Retention Win-Back Campaign"

specializes_laws:
  - id: PRD-1.1
    title: Continuous Discovery
    example_file: examples/PRD-1.1-discovery.md
  - id: PRD-1.2
    title: Problem-First Law
    example_file: examples/PRD-1.2-problem-first.md
  - id: PRD-1.5
    title: Evidence-Based Decision Law
    example_file: examples/PRD-1.5-evidence-based.md
  - id: PRD-2.1
    title: User Journey Mapping
    example_file: examples/PRD-2.1-journey.md
  - id: PRD-3.1
    title: Roadmap Planning
    example_file: examples/PRD-3.1-roadmap.md
  - id: PRD-5.1
    title: MVP Law
    example_file: examples/PRD-5.1-mvp.md
  - id: PRD-6.2
    title: Retention Over Acquisition Law
    example_file: examples/PRD-6.2-retention.md
  - id: BUS-4.3
    title: Data Subject Rights Law
    example_file: examples/BUS-4.3-data-subject-rights.md
  - id: BUS-7.1
    title: Business Audit Trail Law
    example_file: examples/BUS-7.1-audit-trail.md
  - id: BUS-9.3
    title: Breach Notification Law
    example_file: examples/BUS-9.3-breach-notification.md
```

### personas.md Requirements

Define 5 personas with: name, role, goals (3), pain points (3), success metrics:
1. **Campaign Manager** — owns campaign lifecycle, cares about delivery rate and conversion
2. **Data Scientist** — builds propensity models, cares about model lift and retraining cadence
3. **CRM Analyst** — builds segments and targeting rules, cares about audience quality
4. **Marketing Strategist** — sets offer strategy, cares about LTV impact and retention
5. **Customer (Traveler)** — receives offers, cares about relevance and opt-out control

### Example File Requirements

**PRD-1.2-problem-first.md** — Show:
- Compliant: "We observe that 67% of email offers have <1% CTR. Hypothesis: offers are not relevant to recipient travel patterns. We will validate by analyzing correlation between offer destination and customer's historical routes before building a new recommendation model."
- Violation: "We should build a new ML recommendation engine" (solution-first, no problem validation)

**PRD-1.5-evidence-based.md** — Show:
- Compliant: A/B test results table (control vs. treatment CTR/conversion), propensity model lift curve, cohort analysis of re-engagement by offer type — all used as decision inputs
- Violation: Choosing an offer strategy based on stakeholder opinion without data

**PRD-5.1-mvp.md** — Show:
- Compliant: "Run a 2-week holdout experiment on 5% of c_lpr customers with a simplified offer selection rule before committing to a full ML model rebuild."
- Violation: "Let's rebuild the entire campaign pipeline before testing the hypothesis"

**PRD-6.2-retention.md** — Show:
- Compliant: KPI framework that prioritizes 90-day re-engagement rate and LTV over raw email open count; roadmap gated on retention metrics
- Violation: Optimizing purely for impression volume without measuring downstream retention

**BUS-4.3-data-subject-rights.md** — Show:
- Compliant: Opt-out mechanism that removes customer from all propensity model training data and targeting segments within 30 days; documented erasure process for Delta table PII
- Violation: No mechanism for customers to opt out of offer targeting

**BUS-7.1-audit-trail.md** — Show:
- Compliant: Offer decision log schema (`customer_id_hash`, `offer_id`, `model_version`, `score`, `channel`, `delivered_at`, `campaign_run_id`) in append-only Delta table with 7-year retention
- Violation: No record of which offer was shown to which customer

**BUS-9.3-breach-notification.md** — Show:
- Compliant: Documented 72-hour notification runbook for targeting data exposure (who to notify, what data was exposed, remediation steps)
- Violation: No breach response plan for customer PII used in offer targeting

---

## Registry Update

### `avatars/index.yaml` Addition

Add the following entries to the appropriate sections:

```yaml
# Under technology category:
- id: avatar-technology-databricks-pyspark
  name: "Databricks / PySpark / Delta Lake"
  path: avatars/technology/databricks-pyspark/
  activates:
    skills: [skill-06-atomic-tdd, skill-07-vertical-slice-dev, skill-08-code-review]
  specializes_laws: [ENG-4.1, ENG-6.1, ENG-6.4, ENG-6.7, ENG-3.1, ENG-5.1, BUS-7.1]

- id: avatar-technology-r-shiny
  name: "R / Shiny"
  path: avatars/technology/r-shiny/
  activates:
    skills: [skill-06-atomic-tdd, skill-08-code-review]
  specializes_laws: [ENG-4.1, ENG-6.1, ENG-3.1, ENG-6.5]

- id: avatar-technology-azure-data-factory
  name: "Azure Data Factory"
  path: avatars/technology/azure-data-factory/
  activates:
    skills: [skill-06-atomic-tdd, skill-08-code-review]
  specializes_laws: [ENG-4.1, ENG-5.1, ENG-6.1, ENG-6.7]

# Under product-type category:
- id: avatar-product-marketing-personalization
  name: "Marketing Personalization & Targeted Offers"
  path: avatars/product-type/marketing-personalization/
  activates:
    skills: [skill-02-user-journey-mapping, skill-03-executable-spec, skill-04-business-domain-modeling]
    workflows: [workflow-discovery-to-delivery]
  specializes_laws: [PRD-1.1, PRD-1.2, PRD-1.5, PRD-2.1, PRD-3.1, PRD-5.1, PRD-6.2, BUS-4.3, BUS-7.1, BUS-9.3]
```

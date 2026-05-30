# Proposal: topml Avatar Expansion — Databricks, R/Shiny, Azure Data Factory & Marketing Personalization

## Why

The **Targeted Offer Platform (topml)** is American Airlines' core marketing personalization and ML platform — 561 Python files, 69 Azure Data Factory pipelines, an R Shiny monitoring dashboard, and a full Databricks/Delta Lake/MLflow stack. During an ORAA adoption clinic, a gap analysis revealed that the Hangar AI Constitution is missing the avatars required to govern this codebase effectively.

Specifically:
- The entire topml compute layer runs on **Databricks (PySpark, Delta Lake, Databricks SDK)** — no avatar exists for this stack despite it being the most widely used enterprise data/ML platform at AA.
- The monitoring dashboard is **R Shiny** — no avatar exists for this language/framework at all.
- Orchestration is driven by **Azure Data Factory** (69 pipelines, 30 triggers) — no avatar covers ADF-based pipeline governance.
- The product domain — **Marketing Personalization & Targeted Offers** — is entirely uncovered. The `loyalty-aadvantage` avatar covers earning/redemption, but nobody covers the offer decisioning engine, campaign management, customer segmentation, propensity scoring, and A/B testing that define topml's product surface.

Additionally, no existing avatar (tech or product) provides examples for the non-negotiable laws **ENG-6.1, ENG-6.4, ENG-6.7, BUS-4.3, BUS-7.1, or BUS-9.3** — all of which are critically relevant to topml given its handling of customer PII and financial offer decisions at scale.

## What Changes

- **Add `avatars/technology/databricks-pyspark/`** — Databricks, PySpark, Delta Lake, Unity Catalog, Databricks SDK, MLflow. Specializes all 4 engineering non-negotiable laws with Databricks-native examples.
- **Add `avatars/technology/r-shiny/`** — R Shiny dashboard framework, testthat, shinytest2, AzureStor. Specializes ENG-4.1 and ENG-6.1 with R-native examples.
- **Add `avatars/technology/azure-data-factory/`** — ADF pipeline authoring, linked services, triggers, ARM/JSON governance, CI/CD deployment. Specializes ENG-5.1, ENG-6.1, ENG-6.7.
- **Add `avatars/product-type/marketing-personalization/`** — Offer targeting, campaign management, propensity scoring, A/B testing, customer segmentation. Specializes all product and business non-negotiable laws with topml-specific examples.
- **Update `avatars/index.yaml`** — Register all 4 new avatars.

## New Avatars

### 1. Technology: Databricks / PySpark / Delta Lake

| Field | Value |
|-------|-------|
| **ID** | `avatar-technology-databricks-pyspark` |
| **Stack** | Python 3.10+, PySpark, Delta Lake, Databricks SDK, MLflow, Unity Catalog |
| **Testing** | pytest, databricks-connect, delta-rs, pytest-spark |
| **Specializes Laws** | ENG-4.1, ENG-6.1, ENG-6.4, ENG-6.7, ENG-3.1, ENG-5.1, BUS-7.1 |
| **Non-Negotiable Coverage** | ENG-4.1 ✅ ENG-6.1 ✅ ENG-6.4 ✅ ENG-6.7 ✅ BUS-7.1 ✅ |

**Law Examples:**
- `ENG-4.1`: Atomic TDD for PySpark transformations using pytest + Delta table fixtures
- `ENG-6.1`: Security by Design — Unity Catalog RBAC, Databricks Secrets, workspace isolation, service principal auth
- `ENG-6.4`: Data Protection — Delta Lake column masking, PII encryption at rest, Fernet token management for customer IDs
- `ENG-6.7`: Audit Trail — Delta table `DESCRIBE HISTORY`, MLflow run provenance, immutable audit log tables
- `ENG-3.1`: Complexity limits for PySpark transformation chains
- `ENG-5.1`: CI/CD with Databricks Asset Bundles + GitHub Actions
- `BUS-7.1`: Business audit trail for offer decisions and model predictions

---

### 2. Technology: R / Shiny

| Field | Value |
|-------|-------|
| **ID** | `avatar-technology-r-shiny` |
| **Stack** | R 4.x, Shiny, shinydashboard, testthat, shinytest2, AzureStor |
| **Testing** | testthat, shinytest2 |
| **Specializes Laws** | ENG-4.1, ENG-6.1, ENG-3.1, ENG-6.5 |
| **Non-Negotiable Coverage** | ENG-4.1 ✅ ENG-6.1 ✅ |

**Law Examples:**
- `ENG-4.1`: Atomic TDD for Shiny reactive expressions and server logic using testthat + shinytest2
- `ENG-6.1`: Security by Design — Azure AD authentication, session token management, input sanitization in Shiny apps
- `ENG-3.1`: Complexity limits for reactive dependency chains
- `ENG-6.5`: Input validation for Shiny UI inputs

---

### 3. Technology: Azure Data Factory

| Field | Value |
|-------|-------|
| **ID** | `avatar-technology-azure-data-factory` |
| **Stack** | Azure Data Factory, ARM/JSON pipelines, Linked Services, Azure Key Vault, GitHub Actions |
| **Testing** | ADF Test Framework, pipeline unit testing via REST API |
| **Specializes Laws** | ENG-4.1, ENG-5.1, ENG-6.1, ENG-6.7 |
| **Non-Negotiable Coverage** | ENG-4.1 ✅ ENG-6.1 ✅ ENG-6.7 ✅ |

**Law Examples:**
- `ENG-4.1`: Atomic TDD for ADF pipeline activities — test each activity in isolation before composing
- `ENG-5.1`: CI/CD pipeline governance — ARM template deployment, environment promotion (dev → stage → prod)
- `ENG-6.1`: Security by Design — Managed Identity for linked services, Key Vault parameter references, no hardcoded credentials in JSON
- `ENG-6.7`: Audit Trail — ADF monitor activity runs, pipeline run history, diagnostic log retention

---

### 4. Product Type: Marketing Personalization & Targeted Offers

| Field | Value |
|-------|-------|
| **ID** | `avatar-product-marketing-personalization` |
| **Domain** | Offer targeting, campaign management, propensity scoring, A/B testing, customer segmentation |
| **Personas** | Campaign Manager, Data Scientist, CRM Analyst, Marketing Strategist, Customer (traveler) |
| **Core Journeys** | Offer Selection & Ranking, Campaign Experiment Design, Customer Segmentation, Offer Delivery & Attribution, Retention Win-Back |
| **Specializes Laws** | PRD-1.1, PRD-1.2, PRD-1.5, PRD-2.1, PRD-3.1, PRD-5.1, PRD-6.2, BUS-4.3, BUS-7.1, BUS-9.3 |
| **Non-Negotiable Coverage** | PRD-1.2 ✅ PRD-1.5 ✅ PRD-5.1 ✅ PRD-6.2 ✅ BUS-4.3 ✅ BUS-7.1 ✅ BUS-9.3 ✅ |

**Law Examples:**
- `PRD-1.1`: Continuous Discovery — interview campaign managers, analyze CTR/conversion data, research competitor personalization approaches
- `PRD-1.2`: Problem-First Law — define the offer relevance problem before choosing ML model architecture
- `PRD-1.5`: Evidence-Based Decision — A/B test results, propensity model lift curves, campaign conversion attribution
- `PRD-2.1`: User Journey Mapping — customer path from offer impression → click → conversion → loyalty impact
- `PRD-3.1`: Roadmap Planning — campaign calendar, model retraining cadence, channel expansion roadmap
- `PRD-5.1`: MVP Law — campaign experiment as the smallest test to validate offer hypothesis (not a full campaign build)
- `PRD-6.2`: Retention Over Acquisition — optimize for customer LTV and re-engagement, not raw impression count
- `BUS-4.3`: Data Subject Rights — opt-out of offer targeting, right to erasure from propensity model training data
- `BUS-7.1`: Business Audit Trail — which offer was shown, to which customer, at what time, by which model version
- `BUS-9.3`: Breach Notification — customer PII exposure response procedure for offer/targeting data

## Capabilities

### New Capabilities

- `avatar-technology-databricks-pyspark`: Full Databricks stack governance with non-negotiable law coverage for PySpark, Delta Lake, MLflow, and Unity Catalog
- `avatar-technology-r-shiny`: R Shiny dashboard governance with TDD and security patterns
- `avatar-technology-azure-data-factory`: ADF pipeline governance including JSON authoring standards, CI/CD, and audit trail requirements
- `avatar-product-marketing-personalization`: Product governance for offer targeting, campaign experiments, and customer data rights in personalization systems

### Modified Capabilities

- `avatars/index.yaml`: Register 4 new avatars in the central registry

## Non-Negotiable Law Coverage Summary

| Law | Before | After |
|-----|--------|-------|
| ENG-4.1 Atomic TDD | ✅ most tech avatars | ✅ + Databricks, R/Shiny, ADF examples |
| ENG-6.1 Security by Design | ❌ no tech avatar covers this | ✅ Databricks, R/Shiny, ADF |
| ENG-6.4 Data Protection | ❌ no tech avatar covers this | ✅ Databricks (PII in Delta Lake) |
| ENG-6.7 Audit Trail | ❌ no tech avatar covers this | ✅ Databricks, ADF |
| PRD-1.2 Problem-First Law | ❌ no product avatar covers this | ✅ Marketing Personalization |
| PRD-1.5 Evidence-Based Decision | ❌ no product avatar covers this | ✅ Marketing Personalization |
| PRD-5.1 MVP Law | ✅ product avatars | ✅ + campaign experiment examples |
| PRD-6.2 Retention Over Acquisition | ❌ no product avatar covers this | ✅ Marketing Personalization |
| BUS-4.3 Data Subject Rights | ❌ no avatar covers this | ✅ Marketing Personalization |
| BUS-7.1 Business Audit Trail | ❌ no avatar covers this | ✅ Databricks + Marketing Personalization |
| BUS-9.3 Breach Notification | ❌ no avatar covers this | ✅ Marketing Personalization |

## Impact

- **Avatars added:** 4 (3 technology, 1 product-type)
- **Docs affected:** `avatars/index.yaml`
- **Laws with new examples:** ENG-6.1, ENG-6.4, ENG-6.7, PRD-1.2, PRD-1.5, PRD-6.2, BUS-4.3, BUS-7.1, BUS-9.3
- **Teams benefiting:** topml team (ORAA), any team using Databricks, R Shiny, or ADF at AA
- **Workshops affected:** Constitution Adoption Clinic — new avatars immediately usable for topml adoption
- **Breaking changes:** None — additive only

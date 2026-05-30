# Ground Ops Staffing Analytics — Product Guidance

Welcome to the American Airlines Ground Ops Staffing Analytics product avatar! This guide helps
you apply the Hangar AI Constitution to workforce optimization, bag delivery analytics, and ramp
staffing decision-support products.

---

## What We Do

Ground Ops Staffing Analytics predicts how many ramp agents (drivers) are needed per shift, per
delivery type, per hub station. The system ingests historical bag scan events, flight schedules,
and passenger manifests, then trains quantile regression models to produce calibrated staffing
recommendations. Operations supervisors use these plans to right-size their crews before each
seasonal period — reducing both missed SLAs (under-staffing) and labor waste (over-staffing).

**Key differentiators:**
- **Accuracy:** Quantile calibration allows choosing a risk profile (e.g., 75th percentile = staffed for
  75% of observed demand scenarios)
- **Transparency:** Pipeline is auditable — every run tied to a `run_id`, every output traceable to source data
- **Station-aware:** Per-station config drives all thresholds — no one-size-fits-all model
- **IROP-resilient:** IROP day flagging prevents model from under-staffing on disruption-heavy days

---

## Product Laws for Ground Ops Staffing

### 1. PRD-1.1: Continuous Discovery

**For Staffing Analytics specifically:**

- Interview ramp supervisors monthly about accuracy gaps in current staffing plans
- Review post-season retrospectives: which shifts were under/over-staffed and by how much?
- Analyze historical pull-time data to find delivery-type patterns the model may be missing
- Study IROP event logs to understand staffing failure modes during irregular operations

**Example:** Supervisors at CLT reported that T-Link (international transfer) bags required 2
additional drivers on Friday evenings not captured in the model. Discovery revealed T-Link volumes
spike 40% on Friday evenings due to inbound European connections — a feature gap in the model.

---

### 2. PRD-2.1: User Journey Mapping

**For Staffing Analytics specifically — the analyst workflow:**

```
STAFFING PLAN GENERATION JOURNEY

┌──────────────────────────────────────────────────────────────────┐
│  STEP 1: Configure Run                                           │
│  └─ Set run_config.json: station, season, years, process type    │
│  └─ Pain point: Manual JSON editing — no UI                       │
│                                                                  │
│  STEP 2: Extract Data (01_load_data.ipynb)                       │
│  └─ Query ADLS (bag events, flights) + Mosaic (pax)              │
│  └─ Pain point: Queries take 20–40 min; failure = manual rerun   │
│                                                                  │
│  STEP 3: Feature Engineering (02_feature_engineering.ipynb)      │
│  └─ Join data, compute pull times, classify stop temperatures    │
│  └─ Pain point: Station config changes require notebook edits    │
│                                                                  │
│  STEP 4: Input Statistics (03_input_statistics.ipynb)            │
│  └─ Validate data quality before model training                  │
│  └─ Pain point: Manual review required — no automated gates      │
│                                                                  │
│  STEP 5: Train Model (ml/01_decision_tree.ipynb)                 │
│  └─ Train per-delivery-type models                               │
│  └─ Pain point: No experiment tracking — can't compare runs      │
│                                                                  │
│  STEP 6: Business Rules (ml/02_rule_post_process.ipynb)          │
│  └─ Apply caps, floors, IROP adjustments                         │
│  └─ Pain point: Business rules are hard-coded in notebook cells  │
│                                                                  │
│  STEP 7: Percentile Selection (postprocess/01_percentile.ipynb)  │
│  └─ Choose staffing level at configured quantile                 │
│  └─ Pain point: Quantile is hard-coded — no UI to adjust         │
│                                                                  │
│  STEP 8: Review & Approve                                        │
│  └─ Supervisor reviews staffing_plan.json                        │
│  └─ Pain point: JSON output — no dashboard for review            │
└──────────────────────────────────────────────────────────────────┘
```

---

### 3. PRD-3.1: Roadmap Planning

**For Staffing Analytics — sequencing by constraint:**

| Priority | Feature | Rationale | Effort |
|----------|---------|-----------|--------|
| 1 | Safety net: characterization tests (utils/) | Safety before any change | Phase 1 |
| 2 | Extract notebook logic to tested modules | Makes model trustworthy to modify | Phase 2 |
| 3 | Automated data quality gates (step 3) | Prevents silent bad-data runs | Phase 2 |
| 4 | MLflow experiment tracking | Enables model comparison across seasons | Phase 3 |
| 5 | Configurable quantile via run_config | Removes magic constant in notebook | Phase 3 |
| 6 | Streamlit review dashboard | Replaces JSON review with visual plan | Phase 4 |
| 7 | New station onboarding automation | Scale from 4 to 8+ stations | Phase 4 |

---

### 4. PRD-4.1: MVP & Product-Market Fit

**For Staffing Analytics — validate before expanding:**

- **Accuracy gate:** Predicted staffing within 15% of actual on ≥80% of shifts
- **Pilot station:** DFW Summer 2024 retrospective (known actuals available)
- **Pilot user:** One station operations manager reviewing JSON output
- **Decision threshold:**
  - Accuracy >80%: Proceed to Phase 2 extraction
  - Accuracy 60–80%: Improve feature engineering first
  - Accuracy <60%: Re-examine domain assumptions with supervisors (discovery loop)

---

### 5. PRD-5.1: Metrics & Success Definition

**Primary outcome metrics:**

| Metric | Baseline | Target | How Measured |
|--------|----------|--------|-------------|
| **Staffing accuracy** | Unknown (manual estimates) | ±15% on 80%+ shifts | predicted vs. actual headcount per shift |
| **Pull-time SLA** | Current season actuals | ≥85% within `first_pulltime` | bag scan timestamps vs. delivery threshold |
| **Over-staffing waste** | Current season baseline | 20% reduction | (actual − required) × hourly rate |
| **Pipeline reliability** | Unknown | 100% successful runs per season | run completion rate |
| **Model coverage** | CLT, DFW, PHX, MIA | +4 stations by end of year | active station count |

**Process metrics:**

| Metric | Baseline | Target |
|--------|----------|--------|
| Pipeline run time | ~2 hours (manual) | <45 min (automated) |
| Rerun rate due to data errors | ~30% (estimated) | <5% with data gates |
| Analyst time for plan review | 4 hours | <30 min with dashboard |

---

## Brownfield Modernization Guidance

### Notebook Preservation Policy (ENG-4.4 + legacy-ml-interop)

> **Default: DO NOT modify notebook cells until the Phase 1 safety net is complete.**

The ABR-Staffing pipeline consists of Jupyter notebooks containing business logic mixed with
orchestration. Per the `legacy-ml-interop` avatar:

- **Phase 1:** Characterize `utils/` Python modules with unit tests (no notebook changes)
- **Phase 2:** Extract embedded notebook logic into `src/abr/` tested modules (using TDD)
- **Phase 3:** Notebooks become orchestration-only — calling tested `src/abr/` functions

**Extraction targets (Phase 2):**

| Notebook Section | Extract To | Law |
|-----------------|-----------|-----|
| Pull time calculation | `src/abr/features.py::compute_pull_time()` | ENG-4.4 |
| Stop temperature classification | `src/abr/features.py::classify_stop_temperature()` | ENG-4.4 |
| Data quality validation | `src/abr/validation.py::validate_input_data()` | ENG-4.4 |
| Business rule application | `src/abr/business_rules.py::apply_staffing_caps()` | ENG-4.4 |
| Percentile selection | `src/abr/percentile_selector.py::select_at_quantile()` | ENG-4.4 |
| Model training loop | `src/abr/model_trainer.py::train_per_delivery_type()` | ENG-4.4 |

### Station Config as Single Source of Truth

`config/application.yml` is the authoritative source for all operational thresholds:
- `first_pulltime` — delivery SLA benchmark
- `daily_irop_pct_threshold` — IROP flagging sensitivity
- `max_driver_per_inbound_flight` — hard cap on staffing predictions
- `hot_stop_min_time` / `hot_stop_max_time` — stop temperature classification bounds

**Tests MUST read thresholds from config, not hardcode them.** Per ENG-4.4, tests that hardcode
thresholds will drift from production behavior as config evolves.

---

## Technology Stack Guidance

For Ground Ops Staffing Analytics products, use these technology avatars:

| Layer | Avatar | Purpose |
|-------|--------|---------|
| **ML / Feature Engineering** | `ml-analytics` (PRIMARY) | scikit-learn, pandas, quantile regression, pytest |
| **Data Ingestion** | `databricks-pyspark` (SECONDARY) | Databricks SQL, ADLS, seasonal query patterns |
| **Notebook Extraction** | `legacy-ml-interop` | Strangler Fig — preserve notebooks, extract to modules |
| **Review Dashboard** (future) | `python-streamlit` | Phase 4 supervisor review dashboard |

---

## Domain Glossary

| Term | Definition |
|------|-----------|
| **ABR** | Airport Baggage Ramp — the ground crew team handling bag delivery |
| **Delivery Type** | `gate`, `bagroom`, `customs`, `preclearance`, `claim`, `transfer` |
| **Pull Time** | Elapsed minutes: flight arrival → first bag delivery scan |
| **IROP** | Irregular Operations — flights disrupted by weather, mechanical, etc. |
| **Run ID** | Unique pipeline execution ID: `{station}_{date}_{time}_{uuid}_{process_type}` |
| **Season** | The historical analysis window (e.g., Summer = June–August) |
| **Process Type** | `mainline` (AA-operated) vs. `regional` (partner-operated) flights |
| **T-Link** | Transfer Link — bags transferring from international to domestic flights |
| **Hot Stop** | Route stop with tight time constraint (`hot_stop_min_time` < min ≤ `hot_stop_max_time`) |
| **Cold Stop** | Route stop with relaxed time constraint (min > `cold_stop_max_time`) |
| **Quantile** | The staffing risk level (e.g., 75th = staffed for 75% of demand scenarios) |
| **Station Config** | YAML file with per-station operational parameters driving all thresholds |

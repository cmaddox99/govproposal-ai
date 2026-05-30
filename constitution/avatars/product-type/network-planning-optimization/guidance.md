# Network Planning & Optimization Product Guidance

Welcome to the American Airlines Network Planning & Optimization product avatar! This guide helps you apply the Hangar AI Constitution to network planning and capacity optimization product decisions.

---

## What We Do

American Airlines Network Planning & Optimization provides data-driven decision support for strategic network design and operational resource allocation. We compete on forecast accuracy, optimization speed, and decision confidence. Our key differentiators are:

- **Accuracy:** Demand forecast precision (target: 85%+ accuracy within 10% MAPE)
- **Speed:** Scenario analysis turnaround (target: <2 hours for network reallocation)
- **Confidence:** Data-driven recommendations with explainable rationale
- **Integration:** Connection to revenue management, operations, and crew scheduling systems

---

## Product Laws for Network Planning

> **Full PRD law definitions** are in the [PRD Laws Reference](../../../docs/guides/avatars/prd-laws-reference.md). This section shows network planning-specific applications.

### 1. PRD-1.1: Continuous Discovery

**Reference:** [PRD-1.1 Full Definition](../../../docs/guides/avatars/prd-laws-reference.md#prd-11-continuous-discovery)

**For Network Planning specifically:**
- Interview network planning analysts about route analysis pain points (monthly)
- Analyze strategic planning cycles and decision-making bottlenecks
- Monitor forecast accuracy vs. actuals (weekly retrospectives)
- Study operational constraints (crew availability, aircraft utilization, gate capacity)

**Example:** We discovered analysts spend 40% of their time manually collecting and cleaning data from multiple sources before they can even start route profitability analysis. If we automate ETL, we unlock 16 hours/week per analyst for higher-value strategic work.

---

### 2. PRD-2.1: User Journey Mapping

**Reference:** [PRD-2.1 Full Definition](../../../docs/guides/avatars/prd-laws-reference.md#prd-21-user-journey-mapping)

**For Network Planning specifically:**
- Map data collection → cleaning → modeling → scenario analysis → recommendation journey
- Identify manual handoffs where errors occur (60% of forecast misses trace to data quality issues)
- Track tool fragmentation (Excel, R scripts, PySpark notebooks, BI dashboards)
- Document collaboration touchpoints (planning ↔ revenue management ↔ operations)

**Example:** Carlos runs route profitability analysis using 5 tools: SQL query (30 min), R script (45 min), Excel pivot (15 min), PowerPoint deck (60 min), email consensus (2 days). We consolidated to single dashboard with automated data refresh—reducing cycle time from 4 days to 2 hours.

---

### 3. PRD-3.1: Roadmap Planning

**Reference:** [PRD-3.1 Full Definition](../../../docs/guides/avatars/prd-laws-reference.md#prd-31-roadmap-planning)

**For Network Planning specifically:**
- Rank features by decision impact: Forecast accuracy (+$10M revenue from better demand prediction), Scenario speed (+$5M from faster reallocation), Data automation (unlocks 40% analyst capacity)
- Evaluate engineering effort: Data pipeline (8 weeks), Forecasting model (12 weeks), Scenario engine (10 weeks)
- Sequence to build foundations: Data pipeline first (Q1 2026, unlocks all downstream work), then forecasting model (Q2 2026), then scenario engine (Q3 2026)
- Align to planning cycles: Launch before Q4 2026 strategic planning window

**Example:** We prioritized data pipeline automation before forecast model improvements because: (a) bad data = bad forecasts regardless of algorithm, (b) analysts spend 40% time on ETL, (c) clean data unlocks model experimentation. Sequence is constraint-driven, not feature-driven.

---

### 4. PRD-4.1: MVP & Product-Market Fit

**Reference:** [PRD-4.1 Full Definition](../../../docs/guides/avatars/prd-laws-reference.md#prd-41-mvp--product-market-fit)

**For Network Planning specifically:**
- Define MVP scope rigorously: In (automated data pipeline, route profitability dashboard, basic scenario comparison) | Out (optimization engine, crew constraints, gate allocation)
- Choose pilot users strategically: 2-3 senior analysts covering different regions (domestic vs. international) and planning horizons (tactical vs. strategic)
- Measure 6-week pilot using decision-quality signals: Time-to-insight <4 hours (vs. 2 days baseline), Forecast accuracy within 10% MAPE, Scenario count 3x increase
- Define decision gates: Time savings >50% + accuracy stable → scale to 10 analysts | Savings 30-50% → iterate 3 weeks | Savings <30% → pivot

**Example:** March 2026 pilot with Lisa (domestic capacity), Marcus (international routes). Results: 1.8 hour time-to-insight (78% reduction), 8.2% MAPE (vs. 9.1% baseline), 5x scenario count. Decision: Scale to full planning team by May, parallel work on optimization engine for Q3 launch.

---

### 5. PRD-5.1: Metrics & Success Definition

**Reference:** [PRD-5.1 Full Definition](../../../docs/guides/avatars/prd-laws-reference.md#prd-51-metrics--success-definition)

**For Network Planning specifically:**
- **Outcome metrics:** Revenue impact from optimized network (+$10M/year target), Forecast accuracy improvement (8% → 6% MAPE), Decision confidence (analyst NPS 40+)
- **Process metrics:** Time-to-insight (4 days → 2 hours), Scenario analysis throughput (1/week → 5/week), Data quality (error rate <2%)
- **Behavior metrics:** Adoption rate (80% of analysts using new tools within 3 months), Feature usage (scenario engine used 2x/week per analyst), Collaboration (cross-functional meetings reduced 30%)

**Example:** We track **outcome** (revenue impact from network changes), **process** (time-to-insight and scenario count), and **behavior** (adoption rate). All three must improve: revenue validates business value, process validates efficiency, behavior validates product-market fit.

---

## Brownfield Modernization Guidance

### Legacy Code Preservation (ENG-10.1)

**Context:** Network planning systems often have legacy R scripts, PySpark pipelines, and Jupyter notebooks with domain-specific forecasting logic built over years.

**Default Policy:**
1. **DO NOT** rewrite R/PySpark to Python without explicit migration approval
2. **Preserve** existing forecasting algorithms and optimization logic
3. **Containerize** legacy models rather than reimplementing algorithms
4. **Validate** side-by-side with output parity tests before replacing production logic

**When to preserve vs. migrate:**
- **Preserve:** Statistical models with validated accuracy, optimization algorithms with proven performance, domain-specific business rules encoded in R/PySpark
- **Migrate (with approval):** Clear accuracy/performance improvements, significant maintenance burden, tech stack consolidation with validated parity
- **Never rewrite without:** Stakeholder signoff, side-by-side validation, regression test suite, rollback plan

**Example:** NP_RAVEN_NCBC repo has R scripts for route profitability forecasting. Default approach:
1. Containerize R scripts with API wrapper (preserve logic)
2. Build Python dashboard that calls R API (no rewrite)
3. Run side-by-side validation for 4 weeks (output parity tests)
4. Only migrate to Python if: (a) accuracy improves OR (b) R maintenance cost > Python migration cost AND (c) stakeholder approval

---

## Technology Stack Guidance

**For Network Planning & Optimization products**, prefer these technology avatars:

- **Data Processing:** `python-pyspark`, `python-pandas`, `legacy-ml-interop` (for R/PySpark preservation)
- **ML/Forecasting:** `azure-ml`, `python-scikit-learn`, `r-statistical-modeling` (brownfield only)
- **Visualization:** `python-streamlit`, `powerbi`, `tableau`
- **APIs:** `python-fastapi`, `azure-functions`
- **Infrastructure:** `azure-databricks`, `azure-synapse`, `docker-containers`

**Brownfield codebases may require:**
- `legacy-ml-interop` for R script containerization and API wrapping
- `python-streamlit` for quick dashboard MVPs that call legacy models
- `docker-containers` for legacy code preservation without rewrites

---

## Related Avatars

- **Product:** `cargo-freight` (similar operational optimization), `loyalty-aadvantage` (similar forecasting/modeling)
- **Technology:** `azure-ml`, `python-fastapi`, `legacy-ml-interop`, `python-streamlit`

---

## Activation

This avatar activates:
- **Skills:** skill-spec-governance (Spec Governance), skill-01 (Research Discovery), skill-06 (Atomic TDD), skill-22 (ML Experiment Tracking), skill-24 (Model Validation), skill-30 (Taxonomy-Governed Enrichment)
- **Workflows:** product-discovery-stage-a-f, workflow-ml-model-development, legacy-rescue-decision-track
- **Laws:** PRD-1.1 (Discovery), PRD-2.1 (Journey Mapping), PRD-4.1 (MVP), ENG-4.1 (Atomic TDD), ENG-10.1 (Brownfield Preservation)

---

## Anti-Patterns to Avoid

❌ **DO NOT use organization names as product types:**
- "ORAA" is an organization, not a product capability → Use "Network Planning & Optimization" instead
- "Data Engineering" is a team function, not a product domain → Use capability-based taxonomy

❌ **DO NOT rewrite legacy R/PySpark without validation:**
- Default to preserve existing forecasting logic with containerization
- Require side-by-side validation and stakeholder approval for algorithm changes
- Never assume "Python is better" without data-driven accuracy/performance proof

❌ **DO NOT build models in isolation:**
- Engage analysts early and continuously (PRD-1.1: Continuous Discovery)
- Validate MVP with pilot users before scaling (PRD-4.1: MVP & Product-Market Fit)
- Track adoption and usage metrics, not just model accuracy (PRD-5.1: Metrics)

---

## Contact & Feedback

For questions about this avatar or brownfield adoption guidance, consult:
- `docs/guides/avatars/product-taxonomy-governance.md` (taxonomy validation)
- `docs/guides/adoption/taxonomy-aligned-avatar-enrichment-workflow.md` (enrichment process)
- `docs/guides/adoption/brownfield-code-preservation.md` (legacy code policy)

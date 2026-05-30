# Network Planning & Optimization Use Case: Route Profitability Analysis

## Business Context

American Airlines Network Planning analysts need to evaluate the profitability of existing domestic routes to identify opportunities for capacity reallocation. Current analysis takes 4 days per route due to manual data collection, cleaning, and R script debugging.

**Goal:** Reduce route profitability analysis time from 4 days to <2 hours while maintaining forecast accuracy.

---

## User Story

**As** Lisa Chen (Network Planning Analyst),  
**I want** to analyze route profitability for DFW→SFO in <2 hours,  
**So that** I can respond quickly to competitive pricing changes and recommend capacity reallocations before revenue loss occurs.

---

## Current Workflow (Baseline)

1. **Data Collection (4 hours):** Manually query Azure Synapse for bookings, revenue, load factor, and operational cost data across 5 tables
2. **Data Cleaning (3 hours):** Fix data quality issues in Excel (missing values, duplicates, currency conversions)
3. **R Script Execution (2 hours):** Run legacy profitability model (often fails due to dependency issues, requires debugging)
4. **Scenario Modeling (1 day):** Manually rerun R script with different capacity assumptions (3 scenarios × 2 hours each)
5. **PowerPoint Report (4 hours):** Create deck with charts and recommendations for leadership review
6. **Collaboration (2 days):** Email thread with revenue management and operations to validate assumptions

**Total Time:** 4 days (including 2 days of async email collaboration)

**Pain Points:**
- Manual ETL consumes 40% of analyst time
- R script errors cause 2-4 hour debugging sessions
- Scenario reruns are sequential (can't parallelize)
- No shared dashboard→collaboration requires PowerPoint decks and email threads

---

## Proposed Workflow (MVP)

1. **Automated Data Pipeline (5 minutes):** Pre-built pipeline pulls and cleans data from Azure Synapse, refreshes hourly
2. **Route Profitability Dashboard (10 minutes):** Streamlit dashboard shows DFW→SFO profitability with 1-click scenario comparison
3. **Legacy R Model Preservation (containerized):** R profitability model runs in Docker container with API wrapper—no Python rewrite required
4. **Scenario Engine (30 minutes):** Analysts adjust capacity assumptions in dashboard, API calls containerized R model, results display in real-time
5. **Shared Dashboard (0 minutes):** Revenue management and operations have live access—no PowerPoint needed
6. **Async Collaboration (4 hours):** Slack thread replaces 2-day email chains, decisions made in 1 business day

**Total Time:** 2 hours for analysis + 4 hours for collaboration = <1 day total

**Success Criteria:**
- Time-to-insight: 4 days → <2 hours (80% reduction)
- Forecast accuracy: 9% MAPE → 9% MAPE (no degradation—R model preserved)
- Scenario throughput: 1/week → 5/week (5x increase)
- Collaboration overhead: 2 days → 4 hours (75% reduction)

---

## Hangar SDD Requirements

### Epic: Automated Route Profitability Analysis

**Acceptance Criteria:**
1. Data pipeline refreshes hourly from Azure Synapse (bookings, revenue, load factor, costs)
2. Streamlit dashboard displays DFW→SFO profitability with 1-click scenario comparison
3. Legacy R model runs in Docker container with API wrapper (no Python rewrite)
4. Scenario engine supports 3 capacity assumptions (baseline, +10%, -10%) with <1 minute response time
5. Dashboard shared with revenue management and operations (role-based access)

**MVP Scope:**
- **In Scope:** Data pipeline, dashboard, containerized R model, scenario engine, shared access
- **Out of Scope:** Optimization engine, crew constraints, gate allocation, mobile app, API for external systems

**Pilot Plan:**
- **Users:** Lisa Chen (domestic routes), Marcus Rodriguez (international routes)
- **Duration:** 6 weeks
- **Routes:** DFW→SFO, DFW→LHR, DFW→ORD (3 routes, varied characteristics)
- **Success Metrics:** Time-to-insight <2 hours, accuracy stable (9% MAPE), scenario count 5x increase, analyst NPS 40+

---

## Technical Architecture

### System Components

1. **Data Pipeline (Azure Databricks):**
   - **Trigger:** Hourly cron job
   - **Source:** Azure Synapse (bookings, revenue, load factor, costs)
   - **Transform:** Data quality checks, currency conversion, aggregation by route
   - **Destination:** Azure SQL Database (cleaned data for dashboard)

2. **Legacy R Model (Docker Container):**
   - **Container:** `network-planning-r-profitability:v1`
   - **API Wrapper:** FastAPI endpoint `/profitability/forecast` (POST request with route, capacity parameters)
   - **Deployment:** Azure Container Instances
   - **Validation:** Side-by-side testing with historical data (output parity vs. existing R script)

3. **Streamlit Dashboard (Python):**
   - **UI:** Route selector, capacity scenario inputs, profitability chart, sensitivity analysis table
   - **Backend:** Calls FastAPI wrapper to containerized R model
   - **Deployment:** Azure App Service
   - **Auth:** Azure AD (role-based access for analysts, revenue management, operations)

4. **Scenario Engine (FastAPI):**
   - **Endpoint:** `/scenarios/compare` (POST request with baseline, +10%, -10% capacity)
   - **Logic:** Calls R model 3 times in parallel, aggregates results
   - **Response Time:** <1 minute for 3 scenarios

---

## Atomic TDD Workflow

### Test-First Development (ENG-4.1)

**Before writing code, write tests:**

1. **Data Pipeline Tests:**
   ```python
   def test_bookings_data_quality():
       # Given: Raw bookings data with missing values
       # When: Data pipeline runs
       # Then: Missing values filled with default logic, no nulls in output
   
   def test_currency_conversion():
       # Given: Revenue in GBP, EUR, JPY
       # When: Pipeline converts to USD
       # Then: Conversion rate matches published rates within 0.1%
   ```

2. **R Model API Tests (Regression):**
   ```python
   def test_r_model_output_parity():
       # Given: Historical route data for DFW→SFO (Q1 2025)
       # When: Containerized R model runs
       # Then: Output matches legacy R script output within 1% error
   
   def test_r_model_response_time():
       # Given: 1 route with 3 scenarios
       # When: API called
       # Then: Response time <1 minute
   ```

3. **Streamlit Dashboard Tests:**
   ```python
   def test_dashboard_displays_profitability():
       # Given: DFW→SFO route selected
       # When: Dashboard loads
       # Then: Profitability chart shows revenue, cost, margin for last 12 months
   
   def test_scenario_comparison():
       # Given: Baseline, +10%, -10% capacity scenarios
       # When: Analyst clicks "Compare Scenarios"
       # Then: Table shows revenue, cost, margin for all 3 scenarios
   ```

**RED-GREEN-REFACTOR:**
- **RED:** Write failing test (data pipeline returns nulls)
- **GREEN:** Implement minimal code to pass test (fill nulls with default logic)
- **REFACTOR:** Clean up code (extract null-filling logic to reusable function)

---

## Brownfield Preservation Strategy

### DO NOT Rewrite R Model

**Rationale:**
- Legacy R profitability model has 5+ years of domain logic, validated accuracy (9% MAPE)
- Rewriting to Python risks introducing bugs, degrading accuracy, and delaying MVP by 8+ weeks
- Analysts trust existing model—migration requires stakeholder validation and signoff

**Preservation Approach:**
1. **Containerize R Script:** Wrap existing R code in Docker container with Rscript entrypoint
2. **API Wrapper:** Build FastAPI endpoint that calls containerized R script via subprocess
3. **Validation:** Run side-by-side tests with historical data (output parity within 1% error)
4. **Deployment:** Deploy container to Azure Container Instances (no Python rewrite)

**Migration Decision Gate:**
- **Preserve:** If R model accuracy is stable (9% MAPE) and container performs well (<1 minute response time)
- **Migrate:** Only if Python model demonstrates 10%+ accuracy improvement (e.g., 9% → 8% MAPE) AND stakeholder approval

**Example Dockerfile:**
```dockerfile
FROM rocker/r-ver:4.3.0
RUN R -e "install.packages(c('dplyr', 'forecast', 'jsonlite'))"
COPY profitability_model.R /app/
WORKDIR /app
CMD ["Rscript", "profitability_model.R"]
```

---

## Launch Plan

### Pilot Phase (6 weeks)

**Week 1-2:** Build data pipeline, containerize R model, deploy FastAPI wrapper  
**Week 3-4:** Build Streamlit dashboard, integrate with R API, add scenario engine  
**Week 5:** Pilot with Lisa (DFW→SFO), Marcus (DFW→LHR) - collect usage metrics  
**Week 6:** Retrospective, validate success criteria, decide on scale vs. iterate

**Success Criteria:**
- ✅ Time-to-insight <2 hours (vs. 4 days baseline)
- ✅ Forecast accuracy 9% MAPE (no degradation from R model preservation)
- ✅ Scenario throughput 5x increase (5 scenarios/week vs. 1/week baseline)
- ✅ Analyst NPS 40+ (vs. 30 baseline)

**Scale Decision:**
- **If 3/4 criteria met:** Scale to full planning team (10 analysts), parallel work on optimization engine
- **If 2/4 criteria met:** Iterate 3 weeks, focus on bottlenecks (e.g., dashboard UX, scenario engine speed)
- **If <2/4 criteria met:** Pivot to different approach (e.g., Power BI dashboard instead of Streamlit)

---

## Related Assets

- **Avatar:** `avatars/product-type/network-planning-optimization/`
- **Skills:** skill-spec-governance (Spec Governance), skill-06 (Atomic TDD), skill-22 (ML Experiment Tracking), skill-30 (Taxonomy-Governed Enrichment)
- **Workflows:** `product-discovery-stage-a-f`, `legacy-rescue-decision-track`
- **Guides:** `docs/guides/adoption/brownfield-code-preservation.md`, `docs/guides/adoption/taxonomy-aligned-avatar-enrichment-workflow.md`

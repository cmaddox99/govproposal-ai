# Brownfield Code Preservation Policy

**Purpose:** Establish default-preserve strategy for legacy ML code (R, PySpark, Jupyter notebooks) during Constitution adoption.

**Time to Read:** 15 minutes

---

## Constitutional Authority

This guide implements requirements from the **hangar-ai-constitution**:

### Laws Implemented

| Law ID | Title | How This Guide Implements It |
|--------|-------|------------------------------|
| **ENG-10.1** | Brownfield Code Preservation | Default to preserve with containerization, not rewrite |
| **ENG-4.1** | Atomic TDD Law | Regression tests validate output parity with legacy code |
| **ENG-2.2** | Layered Architecture Law | Separate presentation, API, and legacy execution layers |
| **ENG-6.5** | Input Validation Law | Validate at API boundary before passing to legacy models |
| **BUS-7.1** | Audit Trail Law | Log inputs, outputs, execution time for legacy model calls |

### Skills Invoked

| Skill | Purpose | Primary Laws |
|-------|---------|-------------|
| **skill-30-taxonomy-governed-avatar-enrichment** | Ensure brownfield enrichment follows taxonomy | PRD-3.1, BUS-1.1 |
| **skill-06-atomic-tdd** | Write regression tests for legacy code preservation | ENG-4.1, ENG-4.4 |

### Technology Avatars Activated

| Avatar | Purpose | When to Use |
|--------|---------|-------------|
| **legacy-ml-interop** | R/PySpark containerization, API wrappers, regression testing | Default for all legacy ML code |
| **python-streamlit** | UI layer for legacy models (no rewrite required) | MVP dashboards calling legacy APIs |
| **python-fastapi** | API wrappers for containerized legacy models | Bridge between UI and legacy execution |

---

## Philosophy: Preserve, Don't Rewrite

**Default Strategy:** Containerize legacy code and wrap with APIs—do NOT rewrite to Python without validation.

### Why Preserve?

1. **Risk Mitigation:** Rewriting introduces bugs, degrades accuracy, breaks domain logic
2. **Speed:** Containerization takes 1-2 weeks, rewriting takes 8-12 weeks
3. **Trust:** Analysts and stakeholders trust existing models
4. **Modernization:** Update infrastructure and UI without changing logic

### When to Migrate (with approval only)?

1. **Accuracy:** New model demonstrates 10%+ accuracy improvement (validated with side-by-side tests)
2. **Performance:** New model demonstrates 50%+ speed improvement (validated with benchmarks)
3. **Maintainability:** Legacy code is unmaintainable (broken dependencies, no documentation, technical debt > migration cost)
4. **Approval:** Stakeholder signoff with validated parity tests and rollback plan

### Never Migrate Without:

1. Stakeholder approval from model owners and users
2. Side-by-side validation tests (output parity within 1% tolerance)
3. Regression test suite covering critical use cases
4. Rollback plan (keep containerized legacy model deployable)

---

## Architecture: Layered Integration (ENG-2.2)

**Separate presentation, API layer, and legacy model execution:**

```
[Streamlit Dashboard] → [FastAPI Wrapper] → [Docker Container: R/PySpark Model]
   (Presentation)          (API Layer)         (Legacy Execution)
```

**Layers:**
1. **Presentation:** Streamlit dashboard, React UI, Power BI (user-facing)
2. **API Layer:** FastAPI endpoints with Pydantic validation (integration boundary)
3. **Legacy Execution:** Docker container with R/PySpark code preserved (domain logic)

**Key Principle:** No direct calls to legacy code from presentation layer—API layer is the integration boundary.

---

## Preservation Strategies by Technology

### R Scripts (Statistical Models)

**Context:** Legacy R scripts for forecasting, profitability analysis, optimization

**Preservation Approach:**
1. **Containerize R Script:** Wrap existing R code in Docker container with Rscript entrypoint
2. **API Wrapper:** Build FastAPI endpoint that calls containerized R script via subprocess
3. **Validation:** Run side-by-side tests with historical data (output parity within 1% error)
4. **Deployment:** Deploy container to Azure Container Instances (no Python rewrite)

**Example Dockerfile:**
```dockerfile
FROM rocker/r-ver:4.3.0
RUN R -e "install.packages(c('dplyr', 'forecast', 'jsonlite'))"
COPY profitability_model.R /app/
WORKDIR /app
CMD ["Rscript", "profitability_model.R"]
```

**Example FastAPI Wrapper:**
```python
from fastapi import APIRouter, HTTPException
import subprocess
import json

@router.post("/profitability/forecast")
def forecast(route: str):
    result = subprocess.run(
        ["docker", "run", "--rm", "r-profitability:v1", route],
        capture_output=True,
        text=True,
        timeout=60
    )
    if result.returncode != 0:
        raise HTTPException(status_code=500, detail=f"R model failed: {result.stderr}")
    return json.loads(result.stdout)
```

### PySpark Pipelines (Large-Scale Data Processing)

**Context:** Legacy PySpark jobs for network optimization, capacity allocation

**Preservation Approach:**
1. **Containerize PySpark Job:** Use pyspark base image, copy scripts, set spark-submit entrypoint
2. **API Wrapper:** Build FastAPI endpoint that triggers PySpark job via subprocess or HTTP
3. **Validation:** Add unit tests for PySpark transformations, regression tests for end-to-end outputs
4. **Deployment:** Deploy to Azure Databricks or Azure Container Instances

**Example Dockerfile:**
```dockerfile
FROM bitnami/spark:3.5
COPY optimize_network.py /app/
COPY routes.csv /app/
WORKDIR /app
ENTRYPOINT ["spark-submit", "optimize_network.py"]
```

**Example FastAPI Wrapper:**
```python
@router.post("/optimization/optimize")
def optimize_network():
    result = subprocess.run(
        ["docker", "run", "--rm", "-v", "$(pwd)/data:/app/data", "pyspark-optimization:v1"],
        capture_output=True,
        text=True,
        timeout=600  # 10 minutes
    )
    if result.returncode != 0:
        raise HTTPException(status_code=500, detail=f"PySpark job failed: {result.stderr}")
    return {"status": "success", "output": result.stdout}
```

### Jupyter Notebooks (Ad-Hoc Analysis)

**Context:** Jupyter notebooks for exploratory analysis, prototyping, one-off reports

**Preservation Approach:**
1. **Extract Reusable Logic:** Move reusable functions to tested Python modules (`domain/`, `clients/`)
2. **Keep Notebooks for Exploration:** Retain notebooks for ad-hoc analysis, not production
3. **Containerize if Needed:** If notebook has production logic, extract to module and containerize
4. **Test Extracted Modules:** Write unit tests for extracted functions (ENG-4.1)

**Before (notebook):**
```python
# notebook cell 1: Load data
import pandas as pd
data = pd.read_csv("route_data.csv")

# notebook cell 2: Calculate profitability
data["margin"] = data["revenue"] - data["cost"]

# notebook cell 3: Visualize
import matplotlib.pyplot as plt
plt.bar(data["route"], data["margin"])
```

**After (tested module + notebook):**
```python
# domain/profitability.py (TESTED)
import pandas as pd

def calculate_margin(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate profit margin for each route."""
    data = data.copy()
    data["margin"] = data["revenue"] - data["cost"]
    return data

# tests/test_profitability.py
def test_calculate_margin():
    data = pd.DataFrame({"route": ["DFW→SFO"], "revenue": [1_000_000], "cost": [600_000]})
    result = calculate_margin(data)
    assert result["margin"].iloc[0] == 400_000

# notebook.ipynb (ad-hoc exploration)
from domain.profitability import calculate_margin
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("route_data.csv")
data = calculate_margin(data)  # Call tested module
plt.bar(data["route"], data["margin"])
```

---

## Regression Testing Strategy (ENG-4.1)

**For brownfield code, prioritize regression tests before adding new features.**

### Regression Test Checklist

1. **Identify Critical Logic:** Route profitability calculations, demand forecasting models, optimization algorithms
2. **Capture Current Behavior:** Run legacy code with historical data, record outputs
3. **Write Regression Tests:** Assert new code produces identical outputs (within 1% tolerance for floating-point)
4. **Add Unit Tests:** Write tests for new features (RED-GREEN-REFACTOR)

### Example: Testing Containerized R Model

```python
def test_r_profitability_model_output_parity():
    """
    Regression test: Containerized R model should match legacy R script output.
    """
    # Given: Historical route data for DFW→SFO (Q1 2025)
    input_data = load_historical_data("DFW_SFO_Q1_2025.csv")
    
    # When: Call containerized R model via API
    response = requests.post("http://api/profitability/forecast", json=input_data)
    container_output = response.json()
    
    # Then: Output matches legacy R script within 1% error
    legacy_output = load_legacy_output("DFW_SFO_Q1_2025_expected.json")
    assert abs(container_output["revenue"] - legacy_output["revenue"]) / legacy_output["revenue"] < 0.01
    assert abs(container_output["margin"] - legacy_output["margin"]) / legacy_output["margin"] < 0.01
```

### Baseline Capture Process

1. **Before Containerization:** Run legacy R/PySpark code with historical data (last 6-12 months)
2. **Save Outputs:** Store outputs to `baselines/{component}_{scenario}_expected.json`
3. **Document Assumptions:** Record input data, parameters, environment (R version, package versions)
4. **Version Control:** Commit baselines to Git for repeatability

---

## Decision Framework: Preserve vs. Migrate

### Preserve (default)

**When:**
- Legacy model has validated accuracy (e.g., 9% MAPE, stakeholder trust)
- Domain logic is complex and poorly documented (rewrite risk high)
- Time-to-market is critical (containerization = 1-2 weeks vs. rewrite = 8-12 weeks)
- No clear accuracy/performance improvement from migration

**How:**
- Containerize R/PySpark code with Docker
- Wrap with FastAPI endpoints (Pydantic validation)
- Write regression tests validating output parity (within 1% tolerance)
- Deploy to Azure Container Instances or Databricks

**Example:** NP_RAVEN_NCBC repo has R scripts for route profitability forecasting with 5+ years of validated accuracy. Default approach:
1. Containerize R scripts with API wrapper (preserve logic)
2. Build Streamlit dashboard that calls R API (no rewrite)
3. Run side-by-side validation for 4 weeks (output parity tests)
4. Only migrate to Python if: (a) accuracy improves 10%+ OR (b) R maintenance cost > Python migration cost AND (c) stakeholder approval

### Migrate (with approval)

**When:**
- **Accuracy Improvement:** New Python model demonstrates 10%+ accuracy improvement (e.g., 9% MAPE → 8% MAPE)
- **Performance Improvement:** New Python model runs 50%+ faster (e.g., 6 hours → 3 hours)
- **Maintenance Cost:** Legacy code is unmaintainable (broken dependencies, no documentation, tech debt > migration cost)
- **Stakeholder Approval:** Model owners, users, and operations approve migration with validated parity tests

**How:**
1. **Build New Model:** Implement Python equivalent with same inputs/outputs
2. **Side-by-Side Validation:** Run both models with historical data, validate output parity within 1% tolerance
3. **Shadow Deployment:** Deploy new model in shadow mode (no production traffic), compare outputs with legacy model
4. **Gradual Rollout:** Route 1% → 10% → 50% → 100% of traffic to new model, monitor accuracy metrics
5. **Rollback Plan:** Keep containerized legacy model deployable for 3-6 months

**Example:** NP_RAVEN_NCBC forecasting model migration decision:
- **Hypothesis:** Python XGBoost model improves accuracy from 9% MAPE to 7.5% MAPE
- **Validation:** Run side-by-side with 12 months of historical data
- **Result:** XGBoost achieves 7.8% MAPE (13% accuracy improvement)
- **Decision:** Stakeholder approval obtained, gradual rollout with 4-week shadow deployment
- **Rollback:** Containerized R model kept deployable for 6 months

### Never Migrate Without

1. **Stakeholder Signoff:** Model owners, users, operations approve migration
2. **Side-by-Side Validation:** Output parity within 1% tolerance for critical use cases
3. **Regression Test Suite:** 90%+ coverage of legacy logic with regression tests
4. **Rollback Plan:** Containerized legacy model deployable for 3-6 months
5. **Documentation:** Migration decision captured in Hangar SDD proposal with rationale

---

## Integration with RAG and Avatar System

**This guide is RAG-retrievable through multiple paths:**

1. **Product Avatar:** `avatars/product-type/network-planning-optimization/ADOPTION.md` → Links to this guide
2. **Technology Avatar:** `avatars/technology/legacy-ml-interop/guidance.md` → References this policy
3. **Skill:** `agent-skills/skills-by-domain/discovery-research/30-taxonomy-governed-avatar-enrichment.md` → Cites this guide
4. **Workflow:** `docs/guides/adoption/taxonomy-aligned-avatar-enrichment-workflow.md` → Step 7 validation uses this guide

**RAG Triggers for AI Agents:**
- "How to preserve legacy R models?" → Load this guide + `legacy-ml-interop` avatar
- "Brownfield adoption for PySpark?" → Load this guide + `network-planning-optimization` avatar
- "When to rewrite vs containerize?" → Load decision framework section
- "Regression testing for legacy models?" → Load regression testing strategy section

---

## Anti-Patterns to Avoid

❌ **DO NOT rewrite without validation**
- **Wrong:** "Python is better, let's rewrite all R code"
- **Right:** "Preserve R code with containerization, only migrate if Python demonstrates 10%+ accuracy improvement with stakeholder approval"

❌ **DO NOT call legacy code directly from UI**
- **Wrong:** `subprocess.run(["Rscript", "model.R"])` in Streamlit app.py
- **Right:** API layer (FastAPI) between UI and legacy models

❌ **DO NOT skip regression tests**
- **Wrong:** "Trust gut feeling that containerized model works"
- **Right:** Write regression tests with historical data, validate output parity within 1% tolerance

❌ **DO NOT assume Python is superior**
- **Wrong:** "Python is more popular, so it's better"
- **Right:** Validate with data (accuracy, performance, maintainability) before migrating

---

## Related Assets

- **Product Avatar:** `avatars/product-type/network-planning-optimization/`
- **Technology Avatars:** `avatars/technology/legacy-ml-interop/`, `avatars/technology/python-streamlit/`
- **Skill:** `agent-skills/skills-by-domain/discovery-research/30-taxonomy-governed-avatar-enrichment.md`
- **Workflow:** `docs/guides/adoption/taxonomy-aligned-avatar-enrichment-workflow.md`
- **Taxonomy Governance:** `docs/guides/avatars/product-taxonomy-governance.md`

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-20 | Initial creation for ORAA brownfield enrichment governance |

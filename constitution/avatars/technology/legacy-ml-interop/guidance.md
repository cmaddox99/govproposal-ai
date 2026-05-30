# Legacy ML Interoperability Technical Guidance

Welcome to the Legacy ML Interoperability technology avatar! This guide helps you preserve and modernize legacy R, PySpark, and Jupyter notebook-based ML systems following the Hangar AI Constitution.

---

## Philosophy: Preserve, Don't Rewrite

**Default Strategy:** Containerize legacy code and wrap with APIs—do NOT rewrite to Python without validation.

**Why Preserve:**
- **Risk Mitigation:** Rewriting introduces bugs, degrades accuracy, breaks domain logic
- **Speed:** Containerization takes 1-2 weeks, rewriting takes 8-12 weeks
- **Trust:** Analysts and stakeholders trust existing models
- **Modernization:** Update infrastructure and UI without changing logic

**When to Migrate:**
- **Accuracy:** New model demonstrates 10%+ accuracy improvement (validated with side-by-side tests)
- **Performance:** New model demonstrates 50%+ speed improvement (validated with benchmarks)
- **Maintainability:** Legacy code is unmaintainable (broken dependencies, no documentation)
- **Approval:** Stakeholder signoff with validated parity tests and rollback plan

---

## Architecture: Layered Integration (ENG-2.2)

**Separate presentation, API layer, and legacy model execution:**

```
[Streamlit Dashboard] → [FastAPI Wrapper] → [Docker Container: R Model]
```

**Layers:**
1. **Presentation:** Streamlit dashboard, React UI, Power BI (user-facing)
2. **API Layer:** FastAPI endpoints with Pydantic validation (integration boundary)
3. **Legacy Execution:** Docker container with R/PySpark code preserved (domain logic)

**Key Principle:** No direct calls to legacy code from presentation layer—API layer is the integration boundary.

---

## Containerizing Legacy R Models

### Example: R Route Profitability Model

**Original R Script (`profitability_model.R`):**
```r
# profitability_model.R
library(dplyr)
library(forecast)
library(jsonlite)

# Read input from command-line args
args <- commandArgs(trailingOnly = TRUE)
route <- args[1]

# Load data and run profitability model
data <- read.csv("route_data.csv") %>% filter(Route == route)
revenue <- sum(data$Revenue)
cost <- sum(data$Cost)
margin <- revenue - cost

# Output JSON
output <- list(route = route, revenue = revenue, cost = cost, margin = margin)
cat(toJSON(output))
```

**Dockerfile (`docker/r-profitability/Dockerfile`):**
```dockerfile
FROM rocker/r-ver:4.3.0

# Install R packages
RUN R -e "install.packages(c('dplyr', 'forecast', 'jsonlite'), repos='http://cran.rstudio.com/')"

# Copy R script and data
COPY profitability_model.R /app/
COPY route_data.csv /app/
WORKDIR /app

# Entrypoint: Rscript
ENTRYPOINT ["Rscript", "profitability_model.R"]
```

**Build and Test:**
```bash
# Build container
docker build -t network-planning-r-profitability:v1 -f docker/r-profitability/Dockerfile .

# Test container
docker run network-planning-r-profitability:v1 "DFW→SFO"
# Output: {"route":"DFW→SFO","revenue":1000000,"cost":600000,"margin":400000}
```

---

## FastAPI Wrapper for Legacy Models

**API Wrapper (`api/routers/profitability.py`):**
```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import subprocess
import json

router = APIRouter(prefix="/profitability", tags=["profitability"])

class ForecastRequest(BaseModel):
    route: str = Field(..., example="DFW→SFO", pattern="^[A-Z]{3}→[A-Z]{3}$")

class ForecastResponse(BaseModel):
    route: str
    revenue: float
    cost: float
    margin: float

@router.post("/forecast", response_model=ForecastResponse)
def forecast(request: ForecastRequest):
    """
    Call containerized R profitability model.
    """
    try:
        # Call Docker container with route parameter
        result = subprocess.run(
            ["docker", "run", "--rm", "network-planning-r-profitability:v1", request.route],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=f"R model failed: {result.stderr}")
        
        # Parse JSON output from R script
        data = json.loads(result.stdout)
        return ForecastResponse(**data)
    
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="R model timed out (>60s)")
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Invalid R model output: {e}")
```

**Key Practices:**
- **Input Validation:** Pydantic validates route format before passing to R model
- **Error Handling:** Catch subprocess errors, return user-friendly HTTP errors
- **Timeout:** Prevent hanging (60s timeout)
- **Logging:** Log inputs, outputs, execution time for debugging

---

## Regression Testing (ENG-4.1)

**Write tests to validate containerized model produces identical outputs to legacy code.**

**Regression Test (`tests/test_r_model_regression.py`):**
```python
import pytest
import requests
import json

@pytest.fixture
def api_client():
    return "http://localhost:8000"

def test_r_profitability_model_output_parity(api_client):
    """
    Regression test: Containerized R model should match legacy R script output.
    """
    # Given: Historical route data for DFW→SFO (Q1 2025)
    # Expected output from legacy R script (baseline)
    expected = {
        "route": "DFW→SFO",
        "revenue": 1_000_000,
        "cost": 600_000,
        "margin": 400_000
    }
    
    # When: Call FastAPI wrapper
    response = requests.post(f"{api_client}/profitability/forecast", json={"route": "DFW→SFO"})
    assert response.status_code == 200
    
    actual = response.json()
    
    # Then: Output matches legacy R script within 1% tolerance
    assert actual["route"] == expected["route"]
    assert abs(actual["revenue"] - expected["revenue"]) / expected["revenue"] < 0.01
    assert abs(actual["cost"] - expected["cost"]) / expected["cost"] < 0.01
    assert abs(actual["margin"] - expected["margin"]) / expected["margin"] < 0.01

def test_r_model_performance(api_client):
    """
    Performance test: Containerized R model should respond in <60s.
    """
    import time
    
    # When: Call FastAPI wrapper
    start = time.time()
    response = requests.post(f"{api_client}/profitability/forecast", json={"route": "DFW→SFO"})
    elapsed = time.time() - start
    
    # Then: Response time <60s
    assert response.status_code == 200
    assert elapsed < 60
```

**Baseline Capture (before containerization):**
1. Run legacy R script with historical data: `Rscript profitability_model.R "DFW→SFO"`
2. Save output to `baselines/DFW_SFO_Q1_2025_expected.json`
3. Write regression test that asserts containerized model matches baseline

---

## Streamlit Dashboard Integration

**Streamlit Dashboard Calling Containerized R Model:**

```python
# app.py
import streamlit as st
from clients.profitability_client import ProfitabilityClient

st.title("Route Profitability Analysis")

# User input
route = st.selectbox("Route", ["DFW→SFO", "DFW→LHR", "DFW→ORD"])

# Call API wrapper (which calls containerized R model)
if st.button("Analyze"):
    client = ProfitabilityClient("http://api:8000")
    data = client.get_forecast(route)
    
    # Display results
    st.metric("Revenue", f"${data['revenue']:,.0f}")
    st.metric("Cost", f"${data['cost']:,.0f}")
    st.metric("Margin", f"${data['margin']:,.0f}")
```

**Python API Client (`clients/profitability_client.py`):**
```python
import requests
from typing import Dict

class ProfitabilityClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
    
    def get_forecast(self, route: str) -> Dict:
        """Fetch profitability forecast from API."""
        response = requests.post(
            f"{self.base_url}/profitability/forecast",
            json={"route": route},
            timeout=60
        )
        response.raise_for_status()
        return response.json()
```

---

## PySpark Containerization

**Example: PySpark Network Optimization Pipeline**

**Original PySpark Script (`optimize_network.py`):**
```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("NetworkOptimization").getOrCreate()

# Load data
routes = spark.read.csv("routes.csv", header=True, inferSchema=True)

# Optimization logic
optimized = routes.filter(routes["load_factor"] < 0.7)

# Save results
optimized.write.csv("optimized_routes.csv", header=True, mode="overwrite")
```

**Dockerfile (`docker/pyspark-optimization/Dockerfile`):**
```dockerfile
FROM bitnami/spark:3.5

# Copy PySpark script and data
COPY optimize_network.py /app/
COPY routes.csv /app/
WORKDIR /app

# Entrypoint: spark-submit
ENTRYPOINT ["spark-submit", "optimize_network.py"]
```

**FastAPI Wrapper (`api/routers/optimization.py`):**
```python
from fastapi import APIRouter, HTTPException
import subprocess

router = APIRouter(prefix="/optimization", tags=["optimization"])

@router.post("/optimize")
def optimize_network():
    """
    Run PySpark network optimization job in Docker container.
    """
    try:
        result = subprocess.run(
            ["docker", "run", "--rm", "-v", "$(pwd)/data:/app/data", "pyspark-optimization:v1"],
            capture_output=True,
            text=True,
            timeout=600  # 10 minutes
        )
        
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=f"PySpark job failed: {result.stderr}")
        
        return {"status": "success", "output": result.stdout}
    
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="PySpark job timed out (>10 minutes)")
```

---

## Jupyter Notebook Extraction

**Challenge:** Jupyter notebooks are good for exploration, bad for production (no tests, no version control, no CI/CD).

**Solution:** Extract reusable logic to tested Python modules, keep notebooks for ad-hoc analysis.

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

**After (tested module):**
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
    # Given: route data
    data = pd.DataFrame({
        "route": ["DFW→SFO"],
        "revenue": [1_000_000],
        "cost": [600_000]
    })
    
    # When: calculate margin
    result = calculate_margin(data)
    
    # Then: margin is correct
    assert result["margin"].iloc[0] == 400_000
```

**Notebook (ad-hoc analysis only):**
```python
# notebook.ipynb
from domain.profitability import calculate_margin
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("route_data.csv")
data = calculate_margin(data)  # Call tested module
plt.bar(data["route"], data["margin"])
```

---

## Input Validation (ENG-6.5)

**Validate inputs at API boundary before passing to legacy models:**

```python
from pydantic import BaseModel, Field, validator

class ForecastRequest(BaseModel):
    route: str = Field(..., example="DFW→SFO", pattern="^[A-Z]{3}→[A-Z]{3}$")
    capacity_pct: float = Field(0, ge=-50, le=50, description="Capacity adjustment (-50% to +50%)")
    
    @validator("route")
    def validate_route(cls, v):
        """Validate route format."""
        parts = v.split("→")
        if len(parts) != 2 or len(parts[0]) != 3 or len(parts[1]) != 3:
            raise ValueError("Route must be in format 'XXX→YYY' (e.g., 'DFW→SFO')")
        return v
```

**Why validate:**
- Prevent injection attacks (malformed inputs passed to subprocess)
- Catch errors early (before calling expensive legacy models)
- Improve UX (user-friendly error messages instead of cryptic R errors)

---

## Decision Framework: Preserve vs. Migrate

**Preserve (default):**
- Legacy model has validated accuracy (e.g., 9% MAPE, stakeholder trust)
- Domain logic is complex and poorly documented
- Time-to-market is critical (containerization = 1-2 weeks vs. rewrite = 8-12 weeks)
- No clear accuracy/performance improvement from migration

**Migrate (with approval):**
- New model demonstrates 10%+ accuracy improvement (validated with side-by-side tests)
- New model demonstrates 50%+ performance improvement (validated with benchmarks)
- Legacy code is unmaintainable (broken dependencies, no documentation)
- Stakeholder signoff with validated parity tests and rollback plan

**Never migrate without:**
1. Stakeholder approval from model owners and users
2. Side-by-side validation tests (output parity within 1% tolerance)
3. Regression test suite covering critical use cases
4. Rollback plan (keep containerized legacy model deployable)

---

## Anti-Patterns to Avoid

❌ **DO NOT rewrite without validation**
- **Wrong:** "Python is better, let's rewrite all R code"
- **Right:** "Preserve R code with containerization, only migrate if Python demonstrates 10%+ accuracy improvement"

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

## Related Avatars

- **Technology:** `python-fastapi` (API wrappers), `python-streamlit` (UI layer), `python-pyspark` (data processing)
- **Product:** `network-planning-optimization`, `cargo-freight`

---

## Activation

This avatar activates:
- **Skills:** skill-06 (Atomic TDD), skill-07 (Vertical Slice), skill-30 (Taxonomy-Governed Enrichment)
- **Workflows:** legacy-rescue-decision-track, product-discovery-stage-a-f
- **Laws:** ENG-10.1 (Brownfield Preservation), ENG-4.1 (Atomic TDD Regression), ENG-2.2 (Layered Architecture), ENG-6.5 (Input Validation)

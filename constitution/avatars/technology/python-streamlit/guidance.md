# Python/Streamlit Technical Guidance

Welcome to the Python/Streamlit technology avatar! This guide helps you build maintainable, testable Streamlit dashboards following the Hangar AI Constitution.

---

## What Streamlit Is Good For

Streamlit is a Python framework for building interactive data dashboards quickly. Use it for:

- **MVP Dashboards:** Rapid prototyping for internal analysts and planners (days instead of weeks)
- **Brownfield Integration:** UI layer for legacy R/PySpark models (no rewrite required)
- **Interactive Analysis:** Scenario modeling, what-if analysis, data exploration
- **Proof-of-Concept:** Validate features before building production web apps

**NOT good for:**
- Production systems with high concurrency (use FastAPI + React instead)
- Complex multi-user workflows (no role-based access control out-of-box)
- Real-time data streaming (limited WebSocket support)

---

## Architecture: Layered Design (ENG-2.2)

**Separate presentation, business logic, and data access:**

```
streamlit_app/
  app.py                    # Presentation: Streamlit widgets, charts, layout
  pages/                    # Multi-page app
    01_route_analysis.py
    02_scenario_comparison.py
  domain/                   # Business Logic: data transformations, calculations (TESTED)
    profitability.py
    scenarios.py
  clients/                  # Data Access: API clients, database queries (TESTED)
    profitability_api.py
  tests/
    test_profitability.py
    test_scenarios.py
    test_api_client.py
```

**Key Principle:** Business logic and data access must be testable—extract them from `app.py`.

---

## Atomic TDD for Streamlit (ENG-4.1)

**Challenge:** Streamlit UI is hard to test directly (requires selenium for end-to-end tests).

**Solution:** Test business logic and API clients with pytest, keep UI thin.

### Example: Route Profitability Dashboard

**BAD (untestable):**
```python
# app.py
import streamlit as st
import requests

st.title("Route Profitability Analysis")
route = st.selectbox("Route", ["DFW→SFO", "DFW→LHR"])

# Business logic mixed with UI—hard to test
response = requests.post("http://api/profitability/forecast", json={"route": route})
data = response.json()
revenue = data["revenue"]
margin = revenue - data["cost"]

st.metric("Profit Margin", f"${margin:,.0f}")
```

**GOOD (testable):**
```python
# domain/profitability.py (TESTED)
def calculate_margin(revenue: float, cost: float) -> float:
    """Calculate profit margin."""
    return revenue - cost

# clients/profitability_api.py (TESTED)
import requests

class ProfitabilityClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
    
    def get_forecast(self, route: str) -> dict:
        """Fetch profitability forecast from API."""
        response = requests.post(f"{self.base_url}/forecast", json={"route": route})
        response.raise_for_status()
        return response.json()

# app.py (THIN)
import streamlit as st
from domain.profitability import calculate_margin
from clients.profitability_api import ProfitabilityClient

st.title("Route Profitability Analysis")
route = st.selectbox("Route", ["DFW→SFO", "DFW→LHR"])

client = ProfitabilityClient("http://api")
data = client.get_forecast(route)
margin = calculate_margin(data["revenue"], data["cost"])

st.metric("Profit Margin", f"${margin:,.0f}")
```

**Tests:**
```python
# tests/test_profitability.py
from domain.profitability import calculate_margin

def test_calculate_margin():
    # Given: revenue and cost
    revenue = 1_000_000
    cost = 600_000
    
    # When: calculate margin
    margin = calculate_margin(revenue, cost)
    
    # Then: margin is correct
    assert margin == 400_000

# tests/test_api_client.py
from clients.profitability_api import ProfitabilityClient
from unittest.mock import Mock

def test_get_forecast(requests_mock):
    # Given: API returns forecast data
    requests_mock.post("http://api/forecast", json={"revenue": 1_000_000, "cost": 600_000})
    
    # When: client fetches forecast
    client = ProfitabilityClient("http://api")
    data = client.get_forecast("DFW→SFO")
    
    # Then: data is parsed correctly
    assert data["revenue"] == 1_000_000
    assert data["cost"] == 600_000
```

**RED-GREEN-REFACTOR:**
1. **RED:** Write failing test for `calculate_margin`
2. **GREEN:** Implement `calculate_margin` to pass test
3. **REFACTOR:** Extract API client, test with mock

---

## Complexity Limits (ENG-3.1)

**Goal:** Keep functions simple (cyclomatic complexity ≤10).

**BAD (complex callback):**
```python
# app.py
def on_scenario_change():
    if scenario == "Baseline":
        if route == "DFW→SFO":
            if capacity_adjustment > 0:
                data = fetch_data("DFW→SFO", "high")
            else:
                data = fetch_data("DFW→SFO", "low")
        else:
            data = fetch_data(route, "baseline")
    elif scenario == "+10%":
        data = fetch_data(route, "high")
    # ... 20 more lines
```

**GOOD (extract to helper):**
```python
# domain/scenarios.py (TESTED)
def determine_scenario_config(route: str, scenario: str, capacity_adjustment: int) -> dict:
    """Determine API parameters for scenario."""
    if scenario == "Baseline":
        return {"route": route, "capacity": "baseline"}
    elif scenario == "+10%":
        return {"route": route, "capacity": "high"}
    elif scenario == "-10%":
        return {"route": route, "capacity": "low"}

# app.py (SIMPLE)
def on_scenario_change():
    config = determine_scenario_config(route, scenario, capacity_adjustment)
    data = fetch_data(**config)
```

---

## Brownfield Integration (ENG-10.1)

**Use Case:** Build Streamlit dashboard that calls legacy R model via API wrapper.

**Architecture:**
```
[Streamlit Dashboard] → [FastAPI Wrapper] → [Containerized R Model]
```

**Example: Route Profitability with Legacy R Model**

**1. Containerize R Model (preserve logic):**
```dockerfile
# Dockerfile
FROM rocker/r-ver:4.3.0
RUN R -e "install.packages(c('dplyr', 'forecast', 'jsonlite'))"
COPY profitability_model.R /app/
WORKDIR /app
CMD ["Rscript", "profitability_model.R"]
```

**2. FastAPI Wrapper:**
```python
# api/main.py
from fastapi import FastAPI
import subprocess
import json

app = FastAPI()

@app.post("/profitability/forecast")
def forecast(route: str):
    # Call containerized R model
    result = subprocess.run(
        ["Rscript", "profitability_model.R", route],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)
```

**3. Streamlit Dashboard (presentation layer):**
```python
# app.py
import streamlit as st
from clients.profitability_api import ProfitabilityClient

st.title("Route Profitability Analysis")
route = st.selectbox("Route", ["DFW→SFO", "DFW→LHR"])

client = ProfitabilityClient("http://api")
data = client.get_forecast(route)

st.metric("Revenue", f"${data['revenue']:,.0f}")
st.metric("Cost", f"${data['cost']:,.0f}")
st.metric("Margin", f"${data['revenue'] - data['cost']:,.0f}")
```

**Key Principle:** Dashboard is presentation layer—legacy R model logic is preserved, not rewritten.

---

## Input Validation (ENG-6.5)

**Validate user input from Streamlit widgets:**

```python
# app.py
import streamlit as st
from datetime import date, timedelta

# Date range validation
start_date = st.date_input("Start Date", date.today() - timedelta(days=30))
end_date = st.date_input("End Date", date.today())

if start_date > end_date:
    st.error("Start date must be before end date")
    st.stop()

if (end_date - start_date).days > 365:
    st.warning("Date range exceeds 1 year—performance may be slow")

# Numeric input validation
capacity_pct = st.slider("Capacity Adjustment (%)", -50, 50, 0)

if capacity_pct < -30:
    st.warning("Large capacity reduction may impact forecast accuracy")
```

---

## Caching & Performance

**Use Streamlit caching to avoid redundant API calls:**

```python
import streamlit as st

@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_route_data(route: str) -> dict:
    """Load route data from API (cached)."""
    client = ProfitabilityClient("http://api")
    return client.get_forecast(route)

@st.cache_resource
def get_api_client() -> ProfitabilityClient:
    """Create API client (singleton)."""
    return ProfitabilityClient("http://api")
```

**When to cache:**
- `@st.cache_data`: Data loading (API calls, database queries, CSV parsing)
- `@st.cache_resource`: Singleton objects (API clients, database connections)

---

## Multi-Page Apps

**Organize complex dashboards with multiple pages:**

```
streamlit_app/
  app.py                    # Landing page
  pages/
    01_route_analysis.py    # Page 1: Route profitability
    02_scenario_comparison.py  # Page 2: Scenario modeling
    03_admin.py             # Page 3: Admin settings
```

**Navigation is automatic:**
- Streamlit generates sidebar navigation for files in `pages/`
- Pages are ordered by filename prefix (`01_`, `02_`)

---

## Anti-Patterns to Avoid

❌ **DO NOT put business logic in app.py**
- **Wrong:** Complex calculations, data transformations in Streamlit callbacks
- **Right:** Extract to tested modules in `domain/`, keep UI thin

❌ **DO NOT call R/PySpark directly from Streamlit**
- **Wrong:** `subprocess.run(["Rscript", "model.R"])` in app.py
- **Right:** API layer (FastAPI) between Streamlit and legacy models

❌ **DO NOT skip tests for logic modules**
- **Wrong:** "Streamlit is a prototype, no tests needed"
- **Right:** Test `domain/` and `clients/` modules with pytest, keep UI thin

❌ **DO NOT use Streamlit for production-critical systems**
- **Wrong:** High-concurrency production app with 1000+ users
- **Right:** Use Streamlit for MVPs, migrate to FastAPI + React if scale/complexity grows

---

## Brownfield Use Cases

### Use Case 1: R Model Dashboard
- **Context:** Legacy R scripts for route profitability forecasting
- **Solution:** Containerize R, wrap in FastAPI, build Streamlit dashboard
- **Outcome:** Analysts get interactive UI without R code rewrite

### Use Case 2: PySpark Pipeline Visualization
- **Context:** PySpark notebooks for network optimization
- **Solution:** Extract PySpark logic to modules, trigger via Streamlit UI
- **Outcome:** Non-technical users can run optimizations and view results

### Use Case 3: Jupyter Notebook Replacement
- **Context:** Ad-hoc analysis in Jupyter notebooks (not production-ready)
- **Solution:** Extract reusable logic, wrap in Streamlit UI
- **Outcome:** Repeatable analysis tool that non-technical users can run

---

## Related Avatars

- **Technology:** `python-fastapi` (API layer), `legacy-ml-interop` (R/PySpark preservation), `python-pyspark` (data processing)
- **Product:** `network-planning-optimization`, `cargo-freight`

---

## Activation

This avatar activates:
- **Skills:** skill-06 (Atomic TDD), skill-07 (Vertical Slice), skill-30 (Taxonomy-Governed Enrichment)
- **Workflows:** product-discovery-stage-a-f, legacy-rescue-decision-track
- **Laws:** ENG-4.1 (Atomic TDD), ENG-3.1 (Complexity Limits), ENG-2.2 (Layered Architecture), ENG-10.1 (Brownfield Integration)

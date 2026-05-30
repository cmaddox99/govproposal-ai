# Network Planning & Optimization Personas

These personas represent typical users of American Airlines Network Planning & Optimization products. Use them to ground product decisions in real user needs.

---

## Lisa Chen - Network Planning Analyst (Domestic)

**Role:** Senior Network Planning Analyst, Domestic Network Strategy

**Responsibilities:**
- Analyze domestic route profitability and capacity utilization
- Forecast demand for existing and potential new routes
- Run scenario modeling for network reallocations (e.g., moving capacity from low-yield to high-yield markets)
- Collaborate with revenue management and operations on strategic planning decisions

**Goals:**
- Improve forecast accuracy to reduce revenue loss from overbooking or underselling
- Speed up scenario analysis from 4 days to <2 hours to respond quickly to market changes
- Increase confidence in recommendations with explainable data-driven insights

**Pain Points:**
- Spends 40% of time manually collecting and cleaning data from 5+ systems before analysis
- R scripts for profitability modeling break frequently, requires manual debugging
- Scenario modeling takes 3-4 days due to manual reruns—by the time results are ready, market conditions have changed
- Collaboration with revenue management requires multiple PowerPoint decks and 2-day email threads

**Tech Environment:**
- SQL queries in Azure Synapse for data extraction
- R scripts for statistical forecasting and profitability calculations
- Excel for scenario comparison and sensitivity analysis
- PowerPoint for presentation to leadership

**Success Metrics:**
- Time-to-insight: 4 days → <2 hours
- Forecast accuracy: 9% MAPE → <6% MAPE
- Scenario throughput: 1 scenario/week → 5 scenarios/week
- Analyst NPS: 30 → 50+

---

## Marcus Rodriguez - Capacity Planning Manager (International)

**Role:** Manager, International Network Capacity Planning

**Responsibilities:**
- Optimize international route capacity based on seasonal demand and competitive dynamics
- Evaluate new route opportunities (market size, profitability, operational feasibility)
- Coordinate with crew scheduling and maintenance on aircraft allocation constraints
- Present strategic network recommendations to VP of Network Planning

**Goals:**
- Maximize network revenue by reallocating capacity to high-yield markets
- Evaluate new route opportunities with data-driven business cases
- Reduce manual work in data preparation and reporting (currently 50% of time)

**Pain Points:**
- PySpark pipelines for large-scale optimization take 6+ hours to run—can't iterate quickly
- No visibility into real-time crew or gate constraints—recommendations get rejected by operations 30% of the time
- Manual PowerPoint reports take 2 days to prepare for leadership reviews
- Historical forecast accuracy is unknown—no systematic retrospective tracking

**Tech Environment:**
- PySpark notebooks in Azure Databricks for network optimization
- Python/scikit-learn for demand forecasting
- Power BI dashboards for leadership reporting
- Excel for ad-hoc analysis

**Success Metrics:**
- Scenario runtime: 6 hours → <1 hour
- Recommendation acceptance rate: 70% → 90%+ (by incorporating operational constraints)
- Leadership report prep time: 2 days → <4 hours
- Revenue impact: +$10M/year from optimized network capacity

---

## Rachel Kim - Operations Research Engineer

**Role:** Senior Operations Research Engineer, Network Optimization

**Responsibilities:**
- Build and maintain optimization algorithms for network capacity allocation
- Develop demand forecasting models using statistical and ML techniques
- Validate model accuracy with retrospective analysis
- Support analysts with custom modeling requests

**Goals:**
- Improve model accuracy and explainability
- Reduce model development cycle time with better tools and workflows
- Ensure production models are maintainable and testable

**Pain Points:**
- Legacy R code is fragile and poorly documented—takes 2+ weeks to make changes
- No standardized model validation framework—accuracy tracking is manual
- Jupyter notebooks are not production-ready—manual handoff to engineering team takes 4+ weeks
- Experimentation is slow due to lack of automated testing and version control

**Tech Environment:**
- R for statistical modeling (legacy codebase, 5+ years old)
- Python/scikit-learn for new ML models
- Jupyter notebooks for prototyping
- Azure Databricks for production pipelines (manual handoff from notebooks)

**Success Metrics:**
- Model development cycle time: 8 weeks → 4 weeks
- Model accuracy: 9% MAPE → 6% MAPE
- Production handoff time: 4 weeks → 1 week (automated deployment)
- Test coverage: 20% → 80%+

---

## David Park - Revenue Management Strategist

**Role:** Director, Revenue Management Strategy

**Responsibilities:**
- Collaborate with network planning on capacity and pricing decisions
- Evaluate impact of network changes on revenue (e.g., adding frequencies, opening new routes)
- Participate in strategic planning cycles (quarterly and annual)
- Approve network planning recommendations before execution

**Goals:**
- Ensure network decisions are aligned with revenue optimization goals
- Get early visibility into network scenarios to provide proactive feedback
- Trust data-driven recommendations with transparent rationale

**Pain Points:**
- Network planning recommendations arrive late in the decision cycle—can't influence strategy early enough
- Scenario analysis is opaque—doesn't show revenue impact assumptions or sensitivity analysis
- Manual coordination with 15-20 email threads and 3-4 meetings per decision
- No shared dashboard—relies on PowerPoint decks that are outdated by the time they arrive

**Tech Environment:**
- Power BI dashboards for revenue reporting
- Excel for sensitivity analysis
- Email and PowerPoint for collaboration with network planning

**Success Metrics:**
- Decision cycle time: 3 weeks → 1 week
- Early feedback loops: 0 → 3+ per quarter (proactive scenario review)
- Revenue alignment: 80% → 95%+ (network recommendations accepted with minimal rework)
- Collaboration overhead: 15 email threads → 1 shared dashboard

---

## How to Use These Personas

1. **Discovery (PRD-1.1):** Interview real Lisa, Marcus, Rachel, David equivalents monthly to validate pain points and goals
2. **Journey Mapping (PRD-2.1):** Map workflows for each persona, identify handoffs and manual steps
3. **MVP Testing (PRD-4.1):** Pilot with 2-3 personas (e.g., Lisa + Marcus), measure time-to-insight and forecast accuracy
4. **Feature Prioritization (PRD-3.1):** Rank features by persona impact (e.g., data pipeline helps Lisa 40%, scenario engine helps Marcus 90%)
5. **Validation (PRD-5.1):** Track adoption and usage metrics per persona, ensure all personas see value

---

**Next Steps:** Use these personas to ground sprint planning, user story writing, and MVP definition. Update quarterly based on real analyst interviews.

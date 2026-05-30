# Ground Ops Staffing Analytics — Personas

These personas represent the primary users of ABR-Staffing and similar ramp workforce
optimization systems at American Airlines. Use them to ground product decisions in real operator needs.

---

## Jordan Rivera — Ground Ops Analyst (Staffing Optimizer)

**Role:** Senior Ground Operations Analyst, Hub Station Staffing

**Responsibilities:**
- Run the ABR-Staffing pipeline each season to generate staffing plans for CLT, DFW, PHX, MIA
- Configure `run_config.json` with season parameters and validate input data quality
- Review ML model outputs and adjust business rules when station operations change
- Present staffing plans to station operations managers for approval

**Goals:**
- Generate accurate staffing plans faster (currently 2+ hours of manual monitoring per run)
- Reduce rerun rate caused by data errors discovered mid-pipeline
- Easily compare this season's plan to prior season actuals

**Pain Points:**
- Must manually edit JSON config files — no UI validation
- Notebook failures midway through the pipeline require debugging cell-by-cell
- No experiment tracking — can't tell why this season's model differs from last season
- Staffing plan is a raw JSON file — hard to review or share with supervisors

**Tech Environment:**
- Jupyter notebooks in VS Code / Azure ML Studio
- Databricks SQL for ADLS queries
- Python/scikit-learn for ML
- Email for sharing staffing plans

**Success Metrics:**
- Pipeline run time: 2 hours → <45 minutes
- Rerun rate: ~30% → <5%
- Plan accuracy: within 15% of actual staffing on 80%+ of shifts

---

## Marcus Webb — Ramp Operations Supervisor

**Role:** Baggage Ramp Supervisor, DFW Hub

**Responsibilities:**
- Review and approve seasonal staffing plans from the analytics team
- Adjust daily staffing based on IROP events and real-time flight changes
- Escalate staffing gaps to station operations manager

**Goals:**
- Trust the staffing plan enough to use it without heavy manual override
- Know which delivery types need more people on IROP days
- Have a fast way to review the plan without opening JSON files

**Pain Points:**
- Receives staffing plan as a JSON file — requires translating to a shift schedule manually
- Model doesn't always account for Friday T-Link volume spikes
- No visibility into model confidence — single number vs. range

**Success Metrics:**
- Plan adoption rate: >70% of shifts use model-generated headcount without override
- IROP staffing accuracy: <20% deviation on disruption days

---

## Priya Nair — Station Operations Manager

**Role:** Manager, Airport Station Operations (CLT)

**Responsibilities:**
- Own labor budget for the station across all ground operations
- Review and sign off on seasonal staffing plans
- Escalate staffing outcome misses to VP of Airport Operations

**Goals:**
- Reduce over-staffing waste (currently estimated at 15–25% seasonal budget overage)
- Have a defensible data-driven rationale for staffing decisions during audits
- Track staffing accuracy retrospectively to improve future seasons

**Pain Points:**
- No dashboard for season-over-season comparison
- Model is a black box — hard to explain to finance teams
- Over-staffing on slow delivery-type days (e.g., claim on short-haul-only days)

**Success Metrics:**
- Over-staffing cost reduction: 20% per season
- Audit readiness: all staffing decisions traceable to run_id and model version

---

## Alex Torres — Airport Planning Engineer

**Role:** Senior Engineer, Airport Operations Analytics

**Responsibilities:**
- Maintain and improve the ABR-Staffing ML pipeline codebase
- Add support for new stations as the hub network expands
- Debug and remediate data quality issues from ADLS or Mosaic
- Ensure pipeline meets constitutional development standards (testing, audit trail)

**Goals:**
- Adopt a testing framework so notebook changes don't break production runs silently
- Extract notebook business logic into reusable, testable Python modules
- Add MLflow tracking to compare model performance across stations and seasons

**Pain Points:**
- No unit tests — every change requires a full end-to-end run to validate
- Business logic buried in notebook cells — hard to reason about or refactor
- Station config changes require notebook edits — risky and error-prone
- No standard way to onboard a new station

**Success Metrics:**
- Test coverage on `utils/`: 0% → ≥90% (Phase 1)
- Extracted modules coverage: ≥90% (Phase 2)
- New station onboarding time: 2 weeks → <3 days (Phase 3)

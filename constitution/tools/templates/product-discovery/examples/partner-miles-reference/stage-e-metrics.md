---
type: discovery
id: disc-2026-042
spec_id: disc-2026-042
stage: E
stage_label: Metric Rebaseline
status: APPROVED
created: 2026-04-17
branch: exploratory-demo
workflow: product-discovery
workflow_version: "2.0.0"
skill: skill-product-discovery-orchestration
title: "AAdvantage Partner-Miles Posting — Metric Rebaseline"

mode: Exploratory
tier: Tier 2

laws:
  - PRD-6.1
  - ENG-10.1
  - BUS-7.1
  - ENG-13.1

laws_applied:
  - PRD-6.1
  - ENG-10.1
  - BUS-7.1
  - ENG-13.1

stages:
  - id: A
    label: Initialize
    status: done
  - id: B
    label: Field Study
    status: done
  - id: C
    label: Code Evidence
    status: done
  - id: D
    label: Validation
    status: done
  - id: E
    label: Metrics
    status: active
  - id: F
    label: Roadmap Lock
    status: locked

gates:
  entry:
    status: met
    description: >
      Stage D Validation complete. DVFT matrix produced 4 GREEN, 1
      YELLOW (needs observability instrumentation), 1 RED (retention
      lift untested). Stage E defines the measurement plan that resolves
      the YELLOW and frames the RED as a hypothesis to be tested.
  exit:
    status: pending
    description: >
      Awaiting §Render Gate APPROVE. Metric spec covers AARRR funnel,
      baselines, targets, PMF signal, and explicit measurement plan
      naming owner + frequency + tooling per metric.

mode_selection:
  selected: Exploratory
  rationale: >
    Mode locked at Stage A.

tier_selection:
  tier: Tier 2
  rationale: >
    Tier 2 carried; full AARRR funnel + PMF signal + leading/lagging
    indicators required.

problem_validation:
  dim1:
    label: "1. Problem Exists"
    status: ok
    text: "Validated. Carried."
  dim2:
    label: "2. Problem Matters"
    status: ok
    text: "Validated. Baseline cost: $2.4M annual support volume."
  dim3:
    label: "3. Problem Is Solvable"
    status: ok
    text: "Validated. Carried."
  dim4:
    label: "4. Users Will Exchange Value"
    status: ok
    text: "Validated. Carried."

domain_landscape_title: "AARRR Funnel — Metrics, Baselines, Targets (PRD-6.1)"
domains:
  - name: "ACQUISITION — Tracker discovered"
    icon: "👀"
    header_bg: "#f0f4ff"
    header_color: "#1d4ed8"
    role: "% of Gold members who see the tracker entry point in app"
    stack: "Baseline: 0% (does not exist) · Target: 80% within 30d of launch"
    submodules: "M1"
    tags:
      - {text: "Leading indicator", tone: "blue"}
      - {text: "App analytics", tone: "blue"}
  - name: "ACTIVATION — First open"
    icon: "✋"
    header_bg: "#f5f3ff"
    header_color: "#5b21b6"
    role: "% of Gold members who open the tracker within 30d"
    stack: "Baseline: 0% · Target: 40% · PMF signal: ≥35%"
    submodules: "M2"
    tags:
      - {text: "PMF metric", tone: "purple"}
      - {text: "Concept-test predicted 87%", tone: "yellow"}
  - name: "RETENTION — Repeat use"
    icon: "🔁"
    header_bg: "#fffbeb"
    header_color: "#92400e"
    role: "% of activated members who return weekly during a partner-trip cycle"
    stack: "Baseline: N/A · Target: 60% · Window: 30d post-flight"
    submodules: "M3"
    tags:
      - {text: "Behavior change", tone: "yellow"}
      - {text: "Funnel core", tone: "yellow"}
  - name: "REVENUE — Support cost reduction"
    icon: "💰"
    header_bg: "#f0fdf4"
    header_color: "#166534"
    role: "Reduction in 'where are my partner miles?' support call volume"
    stack: "Baseline: 7.3% of total volume ($2.4M/yr) · Target: −30% (–$720K/yr)"
    submodules: "M4"
    tags:
      - {text: "Lagging indicator", tone: "green"}
      - {text: "CX analytics", tone: "green"}
      - {text: "Resolves DVFT-A2", tone: "green"}
  - name: "REVENUE — Retention (HYPOTHESIS)"
    icon: "📈"
    header_bg: "#fef2f2"
    header_color: "#991b1b"
    role: "Gold-tier renewal rate change vs matched cohort"
    stack: "Baseline: X · Target: NOT PROMISED · Hypothesis: +2pts (DVFT-A3 RED)"
    submodules: "M5"
    tags:
      - {text: "🔴 Hypothesis only", tone: "red"}
      - {text: "Requires A/B", tone: "red"}
      - {text: "Do NOT promise", tone: "red"}
  - name: "REFERRAL — NPS lift"
    icon: "💬"
    header_bg: "#eff6ff"
    header_color: "#1d4ed8"
    role: "Member NPS in cohort with tracker vs control"
    stack: "Baseline: 32 (Gold tier) · Target: +3 NPS · Survey: 90d post-launch"
    submodules: "M6"
    tags:
      - {text: "Sentiment proxy", tone: "blue"}
      - {text: "Quarterly NPS", tone: "blue"}

arch_title: "Measurement Plan — Owner, Frequency, Tooling per Metric"
arch_flow: |
  M1  Acquisition         · Mobile Eng     · daily       · LaunchDarkly impressions + Mixpanel
  M2  Activation (PMF)    · Product / Amal · weekly cohort · Mixpanel funnel
  M3  Retention           · Product / Amal · weekly cohort · Mixpanel return-frequency
  M4  Support cost (CORE) · CX Analytics   · weekly       · Looker dashboard 'partner-miles-cx'
  M5  Renewal lift (HYPO) · Loyalty Strat  · per renewal cycle · Matched-cohort A/B (designed Q3)
  M6  NPS lift            · Member Insights· quarterly    · NPS survey segmentation

  PMF declared if: M2 ≥ 35% AND M4 ≥ −20% by Day 90 post-launch.
  PMF strong if:   M2 ≥ 50% AND M4 ≥ −30% AND M6 ≥ +3 NPS by Day 90.

findings_title: "Metric Spec Decisions"
findings:
  - title: "PMF defined as M2 (activation) ≥ 35% AND M4 (cost) ≥ −20% at Day 90"
    description: "Two-metric AND condition prevents a vanity-activation declaration. Both adoption AND business impact must move."
    status: done
    laws: [PRD-6.1]
  - title: "Retention claim (M5) framed as hypothesis with named A/B owner"
    description: "Per Stage D DVFT-A3 RED finding. Loyalty Strategy team owns the matched-cohort experiment. Designed Q3, executed Q4–Q1."
    status: done
    laws: [PRD-6.1]
  - title: "Support cost reduction (M4) is the primary success metric"
    description: "Cleanly attributable, baseline known, drives the business case. Drop in 'where are my partner miles?' call-reason code is the leading signal."
    status: done
    laws: [PRD-6.1]
  - title: "Observability instrumentation gate added (resolves DVFT-A2 conditional)"
    description: "Stage F implementation MUST include call-reason attribution from CX system to member's tracker state at time of call. Without this, M4 attribution is too noisy."
    status: done
    laws: [ENG-10.1]
  - title: "Quarterly check-in cadence with Discovery Sponsor"
    description: "Q1 post-launch: full AARRR funnel review. Q2: PMF declaration go/no-go. Q3: A/B kickoff. Q4: A/B readout."
    status: done
    laws: [PRD-6.1]

ensemble_verdict:
  verdicts:
    - persona: Amal (Product Coach)
      law: PRD-6.1
      note: "AARRR funnel complete with 6 metrics. PMF criteria are concrete (M2 ≥ 35% AND M4 ≥ −20%). RED-tagged hypothesis isolated from PMF claim."
      verdict: PASS
    - persona: Amaya (Technical Coach)
      law: ENG-10.1
      note: "Observability gate added to Stage F implementation. Without it, M4 attribution would be unreliable. Tooling identified per metric."
      verdict: PASS
    - persona: Sentinel
      law: BUS-7.1
      note: "Audit trail intact. Measurement plan names owners (BUS-7.1 actor accountability)."
      verdict: PASS

exit_checklist:
  - title: "AARRR funnel complete"
    description: "6 metrics across A/A/R/R/R covering full member journey."
    status: done
    laws: [PRD-6.1]
  - title: "Baselines documented for all measurable metrics"
    description: "Baselines: M1=0, M2=0, M4=7.3% volume / $2.4M, M6=32 NPS. M3, M5 N/A baselines."
    status: done
    laws: [PRD-6.1]
  - title: "Targets set with PMF criteria"
    description: "PMF: M2 ≥ 35% AND M4 ≥ −20% at Day 90. Strong PMF: also M6 ≥ +3."
    status: done
    laws: [PRD-6.1]
  - title: "Leading vs lagging indicators classified"
    description: "Leading: M1, M2, M3. Lagging: M4, M5, M6."
    status: done
    laws: [PRD-6.1]
  - title: "Measurement plan names owner + frequency + tooling per metric"
    description: "All 6 metrics have named owner, cadence, and tool."
    status: done
    laws: [ENG-10.1]
  - title: "Stakeholder approval — Director+ (must include Finance/Analytics)"
    description: "Pending: Adeel Ali + CFO delegate."
    status: wait
    laws: [PRD-2.5]
  - title: "HTML render gate — APPROVED in browser"
    description: "Awaiting ticked APPROVE."
    status: wait
    laws: [ENG-13.1]
  - title: "BUS-7.1 audit event filed for Stage E → F"
    description: "Will append on APPROVE."
    status: wait
    laws: [BUS-7.1]

audit_log:
  - event: "Stage D → E"
    actor: "Adeel Ali"
    role: "Inventor / Approver"
    system: "manual"
    timestamp: "2026-04-17"
    outcome: "APPROVED"
  - event: "AARRR funnel drafted"
    actor: "Amal"
    role: "Product Coach"
    system: "Hangar AI Constitution"
    timestamp: "2026-04-17"
    outcome: "OK"
  - event: "PMF criteria defined"
    actor: "Amal"
    role: "Product Coach"
    system: "Hangar AI Constitution"
    timestamp: "2026-04-17"
    outcome: "OK"
  - event: "Measurement-plan ownership assigned"
    actor: "Amal + Amaya"
    role: "Product + Technical"
    system: "Hangar AI Constitution"
    timestamp: "2026-04-17"
    outcome: "OK"
  - event: "Stage E → F"
    actor: "Adeel Ali"
    role: "Inventor / Approver"
    system: "manual"
    timestamp: "TBD"
    outcome: "AWAITING"

render_gate:
  status: pending

spec_artifacts:
  - filename: "stage-e-metrics.md"
    icon: "📄"
    status: "DRAFTED"
  - filename: "metrics-spec.csv"
    icon: "📊"
    status: "OK"
  - filename: "looker-dashboard-spec.json"
    icon: "📈"
    status: "OK"
  - filename: "stage-e-metrics.html"
    icon: "🌐"
    status: "RENDERED"

avatars:
  - name: "product"
    icon: "🎯"
    context: "lead at Stage E"
  - name: "engineering"
    icon: "🔴"
    context: "Amaya — observability gate"
  - name: "business"
    icon: "💼"
    context: "Finance / CX Analytics"
  - name: "avatar-product-loyalty"
    icon: "✈️"
    context: "AAdvantage"

stakeholder:
  approver: "Adeel Ali"
  title: "Inventor / Discovery Sponsor"
  date: "Pending"
  method: "In-session workshop review"
  self_cert: false

footer_id: disc-2026-042
footer_project: "AAdvantage Partner-Miles Posting · Stage E"
---

# Stage E Evidence: Metric Rebaseline — AAdvantage Partner-Miles Posting

> **Reference example.** Synthesized data; demonstrates a complete Stage E under the rich-card discovery template.

---

## Render Gate (ENG-13.1)

> **NON-NEGOTIABLE:** Reviewer ticks exactly one decision below.

- [ ] ✅ **APPROVE** — Metric spec sufficient; Stage F Roadmap Lock may begin
- [ ] 🔄 **ENHANCE** — Specific metric needs better baseline / target / owner
- [ ] ❌ **REJECT** — Measurability gap blocks roadmap; do NOT advance

| Field | Value |
|-------|-------|
| **Reviewer name** | _pending_ |
| **Reviewer role** | Inventor / Discovery Sponsor (with Finance delegate) |
| **Decision timestamp** | _pending_ |
| **Review method** | In-browser render |
| **Self-cert?** | No — initiator (Amal) ≠ reviewer (Adeel) |

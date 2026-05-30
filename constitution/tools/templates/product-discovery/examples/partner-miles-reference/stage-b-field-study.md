---
# Stage B EVIDENCE — Field Study · Product Discovery v2.0.0
type: discovery
id: disc-2026-042
spec_id: disc-2026-042
stage: B
stage_label: Field Study
status: APPROVED
created: 2026-04-17
branch: exploratory-demo
workflow: product-discovery
workflow_version: "2.0.0"
skill: skill-product-discovery-orchestration
title: "AAdvantage Partner-Miles Posting — Field Study"

mode: Exploratory
tier: Tier 2

laws:
  - PRD-2.3
  - PRD-2.4
  - PRD-3.1
  - PRD-3.2
  - BUS-7.1
  - ENG-13.1

laws_applied:
  - PRD-2.3
  - PRD-2.4
  - PRD-3.1
  - PRD-3.2
  - BUS-7.1
  - ENG-13.1

stages:
  - id: A
    label: Initialize
    status: done
  - id: B
    label: Field Study
    status: active
  - id: C
    label: Code Evidence
    status: locked
  - id: D
    label: Validation
    status: locked
  - id: E
    label: Metrics
    status: locked
  - id: F
    label: Roadmap Lock
    status: locked

gates:
  entry:
    status: met
    description: >
      Stage A PROPOSAL approved 2026-04-17 by Adeel Ali (Inventor). Hypothesis
      from Stage A: pain is the silence during the 4–6 week posting window,
      not the delay itself. Stage B set out to test that hypothesis with
      live members.
  exit:
    status: pending
    description: >
      Awaiting §Render Gate APPROVE before advancing to Stage C Code Evidence.

mode_selection:
  selected: Exploratory
  rationale: >
    Mode locked at Stage A. Stage B research conducted from scratch — no
    pre-validated problem statement to anchor against.

tier_selection:
  tier: Tier 2
  rationale: >
    Carried from Stage A. Tier 2 manifest required for Stage B: personas
    (≥3), journey map, competitive analysis, full user research log.

problem_validation:
  dim1:
    label: "1. Problem Exists"
    status: ok
    text: >
      CONFIRMED. 14/14 Gold/Platinum members interviewed report loss of
      trust during the 4–6 week posting window. Direct quote (Maria,
      Gold, 38 segments/yr): "I don't mind waiting. I mind not knowing."
  dim2:
    label: "2. Problem Matters"
    status: ok
    text: >
      CONFIRMED. CX analytics pull shows 7.3% of total member support
      volume attributable to "partner miles posting" call-reason code.
      Annualized cost estimate $2.4M+ in support handle time alone.
  dim3:
    label: "3. Problem Is Solvable"
    status: warn
    text: >
      Solvability hypothesis still open at Stage B — defer to Stage C
      Code Evidence for technical feasibility assessment of a status tracker.
  dim4:
    label: "4. Users Will Exchange Value"
    status: ok
    text: >
      CONFIRMED. Concept-test (Figma prototype) shown to 8 members:
      7/8 would open a status tracker weekly. 6/8 explicitly said
      they'd accept the 4-week window if visibility were provided.

domain_landscape_title: "Personas — From 21 Member Interviews (2026-04-15 to 2026-04-17)"
domains:
  - name: "Maria — Gold Frequent Traveler"
    icon: "✈️"
    header_bg: "#fffbeb"
    header_color: "#92400e"
    role: "Business consultant · 38 partner segments/yr · oneworld primary"
    stack: "AA app daily · checks miles 3x/week"
    submodules: "n=6"
    tags:
      - {text: "High pain", tone: "red"}
      - {text: "Daily checker", tone: "yellow"}
      - {text: "Tracker preferred", tone: "green"}
  - name: "James — Platinum Elite"
    icon: "👔"
    header_bg: "#fff1f2"
    header_color: "#9f1239"
    role: "Senior exec · 65 segments/yr · status-driven flyer"
    stack: "AA app + AAdvantage portal"
    submodules: "n=4"
    tags:
      - {text: "Renewal at risk", tone: "red"}
      - {text: "Compares Delta", tone: "yellow"}
      - {text: "Trust-critical", tone: "red"}
  - name: "Linda — Casual Member"
    icon: "🧳"
    header_bg: "#f0f4ff"
    header_color: "#1d4ed8"
    role: "Leisure traveler · 4 partner segments/yr"
    stack: "Browser only · checks miles after trip"
    submodules: "n=7"
    tags:
      - {text: "Low pain", tone: "green"}
      - {text: "Forgets miles posted", tone: "blue"}
      - {text: "Control group", tone: "blue"}
  - name: "David — Internal Program Manager"
    icon: "🏢"
    header_bg: "#f5f3ff"
    header_color: "#5b21b6"
    role: "AAdvantage retention strategy"
    stack: "Looker · CX analytics"
    submodules: "n=4"
    tags:
      - {text: "Cost-conscious", tone: "yellow"}
      - {text: "Retention-driven", tone: "green"}
      - {text: "Sponsors fix", tone: "green"}

arch_title: "Member Journey — Books Partner Flight to Trust Erosion"
arch_flow: |
  Step 1  Member books partner-airline ticket (e.g., British Airways via aa.com)
          ↓
          Booking confirmation arrives. AAdvantage number captured.
          ↳ Expectation set: "miles will post"

  Step 2  Member flies the partner segment
          ↓
          Boarding pass scanned. Flight completes.
          ↳ Member checks AA app same day (8/14 Gold members do this)
          ↳ App shows: nothing. No partner miles entry.

  Step 3  Days 1–14 — silence
          ↓
          Member checks AA app 2-7 more times in the first 2 weeks.
          ↳ Trust starts to fray (avg sentiment shift Day 7-10)

  Step 4  Days 14–28 — first support call
          ↓
          11/14 Gold members called support; 9/14 called more than once.
          Support response: "Please wait 4-6 weeks. Open a case if missing."
          ↳ "I felt the system didn't see me." (James, Platinum)

  Step 5  Day 28-42 — miles post (or don't)
          ↓
          Most miles post by Day 35. 2/14 cases required manual case escalation.
          ↳ Member relief, but trust damage already done.

findings_title: "Field Study Findings — Competitive Analysis + Research Log"
findings:
  - title: "Delta SkyMiles posts partner miles in 5–10 days with status tracker (PRD-2.4)"
    description: "Delta exposes 'In Process' / 'Posted' / 'Investigating' states in their app from Day 0. Members report this 'feels reassuring even when slow' (cross-program member panel)."
    status: done
    laws: [PRD-2.4]
  - title: "United MileagePlus posts in 7–14 days, no real-time tracker"
    description: "United's window is shorter than AA's (14 days vs 28-42) but they don't expose status. Mid-tier finding: speed alone helps, but visibility helps more."
    status: done
    laws: [PRD-2.4]
  - title: "JTBD: 'know my earning is safe' (PRD-2.3)"
    description: "12/14 Gold members framed the job as 'I just want to know it's processing,' not 'I want it faster.' Validates the Stage A hypothesis: silence is the pain, not delay."
    status: done
    laws: [PRD-2.3]
  - title: "Support call cost is real and measurable"
    description: "CX analytics confirm 7.3% of all support volume is partner-miles related. At $18 average handle time × volume = $2.4M annual. This is the viability signal."
    status: done
    laws: [PRD-3.1]
  - title: "Concept test outcome — 7/8 would adopt a tracker"
    description: "Figma prototype showing 'Your Iberia flight from MAD-MIA: Posting expected by April 28' tested with 8 members. 7/8 said they would open weekly. 6/8 said it would replace a support call."
    status: done
    laws: [PRD-3.1]
  - title: "Negative finding — partner-side cooperation may be limited"
    description: "Two former AAdvantage program managers we spoke with noted that getting real-time push from oneworld partners is contractually difficult. The tracker should NOT depend on it. Read-only view of internal posting state is the safe scope."
    status: done
    laws: [PRD-3.2]
  - title: "Open blocker for Stage C — codebase access"
    description: "Need access to aa-loyalty-ledger and aa-member-app repos to confirm the in-flight status enum hypothesis. Awaiting platform-eng signoff."
    status: wait
    laws: [PRD-3.2]

ensemble_verdict:
  verdicts:
    - persona: Amal (Product Coach)
      law: PRD-3.1
      note: "Field study scope met Tier 2 minimum (≥12 interviews, ≥3 personas, journey map, competitive analysis, research log). Hypothesis from Stage A confirmed by direct member quotes — strong qualitative + quantitative signal."
      verdict: PASS
    - persona: Sentinel
      law: BUS-7.1
      note: "Audit log entries present for all 21 interviews. Recordings retained per BUS-4.3. CX analytics pull authorized via internal data request DR-2026-1147."
      verdict: PASS
    - persona: Willem (Constitutional Architect)
      law: PRD-2.5
      note: "Stage B exit gate criteria met. Stage C may begin — pending codebase access."
      verdict: PASS

exit_checklist:
  - title: "Personas documented (≥3 for Tier 2)"
    description: "4 personas — Maria (Gold), James (Platinum), Linda (Casual), David (Internal PM)."
    status: done
    laws: [PRD-3.1]
  - title: "Journey map captured end-to-end"
    description: "5-step current-state journey with sentiment shift mapped to days 7-10."
    status: done
    laws: [PRD-3.2]
  - title: "Competitive analysis completed (≥2 competitors)"
    description: "Delta SkyMiles + United MileagePlus benchmarked."
    status: done
    laws: [PRD-2.4]
  - title: "User research log filed"
    description: "21 interviews, 6 hrs concept-test sessions, transcripts retained."
    status: done
    laws: [PRD-3.1]
  - title: "JTBD framing applied"
    description: "Job-to-be-done: 'know my earning is safe' (validated, not 'get miles faster')."
    status: done
    laws: [PRD-2.3]
  - title: "≥3 validated user insights filed in hangar-ai-specs/"
    description: "5 validated insights documented (silence pain, cost surface, tracker adoption signal, partner-cooperation constraint, casual-member control)."
    status: done
    laws: [PRD-2.5]
  - title: "Stakeholder approval — named approver Director+"
    description: "Pending: Adeel Ali."
    status: wait
    laws: [PRD-2.1, PRD-2.5, BUS-7.1]
  - title: "HTML evidence rendered + APPROVED in browser"
    description: "Awaiting ticked APPROVE in §Render Gate."
    status: wait
    laws: [ENG-13.1]
  - title: "BUS-7.1 audit event filed for Stage B → C transition"
    description: "Will append on APPROVE."
    status: wait
    laws: [BUS-7.1]

audit_log:
  - event: "Stage A → B advanced"
    actor: "Adeel Ali"
    role: "Inventor / Approver"
    system: "manual"
    timestamp: "2026-04-17"
    outcome: "APPROVED"
  - event: "Field study initiated"
    actor: "Amal"
    role: "Product Coach"
    system: "Hangar AI Constitution"
    timestamp: "2026-04-17"
    outcome: "IN_PROGRESS"
  - event: "21 member interviews completed"
    actor: "Field Research Team"
    role: "Member Insights"
    system: "Looker + interview platform"
    timestamp: "2026-04-17"
    outcome: "OK"
  - event: "Concept test (Figma)"
    actor: "Amal"
    role: "Product Coach"
    system: "Figma + Maze"
    timestamp: "2026-04-17"
    outcome: "OK"
  - event: "Competitive analysis"
    actor: "Amal"
    role: "Product Coach"
    system: "Hangar AI Constitution"
    timestamp: "2026-04-17"
    outcome: "OK"
  - event: "Stage B → C"
    actor: "Adeel Ali"
    role: "Inventor / Approver"
    system: "manual"
    timestamp: "TBD"
    outcome: "AWAITING"

render_gate:
  status: pending
  reviewer: ""
  timestamp: ""

spec_artifacts:
  - filename: "stage-a-proposal.md"
    icon: "📄"
    status: "APPROVED"
  - filename: "stage-b-field-study.md"
    icon: "📄"
    status: "DRAFTED"
  - filename: "stage-b-interview-transcripts/"
    icon: "📂"
    status: "OK"
  - filename: "stage-b-competitive-matrix.csv"
    icon: "📊"
    status: "OK"
  - filename: "stage-b-field-study.html"
    icon: "🌐"
    status: "RENDERED"

avatars:
  - name: "product"
    icon: "🎯"
    context: "lead at Stage B"
  - name: "business"
    icon: "💼"
    context: "constitutional context"
  - name: "avatar-product-loyalty"
    icon: "✈️"
    context: "AAdvantage · 180M members"

stakeholder:
  approver: "Adeel Ali"
  title: "Inventor, Hangar AI Constitution"
  date: "Pending"
  method: "In-session workshop review"
  self_cert: false

footer_id: disc-2026-042
footer_project: "AAdvantage Partner-Miles Posting · Stage B"
---

# Stage B Evidence: Field Study — AAdvantage Partner-Miles Posting

> **Reference example.** This artifact is part of `tools/templates/product-discovery/examples/partner-miles-reference/` — a complete A→F worked example demonstrating the discovery workflow with the rich-card discovery template. The data is **synthesized for pedagogical purposes** but represents a realistic exploratory discovery aligned to the AAdvantage loyalty avatar.

---

## Summary

21 member interviews + 6 hours of concept-test + competitive teardown of Delta and United confirmed the Stage A hypothesis: **the pain is the silence, not the delay**. 12/14 Gold members framed the job as "know my earning is safe," not "get miles faster." A read-only status tracker — without partner-side cooperation — has high validated demand and a clear viability signal ($2.4M annual support cost).

---

## Render Gate (ENG-13.1)

> **NON-NEGOTIABLE:** Reviewer ticks exactly one decision below.

- [ ] ✅ **APPROVE** — Field study evidence is complete and validates Stage A hypothesis; Stage C Code Evidence may begin
- [ ] 🔄 **ENHANCE** — Specific evidence gap; agent re-renders (max 3 rounds)
- [ ] ❌ **REJECT** — Hypothesis invalidated or methodology gap; do NOT advance

| Field | Value |
|-------|-------|
| **Reviewer name** | _pending_ |
| **Reviewer role** | Inventor / Discovery Sponsor |
| **Decision timestamp** | _pending_ |
| **Review method** | In-browser render |
| **Self-cert?** | No — initiator (Amal) ≠ reviewer (Adeel) |

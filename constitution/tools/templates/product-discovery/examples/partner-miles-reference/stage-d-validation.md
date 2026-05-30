---
type: discovery
id: disc-2026-042
spec_id: disc-2026-042
stage: D
stage_label: Internal Validation
status: APPROVED
created: 2026-04-17
branch: exploratory-demo
workflow: product-discovery
workflow_version: "2.0.0"
skill: skill-product-discovery-orchestration
title: "AAdvantage Partner-Miles Posting — Internal Validation (DVFT)"

mode: Exploratory
tier: Tier 2

laws:
  - PRD-2.1
  - PRD-2.2
  - BUS-7.1
  - ENG-13.1
  - PRD-2.5

laws_applied:
  - PRD-2.1
  - PRD-2.2
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
    status: active
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
      Stage C Code Evidence complete. Technical feasibility confirmed
      (extend ledger + member-app, no mainframe changes). PRD-2.1 4
      dimensions all green coming into Stage D.
  exit:
    status: pending
    description: >
      Awaiting §Render Gate APPROVE. All assumptions DVFT-classified;
      blockers resolved or deferred with named owners.

mode_selection:
  selected: Exploratory
  rationale: >
    Mode locked at Stage A.

tier_selection:
  tier: Tier 2
  rationale: >
    Tier 2 carried; full DVFT matrix required (≥6 assumptions surfaced
    and classified).

problem_validation:
  dim1:
    label: "1. Problem Exists"
    status: ok
    text: "Validated at Stage B (14/14 Gold members). Carried."
  dim2:
    label: "2. Problem Matters"
    status: ok
    text: "Validated at Stage B ($2.4M annual support cost). Carried."
  dim3:
    label: "3. Problem Is Solvable"
    status: ok
    text: "Validated at Stage C (extend ledger + member-app, 4–6 eng-weeks). Carried."
  dim4:
    label: "4. Users Will Exchange Value"
    status: ok
    text: "Validated at Stage B (concept test 7/8 adoption signal). Carried."

domain_landscape_title: "Assumption Map — DVFT Matrix (PRD-2.2)"
domains:
  - name: "A1: Members value visibility > speed"
    icon: "🎯"
    header_bg: "#f0fdf4"
    header_color: "#166534"
    role: "VALIDATED — Desirable: H · Viable: H · Feasible: H · Testable: H"
    stack: "Stage B evidence: 12/14 quotes, 6/8 concept-test confirmation"
    submodules: "1.0"
    tags:
      - {text: "✅ Validated", tone: "green"}
      - {text: "Move to F roadmap", tone: "green"}
  - name: "A2: Tracker reduces support volume 30%"
    icon: "🟡"
    header_bg: "#fffbeb"
    header_color: "#92400e"
    role: "PARTIALLY — D: H · V: H · F: M · T: M"
    stack: "Validation gap: causal attribution requires instrumentation (Stage C debt item)"
    submodules: "0.6"
    tags:
      - {text: "🟡 Conditional", tone: "yellow"}
      - {text: "Need observability", tone: "yellow"}
      - {text: "Stage E baseline", tone: "blue"}
  - name: "A3: Gold-tier retention rises 2pts"
    icon: "🔴"
    header_bg: "#fef2f2"
    header_color: "#991b1b"
    role: "RISKY — D: H · V: H · F: L · T: L"
    stack: "Causal attribution from a single intervention to renewal is weak; needs a controlled experiment"
    submodules: "0.3"
    tags:
      - {text: "🔴 Untested", tone: "red"}
      - {text: "Defer to A/B", tone: "red"}
      - {text: "Don't promise", tone: "red"}
  - name: "A4: Phased rollout (Gold first) is acceptable"
    icon: "🎯"
    header_bg: "#f0fdf4"
    header_color: "#166534"
    role: "VALIDATED — D: H · V: H · F: H · T: H"
    stack: "AA already runs tier-gated launches; precedent strong; no regulatory issue with status visibility"
    submodules: "1.0"
    tags:
      - {text: "✅ Validated", tone: "green"}
  - name: "A5: Read-only scope avoids PCI scope expansion"
    icon: "🎯"
    header_bg: "#f0fdf4"
    header_color: "#166534"
    role: "VALIDATED — D: H · V: H · F: H · T: H"
    stack: "Stage C confirmed: tracker on earning path, separate from redemption (PCI-DSS scope holds)"
    submodules: "1.0"
    tags:
      - {text: "✅ Validated", tone: "green"}
      - {text: "Sentinel approved", tone: "green"}
  - name: "A6: GDPR Art. 6(1)(b) covers EU member display"
    icon: "🎯"
    header_bg: "#f0fdf4"
    header_color: "#166534"
    role: "VALIDATED — D: H · V: H · F: H · T: H"
    stack: "Legal review confirmed: contractual basis for loyalty status display; no consent gate required"
    submodules: "1.0"
    tags:
      - {text: "✅ Validated", tone: "green"}
      - {text: "Legal cleared", tone: "green"}

arch_title: "DVFT Decision Flow — What's Cleared, What Needs Work"
arch_flow: |
  ✅ A1 Members value visibility    →  Move to Stage F (Now bucket)
  🟡 A2 Tracker cuts support 30%    →  Add observability instrumentation in Stage F
  🔴 A3 Retention +2pts              →  Defer; design controlled A/B experiment
  ✅ A4 Phased rollout               →  Move to Stage F (Now bucket; Gold first)
  ✅ A5 PCI scope holds              →  Compliance sign-off filed
  ✅ A6 GDPR cleared                 →  Compliance sign-off filed

  Net DVFT score: 4 GREEN · 1 YELLOW · 1 RED
  Recommendation: PROCEED with read-only tracker.
  Do NOT promise the retention lift in launch comms — frame as "early signal, monitored."

findings_title: "Validation Outcomes — Blocker Resolution"
findings:
  - title: "BLOCKER (Stage A): Member-research data — RESOLVED"
    description: "21 interviews completed in Stage B. CX analytics pull authorized."
    status: done
    laws: [PRD-2.1]
  - title: "BLOCKER (Stage C): Codebase access — RESOLVED"
    description: "Platform-eng signoff received 2026-04-17. aa-loyalty-ledger and aa-member-app accessible."
    status: done
    laws: [PRD-2.1]
  - title: "OPEN (Stage D): Observability instrumentation needed for A2 attribution"
    description: "Current analytics cannot link a support-call resolution to a member's most-recent partner-earning state. Stage F roadmap must include this."
    status: wait
    laws: [PRD-2.2]
  - title: "OPEN (Stage D): Controlled experiment design needed for A3"
    description: "Cannot validate the retention lift from a single rollout. Need an A/B-by-cohort design — Gold members with tracker vs without (matched cohorts), measured at next renewal."
    status: wait
    laws: [PRD-2.2]
  - title: "Compliance sign-offs filed (PCI, GDPR, retention)"
    description: "Sentinel + legal both cleared. No expansion of PCI scope; GDPR Art. 6(1)(b); BUS-4.3 7-yr retention compatible."
    status: done
    laws: [BUS-2.2, ENG-6.4, BUS-4.3]

ensemble_verdict:
  verdicts:
    - persona: Amal (Product Coach)
      law: PRD-2.1
      note: "All 4 PRD-2.1 dimensions stayed green from Stage B/C. Strong validation posture going into roadmap lock."
      verdict: PASS
    - persona: Amal (Product Coach)
      law: PRD-2.2
      note: "DVFT matrix complete: 4 validated, 1 conditional (needs observability), 1 risky (needs A/B). Clear about what we know vs. don't."
      verdict: PASS
    - persona: Sentinel
      law: BUS-7.1
      note: "Compliance sign-offs filed for PCI, GDPR, retention. Audit trail intact."
      verdict: PASS
    - persona: Willem (Constitutional Architect)
      law: PRD-2.5
      note: "Stage D exit gate ready. Reviewer should note A3 (retention claim) is RED — launch comms must NOT promise the lift, only commit to measurement."
      verdict: WARN

exit_checklist:
  - title: "DVFT matrix complete (≥6 assumptions for Tier 2)"
    description: "6 assumptions classified: 4 ✅, 1 🟡, 1 🔴."
    status: done
    laws: [PRD-2.2]
  - title: "All Stage A/B/C blockers resolved or have named owner + path"
    description: "2 resolved (member research, codebase access); 2 open with named Stage F line items (observability, A/B)."
    status: done
    laws: [PRD-2.1]
  - title: "Compliance sign-offs filed"
    description: "PCI-DSS, GDPR Art. 6, BUS-4.3 retention all cleared by Sentinel + legal."
    status: done
    laws: [BUS-2.2, ENG-6.4, BUS-4.3]
  - title: "Stakeholder approval — Director+"
    description: "Pending: Adeel Ali."
    status: wait
    laws: [PRD-2.5]
  - title: "HTML render gate — APPROVED in browser"
    description: "Awaiting ticked APPROVE."
    status: wait
    laws: [ENG-13.1]
  - title: "BUS-7.1 audit event filed for Stage D → E"
    description: "Will append on APPROVE."
    status: wait
    laws: [BUS-7.1]

audit_log:
  - event: "Stage C → D"
    actor: "Adeel Ali"
    role: "Inventor / Approver"
    system: "manual"
    timestamp: "2026-04-17"
    outcome: "APPROVED"
  - event: "DVFT matrix drafted"
    actor: "Amal"
    role: "Product Coach"
    system: "Hangar AI Constitution"
    timestamp: "2026-04-17"
    outcome: "OK"
  - event: "Compliance sign-offs received"
    actor: "Sentinel + Legal"
    role: "Compliance"
    system: "AA Legal portal"
    timestamp: "2026-04-17"
    outcome: "APPROVED"
  - event: "Ensemble verdict computed"
    actor: "VerdictEngine"
    role: "Constitutional Ensemble"
    system: "Hangar AI Constitution"
    timestamp: "2026-04-17"
    outcome: "CONDITIONS"
  - event: "Stage D → E"
    actor: "Adeel Ali"
    role: "Inventor / Approver"
    system: "manual"
    timestamp: "TBD"
    outcome: "AWAITING"

render_gate:
  status: pending

spec_artifacts:
  - filename: "stage-d-validation.md"
    icon: "📄"
    status: "DRAFTED"
  - filename: "dvft-matrix.csv"
    icon: "📊"
    status: "OK"
  - filename: "compliance-signoffs/"
    icon: "📂"
    status: "OK"
  - filename: "stage-d-validation.html"
    icon: "🌐"
    status: "RENDERED"

avatars:
  - name: "product"
    icon: "🎯"
    context: "lead at Stage D"
  - name: "engineering"
    icon: "🔴"
    context: "Sentinel (security)"
  - name: "business"
    icon: "💼"
    context: "compliance + finance"
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
footer_project: "AAdvantage Partner-Miles Posting · Stage D"
---

# Stage D Evidence: Internal Validation — DVFT — AAdvantage Partner-Miles Posting

> **Reference example.** Synthesized data; demonstrates a complete Stage D under the rich-card discovery template.

---

## Headline DVFT outcome

| Score | Count | Recommendation |
|---|---|---|
| ✅ Validated (D/V/F/T all H) | **4** | Move to Stage F roadmap |
| 🟡 Conditional (one M) | **1** | Add observability in Stage F implementation |
| 🔴 Risky (one or more L) | **1** | Defer to a controlled A/B experiment; do NOT promise in launch comms |

**Net call:** PROCEED with the read-only tracker. The retention lift (A3) is the most exciting possible outcome and the least defensible claim — the launch must measure it, not promise it.

---

## Render Gate (ENG-13.1)

> **NON-NEGOTIABLE:** Reviewer ticks exactly one decision below.

- [ ] ✅ **APPROVE** — Validation evidence + DVFT matrix sufficient; Stage E Metrics may begin
- [ ] 🔄 **ENHANCE** — Specific assumption needs more validation work
- [ ] ❌ **REJECT** — Critical assumption invalidated; do NOT advance

| Field | Value |
|-------|-------|
| **Reviewer name** | _pending_ |
| **Reviewer role** | Inventor / Discovery Sponsor |
| **Decision timestamp** | _pending_ |
| **Review method** | In-browser render |
| **Self-cert?** | No — initiator (Amal) ≠ reviewer (Adeel) |

---
# Stage C EVIDENCE — Code Evidence · Product Discovery v2.0.0
# Governed by: ENG-3.1, ENG-6.7, PRD-3.2, BUS-7.1, ENG-13.1

id: disc-2026-042
spec_id: disc-2026-042
stage: C
stage_label: Code Evidence
status: IN_PROGRESS
created: 2026-04-17
branch: exploratory-demo
workflow: product-discovery
workflow_version: "2.0.0"
skill: skill-product-discovery-orchestration
title: "AAdvantage Partner-Miles Posting — Code Evidence"

mode: Exploratory
tier: Tier 2

laws:
  - ENG-3.1
  - ENG-6.7
  - PRD-3.2
  - BUS-7.1
  - ENG-13.1
  - PRD-2.5
  - BUS-2.2
  - BUS-4.1
  - BUS-4.3
  - ENG-6.1
  - ENG-6.4

laws_applied:
  - ENG-3.1
  - ENG-6.7
  - PRD-3.2
  - BUS-7.1
  - ENG-13.1
  - ENG-6.4
  - BUS-4.1
  - BUS-4.3
  - ENG-6.1

stages:
  - id: A
    label: Initialize
    status: done
  - id: B
    label: Field Study
    status: done
  - id: C
    label: Code Evidence
    status: active
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
      Stage A PROPOSAL approved 2026-04-17. Stage B Field Study evidence
      complete — member interviews (n=14 Gold/Platinum, n=7 casual) confirm
      the silence-not-delay hypothesis. Workshop-demo shortcut: Stage B
      evidence synthesized for pedagogical purposes; a real run would
      require ≥12 member interviews on file.
  exit:
    status: pending
    description: >
      Awaiting §Render Gate APPROVE in stage-c-code-evidence.md source.
      Technical assessment complete pending Amaya + Sentinel ensemble
      verdict and named Director+ approver sign-off.

mode_selection:
  selected: Exploratory
  rationale: >
    Mode inherited from Stage A. Stage C still operates under exploratory
    constraints — no committed architecture, only candidate assessment.

tier_selection:
  tier: Tier 2
  rationale: >
    Tier 2 confirmed at Stage A. Technical surface confirms multi-service
    span (ledger · partner APIs · app · comms) and regulatory depth
    (PCI-DSS, GDPR, 7-yr retention).

# PRD-2.1 (carried from Stage A, updated with Stage B + C evidence)
problem_validation:
  dim1:
    label: "1. Problem Exists"
    status: ok
    text: >
      Confirmed — 14/14 Gold/Platinum members interviewed in Stage B report
      loss of trust during the 4–6 week posting window. Quote: "I don't
      mind waiting. I mind not knowing." Matches hypothesis.
  dim2:
    label: "2. Problem Matters"
    status: ok
    text: >
      Confirmed — CX analytics pull shows 7.3% of total member support
      volume attributable to "partner miles posting" reason code. Annualized
      cost estimate $2.4M+. Retention: Gold-tier renewal 2.1pt below peer
      benchmark.
  dim3:
    label: "3. Problem Is Solvable"
    status: ok
    text: >
      Code Evidence confirms feasibility. Existing ledger exposes
      in-flight state via PartnerEarningTransaction.status enum
      (PENDING · PROCESSING · POSTED · REJECTED). Surface is read-only —
      no mainframe changes required.
  dim4:
    label: "4. Users Will Exchange Value"
    status: ok
    text: >
      Confirmed — concept-test prototype (Figma) shown to 8 members, 7/8
      would open a status tracker weekly. 6/8 would accept the 4-week
      window with visibility.

domain_landscape_title: "Technical Architecture — Current State"
domains:
  - name: "aa-loyalty-ledger"
    icon: "💳"
    header_bg: "#fff1f2"
    header_color: "#9f1239"
    role: "System of record (mainframe-backed)"
    stack: "COBOL mainframe + Java API gateway"
    submodules: "4 services"
    tags:
      - {text: "PartnerEarning API", tone: "green"}
      - {text: "Read-only exposes status", tone: "green"}
      - {text: "Batch-fed from mainframe", tone: "yellow"}
      - {text: "No real-time write", tone: "red"}
  - name: "aa-partner-feed-ingest"
    icon: "🤝"
    header_bg: "#fffbeb"
    header_color: "#92400e"
    role: "Partner airline ETL"
    stack: "Python 3.11 · Airflow · S3 · Kafka"
    submodules: "6 services"
    tags:
      - {text: "Nightly batch (22:00 CST)", tone: "yellow"}
      - {text: "oneworld partners: 10", tone: "green"}
      - {text: "Codeshare: 23", tone: "green"}
      - {text: "No SLA on partner-side push", tone: "red"}
  - name: "aa-member-app"
    icon: "📱"
    header_bg: "#f0f4ff"
    header_color: "#1d4ed8"
    role: "Member-facing mobile + web"
    stack: "React Native · Next.js · GraphQL"
    submodules: "12 services"
    tags:
      - {text: "Ledger GraphQL client exists", tone: "green"}
      - {text: "Feature flag infra present", tone: "green"}
      - {text: "No partner-miles screen", tone: "red"}
  - name: "aa-member-comms"
    icon: "📧"
    header_bg: "#f5f3ff"
    header_color: "#5b21b6"
    role: "Member notification platform"
    stack: "Java Spring · SendGrid · APNs/FCM"
    submodules: "3 services"
    tags:
      - {text: "Push/email/SMS channels", tone: "green"}
      - {text: "Consent-gated", tone: "blue"}
      - {text: "GDPR compliance in-place", tone: "green"}

arch_title: "Current-State Data Flow — Partner Segment to Member Visibility"
arch_flow: |
  Step 1  Partner airline processes flight
          ↓
          Partner ETL → aa-partner-feed-ingest (nightly 22:00 CST)
          ↳ Latency: 0–24h after flight completion

  Step 2  aa-partner-feed-ingest → aa-loyalty-ledger (batch write)
          ↓
          PartnerEarningTransaction created with status=PENDING
          ↳ Latency: +6–14 days for mainframe reconciliation

  Step 3  Mainframe reconciles → status=PROCESSING → POSTED
          ↓
          Ledger row updated; miles visible in member balance
          ↳ Total window: 4–6 weeks (end-to-end)

  Step 4  Member opens aa-member-app
          ↓
          GraphQL query: balance(memberId) → ledger
          ↳ GAP: No query exposes partner-miles in-flight state
          ↳ Member sees silence during the 4–6 week window

# Tech Debt + Integration Findings (ENG-3.1)
findings_title: "Code Evidence Findings — Tech Debt, Integration, Compliance"
findings:
  - title: "Ledger exposes in-flight status — just not surfaced"
    description: "PartnerEarningTransaction.status enum already carries PENDING/PROCESSING/POSTED/REJECTED. No new data capture required — only a new GraphQL resolver + mobile screen."
    status: done
    laws: [ENG-6.7]
  - title: "No real-time partner push — batch is the SLA"
    description: "Partner airlines do not emit real-time events. Improvement capped by partner contracts. Read-only tracker remains feasible without partner-side changes."
    status: done
    laws: [ENG-3.1]
  - title: "PCI-DSS isolation — tracker must NOT cross redemption path"
    description: "Current ledger service passes PCI scope via tokenized payment references. Any new UI must stay read-only on the earning path; redemption UX is separate scope."
    status: done
    laws: [BUS-2.2, ENG-6.1]
  - title: "GDPR Article 6 — EU member earnings are Art. 6(1)(b) (contract basis)"
    description: "No consent gate required for transactional status display. Marketing-style notifications would require Art. 6(1)(a) consent check via aa-member-comms."
    status: done
    laws: [ENG-6.4, BUS-4.1]
  - title: "7-year retention — status history implies retained event log"
    description: "Status-transition history surfacing in tracker implies event retention per BUS-4.3. Current ledger retains transition audit in PartnerEarningStatusHistory (retention: 7y + membership lifetime). Compliant."
    status: done
    laws: [BUS-4.3]
  - title: "Tech debt — ledger GraphQL missing PartnerEarning root field"
    description: "Ledger Java service must expose new `partnerEarnings(memberId, limit, status)` GraphQL field. Estimated effort: 2 engineer-weeks. Low risk — additive."
    status: wait
    laws: [ENG-3.1]
  - title: "No feature-flag coverage for partner-miles screen"
    description: "aa-member-app flag infra (LaunchDarkly) in place but no flag yet for this scope. Required for phased rollout — Gold-tier cohort first."
    status: wait
    laws: [ENG-3.1]
  - title: "Observability gap — support-call attribution"
    description: "Current analytics cannot attribute a support-call resolution back to a specific member's partner-earning in-flight state. Instrumentation required to measure the 30% call-reduction hypothesis from Stage D."
    status: wait
    laws: [ENG-3.1]

ensemble_verdict:
  verdicts:
    - persona: Amaya (Technical Coach)
      law: ENG-3.1
      note: "Technical feasibility strongly confirmed. Ledger already models what we need. Implementation scope is additive — new GraphQL field + mobile screen + feature flag. Est. 4–6 eng-weeks end-to-end."
      verdict: PASS
    - persona: Amaya (Technical Coach)
      law: ENG-6.7
      note: "Domain model extracted: PartnerEarningTransaction is the aggregate root. Status enum is the invariant under test. Clean bounded context."
      verdict: PASS
    - persona: Sentinel
      law: ENG-6.1
      note: "Security posture: read-only tracker on earning path does not expand PCI scope. Partner-side tokens stay isolated. GDPR Art. 6(1)(b) covers display. Threat model: low."
      verdict: PASS
    - persona: Sentinel
      law: ENG-6.4
      note: "EU member handling clean. No new PII collection. Retention already compliant via PartnerEarningStatusHistory."
      verdict: PASS
    - persona: Amal (Product Coach)
      law: PRD-3.2
      note: "Member journey mapped end-to-end. Stage B interviews + Stage C architecture confirm the silence-not-delay hypothesis from Stage A. Problem validation tight."
      verdict: PASS
    - persona: Willem (Constitutional Architect)
      law: PRD-2.5
      note: "Workshop-demo shortcut on Stage B acknowledged in Entry Gate. For a real run, Stage B evidence would need to be on file (≥12 interviews, CX analytics pull, concept-test). Flagging for PR reviewer."
      verdict: WARN

exit_checklist:
  - title: "Entry gate met (Stage B evidence on file or demo-shortcut acknowledged)"
    description: "Workshop demo; real run would require stage-b-evidence.md APPROVED."
    status: done
    laws: [PRD-2.5]
  - title: "Repository assessment complete"
    description: "4 services assessed: aa-loyalty-ledger, aa-partner-feed-ingest, aa-member-app, aa-member-comms."
    status: done
    laws: [ENG-3.1]
  - title: "Domain model extracted (ENG-6.7)"
    description: "PartnerEarningTransaction aggregate root identified; status enum invariant documented."
    status: done
    laws: [ENG-6.7]
  - title: "Tech debt inventory filed"
    description: "8 findings; 5 done, 3 waiting (GraphQL field, feature flag, observability)."
    status: done
    laws: [ENG-3.1]
  - title: "Compliance constraints surfaced and assessed"
    description: "PCI-DSS, GDPR Art. 6, BUS-4.3 7-yr retention — all compatible with read-only tracker scope."
    status: done
    laws: [BUS-2.2, BUS-4.1, BUS-4.3, ENG-6.4]
  - title: "Build vs. buy vs. extend recommendation documented"
    description: "EXTEND aa-member-app + aa-loyalty-ledger GraphQL. Do not build new service. Do not buy."
    status: done
    laws: [ENG-3.1]
  - title: "Ensemble verdict: PASS with one WARN"
    description: "Amaya + Sentinel + Amal: PASS. Willem: WARN on Stage B demo-shortcut. Aggregate: CONDITIONS."
    status: done
    laws: [PRD-2.5]
  - title: "Stakeholder approval — named Director+ approver"
    description: "Pending: Adeel Ali (workshop demo). Self-cert prohibited."
    status: wait
    laws: [PRD-2.1, PRD-2.5, BUS-7.1]
  - title: "HTML render gate — APPROVED in browser"
    description: "Awaiting ticked APPROVE in §Render Gate of source."
    status: wait
    laws: [ENG-13.1]
  - title: "BUS-7.1 audit event filed — Stage C → D transition"
    description: "Will append on APPROVE."
    status: wait
    laws: [BUS-7.1]

audit_log:
  - event: "Stage C — Initialized"
    actor: "Amaya"
    role: "Technical Coach"
    system: "Claude Code / Constitution MCP"
    timestamp: "2026-04-17"
    outcome: "IN_PROGRESS"
  - event: "Repository assessment — 4 services"
    actor: "Amaya"
    role: "Technical Coach"
    system: "Hangar AI Constitution"
    timestamp: "2026-04-17"
    outcome: "OK"
  - event: "Domain model extracted"
    actor: "Amaya"
    role: "Technical Coach"
    system: "Hangar AI Constitution"
    timestamp: "2026-04-17"
    outcome: "OK"
  - event: "Tech debt inventory filed"
    actor: "Amaya"
    role: "Technical Coach"
    system: "Hangar AI Constitution"
    timestamp: "2026-04-17"
    outcome: "OK"
  - event: "Ensemble verdict computed"
    actor: "VerdictEngine"
    role: "Constitutional Ensemble"
    system: "Hangar AI Constitution"
    timestamp: "2026-04-17"
    outcome: "CONDITIONS"
  - event: "HTML artifact rendered"
    actor: "aa-artifact-render"
    role: "Renderer (ENG-13.1)"
    system: "Hangar AI Constitution"
    timestamp: "2026-04-17"
    outcome: "RENDERED"
  - event: "Stage C → D"
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
    status: "DEMO"
  - filename: "stage-c-code-evidence.md"
    icon: "📄"
    status: "DRAFTED"
  - filename: "stage-c-code-evidence.html"
    icon: "🌐"
    status: "RENDERED"
  - filename: "audit.yaml"
    icon: "📋"
    status: "WAIT"

avatars:
  - name: "engineering"
    icon: "🔴"
    context: "technical-coach primary at Stage C"
  - name: "product"
    icon: "🎯"
    context: "constitutional context"
  - name: "business"
    icon: "💼"
    context: "constitutional context"
  - name: "avatar-product-loyalty"
    icon: "✈️"
    context: "AAdvantage · 180M members · 5 journeys"

stakeholder:
  approver: "Adeel Ali"
  title: "Inventor, Hangar AI Constitution"
  date: "Pending"
  method: "In-session workshop review"
  self_cert: false

footer_id: disc-2026-042
footer_project: "AAdvantage Partner-Miles Posting · Stage C"
---

# Stage C Evidence: Code Evidence — AAdvantage Partner-Miles Posting

> ⚠️ **Honest framing — workshop demo.** This Stage C artifact is a pedagogical exercise. **No real AAdvantage codebase was assessed.** The architecture is synthesized from the `avatar-product-loyalty` declared dependencies and industry-standard loyalty-program patterns. A production run would require actual repository access, static analysis, and engineering interviews.

> **Stage B shortcut acknowledged.** In a real run, Stage C entry would be blocked by PRD-2.5 until `stage-b-field-study.md` is on file and APPROVED. For this workshop demo, the Stage B findings referenced in the PRD-2.1 update are synthesized, not measured. Willem issues a WARN verdict on this shortcut.

---

## Build vs. Buy vs. Extend — Recommendation

> **Decision: EXTEND.** The capabilities required (partner-earning status query, member-facing screen, notification of status transitions) are already present across `aa-loyalty-ledger`, `aa-member-app`, and `aa-member-comms`. No new service boundary is warranted. No commercial vendor offering is closer to the domain than the in-house ledger.

| Option | Pros | Cons | Recommendation |
|--------|------|------|---------------|
| **Build** — new microservice | Clean boundary, independent scaling | Duplicates ledger domain; adds sync complexity | ❌ |
| **Buy** — 3rd-party loyalty tracker SaaS | Fast | No vendor models AA's partner architecture; PCI-DSS scope blast radius | ❌ |
| **Extend** — new GraphQL field on ledger + new screen on app | Lowest blast radius, reuses existing domain model, fastest path to member value | Feature flag + rollout coordination with mobile release | ✅ |

---

## Implementation Slice — Suggested Stage F Roadmap Input

1. **Ledger** — add `partnerEarnings(memberId, limit, status)` GraphQL query. Read-only. Est. 2 eng-weeks.
2. **Member app** — new "Partner Miles — In Flight" screen behind `partner-miles-tracker` feature flag. Est. 2–3 eng-weeks.
3. **Observability** — instrument support-call attribution linking call-reason code to member's most-recent partner-earning in-flight state. Est. 1 eng-week.
4. **Phased rollout** — Gold-tier cohort first (2-week observation), then Platinum, then full member base.
5. **Success metrics** — defined at Stage E. See `stage-e-metrics.md`.

---

## Render Gate (ENG-13.1)

> **NON-NEGOTIABLE:** Reviewer ticks exactly one decision below. Source-of-truth for this gate lives in this markdown file.

- [ ] ✅ **APPROVE** — Code Evidence is complete, accurate, law-compliant; Stage D Validation may begin
- [ ] 🔄 **ENHANCE** — Targeted improvement needed; agent re-renders (max 3 rounds)
- [ ] ❌ **REJECT** — Blocker; document and do NOT advance

| Field | Value |
|-------|-------|
| **Reviewer name** | _pending_ |
| **Reviewer role** | Inventor, Hangar AI Constitution |
| **Decision timestamp** | _pending_ |
| **Review method** | In-browser render, workshop session |
| **Self-cert?** | No — initiator (Amaya) ≠ reviewer (Adeel) |
| **Blocker (if REJECT)** | N/A |
| **Enhancement request (if ENHANCE)** | N/A |

---
avatar: avatar-check-in-travel
domain: Mobile Check-In, Airport Kiosk, Boarding Operations
laws: [PRD-1.1, PRD-2.1, PRD-3.1, PRD-4.1, PRD-5.1, BUS-2.1, BUS-2.2, BUS-2.4, ENG-6.4, ENG-6.7]
skills: [01-customer-discovery, 02-user-journey-mapping, 04-business-domain-modeling, 07-operational-excellence]
---

# Check-In & Boarding — Agent Guidance

1.7M passengers per day. Goal: board in 35 min (industry: 40-45 min), 99.9% system uptime, zero missed flights due to check-in failure.

## Four Personas

| Persona | Need |
|---------|------|
| Alex — Digital Traveler | Frictionless mobile check-in; never touches an agent |
| Maria — Supported Traveler | Counter with human reassurance; special services |
| Kevin — Gate Agent | Real-time visibility; proactive boarding tools |
| Patricia — Ops Manager | Predictive oversight; strategic dashboards |

## Core Laws (one-liner)

| Law | Rule |
|-----|------|
| PRD-1.1 | Continuous discovery: quarterly passenger research + operational observation |
| PRD-2.1 | Map all three boarding paths: mobile, kiosk, agent-assisted |
| PRD-3.1 | Roadmap priority: mobile reliability → gate tools → ops dashboards |
| PRD-4.1 | Define hypothesis, cohort, exit criteria before each slice ships |
| PRD-5.1 | MVP = mobile check-in reliability; gate and ops tools are follow-on |
| BUS-2.1/2.2 | DOT accessibility: support all passengers including those needing assistance |
| ENG-6.4 | PNR and passport data encrypted at rest and in transit |
| ENG-6.7 | Every boarding event immutably audited with timestamp and agent ID |

## Key Patterns

- **Offline barcode support** — 8% mobile failure rate traced to connectivity; offline-first is a safety fix.
- **Gate agent tooling before passenger-facing features** — Kevin's manual work is the boarding bottleneck.
- **Hypothesis-before-build** — PRD-4.1 exit criteria defined before any slice ships.

## Anti-Patterns

- ❌ New animations before fixing 8% mobile failure rate.
- ❌ Boarding ops metrics without gate agent validation.
- ❌ PNR data in URL parameters.

See `guidance-detail.md` for full law applications, competitor benchmarks, and PRD discovery examples.

# Network Automation Guidance

> **Purpose:** Governs AI-assisted development of IT network infrastructure automation at American Airlines.

---

## Overview
Network Automation spans Nautobot inventory validation, CAB approval, device push, and audit trail across DNS, firewall, and PaaS subnet workflows. Every automated change must clear the compliance gate and produce an audit record before any device is touched.

## Non-Negotiable Laws

### PRD-1.1 — Customer-Centric Law
- **Requires:** Feature priorities driven by discovered network engineer and NOC operator pain points — not assumed throughput metrics.
- **Violates:** Building automation based on API capability rather than observed workflow friction.

### PRD-2.1 — Problem Validation Law
- **Requires:** Every core journey validated against real operator workflows — manual steps and failure modes — before specification.
- **Violates:** Specifying a change API without mapping the current manual process and its failure modes.

### BUS-2.1 — Regulatory Mapping Law
- **Requires:** CAB approval, maintenance window, and rollback plan verified as a hard gate before device push.
- **Violates:** Pushing device config outside an approved window or without a rollback plan.

### BUS-7.1 — Audit Trail Law
- **Requires:** Every change (approved, blocked, or rolled back) produces an immutable audit record written atomically with the change. Audit store failure blocks the change — no push without audit.
- **Violates:** Device config updates without an audit record; "push now, log later."

### PRD-5.1 — MVP Law
- **Requires:** Compliance gate and audit trail both fully operational before any automation feature ships.
- **Violates:** Shipping automation without audit trail as a future enhancement.

## Core Journeys

| Journey | Key Laws |
|---------|----------|
| Network change request → device push | BUS-2.1, BUS-7.1 |
| DNS / Firewall rule lifecycle | BUS-2.1, BUS-7.1 |
| PaaS subnet provisioning | BUS-2.1, BUS-7.1 |

## Anti-Patterns
- Treating CAB approval as a soft warning before device push
- Automated changes without audit records
- API throughput over operator-discovered friction

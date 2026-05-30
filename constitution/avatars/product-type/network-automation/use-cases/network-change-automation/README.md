# Use Case: Firewall Rule Change Automation

## Context
A network engineer needs to open a new firewall rule to allow a PaaS application to communicate with a downstream data service. The change must be approved by CAB, executed within a maintenance window, pushed to the firewall device via the Apigee Project42 Firewall API + Nautobot, and fully audited.

## Trigger
Network engineer receives a Jira ticket: "Allow outbound TCP/443 from PaaS subnet 10.20.30.0/24 to data API endpoint 10.50.60.10 for project42-netmonitor service." Engineer initiates a network change request in the Network Automation platform.

## Happy Path

**1. Change request creation**
Engineer opens a new network change request. The platform pulls the PaaS subnet record from Nautobot (validated against `project42-netmonitor` service entry). Request form pre-populates `source_cidr`, `destination_ip`, `protocol: TCP`, `port: 443`, and device target (edge firewall `fw-core-01`). Engineer adds description and submits. ServiceNow change ticket `CHG0012345` created with status `Draft`.

**2. Rollback plan generation**
Platform generates a rollback plan: "Remove ACL entry — revert `fw-core-01` to previous running config snapshot taken at request time." Engineer reviews and approves rollback plan. Ticket status advances to `Review`.

**3. CAB approval**
IT Change Manager opens the CAB queue. Platform surfaces the Nautobot device record, current ACL state, and rollback plan in the approval view — no separate system access required. Change Manager approves. Ticket status: `Approved`. Maintenance window set: `2026-04-29 02:00–04:00 UTC`.

**4. Compliance gate evaluation (automated — at push time)**
At `2026-04-29 02:05 UTC`, engineer initiates push from the platform:
```
✅ CAB Approval:       CHG0012345 = Approved
✅ Maintenance Window: 02:05 UTC is within 02:00–04:00 UTC
✅ Device Target Match: fw-core-01 matches approved target list
✅ Rollback Plan:       Present (snapshot ID: snap-fw-core-01-20260429T0200Z)
→ COMPLIANCE GATE: PASS — dispatching Nautobot job
```

**5. Nautobot job dispatch and device push**
Platform dispatches Nautobot job `job-fw-acl-20260429-001` to `fw-core-01`. ACL entry pushed via the Apigee Project42 Firewall API. Device returns `STATUS: 200 — ACL applied`.

**6. Audit record written (atomic with push)**
```
correlation_id:     CHG0012345:fw-core-01:2026-04-29T02:05:33Z
change_ticket_id:   CHG0012345
actor:              jdoe@aa.com
device_hostname:    fw-core-01
action_type:        PUSH
compliance_state:   APPROVED
outcome:            SUCCESS
pushed_at:          2026-04-29T02:05:33Z
```

**7. Post-push diff verification**
Platform queries `fw-core-01` running config and diffs against expected state. ACL entry confirmed present. `verified_at` timestamp written to audit record. ServiceNow ticket advanced to `Closed — Successful`.

**8. MOCCA Monitor correlation**
MOCCA Monitor detects a brief traffic spike on `fw-core-01` at `02:05:40 UTC`. Alert auto-enriched with `correlation_id: CHG0012345:fw-core-01:...` from the audit stream — NOC operator sees immediately that the anomaly is tied to an approved change. No incident ticket opened.

## Failure Scenarios

**F1 — Out-of-window push attempt:**
Engineer attempts push at `01:50 UTC` (before window opens).
```
🔴 COMPLIANCE GATE FAIL: Current time 01:50 UTC is outside approved window 02:00–04:00 UTC.
Push blocked.
```
Blocked-attempt audit record written. Engineer notified to retry after 02:00 UTC.

**F2 — Post-push verification fails:**
ACL entry not found in running config diff. Platform immediately initiates rollback using snapshot `snap-fw-core-01-20260429T0200Z`. Rollback audit record written:
```
action_type:   ROLLBACK
outcome:       SUCCESS
failure_reason: Post-push diff — ACL entry not present in running config
```
ServiceNow ticket advanced to `Closed — Unsuccessful`. Network engineer notified with rollback correlation ID.

**F3 — Audit store unavailable at push time:**
Audit store returns connection error. Platform aborts push:
```
🔴 AUDIT STORE UNAVAILABLE — push aborted. Device configuration NOT modified.
Retry after audit store is restored. Incident: INC-AUDIT-20260429-001 opened automatically.
```
No device configuration change occurs. No partial audit state.

## Laws Applied

| Law | Application |
|-----|-------------|
| BUS-2.1 | Compliance gate evaluates CAB approval, maintenance window, device target match, and rollback plan before push |
| BUS-7.1 | Audit record written atomically with push; blocked attempts and rollbacks also audited; `correlation_id` propagated to MOCCA Monitor |
| PRD-1.1 | Feature design driven by discovered pain (cross-system validation friction, out-of-window incidents) not throughput assumptions |
| PRD-2.1 | Current-state journey mapped (8-step manual process with 3 failure modes) before automation specified |
| PRD-5.1 | MVP ships when compliance gate, audit trail, and post-push verification are all operational |

## Success Metrics
- Time from change request creation to device push: ≤10 min (baseline: 45 min manual)
- Out-of-window push incidents: 0 (baseline: 3 in last 6 months)
- Audit record completeness: 100% of pushes, blocks, and rollbacks (baseline: ~60%)
- NOC MTTC (mean time to correlate alert to change): ≤2 min (baseline: 30+ min manual correlation)

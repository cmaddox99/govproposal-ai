# Network Automation Personas

These personas represent typical users of American Airlines Network Automation tooling (Nautobot, DNS lifecycle, firewall rule management, MOCCA monitoring, PaaS subnet provisioning). Use them to ground product decisions in real user needs.

---

## Network Engineer

**Role:** Senior Network Engineer, Enterprise Networking

**Responsibilities:**
- Design and implement network changes across campus, data center, and PaaS environments
- Author Nautobot change requests and validate device targets before push
- Coordinate with NOC and Change Management on maintenance windows and rollback plans

**Goals:**
- Push approved changes safely with a single consolidated workflow
- Eliminate manual cross-system validation between Nautobot, ServiceNow, and device CLI
- Cut mean time to push from 45 min → ≤10 min per change

**Pain Points:**
- Manually cross-references Nautobot inventory, ServiceNow CAB, and device CLI for every change (~45 min)
- No automated rollback — reverting failed config takes 20–90 min
- Out-of-window pushes happen 3×/6mo because window enforcement is manual

**Tech Environment:**
- Nautobot for source-of-truth inventory
- ServiceNow for change records and CAB approval
- Device CLI (Cisco IOS/NX-OS, Juniper) and Ansible for execution

**Success Metrics:**
- Mean time to push: 45 min → ≤10 min
- Out-of-window incidents: 3/6mo → 0
- Rollback time: 20–90 min → ≤5 min

---

## NOC Operator

**Role:** Network Operations Center Operator (24×7 shift)

**Responsibilities:**
- Monitor MOCCA / Eagle Eye alerts and triage network anomalies
- Correlate alerts to recent changes and engage on-call engineers
- Execute approved emergency rollbacks during incidents

**Goals:**
- Correlate every alert to the originating change in <2 min
- Reduce mean time to detect change-induced incidents
- Have one-click rollback on the most recent change when correlation is confirmed

**Pain Points:**
- MOCCA alerts don't carry the change ID that triggered the anomaly — adds 30+ min to root cause analysis
- Manual lookups across 3 tools to identify "what changed in the last hour"
- No standardized rollback runbook surfaced at alert time

**Tech Environment:**
- MOCCA / Eagle Eye monitoring dashboards
- ServiceNow incident queue
- Nautobot for change history lookup

**Success Metrics:**
- Alert-to-change correlation: 30+ min → <2 min
- MTTR for change-induced incidents: 60 min → ≤20 min

---

## Platform/Cloud Engineer

**Role:** Platform Engineer responsible for PaaS subnet provisioning and DNS lifecycle

**Responsibilities:**
- Provision PaaS subnets and DNS records for product teams via self-service APIs
- Manage Apigee-fronted DNS lifecycle automation
- Maintain firewall rule request workflows for cross-zone connectivity

**Goals:**
- Provide self-service provisioning so product teams aren't blocked on tickets
- Ensure every API-triggered change still flows through CAB and audit
- Reduce time-to-provision from days to minutes

**Pain Points:**
- Product teams open ServiceNow tickets that take 2–5 days to resolve
- API-triggered changes bypass change governance unless integrated explicitly
- DNS record sprawl with no automated decommission of stale records

**Tech Environment:**
- Apigee API gateway for DNS lifecycle
- Terraform / Ansible for PaaS subnet provisioning
- Nautobot, Infoblox

**Success Metrics:**
- Time-to-provision (subnet/DNS): 2–5 days → ≤30 min
- Stale DNS records: ~15% → ≤2%
- API-triggered changes with full audit trail: ~60% → 100%

---

## IT Change Manager

**Role:** IT Change Manager — Network Change Advisory Board (CAB) chair

**Responsibilities:**
- Review and approve / reject network change requests in the weekly CAB
- Validate that each request has device targets, maintenance window, and rollback plan
- Investigate failed or out-of-window changes and own corrective action

**Goals:**
- Approve well-formed changes quickly and reject incomplete ones early
- Achieve 100% audit completeness for every executed change
- Drive CAB rejection rate down by improving request quality upstream

**Pain Points:**
- 2–4 hours/week prepping CAB by manually validating device targets against Nautobot
- ~15% of submitted changes are rejected for missing rollback plan or window — late in the cycle
- Audit completeness is ~60% because change events aren't immutably linked to requests

**Tech Environment:**
- ServiceNow CAB workflow
- Nautobot for inventory validation
- Audit log tooling for compliance reporting

**Success Metrics:**
- CAB prep time: 2–4 hr/week → ≤30 min/week
- CAB rejection rate: 15% → ≤3%
- Audit completeness: ~60% → 100%

# Use Case: IROP Single Flight Cancellation — Crew Recovery

## Context
A SOC (System Operations Center) crew scheduler handles crew recovery after a single domestic flight is cancelled due to mechanical issues. The crew recovery solver presents eligible reassignment options for all affected crew members. The scheduler reviews options and commits assignments within the IROP management window.

## Trigger
Flight status published as `CANCELLED` with reason `MECHANICAL` for AA1234 (BOS→DFW). Four crew members (2 pilots, 2 flight attendants) are stranded at BOS.

## Happy Path

1. **IROP event ingestion** — CWR receives `FLIGHT_CANCELLED` event for AA1234 with `correlation_id: cwr-event-{uuid}`. Affected crew roster resolved: [crew-001, crew-002, crew-003, crew-004].

2. **FAR 117 eligibility screening** — For each crew member, `FARPart117EligibilityService` computes eligible window based on last duty period end. crew-003 has only 7.5 hours available rest — all options for crew-003 will be filtered to eligible assignments only.

3. **Recovery option generation** — Available flights from BOS within eligibility windows are queried. Options scored: `far_117_margin_hours` (40%), `experience_match_score` (30%), `proximity_score` (20%), `fatigue_score` (10%).

4. **Options presented to scheduler** — Scheduler sees sorted list per crew member. crew-003 shows only 2 options (limited by FAR 117 constraint). Each option shows `recovery_score` and top contributing factor.

5. **Scheduler commits assignments** — Scheduler selects options for crew-001, crew-002, crew-004 from top suggestions. For crew-003, scheduler selects the lower-ranked option (better aircraft experience) and enters justification: "NCOIC certified A321 — required for BOS-SFO night ops."

6. **Audit records written** — Five audit records written atomically (4 accepts + 1 override). Each record carries `correlation_id: cwr-event-{uuid}`, FAR 117 compliance state, recovery score, and override justification for crew-003.

7. **Crew notification dispatched** — All 4 crew members notified of new assignments within 5 minutes of scheduler commitment.

## Failure Scenarios

**Scenario F1 — FAR 117 violation attempt:** Scheduler attempts to manually enter a crew ID not in the eligible options list (crew member is ineligible). System blocks submission: "Crew member 00X does not satisfy FAR 117.25(a) rest requirement (6.5h available, 10.0h required)." No audit record written for the blocked attempt; warning logged with correlation ID.

**Scenario F2 — Audit write failure:** Atomic audit write fails (store unavailable). CWR rolls back assignment commitment — crew roster is NOT updated. Scheduler sees: "Assignment could not be committed — audit system unavailable. Please retry or contact SOC IT." IROP event remains open in recovery queue.

**Scenario F3 — No eligible options for crew member:** crew-003 has zero eligible flights within FAR 117 window. System presents "Deadhead Home" as the only available option. Scheduler selects deadhead; `decision_type: SYSTEM_AUTO` audit record written.

## Laws Applied

| Law | Application in this use case |
|-----|------------------------------|
| BUS-2.1 | FAR 117 eligibility check run before options presented; ineligible options never displayed |
| PRD-1.5 | Options ranked by evidence-scored recovery_score with factor breakdown visible to scheduler |
| BUS-7.1 | Audit record written for every accept, override, and system-auto decision |
| ENG-6.7 | correlation_id propagated from IROP event through all audit records and log lines |
| PRD-5.1 | This use case represents the complete MVP — all safety gates present |

## Success Metric
All 4 crew members assigned to legal (FAR 117-compliant) replacement flights within 15 minutes of IROP event, with complete audit trail and crew notification within 5 minutes of assignment commitment.

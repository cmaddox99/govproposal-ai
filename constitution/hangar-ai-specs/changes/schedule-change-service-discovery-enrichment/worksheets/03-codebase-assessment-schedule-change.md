# Worksheet 03: Codebase Assessment - Schedule Change Self-Serve

**Purpose:** Capture concrete system inventory and technical constraints from source repositories.  
**Law Anchor:** ENG-2.3, ENG-6.7, ENG-10.1  
**Status:** In Progress (first-pass code evidence captured)

---

## In-Scope Repositories

| Repo | Language/Stack | Role in Journey | Analysis Priority |
|------|----------------|-----------------|-------------------|
| schedule-change-ui | React + TypeScript | Customer and agent interactions | High |
| schedule-change-bff | Java 21 + Spring Boot | Orchestration and API aggregation | Highest |
| schedule-change-eligibility-service | Java 21 + Spring Boot | Rule evaluation | Highest |
| schedule-change-reservation-history-service | Java 21 + Spring Boot | Audit/history retrieval | High |
| drss-schedule-change-reservation-service | Java 21 + Spring Boot | Booking mutation execution | High |
| drss-remarks-service | Java + service integration | Remarks and override context | Medium |

### Stage C Execution Status (2026-03-11)

| Task | Status | Notes |
|------|--------|-------|
| C1 Repository availability audit | Complete | Completed via SSH host alias `github-aa` |
| C2 Repository acquisition | Complete | Core repos and dependencies cloned to `service-recovery/` |
| C3 Service call graph extraction | Complete | BFF -> reservation-history, reservation, cancel services mapped from code |
| C4 API contract extraction | Complete | Primary endpoints captured for BFF, eligibility, history, DRSS reservation, DRSS remarks |
| C5 Reliability/idempotency/fallback extraction | Complete | Circuit breaker config and fallback/error pathways identified |
| C6 Observability/audit extraction | Complete | PNR/transaction logging and MDC/trace propagation points identified |
| C7 Claim reclassification | Complete | Evidence table moved from pending to code-evidenced for extracted categories |

---

## Discovery Questions

1. Where is the canonical eligibility decision path implemented?
2. What contracts exist between BFF and downstream services?
3. Which code paths handle retries/timeouts and can cause duplicate actions?
4. Where are decision and override audit events persisted today?
5. Which modules have weak/no automated test coverage?

---

## Evidence Capture Table

| Category | Expected Evidence | Status | Notes |
|---------|-------------------|--------|-------|
| API contracts | OpenAPI specs or DTO contracts | Code-evidenced | BFF endpoints include `/change-details`, `/view-res/deeplink`, `/cancel/url`, `/cancel/eligibility`. Downstream contracts include history `/retrieveReservationChangeInfo`, eligibility `/eligibility`, reservation `/reservations/{pnr}` + `/reservations/eligibility/{pnr}`, remarks `dynamicreaccom/schedule-change`. |
| Rule engine | Eligibility decision model and reason mapping | Partially code-evidenced | Eligibility flow entrypoint confirmed at `schedule-change-eligibility-service` `/eligibility`; detailed reason-code mapping still pending deeper service-level extraction. |
| Observability | Tracing/metrics/logging instrumentation points | Code-evidenced | BFF logging includes trace/PNR MDC pattern; context propagation enabled (`Hooks.enableAutomaticContextPropagation` + MDC accessor). Reservation history uses Reactor `contextWrite` with `recordLocator`. Multiple controllers/services log PNR and transaction IDs. |
| Testing | Unit/integration/contract coverage snapshot | Code-evidenced | Test inventory snapshot by repo: BFF `32` unit / `3` integration files, Eligibility `23` / `0`, Reservation History `22` / `0`, DRSS Reservation `27` / `3`, DRSS Remarks `16` / `8`. Contract-test coverage remains to be validated. |
| Reliability controls | Retries, fallbacks, idempotency protections | Code-evidenced | Resilience controls present (`@CircuitBreaker` and hystrix circuitBreaker settings). BFF downstream calls include fallback behavior (e.g., empty/default responses and mapped server-error handling). |

---

## Stage C First-Pass Code Evidence (File-Backed)

### C3. Service Call Graph (Code-Evidenced)

1. UI -> BFF via BFF controller endpoints (`/change-details`, `/cancel/*`, `/view-res/deeplink`).
2. BFF `ScheduleChangeController#getChangeDetails` orchestrates:
	 - `RetrieveScheduleChangeReservationService#getReservation` -> reservation service path `/reservations/eligibility/{pnr}`.
	 - `ReservationChangeInfoService#getChangeInformation` -> history service path `/retrieveReservationChangeInfo`.
3. BFF cancel flow calls:
	 - Reservation without eligibility `/reservations/{pnr}`.
	 - Cancel API paths `eligibility` and `init` through cancel WebClient.
4. DRSS history service exposes `/retrieveReservationChangeInfo` and `/update/{recordLocator}`.
5. Apigee history proxy basepath `/sch-ch-history` routes to reservation-history-service internal cluster target.

### C4. API Contract Evidence (Code-Evidenced)

- BFF contracts observed in controllers:
	- `POST /change-details`
	- `POST /view-res/deeplink`
	- `POST /cancel/url`
	- `GET /cancel/eligibility`
- Eligibility service contract observed:
	- `POST /eligibility`
- Reservation history contracts observed:
	- `POST /retrieveReservationChangeInfo`
	- `PUT /update/{recordLocator}`
- Reservation service contracts observed:
	- `GET /reservations/{pnr}`
	- `GET /reservations/eligibility/{pnr}`
- Remarks service contract observed:
	- `POST /dynamicreaccom/schedule-change`

### C5. Reliability / Fallback Evidence (Code-Evidenced)

- BFF application uses `@CircuitBreaker(name = "SCCircuitBreaker")` and has circuit-breaker settings in `application.yml`.
- BFF call wrappers include explicit `onErrorResume` handlers and default responses (e.g., Schedule Change response fallback and reservation/cancel fallback objects).
- Reservation history client maps downstream HTTP failures into domain-specific exceptions for unauthorized/500/other server errors.

### C6. Observability / Audit Evidence (Code-Evidenced)

- BFF logging pattern includes trace fields and `PNR=%X{recordLocator}` MDC support.
- BFF enables Reactor context propagation and registers MDC thread-local accessor.
- Reservation history controller writes `recordLocator` into Reactor context for downstream logging correlation.
- Eligibility, reservation, and remarks controllers/services log request/response context with PNR or transaction IDs.

---

## Exit Criteria

- [ ] Service call graph documented for eligibility-to-rebooking path
- [ ] Top 5 latency/error hotspots identified with evidence
- [ ] Test coverage risk map created by service
- [ ] Brownfield preservation constraints documented for Slice 1

---

## Judicial Review Checkpoint

**JR-003 Ruling:** Stage C evidence extraction approved to proceed.

**Evidence:** In-scope repositories successfully cloned using the user SSH host alias `github-aa`.

**Corrective Action:** Execute C3-C7 and update evidence tables with file-backed findings.

**JR-004 Ruling:** First-pass Stage C extraction accepted.

**Evidence:** Cross-repo controller/service/config analysis yielded call graph, contract, reliability, and observability artifacts with code-backed traces.

**Corrective Action:** Proceed to deep extraction for rule-reason mapping and testing coverage snapshot.

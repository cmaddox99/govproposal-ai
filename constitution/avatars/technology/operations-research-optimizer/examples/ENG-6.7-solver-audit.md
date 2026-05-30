---
law_id: ENG-6.7
avatar: operations-research-optimizer
---

# ENG-6.7: Audit Trail Examples for Operations Research / MIP Optimizer

---

## COMPLIANT: Solver Run Logged with Full Context

```java
// ✅ Every solve attempt produces an immutable audit record
@Slf4j
@Component
public class MathModel {

    private static final String CLASS_NAME = MathModel.class.getSimpleName();

    public SolverResult solveMathModel(XpressOptimizer optimizer, RunContext runContext) {
        long startMs = System.currentTimeMillis();

        optimizer.solve();

        long solveTimeMs = System.currentTimeMillis() - startMs;
        int status       = optimizer.getSolverStatus();
        double objective = optimizer.getObjectiveValue();
        int variables    = optimizer.getNumberOfVariables();
        int constraints  = optimizer.getNumberOfConstraints();

        // ✅ Immutable audit record — snapshot ID ties this to the exact run
        log.info("[{}] snapshotId={} status={} objective={} solveTimeMs={} variables={} constraints={}",
                CLASS_NAME,
                runContext.getSnapshotId(),
                SolverStatus.fromCode(status),
                objective,
                solveTimeMs,
                variables,
                constraints);

        return SolverResult.of(status, objective, solveTimeMs);
    }
}
```

**Why compliant:** Every field is meaningful for post-run analysis — status distinguishes OPTIMAL from INFEASIBLE, objective value is the quality metric, solve time flags performance regressions, and the snapshot ID ties the record to the exact trigger. All fields are logged together so the record is atomic.

---

## COMPLIANT: Run Lifecycle Status Changes Logged

```java
// ✅ Run status transitions are auditable — each state change is logged with snapshot ID
@Slf4j
@Service
public class RunStatusServiceImpl implements RunStatusService {

    private static final String CLASS_NAME = RunStatusServiceImpl.class.getSimpleName();

    @Override
    public void updateStatus(String snapshotId, RunStatus status) {
        log.info("[{}] snapshotId={} status={} timestamp={}",
                CLASS_NAME, snapshotId, status, Instant.now());
        // persist to status store
        statusRepository.upsert(snapshotId, status, Instant.now());
    }
}

// Usage in pipeline — every transition is recorded:
// RUNNING → COMPLETED or RUNNING → FAILED
runStatusService.updateStatus(runContext.getSnapshotId(), RunStatus.RUNNING);
// ... pipeline executes ...
runStatusService.updateStatus(runContext.getSnapshotId(), RunStatus.COMPLETED);
```

**Why compliant:** Status transitions form a chronological audit trail. A FAILED status followed by a RUNNING status (on retry) is reconstructible from logs. The `snapshotId` is the correlation key across all log lines for a run.

---

## COMPLIANT: Config Logged at Run Start

```java
// ✅ Config state captured at the moment of loading — run is reproducible
@Slf4j
@Component
public class DtoProcessor {

    private void loadConfig(Config loadedConfig) {
        BeanUtils.copyProperties(loadedConfig, runContext.getConfig());

        // ✅ Full config logged — any run can be reproduced by restoring this config
        log.info("[DtoProcessor] snapshotId={} config={}",
                runContext.getSnapshotId(),
                runContext.getConfig().toString());  // Lombok @ToString covers all fields

        if (runContext.getConfig().isEnableExperimental()
                && runContext.getConfig().getExperimentalScoringProfile() != null
                && runContext.getConfig().getExperimentalScoringProfile().hasAnyOverrides()) {
            log.info("[DtoProcessor] snapshotId={} experimentalOverrides={}",
                    runContext.getSnapshotId(),
                    runContext.getConfig().getExperimentalScoringProfile());
        }
    }
}
```

**Why compliant:** The config state at run time is logged before the pipeline begins. If a scheduler questions why the solution looked different on a particular day, the config log entry answers it without needing to inspect files or blob storage.

---

## VIOLATION: Solver Result Not Logged

```java
// ❌ VIOLATES ENG-6.7 — solver completes with no audit record
public void solveMathModel(XpressOptimizer optimizer) {
    optimizer.solve();
    // No log statement — status, objective, and solve time silently discarded
    // If this run is questioned later, there is no evidence of what the solver produced
}
```

**Why violates ENG-6.7:** Scheduler decisions are based on the optimizer's output. If a scheduling error is traced back to a JOSE run, there must be an immutable record of what the solver reported. Absence of a log means the run cannot be audited or reproduced.

---

## VIOLATION: Run Status Updated Without Logging

```java
// ❌ VIOLATES ENG-6.7 — status change is persisted but not logged
public void updateStatus(String snapshotId, RunStatus status) {
    statusRepository.upsert(snapshotId, status, Instant.now());
    // No log — a FAILED status 3 weeks ago is invisible unless someone queries the DB
}
```

**Why violates ENG-6.7:** The audit trail requirement means sensitive operations must produce a log entry, not just a database record. Log aggregation (Splunk, Azure Monitor) is the primary tool for incident investigation — a DB-only record is effectively invisible during an outage.

---

## VIOLATION: MDC Context Not Set — Snapshot ID Missing from Logs

```java
// ❌ VIOLATES ENG-6.7 — log lines have no correlation key
// All log output from this run is indistinguishable from other concurrent runs
@Override
public void run(String... args) {
    // MDC never populated — snapshotId never added to logging context
    inputDataService.prepareInputData();
    optionGenerationService.generateFeasibleOptions(bundle);
    // Logs look like:
    // INFO  Fetching student schedules for APR2025
    // INFO  Generated 1240 options
    // INFO  Solver status: OPTIMAL
    // Which run? Which user? Which fleet? Unknown.
}

// ✅ CORRECT — MDC set at the start of the run
MDC.put("snapshotId", runContext.getSnapshotId());
MDC.put("fleet", runContext.getFleet());
MDC.put("contractMonth", runContext.getContractMonth());
// Now every downstream log line automatically includes these fields
```

**Why violates ENG-6.7:** Without MDC context, log lines from concurrent runs are interleaved with no way to correlate them to a specific trigger, user, fleet, or contract month. Post-run analysis and incident investigation become impossible.


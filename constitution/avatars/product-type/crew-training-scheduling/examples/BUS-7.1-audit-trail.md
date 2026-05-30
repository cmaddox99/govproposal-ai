---
law_id: BUS-7.1
avatar: crew-training-scheduling
---

# BUS-7.1: Audit Trail Law Examples for Crew Training Scheduling

> **Law:** All significant actions MUST be logged with immutable, tamper-evident records.
> For crew training scheduling, "significant actions" includes every optimizer run,
> every scheduling recommendation, and every configuration value used to produce it —
> because these outputs directly influence FAA-adjacent pilot training decisions.

---

## COMPLIANT: Complete Run Audit Record

```
# What a complete JOSE run audit trail looks like in the log stream:

[INFO] [RunStatusService]  snapshotId=00241984_320_APR2025_20250415102030_PROD status=RUNNING timestamp=2025-04-15T10:20:30Z

[INFO] [DtoProcessor]      snapshotId=00241984_320_APR2025_20250415102030_PROD config={runTwoMonths=false, restrictMoves=false, freezeDays=6, allowBackToBackSeq=true, ...}

[INFO] [DtoProcessor]      snapshotId=00241984_320_APR2025_20250415102030_PROD Fetched 87 student schedules for APR2025
[INFO] [DtoProcessor]      snapshotId=00241984_320_APR2025_20250415102030_PROD Fetched 42 CKP schedules for APR2025
[INFO] [DtoProcessor]      snapshotId=00241984_320_APR2025_20250415102030_PROD Fetched 18 OE blocked sequences for APR2025

[INFO] [NetworkGenerator]  snapshotId=00241984_320_APR2025_20250415102030_PROD Eligible students: 34 | Excluded: 53
[INFO] [NetworkGenerator]  snapshotId=00241984_320_APR2025_20250415102030_PROD Generated 1,248 options across 34 students

[INFO] [MathModel]         snapshotId=00241984_320_APR2025_20250415102030_PROD status=OPTIMAL objective=4821.5 solveTimeMs=3240 variables=1248 constraints=892

[INFO] [OutputService]     snapshotId=00241984_320_APR2025_20250415102030_PROD openBlkdSeqSaved=12 blkdSeqDropped=2 buySeqDropped=5 studentsCompleted=8 studentsInvolved=34

[INFO] [RunStatusService]  snapshotId=00241984_320_APR2025_20250415102030_PROD status=COMPLETED timestamp=2025-04-15T10:24:15Z
```

**Why compliant:** Every significant event carries the snapshot ID. Any scheduler who questions "why did my pilot get moved on April 15?" can pull all log lines for that snapshot ID and reconstruct the complete decision chain: who triggered it, what config was used, how many options were evaluated, what the solver chose, and what the output contained.

---

## COMPLIANT: Scheduler-Facing Audit in Output Files

```java
// ✅ SolutionRecommendation.xlsx Metrics sheet captures the run's audit summary
// for scheduler review — not just internal logs

public void writeMetricsSheet(Sheet sheet, SolutionMetrics metrics, RunContext runContext) {
    // Who / When / What — the five W's of BUS-7.1
    writeRow(sheet, "Snapshot ID",         runContext.getSnapshotId());
    writeRow(sheet, "Fleet",               runContext.getFleet());
    writeRow(sheet, "Contract Month",      runContext.getContractMonth());
    writeRow(sheet, "Run Date",            runContext.now().toString());
    writeRow(sheet, "Triggered By",        runContext.getConfig().getUserId());
    writeRow(sheet, "Environment",         runContext.getEnvironment());
    // Outcome
    writeRow(sheet, "Solver Status",       metrics.getSolverStatus());
    writeRow(sheet, "Objective Value",     metrics.getObjectiveValue());
    writeRow(sheet, "Open Blkd Seq Saved", metrics.getOpenBlkdSeqSaved());
    writeRow(sheet, "Blkd Seq Dropped",    metrics.getBlkdSeqDropped());
    writeRow(sheet, "Buy Seq Dropped",     metrics.getBuySeqDropped());
    writeRow(sheet, "Students Completed",  metrics.getStudentsCompleted());
    writeRow(sheet, "Students Involved",   metrics.getStudentsInvolved());
    writeRow(sheet, "Freeze Days",         runContext.getConfig().getFreezeDays());
}
```

**Why compliant:** The Metrics sheet is the scheduler-facing audit record. It answers "what did this run do and why?" independently of the internal log system. If a scheduling error is discovered weeks later, the Excel file already on the scheduler's desktop contains the complete run context.

---

## COMPLIANT: Config Snapshot Enables Run Reproducibility

```markdown
## Audit Requirement: Any past run must be reproducible

Because JOSE recommendations influence pilot training assignments, Flight
Standards may need to reconstruct a past run's decision logic. This requires:

1. **Config at run time** — logged via `log.info(config.toString())` in DtoProcessor
2. **Input data snapshot** — FSA/CCS data uploaded to Azure Blob Storage per run
3. **Snapshot ID** — ties the config log, input blobs, and output files together

### Retention Policy (Per BUS-7.1)
- Log retention: 1 year online (Azure Monitor), 7 years archived
- Output files in Azure Blob Storage: minimum 1 year
- Snapshot ID is the durable correlation key across all artifacts
```

---

## VIOLATION: Significant Action With No Audit Record

```java
// ❌ VIOLATES BUS-7.1 — scheduling recommendation written to disk with no log
public void writeToFile(OptimizationDataBundle bundle) {
    ExcelWriter.write(bundle, outputPath);
    // No log of what was written, to where, for which snapshot, with what outcome
    // If a pilot's assignment is questioned later, there is no record of this write
}
```

**Why violates BUS-7.1:** The write to output file IS the scheduling recommendation delivery. It must be logged. The log entry should include snapshot ID, output file paths, and key metrics so there is an immutable record that the file was produced for a specific run with specific results.

---

## VIOLATION: Run Status Updated in DB Only — Not in Logs

```java
// ❌ VIOLATES BUS-7.1 — status transition is persisted but not auditable via logs
public void updateStatus(String snapshotId, RunStatus status) {
    statusRepository.upsert(snapshotId, status);
    // No log — a FAILED run at 3 AM is invisible to on-call unless they query the DB
    // Log aggregation tools (Splunk, Azure Monitor) have no record of this event
}
```

**Why violates BUS-7.1:** An audit trail must be observable through standard log tooling, not just database queries. Incident investigations happen in Splunk or Azure Monitor — if the status transition isn't there, the run is not auditable.


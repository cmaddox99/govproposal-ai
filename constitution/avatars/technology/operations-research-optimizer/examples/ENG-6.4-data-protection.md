---
law_id: ENG-6.4
avatar: operations-research-optimizer
---

# ENG-6.4: Data Protection Examples for Operations Research / MIP Optimizer

---

## COMPLIANT: PII Excluded from Logs

```java
// ✅ Employee IDs and names never appear in log messages
@Slf4j
@Component
public class DtoProcessor {

    private static final String CLASS_NAME = DtoProcessor.class.getSimpleName();

    public RawDataCollection getDtos() {
        List<StudentScheduleDto> schedules = fsaClient.getStudentScheduleDtos(contractMonth);

        // ✅ Log counts and contract month — not employee IDs or names
        log.info("[{}] Fetched {} student schedules for {}",
                CLASS_NAME, schedules.size(), contractMonth);

        return rawDataCollection;
    }
}
```

**Why compliant:** The log records operational metrics (count, contract month) that are needed for audit and debugging without exposing pilot PII. Employee IDs and names stay inside the data objects, never entering the log stream.

---

## COMPLIANT: PII Not Persisted Beyond the Run Lifecycle

```java
// ✅ OptimizationDataBundle is a request-scoped in-memory object
// It is never written to a database or durable store
@Component
public class JoseOptimizerController implements CommandLineRunner {

    @Override
    public void run(String... args) {
        // Bundle lives only in heap memory for the duration of this run
        OptimizationDataBundle bundle = inputDataService.prepareInputData();
        optionGenerationService.generateFeasibleOptions(bundle);
        optimizationService.findOptimalSolution(bundle, ...);

        // Output files contain only schedule metadata (sequence keys, dates)
        // — not raw PII fields from the FSA API response
        outputDataService.writeToFile(bundle);

        // bundle goes out of scope here — GC eligible
        // No employee PII is written to Azure Blob Storage
    }
}
```

**Why compliant:** Pilot PII (employee IDs, names, contact info) fetched from FSA/CCS is used only in-memory during the run. The output Excel files contain scheduling actions referencing sequence keys and base codes — not raw PII fields.

---

## COMPLIANT: Output Files Contain Minimum Necessary PII

```java
// ✅ Student actions sheet uses employee ID only (required for scheduler to act)
// — not full name, address, or other PII
public void writeStudentActionsSheet(Sheet sheet, List<StudentActionDto> actions) {
    for (StudentActionDto action : actions) {
        Row row = sheet.createRow(rowNum++);
        row.createCell(0).setCellValue(action.getEmployeeId());    // needed to identify pilot
        row.createCell(1).setCellValue(action.getActionType());    // ASSIGN / REMOVE / UNCHANGED
        row.createCell(2).setCellValue(action.getSequenceKey());   // which sequence
        row.createCell(3).setCellValue(action.getBaseCode());      // domicile
        // ✅ No phone number, address, SSN, or medical information included
    }
}
```

**Why compliant:** Only the minimum PII fields needed for the scheduler to take action are included. Per ENG-6.4, data minimisation is mandatory — collect and use only what is required for the stated purpose.

---

## VIOLATION: Employee PII Written to Logs

```java
// ❌ VIOLATES ENG-6.4 — employee names and IDs appear in log output
public void processStudentSchedules(List<StudentScheduleDto> schedules) {
    for (StudentScheduleDto schedule : schedules) {
        log.debug("Processing student: {} {} (ID: {})",
                schedule.getFirstName(),    // ← PII in log
                schedule.getLastName(),     // ← PII in log
                schedule.getEmployeeId()); // ← PII in log
    }
}
```

**Why violates ENG-6.4:** Log files are shipped to centralised systems (Splunk, Azure Monitor) accessible to operations staff who have no need for individual pilot names. This violates data minimisation and purpose limitation principles.

---

## VIOLATION: PII Included in Snapshot ID

```java
// ❌ VIOLATES ENG-6.4 — snapshot ID embeds employee name, making it
// visible in file names, blob paths, and all log lines
public String buildSnapshotId(String userId, String fleet, String contractMonth) {
    String pilotName = fsaClient.getPilotName(userId); // ← fetching name to embed in ID
    return pilotName + "_" + fleet + "_" + contractMonth + "_" + timestamp;
    // Produces: "JOHN_DOE_320_APR2025_20250415102030"
    // This name now appears in every log line, every blob path, every email subject
}
```

**Why violates ENG-6.4:** The snapshot ID format `{UserID}_{Fleet}_{ContractMonth}_{Timestamp}_{Env}` uses an employee number (not a name) by design. Embedding a pilot's name propagates PII into every artifact of the run — logs, file names, email subjects, Blob Storage paths.


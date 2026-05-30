# Java/Spring Boot — Legacy Rescue Guide

> **Purpose:** Java/Spring Boot–specific enrichment of `workflows/legacy-rescue-refactor.md`.
> Contains stack tool commands, AA BFF fleet patterns, and learnings from live rescue runs.
> For the full phase-by-phase workflow see `workflows/legacy-rescue-refactor.md`.
> **Laws:** ENG-4.1, ENG-4.10, ENG-4.11, ENG-4.12, ENG-6.1, ENG-6.7, ENG-11.1

---

## Tech Stack Translation

The `legacy-rescue-refactor` workflow is stack-agnostic. This file provides the Java/Spring Boot
command substitutions for each phase.

### Build & Test

| Action | Command |
|--------|---------|
| Run all tests | `./mvnw test` |
| Run with coverage | `./mvnw test jacoco:report` |
| View coverage report | `open target/site/jacoco/index.html` |
| Single test class | `./mvnw test -Dtest=MileageServiceTest` |
| Skip tests (build only) | `./mvnw package -DskipTests` |

> **sonar.java.binaries gotcha:** If SonarQube reports "No binaries directory", the project
> has not been compiled before the scan. Always run `./mvnw compile` before `sonar:sonar`,
> or use `./mvnw verify sonar:sonar` which compiles, tests, and scans in one pass.

### SonarQube — Phase-Gated Commands

```bash
# Phase 1 — Baseline snapshot (run AFTER compile)
./mvnw verify sonar:sonar \
  -Dsonar.projectKey=<your-project-key> \
  -Dsonar.host.url=$SONAR_URL \
  -Dsonar.token=$SONAR_TOKEN

# Phase 3 — Characterization coverage gate (≥95% on IN_SCOPE classes)
./mvnw test jacoco:report sonar:sonar \
  -Dsonar.projectKey=<your-project-key> \
  -Dsonar.host.url=$SONAR_URL \
  -Dsonar.token=$SONAR_TOKEN

# Phase 5/6 — Refactor / Certify (same command; gate enforces new_coverage ≥ 95%)
./mvnw verify sonar:sonar \
  -Dsonar.projectKey=<your-project-key> \
  -Dsonar.host.url=$SONAR_URL \
  -Dsonar.token=$SONAR_TOKEN
```

> **Auth:** Use `SONAR_TOKEN` env var. Never pass `-Dsonar.token=` on the command line —
> it appears in shell history and process lists. Per ENG-6.7.

### JaCoCo Setup (`pom.xml`)

```xml
<plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <version>0.8.11</version>
    <executions>
        <execution>
            <goals><goal>prepare-agent</goal></goals>
        </execution>
        <execution>
            <id>report</id>
            <phase>test</phase>
            <goals><goal>report</goal></goals>
        </execution>
    </executions>
</plugin>
```

### Mutation Testing — PIT (`pitest-maven`)

Phase 7 requires mutation score ≥ 90% on rescued classes (ENG-4.12).

```xml
<!-- pom.xml — add to build/plugins -->
<plugin>
    <groupId>org.pitest</groupId>
    <artifactId>pitest-maven</artifactId>
    <version>1.15.3</version>
    <dependencies>
        <dependency>
            <groupId>org.pitest</groupId>
            <artifactId>pitest-junit5-plugin</artifactId>
            <version>1.2.1</version>
        </dependency>
    </dependencies>
    <configuration>
        <targetClasses>
            <param>com.example.domain.*</param>  <!-- scope to rescued classes -->
        </targetClasses>
        <targetTests>
            <param>com.example.*Test</param>
        </targetTests>
        <mutationThreshold>90</mutationThreshold>
        <outputFormats>
            <outputFormat>HTML</outputFormat>
            <outputFormat>XML</outputFormat>
        </outputFormats>
    </configuration>
</plugin>
```

```bash
# Run mutation testing
./mvnw org.pitest:pitest-maven:mutationCoverage

# View report
open target/pit-reports/index.html
```

Commit the HTML report to `hangar-ai-specs/evidence/mutation-report/` per ENG-4.12.

---

## AA BFF Fleet Patterns

### Phase 1 — God Class Assessment

The AA BFF fleet's most common Phase 1 finding: builder classes exceeding 300 LOC (ENG-3.1).

```bash
# Find god classes — classes over 300 lines
find src/main -name "*.java" | xargs wc -l | sort -rn | head -20

# Find god methods — methods over 30 lines (requires PMD or manual review)
./mvnw pmd:check  # if PMD is configured
```

**Known BFF god classes (evidence from live runs):**

| Class | Repo | LOC | Primary violation |
|-------|------|-----|-------------------|
| `ReservationResponseBuilder` | mobile-manage-minilith | 1,654 | ServiceLocator + god method |
| `TravelHubResponseBuilderV2/V3/V4` | mobile-travelhub-bff | 1,763 combined | Copy-paste versioning + mutable singleton |
| `ReshopResponseBuilder` | mobile-booking-bff | ~800 | `BigDecimal(double)` precision, god method |

### Phase 3 — Characterization Scope Declaration

**Learning from live run (2026-004):** 25 tests were written for 4 of 29 classes. Coverage
landed at 21.7% — far below the ≥95% gate. Scope was never declared.

**Before writing a single test:**

```bash
# 1. Produce class inventory
find src/main/java -name "*.java" | grep -v "Application.java" | sort

# 2. Classify each class in PROPOSAL.md
```

```markdown
## Characterization Scope (Phase 3)

| Class | Category | Reason if EXCLUDED/DEFERRED |
|-------|----------|-----------------------------|
| MileageService | IN_SCOPE | |
| AccrualService | IN_SCOPE | |
| EnrollmentRequest | EXCLUDED | DTO — getters/setters only, no business logic |
| Application | EXCLUDED | Spring Boot entry point |
```

```bash
# 3. Verify JaCoCo counts only IN_SCOPE classes
#    Add exclusions to pom.xml for EXCLUDED classes:
```

```xml
<plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <configuration>
        <excludes>
            <exclude>**/dto/**</exclude>
            <exclude>**/config/**</exclude>
            <exclude>**/*Application.class</exclude>
        </excludes>
    </configuration>
</plugin>
```

### Phase 3 — JUnit 5 + Mockito Characterization Test Template

```java
/**
 * Characterization test — captures CURRENT behavior of MileageService before refactoring.
 * If this test breaks during Phase 4/5, behavior has changed. Do not delete.
 * Per ENG-4.10: characterization tests protect the refactor, not describe the ideal.
 */
@ExtendWith(MockitoExtension.class)
class MileageServiceCharacterizationTest {

    @Mock
    private MileageRepository mileageRepository;

    @InjectMocks
    private MileageService mileageService;

    @BeforeEach
    void setUp() {
        given(mileageRepository.findByMemberId(any()))
            .willReturn(Optional.of(new MileageAccount("AA123", 5000)));
    }

    @Test
    void calculateAccrual_returnsCurrentBehavior_forBaseFlightMiles() {
        // Characterization: pin the current output. This is NOT necessarily correct
        // behavior — it is EXISTING behavior. Fix bugs in Phase 4, not here.
        int result = mileageService.calculateAccrual("AA123", 1500, "Y");
        assertThat(result).isEqualTo(1500); // pin current output
    }
}
```

### Phase 3 — Spring Boot Integration Characterization (`@SpringBootTest`)

For classes too tightly coupled to mock (pre-ServiceLocator removal):

```java
@SpringBootTest
@Transactional
class ReservationResponseBuilderCharacterizationTest {

    @Autowired
    private ReservationResponseBuilder builder;

    @Test
    void build_returnsExpectedStructure_forKnownReservation() {
        ReservationResponse response = builder.build(knownTestRequest());
        // Pin current structure — do not assert correctness of values
        assertThat(response).isNotNull();
        assertThat(response.getSegments()).hasSize(2);  // pin current count
    }
}
```

> Use `@SpringBootTest` characterization tests sparingly — they are slow and couple to
> the full context. Once ServiceLocator is removed (Phase 4), migrate to `@ExtendWith(MockitoExtension.class)`.

### Phase 3 — Spring Boot Characterization Scope Registration

After running Phase 3 tests, register scope in `PROPOSAL.md`:

```bash
# Verify coverage threshold in SonarQube
./mvnw verify sonar:sonar -Dsonar.projectKey=<key> ...
# Check dashboard: coverage metric must show ≥95% before Phase 4 begins
```

---

## Security Remediation — Phase 4 (ENG-6.1, ENG-6.7)

### Hardcoded Credentials

```java
// ❌ Phase 1 finding — hardcoded credential (ENG-6.7 HARD_BLOCK)
private static final String API_KEY = "sk-prod-abc123";

// ✅ Phase 4 fix — externalized via Spring @Value
@Value("${external.api.key}")
private String apiKey;
```

```yaml
# application.properties / application.yml — value from environment
external.api.key=${EXTERNAL_API_KEY}
```

```bash
# SonarQube detects this as S6697 (hardcoded secret) — blocker severity
# Phase 4 gate: critical_violations=0 and vulnerabilities=0 must be satisfied
```

### CORS Wildcard Fix (ENG-6.1)

```java
// ❌ Phase 1 finding — wildcard CORS
@Bean
public CorsConfigurationSource corsConfigurationSource() {
    CorsConfiguration config = new CorsConfiguration();
    config.addAllowedOrigin("*");  // HARD_BLOCK in any auth-protected API
    ...
}

// ✅ Phase 4 fix — explicit origin allowlist
@Bean
public CorsConfigurationSource corsConfigurationSource() {
    CorsConfiguration config = new CorsConfiguration();
    config.setAllowedOrigins(List.of(
        "https://www.aa.com",
        "https://mobile.aa.com"
    ));
    config.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE"));
    config.setAllowCredentials(true);
    ...
}
```

### `@PreAuthorize` on All Endpoints (ENG-6.1)

```java
// ❌ No authorization on sensitive endpoint
@GetMapping("/api/v1/reservations/{pnr}")
public ReservationResponse getReservation(@PathVariable String pnr) { ... }

// ✅ Explicit authorization — every endpoint must declare its requirement
@PreAuthorize("hasRole('AUTHENTICATED_USER') and #principal.memberId == #memberId")
@GetMapping("/api/v1/reservations/{pnr}")
public ReservationResponse getReservation(@PathVariable String pnr,
                                           @AuthenticationPrincipal AAPrincipal principal) { ... }
```

---

## Refactoring — Phase 5

### ServiceLocator → Constructor Injection

See `use-cases/service-locator-to-di/README.md` for the full Minilith migration pattern.

Key sequence (per ENG-4.1 — one test at a time):
1. Add constructor with injected dependencies (keep ServiceLocator call for now)
2. Write the test that was impossible before (GREEN)
3. Delete the ServiceLocator call
4. Verify all tests pass
5. Commit

### Mutable `@Service` Singleton Fix

```java
// ❌ Thread-safety critical defect — mutable instance field in @Service singleton
@Service
public class TravelHubResponseBuilderV2 {
    private List<TravelSegment> segments = new ArrayList<>(); // SHARED across all requests!

    public TravelHubResponse build(TravelData data) {
        segments.clear();  // race condition — another thread may be reading
        ...
    }
}

// ✅ Fix — all state is method-scoped
@Service
public class TravelHubResponseBuilderV2 {
    public TravelHubResponse build(TravelData data) {
        List<TravelSegment> segments = new ArrayList<>(); // local to this invocation
        ...
    }
}
```

### Test Level Migration After Extraction (ENG-4.10)

**Learning from live run (2026-004):** When `AccrualService` was extracted from `MileageService`,
the existing characterization test changed level — from unit test to integration test. Two new
unit tests were needed for the extracted class.

| Before extraction | After extraction |
|------------------|-----------------|
| `MileageServiceCharacterizationTest` — unit | `MileageServiceCharacterizationTest` — integration (tests wiring) |
| (no test) | `AccrualServiceTest` — unit (tests extracted behavior) |

**Rule:** Any class extracted during Phase 5 is automatically IN_SCOPE. Write its unit tests
before closing the Phase 5 gate. `new_coverage ≥ 95%` is a Phase 5 HARD_BLOCK (ENG-4.11).

### Copy-Paste Versioning

See `use-cases/copy-paste-versioning/README.md` for the TravelHub V2/V3/V4 migration.

---

## Phase 7 — Mutation Hardening

Run PIT after Phase 6 certifies GREEN:

```bash
./mvnw org.pitest:pitest-maven:mutationCoverage
open target/pit-reports/index.html
```

Each surviving mutant must be:
- **Killed** by adding or strengthening an assertion, or
- **Accepted** with a law citation in the surviving-mutant register

Commit the register to `hangar-ai-specs/evidence/mutation-report/surviving-mutants.md`.

**Common surviving mutant patterns in BFF code:**

| Mutant type | Typical cause | Fix |
|-------------|--------------|-----|
| Boundary (i+1 vs i) | Loop termination not tested | Add edge-case test at `size - 1` |
| Null return | Null path not exercised | Add test for empty/null input |
| Negated conditional | Missing sad-path test | Add test for the false branch |

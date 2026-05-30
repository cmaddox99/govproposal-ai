# Greenfield MVP Guide

**Purpose:** Learn how to start a new project from scratch using the Hangar AI Constitution for rapid, high-quality MVP development.

**Time to Read:** 35 minutes

---

## Constitutional Authority

This guide implements requirements from the **hangar-ai-constitution**:

### Laws Implemented

| Law ID | Title | How This Guide Implements It |
|--------|-------|------------------------------|
| **ENG-1.2** | AI-Engineer Pairing Law | AI assistants follow Constitution, explain WHY |
| **ENG-4.1** | Atomic TDD Law (NON-NEGOTIABLE) | RED → GREEN → REFACTOR → VERIFY → COMMIT → REPEAT |
| **ENG-4.2** | Test Pyramid Law | Unit 70-80%, Integration 15-25%, E2E 5-10% |
| **ENG-4.6** | Coverage Requirements Law | 90%+ coverage enforced from day one |
| **ENG-3.1** | Cyclomatic Complexity Law | ≤10 per method via quality gates |
| **ENG-3.2** | Cognitive Complexity Law | ≤7 per method |
| **ENG-2.1** | DDD Strategic Design Law | Domain-driven package structure |
| **ENG-2.5** | Vertical Slice Law | Features built in thin vertical slices |
| **ENG-11.1** | Hangar SDD Law (NON-NEGOTIABLE) | All changes governed via Hangar SDD (hangar-ai-specs/) |
| **ENG-6.1** | Security by Design Law | Security built in from start |
| **ENG-6.7** | Audit Trail Law | Task completion tracked with commit hashes |
| **ENG-1.1** | Priority Hierarchy Law | Security > Correctness > Reliability > Maintainability |

### Skills Invoked

| Skill | Purpose | Primary Laws |
|-------|---------|-------------|
| **skill-06-atomic-tdd** | Execute 8-step TDD cycle for all code | ENG-4.1, ENG-4.2, ENG-4.3 |
| **skill-07-vertical-slice-dev** | Break features into thin, deployable slices | ENG-2.5, ENG-1.4 |
| **skill-03-executable-spec** | Create BDD scenarios for acceptance criteria | PRD-5.1 |

> **Per ENG-1.2**: Every decision in this guide references the constitutional law that mandates it.
> **RAG Note**: When AI agents process this guide, they should also load the referenced skills for detailed procedures.

---

## What is Greenfield MVP?

**Greenfield** = brand new codebase with:
- No legacy constraints
- Freedom to set patterns from day one
- Opportunity to build in quality from start
- Clean slate for team practices

**MVP** = Minimum Viable Product:
- Core features only
- Fast time to market
- Validated by real users
- Foundation for growth

**Goal:** Build fast WITHOUT sacrificing quality. The Constitution enables this.

---

## ⚠️ NON-NEGOTIABLE: Atomic TDD from Day One

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   ENG-4.1 ATOMIC TDD LAW — NON-NEGOTIABLE                      │
│                                                                 │
│   Even in greenfield, there are NO EXCEPTIONS to Atomic TDD.   │
│                                                                 │
│   Every feature follows:                                        │
│   RED → GREEN → REFACTOR → VERIFY → UPDATE → COMMIT → REPEAT   │
│                                                                 │
│   VERIFY = 3 Gates (ALL must pass):                            │
│   ├── GATE 1: Tests — ALL tests pass                           │
│   ├── GATE 2: Lint — constitution-lint passes                  │
│   └── GATE 3: Static — PMD/SonarQube (no blockers)             │
│                                                                 │
│   "But it's greenfield, we can add tests later" — NO.          │
│   Tests first. Always. From the very first line of code.       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Why Constitution for MVPs?

```
┌─────────────────────────────────────────────────────────────┐
│              TRADITIONAL MVP vs CONSTITUTIONAL MVP          │
│                                                             │
│   Traditional:                 Constitutional:              │
│   ┌──────────────────┐        ┌──────────────────┐         │
│   │ Fast + Dirty     │        │ Fast + Clean     │         │
│   │ Ship now, fix    │        │ Ship fast with   │         │
│   │ later (never)    │        │ built-in quality │         │
│   └──────────────────┘        └──────────────────┘         │
│                                                             │
│   Result:                      Result:                      │
│   - Technical debt            - Maintainable code          │
│   - Hard to extend            - Easy to extend             │
│   - Bugs in production        - Bugs caught early          │
│   - Rewrite needed            - Grows with product         │
│                                                             │
│   AI teaches quality AS you build, not slowing you down    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Project Bootstrap (Day 1)

> **Per ENG-1.2 (AI-Engineer Pairing Law)**: AI assistants guide setup following Constitutional patterns.
> **Per ENG-11.1 (Hangar SDD Law, NON-NEGOTIABLE)**: All projects MUST use Hangar SDD for change management.

### Step 1.1: Create Project Structure

```bash
# Generate Spring Boot project (or your framework)
# Include: Web, JPA, PostgreSQL, Actuator, Lombok

# Initialize Hangar SDD in your project
mkdir -p hangar-ai-specs/{changes,archive,specs}
```

### Step 1.2: Add Core Governance Files

> **Per ENG-1.2 (AI-Engineer Pairing Law)**: AGENTS.md is REQUIRED for all projects.

Create root AGENTS.md with hangar-ai-constitution authority (see [How to Adopt Constitution](./how-to-adopt-constitution.md) for full template):

```bash
# Create root AGENTS.md with precedence rules
touch AGENTS.md
```

**Important:** The root AGENTS.md must reference hangar-ai-constitution and establish that central constitution laws ALWAYS take precedence over local instructions.

### Step 1.3: Reference hangar-ai-constitution

In your root AGENTS.md, reference the central constitution (don't copy files - reference them):

```markdown
## Adopted Constitutions (from hangar-ai-constitution)

**Repository:** https://github.com/AAInternal/hangar-ai-constitution

- Engineering Constitution: `laws/engineering/` — ENG-* laws
- Product Constitution: `laws/product/` — PRD-* laws
- Business Constitution: `laws/business/` — BUS-* laws
- Aviation/FAA Adoption: `avatars/industry/aviation-faa/`
- Technology Adoption: `avatars/technology/{your-stack}/`
- Product-Type Adoption: `avatars/product-type/{your-domain}/`
```

### Step 1.5: Set Up Quality Gates

> **Per ENG-4.6 (Coverage Requirements Law)**: 90%+ line coverage on new code.
> **Per ENG-3.1 (Cyclomatic Complexity Law)**: ≤10 per method.

```xml
<!-- pom.xml quality configuration -->
<plugins>
    <!-- Test coverage -->
    <plugin>
        <groupId>org.jacoco</groupId>
        <artifactId>jacoco-maven-plugin</artifactId>
        <configuration>
            <rules>
                <rule>
                    <limits>
                        <limit>
                            <counter>LINE</counter>
                            <minimum>0.90</minimum>
                        </limit>
                    </limits>
                </rule>
            </rules>
        </configuration>
    </plugin>
    
    <!-- Complexity checks -->
    <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-pmd-plugin</artifactId>
        <configuration>
            <rulesets>
                <ruleset>code-quality/java.xml</ruleset>
            </rulesets>
        </configuration>
    </plugin>
</plugins>
```

### Step 1.6: Install Constitution Linter

> **Per VERIFY = 3 Gates**: The constitution linter is GATE 2 of every verification.

```bash
# Install from Constitution repo
pip install -e ../hangar-ai-constitution/tools/constitution-lint/

# Verify installation
aa-constitution-lint --version

# Run initial check (expect some warnings - test pyramid not yet established)
aa-constitution-lint .
```

---

## Phase 2: Define MVP Scope (Day 1-2)

> **Per ENG-2.5 (Vertical Slice Law)**: Features SHALL be developed as thin vertical slices.
> **Per ENG-11.1 (Hangar SDD Law)**: All features MUST go through the Hangar SDD change workflow.

### Step 2.1: Create Product Vision Document

```markdown
# Product Vision (add this section to root AGENTS.md)

## Product Vision
[One paragraph describing what the product does and why]

## Target Users
- Primary: [User type 1]
- Secondary: [User type 2]

## MVP Features (Must Have)
1. [Feature 1] - [Why critical for launch]
2. [Feature 2] - [Why critical for launch]
3. [Feature 3] - [Why critical for launch]

## Post-MVP (Nice to Have)
- [Feature A]
- [Feature B]

## Success Metrics
- [Metric 1]: [Target]
- [Metric 2]: [Target]

## Technical Constraints
- [Constraint 1]
- [Constraint 2]
```

### Step 2.2: Slice MVP into Vertical Slices

> **Per ENG-2.5 (Vertical Slice Law)**: Each slice delivers working end-to-end functionality.
> **⚠️ CRITICAL**: Never build horizontal layers. Always deliver working verticals.

```
MVP Feature: User Registration

Traditional Horizontal Slicing (AVOID):
- Sprint 1: Database tables
- Sprint 2: Backend services
- Sprint 3: API endpoints
- Sprint 4: Frontend
- Sprint 5: Integration and bugs
→ Nothing works until Sprint 5!

Constitutional Vertical Slicing (USE):
- Slice 1: Register user with email (full stack) → DEPLOYABLE
- Slice 2: Email verification → DEPLOYABLE
- Slice 3: Password requirements → DEPLOYABLE
- Slice 4: Duplicate email handling → DEPLOYABLE
→ Working registration after Slice 1!
```

### Step 2.3: Create First Change with Hangar SDD

> **Per ENG-11.1 (Hangar SDD Law)**: Use Hangar SDD to manage the change.

```bash
# Create your first change directory
mkdir -p hangar-ai-specs/changes/user-registration

# Scaffold the proposal files
touch hangar-ai-specs/changes/user-registration/PROPOSAL.md
touch hangar-ai-specs/changes/user-registration/tasks.md
```

This creates `hangar-ai-specs/changes/user-registration/` with structured documents:

```
hangar-ai-specs/changes/user-registration/
├── PROPOSAL.md       # Intent, scope, approach (with Constitutional Authority)
└── tasks.md          # Implementation checklist with TDD cycles
```

### Step 2.4: Populate Proposal with Constitutional Authority

> **Per ENG-1.2**: Every proposal MUST cite the Constitutional laws that govern it.

**Update `PROPOSAL.md`:**

```markdown
# Change: User Registration

## Constitutional Authority

| Law | How Applied |
|-----|-------------|
| **ENG-4.1** | Atomic TDD for all implementation (NON-NEGOTIABLE) |
| **ENG-2.5** | Feature split into vertical slices |
| **ENG-4.2** | Test pyramid: Unit 70-80%, Integration 15-25%, E2E 5-10% |
| **ENG-6.5** | Input validation on all user inputs |
| **ENG-6.1** | Password security per OWASP guidelines |

## Intent
Enable users to register accounts with secure email verification.

## Scope
**In scope:** Registration, validation, email verification
**Out of scope:** Social login, profile management

## Vertical Slices

### Slice 1: Basic Registration (Walking Skeleton)
- POST /api/users creates user with email/password
- Returns 201 with user ID
- 400 for invalid input

### Slice 2: Email Verification
- Registration sends verification email
- GET /api/users/verify/{token} activates account
- Unverified users cannot log in

### Slice 3: Password Requirements (per ENG-6.1)
- Minimum 12 characters
- Complexity validation
- bcrypt hashing
```

### Step 2.5: Create BDD Specifications

> **Per PRD-5.1**: Specifications define acceptance criteria as executable scenarios.

**Create `hangar-ai-specs/specs/user-registration.md`:**

```markdown
# User Registration — Specification

## ADDED Requirements

### Requirement: Users can register with email and password

#### Scenario: REG-001 — Successful registration
- **GIVEN** a new user with valid email and password
- **WHEN** POST /api/users is called
- **THEN** response status is 201 Created
- **AND** response body contains userId

#### Scenario: REG-002 — Email already exists
- **GIVEN** a user already exists with email "john@example.com"
- **WHEN** POST /api/users is called with the same email
- **THEN** response status is 409 Conflict
- **AND** error message indicates "Email already registered"

#### Scenario: REG-003 — Invalid email format
- **GIVEN** a registration request with email "not-an-email"
- **WHEN** POST /api/users is called
- **THEN** response status is 400 Bad Request
- **AND** error message indicates "Invalid email format"

#### Scenario: REG-004 — Password too short (per ENG-6.1)
- **GIVEN** a registration request with password "short"
- **WHEN** POST /api/users is called
- **THEN** response status is 400 Bad Request
- **AND** error message indicates "Password must be at least 12 characters"
```

---

## Phase 3: Build with Atomic TDD (Sprints)

> **Per ENG-4.1 (Atomic TDD Law — NON-NEGOTIABLE)**: TDD SHALL be practiced in atomic cycles — ONE test at a time.
> **Invoke:** `skill-06-atomic-tdd` → 8-Step Atomic TDD Cycle

### The Full Atomic TDD Cycle (Per ENG-4.1 — MANDATORY)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│             ATOMIC TDD CYCLE FOR GREENFIELD (Per ENG-4.1)                   │
│                                                                             │
│  For each scenario (e.g., REG-001):                                         │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 1. RED — Write ONE failing test                                     │   │
│  │    • Create test method referencing scenario ID                     │   │
│  │    • Write assertions for expected behavior                         │   │
│  │    • Run test — it FAILS (compilation or assertion)                 │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                              ↓                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 2. GREEN — Write MINIMUM code to pass                               │   │
│  │    • Implement the simplest code that makes the test pass           │   │
│  │    • No extra features, no "future-proofing"                        │   │
│  │    • Run test — it PASSES                                           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                              ↓                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 3. REFACTOR — Improve code quality (tests stay green)               │   │
│  │    • Apply DDD patterns (ENG-2.1)                                   │   │
│  │    • Reduce complexity (ENG-3.1: ≤10)                               │   │
│  │    • Extract value objects (ENG-3.2: immutability)                  │   │
│  │    • Run test — still PASSES                                        │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                              ↓                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 4. VERIFY — Triple-gate validation (ALL must pass)                  │   │
│  │    • GATE 1: ./mvnw test — ALL tests pass                           │   │
│  │    • GATE 2: aa-constitution-lint . — Constitutional compliance     │   │
│  │    • GATE 3: ./mvnw pmd:check — Static analysis (no blockers)       │   │
│  │    • Check coverage increased                                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                              ↓                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 5. UPDATE — Mark task complete in tasks.md (MANDATORY)              │   │
│  │    • Open tasks.md immediately                                      │   │
│  │    • Mark task [x] with ✓ and commit hash                           │   │
│  │    • Update progress summary counts                                 │   │
│  │    • This provides audit trail (ENG-6.7)                            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                              ↓                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 6. COMMIT — Atomic commit with scenario reference                   │   │
│  │    • git add -A                                                     │   │
│  │    • git commit -m "feat(user): REG-001 successful registration     │   │
│  │                                                                     │   │
│  │                     Constitutional: ENG-4.1 Atomic TDD"             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                              ↓                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 7. REPEAT — Next scenario (REG-002)                                 │   │
│  │    • Pick next unchecked task from tasks.md                         │   │
│  │    • Start new cycle at step 1                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ⚠️  NEVER batch multiple scenarios into one commit                        │
│  ⚠️  NEVER skip the REFACTOR step                                          │
│  ⚠️  NEVER skip any VERIFY gate                                            │
│  ⚠️  NEVER skip updating tasks.md after each cycle                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### VERIFY = 3 Gates (ALL Must Pass)

> **Per ENG-4.1, ENG-4.6, ENG-3.1**: All three gates are mandatory at each cycle.

| Gate | Command | Must Pass | Law |
|------|---------|-----------|-----|
| **Tests** | `./mvnw test` (or `pytest`, `npm test`) | All green | ENG-4.1 |
| **Constitution Lint** | `aa-constitution-lint .` | No violations | ENG-1.2 |
| **Static Analysis** | `./mvnw pmd:check` (or equivalent) | No blockers | ENG-3.1 |

```bash
# Example VERIFY for Java/Maven
./mvnw test && aa-constitution-lint . && ./mvnw pmd:check

# Example VERIFY for Python/pytest
pytest --cov=app && aa-constitution-lint . && ruff check .

# Example VERIFY for Node/TypeScript
npm test && aa-constitution-lint . && npm run lint
```

### Task Tracking Protocol (MANDATORY)

> **Per ENG-6.7 (Audit Trail Law)**: All task completions MUST be tracked with commit hashes.
> This is NOT optional — it creates traceability from spec → task → commit.

**Create `tasks.md` with scenario-linked tasks:**

```markdown
# Tasks: User Registration

**Constitutional Authority:** ENG-4.1 Atomic TDD (NON-NEGOTIABLE)
**Source of Truth:** specs/user-registration.md

---

## Progress Summary

| Layer | Total | Done | Remaining |
|-------|-------|------|-----------|
| Unit | 6 | 0 | 6 |
| Integration | 4 | 0 | 4 |
| E2E | 1 | 0 | 1 |

---

## Slice 1: Basic Registration (Walking Skeleton)

### Unit Tests (70-80%)
> Reference: Spec → User Registration

| Status | Task | Scenario | Test Method | Commit |
|--------|------|----------|-------------|--------|
| | 1.1 | REG-001 | `registerUser_validInput_createsUser` | — |
| | 1.2 | REG-003 | `registerUser_invalidEmail_returnsBadRequest` | — |
| | 1.3 | REG-004 | `registerUser_shortPassword_returnsBadRequest` | — |

### Integration Tests (15-25%)
> Reference: Spec → API Contracts

| Status | Task | Scenario | Test Method | Commit |
|--------|------|----------|-------------|--------|
| | 1.4 | REG-001 | `POST /api/users → 201 with userId` | — |
| | 1.5 | REG-002 | `POST /api/users duplicate → 409` | — |

> **Task Completion Protocol (Per ENG-4.1, ENG-6.7):**
> After EACH TDD cycle completes, mark the task:
> ```
> | ✓ | 1.1 | REG-001 | `registerUser_validInput_createsUser` | abc123 |
> ```
> Update Progress Summary counts immediately.

---

## Slice 2: Email Verification
...
```

### Daily Workflow

> **Per ENG-4.1**: RED → GREEN → REFACTOR → VERIFY → UPDATE → COMMIT → REPEAT

```
Morning:
1. Review hangar-ai-specs/changes/[active]/tasks.md for the day
2. Identify current vertical slice
3. Start Atomic TDD cycle on next unchecked task

Each Feature (MANDATORY cycle):
1. RED    — Write ONE failing test
2. GREEN  — Minimum code to pass
3. REFACTOR — Clean up (AI teaches patterns)
4. VERIFY — 3 gates: tests + lint + static
5. UPDATE — Mark task [x] in tasks.md with commit hash
6. COMMIT — Atomic commit with scenario reference
7. REPEAT — Next test

End of Day:
1. All tests passing (GATE 1 ✓)
2. Constitution lint passing (GATE 2 ✓)
3. Static analysis passing (GATE 3 ✓)
4. Coverage maintained (90%+)
5. tasks.md updated with all commits
```

### Example: Building User Entity with Atomic TDD

> **Per ENG-4.1 (Atomic TDD Law)**: One test at a time, minimum code to pass, then refactor.

```
Step 1: RED — Write failing test for REG-001
─────────────────────────────────────────────────
/**
 * Scenario: REG-001 — Successful registration
 * Source: hangar-ai-specs/specs/user-registration.md
 * Constitutional: ENG-4.1 Atomic TDD
 */
@Test
@DisplayName("REG-001: registerUser with valid input creates user")
void registerUser_validInput_createsUser() {
    // Given — valid registration request
    var request = new RegistrationRequest("john@example.com", "securePass123!");
    
    // When — register user
    var result = userService.register(request);
    
    // Then — user created with ID
    assertThat(result.userId()).isNotNull();
    assertThat(result.email()).isEqualTo("john@example.com");
}
→ Compile fails: UserService doesn't exist

Step 2: GREEN — Minimum code to pass
─────────────────────────────────────────────────
public record RegistrationRequest(String email, String password) {}
public record RegistrationResult(UUID userId, String email) {}

@Service
public class UserService {
    public RegistrationResult register(RegistrationRequest request) {
        return new RegistrationResult(UUID.randomUUID(), request.email());
    }
}
→ Test passes

Step 3: REFACTOR — Apply Constitutional patterns
─────────────────────────────────────────────────
// Per ENG-2.1 (DDD): Add proper domain model
// Per ENG-3.2 (Immutability): Value objects are immutable
// Per ENG-6.1 (Security): Hash password

public record Email(String value) {
    public Email {
        if (!value.matches("^[A-Za-z0-9+_.-]+@(.+)$")) {
            throw new IllegalArgumentException("Invalid email format");
        }
    }
}

@Entity
public class User {
    @Id
    private UUID id;
    private Email email;
    private String passwordHash;
    // ...
}
→ Refactored with validation and DDD patterns

Step 4: VERIFY — 3 Gates
─────────────────────────────────────────────────
./mvnw test                  # GATE 1: ✓ All tests pass
aa-constitution-lint .       # GATE 2: ✓ No violations
./mvnw pmd:check            # GATE 3: ✓ No blockers
→ All gates pass

Step 5: UPDATE — Mark task complete
─────────────────────────────────────────────────
# In tasks.md:
| ✓ | 1.1 | REG-001 | `registerUser_validInput_createsUser` | abc123 |

# Update Progress Summary:
| Unit | 6 | 1 | 5 |    ← Updated from 0 to 1

Step 6: COMMIT — Atomic commit
─────────────────────────────────────────────────
git add -A
git commit -m "feat(user): REG-001 successful registration

- Add User entity with Email value object
- Add UserService with registration
- Test: registerUser_validInput_createsUser

Constitutional: ENG-4.1 Atomic TDD, ENG-2.1 DDD"

Step 7: REPEAT — Next scenario (REG-002)
─────────────────────────────────────────────────
→ Start new cycle for duplicate email handling
```

---

## Phase 4: MVP Iterations

> **Per ENG-4.6 (Coverage Requirements Law)**: Maintain 90%+ coverage throughout iterations.
> **Per ENG-2.5 (Vertical Slice Law)**: Each iteration delivers working end-to-end slices.

### Sprint Structure

```
Week 1: Foundation
- Project setup with quality gates (Day 1)
- MVP scope defined with Hangar SDD proposal (Day 1-2)
- First proposal complete (Slice 1-2 done)
- All VERIFY gates passing from day 1

Week 2: Core Features
- Continue vertical slices using Atomic TDD
- First working E2E flow
- Internal demo
- tasks.md shows 50%+ completion

Week 3: Feature Complete
- All MVP slices done
- Integration testing complete
- Bug fixes (each fix follows TDD cycle)
- Coverage verified at 90%+

Week 4: Polish & Launch
- Performance testing
- Security review (per ENG-6.1)
- Documentation complete
- MVP Launch
```

### Tracking Progress in tasks.md

> **Per ENG-4.6, ENG-3.1, ENG-6.7**: Track all metrics continuously with audit trail.

```markdown
# Sprint Dashboard

## Progress Summary

| Layer | Total | Done | Remaining |
|-------|-------|------|-----------|
| Unit | 24 | 18 | 6 |
| Integration | 8 | 6 | 2 |
| E2E | 2 | 1 | 1 |

## Quality Metrics (Per VERIFY = 3 Gates)

| Gate | Target | Current | Status |
|------|--------|---------|--------|
| Test Coverage | ≥90% | 94% | ✓ |
| Complexity | ≤10 | 7 max | ✓ |
| Lint Violations | 0 | 0 | ✓ |

## Proposals Status

| Proposal | Slices | Done | Status |
|----------|--------|------|--------|
| user-registration | 3 | 3 | ✅ Complete |
| user-authentication | 4 | 2 | 🔄 In Progress |
| user-profile | 2 | 0 | ⏳ Not Started |

## Recent Commits (Audit Trail per ENG-6.7)

| Commit | Scenario | Task |
|--------|----------|------|
| abc123 | REG-001 | 1.1 registerUser_validInput_createsUser |
| def456 | REG-002 | 1.2 registerUser_duplicateEmail_returns409 |
| ghi789 | REG-003 | 1.3 registerUser_invalidEmail_returns400 |
```

---

## AI-Assisted MVP Development

> **Per ENG-1.2 (AI-Engineer Pairing Law)**: AI assistants SHALL follow the Constitution strictly and explain the WHY behind every decision.
> **Per ENG-4.1 (Atomic TDD Law — NON-NEGOTIABLE)**: AI MUST enforce the TDD cycle on every task.

### AI Teaching Persona

When working with AI on greenfield projects, the AI should:

1. **Cite Constitutional laws** for every decision
2. **Enforce Atomic TDD** — refuse to skip steps
3. **Guide VERIFY = 3 Gates** — ensure all gates pass before commit
4. **Track tasks** — remind to update tasks.md after each cycle

### Example: Cargo Domain — New PAL Application Service

```
Prompt: "Help me set up a new Spring Boot service for PAL (Partner Airline)
         application processing following Constitutional practices."

AI Response: "I'll help you set up a Constitutional project for cargo/freight domain.
             Applying all three constitutions plus aviation-faa and cargo-freight adoptions:

             **1. Project Structure (Per ENG-2.1 DDD Strategic Design):**
             ```
             src/main/java/com/aa/cargo/pal/
             ├── domain/                    # DDD Aggregates
             │   ├── PalApplication.java    # Aggregate Root
             │   ├── Applicant.java         # Entity
             │   ├── VettingAnswer.java     # Value Object (immutable per ENG-3.2)
             │   └── ApplicationStatus.java # Value Object
             ├── service/
             │   ├── PalApplicationService.java
             │   └── VettingService.java    # TSA integration
             ├── controller/
             │   └── PalApplicationController.java
             ├── repository/
             │   └── PalApplicationRepository.java
             └── integration/
                 └── TsaVettingClient.java  # External API
             ```

             **2. First Atomic TDD Cycle (Per ENG-4.1 — NON-NEGOTIABLE):**
             
             Let's start with scenario PAL-001: Submit new application
             
             RED — Write failing test:
             ```java
             @Test
             @DisplayName("PAL-001: submitApplication with valid data creates application")
             void submitApplication_validData_createsApplication() {
                 var request = new PalApplicationRequest(
                     "ACME Airlines", "contact@acme.com", ApplicantType.CARRIER
                 );
                 
                 var result = palService.submitApplication(request);
                 
                 assertThat(result.applicationId()).isNotNull();
                 assertThat(result.status()).isEqualTo(ApplicationStatus.PENDING_VETTING);
             }
             ```
             
             **3. VERIFY = 3 Gates (Per ENG-4.1):**
             After GREEN and REFACTOR, we'll run:
             - GATE 1: `./mvnw test` — all tests pass
             - GATE 2: `aa-constitution-lint .` — constitutional compliance
             - GATE 3: `./mvnw pmd:check` — static analysis
             
             **4. Task Tracking (Per ENG-6.7):**
             After commit, update tasks.md:
             ```
             | ✓ | 1.1 | PAL-001 | submitApplication_validData_createsApplication | abc123 |
             ```
             
             Ready to start the RED step?"
```

### Example: Booking Domain — Flight Search MVP

```
Prompt: "I need to implement flight search for our new booking platform.
         Help me create a Hangar SDD proposal (PROPOSAL.md) with vertical slices."

AI Response: "Following ENG-2.5 (Vertical Slices) and passenger-booking adoption:

             **Constitutional Authority for This Proposal:**
             | Law | Application |
             |-----|-------------|
             | ENG-4.1 | Atomic TDD for all implementation |
             | ENG-2.5 | Vertical slice decomposition |
             | ENG-6.5 | Input validation on search parameters |
             | BUS-2.3 | DOT fare transparency compliance |

             **Proposed Vertical Slices:**

             **Slice 1: Basic One-Way Search (Walking Skeleton)**
             - Endpoint: GET /api/flights/search
             - Returns: List<FlightOption> with total price
             - TDD cycles: 4 (happy path, validation, empty results, error handling)

             **Slice 2: DOT Fare Transparency (Per BUS-2.3)**
             - Display breakdown: base fare + taxes + carrier fees
             - Total must include all mandatory charges
             - TDD cycles: 3 (breakdown calculation, display format, compliance check)

             **Slice 3: Round-Trip Search**
             - Combine outbound + return searches
             - Show combined pricing
             - TDD cycles: 3

             **tasks.md Structure:**
             ```markdown
             ## Slice 1: Basic One-Way Search

             | Status | Task | Scenario | Test Method | Commit |
             |--------|------|----------|-------------|--------|
             | | 1.1 | SEARCH-001 | searchFlights_validRoute_returnsOptions | — |
             | | 1.2 | SEARCH-002 | searchFlights_invalidRoute_returnsEmpty | — |
             | | 1.3 | SEARCH-003 | searchFlights_missingOrigin_returns400 | — |
             | | 1.4 | SEARCH-004 | searchFlights_apiError_returns503 | — |
             ```

             **First Test (Atomic TDD — Per ENG-4.1):**
             ```java
             @Test
             @DisplayName("SEARCH-001: searchFlights valid route returns options with price")
             void searchFlights_validRoute_returnsOptionsWithTotalPrice() {
                 // Given — valid search request
                 var request = SearchRequest.oneWay("DFW", "LHR", LocalDate.now().plusDays(7));

                 // When — search flights
                 var options = searchService.search(request);

                 // Then — options with compliant pricing (per BUS-2.3)
                 assertThat(options).isNotEmpty();
                 assertThat(options.get(0).getTotalPrice())
                     .isEqualTo(options.get(0).getBaseFare()
                         .add(options.get(0).getTaxes())
                         .add(options.get(0).getCarrierFees()));  // DOT compliance
             }
             ```

             After this test passes (GREEN + REFACTOR + VERIFY), I'll update tasks.md
             and we move to SEARCH-002. Ready to start?"
```

### Loyalty Domain: AAdvantage MVP

```
Prompt: "Help me implement the miles earning feature for our AAdvantage integration."

AI Response: "Following loyalty-aadvantage adoption and all three constitutions:

             **Domain Model (Engineering Section 2.1):**
             - AAdvantageAccount: Aggregate Root (has ID, lifecycle)
             - MilesTransaction: Entity (immutable once created)
             - MilesEarning: Value Object (calculation result)
             - StatusTier: Value Object (Gold, Platinum, Executive Platinum)

             **Business Rules (Business Constitution Article VII):**
             1. Miles are a financial liability - MUST have audit trail
             2. All credits create MilesTransaction records
             3. Reversals create offsetting transactions, never delete
             4. Status multipliers: Gold 25%, Platinum 50%, Exec Plat 100%

             **Atomic TDD Implementation:**

             **Step 1: RED - First Failing Test**
             ```java
             @Test
             void earnMiles_goldMemberFlies1000Miles_earns1250() {
                 // GIVEN - Per loyalty adoption, status affects earning
                 AAdvantageAccount account = AAdvantageAccount.create("ABC123", StatusTier.GOLD);
                 FlightActivity flight = FlightActivity.builder()
                     .withDistance(1000)
                     .withFareClass("Y")  // Full fare economy
                     .build();

                 // WHEN
                 MilesEarning earning = milesService.calculateEarning(account, flight);

                 // THEN - 1000 base + 25% Gold bonus = 1250
                 assertThat(earning.getBaseMiles()).isEqualTo(1000);
                 assertThat(earning.getBonusMiles()).isEqualTo(250);
                 assertThat(earning.getTotalMiles()).isEqualTo(1250);
             }
             ```

             Run this - it should fail because MilesService doesn't exist.

             **Step 2: GREEN - Minimum Implementation**
             [Will provide after you confirm RED]

             **Compliance Note (Business Constitution):**
             After GREEN, we must add audit trail test:
             ```java
             @Test
             void earnMiles_createsAuditableTransaction() {
                 // Per Business Section 7.1 - all miles movements audited
             }
             ```

             Ready to start?"
```

### Operations Domain: IROP MVP

```
Prompt: "We're building an IROP (Irregular Operations) recovery tool.
         Help me plan the MVP with Constitutional compliance."

AI Response: "IROP is operationally critical. Applying airport-operations adoption
             with extra attention to Aviation/FAA compliance:

             **Compliance Requirements (Business Constitution Article XII):**
             - Real-time accuracy (delays affect crew legality)
             - DOT delay reporting requirements
             - Customer notification timelines

             **MVP Vertical Slices:**

             **Slice 1: Flight Delay Detection (2 pts)**
             - Listen for OpsDB delay events
             - Calculate impact on connections
             - Engineering: Event-driven per Section 2.4
             ```java
             @Test
             void onFlightDelayed_withConnections_identifiesAffectedPassengers() {
                 // GIVEN
                 Flight delayed = flight("AA100").delayedBy(Minutes.of(90));
                 List<Passenger> connecting = passengersConnectingFrom(delayed);

                 // WHEN
                 IropEvent event = iropService.assess(delayed);

                 // THEN
                 assertThat(event.getAffectedPassengers()).containsAll(connecting);
                 assertThat(event.getMissedConnections()).isNotEmpty();
             }
             ```

             **Slice 2: Alternative Flight Suggestions (3 pts)**
             - Find next available flights for missed connections
             - Consider elite status for priority
             - Product Constitution: Minimize customer effort

             **Slice 3: Automated Rebooking (3 pts)**
             - Auto-rebook when clear alternative exists
             - Notify customer proactively
             - Per customer-service adoption: empathetic messaging

             **Slice 4: Crew Impact Assessment (2 pts)**
             - Check if delay affects crew legality
             - Per aviation-faa adoption: FAR Part 117 compliance
             - Alert crew scheduling if legality at risk

             **Safety Note:**
             Slice 4 touches FAR Part 117. Per Aviation/FAA adoption Section A.1,
             this may require DO-178C Level C treatment if it affects dispatch decisions.

             Start with Slice 1? It's self-contained and enables the rest."
```

### Cross-Domain: Customer Compensation MVP

```
Prompt: "Build a customer compensation calculator that considers flight delays,
         elite status, and DOT regulations."

AI Response: "This crosses multiple domains. Applying all three constitutions:

             **Domain Mapping:**
             - Customer Service: Compensation rules and policies
             - Loyalty: Elite status lookup and miles awards
             - Operations: Delay duration and cause codes
             - Business: DOT compliance for qualifying delays

             **Compliance (Business Constitution Article XII):**
             - DOT requires compensation for certain controllable delays
             - EU261 for European routes (different rules)
             - Must track for regulatory reporting

             **MVP Slices:**

             **Slice 1: Delay-Based Compensation Calculation (3 pts)**
             ```java
             @Test
             void calculateCompensation_3HourDelay_offersVoucher() {
                 // GIVEN - Per customer-service adoption
                 ServiceCase complaint = ServiceCase.forDelay(Hours.of(3));
                 Customer customer = regularMember();

                 // WHEN
                 CompensationOffer offer = compensationService.calculate(complaint, customer);

                 // THEN - Standard 3hr delay = $100 voucher
                 assertThat(offer.getType()).isEqualTo(CompensationType.VOUCHER);
                 assertThat(offer.getValue()).isEqualTo(Money.of(100, "USD"));
             }
             ```

             **Slice 2: Elite Status Enhancement (2 pts)**
             ```java
             @Test
             void calculateCompensation_eliteMember_offersEnhancedGoodwill() {
                 // GIVEN - Per loyalty adoption, status matters
                 ServiceCase complaint = ServiceCase.forDelay(Hours.of(3));
                 Customer customer = executivePlatinumMember();

                 // WHEN
                 CompensationOffer offer = compensationService.calculate(complaint, customer);

                 // THEN - Elite gets miles + lounge pass
                 assertThat(offer.getMiles()).isGreaterThanOrEqualTo(10_000);
                 assertThat(offer.includesLoungePass()).isTrue();
             }
             ```

             **Slice 3: DOT Compliance Check (2 pts)**
             - Automatically flag delays requiring DOT compensation
             - Track for regulatory reporting
             - Per Business Article XII

             **Slice 4: Compensation Fulfillment (3 pts)**
             - Issue voucher codes
             - Credit miles to AAdvantage (integration with loyalty)
             - Audit trail per Business Section 7.1

             Start with Slice 1 - it establishes the core pattern."
```

---

## Quality from Day One

> **Per ENG-4.1 (NON-NEGOTIABLE)**: These practices are mandatory, not optional.

### Non-Negotiables for MVP

| Practice | Why It's Worth It | Constitutional Law |
|----------|-------------------|-------------------|
| 90% test coverage | Catches bugs before users do | **ENG-4.6** |
| Complexity ≤10 | Code stays maintainable | **ENG-3.1** |
| TDD from start | Faster debugging, better design | **ENG-4.1** (NON-NEGOTIABLE) |
| Hangar SDD proposals | Clear scope, no feature creep | **ENG-11.1** |
| Small commits | Easy to review and revert | **ENG-4.1** |
| VERIFY = 3 Gates | Consistent quality every cycle | **ENG-4.1** |
| Task tracking | Audit trail, resume capability | **ENG-6.7** |

### "But MVPs Should Be Fast!"

Constitutional MVPs ARE fast:
- AI generates code quickly
- Tests prevent debugging time
- Clear scope prevents waste
- No rewrite needed later
- VERIFY gates catch issues immediately

```
Traditional MVP:
  Build (2 weeks) + Debug (2 weeks) + Fix (1 week) = 5 weeks
  + Rewrite later (8 weeks) = 13 weeks total

Constitutional MVP:
  Build with TDD (3 weeks) + Polish (1 week) = 4 weeks
  + Extend (not rewrite) = grows sustainably
```

---

## Common Pitfalls

### ❌ "We'll add tests later"

Later = never. Debt compounds. Test as you go.
**Constitutional violation:** ENG-4.1 (NON-NEGOTIABLE)

### ❌ "Just this once, skip TDD"

One shortcut becomes habit. Stay disciplined.
**Constitutional violation:** ENG-4.1 (NON-NEGOTIABLE)

### ❌ "MVP means quick and dirty"

MVP means "minimum VIABLE" - it must work well.
**Constitutional clarification:** Viable requires quality.

### ❌ "We don't have time for documentation"

AGENTS.md takes 10 minutes. Saves hours of confusion.
**Constitutional requirement:** ENG-1.2

### ❌ "We'll refactor after launch"

You won't. Build it right the first time.
**Constitutional guidance:** ENG-1.3 (Continuous Refactoring)

### ❌ "Skip the lint gate, tests pass"

VERIFY = 3 gates. ALL must pass. No exceptions.
**Constitutional requirement:** ENG-4.1

### ❌ "I'll update tasks.md at the end"

Update immediately after each cycle. Provides audit trail.
**Constitutional requirement:** ENG-6.7

---

## Hangar SDD Quick Reference

| Operation | Command / Action | Purpose |
|-----------|-----------------|---------|
| Create new proposal | `mkdir -p hangar-ai-specs/changes/<name>` | Create new change directory |
| Scaffold proposal | Create `PROPOSAL.md` + `tasks.md` | Document intent, scope, and tasks |
| Track progress | Check `tasks.md` checkboxes with commit hashes | Audit trail per ENG-6.7 |
| Archive on completion | `mv hangar-ai-specs/changes/<id> hangar-ai-specs/archive/$(date +%Y-%m-%d)-<id>` | Archive completed change |
| Full lifecycle | See `skill-spec-governance` | Complete Hangar SDD lifecycle |

---

## Skills Quick Reference (For AI RAG)

When processing this guide, AI agents should load these skills for detailed procedures:

| Skill ID | Name | When to Invoke | Primary Laws |
|----------|------|----------------|--------------|
| **skill-06-atomic-tdd** | Atomic TDD | **ALWAYS** — writing any code (NON-NEGOTIABLE) | **ENG-4.1**, ENG-4.2, ENG-4.3 |
| **skill-07-vertical-slice-dev** | Vertical Slice Development | Breaking features into slices | ENG-2.5, ENG-1.4 |
| **skill-03-executable-spec** | Executable Specification | Creating BDD scenarios | PRD-5.1 |
| **skill-08-code-review** | Code Review | Reviewing Constitutional compliance | ENG-1.2 |

### Skill → Law → Artifact Chain

```
skill-07-vertical-slice-dev (ENG-2.5)
    └── Produces: Hangar SDD PROPOSAL.md with slices
        └── Each slice invokes:
            skill-06-atomic-tdd (ENG-4.1 — NON-NEGOTIABLE)
                └── Produces: Test pyramid tasks in tasks.md
                    └── Each task follows:
                        7-Step Atomic TDD Cycle (MANDATORY)
                        └── Produces: Tested, compliant code
                        
CRITICAL: skill-06-atomic-tdd must be invoked for EVERY coding task.
          No code change is exempt from the Atomic TDD cycle.
```

---

## Success Checklist

### Day 1
- [ ] Project created with quality gates (pom.xml/package.json configured)
- [ ] hangar-ai-specs/ structure in place
- [ ] AGENTS.md added with Constitution references
- [ ] constitution-lint installed and passing
- [ ] First PROPOSAL.md created in hangar-ai-specs/changes/

### Week 1
- [ ] First vertical slice complete with tests
- [ ] VERIFY = 3 gates passing on every commit
- [ ] tasks.md updated with commit hashes for all completed tasks
- [ ] All team members understand Atomic TDD workflow
- [ ] Daily commits with passing tests

### MVP Launch
- [ ] All MVP proposals complete and archived
- [ ] 90%+ test coverage (GATE 1 ✓)
- [ ] Zero constitution-lint violations (GATE 2 ✓)
- [ ] Zero complexity violations (GATE 3 ✓)
- [ ] tasks.md shows complete audit trail
- [ ] Ready to extend, not rewrite

---

## Related Guides

- [Brownfield Adoption](./brownfield-adoption.md) - Adopting Constitution in existing projects
- [How to Adopt Constitution](./how-to-adopt-constitution.md) - AGENTS.md setup
- [Organizational Transformation](./organizational-transformation.md) - Scaling practices

## Related Skills

- [skill-06-atomic-tdd](../../../agent-skills/skills-by-domain/development-practices/06-atomic-tdd.md) - 8-Step TDD Cycle
- [skill-07-vertical-slice-dev](../../../agent-skills/skills-by-domain/development-practices/07-vertical-slice-dev.md) - Feature slicing
- [skill-03-executable-spec](../../../agent-skills/skills-by-domain/product-planning/03-executable-spec.md) - BDD specifications

## The Three Constitutions

Every greenfield project should adopt all three constitutions:

| Constitution | Focus | Key Laws |
|--------------|-------|----------|
| [Engineering](../../../laws/engineering/) | **HOW** to build | ENG-4.1 Atomic TDD, ENG-3.1 Complexity, ENG-2.5 Vertical Slices |
| [Product](../../../laws/product/) | **WHAT** to build | PRD-2.1 User Journeys, ENG-11.1 Hangar SDD |
| [Business](../../../laws/business/) | **WHY** and constraints | BUS-2.3 Compliance, BUS-7.1 Audit Trail |

## AA Product Domain Adoptions

Select the adoption that matches your product domain:

| Domain | When to Use |
|--------|-------------|
| [Passenger Booking](../../../avatars/product-type/passenger-booking/) | Flight search, reservations, pricing, ancillaries |
| [Check-In & Travel](../../../avatars/product-type/check-in-travel/) | Check-in, boarding, flight status, notifications |
| [Cargo & Freight](../../../avatars/product-type/cargo-freight/) | PAL applications, AWB, iCargo, dangerous goods |
| [Loyalty (AAdvantage)](../../../avatars/product-type/loyalty-aadvantage/) | Miles earning/redemption, status, awards |
| [Airport Operations](../../../avatars/product-type/airport-operations/) | Gate management, crew scheduling, IROP recovery |
| [Customer Service](../../../avatars/product-type/customer-service/) | Rebooking, refunds, complaints, compensation |

---

**Last Updated:** February 9, 2026

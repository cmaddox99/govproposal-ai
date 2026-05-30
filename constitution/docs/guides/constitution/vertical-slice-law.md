# Vertical Slice Development Law

**Purpose:** Learn how to slice work vertically for Hangar SDD proposals, enabling incremental delivery and AI-assisted development.

**Constitutional Reference:** Article IV, Section 4.1; Hangar SDD Workflow  
**Time to Read:** 25 minutes

---

## The Law

> **Features SHALL be developed in vertical slices - thin, end-to-end increments that deliver user value and can be independently tested and deployed.**

---

## What Is Vertical Slice Development?

A **vertical slice** cuts through all layers of the application to deliver a complete, thin piece of functionality:

```
┌─────────────────────────────────────────────────────────────────────┐
│                        HORIZONTAL LAYERS                             │
├─────────────────────────────────────────────────────────────────────┤
│  UI/API Layer         [░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]  │
│  Service Layer        [░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]  │
│  Domain Layer         [░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]  │
│  Repository Layer     [░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]  │
│  Database             [░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]  │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                        VERTICAL SLICES                               │
├─────────────────────────────────────────────────────────────────────┤
│  UI/API Layer         [██]    [██]    [██]    [██]    [██]          │
│  Service Layer        [██]    [██]    [██]    [██]    [██]          │
│  Domain Layer         [██]    [██]    [██]    [██]    [██]          │
│  Repository Layer     [██]    [██]    [██]    [██]    [██]          │
│  Database             [██]    [██]    [██]    [██]    [██]          │
│                      Slice1  Slice2  Slice3  Slice4  Slice5         │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Horizontal vs. Vertical Development

### ❌ Horizontal Development (Anti-Pattern)

Build complete layers before moving to the next:

```
Week 1: Build all database tables
Week 2: Build all repository classes
Week 3: Build all service classes
Week 4: Build all controllers
Week 5: Integration testing
Week 6: Bug fixes

Problems:
- No working feature until Week 5
- Integration issues discovered late
- Difficult to course-correct
- AI can't verify compliance until integration
```

### ✅ Vertical Development (Constitutional Pattern)

Build thin slices through all layers:

```
Day 1: Slice 1 - Submit draft application (API to DB)
Day 2: Slice 2 - Send confirmation email (complete flow)
Day 3: Slice 3 - Retrieve application status (complete flow)
Day 4: Slice 4 - Reject application (complete flow)
Day 5: Slice 5 - Approve application (complete flow)

Benefits:
- Working feature from Day 1
- Integration verified continuously
- Easy to course-correct
- AI verifies compliance each slice
```

---

## Slicing for Hangar SDD Proposals

### Step 1: Identify the Feature

Start with the user story or feature request:

```
Feature: PAL Application Submission

As a freight forwarder
I want to submit an order
So that I can apply for PAL certification
```

### Step 2: Break Down into Slices

Identify the smallest end-to-end increments:

```markdown
## Slices for PAL Application Submission

### Slice 1: Create Draft PAL Application
- API: POST /orders (basic fields)
- Service: Create and persist draft
- Database: Insert record
- Response: Return created ID
- **Deliverable:** Can create a draft PAL application

### Slice 2: Add Vetting Answers
- API: PUT /orders/{id}/items
- Service: Update vetting answers
- Validation: Required fields
- **Deliverable:** Can add items to draft PAL application

### Slice 3: Submit Application
- API: POST /orders/{id}/submit
- Service: Change status, validate completeness
- Domain: PalApplication.submit() method
- **Deliverable:** Can submit a complete order

### Slice 4: Send Confirmation Email
- Service: Generate email from template
- Integration: Send via email service
- **Deliverable:** Applicant receives confirmation

### Slice 5: Retrieve Application Status
- API: GET /orders/{id}
- Service: Fetch and return
- **Deliverable:** Can check order status
```

### Step 3: Create Hangar SDD Proposal

Each slice becomes a task in `tasks.md`:

```markdown
# Tasks: PAL Application Submission

## 1. Slice 1: Create Draft PAL Application
- [ ] 1.1 Write test for POST /orders endpoint
- [ ] 1.2 Implement controller endpoint
- [ ] 1.3 Write test for service createDraft()
- [ ] 1.4 Implement service method
- [ ] 1.5 Write integration test for complete flow
- [ ] 1.6 Verify Constitutional compliance

## 2. Slice 2: Add Vetting Answers
- [ ] 2.1 Write test for PUT /orders/{id}/items
- [ ] 2.2 Implement controller and service
- [ ] 2.3 Add validation for required fields
- [ ] 2.4 Verify Constitutional compliance

## 3. Slice 3: Submit Application
- [ ] 3.1 Write test for status change
- [ ] 3.2 Write test for validation
- [ ] 3.3 Implement domain method PalApplication.submit()
- [ ] 3.4 Implement service orchestration
- [ ] 3.5 Verify Constitutional compliance

## 4. Slice 4: Send Confirmation Email
- [ ] 4.1 Write contract test for email service
- [ ] 4.2 Implement email template
- [ ] 4.3 Implement email sending
- [ ] 4.4 Verify Constitutional compliance

## 5. Slice 5: Retrieve Application Status
- [ ] 5.1 Write test for GET /orders/{id}
- [ ] 5.2 Implement endpoint
- [ ] 5.3 Verify Constitutional compliance
```

### Step 4: Write Spec Deltas Per Slice

Create spec deltas that can be merged incrementally:

```markdown
# specs/order/spec.md

## ADDED Requirements

### Requirement: Create Draft PAL Application
The system SHALL allow customers to create draft PAL applications.

#### Scenario: Successful draft creation
- **GIVEN** a valid authenticated user
- **WHEN** they POST to /orders with basic info
- **THEN** the system creates a draft PAL application
- **AND** returns the order ID

### Requirement: Submit Application
The system SHALL allow submission of complete draft PAL applications.

#### Scenario: Successful submission
- **GIVEN** a draft PAL application with all required fields
- **WHEN** the user submits the order
- **THEN** the status changes to SUBMITTED
- **AND** a confirmation email is sent

#### Scenario: Incomplete submission rejected
- **GIVEN** a draft PAL application missing required fields
- **WHEN** the user attempts to submit
- **THEN** the system returns validation errors
- **AND** the status remains DRAFT
```

---

## Slicing Strategies

### Strategy 1: CRUD Operations

Start with Create, then Read, Update, Delete:

```
Slice 1: Create (POST)
Slice 2: Read (GET)
Slice 3: Update (PUT/PATCH)
Slice 4: Delete (DELETE)
```

### Strategy 2: Happy Path First

Start with the success case, then add error handling:

```
Slice 1: Happy path (everything works)
Slice 2: Validation errors
Slice 3: Not found errors
Slice 4: Integration failures
Slice 5: Edge cases
```

### Strategy 3: User Journey

Follow the user's journey through the feature:

```
Slice 1: Start application
Slice 2: Fill out form
Slice 3: Submit for review
Slice 4: Receive confirmation
Slice 5: Check status
```

### Strategy 4: Risk-First

Start with the riskiest or most uncertain parts:

```
Slice 1: Payment gateway integration (highest risk)
Slice 2: Email service (external dependency)
Slice 3: Database operations (well understood)
Slice 4: UI updates (low risk)
```

---

## Vertical Slicing and Atomic TDD

Vertical slices integrate naturally with Atomic TDD:

```
SLICE 1: Create Draft PAL Application
├── TDD Cycle 1: Test POST endpoint returns 201
├── TDD Cycle 2: Test service creates draft
├── TDD Cycle 3: Test repository saves entity
├── TDD Cycle 4: Test validation of required fields
└── TDD Cycle 5: Integration test for complete flow

SLICE 2: Add Vetting Answers
├── TDD Cycle 1: Test PUT endpoint
├── TDD Cycle 2: Test service updates items
├── TDD Cycle 3: Test validation rules
└── TDD Cycle 4: Integration test

... and so on
```

Each TDD cycle follows the 8-step process within each slice.

---

## Prompt Examples for AI-Assisted Slicing

### Creating a Proposal with Slices

```
Prompt: "I need to implement PAL application submission. Help me create an
         Hangar SDD proposal with vertical slices."

AI Response: "Following the Vertical Slice Development Law, I'll help you
             break this feature into end-to-end increments.

             First, let me understand the scope:
             1. What are the main user actions?
             2. What external integrations are needed?
             3. What are the validation rules?

             Based on typical PAL application workflows, I suggest these slices:

             **Slice 1: Create Draft** (Day 1)
             - POST /orders endpoint
             - Service and repository layer
             - Basic validation

             **Slice 2: Add Vetting Answers** (Day 2)
             - PUT endpoint for vetting answers
             - Field validation

             ...

             Shall I create the proposal.md and tasks.md with this structure?"
```

### Working Through a Slice

```
Prompt: "Let's start implementing Slice 1: Create Draft PAL Application"

AI Response: "Following Article IV, Section 4.1 (Atomic TDD Law), let's
             implement Slice 1 through the test-first cycle.

             **Task 1.1: Write test for POST /orders endpoint**

             Starting with RED - here's a failing integration test:

             ```java
             @Test
             public void createApplication_validRequest_returns201() {
                 // GIVEN
                 var request = new CreateApplicationRequest("Freight Forward Inc");

                 // WHEN
                 var response = restTemplate.postForEntity(
                     "/api/orders", request, ApplicationResponse.class);

                 // THEN
                 assertThat(response.getStatusCode()).isEqualTo(CREATED);
                 assertThat(response.getBody().getId()).isNotNull();
             }
             ```

             Please run this test to confirm it fails."
```

### Reviewing Slice Completion

```
Prompt: "Slice 1 is complete. What's the status?"

AI Response: "Let me verify Slice 1 completion against Constitutional requirements:
             
             **Atomic TDD Compliance (Article IV, Section 4.1):**
             ✅ All tasks marked [x] in tasks.md
             ✅ Each TDD cycle followed 8-step process
             
             **Coverage Requirements (Article IV, Section 4.3):**
             ✅ Line coverage: 94% (above 90% threshold)
             ✅ Branch coverage: 88% (above 85% threshold)
             
             **Code Quality (Article III):**
             ✅ Complexity: Max 6 (below 10 threshold)
             ✅ No Law of Demeter violations
             ✅ Methods under 50 lines
             
             **Documentation (Hangar SDD):**
             ✅ tasks.md updated
             ✅ proposal.md documents findings
             ✅ spec.md delta ready for merge
             
             **Slice 1 is COMPLETE and ready for review.**
             
             Shall we proceed to Slice 2: Add Applicant Information?"
```

---

## Slice Size Guidelines

### Too Big (Anti-Pattern)

```
Slice: Implement complete PAL application management workflow

Problems:
- Takes weeks to complete
- Can't verify until done
- Too many moving parts
- Integration issues hidden
```

### Too Small (Anti-Pattern)

```
Slice 1: Add field to entity
Slice 2: Add field to DTO
Slice 3: Add mapping
Slice 4: Add validation

Problems:
- No user value per slice
- Can't demo progress
- Overhead of slice management
```

### Just Right

```
Slice: Submit application and send confirmation email

Characteristics:
- Completes in 1-2 days
- Delivers user value
- Can be demonstrated
- Can be independently tested
- Can be independently deployed
```

---

## Vertical Slicing in Brownfield Projects

When adopting vertical slicing in existing projects:

### Step 1: Identify Characterization Tests Needed

Before slicing, ensure existing behavior is tested:

```
Existing feature: Customer lookup

Before slicing changes:
1. Write characterization tests for current behavior
2. Achieve 90% coverage
3. THEN slice new changes
```

### Step 2: Slice Changes, Not Rewrites

```
❌ WRONG: Rewrite entire customer module in slices

✅ CORRECT: Add new capability in slices
  Slice 1: Add address validation to customer lookup
  Slice 2: Add caching for customer lookup
  Slice 3: Add audit logging for customer changes
```

### Step 3: Keep Slices Independent

Each slice should be mergeable without others:

```
✅ Independent Slices:
  Slice 1: Add email confirmation → Can merge alone
  Slice 2: Add SMS confirmation → Can merge alone
  Slice 3: Add push notification → Can merge alone

❌ Dependent Slices:
  Slice 1: Add notification interface (can't merge alone)
  Slice 2: Implement email (depends on Slice 1)
  Slice 3: Implement SMS (depends on Slice 1)
```

---

## Benefits of Vertical Slicing

### For Engineers

- **Clear focus** - Work on one thing at a time
- **Fast feedback** - See results in hours, not weeks
- **Safe refactoring** - Tests verify each slice
- **AI partnership** - AI can assist slice by slice

### For Product Owners

- **Visible progress** - Demo working features daily
- **Early course-correction** - Adjust after each slice
- **Reduced risk** - Smaller batches = smaller problems
- **Incremental value** - Users benefit sooner

### For AI-Assisted Development

- **Manageable scope** - AI handles one slice at a time
- **Verifiable compliance** - Check laws per slice
- **Clear boundaries** - AI knows when slice is done
- **Teaching moments** - AI explains decisions per slice

---

## Anti-Patterns to Avoid

### ❌ Horizontal Slicing

```
Slice 1: All database tables
Slice 2: All services
Slice 3: All controllers

Problem: No working feature until all slices done
```

### ❌ Technology Slicing

```
Slice 1: Backend implementation
Slice 2: Frontend implementation
Slice 3: Integration

Problem: Integration issues discovered late
```

### ❌ Big Bang Slicing

```
Slice 1: The entire feature

Problem: Not a slice at all!
```

---

## Related Guides

- [Atomic TDD Law](./atomic-tdd-law.md) - TDD within each slice
- [Brownfield Adoption](../adoption/brownfield-adoption.md) - Slicing in existing projects
- [Greenfield MVP](../adoption/greenfield-mvp.md) - Slicing for new projects
- [Prompt Patterns](../prompts/prompt-patterns.md) - AI prompts for slicing

---

**Constitutional Reference:** Article IV, Section 4.1; Hangar SDD Workflow  
**Last Updated:** January 27, 2026

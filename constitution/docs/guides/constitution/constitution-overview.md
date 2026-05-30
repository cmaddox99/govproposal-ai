# Constitution Overview

**Purpose:** Understand the Constitutional governance model that enables 100% AI-Assisted Coding.

**Constitutional Reference:** All Three Constitutions
**Time to Read:** 20 minutes

---

## What Is the Constitution?

The Constitution is a **governance framework** consisting of three complementary documents that define the laws, principles, and standards governing all development. Together, they answer:

| Constitution | Question | Focus |
|--------------|----------|-------|
| [**Engineering**](../../../laws/engineering/) | **HOW** do we build? | Code quality, testing, architecture, DevOps |
| [**Product**](../../../laws/product/) | **WHAT** do we build? | User journeys, metrics, accessibility, experimentation |
| [**Business**](../../../laws/business/) | **WHY** and under what constraints? | Compliance, domain rules, data governance |

### Why Three Constitutions?

- **Engineering Laws** - How code must be written, tested, and deployed
- **Product Laws** - What user problems we solve and how we measure success
- **Business Laws** - Compliance requirements (FAA, TSA, DOT) and domain rules
- **Architecture Patterns** - How systems are structured (DDD, vertical slices)
- **Code Quality Standards** - What "good code" looks like
- **Aviation Compliance** - FAA Part 121, DO-178C, TSA, DOT requirements

---

## Why Constitutional Governance?

### The Problem Without a Constitution

```
Developer A: "I think we should use mocks for everything"
Developer B: "No, we should use real objects"
Developer C: "Let's just copy the pattern from that other project"
AI Agent:    "I'll do whatever you tell me..."

Result: Inconsistent code, conflicting patterns, technical debt
```

### The Solution With a Constitution

```
Constitution: "Section 4.6 - Mock only external I/O boundaries"

Developer A: "The Constitution says mock only I/O"
Developer B: "Makes sense, let's follow that"
Developer C: "I'll update my approach to match"
AI Agent:    "I will follow Section 4.6 and mock only external services"

Result: Consistent code, clear patterns, AI alignment
```

---

## The Constitution Enables AI-Assisted Development

### How AI Agents Use the Constitution

When you work with AI agents in a Constitutional codebase:

1. **AI reads the Constitution** before any development work
2. **AI follows the laws** - no shortcuts, no "just this once"
3. **AI explains decisions** by referencing Constitutional sections
4. **AI refuses violations** - won't write code that breaks laws

**Example Interaction:**

```
Engineer: "Add a quick test that mocks the service layer"

AI: "I notice this would violate Section 4.6 (Test Isolation Law) which states
     'Mock only external I/O boundaries, not internal collaborators.'

     Instead, I'll write a unit test that uses the real service with mocked
     external dependencies (email service, iCargo service).

     Would you like me to proceed with a Constitutional-compliant test?"
```

### The Teaching Feedback Loop

The Constitution creates a **learning partnership** between engineers and AI:

```
┌─────────────────────────────────────────────────────────────────────┐
│  1. AI follows Constitution strictly                                │
│  2. AI explains WHY (references Constitutional principles)          │
│  3. Engineer observes and learns (builds mental models)             │
│  4. Engineer develops judgment (internalizes principles)            │
│  5. Prompts become intentional (better understanding = precision)   │
│  6. Pair becomes effective (junior + AI = senior-level output)      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Constitution Structure

### Preamble
- **Mission** - What the system exists to do
- **Organization** - Who owns the system
- **Architecture** - High-level system design

### Article 0: Project Context
- System landscape and integrations
- Existing codebase assets
- Business domains
- Technology philosophy

### Article I: Foundational Principles
- Primary objectives (priority order)
- Bounded context
- API versioning
- Authentication/authorization
- **Continuous Refactoring Law** (Boy Scout Rule)
- **AI-Engineer Pairing Law**

### Article II: Architecture Laws
- **Domain-Driven Design Law**
- Layered architecture
- Spring Boot best practices
- Database architecture
- Integration patterns
- REST API design

### Article III: Code Quality Laws
- Style and formatting
- **Complexity limits** (cyclomatic ≤10, cognitive ≤7)
- **Immutability Law**
- **Law of Demeter**
- Documentation requirements
- Git workflow

### Article IV: Testing Laws
- **Atomic TDD Law** (8-step cycle)
- **Test Pyramid Law**
- Coverage requirements (90% line, 85% branch)
- Test naming and structure
- **Test Abstraction Level Law**
- Test isolation
- Mutation testing
- Integration test standards
- **Test Decomposition Law**

### Article V: Security and Compliance
- Authentication
- Authorization
- Data protection
- Audit trails
- Input validation
- Error handling

### Article VI: Performance and Reliability
- Performance targets
- Caching strategies
- Database optimization
- Resilience patterns
- Monitoring and observability

### Article VII: Business Domain Laws
- Domain-specific rules
- Entity behaviors
- Validation requirements

### Article VIII: Deployment and Operations
- Environment strategy
- Configuration management
- Build and packaging
- CI/CD requirements

### Article IX: Current State
- Existing codebase status
- Technical debt inventory
- Strengths to preserve

### Article X: Amendment Process
- How to change the Constitution
- Law precedence rules

---

## Key Laws Every Engineer Must Know

### 1. Atomic TDD Law (Article IV, Section 4.1)

**The 8-Step Cycle:**
```
RED → GREEN → REFACTOR → VERIFY → DOCUMENT → COMMIT → PUSH → REPEAT
```

Every test follows this cycle. No batch testing. No skipping steps.

### 2. Test Pyramid Law (Article IV, Section 4.2)

**Distribution:**
- 70-80% Unit Tests (fast, no Spring context)
- 15-25% Integration Tests (controller layer only)
- 5-10% E2E Tests (critical paths only)

### 3. Continuous Refactoring Law (Article I, Section 1.5)

> "Leave the code cleaner than you found it."

When you touch a file, you MUST fix:
- Cyclomatic complexity > 10
- Cognitive complexity > 7
- Law of Demeter violations
- Large methods (>50 lines)
- Missing JavaDoc

### 4. Law of Demeter (Article III, Section 3.4)

**Don't chain method calls:**
```java
// ❌ VIOLATION
String city = application.getCustomer().getAddress().getCity();

// ✅ CORRECT
String city = application.getShippingCity();
```

### 5. Immutability Law (Article III, Section 3.3)

**Value objects and DTOs SHALL be immutable:**
```java
// ✅ CORRECT - Immutable
public final class Money {
    private final BigDecimal amount;
    private final String currency;
    
    public Money add(Money other) {
        return new Money(this.amount.add(other.amount), this.currency);
    }
}
```

---

## How to Read the Constitution

### For New Team Members

1. **Read the Preamble** - Understand the mission
2. **Read Article 0** - Understand the system context
3. **Read Article IV** - Understand testing requirements
4. **Skim other articles** - Know what exists for reference

### For Working on Features

Before starting any work:
1. Read relevant sections for your domain
2. Review the Testing Laws (Article IV)
3. Check Code Quality Laws (Article III)
4. Verify Architecture compliance (Article II)

### For AI Agents

AI agents are instructed to:
1. Read the entire Constitution before any development
2. Reference specific sections when making decisions
3. Refuse to violate Constitutional laws
4. Explain the "why" behind every decision

---

## Constitution vs. Other Documents

| Document | Purpose | Authority |
|----------|---------|-----------|
| **Constitution** | Laws that MUST be followed | Highest - Non-negotiable |
| **AGENTS.md** | Workflow instructions for AI | High - Process guidance |
| **project.md** | Project context and conventions | Medium - Project-specific |
| **specs/** | What IS built (current truth) | Medium - Feature documentation |
| **changes/** | What SHOULD change (proposals) | Low - Proposed changes |

---

## Amending the Constitution

The Constitution can be changed through:

1. **Hangar SDD proposal** - Create change proposal
2. **Review** - Team reviews proposed amendment
3. **Approval** - Maintainers approve change
4. **Documentation** - Update Constitution with changelog

### Law Precedence (When Conflicts Arise)

1. **Security laws** - Non-negotiable
2. **Data integrity** - Takes precedence over performance
3. **Testing laws** - Cannot be waived
4. **Code quality** - Must be maintained
5. **API contracts** - Must remain backward compatible

---

## Common Questions

### Q: Can I skip a Constitutional requirement "just this once"?

**No.** The Constitution exists precisely to prevent "just this once" exceptions that accumulate into technical debt.

### Q: What if the Constitution is wrong?

Create an Hangar SDD proposal to amend it. Don't violate it - change it through the proper process.

### Q: How strictly does AI follow the Constitution?

**100% strictly.** AI agents are configured to refuse any request that violates Constitutional laws.

### Q: What if I don't understand a law?

Read the detailed guide for that law (linked in this index). Ask the AI to explain it. The AI will cite the Constitutional section and explain the reasoning.

---

## The Adoption Hierarchy

Beyond the three base constitutions, laws are specialized through adoptions:

```
┌─────────────────────────────────────────────────────────────────┐
│                    THREE BASE CONSTITUTIONS                      │
│              Engineering + Product + Business                    │
├─────────────────────────────────────────────────────────────────┤
│                   INDUSTRY ADOPTION                              │
│            Aviation: FAA Part 121, DO-178C, TSA, DOT            │
├─────────────────────────────────────────────────────────────────┤
│                  PRODUCT-TYPE ADOPTION                           │
│      Booking | Cargo | Loyalty | Operations | Service           │
├─────────────────────────────────────────────────────────────────┤
│                  TECHNOLOGY ADOPTION                             │
│        Java/Spring | React | Python | .NET | Node.js            │
└─────────────────────────────────────────────────────────────────┘
```

### Aviation Industry Adoption

All American Airlines projects must adopt the [Aviation/FAA Adoption](../../../avatars/industry/aviation-faa/ADOPTION.md), which includes:
- **FAA Part 121** - Air carrier certification
- **DO-178C** - Airborne software assurance levels
- **DO-326A** - Airborne cybersecurity
- **TSA Requirements** - Security and vetting
- **DOT Regulations** - Consumer protection, refund timelines

### Product Domain Adoptions

Select the adoption matching your product domain:

| Domain | When to Use |
|--------|-------------|
| [Passenger Booking](../../../avatars/product-type/passenger-booking/ADOPTION.md) | Flight search, reservations, ancillaries |
| [Check-In & Travel](../../../avatars/product-type/check-in-travel/ADOPTION.md) | Check-in, boarding, flight status |
| [Cargo & Freight](../../../avatars/product-type/cargo-freight/ADOPTION.md) | PAL applications, AWB, iCargo |
| [Loyalty (AAdvantage)](../../../avatars/product-type/loyalty-aadvantage/ADOPTION.md) | Miles, status, awards |
| [Airport Operations](../../../avatars/product-type/airport-operations/ADOPTION.md) | Gate management, crew, IROP |
| [Customer Service](../../../avatars/product-type/customer-service/ADOPTION.md) | Rebooking, refunds, complaints |

---

## Next Steps

1. **Read all three base Constitutions** - Engineering, Product, Business
2. **Review the Aviation/FAA adoption** - Compliance requirements
3. **Select your product domain adoption** - Domain-specific rules
4. **Understand the key laws** - Start with Atomic TDD and Test Pyramid
5. **See laws in action** - Review the detailed guides for each law
6. **Practice with AI** - Let the AI teach you by following the Constitution

---

## Related Guides

- [Atomic TDD Law](./atomic-tdd-law.md) - Deep dive into TDD requirements
- [Code Quality Laws](./code-quality-laws.md) - Complexity, immutability, Law of Demeter
- [AI-Engineer Pairing Law](./ai-engineer-pairing-law.md) - How AI teaches through compliance
- [DDD Law](./ddd-law.md) - Domain-Driven Design principles
- [How to Adopt the Constitution](../adoption/how-to-adopt-constitution.md) - Adoption workflow
- [Brownfield Adoption](../adoption/brownfield-adoption.md) - Adopting in existing projects

---

**Constitutional Reference:** All Three Constitutions
**Last Updated:** January 28, 2026

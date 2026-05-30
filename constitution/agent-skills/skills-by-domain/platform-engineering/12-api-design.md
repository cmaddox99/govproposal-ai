---
skill:
  id: skill-12-api-design
  name: API Design
  category: architecture
  version: "2.0.0"

laws:
  implements:
    - id: ENG-1.5
      title: API-First Design Law
    - id: ENG-2.2
      title: Layered Architecture Law
    - id: ENG-4.9
      title: Contract Testing Law
  references:
    - id: ENG-6.2
      title: Authentication Law
    - id: ENG-6.3
      title: Authorization Law
    - id: ENG-7.6
      title: Idempotency Law

triggers:
  phrases:
    - "Design the API"
    - "API contract"
    - "REST endpoint design"
    - "API versioning"

followed_by:
  - skill-06-atomic-tdd
  - skill-16-documentation
---

# Skill: API Design

> **Purpose:** Design consistent, intuitive, and evolvable APIs that serve as reliable contracts between systems.

---

## Purpose

API Design is the disciplined practice of creating interfaces that are easy to use correctly and hard to use incorrectly. This skill ensures:

1. **Consistency** - Predictable patterns across all endpoints
2. **Discoverability** - APIs are self-documenting and intuitive
3. **Evolvability** - APIs can grow without breaking clients
4. **Security** - Security built into the design
5. **Performance** - Efficient data transfer and processing

**Key principle:** APIs are products. Design them for developers, not for your implementation.

---

## When to Invoke

Invoke this skill when:

- Designing new API endpoints
- Modifying existing API contracts
- Integrating with external systems
- Creating internal service interfaces
- Reviewing API designs
- Versioning existing APIs

**Trigger phrases:**
- "Let's design the API for this feature"
- "What should this endpoint look like?"
- "How do we version this API?"
- "Review this API design"
- "We need to add a new field"

---

## Constitutional Foundation

### Engineering Constitution
- **Article II, Section 2.1** - Simplicity: APIs should be intuitive
- **Article II, Section 2.2** - Consistency: Follow established patterns
- **Article IV, Section 4.1** - Test-First: Contract tests before implementation

### Product Constitution
- **Article V, Section 5.1** - Developer Experience: APIs are usable
- **Article IV, Section 4.1** - Incremental: APIs evolve safely

### Business Constitution
- **Article II, Section 2.1** - Contracts: APIs are stable agreements
- **Article III, Section 3.1** - Compatibility: Don't break clients

---

## Quality Checklist

Before considering API design complete:

### Design
- [ ] Resources named with nouns
- [ ] HTTP methods used correctly
- [ ] Status codes appropriate
- [ ] Request/response documented
- [ ] Error format consistent

### Usability
- [ ] Pagination implemented
- [ ] Filtering supported
- [ ] Sorting supported
- [ ] OpenAPI spec generated

### Security
- [ ] Authentication defined
- [ ] Authorization rules documented
- [ ] Rate limiting configured
- [ ] Input validation comprehensive

### Evolution
- [ ] Versioning strategy defined
- [ ] Deprecation policy documented
- [ ] Backward compatibility considered

---

## Skill Interactions

### Preceded By
- **03-Executable Spec** - API behavior specified
- **04-Business Domain Modeling** - Resources from domain model

### Followed By
- **06-Atomic TDD** - Contract tests implemented
- **10-Security Review** - API security reviewed

### Related Skills
- **08-Code Review** - API design reviewed

> 📎 Examples: See 12-api-design-examples.md

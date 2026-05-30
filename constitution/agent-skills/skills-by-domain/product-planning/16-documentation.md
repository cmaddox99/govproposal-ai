---
skill:
  id: skill-16-documentation
  name: Documentation
  category: quality
  version: "2.0.0"

laws:
  implements:
    - id: ENG-3.6
      title: Documentation Law
  references:
    - id: BUS-7.2
      title: Evidence Preservation Law
    - id: ENG-1.5
      title: API-First Design Law

triggers:
  phrases:
    - "Write documentation"
    - "Create ADR"
    - "Runbook needed"
    - "API docs"

followed_by:
  - skill-12-api-design
  - skill-11-incident-response
---

# Skill: Documentation

> **Purpose:** Create and maintain documentation that preserves knowledge, enables onboarding, and explains why decisions were made.

---

## Purpose

Documentation is the practice of capturing knowledge in durable, accessible form. This skill ensures:

1. **Knowledge preservation** - Information survives team changes
2. **Decision clarity** - Why things are the way they are
3. **Onboarding efficiency** - New team members ramp up quickly
4. **Operational safety** - Runbooks prevent incidents
5. **API usability** - Consumers can integrate successfully

**Key principle:** Write for your future self who has forgotten everything. Write for the person on-call at 3 AM.

---

## When to Invoke

Invoke this skill when:

- Making significant architectural decisions
- Creating new services or systems
- Establishing operational procedures
- Onboarding is taking too long
- Same questions asked repeatedly
- After incidents reveal knowledge gaps

**Trigger phrases:**
- "How does this work?"
- "Why did we build it this way?"
- "What do I do when this breaks?"
- "Where is that documented?"
- "Let's write an ADR for this"

---

## Constitutional Foundation

### Engineering Constitution
- **Article VII, Section 7.1** - Documentation: Systems must be documented
- **Article III, Section 3.1** - Simplicity: Docs should be clear and concise

### Product Constitution
- **Article V, Section 5.1** - Developer Experience: APIs documented for consumers

### Business Constitution
- **Article III, Section 3.3** - Audit Trail: Decisions are recorded
- **Article IV, Section 4.1** - Continuity: Knowledge persists

---

## Documentation Types

### Architecture Decision Records (ADRs)

**Purpose:** Capture why architectural decisions were made.

**Template:**

```markdown
# ADR-001: Use PostgreSQL for Primary Database

## Status
Accepted

## Context
We need to choose a primary database for the order management system.
Requirements:
- ACID transactions for financial data
- Complex queries across related entities
- Team familiarity
- Managed service availability

## Decision
We will use PostgreSQL as our primary database.

## Alternatives Considered

### MongoDB
- Pros: Flexible schema, horizontal scaling
- Cons: Weaker transactions, team inexperience
- Rejected because: Order data has complex relationships

### MySQL
- Pros: Mature, team familiarity
- Cons: Less powerful for complex queries
- Rejected because: PostgreSQL has better JSON support

## Consequences

### Positive
- Strong ACID guarantees
- Rich query capabilities
- Team knows PostgreSQL well
- AWS RDS available

### Negative
- Vertical scaling limits
- Need to manage schema migrations carefully

### Neutral
- Need to set up connection pooling

## References
- [PostgreSQL vs MongoDB comparison](...)
- [Team database survey results](...)
```

**ADR Lifecycle:**
```
Proposed → Accepted/Rejected/Deprecated → Superseded
```

---

### README Files

**Repository README:**

```markdown
# Order Service

Brief description of what this service does.

## Quick Start

```bash
# Prerequisites
- Docker
- Node.js 20+

# Setup
npm install
docker-compose up -d
npm run migrate
npm run dev
```

## Architecture

```
┌─────────────────┐     ┌─────────────────┐
│   API Gateway   │────▶│  Order Service  │
└─────────────────┘     └────────┬────────┘
                                 │
                    ┌────────────┼────────────┐
                    ▼            ▼            ▼
              ┌──────────┐ ┌──────────┐ ┌──────────┐
              │ Postgres │ │  Redis   │ │ Payment  │
              └──────────┘ └──────────┘ │ Service  │
                                        └──────────┘
```

## API Documentation
See [API.md](./docs/API.md) or run `npm run docs`

## Development

### Running Tests
```bash
npm test              # Unit tests
npm run test:int      # Integration tests
npm run test:e2e      # E2E tests
```

### Database Migrations
```bash
npm run migrate       # Run migrations
npm run migrate:undo  # Rollback last migration
npm run migrate:new   # Create new migration
```

## Deployment
See [DEPLOYMENT.md](./docs/DEPLOYMENT.md)

## Contributing
See [CONTRIBUTING.md](./CONTRIBUTING.md)

## Related Docs
- [Architecture Decision Records](./docs/adr/)
- [Runbooks](./docs/runbooks/)
- [API Reference](./docs/api/)
```

---

### Runbooks

**Purpose:** Step-by-step guides for operational procedures.

```markdown
# Runbook: High Error Rate in Order Service

## Overview
This runbook addresses elevated error rates (>5%) in the order service.

## Severity
**SEV-2** if error rate >5%
**SEV-1** if error rate >20% or affecting payments

## Symptoms
- Alerts: `OrderServiceHighErrorRate`
- Metrics: `order_service_error_rate > 0.05`
- User reports: "Order failed" errors

## Diagnosis

### Step 1: Check Recent Deployments
```bash
kubectl rollout history deployment/order-service
```
If recent deployment, consider rollback (Step 5).

### Step 2: Check Logs
```bash
kubectl logs -l app=order-service --since=10m | grep ERROR
```
Look for:
- Database connection errors → See DB Runbook
- Payment service errors → Check payment service health
- Validation errors → May indicate bad input

### Step 3: Check Dependencies
```bash
# Database
kubectl exec -it postgres-0 -- pg_isready

# Redis
kubectl exec -it redis-0 -- redis-cli ping

# Payment service
curl -s http://payment-service/health
```

### Step 4: Check Resources
```bash
kubectl top pods -l app=order-service
```
If CPU/memory high, scale up:
```bash
kubectl scale deployment/order-service --replicas=5
```

## Mitigation

### Step 5: Rollback (if recent deploy)
```bash
kubectl rollout undo deployment/order-service
kubectl rollout status deployment/order-service
```

### Step 6: Enable Circuit Breaker
If payment service is failing:
```bash
kubectl set env deployment/order-service PAYMENT_CIRCUIT_BREAKER=true
```

### Step 7: Scale Up
```bash
kubectl scale deployment/order-service --replicas=10
```

## Resolution Verification
- Error rate returns to <1%
- No new error alerts for 15 minutes
- Sample orders completing successfully

## Post-Incident
- Create incident ticket
- Schedule postmortem if SEV-1/2
- Update this runbook if needed

## Escalation
If not resolved in 30 minutes:
- Page: @order-team-oncall
- Slack: #order-service-incidents

## Related
- [Database Runbook](./database-issues.md)
- [Payment Service Runbook](./payment-service.md)
```

---

### API Documentation

**OpenAPI/Swagger:**

```yaml
openapi: 3.0.3
info:
  title: Order Service API
  description: |
    API for managing customer orders.

    ## Authentication
    All endpoints require Bearer token authentication.

    ## Rate Limiting
    - 100 requests per minute per API key
    - 429 response when exceeded

    ## Pagination
    List endpoints support `page` and `per_page` parameters.

  version: 1.0.0

paths:
  /orders:
    get:
      summary: List orders
      description: |
        Returns a paginated list of orders for the authenticated user.

        Orders are sorted by creation date, newest first.
      parameters:
        - name: status
          in: query
          description: Filter by order status
          schema:
            type: string
            enum: [pending, paid, shipped, delivered]
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: per_page
          in: query
          schema:
            type: integer
            default: 20
            maximum: 100
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/Order'
                  pagination:
                    $ref: '#/components/schemas/Pagination'
              example:
                data:
                  - id: "ord_123"
                    status: "pending"
                    total: 99.99
                pagination:
                  page: 1
                  per_page: 20
                  total_count: 150
```

---

### Code Documentation

**Function Documentation:**

```python
def calculate_shipping_cost(
    items: list[OrderItem],
    destination: Address,
    shipping_method: ShippingMethod
) -> Decimal:
    """
    Calculate shipping cost for an order.

    Uses weight-based pricing with regional adjustments.
    Expedited shipping adds a flat surcharge.

    Args:
        items: List of items to ship. Each must have weight_kg.
        destination: Shipping address with country_code.
        shipping_method: STANDARD, EXPRESS, or OVERNIGHT.

    Returns:
        Shipping cost in USD, rounded to 2 decimal places.

    Raises:
        InvalidAddressError: If destination country not supported.
        ShippingMethodUnavailable: If method not available for destination.

    Example:
        >>> items = [OrderItem(sku="WIDGET", weight_kg=0.5)]
        >>> address = Address(country_code="US", state="CA")
        >>> calculate_shipping_cost(items, address, ShippingMethod.STANDARD)
        Decimal('5.99')

    Note:
        For orders over $100, standard shipping is free (domestic only).
        See SHIPPING_POLICY.md for full pricing rules.
    """
```

**When to document code:**
- Public APIs (always)
- Complex algorithms (explain the why)
- Non-obvious behavior (gotchas)
- Business rules encoded in code

**When NOT to document:**
```python
# BAD: Obvious documentation
def get_user_by_id(user_id: int) -> User:
    """Gets a user by their ID."""  # Adds nothing
    return db.query(User).get(user_id)

# GOOD: No doc needed, code is clear
def get_user_by_id(user_id: int) -> User:
    return db.query(User).get(user_id)
```

---

### Onboarding Documentation

```markdown
# Engineering Onboarding Guide

## Week 1: Environment Setup

### Day 1: Access & Tools
- [ ] GitHub access granted
- [ ] Slack channels joined: #engineering, #team-orders
- [ ] 1Password vault access
- [ ] Development laptop configured

### Day 2: Local Development
- [ ] Clone repositories (see [repos.md](./repos.md))
- [ ] Run local environment (see [local-setup.md](./local-setup.md))
- [ ] Complete "Hello World" deployment

### Day 3-5: Codebase Tour
- [ ] Architecture overview session
- [ ] Read top 5 ADRs
- [ ] Pair with buddy on small task

## Week 2: First Contributions

### Goals
- [ ] Complete first PR (starter issue)
- [ ] Participate in code review
- [ ] Attend team ceremonies

### Suggested First Issues
See issues labeled `good-first-issue`

## Key Resources

| Resource | Purpose |
|----------|---------|
| [Architecture Guide](./architecture.md) | System overview |
| [ADRs](./adr/) | Decision history |
| [Runbooks](./runbooks/) | Operational procedures |
| [API Docs](./api/) | API reference |

## Who to Ask

| Topic | Person |
|-------|--------|
| Architecture | @alice |
| Database | @bob |
| Deployment | @charlie |
| Domain questions | @domain-expert |

## Common Gotchas

1. **Database migrations**: Always run `npm run migrate` after pulling
2. **Environment variables**: Copy `.env.example` to `.env`
3. **Docker memory**: Increase Docker memory to 8GB
```

---

## Documentation Maintenance

### Keep Docs Fresh

```markdown
## Documentation Review Schedule

| Doc Type | Review Frequency | Owner |
|----------|-----------------|-------|
| README | Each release | Team lead |
| ADRs | When superseded | Author |
| Runbooks | After each incident | On-call |
| API docs | Each API change | Developer |
| Onboarding | Quarterly | Team lead |
```

### Doc-as-Code Practices

```yaml
# .github/workflows/docs.yml
name: Documentation CI

on:
  pull_request:
    paths:
      - 'docs/**'
      - '*.md'

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Lint Markdown
        uses: markdownlint/markdownlint-action@v1

  links:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Check Links
        uses: lycheeverse/lychee-action@v1
        with:
          args: --verbose docs/
```

---

## Good Examples

### Example 1: Self-Maintaining Docs

```markdown
<!-- README.md -->

## API Endpoints

<!-- AUTO-GENERATED FROM OPENAPI SPEC -->
<!-- Run `npm run docs:generate` to update -->

| Method | Path | Description |
|--------|------|-------------|
| GET | /orders | List orders |
| POST | /orders | Create order |
| GET | /orders/{id} | Get order |

<!-- END AUTO-GENERATED -->
```

---

## Bad Examples (Anti-Patterns)

### Anti-Pattern 1: Write-Only Documentation

```markdown
# API Guide (Last updated: 2019)

The API uses REST...

[Entire doc is 3 years out of date]
```

**Correct approach:** Review schedule, doc owners, CI checks.

---

### Anti-Pattern 2: Documentation Dump

```markdown
# Everything You Need to Know

[500 pages of unstructured text]
[No table of contents]
[No search]
```

**Correct approach:** Structured docs, clear navigation, searchable.

---

### Anti-Pattern 3: No "Why"

```markdown
# Architecture

We use PostgreSQL.
We use Redis.
We use Kubernetes.

[No explanation of why these choices were made]
```

**Correct approach:** ADRs explain context and rationale.

---

## Quality Checklist

Before considering documentation complete:

### Content
- [ ] Answers "why" not just "what"
- [ ] Written for the audience
- [ ] Examples included
- [ ] Accurate and tested

### Structure
- [ ] Logical organization
- [ ] Table of contents for long docs
- [ ] Cross-references where helpful

### Maintenance
- [ ] Owner assigned
- [ ] Review schedule defined
- [ ] Links validated
- [ ] Version/date visible

### Accessibility
- [ ] Findable (good naming, location)
- [ ] Searchable
- [ ] Readable formatting

---

## Skill Interactions

### Preceded By
- **11-Incident Response** - Incidents reveal documentation gaps
- **All skills** - Major work should be documented

### Followed By
- **Onboarding** - Good docs enable fast ramp-up

### Related Skills
- **14-Technical Debt** - Missing docs is debt
- **12-API Design** - APIs need documentation

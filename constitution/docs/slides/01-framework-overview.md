# The Agentic SDLC Framework

> **How AI Agents Build Software Under Constitutional Governance**

---

## What is Agentic SDLC?

Software Development Lifecycle (SDLC) powered by AI agents that follow explicit rules, use proven techniques, and adapt to your context.

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   Traditional SDLC              vs.        Agentic SDLC             │
│                                                                     │
│   Human writes code                        AI agent writes code     │
│   Human decides approach                   Agent follows Constitution│
│   Quality varies by person                 Quality is consistent    │
│   Knowledge in people's heads              Knowledge in skills      │
│   Process depends on memory                Workflows are explicit   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**The Core Idea:**

> AI agents are powerful, but without guardrails they make inconsistent decisions. The Constitution provides those guardrails. Skills provide the methods. Workflows orchestrate the process.

---

## The Four Components

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│                         AGENTIC SDLC                                │
│                                                                     │
│   ┌─────────────┐                                                   │
│   │ CONSTITUTION│  ← Laws the agent must follow                     │
│   │   (Laws)    │    "Always test first, keep code simple"          │
│   └──────┬──────┘                                                   │
│          │                                                          │
│          │ enforces                                                 │
│          ▼                                                          │
│   ┌─────────────┐                                                   │
│   │   SKILLS    │  ← Techniques the agent knows                     │
│   │ (Techniques)│    "How to do TDD, how to design APIs"            │
│   └──────┬──────┘                                                   │
│          │                                                          │
│          │ combined into                                            │
│          ▼                                                          │
│   ┌─────────────┐                                                   │
│   │  WORKFLOWS  │  ← Processes that chain skills together           │
│   │ (Processes) │    "Discovery → Spec → Build → Review → Ship"     │
│   └──────┬──────┘                                                   │
│          │                                                          │
│          │ customized by                                            │
│          ▼                                                          │
│   ┌─────────────┐                                                   │
│   │  ADOPTIONS  │  ← Context-specific guidance                      │
│   │  (Context)  │    "React patterns, HIPAA compliance, ML ops"     │
│   └─────────────┘                                                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 1. Constitution (The Laws)

The Constitution defines non-negotiable rules that AI agents must follow. Three constitutions govern different concerns:

```
┌─────────────────────────────────────────────────────────────────────┐
│                        THE CONSTITUTION                             │
├─────────────────────┬─────────────────────┬─────────────────────────┤
│                     │                     │                         │
│    ENGINEERING      │      PRODUCT        │       BUSINESS          │
│                     │                     │                         │
│  How we build       │  What we build      │   Why we build          │
│                     │                     │                         │
├─────────────────────┼─────────────────────┼─────────────────────────┤
│                     │                     │                         │
│  • Test-First       │  • Users First      │  • Security Required    │
│    No production    │    Understand the   │    No shipping without  │
│    code without a   │    problem before   │    security review      │
│    failing test     │    building         │                         │
│                     │                     │                         │
│  • Simplicity       │  • Evidence-Based   │  • Audit Trail          │
│    KISS principle,  │    Decisions backed │    All decisions        │
│    no over-         │    by data, not     │    documented and       │
│    engineering      │    assumptions      │    traceable            │
│                     │                     │                         │
│  • Test Pyramid     │  • Small Batches    │  • Compliance           │
│    70-80% unit      │    Ship increments, │    Industry rules       │
│    15-25% integration│   not big bangs    │    are followed         │
│    5-10% E2E        │                     │                         │
│                     │                     │                         │
└─────────────────────┴─────────────────────┴─────────────────────────┘
```

**Real Example - Test-First Law:**

When you ask an AI agent to "add a discount calculation feature", the agent MUST:

```python
# Step 1: Agent writes a failing test FIRST
def test_discount_calculates_percentage():
    cart = Cart(subtotal=100.00)
    discount = Discount(percentage=10)

    result = discount.apply(cart)

    assert result.total == 90.00  # This test fails - no code exists yet

# Step 2: THEN agent writes minimal code to pass
class Discount:
    def __init__(self, percentage: float):
        self.percentage = percentage

    def apply(self, cart: Cart) -> Cart:
        reduction = cart.subtotal * (self.percentage / 100)
        return Cart(subtotal=cart.subtotal - reduction)
```

The Constitution prevents the agent from writing the implementation first and "testing later."

---

## 2. Skills (The Techniques)

Skills are discrete capabilities. Each skill knows how to do ONE thing well while following the Constitution.

```
┌─────────────────────────────────────────────────────────────────────┐
│                          27 SKILLS                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  DISCOVERY & PLANNING                                               │
│  ├── 01-Roadmapping         → Outcome-based planning                │
│  ├── 02-User Journey Mapping → Understanding user problems          │
│  └── 05-Business Rules      → Documenting domain constraints        │
│                                                                     │
│  SPECIFICATION                                                      │
│  ├── 03-Executable Spec     → Gherkin scenarios from requirements   │
│  └── 04-Domain Modeling     → DDD aggregates and bounded contexts   │
│                                                                     │
│  IMPLEMENTATION                                                     │
│  ├── 06-Atomic TDD          → Red-Green-Refactor cycle              │
│  ├── 07-Vertical Slice Dev  → End-to-end feature increments         │
│  └── 08-Code Review         → Quality verification                  │
│                                                                     │
│  OPERATIONS                                                         │
│  ├── 10-Security Review     → OWASP, threat modeling                │
│  ├── 11-Incident Response   → Production issue handling             │
│  ├── 12-API Design          → RESTful patterns                      │
│  └── 13-Observability       → Logging, metrics, tracing             │
│                                                                     │
│  ML/AI                                                              │
│  ├── 17-ML Pipeline         → Training workflows                    │
│  ├── 21-Prompt Engineering  → LLM interaction patterns              │
│  ├── 22-RAG Architecture    → Retrieval-augmented generation        │
│  └── 24-AI Safety           → Guardrails and responsible AI         │
│                                                                     │
│  UX DESIGN                                                          │
│  ├── 25-UX Design           → Design systems, Figma workflows       │
│  └── 26-Design to Code      → Figma MCP, Locofy automation          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Real Example - Skill 06: Atomic TDD:**

When the agent uses this skill, it follows an 8-step cycle:

```
┌─────────────────────────────────────────────────────────────────────┐
│                      ATOMIC TDD CYCLE                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. Pick smallest behavior    "Calculate order total with tax"      │
│  2. Write ONE failing test    test_order_total_includes_tax()       │
│  3. Run test, verify RED      ✗ AssertionError: 0 != 107.50        │
│  4. Write minimal code        def calculate_total(): ...            │
│  5. Run test, verify GREEN    ✓ 1 passed                           │
│  6. Refactor if needed        Extract Tax class                     │
│  7. Run tests again           ✓ 1 passed                           │
│  8. Commit                    "Add order total with tax"            │
│                                                                     │
│  → Repeat for next behavior                                         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

Each skill references which Constitutional laws it follows:

```markdown
## Constitutional Compliance

- **Engineering Article IV, Section 4.1** - Test-First
- **Engineering Article IV, Section 4.2** - Test Pyramid (70% unit)
- **Engineering Article II, Section 2.1** - Simplicity
```

---

## 3. Workflows (The Processes)

Workflows chain multiple skills together for end-to-end processes.

```
┌─────────────────────────────────────────────────────────────────────┐
│              WORKFLOW: Discovery to Delivery                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  PHASE 1: DISCOVER                                                  │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ Skill: User Journey Mapping                                   │  │
│  │                                                               │  │
│  │ Input:  "Users complain checkout is too slow"                 │  │
│  │ Output: Journey map showing 5-step checkout with              │  │
│  │         pain point at payment validation (8 second delay)     │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                              │                                      │
│                              ▼                                      │
│  PHASE 2: SPECIFY                                                   │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ Skill: Executable Spec                                        │  │
│  │                                                               │  │
│  │ Input:  Pain point analysis                                   │  │
│  │ Output: Gherkin scenarios                                     │  │
│  │                                                               │  │
│  │   Scenario: Fast payment validation                           │  │
│  │     Given a customer at checkout with valid card              │  │
│  │     When they submit payment                                  │  │
│  │     Then validation completes within 2 seconds                │  │
│  │     And order confirmation is displayed                       │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                              │                                      │
│                              ▼                                      │
│  PHASE 3: BUILD                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ Skills: Vertical Slice Dev + Atomic TDD                       │  │
│  │                                                               │  │
│  │ Slice 1: Async payment validation                             │  │
│  │   - Unit tests for PaymentValidator (5 tests)                 │  │
│  │   - Integration test for payment gateway (1 test)             │  │
│  │   - E2E test for checkout flow (1 test)                       │  │
│  │                                                               │  │
│  │ Test Pyramid Check: 71% unit, 14% integration, 14% E2E ✓      │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                              │                                      │
│                              ▼                                      │
│  PHASE 4: REVIEW                                                    │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ Skills: Code Review + Security Review                         │  │
│  │                                                               │  │
│  │ Checklist:                                                    │  │
│  │ ✓ Tests pass                                                  │  │
│  │ ✓ No SQL injection in payment handling                        │  │
│  │ ✓ PCI compliance maintained                                   │  │
│  │ ✓ Error handling for gateway timeouts                         │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                              │                                      │
│                              ▼                                      │
│  PHASE 5: SHIP                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ Deploy with monitoring                                        │  │
│  │                                                               │  │
│  │ Metrics: p99 latency dropped from 8s to 1.2s ✓                │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 4. Adoptions (The Context)

Adoptions customize the framework for specific technologies, industries, or product types.

```
┌─────────────────────────────────────────────────────────────────────┐
│                         ADOPTIONS                                   │
├─────────────────────┬─────────────────────┬─────────────────────────┤
│                     │                     │                         │
│    TECHNOLOGY       │     INDUSTRY        │    PRODUCT TYPE         │
│                     │                     │                         │
│  Same Constitution, │  Same Constitution, │  Same Constitution,     │
│  different tools    │  extra compliance   │  different patterns     │
│                     │                     │                         │
├─────────────────────┼─────────────────────┼─────────────────────────┤
│                     │                     │                         │
│  • React/TypeScript │  • Healthcare       │  • E-commerce           │
│  • Python/FastAPI   │    (HIPAA)          │  • SaaS                 │
│  • Java/Spring      │  • Finance          │  • Mobile               │
│  • PyTorch          │    (SOX, PCI)       │  • Data Platform        │
│  • LangChain        │  • Aviation         │  • ML/AI                │
│  • AWS SageMaker    │    (FAA)            │                         │
│  • Vector DBs       │                     │                         │
│                     │                     │                         │
└─────────────────────┴─────────────────────┴─────────────────────────┘
```

**Real Example - React/TypeScript Adoption:**

When building a React component, the adoption provides:

```typescript
// Testing pattern from adoption
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

describe('PaymentForm', () => {
  it('submits payment when form is valid', async () => {
    const onSubmit = jest.fn();
    render(<PaymentForm onSubmit={onSubmit} />);

    await userEvent.type(screen.getByLabelText('Card Number'), '4111111111111111');
    await userEvent.type(screen.getByLabelText('Expiry'), '12/25');
    await userEvent.click(screen.getByRole('button', { name: 'Pay' }));

    expect(onSubmit).toHaveBeenCalledWith({
      cardNumber: '4111111111111111',
      expiry: '12/25'
    });
  });
});

// Component pattern from adoption
export const PaymentForm: React.FC<PaymentFormProps> = ({ onSubmit }) => {
  const [formState, setFormState] = useState<PaymentFormState>(initialState);

  // ... implementation follows adoption patterns
};
```

**Real Example - Healthcare (HIPAA) Adoption:**

Adds extra requirements to the Constitution:

```
┌─────────────────────────────────────────────────────────────────────┐
│  HIPAA ADOPTION - Additional Rules                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ✓ All PHI must be encrypted at rest and in transit                 │
│  ✓ Access logs required for any data containing PHI                 │
│  ✓ Minimum necessary principle - only access needed data            │
│  ✓ Audit trails for all PHI access                                  │
│  ✓ Security review MUST include PHI exposure check                  │
│                                                                     │
│  Code Review Checklist Addition:                                    │
│  - [ ] No PHI in logs                                               │
│  - [ ] No PHI in error messages                                     │
│  - [ ] PHI access is role-gated                                     │
│  - [ ] Data retention policies enforced                             │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## How It Works Together

**Scenario:** "Add a patient appointment booking feature to our healthcare app"

```
┌─────────────────────────────────────────────────────────────────────┐
│  1. WORKFLOW SELECTED                                               │
│     → Discovery to Delivery workflow                                │
│                                                                     │
│  2. ADOPTIONS ACTIVATED                                             │
│     → React/TypeScript (frontend)                                   │
│     → Python/FastAPI (backend)                                      │
│     → Healthcare/HIPAA (compliance)                                 │
│                                                                     │
│  3. SKILLS EXECUTED (following workflow)                            │
│                                                                     │
│     User Journey Mapping                                            │
│     └── Output: Patient booking journey with PHI touchpoints        │
│                                                                     │
│     Executable Spec                                                 │
│     └── Output: Gherkin scenarios including HIPAA scenarios         │
│         "Given a patient's PHI is displayed                         │
│          When an unauthorized user accesses the page                │
│          Then access is denied and audit log is created"            │
│                                                                     │
│     Atomic TDD                                                      │
│     └── Tests written first, following React Testing Library        │
│         patterns from the adoption                                  │
│                                                                     │
│     Security Review                                                 │
│     └── HIPAA checklist from adoption is included                   │
│         - PHI encryption verified                                   │
│         - Audit logging verified                                    │
│         - Access controls verified                                  │
│                                                                     │
│  4. CONSTITUTION ENFORCED (throughout)                              │
│     ✓ Test-First Law: All code has tests                           │
│     ✓ Simplicity Law: No over-engineering                          │
│     ✓ Security Law: HIPAA compliance verified                      │
│     ✓ Audit Law: All decisions documented                          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Good vs. Bad Examples

### Testing

```
┌─────────────────────────────────────────────────────────────────────┐
│  ✗ VIOLATES CONSTITUTION                                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  // Agent writes implementation first                               │
│  class PaymentProcessor:                                            │
│      def process(self, amount):                                     │
│          return self.gateway.charge(amount)                         │
│                                                                     │
│  // Then adds tests after (or never)                                │
│  # TODO: Add tests later                                            │
│                                                                     │
│  Problem: No failing test existed before code was written           │
│  Violation: Engineering Constitution Article IV, Section 4.1        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  ✓ FOLLOWS CONSTITUTION                                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  # Step 1: Agent writes failing test                                │
│  def test_payment_processor_charges_gateway():                      │
│      gateway = MockGateway()                                        │
│      processor = PaymentProcessor(gateway)                          │
│                                                                     │
│      processor.process(amount=100.00)                               │
│                                                                     │
│      gateway.charge.assert_called_once_with(100.00)                 │
│                                                                     │
│  # Step 2: Agent runs test → RED (fails, class doesn't exist)       │
│  # Step 3: Agent writes minimal implementation                      │
│  # Step 4: Agent runs test → GREEN                                  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Complexity

```
┌─────────────────────────────────────────────────────────────────────┐
│  ✗ VIOLATES CONSTITUTION                                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  // Agent over-engineers for hypothetical future needs              │
│  class AbstractPaymentStrategyFactoryBuilder<T extends Payment> {   │
│      private final Map<String, Supplier<Strategy<T>>> registry;     │
│      private final ConfigurationProvider configProvider;            │
│      // ... 200 more lines for a simple payment                     │
│  }                                                                  │
│                                                                     │
│  Problem: Building for imaginary future requirements                │
│  Violation: Engineering Constitution Article II, Section 2.1       │
│             "Simplicity: KISS principle"                            │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  ✓ FOLLOWS CONSTITUTION                                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  // Agent writes simplest thing that works                          │
│  class PaymentProcessor:                                            │
│      def __init__(self, gateway):                                   │
│          self.gateway = gateway                                     │
│                                                                     │
│      def process(self, amount: Decimal) -> PaymentResult:           │
│          return self.gateway.charge(amount)                         │
│                                                                     │
│  // If we need strategies later, we'll add them when needed         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Test Pyramid

```
┌─────────────────────────────────────────────────────────────────────┐
│  ✗ VIOLATES CONSTITUTION                                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Test Distribution:                                                 │
│  • Unit tests: 10%         ← Too few                               │
│  • Integration tests: 20%                                           │
│  • E2E tests: 70%          ← Way too many (slow, brittle)          │
│                                                                     │
│  Problem: Inverted pyramid, slow test suite, flaky tests            │
│  Violation: Engineering Constitution Article IV, Section 4.2        │
│             "Test Pyramid: 70-80% unit, 15-25% int, 5-10% E2E"     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  ✓ FOLLOWS CONSTITUTION                                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Test Distribution:                                                 │
│  • Unit tests: 75%         ← Fast, focused, isolated               │
│  • Integration tests: 18%  ← API boundaries, database              │
│  • E2E tests: 7%           ← Critical user journeys only           │
│                                                                     │
│  Result: Fast feedback, reliable tests, easy debugging              │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Security

```
┌─────────────────────────────────────────────────────────────────────┐
│  ✗ VIOLATES CONSTITUTION                                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  // Agent skips security review to ship faster                      │
│  def get_user(user_id):                                             │
│      query = f"SELECT * FROM users WHERE id = {user_id}"            │
│      return db.execute(query)  # SQL injection vulnerability        │
│                                                                     │
│  Problem: Security review skipped, SQL injection shipped            │
│  Violation: Business Constitution Article VII, Section 7.1          │
│             "Security vulnerabilities are prevented"                │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  ✓ FOLLOWS CONSTITUTION                                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  // Agent uses parameterized queries                                │
│  def get_user(user_id: int) -> User:                                │
│      query = "SELECT * FROM users WHERE id = :id"                   │
│      return db.execute(query, {"id": user_id})                      │
│                                                                     │
│  // Security review checklist completed:                            │
│  // ✓ Parameterized queries (no SQL injection)                      │
│  // ✓ Input validation on user_id                                   │
│  // ✓ Authorization check before data access                        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Summary

```
┌─────────────────────────────────────────────────────────────────────┐
│                      AGENTIC SDLC FRAMEWORK                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  CONSTITUTION     What rules must be followed                       │
│                   "Test first, keep it simple, security required"   │
│                                                                     │
│  SKILLS           How to do specific tasks                          │
│                   "TDD cycle, API design patterns, security review" │
│                                                                     │
│  WORKFLOWS        When to use which skills                          │
│                   "For new features: discover → spec → build → ship"│
│                                                                     │
│  ADOPTIONS        How to adapt for context                          │
│                   "React patterns, HIPAA rules, ML pipelines"       │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Result: AI agents that produce consistent, high-quality software   │
│          regardless of which developer is working with them         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Why It Matters

**Without Constitutional Governance:**
- AI agents make inconsistent decisions
- Quality varies based on prompts
- Security vulnerabilities slip through
- Technical debt accumulates
- Knowledge stays in people's heads

**With Constitutional Governance:**
- Every AI agent follows the same rules
- Quality is predictable and measurable
- Security is built in, not bolted on
- Code is maintainable and consistent
- Knowledge is encoded in skills and workflows

---

*"The Constitution is not about restricting AI—it's about channeling its power toward consistently excellent outcomes."*

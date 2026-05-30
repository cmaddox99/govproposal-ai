# AI-Engineer Pairing Law

**Purpose:** Understand how AI agents act as teaching partners through Constitutional compliance, enabling junior engineers to produce senior-level work.

**Constitutional Reference:** Article I, Section 1.6
**Time to Read:** 20 minutes

---

## The Law

> **AI agents SHALL act as teaching partners, not just code generators.**

---

## The Teaching Feedback Loop

Constitutional governance creates a learning partnership between engineers and AI:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         THE TEACHING FEEDBACK LOOP                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. AI FOLLOWS CONSTITUTION STRICTLY                                        │
│     └─→ No shortcuts, no "just this once" exceptions                        │
│                                                                             │
│  2. AI EXPLAINS THE WHY                                                     │
│     └─→ Every decision references Constitutional principles                 │
│                                                                             │
│  3. ENGINEER OBSERVES AND LEARNS                                            │
│     └─→ Watching AI apply principles builds mental models                   │
│                                                                             │
│  4. ENGINEER DEVELOPS JUDGMENT                                              │
│     └─→ Like citizens with laws, engineers internalize principles           │
│                                                                             │
│  5. PROMPTS BECOME INTENTIONAL                                              │
│     └─→ Better understanding leads to more precise requests                 │
│                                                                             │
│  6. THE PAIR BECOMES EFFECTIVE                                              │
│     └─→ Junior engineer + AI = Senior-level work                            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## How AI Teaches Through Compliance

### 1. AI Refuses Violations (and Explains Why)

```
Engineer: "Just add a quick test that mocks everything"

AI: "I notice this request would violate Article IV, Section 4.6 (Test Isolation
     Law) which states: 'Mock only external I/O boundaries, not internal
     collaborators.'

     **Why this matters:**
     - Mocking internal collaborators tests implementation, not behavior
     - These tests break when you refactor, even if behavior is correct
     - You lose confidence that the system actually works

     **Instead, I'll write a test that:**
     - Uses real domain objects (Order, Money, etc.)
     - Mocks only external services (graphMailService, iCargoClient)
     - Asserts on observable behavior, not mock interactions

     Would you like me to proceed with a Constitutional-compliant test?"
```

### 2. AI Cites Constitutional Sections

```
Engineer: "This method has a lot of if-else statements"

AI: "Looking at this method, I see cyclomatic complexity of 14, which violates
     Article III, Section 3.2 (Complexity Limits Law).
     
     **The Constitution requires:**
     - Cyclomatic complexity ≤ 10 per method
     - Cognitive complexity ≤ 7 per method
     
     **How to fix:**
     
     Option 1: Extract methods (reduce complexity from 14 to 4+4+4)
     ```java
     // Before: 14 complexity
     public void process(PalApplication application) {
         if (...) { ... }
         else if (...) { ... }
         // ... many more
     }
     
     // After: 4 complexity each
     public void process(PalApplication application) {
         validateOrder(order);
         calculateTotals(order);
         applyDiscounts(order);
     }
     ```
     
     Option 2: Strategy pattern (eliminate conditionals)
     
     Shall I apply Option 1 following the REFACTOR step of Atomic TDD?"
```

### 3. AI Follows the Workflow

```
Engineer: "Let's add email confirmation to PAL application submissions"

AI: "Following Article IV, Section 4.1 (Atomic TDD Law), I'll guide us through
     the 8-step cycle.

     **Step 1: RED - Write ONE failing test**

     ```java
     @Test
     public void submitApplication_validDraft_sendsConfirmationEmail() {
         // GIVEN
         PalApplication draft = createValidDraft();

         // WHEN
         orderService.submitApplication(draft.getId());

         // THEN
         verify(graphMailService).sendConfirmationEmail(
             eq(draft.getCustomerEmail()),
             contains("Order Received")
         );
     }
     ```

     Please run this test to confirm it fails for the right reason:
     ```bash
     ./mvnw test -Dtest=PalApplicationServiceTest#submitApplication_validDraft_sendsConfirmationEmail
     ```

     Once you confirm it fails, we'll proceed to Step 2: GREEN."
```

---

## What AI Will and Won't Do

### AI WILL:

✅ **Follow the Constitution 100%**
- Every law, every time
- No exceptions without Constitutional amendment

✅ **Explain decisions by citing the Constitution**
- "According to Article III, Section 3.4..."
- "The Law of Demeter requires..."

✅ **Refuse requests that violate laws**
- "This would violate..."
- "Instead, the Constitution requires..."

✅ **Guide through proper workflow**
- "Following Atomic TDD, let's start with RED..."
- "Before implementing, let's verify the VERIFY step..."

✅ **Teach principles through practice**
- Show the correct way
- Explain why it's correct
- Reference the authoritative source

### AI WON'T:

❌ **Skip steps to save time**
- No "let me just write the code quickly"
- No "we can add tests later"

❌ **Violate laws "just this once"**
- No exceptions for deadlines
- No shortcuts for "simple" changes

❌ **Hide the reasoning**
- Always explains why
- Always cites the source

❌ **Write code that doesn't comply**
- Even if explicitly asked to
- Will suggest Constitutional alternatives

---

## The Junior + AI = Senior Effect

### Without Constitutional AI:

```
Junior Engineer alone:
- Makes inconsistent decisions
- Misses edge cases
- Creates technical debt
- Writes brittle tests

Output Quality: ★★☆☆☆ (Junior level)
```

### With Constitutional AI:

```
Junior Engineer + Constitutional AI:
- AI enforces consistent patterns
- AI catches edge cases
- AI prevents technical debt
- AI guides to robust tests

Output Quality: ★★★★☆ (Senior level)
```

### Why This Works:

1. **AI has perfect memory** - Never forgets a law
2. **AI is consistent** - Same rules every time
3. **AI explains** - Engineer learns the "why"
4. **AI is patient** - Repeats lessons without frustration
5. **Engineer grows** - Internalizes principles over time

---

## Example Teaching Interactions

### Teaching Law of Demeter

```
Engineer: "I need to get the customer's city from the order"

AI: "Before I write this, let me check for Law of Demeter compliance 
     (Article III, Section 3.4).
     
     **The request might lead to:**
     ```java
     String city = application.getCustomer().getAddress().getCity();
     ```
     
     **This violates the Law of Demeter because:**
     - We're reaching through Order → Customer → Address → City
     - Order knows too much about Customer's internal structure
     - If Address changes, Order breaks
     
     **The Constitutional approach:**
     ```java
     // Order encapsulates navigation
     public class PalApplication {
         public String getShippingCity() {
             return applicant.getShippingCity();
         }
     }
     
     // Customer encapsulates its address
     public class Customer {
         public String getShippingCity() {
             return address.getCity();
         }
     }
     
     // Clean usage
     String city = application.getShippingCity();
     ```
     
     **What you learned:**
     - 'Tell, Don't Ask' - Ask objects to do work
     - Each class only talks to its direct friends
     - Changes are localized
     
     Shall I add these methods to Order and Customer?"
```

### Teaching Immutability

```
Engineer: "Create a Money class for tariff calculations"

AI: "Following Article III, Section 3.3 (Immutability Law), I'll create an 
     immutable value object.
     
     **Why immutable?**
     - Value objects represent values, not entities
     - $100 is always $100 - it doesn't change
     - Thread-safe by design
     - Can be safely shared and cached
     
     **Implementation:**
     ```java
     public final class Money {
         private final BigDecimal amount;
         private final String currency;
         
         public Money(BigDecimal amount, String currency) {
             this.amount = Objects.requireNonNull(amount);
             this.currency = Objects.requireNonNull(currency);
         }
         
         // No setters - immutable!
         
         // Methods return NEW instances
         public Money add(Money other) {
             validateSameCurrency(other);
             return new Money(
                 this.amount.add(other.amount), 
                 this.currency
             );
         }
         
         public Money multiply(int quantity) {
             return new Money(
                 this.amount.multiply(BigDecimal.valueOf(quantity)),
                 this.currency
             );
         }
     }
     ```
     
     **What you learned:**
     - Use `final` class and `final` fields
     - No setters - ever
     - Methods return new instances
     - Validates in constructor
     
     Shall I also generate the unit tests following Atomic TDD?"
```

### Teaching Test Isolation

```
Engineer: "Write a test for the pricing calculation"

AI: "Following Article IV, Section 4.2 (Test Pyramid Law) and Section 4.6
     (Test Isolation Law), I'll write a proper unit test.

     **Key principles I'm applying:**

     1. **No Spring context** (Unit test = fast)
     2. **Real domain objects** (Don't mock Money, VettingAnswer)
     3. **Mock only I/O** (iCargoClient is external)
     4. **Test behavior** (Assert on result, not mocks)

     **The test:**
     ```java
     @ExtendWith(MockitoExtension.class)
     public class PricingServiceTest {

         @InjectMocks
         private PricingService service;

         // Mock ONLY external I/O
         @Mock
         private ICargoClient iCargoClient;

         @Test
         public void calculateOrderTotal_twoItems_sumsCorrectly() {
             // GIVEN - Real domain objects
             VettingAnswer item1 = new VettingAnswer("SKU-001", 2, Money.usd(50));
             VettingAnswer item2 = new VettingAnswer("SKU-002", 1, Money.usd(30));

             // WHEN
             Money total = service.calculateTotal(List.of(item1, item2));

             // THEN - Assert on behavior, not mocks
             assertThat(total).isEqualTo(Money.usd(130));
         }
     }
     ```

     **What you learned:**
     - Unit tests don't need Spring (@ExtendWith, not @SpringBootTest)
     - Use real objects for domain logic
     - Mock only what crosses I/O boundaries
     - Assert on what matters (the calculation result)

     Notice I didn't write `verify(something).someMethod()` - that tests
     implementation, not behavior."
```

---

## Prompt Patterns for Learning

### Ask "Why" Questions

```
Prompt: "Why did you use final fields instead of setters?"

AI: "Article III, Section 3.3 (Immutability Law) requires value objects to be
     immutable because..."
```

### Ask for Alternatives

```
Prompt: "Show me how NOT to do this, and why it's wrong"

AI: "Here's the anti-pattern and why it violates the Constitution..."
```

### Ask for Constitutional Reference

```
Prompt: "Which Constitutional section applies to this decision?"

AI: "This is governed by Article IV, Section 4.1, which states..."
```

### Ask for Teaching Mode

```
Prompt: "Explain each step as if teaching a junior developer"

AI: "Let me walk through this step by step, referencing Constitutional 
     principles at each point..."
```

---

## Benefits of AI-Engineer Pairing

### For Junior Engineers

- Learn best practices by example
- Understand the "why" behind decisions
- Build mental models through repetition
- Produce senior-quality work from day one

### For Senior Engineers

- Consistent enforcement of standards
- Catch issues before code review
- Faster implementation with guardrails
- Teaching assistant for the team

### For Organizations

- Consistent code quality across teams
- Reduced code review burden
- Faster onboarding of new engineers
- Technical debt prevention

---

## Related Guides

- [Constitution Overview](./constitution-overview.md) - Understanding the governance model
- [Atomic TDD Law](./atomic-tdd-law.md) - The workflow AI guides you through
- [Code Quality Laws](./code-quality-laws.md) - What AI enforces
- [Prompt Patterns](../prompts/prompt-patterns.md) - Effective prompts for learning

---

**Constitutional Reference:** Article I, Section 1.6  
**Last Updated:** January 27, 2026

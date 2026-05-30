> Examples for: skill-03-executable-spec  
> Parent skill: 03-executable-spec.md  
> These are optional pedagogical supplements — not in governance scope.

---

## Good Examples

### Example 1: E-commerce Checkout

**Context:** User wants to complete a purchase

```gherkin
Feature: Shopping Cart Checkout
  As a freight forwarder
  I want to complete my purchase
  So that I can receive the products I selected

  Background:
    Given I am a registered customer
    And I have items in my shopping cart

  Scenario: Successful checkout with valid payment
    Given my cart total is $99.99
    And I have entered valid shipping information
    When I submit payment with a valid credit card
    Then my order should be confirmed
    And I should receive an order confirmation email
    And my cart should be empty

  Scenario: Checkout fails with insufficient inventory
    Given my cart contains 5 units of "Widget Pro"
    And only 3 units of "Widget Pro" are in stock
    When I attempt to checkout
    Then I should see an inventory error message
    And I should be offered to adjust my quantity
    And my payment should not be processed

  Scenario: Checkout fails with expired credit card
    Given I have entered an expired credit card
    When I submit payment
    Then I should see a payment error message
    And my order should not be created
    And my cart items should be preserved

  Scenario Outline: Shipping cost calculation by region
    Given my cart total is $50.00
    And my shipping address is in <region>
    When I view my order summary
    Then my shipping cost should be <shipping_cost>
    And my order total should be <total>

    Examples:
      | region        | shipping_cost | total  |
      | domestic      | $5.99         | $55.99 |
      | international | $19.99        | $69.99 |
      | local_pickup  | $0.00         | $50.00 |
```

**Why it's good:**
- Written from user perspective
- Clear Given/When/Then structure
- Covers happy path and key edge cases
- Uses Background to reduce duplication
- Scenario Outline for data variations
- No implementation details

### Example 2: User Authentication

**Context:** User login functionality

```gherkin
Feature: User Authentication
  As a registered user
  I want to log into my account
  So that I can access my personalized content

  Scenario: Successful login with valid credentials
    Given I am on the login page
    And I have a registered account with email "user@example.com"
    When I enter email "user@example.com"
    And I enter my correct password
    And I click the login button
    Then I should be redirected to my dashboard
    And I should see a welcome message with my name

  Scenario: Login fails with incorrect password
    Given I am on the login page
    And I have a registered account with email "user@example.com"
    When I enter email "user@example.com"
    And I enter an incorrect password
    And I click the login button
    Then I should see an error message "Invalid email or password"
    And I should remain on the login page
    And the password field should be cleared

  Scenario: Account locked after multiple failed attempts
    Given I am on the login page
    And I have a registered account with email "user@example.com"
    And I have failed login 4 times in the last hour
    When I enter incorrect credentials again
    Then my account should be temporarily locked
    And I should see a message about the lockout duration
    And I should receive a security alert email

  Scenario: Login with unverified email
    Given I am on the login page
    And I have a registered but unverified account
    When I enter valid credentials
    Then I should see a message to verify my email
    And I should have the option to resend verification
```

**Why it's good:**
- Security considerations included
- Progressive failure handling
- User feedback clearly specified
- Independent scenarios

---

## Bad Examples (Anti-Patterns)

### Anti-Pattern 1: Implementation Details in Specs

```gherkin
# BAD - Exposes implementation
Scenario: User logs in
  Given the user table has a row with email "user@example.com"
  And the password hash is "bcrypt$2b$10$..."
  When I POST to /api/v1/auth/login with JSON body
  And the server validates against the users table
  Then the server returns HTTP 200
  And the response contains a JWT token with 24h expiry
```

**Why it's wrong:**
- References database tables (implementation detail)
- Mentions HTTP methods and endpoints (technical detail)
- Specifies encryption algorithm (implementation detail)
- Business stakeholders cannot understand this

**Correct approach:**
```gherkin
Scenario: Successful login with valid credentials
  Given I have a registered account
  When I log in with valid credentials
  Then I should be authenticated
  And I should remain logged in for the session
```

### Anti-Pattern 2: Vague or Untestable Criteria

```gherkin
# BAD - Vague and untestable
Scenario: Good user experience
  Given a user visits the site
  When they use the features
  Then they should have a good experience
  And the site should be fast
  And it should be easy to use
```

**Why it's wrong:**
- "Good experience" is not measurable
- "Fast" is not defined
- "Easy to use" is subjective
- Cannot be automated

**Correct approach:**
```gherkin
Scenario: Page loads within performance budget
  Given I am on a standard connection
  When I navigate to the product listing page
  Then the page should be interactive within 3 seconds
  And the product images should load progressively

Scenario: User can complete primary task without help
  Given I am a first-time visitor
  When I want to find and purchase a product
  Then I should be able to complete checkout in under 5 steps
  And each step should have clear instructions
```

### Anti-Pattern 3: Dependent Scenarios

```gherkin
# BAD - Scenarios depend on each other
Scenario: Step 1 - Create account
  When I create an account
  Then the account should be created

Scenario: Step 2 - Verify email (depends on Step 1)
  When I click the verification link
  Then my email should be verified

Scenario: Step 3 - Login (depends on Steps 1 and 2)
  When I log in
  Then I should see my dashboard
```

**Why it's wrong:**
- Scenarios are not independent
- Cannot run in isolation
- Order matters (fragile tests)
- Harder to debug failures

**Correct approach:**
```gherkin
Scenario: Create account with valid information
  Given I am a new user
  When I submit valid registration information
  Then my account should be created
  And I should receive a verification email

Scenario: Verify email address
  Given I have a registered but unverified account
  And I have received a verification email
  When I click the verification link
  Then my email should be verified

Scenario: Login with verified account
  Given I have a verified account
  When I log in with valid credentials
  Then I should see my dashboard
```

---

## Artifacts & Templates

### Template: Feature File

```gherkin
Feature: [Feature Name]
  [Optional description providing context]

  As a [role/persona]
  I want [capability/action]
  So that [benefit/value]

  Background:
    Given [common preconditions shared by all scenarios]

  # Happy Path
  Scenario: [Primary success scenario]
    Given [initial state/context]
    When [action performed]
    Then [expected outcome]
    And [additional verifications]

  # Validation Edge Cases
  Scenario: [Validation failure case]
    Given [context]
    When [action with invalid input]
    Then [expected error handling]

  # Authorization Edge Cases
  Scenario: [Authorization failure case]
    Given [unauthorized context]
    When [action attempted]
    Then [expected denial]

  # Business Rule Edge Cases
  Scenario: [Business rule violation]
    Given [context that triggers rule]
    When [action attempted]
    Then [expected rule enforcement]

  # Data Variations
  Scenario Outline: [Parameterized scenario name]
    Given [context with <param1>]
    When [action with <param2>]
    Then [outcome should be <expected>]

    Examples:
      | param1 | param2 | expected |
      | val1   | x      | result1  |
      | val2   | y      | result2  |
```

### Template: Scenario Checklist

```markdown
## Specification Completeness Checklist

### Coverage
- [ ] Happy path documented
- [ ] Validation failures covered
- [ ] Authorization scenarios included
- [ ] Business rule edge cases identified
- [ ] Error states specified
- [ ] Boundary conditions tested

### Quality
- [ ] Written in business language (no tech jargon)
- [ ] Each scenario is independent
- [ ] Given/When/Then clearly separated
- [ ] Scenarios have descriptive names
- [ ] Examples use realistic data

### Stakeholder Validation
- [ ] Product owner has reviewed
- [ ] Business rules verified with domain expert
- [ ] Edge cases validated with support team
```

---


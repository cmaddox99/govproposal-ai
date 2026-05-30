> Examples for: skill-07-vertical-slice-dev  
> Parent skill: 07-vertical-slice-dev.md  
> These are optional pedagogical supplements — not in governance scope.

---

## Good Examples

### Example 1: E-commerce Product Search

**Feature:** Users can search for products and filter results

**Walking Skeleton (Slice 1):**
```
Slice 1: Basic Search
- User types in search box and presses enter
- Results page shows product names matching the query
- No filters, no pagination, no sorting

Layers:
- UI: Search input, basic results list
- API: GET /products?q={query}
- Domain: ProductSearch.find(query)
- Database: SELECT * FROM products WHERE name LIKE '%query%'

Acceptance: Searching "widget" shows products with "widget" in name
```

**Subsequent Slices:**
```
Slice 2: Search Result Details
- Results show product name, price, and thumbnail
- Clicking a result goes to product page
- No filters yet

Slice 3: Category Filter
- Results page shows category checkboxes
- Checking a category filters results
- Multiple categories can be selected

Slice 4: Price Range Filter
- Results page shows price range slider
- Adjusting range filters results
- Combined with category filter

Slice 5: Sort Options
- Results page has sort dropdown
- Options: Relevance, Price Low-High, Price High-Low
- Default is Relevance

Slice 6: Pagination
- Results show 20 per page
- Pagination controls at bottom
- Preserves filters and sort when paging
```

**Why it's good:**
- Each slice is deployable independently
- Users get value from Slice 1 (basic search works)
- Risk addressed early (search infrastructure proven in Slice 1)
- Clear progression of value

### Example 2: User Registration

**Feature:** New users can create an account

**Walking Skeleton:**
```
Slice 1: Minimal Registration
- Form with email and password only
- Clicking submit creates account
- Redirect to success page
- No validation, no confirmation email

Acceptance: Can create account with any email/password
```

**Subsequent Slices:**
```
Slice 2: Email Validation
- Email must be valid format
- Email must be unique
- Error messages displayed inline

Slice 3: Password Requirements
- Password minimum length
- Password strength indicator
- Clear error messages

Slice 4: Confirmation Email
- Email sent after registration
- Email contains verification link
- Success page mentions checking email

Slice 5: Email Verification
- Clicking link verifies email
- Account marked as verified
- Unverified accounts have limitations

Slice 6: Additional Profile Fields
- Name fields added
- Optional fields don't block registration
- Profile completion prompt after verification
```

---

## Bad Examples (Anti-Patterns)

### Anti-Pattern 1: Horizontal Layer Development

```
# BAD - Building layer by layer

Week 1: Database Layer
- Create all tables (users, products, orders, cart, reviews)
- Write all database migrations
- Set up all indexes

Week 2: API Layer
- Create all REST endpoints
- Implement all DTOs
- Add all validation

Week 3: Business Logic
- Implement all services
- Add all business rules
- Write all domain logic

Week 4: UI
- Build all screens
- Connect all APIs
- Add all interactions
```

**Why it's wrong:**
- No user value until Week 4
- Can't test end-to-end until complete
- High risk of integration issues
- No feedback until very late
- Hard to adjust based on learning

**Correct approach:** Build one thin feature through all layers, then the next.

### Anti-Pattern 2: Slice Too Thick

```
# BAD - Slice that's really a whole feature

Slice 1: Complete Shopping Cart
- Add items with quantity selection
- Remove items
- Update quantities
- Apply coupon codes
- Calculate shipping
- Show item availability
- Save for later functionality
- Share cart feature
```

**Why it's wrong:**
- Not a slice, it's the entire feature
- Takes too long to complete
- Too much work-in-progress
- Can't get feedback on parts

**Correct approach:** Split into many thin slices, starting with "add one item."

### Anti-Pattern 3: Technical Slices

```
# BAD - Slices organized by technical tasks

Slice 1: Set up Redux store
Slice 2: Create API client
Slice 3: Build cart component
Slice 4: Write cart service
Slice 5: Create cart table
```

**Why it's wrong:**
- No user value in any slice
- Can't demonstrate progress to stakeholders
- Still horizontal thinking, just smaller
- No end-to-end verification

**Correct approach:** Each slice should deliver user-visible functionality.

### Anti-Pattern 4: Dependent Slices

```
# BAD - Slices that must be done in sequence

Slice 1: Build authentication system
Slice 2: Build user profile (needs auth)
Slice 3: Build shopping cart (needs user)
Slice 4: Build checkout (needs cart)
Slice 5: Build order history (needs orders)

Problem: Can't work on Slice 5 until 1-4 are done
```

**Why it's wrong:**
- Creates bottlenecks
- Reduces parallelization opportunity
- Risk concentrated in early slices

**Correct approach:** Find ways to make slices independent:
- Use feature flags
- Stub dependencies
- Defer authentication to later slice
- Allow anonymous cart initially

---

## Artifacts & Templates

### Template: Slice Plan

```markdown
# Feature Slice Plan: [Feature Name]

## Feature Overview
**User Goal:** [What the user wants to accomplish]
**Total Acceptance Criteria:** [Number of scenarios]
**Estimated Slices:** [Number]

---

## Walking Skeleton (Slice 1)
**Goal:** Prove end-to-end path works with minimal functionality

**Implementation:**
- UI: [Minimal UI element]
- API: [Single endpoint]
- Domain: [Core operation]
- Database: [Minimal schema]

**Acceptance:** [Single happy path criterion]

---

## Slice 2: [Name]
**Goal:** [What this adds]

**Implementation:**
- UI: [Changes]
- API: [Changes]
- Domain: [Changes]
- Database: [Changes]

**Acceptance:**
- [ ] [Criterion]

**Depends on:** Slice 1

---

## Slice 3: [Name]
[Continue pattern...]

---

## Slice Dependency Graph

```
[Slice 1] → [Slice 2] → [Slice 4]
              ↓
           [Slice 3] → [Slice 5]
```

## Parallel Opportunities
- Slices [X] and [Y] can be developed in parallel
- Slices [A] and [B] have no dependencies
```

### Template: Individual Slice Specification

```markdown
# Slice Specification: [Slice Name]

## Overview
**Feature:** [Parent feature name]
**Slice Number:** [N of M]
**Priority:** [High/Medium/Low]

## User Story
As a [role]
I want [action]
So that [benefit]

## Scope

### In Scope
- [What this slice includes]
- [Specific behaviors]

### Out of Scope (Future Slices)
- [What's deliberately excluded]
- [Behaviors for later]

## Technical Layers

### UI Changes
- [ ] [Component/Page changes]

### API Changes
- [ ] [Endpoint: METHOD /path]

### Domain Logic
- [ ] [Service/Entity changes]

### Data Changes
- [ ] [Schema/Query changes]

### External Services
- [ ] [Integration changes]

## Acceptance Criteria
```gherkin
Scenario: [Happy path]
  Given [context]
  When [action]
  Then [outcome]

Scenario: [Edge case]
  Given [context]
  When [action]
  Then [outcome]
```

## Dependencies
- **Requires:** [Other slices that must be done first]
- **Enables:** [Slices that can start after this]

## Notes
[Any additional context, decisions, or considerations]
```

---


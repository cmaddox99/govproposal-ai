---
laws: [ENG-4.1]
avatar: [angular]
title: Atomic TDD — TypeScript/Angular
---

# ENG-4.1: Atomic TDD — angular

Every production behaviour must be covered by a unit test written **before** the implementation.
Tests must run without network, database, or file-system dependencies.

## Example

```
describe('PassengerSearchComponent', () => {
  it('should filter results by destination', () => {
    const results = filterByDestination(flights, 'DFW');
    expect(results.every(f => f.destination === 'DFW')).toBe(true);
  });
});
```

**Rule**: Each test verifies exactly one behaviour. No shared mutable state between tests.

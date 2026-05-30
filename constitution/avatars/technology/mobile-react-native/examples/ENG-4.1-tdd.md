---
laws: [ENG-4.1]
avatar: [mobile-react-native]
title: Atomic TDD — React Native
---

# ENG-4.1: Atomic TDD — mobile-react-native

Every production behaviour must be covered by a unit test written **before** the implementation.
Tests must run without network, database, or file-system dependencies.

## Example

```
it('renders seat selection map with occupied seats greyed out', () => {
  const { getAllByTestId } = render(<SeatMap seats={mockSeats} />);
  const occupied = getAllByTestId('seat-occupied');
  expect(occupied.length).toBe(mockSeats.filter(s=>!s.available).length);
});
```

**Rule**: Each test verifies exactly one behaviour. No shared mutable state between tests.

---
laws: [ENG-4.1]
avatar: [react-typescript]
title: Atomic TDD — TypeScript/React
---

# ENG-4.1: Atomic TDD — react-typescript

Every production behaviour must be covered by a unit test written **before** the implementation.
Tests must run without network, database, or file-system dependencies.

## Example

```
it('shows error message when booking fails', async () => {
  server.use(rest.post('/api/book', (req,res,ctx) => res(ctx.status(500))));
  render(<BookingForm />);
  fireEvent.click(screen.getByRole('button', {name: /confirm/i}));
  expect(await screen.findByText(/booking failed/i)).toBeInTheDocument();
});
```

**Rule**: Each test verifies exactly one behaviour. No shared mutable state between tests.

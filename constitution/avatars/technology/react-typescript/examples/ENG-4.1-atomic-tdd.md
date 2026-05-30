---
law_id: ENG-4.1
avatar: react-typescript
---

# ENG-4.1: Atomic TDD Examples for React + TypeScript

## COMPLIANT: Test-First Development with React Testing Library

```typescript
// UserProfile.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { UserProfile } from './UserProfile';

describe('UserProfile', () => {
  // Step 1: Write the test FIRST (Red phase)
  it('displays user name after loading', async () => {
    // Arrange
    const mockUser = { id: '1', name: 'Jane Doe', email: 'jane@example.com' };

    // Act
    render(<UserProfile userId="1" fetchUser={async () => mockUser} />);

    // Assert
    await waitFor(() => {
      expect(screen.getByRole('heading', { name: /jane doe/i })).toBeInTheDocument();
    });
  });

  it('shows loading state initially', () => {
    render(<UserProfile userId="1" fetchUser={() => new Promise(() => {})} />);

    expect(screen.getByRole('status', { name: /loading/i })).toBeInTheDocument();
  });

  it('handles error state gracefully', async () => {
    const failingFetch = async () => {
      throw new Error('Network error');
    };

    render(<UserProfile userId="1" fetchUser={failingFetch} />);

    await waitFor(() => {
      expect(screen.getByRole('alert')).toHaveTextContent(/failed to load user/i);
    });
  });
});
```

```typescript
// UserProfile.tsx - Step 2: Write minimal implementation (Green phase)
import { useState, useEffect } from 'react';

interface User {
  id: string;
  name: string;
  email: string;
}

interface UserProfileProps {
  userId: string;
  fetchUser: (id: string) => Promise<User>;
}

export function UserProfile({ userId, fetchUser }: UserProfileProps) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchUser(userId)
      .then(setUser)
      .catch(() => setError('Failed to load user'))
      .finally(() => setLoading(false));
  }, [userId, fetchUser]);

  if (loading) {
    return <div role="status" aria-label="Loading">Loading...</div>;
  }

  if (error) {
    return <div role="alert">{error}</div>;
  }

  return (
    <article>
      <h1>{user?.name}</h1>
      <p>{user?.email}</p>
    </article>
  );
}
```

**Why compliant:** Tests are written before implementation following the Red-Green-Refactor cycle. Each test is atomic, testing one specific behavior. Tests use React Testing Library's user-centric queries (getByRole) and avoid implementation details.

---

## COMPLIANT: Testing User Interactions Atomically

```typescript
// Counter.test.tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Counter } from './Counter';

describe('Counter', () => {
  it('starts at zero', () => {
    render(<Counter />);
    expect(screen.getByRole('spinbutton')).toHaveValue(0);
  });

  it('increments when plus button is clicked', async () => {
    const user = userEvent.setup();
    render(<Counter />);

    await user.click(screen.getByRole('button', { name: /increment/i }));

    expect(screen.getByRole('spinbutton')).toHaveValue(1);
  });

  it('decrements when minus button is clicked', async () => {
    const user = userEvent.setup();
    render(<Counter initialValue={5} />);

    await user.click(screen.getByRole('button', { name: /decrement/i }));

    expect(screen.getByRole('spinbutton')).toHaveValue(4);
  });

  it('does not go below zero', async () => {
    const user = userEvent.setup();
    render(<Counter initialValue={0} />);

    await user.click(screen.getByRole('button', { name: /decrement/i }));

    expect(screen.getByRole('spinbutton')).toHaveValue(0);
  });
});
```

**Why compliant:** Each test focuses on a single atomic behavior. Tests are independent and can run in any order. User interactions are tested through realistic userEvent calls rather than firing synthetic events.

---

## VIOLATION: Testing Implementation Details

```typescript
// BAD: UserProfile.test.tsx
import { render, screen } from '@testing-library/react';
import { UserProfile } from './UserProfile';

describe('UserProfile', () => {
  it('sets loading state and fetches user', () => {
    const { container } = render(<UserProfile userId="1" />);

    // Testing implementation details - internal state
    const component = container.querySelector('.user-profile');
    expect(component?.dataset.loading).toBe('true');
  });

  it('calls useEffect on mount', () => {
    // Spying on React internals
    const useEffectSpy = jest.spyOn(React, 'useEffect');
    render(<UserProfile userId="1" />);

    expect(useEffectSpy).toHaveBeenCalled();
  });

  it('updates internal state correctly', () => {
    const wrapper = shallow(<UserProfile userId="1" />);

    // Directly accessing component state
    expect(wrapper.state('isLoading')).toBe(true);

    wrapper.instance().handleFetchComplete({ name: 'Test' });
    expect(wrapper.state('user')).toEqual({ name: 'Test' });
  });
});
```

**Why violates ENG-4.1:** Tests are coupled to implementation details (CSS classes, React internals, component state). These tests will break when refactoring even if behavior remains correct. Tests should verify what users see and do, not internal component structure.

---

## VIOLATION: Non-Atomic Tests with Multiple Assertions on Different Behaviors

```typescript
// BAD: LoginForm.test.tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { LoginForm } from './LoginForm';

describe('LoginForm', () => {
  it('handles the entire login flow', async () => {
    const user = userEvent.setup();
    const onSubmit = jest.fn();
    render(<LoginForm onSubmit={onSubmit} />);

    // Testing multiple unrelated behaviors in one test

    // Behavior 1: Form renders correctly
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /sign in/i })).toBeInTheDocument();

    // Behavior 2: Validation shows errors
    await user.click(screen.getByRole('button', { name: /sign in/i }));
    expect(screen.getByText(/email is required/i)).toBeInTheDocument();
    expect(screen.getByText(/password is required/i)).toBeInTheDocument();

    // Behavior 3: Input handling
    await user.type(screen.getByLabelText(/email/i), 'test@example.com');
    await user.type(screen.getByLabelText(/password/i), 'password123');
    expect(screen.queryByText(/email is required/i)).not.toBeInTheDocument();

    // Behavior 4: Form submission
    await user.click(screen.getByRole('button', { name: /sign in/i }));
    expect(onSubmit).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'password123'
    });

    // Behavior 5: Loading state
    expect(screen.getByRole('button', { name: /sign in/i })).toBeDisabled();
  });
});
```

**Why violates ENG-4.1:** This test combines 5 different behaviors into one test, making it non-atomic. When it fails, it is unclear which specific behavior broke. Each behavior should be tested in isolation. Tests should follow the "one assertion per behavior" principle.

---

## VIOLATION: Writing Tests After Implementation

```typescript
// BAD: Developer wrote the component first without tests
// ShoppingCart.tsx (written first)
export function ShoppingCart({ items, onCheckout }: ShoppingCartProps) {
  const total = items.reduce((sum, item) => sum + item.price * item.quantity, 0);

  return (
    <div className="cart">
      <ul>
        {items.map(item => (
          <li key={item.id}>{item.name} - ${item.price} x {item.quantity}</li>
        ))}
      </ul>
      <p>Total: ${total}</p>
      <button onClick={onCheckout}>Checkout</button>
    </div>
  );
}

// ShoppingCart.test.tsx (written after, just to increase coverage)
describe('ShoppingCart', () => {
  it('renders', () => {
    const { container } = render(
      <ShoppingCart items={[]} onCheckout={() => {}} />
    );
    expect(container).toBeDefined();
  });

  it('shows items', () => {
    render(
      <ShoppingCart
        items={[{ id: '1', name: 'Thing', price: 10, quantity: 1 }]}
        onCheckout={() => {}}
      />
    );
    expect(screen.getByText(/Thing/)).toBeInTheDocument();
  });
});
```

**Why violates ENG-4.1:** Tests were written after implementation as an afterthought, not driving the design. The tests are superficial, only checking that the component renders rather than verifying meaningful behaviors. TDD requires writing tests first to define expected behavior before implementation.

---

## TDD Cycle Commands

```bash
# RED: Run specific test, see it fail
npm test -- --testNamePattern="displays user name after loading"

# GREEN: Write code, run test again
npm test -- --testNamePattern="displays user name after loading"

# REFACTOR: Run all unit tests
npm test

# VERIFY: Check coverage and constitutional compliance
npm test -- --coverage
constitution-lint .

# Commit when green and compliant
git add -A && git commit -m "Add user profile display component"
```

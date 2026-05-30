---
law_id: ENG-4.1
avatar: mobile-react-native
---

# ENG-4.1: Atomic TDD Examples for React Native

## COMPLIANT: Test-First Development with Jest and React Native Testing Library

```typescript
// UserProfile.test.tsx
import React from 'react';
import { render, screen, waitFor } from '@testing-library/react-native';
import { UserProfile } from './UserProfile';

describe('UserProfile', () => {
  const mockUser = {
    id: '1',
    name: 'Jane Doe',
    email: 'jane@example.com',
    avatarUrl: 'https://example.com/avatar.jpg'
  };

  // Step 1: Write tests FIRST (Red phase)
  it('displays user name after loading', async () => {
    const fetchUser = jest.fn().mockResolvedValue(mockUser);

    render(<UserProfile userId="1" fetchUser={fetchUser} />);

    await waitFor(() => {
      expect(screen.getByText('Jane Doe')).toBeTruthy();
    });
  });

  it('shows loading indicator initially', () => {
    const fetchUser = jest.fn().mockReturnValue(new Promise(() => {}));

    render(<UserProfile userId="1" fetchUser={fetchUser} />);

    expect(screen.getByTestId('loading-indicator')).toBeTruthy();
  });

  it('shows error message on fetch failure', async () => {
    const fetchUser = jest.fn().mockRejectedValue(new Error('Network error'));

    render(<UserProfile userId="1" fetchUser={fetchUser} />);

    await waitFor(() => {
      expect(screen.getByText(/failed to load/i)).toBeTruthy();
    });
  });

  it('displays user avatar when available', async () => {
    const fetchUser = jest.fn().mockResolvedValue(mockUser);

    render(<UserProfile userId="1" fetchUser={fetchUser} />);

    await waitFor(() => {
      const avatar = screen.getByTestId('user-avatar');
      expect(avatar.props.source.uri).toBe(mockUser.avatarUrl);
    });
  });
});
```

```typescript
// UserProfile.tsx - Step 2: Minimal implementation (Green phase)
import React, { useState, useEffect } from 'react';
import { View, Text, Image, ActivityIndicator, StyleSheet } from 'react-native';

interface User {
  id: string;
  name: string;
  email: string;
  avatarUrl?: string;
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
      .catch(() => setError('Failed to load user profile'))
      .finally(() => setLoading(false));
  }, [userId, fetchUser]);

  if (loading) {
    return (
      <View style={styles.container}>
        <ActivityIndicator
          testID="loading-indicator"
          size="large"
          accessibilityLabel="Loading user profile"
        />
      </View>
    );
  }

  if (error) {
    return (
      <View style={styles.container} accessibilityRole="alert">
        <Text style={styles.error}>{error}</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {user?.avatarUrl && (
        <Image
          testID="user-avatar"
          source={{ uri: user.avatarUrl }}
          style={styles.avatar}
          accessibilityLabel={`Avatar for ${user.name}`}
        />
      )}
      <Text style={styles.name} accessibilityRole="header">
        {user?.name}
      </Text>
      <Text style={styles.email}>{user?.email}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { padding: 16, alignItems: 'center' },
  avatar: { width: 100, height: 100, borderRadius: 50 },
  name: { fontSize: 24, fontWeight: 'bold', marginTop: 12 },
  email: { fontSize: 16, color: '#666', marginTop: 4 },
  error: { color: '#d32f2f', fontSize: 16 }
});
```

**Why compliant:** Tests are written before implementation following Red-Green-Refactor. Each test verifies one specific behavior. Uses React Native Testing Library's query methods. Tests avoid implementation details and focus on user-visible behavior.

---

## COMPLIANT: Testing User Interactions with fireEvent

```typescript
// Counter.test.tsx
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react-native';
import { Counter } from './Counter';

describe('Counter', () => {
  it('starts at zero by default', () => {
    render(<Counter />);

    expect(screen.getByText('0')).toBeTruthy();
  });

  it('starts at provided initial value', () => {
    render(<Counter initialValue={5} />);

    expect(screen.getByText('5')).toBeTruthy();
  });

  it('increments when plus button is pressed', () => {
    render(<Counter />);

    fireEvent.press(screen.getByLabelText('Increment'));

    expect(screen.getByText('1')).toBeTruthy();
  });

  it('decrements when minus button is pressed', () => {
    render(<Counter initialValue={5} />);

    fireEvent.press(screen.getByLabelText('Decrement'));

    expect(screen.getByText('4')).toBeTruthy();
  });

  it('does not go below minimum value', () => {
    render(<Counter initialValue={0} min={0} />);

    fireEvent.press(screen.getByLabelText('Decrement'));

    expect(screen.getByText('0')).toBeTruthy();
  });

  it('calls onChange callback when value changes', () => {
    const onChange = jest.fn();
    render(<Counter onChange={onChange} />);

    fireEvent.press(screen.getByLabelText('Increment'));

    expect(onChange).toHaveBeenCalledWith(1);
  });

  it('disables decrement button at minimum', () => {
    render(<Counter initialValue={0} min={0} />);

    const decrementButton = screen.getByLabelText('Decrement');
    expect(decrementButton.props.accessibilityState?.disabled).toBe(true);
  });
});
```

**Why compliant:** Each test focuses on a single atomic behavior. Tests are independent and can run in any order. User interactions are tested through fireEvent.press. Accessibility labels are used to query interactive elements.

---

## COMPLIANT: Testing Navigation with Mocked Navigator

```typescript
// HomeScreen.test.tsx
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react-native';
import { NavigationContainer } from '@react-navigation/native';
import { HomeScreen } from './HomeScreen';

const mockNavigate = jest.fn();

jest.mock('@react-navigation/native', () => ({
  ...jest.requireActual('@react-navigation/native'),
  useNavigation: () => ({
    navigate: mockNavigate
  })
}));

describe('HomeScreen', () => {
  beforeEach(() => {
    mockNavigate.mockClear();
  });

  it('renders welcome message', () => {
    render(
      <NavigationContainer>
        <HomeScreen />
      </NavigationContainer>
    );

    expect(screen.getByText(/welcome/i)).toBeTruthy();
  });

  it('navigates to Profile screen when button is pressed', () => {
    render(
      <NavigationContainer>
        <HomeScreen />
      </NavigationContainer>
    );

    fireEvent.press(screen.getByText('View Profile'));

    expect(mockNavigate).toHaveBeenCalledWith('Profile');
  });

  it('navigates to Settings with correct params', () => {
    render(
      <NavigationContainer>
        <HomeScreen userId="123" />
      </NavigationContainer>
    );

    fireEvent.press(screen.getByText('Settings'));

    expect(mockNavigate).toHaveBeenCalledWith('Settings', { userId: '123' });
  });
});
```

**Why compliant:** Navigation is mocked to isolate component behavior. Each test verifies one navigation action. Tests verify both navigation target and parameters. Clear setup and cleanup between tests.

---

## COMPLIANT: Testing Async Operations with waitFor

```typescript
// ProductList.test.tsx
import React from 'react';
import { render, screen, waitFor, within } from '@testing-library/react-native';
import { ProductList } from './ProductList';

describe('ProductList', () => {
  const mockProducts = [
    { id: '1', name: 'Product A', price: 29.99 },
    { id: '2', name: 'Product B', price: 49.99 }
  ];

  it('shows loading state initially', () => {
    const fetchProducts = jest.fn().mockReturnValue(new Promise(() => {}));

    render(<ProductList fetchProducts={fetchProducts} />);

    expect(screen.getByTestId('loading-spinner')).toBeTruthy();
  });

  it('renders product list after loading', async () => {
    const fetchProducts = jest.fn().mockResolvedValue(mockProducts);

    render(<ProductList fetchProducts={fetchProducts} />);

    await waitFor(() => {
      expect(screen.getByText('Product A')).toBeTruthy();
      expect(screen.getByText('Product B')).toBeTruthy();
    });
  });

  it('shows empty state when no products', async () => {
    const fetchProducts = jest.fn().mockResolvedValue([]);

    render(<ProductList fetchProducts={fetchProducts} />);

    await waitFor(() => {
      expect(screen.getByText(/no products found/i)).toBeTruthy();
    });
  });

  it('displays correct price for each product', async () => {
    const fetchProducts = jest.fn().mockResolvedValue(mockProducts);

    render(<ProductList fetchProducts={fetchProducts} />);

    await waitFor(() => {
      const productA = screen.getByTestId('product-1');
      expect(within(productA).getByText('$29.99')).toBeTruthy();
    });
  });

  it('calls refresh function on pull to refresh', async () => {
    const fetchProducts = jest.fn().mockResolvedValue(mockProducts);

    render(<ProductList fetchProducts={fetchProducts} />);

    await waitFor(() => {
      expect(screen.getByText('Product A')).toBeTruthy();
    });

    // Simulate pull to refresh
    const flatList = screen.getByTestId('product-list');
    flatList.props.onRefresh();

    expect(fetchProducts).toHaveBeenCalledTimes(2);
  });
});
```

**Why compliant:** Uses waitFor for async operations. Each test verifies one specific behavior. Tests cover loading, success, empty, and refresh states. Uses within for scoped queries within list items.

---

## VIOLATION: Testing Implementation Details

```typescript
// BAD: UserProfile.test.tsx
import React from 'react';
import { render } from '@testing-library/react-native';
import { UserProfile } from './UserProfile';

describe('UserProfile', () => {
  it('sets loading state correctly', () => {
    const { UNSAFE_root } = render(<UserProfile userId="1" />);

    // Accessing internal state through UNSAFE methods
    const instance = UNSAFE_root.instance;
    expect(instance.state.loading).toBe(true);
  });

  it('has correct component structure', () => {
    const { UNSAFE_getAllByType } = render(<UserProfile userId="1" />);

    // Testing component tree structure
    const views = UNSAFE_getAllByType('View');
    expect(views.length).toBe(3);

    const texts = UNSAFE_getAllByType('Text');
    expect(texts.length).toBe(2);
  });

  it('calls useEffect on mount', () => {
    const useEffectSpy = jest.spyOn(React, 'useEffect');

    render(<UserProfile userId="1" />);

    expect(useEffectSpy).toHaveBeenCalled();
  });

  it('has correct style properties', () => {
    const { getByTestId } = render(<UserProfile userId="1" />);

    const container = getByTestId('container');
    // Testing implementation detail: specific style values
    expect(container.props.style.padding).toBe(16);
    expect(container.props.style.backgroundColor).toBe('#fff');
  });
});
```

**Why violates ENG-4.1:** Tests use UNSAFE methods to access internal state and component structure. Tests verify React hook calls rather than behavior. Tests check specific style values which are implementation details. These tests will break during refactoring even if behavior is unchanged.

---

## VIOLATION: Non-Atomic Tests with Multiple Assertions

```typescript
// BAD: LoginScreen.test.tsx
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react-native';
import { LoginScreen } from './LoginScreen';

describe('LoginScreen', () => {
  it('handles complete login flow', async () => {
    const onLogin = jest.fn();
    render(<LoginScreen onLogin={onLogin} />);

    // BEHAVIOR 1: Form renders correctly
    expect(screen.getByPlaceholderText('Email')).toBeTruthy();
    expect(screen.getByPlaceholderText('Password')).toBeTruthy();
    expect(screen.getByText('Sign In')).toBeTruthy();

    // BEHAVIOR 2: Validation errors on empty submit
    fireEvent.press(screen.getByText('Sign In'));
    expect(screen.getByText('Email is required')).toBeTruthy();
    expect(screen.getByText('Password is required')).toBeTruthy();

    // BEHAVIOR 3: Invalid email format
    fireEvent.changeText(screen.getByPlaceholderText('Email'), 'invalid');
    fireEvent.press(screen.getByText('Sign In'));
    expect(screen.getByText('Invalid email format')).toBeTruthy();

    // BEHAVIOR 4: Valid input clears errors
    fireEvent.changeText(screen.getByPlaceholderText('Email'), 'test@example.com');
    fireEvent.changeText(screen.getByPlaceholderText('Password'), 'password123');
    expect(screen.queryByText('Email is required')).toBeNull();

    // BEHAVIOR 5: Successful submission
    fireEvent.press(screen.getByText('Sign In'));
    await waitFor(() => {
      expect(onLogin).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'password123'
      });
    });

    // BEHAVIOR 6: Loading state
    expect(screen.getByTestId('loading-indicator')).toBeTruthy();
  });
});
```

**Why violates ENG-4.1:** Test combines 6 different behaviors into one test. When it fails, unclear which specific behavior broke. Each validation scenario, input handling, and submission should be tested separately. Violates "one behavior per test" principle.

---

## VIOLATION: Brittle Tests with Hardcoded Timeouts

```typescript
// BAD: AnimatedComponent.test.tsx
import React from 'react';
import { render, screen } from '@testing-library/react-native';
import { AnimatedComponent } from './AnimatedComponent';

describe('AnimatedComponent', () => {
  it('shows content after animation', async () => {
    render(<AnimatedComponent />);

    // BAD: Using fixed timeout instead of waitFor
    await new Promise(resolve => setTimeout(resolve, 500));

    expect(screen.getByText('Content')).toBeTruthy();
  });

  it('completes fade in animation', async () => {
    render(<AnimatedComponent />);

    // BAD: Checking intermediate animation values
    await new Promise(resolve => setTimeout(resolve, 100));
    expect(screen.getByTestId('container').props.style.opacity).toBeCloseTo(0.3, 1);

    await new Promise(resolve => setTimeout(resolve, 200));
    expect(screen.getByTestId('container').props.style.opacity).toBeCloseTo(0.7, 1);

    await new Promise(resolve => setTimeout(resolve, 200));
    expect(screen.getByTestId('container').props.style.opacity).toBe(1);
  });

  it('handles rapid state changes', async () => {
    const { rerender } = render(<AnimatedComponent visible={true} />);

    // BAD: Race condition prone test
    rerender(<AnimatedComponent visible={false} />);
    await new Promise(resolve => setTimeout(resolve, 50));
    rerender(<AnimatedComponent visible={true} />);
    await new Promise(resolve => setTimeout(resolve, 50));

    expect(screen.getByText('Content')).toBeTruthy();
  });
});
```

**Why violates ENG-4.1:** Uses fixed setTimeout delays which make tests slow and brittle. Tests intermediate animation values which are implementation details. Race conditions make tests flaky. Should use waitFor or jest.useFakeTimers() and test final states rather than animation frames.

---

## TDD Cycle Commands

```bash
# RED: Run specific test, see it fail
npm test -- --testNamePattern="should display user name"

# GREEN: Write code, run test again
npm test -- --testNamePattern="should display user name"

# REFACTOR: Run all unit tests
npm test

# VERIFY: Check coverage and constitutional compliance
npm test -- --coverage
constitution-lint .

# Commit when green and compliant
git add -A && git commit -m "Add user profile screen"
```

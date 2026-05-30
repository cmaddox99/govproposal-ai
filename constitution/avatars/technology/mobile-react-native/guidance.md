# React Native Guidance

> **Purpose:** Stack-specific agent behaviors for React Native cross-platform mobile applications.

---

## Overview

This guidance provides patterns for AI agents working with React Native applications. It covers testing with Jest and React Native Testing Library, component patterns, navigation, and mobile-specific considerations.

---

## Testing Framework

**Primary Framework:** Jest + React Native Testing Library

### Test Structure

```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react-native';
import { OrderSummary } from './OrderSummary';
import { Order } from '../types';

describe('OrderSummary', () => {
  const mockOrder: Order = {
    id: 'order-123',
    items: [{ id: '1', name: 'Widget', price: 100, quantity: 2 }],
    total: 200,
    status: 'draft',
  };

  it('displays the order total', () => {
    // Arrange & Act
    render(<OrderSummary order={mockOrder} />);

    // Assert
    expect(screen.getByText('$200.00')).toBeOnTheScreen();
  });

  it('calls onCheckout when button is pressed', () => {
    // Arrange
    const onCheckout = jest.fn();

    // Act
    render(<OrderSummary order={mockOrder} onCheckout={onCheckout} />);
    fireEvent.press(screen.getByRole('button', { name: /checkout/i }));

    // Assert
    expect(onCheckout).toHaveBeenCalledWith('order-123');
  });

  it('disables checkout button for empty orders', () => {
    // Arrange
    const emptyOrder = { ...mockOrder, items: [], total: 0 };

    // Act
    render(<OrderSummary order={emptyOrder} />);

    // Assert
    expect(screen.getByRole('button', { name: /checkout/i })).toBeDisabled();
  });
});
```

### Testing with Navigation

```typescript
import { NavigationContainer } from '@react-navigation/native';
import { render, screen, fireEvent } from '@testing-library/react-native';
import { OrderListScreen } from './OrderListScreen';

const mockNavigate = jest.fn();

jest.mock('@react-navigation/native', () => ({
  ...jest.requireActual('@react-navigation/native'),
  useNavigation: () => ({ navigate: mockNavigate }),
}));

describe('OrderListScreen', () => {
  it('navigates to order detail when item pressed', async () => {
    // Arrange
    render(
      <NavigationContainer>
        <OrderListScreen />
      </NavigationContainer>
    );

    // Act
    await waitFor(() => {
      fireEvent.press(screen.getByText('Order #123'));
    });

    // Assert
    expect(mockNavigate).toHaveBeenCalledWith('OrderDetail', { orderId: '123' });
  });
});
```

---

## Component Patterns

### Screen Component

```typescript
import { View, FlatList, StyleSheet, RefreshControl } from 'react-native';
import { useOrders } from '../hooks/useOrders';
import { OrderCard } from '../components/OrderCard';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorMessage } from '../components/ErrorMessage';

interface OrderListScreenProps {
  navigation: NavigationProp<RootStackParamList, 'OrderList'>;
}

export function OrderListScreen({ navigation }: OrderListScreenProps) {
  const { orders, isLoading, error, refresh } = useOrders();

  if (isLoading && !orders.length) {
    return <LoadingSpinner />;
  }

  if (error) {
    return <ErrorMessage message={error} onRetry={refresh} />;
  }

  return (
    <FlatList
      data={orders}
      keyExtractor={(item) => item.id}
      renderItem={({ item }) => (
        <OrderCard
          order={item}
          onPress={() => navigation.navigate('OrderDetail', { orderId: item.id })}
        />
      )}
      refreshControl={
        <RefreshControl refreshing={isLoading} onRefresh={refresh} />
      }
      contentContainerStyle={styles.list}
    />
  );
}

const styles = StyleSheet.create({
  list: {
    padding: 16,
  },
});
```

### Presentational Component

```typescript
import { View, Text, Pressable, StyleSheet } from 'react-native';
import { Order } from '../types';
import { formatCurrency } from '../utils/format';

interface OrderCardProps {
  order: Order;
  onPress: () => void;
}

export function OrderCard({ order, onPress }: OrderCardProps) {
  return (
    <Pressable
      onPress={onPress}
      style={({ pressed }) => [
        styles.card,
        pressed && styles.cardPressed,
      ]}
      accessibilityRole="button"
      accessibilityLabel={`Order ${order.id}, total ${formatCurrency(order.total)}`}
    >
      <View style={styles.header}>
        <Text style={styles.orderId}>Order #{order.id}</Text>
        <Text style={styles.status}>{order.status}</Text>
      </View>
      <Text style={styles.total}>{formatCurrency(order.total)}</Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#fff',
    borderRadius: 8,
    padding: 16,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  cardPressed: {
    opacity: 0.7,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 8,
  },
  orderId: {
    fontSize: 16,
    fontWeight: '600',
  },
  status: {
    fontSize: 14,
    color: '#666',
  },
  total: {
    fontSize: 18,
    fontWeight: '700',
  },
});
```

### Custom Hook

```typescript
import { useState, useEffect, useCallback } from 'react';
import { orderService } from '../services/orderService';
import { Order } from '../types';

interface UseOrdersResult {
  orders: Order[];
  isLoading: boolean;
  error: string | null;
  refresh: () => Promise<void>;
}

export function useOrders(): UseOrdersResult {
  const [orders, setOrders] = useState<Order[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchOrders = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await orderService.getOrders();
      setOrders(data);
    } catch (err) {
      setError('Failed to load orders');
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchOrders();
  }, [fetchOrders]);

  return { orders, isLoading, error, refresh: fetchOrders };
}
```

---

## Common Patterns

### Navigation Setup

```typescript
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { OrderListScreen } from './screens/OrderListScreen';
import { OrderDetailScreen } from './screens/OrderDetailScreen';

export type RootStackParamList = {
  OrderList: undefined;
  OrderDetail: { orderId: string };
  Checkout: { orderId: string };
};

const Stack = createNativeStackNavigator<RootStackParamList>();

export function RootNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="OrderList">
        <Stack.Screen
          name="OrderList"
          component={OrderListScreen}
          options={{ title: 'Orders' }}
        />
        <Stack.Screen
          name="OrderDetail"
          component={OrderDetailScreen}
          options={{ title: 'Order Details' }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

### API Service

```typescript
const API_BASE = 'https://api.example.com/v1';

async function request<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  });

  if (!response.ok) {
    throw new ApiError(response.status, await response.text());
  }

  return response.json();
}

export const orderService = {
  getOrders: () => request<Order[]>('/orders'),
  getOrder: (id: string) => request<Order>(`/orders/${id}`),
  createOrder: (data: CreateOrderRequest) =>
    request<Order>('/orders', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
};
```

### Context for Global State

```typescript
import { createContext, useContext, useState, ReactNode } from 'react';

interface AuthContextValue {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);

  const login = async (email: string, password: string) => {
    const user = await authService.login(email, password);
    setUser(user);
  };

  const logout = async () => {
    await authService.logout();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
```

---

## Anti-Patterns to Avoid

### Inline Styles for Reusable Values

```typescript
// BAD - Repeated magic numbers
<View style={{ padding: 16, margin: 8 }}>
<View style={{ padding: 16, margin: 8 }}>

// GOOD - Centralized theme
const theme = {
  spacing: { sm: 8, md: 16, lg: 24 },
  colors: { primary: '#007AFF', text: '#333' },
};

<View style={{ padding: theme.spacing.md }}>
```

### Fetching in Components

```typescript
// BAD - Business logic in component
function OrderScreen() {
  const [order, setOrder] = useState(null);

  useEffect(() => {
    fetch('/api/orders/123')
      .then(res => res.json())
      .then(data => setOrder(data));
  }, []);

  // ...
}

// GOOD - Extracted to hook
function OrderScreen({ orderId }) {
  const { order, isLoading, error } = useOrder(orderId);
  // ...
}
```

### Platform-Specific Code Scattered

```typescript
// BAD - Platform checks everywhere
<View style={{ padding: Platform.OS === 'ios' ? 20 : 16 }}>

// GOOD - Platform-specific files or centralized
// Button.ios.tsx / Button.android.tsx
// OR
const platformStyles = StyleSheet.create({
  container: {
    ...Platform.select({
      ios: { padding: 20 },
      android: { padding: 16 },
    }),
  },
});
```

---

## React Native Specific Guidance

### Accessibility

```typescript
<Pressable
  onPress={onPress}
  accessibilityRole="button"
  accessibilityLabel="Add item to cart"
  accessibilityHint="Double tap to add this item to your shopping cart"
>
  <Text>Add to Cart</Text>
</Pressable>

<TextInput
  accessibilityLabel="Email address"
  keyboardType="email-address"
  autoComplete="email"
  textContentType="emailAddress"
/>
```

### Performance

```typescript
// Memoize expensive components
const MemoizedOrderCard = memo(OrderCard);

// Use useCallback for event handlers passed to children
const handlePress = useCallback(() => {
  navigation.navigate('OrderDetail', { orderId });
}, [navigation, orderId]);

// FlatList optimizations
<FlatList
  data={orders}
  keyExtractor={(item) => item.id}
  renderItem={renderItem}
  initialNumToRender={10}
  maxToRenderPerBatch={10}
  windowSize={5}
  removeClippedSubviews={true}
/>
```

### Safe Area Handling

```typescript
import { SafeAreaProvider, useSafeAreaInsets } from 'react-native-safe-area-context';

function App() {
  return (
    <SafeAreaProvider>
      <RootNavigator />
    </SafeAreaProvider>
  );
}

function OrderListScreen() {
  const insets = useSafeAreaInsets();

  return (
    <View style={{ paddingTop: insets.top, paddingBottom: insets.bottom }}>
      {/* Content */}
    </View>
  );
}
```

### Error Boundaries

```typescript
import { ErrorBoundary } from 'react-error-boundary';

function ErrorFallback({ error, resetErrorBoundary }) {
  return (
    <View style={styles.error}>
      <Text>Something went wrong</Text>
      <Button title="Try again" onPress={resetErrorBoundary} />
    </View>
  );
}

function App() {
  return (
    <ErrorBoundary FallbackComponent={ErrorFallback}>
      <RootNavigator />
    </ErrorBoundary>
  );
}
```

---

## Tools and Commands

### Development

```bash
# Start Metro bundler
npm start

# Run on iOS
npm run ios

# Run on Android
npm run android

# Clear Metro cache
npm start -- --reset-cache

# Install pods (iOS)
cd ios && pod install && cd ..
```

### Testing

```bash
# Run tests
npm test

# Watch mode
npm test -- --watch

# Coverage
npm test -- --coverage

# Update snapshots
npm test -- -u
```

### Code Quality

```bash
# ESLint
npm run lint

# TypeScript check
npm run typecheck

# Format
npm run format
```

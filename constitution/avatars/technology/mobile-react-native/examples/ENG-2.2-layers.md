---
law_id: ENG-2.2
avatar: mobile-react-native
---

# ENG-2.2: Layered Architecture Examples for React Native

## COMPLIANT: Screen-Hook-Service Layer Separation

```typescript
// === PRESENTATION LAYER: Screens handle UI rendering only ===

// screens/OrderListScreen.tsx
import React from 'react';
import { View, FlatList, Text, StyleSheet, ActivityIndicator } from 'react-native';
import { useOrders } from '../hooks/useOrders';
import { OrderCard } from '../components/OrderCard';

export function OrderListScreen() {
  const { orders, isLoading, error, submitOrder, refresh } = useOrders();

  if (isLoading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator
          testID="loading-indicator"
          size="large"
          accessibilityLabel="Loading orders"
        />
      </View>
    );
  }

  if (error) {
    return (
      <View style={styles.center} accessibilityRole="alert">
        <Text style={styles.error}>{error}</Text>
      </View>
    );
  }

  return (
    <FlatList
      testID="order-list"
      data={orders}
      keyExtractor={(item) => item.id}
      renderItem={({ item }) => (
        <OrderCard order={item} onSubmit={() => submitOrder(item.id)} />
      )}
      onRefresh={refresh}
      refreshing={isLoading}
      ListEmptyComponent={<Text style={styles.empty}>No orders found</Text>}
    />
  );
}

const styles = StyleSheet.create({
  center: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  error: { color: '#d32f2f', fontSize: 16 },
  empty: { textAlign: 'center', padding: 24, color: '#666' },
});


// === APPLICATION LAYER: Hooks orchestrate use cases ===

// hooks/useOrders.ts
import { useState, useEffect, useCallback } from 'react';
import { Order } from '../domain/models/Order';
import { orderService } from '../services/orderService';

export function useOrders() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadOrders = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await orderService.fetchOrders();
      setOrders(data);
    } catch {
      setError('Failed to load orders');
    } finally {
      setIsLoading(false);
    }
  }, []);

  const submitOrder = useCallback(async (orderId: string) => {
    try {
      const order = orders.find(o => o.id === orderId);
      if (!order) return;

      const submitted = order.submit();
      await orderService.updateOrder(submitted);
      await loadOrders();
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to submit order');
    }
  }, [orders, loadOrders]);

  useEffect(() => {
    loadOrders();
  }, [loadOrders]);

  return { orders, isLoading, error, submitOrder, refresh: loadOrders };
}


// === DOMAIN LAYER: Models contain business logic, no dependencies ===

// domain/models/Order.ts
export type OrderStatus = 'draft' | 'submitted' | 'confirmed';

export interface LineItem {
  readonly productId: string;
  readonly quantity: number;
  readonly unitPrice: number;
}

export class Order {
  constructor(
    readonly id: string,
    readonly customerId: string,
    readonly items: readonly LineItem[],
    readonly status: OrderStatus,
    readonly createdAt: Date
  ) {}

  submit(): Order {
    if (this.status !== 'draft') {
      throw new Error('Only draft orders can be submitted');
    }
    if (this.items.length === 0) {
      throw new Error('Cannot submit an empty order');
    }
    return new Order(this.id, this.customerId, this.items, 'submitted', this.createdAt);
  }

  get total(): number {
    return this.items.reduce(
      (sum, item) => sum + item.quantity * item.unitPrice,
      0
    );
  }
}


// === INFRASTRUCTURE LAYER: Services handle external communication ===

// services/orderService.ts
import { Order, LineItem } from '../domain/models/Order';

interface OrderDto {
  id: string;
  customerId: string;
  items: Array<{ productId: string; quantity: number; unitPrice: number }>;
  status: string;
  createdAt: string;
}

const API_BASE = 'https://api.example.com';

function toDomain(dto: OrderDto): Order {
  return new Order(
    dto.id,
    dto.customerId,
    dto.items,
    dto.status as Order['status'],
    new Date(dto.createdAt)
  );
}

function toDto(order: Order): OrderDto {
  return {
    id: order.id,
    customerId: order.customerId,
    items: [...order.items],
    status: order.status,
    createdAt: order.createdAt.toISOString(),
  };
}

export const orderService = {
  async fetchOrders(): Promise<Order[]> {
    const response = await fetch(`${API_BASE}/orders`);
    if (!response.ok) throw new Error('Failed to fetch orders');
    const data: OrderDto[] = await response.json();
    return data.map(toDomain);
  },

  async updateOrder(order: Order): Promise<void> {
    const response = await fetch(`${API_BASE}/orders/${order.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(toDto(order)),
    });
    if (!response.ok) throw new Error('Failed to update order');
  },
};
```

**Why compliant:**
- Screen (presentation) only renders UI and delegates actions to hooks
- Hook (application) orchestrates the use case: loading, submitting, error handling
- Domain model contains business rules (status transitions, validation) with no imports
- Service (infrastructure) handles HTTP communication and DTO mapping
- Dependencies point inward: Service -> Domain, Hook -> Domain + Service, Screen -> Hook

---

## VIOLATION: API Calls Directly in Screen Components

```typescript
// BAD: Screen doing everything - API calls, business logic, state management
import React, { useState, useEffect } from 'react';
import { View, FlatList, Text, Button, Alert, StyleSheet } from 'react-native';

export function OrderListScreen() {
  const [orders, setOrders] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Direct API call in screen component!
    fetch('https://api.example.com/orders')
      .then(res => res.json())
      .then(data => {
        setOrders(data);
        setLoading(false);
      })
      .catch(() => {
        Alert.alert('Error', 'Failed to load');
        setLoading(false);
      });
  }, []);

  const submitOrder = async (order: any) => {
    // Business logic in screen!
    if (order.status !== 'draft') {
      Alert.alert('Error', 'Cannot submit non-draft order');
      return;
    }
    if (!order.items || order.items.length === 0) {
      Alert.alert('Error', 'Cannot submit empty order');
      return;
    }

    // Calculate total in screen component!
    let total = 0;
    for (const item of order.items) {
      if (item.quantity > 10) {
        total += item.unitPrice * item.quantity * 0.9;  // Discount logic!
      } else {
        total += item.unitPrice * item.quantity;
      }
    }

    // Direct API call in screen!
    try {
      const response = await fetch(`https://api.example.com/orders/${order.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...order, status: 'submitted', total }),
      });

      if (!response.ok) throw new Error('Failed');

      // Direct API call for analytics in screen!
      await fetch('https://api.example.com/analytics', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          event: 'order_submitted',
          orderId: order.id,
          total,
        }),
      });

      // Mutating state directly
      const updated = orders.map(o =>
        o.id === order.id ? { ...o, status: 'submitted', total } : o
      );
      setOrders(updated);

      Alert.alert('Success', `Order submitted! Total: $${total.toFixed(2)}`);
    } catch {
      Alert.alert('Error', 'Submission failed');
    }
  };

  return (
    <FlatList
      data={orders}
      keyExtractor={(item) => item.id}
      renderItem={({ item }) => (
        <View style={styles.card}>
          <Text>Order {item.id}</Text>
          <Text>Status: {item.status}</Text>
          <Button title="Submit" onPress={() => submitOrder(item)} />
        </View>
      )}
    />
  );
}

const styles = StyleSheet.create({
  card: { padding: 16, borderBottomWidth: 1, borderColor: '#eee' },
});
```

**Why violates ENG-2.2:**
- Screen component makes direct `fetch()` calls to the API
- Business rules (status validation, discount calculation) are in the UI layer
- Analytics tracking is coupled to the submission flow in the screen
- No domain model; data is untyped `any` objects
- Cannot test business logic without rendering the component
- Cannot reuse order submission logic in a different screen

---

## Layer Responsibilities

| Layer | Responsibility | React Native Artifacts |
|-------|----------------|------------------------|
| **Presentation (Screens)** | UI rendering, user interaction | Screen components, UI components |
| **Application (Hooks)** | Use case orchestration, state | Custom hooks (`useOrders`, `useAuth`) |
| **Domain (Models)** | Business rules, validation | Classes, interfaces, pure functions |
| **Infrastructure (Services)** | API, storage, notifications | Service modules, AsyncStorage adapters |

---

## Dependency Injection via Props and Modules

```typescript
// Hook depends on domain and service (injected via module import)
import { Order } from '../domain/models/Order';
import { orderService } from '../services/orderService';

// For testing, inject service as parameter
export function useOrders(service = orderService) {
  // ... hook logic using injected service
}

// Screen depends only on hook (clean separation)
export function OrderListScreen() {
  const { orders, submitOrder } = useOrders();
  // ... render only
}
```

**Key principle:** Screens depend on hooks, hooks depend on domain models and services, services implement infrastructure concerns. Each layer can be tested independently.

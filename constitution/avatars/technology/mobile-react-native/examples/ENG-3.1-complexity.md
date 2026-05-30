---
law_id: ENG-3.1
avatar: mobile-react-native
---

# ENG-3.1: Complexity Limits Examples for React Native

## COMPLIANT: Small Focused Components Under Complexity Limits

```typescript
// OrderStatusBadge.tsx - Single purpose, minimal branching
// Cyclomatic complexity: 1
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

type OrderStatus = 'draft' | 'submitted' | 'confirmed' | 'shipped' | 'delivered';

interface OrderStatusBadgeProps {
  status: OrderStatus;
}

const STATUS_CONFIG: Record<OrderStatus, { label: string; color: string }> = {
  draft: { label: 'Draft', color: '#9E9E9E' },
  submitted: { label: 'Submitted', color: '#2196F3' },
  confirmed: { label: 'Confirmed', color: '#FF9800' },
  shipped: { label: 'Shipped', color: '#9C27B0' },
  delivered: { label: 'Delivered', color: '#4CAF50' },
};

export function OrderStatusBadge({ status }: OrderStatusBadgeProps) {
  const config = STATUS_CONFIG[status];

  return (
    <View style={[styles.badge, { backgroundColor: config.color }]}>
      <Text style={styles.label}>{config.label}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  badge: { paddingHorizontal: 12, paddingVertical: 4, borderRadius: 12 },
  label: { color: '#fff', fontSize: 12, fontWeight: '600' },
});
```

**Why compliant:** Component has a single responsibility with no conditional branching. Status-to-display mapping uses a lookup table instead of if/else chains. Cyclomatic complexity is 1.

---

## COMPLIANT: Extracting Complex Logic into Custom Hooks

```typescript
// hooks/useOrderPricing.ts - Business logic extracted from component
// Each function has low cyclomatic complexity
import { useMemo } from 'react';

interface LineItem {
  productId: string;
  quantity: number;
  unitPrice: number;
}

interface PricingResult {
  subtotal: number;
  discount: number;
  tax: number;
  total: number;
  formattedTotal: string;
}

const TAX_RATE = 0.08;

const VOLUME_DISCOUNTS: Array<{ minQuantity: number; rate: number }> = [
  { minQuantity: 50, rate: 0.15 },
  { minQuantity: 20, rate: 0.10 },
  { minQuantity: 10, rate: 0.05 },
];

function calculateSubtotal(items: readonly LineItem[]): number {
  return items.reduce((sum, item) => sum + item.quantity * item.unitPrice, 0);
}

function calculateDiscount(items: readonly LineItem[]): number {
  return items.reduce((total, item) => {
    const tier = VOLUME_DISCOUNTS.find(d => item.quantity >= d.minQuantity);
    const rate = tier?.rate ?? 0;
    return total + item.quantity * item.unitPrice * rate;
  }, 0);
}

function calculateTax(amount: number): number {
  return Math.round(amount * TAX_RATE * 100) / 100;
}

export function useOrderPricing(items: readonly LineItem[]): PricingResult {
  return useMemo(() => {
    const subtotal = calculateSubtotal(items);
    const discount = calculateDiscount(items);
    const taxableAmount = subtotal - discount;
    const tax = calculateTax(taxableAmount);
    const total = taxableAmount + tax;

    return {
      subtotal,
      discount,
      tax,
      total,
      formattedTotal: `$${total.toFixed(2)}`,
    };
  }, [items]);
}
```

```typescript
// components/OrderSummary.tsx - Component stays simple by delegating logic
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { useOrderPricing } from '../hooks/useOrderPricing';

interface OrderSummaryProps {
  items: readonly LineItem[];
}

export function OrderSummary({ items }: OrderSummaryProps) {
  const pricing = useOrderPricing(items);

  return (
    <View style={styles.container}>
      <PricingRow label="Subtotal" amount={pricing.subtotal} />
      {pricing.discount > 0 && (
        <PricingRow label="Discount" amount={-pricing.discount} />
      )}
      <PricingRow label="Tax" amount={pricing.tax} />
      <PricingRow label="Total" amount={pricing.total} bold />
    </View>
  );
}

function PricingRow({ label, amount, bold }: {
  label: string;
  amount: number;
  bold?: boolean;
}) {
  return (
    <View style={styles.row}>
      <Text style={bold ? styles.boldText : styles.text}>{label}</Text>
      <Text style={bold ? styles.boldText : styles.text}>
        ${amount.toFixed(2)}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { padding: 16 },
  row: { flexDirection: 'row', justifyContent: 'space-between', paddingVertical: 4 },
  text: { fontSize: 14, color: '#333' },
  boldText: { fontSize: 16, fontWeight: 'bold', color: '#000' },
});
```

**Why compliant:** Complex pricing logic is extracted into a custom hook with small focused functions. The component only handles rendering. Each function has cyclomatic complexity under 5. Volume discount tiers use a configuration array rather than nested conditionals.

---

## COMPLIANT: Using Composition to Reduce Component Complexity

```typescript
// screens/OrderDetailScreen.tsx - Composed of small components
import React from 'react';
import { ScrollView, StyleSheet } from 'react-native';
import { useOrder } from '../hooks/useOrder';
import { OrderHeader } from '../components/OrderHeader';
import { OrderItemList } from '../components/OrderItemList';
import { OrderSummary } from '../components/OrderSummary';
import { OrderActions } from '../components/OrderActions';
import { LoadingScreen } from '../components/LoadingScreen';
import { ErrorScreen } from '../components/ErrorScreen';

interface OrderDetailScreenProps {
  orderId: string;
}

export function OrderDetailScreen({ orderId }: OrderDetailScreenProps) {
  const { order, isLoading, error, submitOrder } = useOrder(orderId);

  if (isLoading) return <LoadingScreen />;
  if (error) return <ErrorScreen message={error} />;
  if (!order) return <ErrorScreen message="Order not found" />;

  return (
    <ScrollView style={styles.container}>
      <OrderHeader order={order} />
      <OrderItemList items={order.items} />
      <OrderSummary items={order.items} />
      <OrderActions order={order} onSubmit={submitOrder} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff' },
});
```

**Why compliant:** Screen component delegates to child components and hooks. Each child component is independently testable. Guard clauses handle loading/error states with early returns. Cyclomatic complexity of the screen is 4 (three guards plus the happy path).

---

## VIOLATION: Large Component with Too Many Conditionals

```typescript
// BAD: OrderDetailScreen.tsx - Monolithic component with high complexity
import React, { useState, useEffect } from 'react';
import {
  View, Text, FlatList, Button, Alert, StyleSheet,
  ActivityIndicator, TextInput, Modal, TouchableOpacity
} from 'react-native';

// Cyclomatic complexity: 25+
export function OrderDetailScreen({ orderId, userId, userRole }: any) {
  const [order, setOrder] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [editingItem, setEditingItem] = useState<any>(null);
  const [showModal, setShowModal] = useState(false);
  const [quantity, setQuantity] = useState('');
  const [discount, setDiscount] = useState('');

  useEffect(() => {
    fetch(`https://api.example.com/orders/${orderId}`)
      .then(res => res.json())
      .then(data => { setOrder(data); setLoading(false); })
      .catch(() => { Alert.alert('Error'); setLoading(false); });
  }, [orderId]);

  if (loading) return <ActivityIndicator />;

  // Deeply nested conditionals for total calculation
  const calculateTotal = () => {
    let total = 0;
    if (order && order.items) {
      for (const item of order.items) {
        if (item.quantity > 0) {
          if (item.onSale) {
            if (item.saleType === 'percentage') {
              if (item.salePercentage > 50) {
                total += item.unitPrice * item.quantity * 0.5;
              } else {
                total += item.unitPrice * item.quantity * (1 - item.salePercentage / 100);
              }
            } else if (item.saleType === 'fixed') {
              if (item.saleAmount > item.unitPrice) {
                total += 0;
              } else {
                total += (item.unitPrice - item.saleAmount) * item.quantity;
              }
            } else {
              total += item.unitPrice * item.quantity;
            }
          } else {
            if (item.category === 'electronics') {
              if (item.quantity > 5) {
                total += item.unitPrice * item.quantity * 0.95;
              } else {
                total += item.unitPrice * item.quantity;
              }
            } else if (item.category === 'clothing') {
              if (order.season === 'clearance') {
                total += item.unitPrice * item.quantity * 0.7;
              } else {
                total += item.unitPrice * item.quantity;
              }
            } else {
              total += item.unitPrice * item.quantity;
            }
          }
        }
      }
    }

    // More nested conditionals for user-specific discounts
    if (userRole === 'employee') {
      if (total > 100) {
        total *= 0.8;
      } else {
        total *= 0.9;
      }
    } else if (userRole === 'vip') {
      if (order.isFirstOrder) {
        total *= 0.75;
      } else {
        total *= 0.85;
      }
    }

    return total;
  };

  const handleSubmit = () => {
    if (!order) return;
    if (order.items.length === 0) {
      Alert.alert('Error', 'Empty order');
      return;
    }
    if (order.status !== 'draft') {
      Alert.alert('Error', 'Not a draft');
      return;
    }
    if (userRole !== 'admin' && userRole !== 'manager') {
      if (calculateTotal() > 10000) {
        Alert.alert('Error', 'Need approval for orders over $10,000');
        return;
      }
    }

    // Submit logic...
    fetch(`https://api.example.com/orders/${orderId}/submit`, { method: 'POST' })
      .then(() => Alert.alert('Success'))
      .catch(() => Alert.alert('Error'));
  };

  const handleEditItem = (item: any) => {
    if (order.status !== 'draft') {
      Alert.alert('Error', 'Cannot edit submitted order');
      return;
    }
    if (userRole === 'viewer') {
      Alert.alert('Error', 'No permission');
      return;
    }
    setEditingItem(item);
    setQuantity(item.quantity.toString());
    setShowModal(true);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Order {orderId}</Text>

      {/* Complex conditional rendering */}
      {order.status === 'draft' ? (
        <Text style={{ color: 'gray' }}>Draft</Text>
      ) : order.status === 'submitted' ? (
        <Text style={{ color: 'blue' }}>Submitted</Text>
      ) : order.status === 'confirmed' ? (
        <Text style={{ color: 'green' }}>Confirmed</Text>
      ) : order.status === 'cancelled' ? (
        <Text style={{ color: 'red' }}>Cancelled</Text>
      ) : (
        <Text>Unknown</Text>
      )}

      <Text>Total: ${calculateTotal().toFixed(2)}</Text>

      <FlatList
        data={order.items}
        keyExtractor={(item: any) => item.id}
        renderItem={({ item }) => (
          <TouchableOpacity onPress={() => handleEditItem(item)}>
            <Text>{item.name} x{item.quantity}</Text>
          </TouchableOpacity>
        )}
      />

      {order.status === 'draft' && userRole !== 'viewer' && (
        <Button title="Submit Order" onPress={handleSubmit} />
      )}

      {/* Inline modal */}
      <Modal visible={showModal} animationType="slide">
        <View style={styles.modal}>
          <TextInput
            value={quantity}
            onChangeText={setQuantity}
            keyboardType="numeric"
            placeholder="Quantity"
          />
          {userRole === 'admin' && (
            <TextInput
              value={discount}
              onChangeText={setDiscount}
              keyboardType="numeric"
              placeholder="Discount %"
            />
          )}
          <Button title="Save" onPress={() => {
            // More inline logic...
            const qty = parseInt(quantity);
            if (isNaN(qty) || qty <= 0) {
              Alert.alert('Error', 'Invalid quantity');
              return;
            }
            // Update item...
            setShowModal(false);
          }} />
          <Button title="Cancel" onPress={() => setShowModal(false)} />
        </View>
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16 },
  title: { fontSize: 24, fontWeight: 'bold' },
  modal: { flex: 1, padding: 24, justifyContent: 'center' },
});
```

**Why violates ENG-3.1:**
- `calculateTotal` has cyclomatic complexity over 15 with deeply nested conditionals
- Component handles data fetching, business logic, UI rendering, and modals all in one place
- Role-based logic is scattered throughout with nested if/else chains
- Status display uses chained ternaries instead of a lookup table
- Inline modal with its own validation creates additional branching
- Should be decomposed into: `useOrderPricing` hook, `OrderStatusBadge` component, `EditItemModal` component, and a pricing strategy module

---

## How to Fix

1. **Extract pricing logic** into a custom hook or pure function module with lookup tables
2. **Break status display** into an `OrderStatusBadge` component using a config map
3. **Extract the modal** into a separate `EditItemModal` component
4. **Move API calls** into a service layer and orchestrate via a custom hook
5. **Use composition** to assemble the screen from small, focused components

```typescript
// Fixed: Small focused hook for pricing
function calculateItemPrice(item: LineItem, saleConfig: SaleConfig): number {
  if (!item.onSale) return item.unitPrice * item.quantity;

  const discount = SALE_STRATEGIES[saleConfig.saleType]?.(item) ?? 0;
  return Math.max(0, (item.unitPrice - discount) * item.quantity);
}

const SALE_STRATEGIES: Record<string, (item: LineItem) => number> = {
  percentage: (item) => item.unitPrice * Math.min(item.salePercentage / 100, 0.5),
  fixed: (item) => Math.min(item.saleAmount, item.unitPrice),
};
```

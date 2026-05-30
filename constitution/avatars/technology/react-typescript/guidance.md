# React/TypeScript Guidance

> **Purpose:** Stack-specific agent behaviors for React/TypeScript applications.

---

## Overview

This guidance provides patterns for AI agents working with React and TypeScript applications. It covers testing with Jest and React Testing Library, component patterns, and state management.

---

## Testing Framework

**Primary Framework:** Jest + React Testing Library + user-event

### Test Structure

```typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { OrderCard } from './OrderCard';

describe('OrderCard', () => {
  const mockOrder = {
    id: 'order-123',
    customerName: 'John Doe',
    total: 150.00,
    status: 'pending',
  };

  it('renders order details correctly', () => {
    // Arrange & Act
    render(<OrderCard order={mockOrder} />);

    // Assert
    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('$150.00')).toBeInTheDocument();
    expect(screen.getByText('pending')).toBeInTheDocument();
  });

  it('calls onSelect when clicked', async () => {
    // Arrange
    const handleSelect = jest.fn();
    const user = userEvent.setup();
    render(<OrderCard order={mockOrder} onSelect={handleSelect} />);

    // Act
    await user.click(screen.getByRole('article'));

    // Assert
    expect(handleSelect).toHaveBeenCalledWith('order-123');
  });

  it('displays loading state', () => {
    // Arrange & Act
    render(<OrderCard order={mockOrder} isLoading />);

    // Assert
    expect(screen.getByRole('progressbar')).toBeInTheDocument();
  });
});
```

### Testing Patterns

- Use `screen` queries over destructured render results
- Prefer `getByRole` for accessibility-friendly queries
- Use `userEvent` over `fireEvent` for realistic interactions
- Test behavior, not implementation details
- Mock API calls with MSW (Mock Service Worker)

---

## Component Patterns

### Functional Component with Props

```typescript
interface OrderCardProps {
  order: Order;
  onSelect?: (orderId: string) => void;
  isLoading?: boolean;
  className?: string;
}

export const OrderCard: React.FC<OrderCardProps> = ({
  order,
  onSelect,
  isLoading = false,
  className,
}) => {
  const handleClick = useCallback(() => {
    onSelect?.(order.id);
  }, [onSelect, order.id]);

  if (isLoading) {
    return <OrderCardSkeleton className={className} />;
  }

  return (
    <article
      className={cn('order-card', className)}
      onClick={handleClick}
      role="article"
      aria-label={`Order for ${order.customerName}`}
    >
      <h3>{order.customerName}</h3>
      <p className="total">{formatCurrency(order.total)}</p>
      <OrderStatusBadge status={order.status} />
    </article>
  );
};

OrderCard.displayName = 'OrderCard';
```

### Custom Hook Pattern

```typescript
interface UseOrdersOptions {
  status?: OrderStatus;
  page?: number;
  pageSize?: number;
}

interface UseOrdersResult {
  orders: Order[];
  isLoading: boolean;
  error: Error | null;
  refetch: () => void;
  hasNextPage: boolean;
  fetchNextPage: () => void;
}

export function useOrders(options: UseOrdersOptions = {}): UseOrdersResult {
  const { status, page = 1, pageSize = 20 } = options;

  const queryKey = ['orders', { status, page, pageSize }];

  const { data, isLoading, error, refetch } = useQuery({
    queryKey,
    queryFn: () => orderApi.getOrders({ status, page, pageSize }),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });

  return {
    orders: data?.orders ?? [],
    isLoading,
    error,
    refetch,
    hasNextPage: data?.hasNextPage ?? false,
    fetchNextPage: () => {/* implementation */},
  };
}
```

---

## State Management

### Zustand Store Pattern

```typescript
interface OrderStore {
  orders: Order[];
  selectedOrderId: string | null;
  isLoading: boolean;

  // Actions
  setOrders: (orders: Order[]) => void;
  selectOrder: (orderId: string | null) => void;
  addOrder: (order: Order) => void;
  updateOrder: (orderId: string, updates: Partial<Order>) => void;
}

export const useOrderStore = create<OrderStore>((set) => ({
  orders: [],
  selectedOrderId: null,
  isLoading: false,

  setOrders: (orders) => set({ orders }),

  selectOrder: (orderId) => set({ selectedOrderId: orderId }),

  addOrder: (order) =>
    set((state) => ({ orders: [...state.orders, order] })),

  updateOrder: (orderId, updates) =>
    set((state) => ({
      orders: state.orders.map((o) =>
        o.id === orderId ? { ...o, ...updates } : o
      ),
    })),
}));
```

---

## Common Patterns

### Error Boundary

```typescript
interface ErrorBoundaryProps {
  fallback: React.ReactNode;
  children: React.ReactNode;
}

export class ErrorBoundary extends React.Component<
  ErrorBoundaryProps,
  { hasError: boolean }
> {
  state = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback;
    }
    return this.props.children;
  }
}
```

### Accessible Form Pattern

```typescript
export const OrderForm: React.FC<OrderFormProps> = ({ onSubmit }) => {
  const [errors, setErrors] = useState<FormErrors>({});

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const formData = new FormData(e.target as HTMLFormElement);
    const result = validateOrderForm(formData);

    if (!result.success) {
      setErrors(result.errors);
      return;
    }

    await onSubmit(result.data);
  };

  return (
    <form onSubmit={handleSubmit} aria-label="Create order">
      <div>
        <label htmlFor="customerName">Customer Name</label>
        <input
          id="customerName"
          name="customerName"
          aria-describedby={errors.customerName ? 'customerName-error' : undefined}
          aria-invalid={!!errors.customerName}
        />
        {errors.customerName && (
          <span id="customerName-error" role="alert">
            {errors.customerName}
          </span>
        )}
      </div>
      <button type="submit">Create Order</button>
    </form>
  );
};
```

---

## Anti-Patterns to Avoid

### Direct DOM Manipulation

```typescript
// BAD - Direct DOM manipulation
const Component = () => {
  useEffect(() => {
    document.getElementById('my-div')!.style.color = 'red';
  }, []);
  return <div id="my-div">Text</div>;
};

// GOOD - React state
const Component = () => {
  const [isHighlighted, setIsHighlighted] = useState(false);
  return (
    <div className={isHighlighted ? 'text-red' : ''}>Text</div>
  );
};
```

### Missing Dependency Arrays

```typescript
// BAD - Missing dependency
const Component = ({ userId }) => {
  useEffect(() => {
    fetchUser(userId);
  }, []); // userId missing from deps
};

// GOOD - Complete dependency array
const Component = ({ userId }) => {
  useEffect(() => {
    fetchUser(userId);
  }, [userId]);
};
```

---

## Tools and Commands

### Development

```bash
# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Testing

```bash
# Run all tests
npm test

# Watch mode
npm test -- --watch

# Coverage
npm test -- --coverage

# Single file
npm test -- OrderCard.test.tsx
```

### Code Quality

```bash
# Lint
npm run lint

# Type check
npx tsc --noEmit

# Format
npm run format
```

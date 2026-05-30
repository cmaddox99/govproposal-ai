---
law_id: ENG-3.1
avatar: react-typescript
---

# ENG-3.1: Complexity Examples for React + TypeScript

## COMPLIANT: Single Responsibility Component with Low Cyclomatic Complexity

```typescript
// UserAvatar.tsx - Single purpose, minimal branching
interface UserAvatarProps {
  user: {
    name: string;
    avatarUrl?: string;
  };
  size?: 'small' | 'medium' | 'large';
}

const sizeMap = {
  small: 32,
  medium: 48,
  large: 64,
} as const;

export function UserAvatar({ user, size = 'medium' }: UserAvatarProps) {
  const dimension = sizeMap[size];
  const initials = user.name
    .split(' ')
    .map(word => word[0])
    .join('')
    .slice(0, 2)
    .toUpperCase();

  return (
    <div
      className="avatar"
      style={{ width: dimension, height: dimension }}
      role="img"
      aria-label={`Avatar for ${user.name}`}
    >
      {user.avatarUrl ? (
        <img src={user.avatarUrl} alt="" />
      ) : (
        <span className="initials">{initials}</span>
      )}
    </div>
  );
}
```

**Why compliant:** Component has a single responsibility (displaying user avatar). Cyclomatic complexity is low with only one conditional branch. Logic is simple and easily testable.

---

## COMPLIANT: Extracting Complex Logic into Custom Hooks

```typescript
// useFormValidation.ts - Complex logic isolated in a reusable hook
import { useState, useCallback } from 'react';

interface ValidationRule<T> {
  validate: (value: T) => boolean;
  message: string;
}

interface FieldConfig<T> {
  initialValue: T;
  rules: ValidationRule<T>[];
}

export function useFormValidation<T extends Record<string, unknown>>(
  config: { [K in keyof T]: FieldConfig<T[K]> }
) {
  const [values, setValues] = useState<T>(() => {
    const initial = {} as T;
    for (const key in config) {
      initial[key] = config[key].initialValue;
    }
    return initial;
  });

  const [errors, setErrors] = useState<Partial<Record<keyof T, string>>>({});
  const [touched, setTouched] = useState<Partial<Record<keyof T, boolean>>>({});

  const validateField = useCallback((field: keyof T, value: T[keyof T]): string | null => {
    const fieldConfig = config[field];
    for (const rule of fieldConfig.rules) {
      if (!rule.validate(value)) {
        return rule.message;
      }
    }
    return null;
  }, [config]);

  const setValue = useCallback(<K extends keyof T>(field: K, value: T[K]) => {
    setValues(prev => ({ ...prev, [field]: value }));
    if (touched[field]) {
      const error = validateField(field, value);
      setErrors(prev => ({ ...prev, [field]: error ?? undefined }));
    }
  }, [touched, validateField]);

  const setFieldTouched = useCallback((field: keyof T) => {
    setTouched(prev => ({ ...prev, [field]: true }));
    const error = validateField(field, values[field]);
    setErrors(prev => ({ ...prev, [field]: error ?? undefined }));
  }, [validateField, values]);

  const validateAll = useCallback((): boolean => {
    const newErrors: Partial<Record<keyof T, string>> = {};
    let isValid = true;

    for (const field in config) {
      const error = validateField(field, values[field]);
      if (error) {
        newErrors[field] = error;
        isValid = false;
      }
    }

    setErrors(newErrors);
    return isValid;
  }, [config, validateField, values]);

  return { values, errors, touched, setValue, setFieldTouched, validateAll };
}
```

```typescript
// LoginForm.tsx - Component remains simple by delegating logic to hook
import { useFormValidation } from './useFormValidation';

const loginFormConfig = {
  email: {
    initialValue: '',
    rules: [
      { validate: (v: string) => v.length > 0, message: 'Email is required' },
      { validate: (v: string) => v.includes('@'), message: 'Invalid email format' },
    ],
  },
  password: {
    initialValue: '',
    rules: [
      { validate: (v: string) => v.length > 0, message: 'Password is required' },
      { validate: (v: string) => v.length >= 8, message: 'Password must be at least 8 characters' },
    ],
  },
};

export function LoginForm({ onSubmit }: { onSubmit: (data: { email: string; password: string }) => void }) {
  const { values, errors, setValue, setFieldTouched, validateAll } = useFormValidation(loginFormConfig);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (validateAll()) {
      onSubmit(values);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          value={values.email}
          onChange={e => setValue('email', e.target.value)}
          onBlur={() => setFieldTouched('email')}
          aria-describedby={errors.email ? 'email-error' : undefined}
        />
        {errors.email && <span id="email-error" role="alert">{errors.email}</span>}
      </div>
      <div>
        <label htmlFor="password">Password</label>
        <input
          id="password"
          type="password"
          value={values.password}
          onChange={e => setValue('password', e.target.value)}
          onBlur={() => setFieldTouched('password')}
          aria-describedby={errors.password ? 'password-error' : undefined}
        />
        {errors.password && <span id="password-error" role="alert">{errors.password}</span>}
      </div>
      <button type="submit">Sign In</button>
    </form>
  );
}
```

**Why compliant:** Complex validation logic is extracted into a reusable hook. The component focuses solely on rendering UI and connecting to the hook. Each piece has low cyclomatic complexity and clear responsibilities.

---

## COMPLIANT: Composition Over Conditional Complexity

```typescript
// PaymentMethodDisplay.tsx - Using composition to avoid complex conditionals
interface PaymentMethod {
  type: 'credit_card' | 'bank_account' | 'paypal' | 'crypto';
  details: Record<string, string>;
}

// Individual display components - each with minimal complexity
function CreditCardDisplay({ details }: { details: Record<string, string> }) {
  return (
    <div className="payment-method credit-card">
      <span className="card-brand">{details.brand}</span>
      <span className="card-last4">****{details.last4}</span>
      <span className="card-expiry">Exp: {details.expMonth}/{details.expYear}</span>
    </div>
  );
}

function BankAccountDisplay({ details }: { details: Record<string, string> }) {
  return (
    <div className="payment-method bank-account">
      <span className="bank-name">{details.bankName}</span>
      <span className="account-last4">****{details.last4}</span>
    </div>
  );
}

function PayPalDisplay({ details }: { details: Record<string, string> }) {
  return (
    <div className="payment-method paypal">
      <span className="paypal-email">{details.email}</span>
    </div>
  );
}

function CryptoDisplay({ details }: { details: Record<string, string> }) {
  return (
    <div className="payment-method crypto">
      <span className="wallet-address">{details.address.slice(0, 8)}...</span>
      <span className="network">{details.network}</span>
    </div>
  );
}

// Component map replaces switch statement
const paymentDisplayComponents: Record<PaymentMethod['type'], React.ComponentType<{ details: Record<string, string> }>> = {
  credit_card: CreditCardDisplay,
  bank_account: BankAccountDisplay,
  paypal: PayPalDisplay,
  crypto: CryptoDisplay,
};

// Main component has minimal complexity
export function PaymentMethodDisplay({ method }: { method: PaymentMethod }) {
  const DisplayComponent = paymentDisplayComponents[method.type];
  return <DisplayComponent details={method.details} />;
}
```

**Why compliant:** Uses composition pattern with a component map instead of complex if/else or switch statements. Each payment method display is a separate, simple component. Main component has cyclomatic complexity of 1.

---

## VIOLATION: Monolithic Component with High Cyclomatic Complexity

```typescript
// BAD: UserDashboard.tsx - Massive component doing too many things
import { useState, useEffect } from 'react';

interface UserDashboardProps {
  userId: string;
  userRole: 'admin' | 'manager' | 'employee' | 'guest';
  featureFlags: Record<string, boolean>;
}

export function UserDashboard({ userId, userRole, featureFlags }: UserDashboardProps) {
  const [user, setUser] = useState<any>(null);
  const [notifications, setNotifications] = useState<any[]>([]);
  const [tasks, setTasks] = useState<any[]>([]);
  const [messages, setMessages] = useState<any[]>([]);
  const [analytics, setAnalytics] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');
  const [showModal, setShowModal] = useState(false);
  const [modalType, setModalType] = useState<string | null>(null);
  const [formData, setFormData] = useState<any>({});
  const [errors, setErrors] = useState<any>({});

  useEffect(() => {
    // Fetching everything in one massive effect
    Promise.all([
      fetch(`/api/users/${userId}`),
      fetch(`/api/notifications/${userId}`),
      fetch(`/api/tasks/${userId}`),
      fetch(`/api/messages/${userId}`),
      userRole === 'admin' || userRole === 'manager'
        ? fetch(`/api/analytics/${userId}`)
        : Promise.resolve(null)
    ]).then(async ([userRes, notifRes, taskRes, msgRes, analyticsRes]) => {
      setUser(await userRes.json());
      setNotifications(await notifRes.json());
      setTasks(await taskRes.json());
      setMessages(await msgRes.json());
      if (analyticsRes) setAnalytics(await analyticsRes.json());
      setLoading(false);
    });
  }, [userId, userRole]);

  const handleFormSubmit = () => {
    // Complex validation logic inline
    const newErrors: any = {};
    if (modalType === 'task') {
      if (!formData.title) newErrors.title = 'Required';
      if (!formData.description) newErrors.description = 'Required';
      if (formData.priority && !['low', 'medium', 'high'].includes(formData.priority)) {
        newErrors.priority = 'Invalid priority';
      }
      if (formData.dueDate && new Date(formData.dueDate) < new Date()) {
        newErrors.dueDate = 'Cannot be in the past';
      }
    } else if (modalType === 'message') {
      if (!formData.recipient) newErrors.recipient = 'Required';
      if (!formData.content) newErrors.content = 'Required';
      if (formData.content && formData.content.length > 1000) {
        newErrors.content = 'Too long';
      }
    } else if (modalType === 'notification') {
      if (!formData.type) newErrors.type = 'Required';
      if (!formData.message) newErrors.message = 'Required';
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    // Different submission logic per type
    if (modalType === 'task') {
      fetch('/api/tasks', { method: 'POST', body: JSON.stringify(formData) });
    } else if (modalType === 'message') {
      fetch('/api/messages', { method: 'POST', body: JSON.stringify(formData) });
    }
    setShowModal(false);
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div className="dashboard">
      {/* Complex role-based header */}
      <header>
        <h1>
          {userRole === 'admin' ? 'Admin Dashboard' :
           userRole === 'manager' ? 'Manager Dashboard' :
           userRole === 'employee' ? 'Employee Dashboard' : 'Guest Dashboard'}
        </h1>
        {(userRole === 'admin' || userRole === 'manager') && (
          <div className="admin-actions">
            <button onClick={() => { setModalType('task'); setShowModal(true); }}>
              New Task
            </button>
            {userRole === 'admin' && (
              <button onClick={() => { setModalType('notification'); setShowModal(true); }}>
                Send Notification
              </button>
            )}
          </div>
        )}
      </header>

      {/* Complex tab navigation */}
      <nav>
        <button onClick={() => setActiveTab('overview')}>Overview</button>
        <button onClick={() => setActiveTab('tasks')}>Tasks</button>
        <button onClick={() => setActiveTab('messages')}>Messages</button>
        {(userRole === 'admin' || userRole === 'manager') && (
          <button onClick={() => setActiveTab('analytics')}>Analytics</button>
        )}
        {featureFlags.newFeature && (
          <button onClick={() => setActiveTab('beta')}>Beta Features</button>
        )}
      </nav>

      {/* Complex conditional content */}
      <main>
        {activeTab === 'overview' && (
          <div>
            <section>
              <h2>Recent Notifications</h2>
              {notifications.length === 0 ? (
                <p>No notifications</p>
              ) : (
                notifications.slice(0, 5).map(n => (
                  <div key={n.id} className={`notification ${n.read ? 'read' : 'unread'}`}>
                    {n.type === 'urgent' ? <strong>{n.message}</strong> : n.message}
                  </div>
                ))
              )}
            </section>
            <section>
              <h2>Tasks Due Today</h2>
              {tasks.filter(t => {
                const today = new Date().toDateString();
                return new Date(t.dueDate).toDateString() === today;
              }).map(task => (
                <div key={task.id}>
                  {task.priority === 'high' && <span className="urgent">!</span>}
                  {task.title}
                </div>
              ))}
            </section>
          </div>
        )}
        {activeTab === 'tasks' && (
          <div>
            {/* More complex rendering logic... */}
          </div>
        )}
        {activeTab === 'analytics' && (userRole === 'admin' || userRole === 'manager') && (
          <div>
            {/* Analytics rendering... */}
          </div>
        )}
      </main>

      {/* Complex modal rendering */}
      {showModal && (
        <div className="modal">
          {modalType === 'task' && (
            <form>
              <input
                value={formData.title || ''}
                onChange={e => setFormData({...formData, title: e.target.value})}
              />
              {errors.title && <span>{errors.title}</span>}
              {/* More fields... */}
            </form>
          )}
          {modalType === 'message' && (
            <form>
              {/* Message form... */}
            </form>
          )}
        </div>
      )}
    </div>
  );
}
```

**Why violates ENG-3.1:** Component has extremely high cyclomatic complexity with numerous nested conditionals. It handles multiple responsibilities: data fetching, form validation, state management, role-based UI, tab navigation, and modal management. Should be decomposed into smaller, focused components and hooks.

---

## VIOLATION: Deeply Nested Conditional Rendering

```typescript
// BAD: OrderStatus.tsx - Excessive nesting and branching
interface Order {
  status: string;
  paymentStatus: string;
  shippingStatus: string;
  items: { type: string; fragile: boolean; size: string }[];
  customer: { type: string; membership: string };
  delivery: { type: string; scheduled: boolean };
}

export function OrderStatus({ order }: { order: Order }) {
  return (
    <div>
      {order.status === 'pending' ? (
        order.paymentStatus === 'awaiting' ? (
          order.customer.type === 'business' ? (
            order.customer.membership === 'premium' ? (
              <div>Premium business - payment pending, priority processing</div>
            ) : (
              <div>Business account - awaiting payment verification</div>
            )
          ) : (
            order.customer.membership === 'premium' ? (
              <div>Premium customer - payment pending</div>
            ) : (
              <div>Payment pending - please complete checkout</div>
            )
          )
        ) : order.paymentStatus === 'processing' ? (
          <div>Payment is being processed...</div>
        ) : (
          <div>Payment confirmed</div>
        )
      ) : order.status === 'processing' ? (
        order.shippingStatus === 'preparing' ? (
          order.items.some(i => i.fragile) ? (
            order.items.some(i => i.size === 'oversized') ? (
              <div>Special handling: fragile oversized items</div>
            ) : (
              <div>Careful packaging for fragile items</div>
            )
          ) : (
            <div>Preparing your order</div>
          )
        ) : order.shippingStatus === 'ready' ? (
          order.delivery.type === 'express' ? (
            order.delivery.scheduled ? (
              <div>Ready for scheduled express pickup</div>
            ) : (
              <div>Ready for next express shipment</div>
            )
          ) : (
            <div>Ready for standard shipping</div>
          )
        ) : (
          <div>Processing order</div>
        )
      ) : order.status === 'shipped' ? (
        <div>Order shipped</div>
      ) : order.status === 'delivered' ? (
        <div>Order delivered</div>
      ) : (
        <div>Unknown status</div>
      )}
    </div>
  );
}
```

**Why violates ENG-3.1:** Deeply nested ternary operators create extremely high cyclomatic complexity and are nearly impossible to read, test, or maintain. Each nesting level multiplies the number of possible paths. Should use early returns, lookup tables, or decompose into smaller functions.

---

## VIOLATION: Complex Inline Logic in JSX

```typescript
// BAD: ProductCard.tsx - Business logic mixed with rendering
export function ProductCard({ product, user, cart, promotions }: ProductCardProps) {
  return (
    <div className="product-card">
      <h3>{product.name}</h3>

      {/* Complex price calculation inline */}
      <p className="price">
        $
        {(
          product.basePrice -
          (promotions.find(p => p.productId === product.id)?.discount || 0) -
          (user.membership === 'gold'
            ? product.basePrice * 0.1
            : user.membership === 'silver'
              ? product.basePrice * 0.05
              : 0) -
          (cart.items.length > 5
            ? product.basePrice * 0.02
            : 0) +
          (product.category === 'electronics' && product.warrantyIncluded
            ? 0
            : product.category === 'electronics'
              ? 29.99
              : 0)
        ).toFixed(2)}
      </p>

      {/* Complex availability logic inline */}
      <p className="availability">
        {product.inventory > 0
          ? product.inventory > 10
            ? 'In Stock'
            : product.inventory > 5
              ? `Only ${product.inventory} left`
              : product.preorder
                ? `${product.inventory} left - preorder for more`
                : `Last ${product.inventory}!`
          : product.preorder
            ? product.preorderDate
              ? `Preorder - ships ${new Date(product.preorderDate).toLocaleDateString()}`
              : 'Preorder available'
            : product.restockDate
              ? `Out of stock - expected ${new Date(product.restockDate).toLocaleDateString()}`
              : 'Out of stock'}
      </p>

      {/* Complex button state logic inline */}
      <button
        disabled={
          product.inventory === 0 && !product.preorder ||
          cart.items.some(i => i.productId === product.id) && !product.allowMultiple ||
          user.membership === 'none' && product.membersOnly ||
          product.ageRestricted && (!user.verified || user.age < 21)
        }
      >
        {cart.items.some(i => i.productId === product.id)
          ? product.allowMultiple
            ? 'Add Another'
            : 'In Cart'
          : product.inventory === 0
            ? product.preorder
              ? 'Preorder Now'
              : 'Notify Me'
            : 'Add to Cart'}
      </button>
    </div>
  );
}
```

**Why violates ENG-3.1:** Complex business logic (pricing calculations, availability rules, button state) is embedded directly in JSX. This mixes concerns, makes testing difficult, and creates high cognitive load. Logic should be extracted into separate functions or hooks that can be tested independently.

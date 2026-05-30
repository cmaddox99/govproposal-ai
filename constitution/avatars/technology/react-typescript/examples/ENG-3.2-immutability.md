---
law_id: ENG-3.2
avatar: react-typescript
---

# ENG-3.2: Immutability Law Examples for React/TypeScript

## COMPLIANT: Readonly Props and Immutable State Updates

### Readonly Component Props

```tsx
// Readonly props prevent accidental mutation
type FlightCardProps = {
  readonly flightNumber: string;
  readonly origin: string;
  readonly destination: string;
  readonly departureTime: Date;
  readonly price: Money;
  readonly onSelect: (flightNumber: string) => void;
};

function FlightCard({
  flightNumber,
  origin,
  destination,
  departureTime,
  price,
  onSelect,
}: FlightCardProps) {
  return (
    <div className="flight-card">
      <h3>{flightNumber}</h3>
      <p>{origin} → {destination}</p>
      <p>{departureTime.toLocaleTimeString()}</p>
      <p>{formatMoney(price)}</p>
      <button onClick={() => onSelect(flightNumber)}>Select</button>
    </div>
  );
}
```

### Immutable State Updates with Spread Operator

```tsx
type CartState = {
  readonly items: readonly CartItem[];
  readonly promoCode: string | null;
};

type CartItem = {
  readonly id: string;
  readonly name: string;
  readonly price: number;
  readonly quantity: number;
};

function useCart() {
  const [cart, setCart] = useState<CartState>({
    items: [],
    promoCode: null,
  });

  // Immutable add: spread existing items, append new one
  const addItem = (item: Omit<CartItem, "quantity">) => {
    setCart((prev) => ({
      ...prev,
      items: [...prev.items, { ...item, quantity: 1 }],
    }));
  };

  // Immutable update: map to produce new array
  const updateQuantity = (itemId: string, quantity: number) => {
    setCart((prev) => ({
      ...prev,
      items: prev.items.map((item) =>
        item.id === itemId ? { ...item, quantity } : item
      ),
    }));
  };

  // Immutable remove: filter to produce new array
  const removeItem = (itemId: string) => {
    setCart((prev) => ({
      ...prev,
      items: prev.items.filter((item) => item.id !== itemId),
    }));
  };

  return { cart, addItem, updateQuantity, removeItem };
}
```

### Using Immer for Complex State Updates

```tsx
import { useImmerReducer } from "use-immer";

type BookingState = {
  readonly passengers: readonly Passenger[];
  readonly selectedSeats: ReadonlyMap<string, string>;
  readonly step: "passengers" | "seats" | "payment" | "confirmation";
};

type BookingAction =
  | { type: "ADD_PASSENGER"; passenger: Passenger }
  | { type: "SELECT_SEAT"; passengerId: string; seatId: string }
  | { type: "NEXT_STEP" };

function bookingReducer(draft: BookingState, action: BookingAction) {
  switch (action.type) {
    case "ADD_PASSENGER":
      // Immer lets you write "mutative" code that produces immutable updates
      draft.passengers.push(action.passenger);
      break;
    case "SELECT_SEAT":
      draft.selectedSeats.set(action.passengerId, action.seatId);
      break;
    case "NEXT_STEP":
      const steps = ["passengers", "seats", "payment", "confirmation"] as const;
      const currentIndex = steps.indexOf(draft.step);
      if (currentIndex < steps.length - 1) {
        draft.step = steps[currentIndex + 1];
      }
      break;
  }
}

function BookingWizard() {
  const [state, dispatch] = useImmerReducer(bookingReducer, {
    passengers: [],
    selectedSeats: new Map(),
    step: "passengers",
  });

  // State is always immutable -- Immer handles the conversion
  return <BookingStepRenderer state={state} dispatch={dispatch} />;
}
```

**Why compliant:** `readonly` on props and state types prevents accidental mutation at compile time. The spread operator and `Array.map()`/`Array.filter()` create new references, which React needs to detect changes. Immer provides ergonomic syntax while still producing immutable updates under the hood.

---

## VIOLATION: Mutating State Directly

```tsx
// BAD: Mutable props type
type FlightCardProps = {
  flightNumber: string;
  price: number;
  // VIOLATION: No readonly -- props can be accidentally mutated
};

// BAD: Direct state mutation
function Cart() {
  const [items, setItems] = useState<CartItem[]>([]);

  const addItem = (item: CartItem) => {
    // VIOLATION: Mutating the existing state array directly
    items.push(item);
    setItems(items); // React may not re-render -- same reference!
  };

  const updateQuantity = (itemId: string, qty: number) => {
    // VIOLATION: Mutating object inside array
    const item = items.find((i) => i.id === itemId);
    if (item) {
      item.quantity = qty; // Mutating existing object in state
      setItems([...items]); // Spread does not fix deep mutation
    }
  };

  const clearPromo = (cart: CartState) => {
    // VIOLATION: Direct property mutation
    cart.promoCode = null;
  };

  return (
    <div>
      {items.map((item) => (
        <div key={item.id}>
          {item.name}
          {/* VIOLATION: Mutating state object in event handler */}
          <button onClick={() => { item.quantity += 1; setItems([...items]); }}>
            +
          </button>
        </div>
      ))}
    </div>
  );
}
```

**Why violates ENG-3.2:** Direct mutation of state objects (`items.push()`, `item.quantity = qty`) bypasses React's change detection. React compares references to decide whether to re-render; mutating in place preserves the same reference, causing stale UI. Even when a new array is spread, deeply mutated objects inside it still share references, leading to subtle rendering bugs and broken memoization.

---

## Quick Reference

| Pattern | Mutable (Avoid) | Immutable (Prefer) |
|---------|-----------------|---------------------|
| Props | `type Props = { name: string }` | `type Props = { readonly name: string }` |
| Add to array | `arr.push(item)` | `[...arr, item]` |
| Update in array | `arr[i].prop = val` | `arr.map(x => x.id === id ? { ...x, prop: val } : x)` |
| Remove from array | `arr.splice(i, 1)` | `arr.filter(x => x.id !== id)` |
| Update object | `obj.prop = val` | `{ ...obj, prop: val }` |
| Complex updates | manual deep cloning | Immer (`produce` / `useImmerReducer`) |

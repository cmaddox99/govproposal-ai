---
law_id: ENG-3.2
avatar: angular
---

# ENG-3.2: Immutability Law Examples for Angular

## COMPLIANT: Readonly Properties and OnPush Change Detection

### Readonly Angular Service with Immutable State

```typescript
import { Injectable, Signal, computed, signal } from "@angular/core";

type FlightFilter = {
  readonly origin: string;
  readonly destination: string;
  readonly departureDate: string;
  readonly maxStops: number;
};

type FlightResult = {
  readonly flightNumber: string;
  readonly price: number;
  readonly stops: number;
  readonly departureTime: string;
};

type FlightSearchState = {
  readonly filter: FlightFilter;
  readonly results: readonly FlightResult[];
  readonly loading: boolean;
  readonly error: string | null;
};

@Injectable({ providedIn: "root" })
export class FlightSearchStore {
  // Private writable signal -- only this service can update state
  private readonly state = signal<FlightSearchState>({
    filter: { origin: "", destination: "", departureDate: "", maxStops: 2 },
    results: [],
    loading: false,
    error: null,
  });

  // Public readonly selectors
  readonly filter: Signal<FlightFilter> = computed(() => this.state().filter);
  readonly results: Signal<readonly FlightResult[]> = computed(() => this.state().results);
  readonly loading: Signal<boolean> = computed(() => this.state().loading);

  // Immutable state transitions -- always produce new state objects
  updateFilter(partial: Partial<FlightFilter>): void {
    this.state.update((s) => ({
      ...s,
      filter: { ...s.filter, ...partial },
    }));
  }

  setResults(results: readonly FlightResult[]): void {
    this.state.update((s) => ({
      ...s,
      results,
      loading: false,
      error: null,
    }));
  }

  setLoading(): void {
    this.state.update((s) => ({ ...s, loading: true, error: null }));
  }

  setError(error: string): void {
    this.state.update((s) => ({ ...s, loading: false, error }));
  }
}
```

### OnPush Component with Immutable Inputs

```typescript
import { Component, ChangeDetectionStrategy, input, output } from "@angular/core";

type CartItem = {
  readonly id: string;
  readonly name: string;
  readonly price: number;
  readonly quantity: number;
};

@Component({
  selector: "app-cart-item",
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <div class="cart-item">
      <span>{{ item().name }}</span>
      <span>{{ item().price | currency }}</span>
      <button (click)="onRemove.emit(item().id)">Remove</button>
    </div>
  `,
})
export class CartItemComponent {
  readonly item = input.required<CartItem>();
  readonly onRemove = output<string>();
}

@Component({
  selector: "app-cart",
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <app-cart-item
      *ngFor="let item of items(); trackBy: trackById"
      [item]="item"
      (onRemove)="removeItem($event)"
    />
    <p>Total: {{ total() | currency }}</p>
  `,
})
export class CartComponent {
  readonly items = input.required<readonly CartItem[]>();
  readonly onRemove = output<string>();

  readonly total = computed(() =>
    this.items().reduce((sum, item) => sum + item.price * item.quantity, 0)
  );

  trackById(_index: number, item: CartItem): string {
    return item.id;
  }

  removeItem(itemId: string): void {
    this.onRemove.emit(itemId);
  }
}
```

**Why compliant:** State is managed through Angular signals with immutable updates via the spread operator. `ChangeDetectionStrategy.OnPush` relies on reference changes to trigger re-renders, which immutability guarantees. `readonly` properties prevent accidental mutation at compile time. Public selectors expose read-only views of state.

---

## VIOLATION: Mutable Shared State in a Service

```typescript
import { Injectable } from "@angular/core";

// BAD: Mutable shared state
@Injectable({ providedIn: "root" })
export class FlightSearchService {
  // VIOLATION: Mutable public properties
  filter = {
    origin: "",
    destination: "",
    departureDate: "",
    maxStops: 2,
  };
  results: FlightResult[] = [];
  loading = false;

  // VIOLATION: Mutating state in place
  updateOrigin(origin: string): void {
    this.filter.origin = origin; // Direct property mutation
  }

  setResults(results: FlightResult[]): void {
    this.results = results;
    this.loading = false;
  }

  // VIOLATION: Sorting mutates the array in place
  sortByPrice(): void {
    this.results.sort((a, b) => a.price - b.price);
  }

  addResult(result: FlightResult): void {
    this.results.push(result); // Mutating the array
  }
}

// BAD: Component with default change detection relying on mutable service
@Component({
  selector: "app-flight-list",
  // VIOLATION: Missing ChangeDetectionStrategy.OnPush
  template: `
    <div *ngFor="let flight of searchService.results">
      {{ flight.flightNumber }} - {{ flight.price }}
    </div>
  `,
})
export class FlightListComponent {
  // VIOLATION: Direct access to mutable service state
  constructor(public searchService: FlightSearchService) {}

  // VIOLATION: External mutation of service state
  clearResults(): void {
    this.searchService.results.length = 0;
  }
}
```

**Why violates ENG-3.2:** Mutable service properties can be changed by any component that injects the service, leading to unpredictable state. `Array.sort()` and `Array.push()` mutate in place, so components using `OnPush` would miss updates. Without `readonly`, nothing prevents external code from directly overwriting or mutating shared state, making the application fragile and hard to debug.

---

## Quick Reference

| Pattern | Mutable (Avoid) | Immutable (Prefer) |
|---------|-----------------|---------------------|
| Service state | public mutable properties | `signal()` with `readonly` selectors |
| State update | `this.prop = val` | `state.update(s => ({ ...s, prop: val }))` |
| Array add | `arr.push(item)` | `[...arr, item]` |
| Array sort | `arr.sort()` | `[...arr].sort()` |
| Change detection | Default | `ChangeDetectionStrategy.OnPush` |
| Component inputs | `@Input() item: T` | `readonly item = input.required<T>()` |

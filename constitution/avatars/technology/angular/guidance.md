# Angular Guidance

> **Purpose:** Stack-specific agent behaviors for Angular frontend applications.

---

## Overview

This guidance provides patterns for AI agents working with Angular and TypeScript applications. It covers testing with Jasmine/Jest and Angular Testing Library, component patterns, and Angular-specific idioms.

---

## Testing Framework

**Primary Framework:** Jest + Angular Testing Library (or Jasmine/Karma)

### Test Structure

```typescript
import { render, screen, fireEvent } from '@testing-library/angular';
import { OrderSummaryComponent } from './order-summary.component';
import { Order, OrderItem } from '../../models/order.model';

describe('OrderSummaryComponent', () => {
  const mockOrder: Order = {
    id: 'order-123',
    items: [
      { id: '1', name: 'Widget', price: 100, quantity: 2 }
    ],
    total: 200,
    status: 'draft'
  };

  it('should display the order total', async () => {
    // Arrange & Act
    await render(OrderSummaryComponent, {
      componentInputs: { order: mockOrder }
    });

    // Assert
    expect(screen.getByText('$200.00')).toBeInTheDocument();
  });

  it('should emit checkout event when button clicked', async () => {
    // Arrange
    const onCheckout = jest.fn();
    await render(OrderSummaryComponent, {
      componentInputs: { order: mockOrder },
      componentOutputs: { checkout: { emit: onCheckout } as any }
    });

    // Act
    fireEvent.click(screen.getByRole('button', { name: /checkout/i }));

    // Assert
    expect(onCheckout).toHaveBeenCalledWith('order-123');
  });
});
```

### Service Testing

```typescript
import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { OrderService } from './order.service';

describe('OrderService', () => {
  let service: OrderService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [OrderService]
    });

    service = TestBed.inject(OrderService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should fetch order by id', () => {
    const mockOrder = { id: '123', total: 100 };

    service.getOrder('123').subscribe(order => {
      expect(order).toEqual(mockOrder);
    });

    const req = httpMock.expectOne('/api/orders/123');
    expect(req.request.method).toBe('GET');
    req.flush(mockOrder);
  });
});
```

---

## Component Patterns

### Smart/Container Component

```typescript
@Component({
  selector: 'app-order-container',
  standalone: true,
  imports: [OrderSummaryComponent, AsyncPipe, NgIf],
  template: `
    <ng-container *ngIf="order$ | async as order; else loading">
      <app-order-summary
        [order]="order"
        (checkout)="onCheckout($event)"
      />
    </ng-container>
    <ng-template #loading>
      <app-loading-spinner />
    </ng-template>
  `
})
export class OrderContainerComponent implements OnInit {
  @Input() orderId!: string;

  order$!: Observable<Order>;

  constructor(
    private orderService: OrderService,
    private router: Router
  ) {}

  ngOnInit() {
    this.order$ = this.orderService.getOrder(this.orderId);
  }

  onCheckout(orderId: string) {
    this.orderService.checkout(orderId).subscribe({
      next: () => this.router.navigate(['/confirmation', orderId]),
      error: (err) => console.error('Checkout failed:', err)
    });
  }
}
```

### Presentational Component

```typescript
@Component({
  selector: 'app-order-summary',
  standalone: true,
  imports: [CurrencyPipe, NgFor],
  template: `
    <div class="order-summary">
      <h2>Order Summary</h2>

      <ul class="order-items">
        <li *ngFor="let item of order.items">
          {{ item.name }} x {{ item.quantity }}:
          {{ item.price * item.quantity | currency }}
        </li>
      </ul>

      <div class="order-total">
        <strong>Total:</strong>
        {{ order.total | currency }}
      </div>

      <button
        (click)="checkout.emit(order.id)"
        [disabled]="order.items.length === 0"
        aria-label="Proceed to checkout"
      >
        Checkout
      </button>
    </div>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class OrderSummaryComponent {
  @Input({ required: true }) order!: Order;
  @Output() checkout = new EventEmitter<string>();
}
```

### Signal-Based Component (Angular 17+)

```typescript
@Component({
  selector: 'app-order-summary',
  standalone: true,
  imports: [CurrencyPipe],
  template: `
    <div class="order-summary">
      <h2>Order Summary</h2>
      <div class="order-total">
        Total: {{ total() | currency }}
      </div>
      <button (click)="onCheckout()">Checkout</button>
    </div>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class OrderSummaryComponent {
  order = input.required<Order>();
  checkout = output<string>();

  total = computed(() =>
    this.order().items.reduce(
      (sum, item) => sum + item.price * item.quantity,
      0
    )
  );

  onCheckout() {
    this.checkout.emit(this.order().id);
  }
}
```

---

## Domain Modeling

### Models/Types

```typescript
// models/order.model.ts

export interface Money {
  readonly amount: number;
  readonly currency: string;
}

export interface OrderItem {
  readonly id: string;
  readonly productId: string;
  readonly name: string;
  readonly price: number;
  readonly quantity: number;
}

export interface Order {
  readonly id: string;
  readonly customerId: string;
  readonly items: readonly OrderItem[];
  readonly status: OrderStatus;
  readonly total: number;
}

export type OrderStatus = 'draft' | 'placed' | 'shipped' | 'delivered';

// Domain functions
export function calculateOrderTotal(items: readonly OrderItem[]): number {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

export function canModifyOrder(order: Order): boolean {
  return order.status === 'draft';
}
```

---

## Common Patterns

### Service with HttpClient

```typescript
@Injectable({ providedIn: 'root' })
export class OrderService {
  private readonly apiUrl = '/api/orders';

  constructor(private http: HttpClient) {}

  getOrder(id: string): Observable<Order> {
    return this.http.get<Order>(`${this.apiUrl}/${id}`);
  }

  getOrders(): Observable<Order[]> {
    return this.http.get<Order[]>(this.apiUrl);
  }

  createOrder(customerId: string): Observable<Order> {
    return this.http.post<Order>(this.apiUrl, { customerId });
  }

  checkout(orderId: string): Observable<Order> {
    return this.http.post<Order>(`${this.apiUrl}/${orderId}/checkout`, {});
  }
}
```

### State Management with Signals

```typescript
@Injectable({ providedIn: 'root' })
export class OrderStore {
  // State
  private readonly _orders = signal<Order[]>([]);
  private readonly _loading = signal(false);
  private readonly _error = signal<string | null>(null);

  // Public selectors
  readonly orders = this._orders.asReadonly();
  readonly loading = this._loading.asReadonly();
  readonly error = this._error.asReadonly();

  readonly orderCount = computed(() => this._orders().length);

  constructor(private orderService: OrderService) {}

  loadOrders(): void {
    this._loading.set(true);
    this._error.set(null);

    this.orderService.getOrders().subscribe({
      next: (orders) => {
        this._orders.set(orders);
        this._loading.set(false);
      },
      error: (err) => {
        this._error.set('Failed to load orders');
        this._loading.set(false);
      }
    });
  }
}
```

### Route Guards

```typescript
export const authGuard: CanActivateFn = (route, state) => {
  const authService = inject(AuthService);
  const router = inject(Router);

  if (authService.isAuthenticated()) {
    return true;
  }

  return router.createUrlTree(['/login'], {
    queryParams: { returnUrl: state.url }
  });
};

// Usage in routes
export const routes: Routes = [
  {
    path: 'orders',
    loadComponent: () => import('./features/orders/orders.component'),
    canActivate: [authGuard]
  }
];
```

---

## Anti-Patterns to Avoid

### Logic in Templates

```typescript
// BAD - Complex logic in template
@Component({
  template: `
    <div>
      Total: {{ items.reduce((sum, item) =>
        sum + (item.price * item.quantity * (1 - (item.discount || 0))), 0
      ) | currency }}
    </div>
  `
})

// GOOD - Logic in component
@Component({
  template: `<div>Total: {{ total | currency }}</div>`
})
export class OrderComponent {
  items = input.required<OrderItem[]>();
  total = computed(() => calculateOrderTotal(this.items()));
}
```

### Manual Subscriptions without Cleanup

```typescript
// BAD - Memory leak
@Component({})
export class OrderComponent implements OnInit {
  order: Order;

  ngOnInit() {
    this.orderService.getOrder('123').subscribe(order => {
      this.order = order; // Subscription never cleaned up!
    });
  }
}

// GOOD - Using async pipe
@Component({
  template: `
    <div *ngIf="order$ | async as order">{{ order.total }}</div>
  `
})
export class OrderComponent {
  order$ = this.orderService.getOrder('123');
}

// GOOD - Using takeUntilDestroyed
@Component({})
export class OrderComponent {
  order = signal<Order | null>(null);

  constructor() {
    this.orderService.getOrder('123')
      .pipe(takeUntilDestroyed())
      .subscribe(order => this.order.set(order));
  }
}
```

---

## Tools and Commands

### Development

```bash
# Start dev server
ng serve

# Build for production
ng build --configuration production

# Generate component
ng generate component features/orders/components/order-item

# Generate service
ng generate service core/services/order

# Update Angular
ng update @angular/core @angular/cli
```

### Testing

```bash
# Run tests
ng test

# Single run (CI)
ng test --watch=false --browsers=ChromeHeadless

# With coverage
ng test --code-coverage

# Specific file
ng test --include=**/order*.spec.ts
```

### Code Quality

```bash
# Lint
ng lint

# Format (if using Prettier)
npm run format

# Build to check for errors
ng build --configuration production
```

---

## Angular-Specific Guidance

### Dependency Injection

```typescript
// Prefer providedIn: 'root' for singleton services
@Injectable({ providedIn: 'root' })
export class OrderService { }

// Use injection tokens for configuration
export const API_URL = new InjectionToken<string>('API_URL');

// Provide at component level for scoped instances
@Component({
  providers: [OrderFormService]
})
export class OrderFormComponent { }
```

### Change Detection

```typescript
// Use OnPush for better performance
@Component({
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class OrderItemComponent {
  @Input() item!: OrderItem;
}

// With OnPush, ensure inputs are immutable
// Update objects/arrays with new references
this.items = [...this.items, newItem]; // Creates new array
```

### Lazy Loading

```typescript
// app.routes.ts
export const routes: Routes = [
  {
    path: 'orders',
    loadChildren: () =>
      import('./features/orders/orders.routes').then(m => m.ORDER_ROUTES)
  }
];

// features/orders/orders.routes.ts
export const ORDER_ROUTES: Routes = [
  {
    path: '',
    loadComponent: () =>
      import('./components/order-list/order-list.component')
  },
  {
    path: ':id',
    loadComponent: () =>
      import('./components/order-detail/order-detail.component')
  }
];
```

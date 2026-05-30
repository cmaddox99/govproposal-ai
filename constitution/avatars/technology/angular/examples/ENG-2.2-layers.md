---
law_id: ENG-2.2
avatar: angular
---

# ENG-2.2: Layered Architecture Examples for Angular

## COMPLIANT: Clean Layers with Proper Separation

```typescript
// === PRESENTATION LAYER: Components handle UI only ===

// order-list.component.ts
import { Component, inject, ChangeDetectionStrategy } from '@angular/core';
import { CommonModule, AsyncPipe } from '@angular/common';
import { OrderFacade } from '../../application/order.facade';

@Component({
  selector: 'app-order-list',
  standalone: true,
  imports: [CommonModule, AsyncPipe],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <section *ngIf="orders$ | async as orders">
      <app-order-card
        *ngFor="let order of orders"
        [order]="order"
        (submit)="onSubmit(order.id)" />
    </section>
    <p *ngIf="error$ | async as error" role="alert">{{ error }}</p>
  `
})
export class OrderListComponent {
  private readonly facade = inject(OrderFacade);

  readonly orders$ = this.facade.orders$;
  readonly error$ = this.facade.error$;

  onSubmit(orderId: string): void {
    this.facade.submitOrder(orderId);
  }
}


// === APPLICATION LAYER: Facades orchestrate use cases ===

// order.facade.ts
import { Injectable, inject } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { Order } from '../../domain/models/order.model';
import { OrderRepository } from '../../domain/ports/order.repository';
import { NotificationService } from '../../domain/ports/notification.service';

@Injectable({ providedIn: 'root' })
export class OrderFacade {
  private readonly repository = inject(OrderRepository);
  private readonly notifications = inject(NotificationService);

  private readonly ordersSubject = new BehaviorSubject<Order[]>([]);
  private readonly errorSubject = new BehaviorSubject<string | null>(null);

  readonly orders$: Observable<Order[]> = this.ordersSubject.asObservable();
  readonly error$: Observable<string | null> = this.errorSubject.asObservable();

  async loadOrders(): Promise<void> {
    try {
      const orders = await this.repository.findAll();
      this.ordersSubject.next(orders);
    } catch {
      this.errorSubject.next('Failed to load orders');
    }
  }

  async submitOrder(orderId: string): Promise<void> {
    const order = this.ordersSubject.value.find(o => o.id === orderId);
    if (!order) return;

    const submitted = order.submit();
    await this.repository.save(submitted);
    await this.notifications.notify(`Order ${orderId} submitted`);
    await this.loadOrders();
  }
}


// === DOMAIN LAYER: Models contain business logic, no external dependencies ===

// domain/models/order.model.ts
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
    return this.items.reduce((sum, item) => sum + item.quantity * item.unitPrice, 0);
  }
}

// domain/ports/order.repository.ts (interface only)
export abstract class OrderRepository {
  abstract findAll(): Promise<Order[]>;
  abstract findById(id: string): Promise<Order | null>;
  abstract save(order: Order): Promise<void>;
}


// === INFRASTRUCTURE LAYER: Implements domain ports ===

// infrastructure/http-order.repository.ts
import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { firstValueFrom } from 'rxjs';
import { Order } from '../../domain/models/order.model';
import { OrderRepository } from '../../domain/ports/order.repository';

@Injectable({ providedIn: 'root' })
export class HttpOrderRepository extends OrderRepository {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = '/api/orders';

  async findAll(): Promise<Order[]> {
    const response = await firstValueFrom(
      this.http.get<OrderDto[]>(this.baseUrl)
    );
    return response.map(this.toDomain);
  }

  async findById(id: string): Promise<Order | null> {
    const response = await firstValueFrom(
      this.http.get<OrderDto>(`${this.baseUrl}/${id}`)
    );
    return response ? this.toDomain(response) : null;
  }

  async save(order: Order): Promise<void> {
    await firstValueFrom(
      this.http.put(`${this.baseUrl}/${order.id}`, this.toDto(order))
    );
  }

  private toDomain(dto: OrderDto): Order {
    return new Order(dto.id, dto.customerId, dto.items, dto.status, new Date(dto.createdAt));
  }

  private toDto(order: Order): OrderDto {
    return {
      id: order.id,
      customerId: order.customerId,
      items: [...order.items],
      status: order.status,
      createdAt: order.createdAt.toISOString()
    };
  }
}
```

**Why compliant:**
- Presentation layer (components) handles only UI rendering and user events
- Application layer (facades) orchestrates use cases without business logic
- Domain layer defines models and interfaces with no external dependencies
- Infrastructure layer implements domain ports with HTTP details isolated
- Dependencies point inward: Infrastructure -> Application -> Domain

---

## VIOLATION: Business Logic in Components, Direct HTTP Calls

```typescript
// BAD: Component doing everything
import { Component, OnInit, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-order-list',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div *ngFor="let order of orders">
      <span>{{ order.id }}</span>
      <span>Total: ${{ calculateTotal(order) }}</span>
      <button
        [disabled]="order.status !== 'draft' || order.items.length === 0"
        (click)="submitOrder(order)">
        Submit
      </button>
    </div>
  `
})
export class OrderListComponent implements OnInit {
  private readonly http = inject(HttpClient);  // Direct HTTP in component!

  orders: any[] = [];

  ngOnInit(): void {
    // Direct HTTP call from component - no service layer
    this.http.get<any[]>('/api/orders').subscribe(data => {
      this.orders = data;
    });
  }

  // Business logic in the component!
  calculateTotal(order: any): string {
    let total = 0;
    for (const item of order.items) {
      if (item.quantity > 10) {
        total += item.unitPrice * item.quantity * 0.9;  // Discount logic in component!
      } else {
        total += item.unitPrice * item.quantity;
      }
    }
    return total.toFixed(2);
  }

  submitOrder(order: any): void {
    // Business validation in component!
    if (order.status !== 'draft') {
      alert('Cannot submit non-draft order');
      return;
    }
    if (order.items.length === 0) {
      alert('Cannot submit empty order');
      return;
    }

    // Direct HTTP call with status mutation
    order.status = 'submitted';
    this.http.put(`/api/orders/${order.id}`, order).subscribe({
      next: () => alert('Order submitted!'),
      error: () => alert('Failed to submit')
    });
  }
}
```

**Why violates ENG-2.2:**
- Component makes direct HTTP calls, bypassing any service or repository layer
- Business rules (discount calculation, status validation) are in the presentation layer
- No separation between domain logic and UI concerns
- Impossible to test business rules without rendering the component
- Adding a new UI (e.g., mobile) would require duplicating all business logic

---

## Layer Responsibilities

| Layer | Responsibility | Angular Artifacts |
|-------|----------------|-------------------|
| **Presentation** | UI rendering, user events | Components, Directives, Pipes |
| **Application** | Use case orchestration | Facades, State Services |
| **Domain** | Business rules, models | Classes, Interfaces, Value Objects |
| **Infrastructure** | External systems | HTTP Services, Storage, WebSocket |

---

## Dependency Inversion with Angular DI

```typescript
// Domain defines the PORT (abstract class as interface)
export abstract class OrderRepository {
  abstract findAll(): Promise<Order[]>;
  abstract save(order: Order): Promise<void>;
}

// Infrastructure provides the ADAPTER
@Injectable({ providedIn: 'root' })
export class HttpOrderRepository extends OrderRepository {
  // ... HTTP implementation
}

// Wire in app.config.ts
export const appConfig: ApplicationConfig = {
  providers: [
    { provide: OrderRepository, useClass: HttpOrderRepository }
  ]
};
```

**Key principle:** Domain defines abstract classes (ports), infrastructure implements them (adapters), and Angular's DI wires them together.

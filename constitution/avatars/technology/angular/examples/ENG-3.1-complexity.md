---
law_id: ENG-3.1
avatar: angular
---

# ENG-3.1: Complexity Examples for Angular

## COMPLIANT: Single Responsibility Component with Low Cyclomatic Complexity

```typescript
// user-avatar.component.ts - Single purpose, minimal branching
import { Component, Input, ChangeDetectionStrategy } from '@angular/core';
import { CommonModule } from '@angular/common';

type AvatarSize = 'small' | 'medium' | 'large';

interface User {
  name: string;
  avatarUrl?: string;
}

@Component({
  selector: 'app-user-avatar',
  standalone: true,
  imports: [CommonModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <div
      class="avatar"
      [style.width.px]="dimension"
      [style.height.px]="dimension"
      role="img"
      [attr.aria-label]="'Avatar for ' + user.name">
      <img *ngIf="user.avatarUrl; else initials" [src]="user.avatarUrl" alt="" />
      <ng-template #initials>
        <span class="initials">{{ getInitials() }}</span>
      </ng-template>
    </div>
  `,
  styles: [`
    .avatar { border-radius: 50%; overflow: hidden; display: flex; align-items: center; justify-content: center; }
    .initials { font-weight: bold; }
  `]
})
export class UserAvatarComponent {
  @Input({ required: true }) user!: User;
  @Input() size: AvatarSize = 'medium';

  private readonly sizeMap: Record<AvatarSize, number> = {
    small: 32,
    medium: 48,
    large: 64
  };

  get dimension(): number {
    return this.sizeMap[this.size];
  }

  getInitials(): string {
    return this.user.name
      .split(' ')
      .map(word => word[0])
      .join('')
      .slice(0, 2)
      .toUpperCase();
  }
}
```

**Why compliant:** Component has a single responsibility (displaying user avatar). Cyclomatic complexity is low with only one conditional (ngIf). Uses OnPush change detection for performance. Logic is simple and easily testable.

---

## COMPLIANT: Extracting Complex Logic into Services

```typescript
// form-validation.service.ts - Complex logic isolated in a service
import { Injectable } from '@angular/core';
import { AbstractControl, ValidatorFn, ValidationErrors } from '@angular/forms';

export interface ValidationRule {
  validator: ValidatorFn;
  message: string;
}

@Injectable({ providedIn: 'root' })
export class FormValidationService {
  required(message = 'This field is required'): ValidationRule {
    return {
      validator: (control: AbstractControl): ValidationErrors | null => {
        return control.value?.trim() ? null : { required: true };
      },
      message
    };
  }

  email(message = 'Invalid email format'): ValidationRule {
    return {
      validator: (control: AbstractControl): ValidationErrors | null => {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(control.value) ? null : { email: true };
      },
      message
    };
  }

  minLength(min: number, message?: string): ValidationRule {
    return {
      validator: (control: AbstractControl): ValidationErrors | null => {
        return control.value?.length >= min ? null : { minLength: { min } };
      },
      message: message ?? `Must be at least ${min} characters`
    };
  }

  pattern(regex: RegExp, message: string): ValidationRule {
    return {
      validator: (control: AbstractControl): ValidationErrors | null => {
        return regex.test(control.value) ? null : { pattern: true };
      },
      message
    };
  }

  getErrorMessage(control: AbstractControl, rules: ValidationRule[]): string | null {
    if (!control.errors || !control.touched) return null;

    for (const rule of rules) {
      const errorKey = Object.keys(control.errors)[0];
      if (rule.validator(control)) continue;
      return rule.message;
    }
    return null;
  }
}
```

```typescript
// login-form.component.ts - Component remains simple by delegating logic
import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
import { FormValidationService } from '../services/form-validation.service';

@Component({
  selector: 'app-login-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  template: `
    <form [formGroup]="form" (ngSubmit)="onSubmit()">
      <div class="form-group">
        <label for="email">Email</label>
        <input id="email" type="email" formControlName="email" />
        <span *ngIf="getError('email')" role="alert">{{ getError('email') }}</span>
      </div>

      <div class="form-group">
        <label for="password">Password</label>
        <input id="password" type="password" formControlName="password" />
        <span *ngIf="getError('password')" role="alert">{{ getError('password') }}</span>
      </div>

      <button type="submit" [disabled]="form.invalid">Sign In</button>
    </form>
  `
})
export class LoginFormComponent {
  private fb = inject(FormBuilder);
  private validation = inject(FormValidationService);

  private emailRules = [
    this.validation.required('Email is required'),
    this.validation.email()
  ];

  private passwordRules = [
    this.validation.required('Password is required'),
    this.validation.minLength(8)
  ];

  form = this.fb.group({
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(8)]]
  });

  getError(field: 'email' | 'password'): string | null {
    const control = this.form.get(field);
    const rules = field === 'email' ? this.emailRules : this.passwordRules;
    return control ? this.validation.getErrorMessage(control, rules) : null;
  }

  onSubmit(): void {
    if (this.form.valid) {
      console.log('Form submitted', this.form.value);
    }
  }
}
```

**Why compliant:** Complex validation logic is extracted into a reusable service. Component focuses solely on rendering UI and connecting to the service. Each piece has low cyclomatic complexity and clear responsibilities.

---

## COMPLIANT: Using Structural Directives to Reduce Complexity

```typescript
// payment-method-display.component.ts - Using ngSwitch for cleaner branching
import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

type PaymentType = 'credit_card' | 'bank_account' | 'paypal' | 'crypto';

interface PaymentMethod {
  type: PaymentType;
  details: Record<string, string>;
}

@Component({
  selector: 'app-payment-method',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="payment-method" [ngSwitch]="method.type">
      <ng-container *ngSwitchCase="'credit_card'">
        <app-credit-card [details]="method.details" />
      </ng-container>

      <ng-container *ngSwitchCase="'bank_account'">
        <app-bank-account [details]="method.details" />
      </ng-container>

      <ng-container *ngSwitchCase="'paypal'">
        <app-paypal [details]="method.details" />
      </ng-container>

      <ng-container *ngSwitchCase="'crypto'">
        <app-crypto [details]="method.details" />
      </ng-container>
    </div>
  `
})
export class PaymentMethodDisplayComponent {
  @Input({ required: true }) method!: PaymentMethod;
}

// Individual display components - each with minimal complexity
@Component({
  selector: 'app-credit-card',
  standalone: true,
  template: `
    <div class="credit-card">
      <span class="card-brand">{{ details['brand'] }}</span>
      <span class="card-last4">****{{ details['last4'] }}</span>
      <span class="card-expiry">Exp: {{ details['expMonth'] }}/{{ details['expYear'] }}</span>
    </div>
  `
})
export class CreditCardComponent {
  @Input({ required: true }) details!: Record<string, string>;
}

@Component({
  selector: 'app-bank-account',
  standalone: true,
  template: `
    <div class="bank-account">
      <span class="bank-name">{{ details['bankName'] }}</span>
      <span class="account-last4">****{{ details['last4'] }}</span>
    </div>
  `
})
export class BankAccountComponent {
  @Input({ required: true }) details!: Record<string, string>;
}

@Component({
  selector: 'app-paypal',
  standalone: true,
  template: `
    <div class="paypal">
      <span class="paypal-email">{{ details['email'] }}</span>
    </div>
  `
})
export class PayPalComponent {
  @Input({ required: true }) details!: Record<string, string>;
}

@Component({
  selector: 'app-crypto',
  standalone: true,
  template: `
    <div class="crypto">
      <span class="wallet-address">{{ details['address'] | slice:0:8 }}...</span>
      <span class="network">{{ details['network'] }}</span>
    </div>
  `
})
export class CryptoComponent {
  @Input({ required: true }) details!: Record<string, string>;
}
```

**Why compliant:** Uses ngSwitch directive for clean branching instead of nested conditionals. Each payment method display is a separate, simple component. Main component delegates rendering to child components. Each piece has cyclomatic complexity of 1-2.

---

## COMPLIANT: Using Pipes to Extract Template Logic

```typescript
// price-display.pipe.ts
import { Pipe, PipeTransform } from '@angular/core';

interface PriceConfig {
  basePrice: number;
  discount?: number;
  membershipType?: 'gold' | 'silver' | 'none';
  taxRate?: number;
}

@Pipe({
  name: 'priceDisplay',
  standalone: true
})
export class PriceDisplayPipe implements PipeTransform {
  private readonly membershipDiscounts: Record<string, number> = {
    gold: 0.10,
    silver: 0.05,
    none: 0
  };

  transform(config: PriceConfig): string {
    const membershipDiscount = this.membershipDiscounts[config.membershipType ?? 'none'];
    const discountAmount = config.discount ?? 0;

    let finalPrice = config.basePrice;
    finalPrice -= discountAmount;
    finalPrice -= config.basePrice * membershipDiscount;

    if (config.taxRate) {
      finalPrice += finalPrice * config.taxRate;
    }

    return finalPrice.toFixed(2);
  }
}
```

```typescript
// product-card.component.ts - Clean template using pipe
import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PriceDisplayPipe } from '../pipes/price-display.pipe';

@Component({
  selector: 'app-product-card',
  standalone: true,
  imports: [CommonModule, PriceDisplayPipe],
  template: `
    <article class="product-card">
      <h3>{{ product.name }}</h3>
      <p class="price">
        ${{ { basePrice: product.price, discount: discount, membershipType: membershipType } | priceDisplay }}
      </p>
      <button (click)="addToCart.emit(product)">Add to Cart</button>
    </article>
  `
})
export class ProductCardComponent {
  @Input({ required: true }) product!: { name: string; price: number };
  @Input() discount = 0;
  @Input() membershipType: 'gold' | 'silver' | 'none' = 'none';
  @Output() addToCart = new EventEmitter<typeof this.product>();
}
```

**Why compliant:** Complex price calculation logic is extracted into a reusable pipe. Component template remains clean and readable. Pipe is easily testable in isolation. Separation of concerns between presentation and business logic.

---

## VIOLATION: Monolithic Component with High Cyclomatic Complexity

```typescript
// BAD: user-dashboard.component.ts - Massive component doing too many things
import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Subscription, forkJoin } from 'rxjs';

@Component({
  selector: 'app-user-dashboard',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="dashboard">
      <!-- Complex role-based header -->
      <header>
        <h1>
          {{ userRole === 'admin' ? 'Admin Dashboard' :
             userRole === 'manager' ? 'Manager Dashboard' :
             userRole === 'employee' ? 'Employee Dashboard' : 'Guest Dashboard' }}
        </h1>
        <div *ngIf="userRole === 'admin' || userRole === 'manager'" class="admin-actions">
          <button (click)="openModal('task')">New Task</button>
          <button *ngIf="userRole === 'admin'" (click)="openModal('notification')">
            Send Notification
          </button>
        </div>
      </header>

      <!-- Complex tab navigation -->
      <nav>
        <button (click)="activeTab = 'overview'">Overview</button>
        <button (click)="activeTab = 'tasks'">Tasks</button>
        <button (click)="activeTab = 'messages'">Messages</button>
        <button *ngIf="userRole === 'admin' || userRole === 'manager'"
                (click)="activeTab = 'analytics'">Analytics</button>
        <button *ngIf="featureFlags['newFeature']"
                (click)="activeTab = 'beta'">Beta Features</button>
      </nav>

      <!-- Complex conditional content -->
      <main>
        <div *ngIf="activeTab === 'overview'">
          <section>
            <h2>Recent Notifications</h2>
            <p *ngIf="notifications.length === 0">No notifications</p>
            <div *ngFor="let n of notifications.slice(0, 5)"
                 [class.read]="n.read"
                 [class.unread]="!n.read">
              <strong *ngIf="n.type === 'urgent'">{{ n.message }}</strong>
              <span *ngIf="n.type !== 'urgent'">{{ n.message }}</span>
            </div>
          </section>
          <section>
            <h2>Tasks Due Today</h2>
            <div *ngFor="let task of getTasksDueToday()">
              <span *ngIf="task.priority === 'high'" class="urgent">!</span>
              {{ task.title }}
            </div>
          </section>
        </div>

        <div *ngIf="activeTab === 'tasks'">
          <!-- More complex rendering... -->
        </div>

        <div *ngIf="activeTab === 'analytics' && (userRole === 'admin' || userRole === 'manager')">
          <!-- Analytics rendering... -->
        </div>
      </main>

      <!-- Complex modal -->
      <div *ngIf="showModal" class="modal">
        <form *ngIf="modalType === 'task'" (ngSubmit)="handleFormSubmit()">
          <input [(ngModel)]="formData.title" name="title" />
          <span *ngIf="errors['title']">{{ errors['title'] }}</span>
          <!-- More fields... -->
        </form>
        <form *ngIf="modalType === 'message'" (ngSubmit)="handleFormSubmit()">
          <!-- Message form... -->
        </form>
      </div>
    </div>
  `
})
export class UserDashboardComponent implements OnInit, OnDestroy {
  userId!: string;
  userRole: 'admin' | 'manager' | 'employee' | 'guest' = 'guest';
  featureFlags: Record<string, boolean> = {};

  user: any = null;
  notifications: any[] = [];
  tasks: any[] = [];
  messages: any[] = [];
  analytics: any = null;

  loading = true;
  activeTab = 'overview';
  showModal = false;
  modalType: string | null = null;
  formData: any = {};
  errors: any = {};

  private subscriptions: Subscription[] = [];

  ngOnInit(): void {
    // Massive data fetching
    const sub = forkJoin([
      this.userService.getUser(this.userId),
      this.notificationService.getNotifications(this.userId),
      this.taskService.getTasks(this.userId),
      this.messageService.getMessages(this.userId),
      ...(this.userRole === 'admin' || this.userRole === 'manager'
        ? [this.analyticsService.getAnalytics(this.userId)]
        : [])
    ]).subscribe(([user, notifications, tasks, messages, analytics]) => {
      this.user = user;
      this.notifications = notifications;
      this.tasks = tasks;
      this.messages = messages;
      if (analytics) this.analytics = analytics;
      this.loading = false;
    });

    this.subscriptions.push(sub);
  }

  ngOnDestroy(): void {
    this.subscriptions.forEach(sub => sub.unsubscribe());
  }

  getTasksDueToday(): any[] {
    const today = new Date().toDateString();
    return this.tasks.filter(t => new Date(t.dueDate).toDateString() === today);
  }

  openModal(type: string): void {
    this.modalType = type;
    this.showModal = true;
  }

  handleFormSubmit(): void {
    // Complex validation logic inline
    const newErrors: any = {};
    if (this.modalType === 'task') {
      if (!this.formData.title) newErrors['title'] = 'Required';
      if (!this.formData.description) newErrors['description'] = 'Required';
      if (this.formData.priority && !['low', 'medium', 'high'].includes(this.formData.priority)) {
        newErrors['priority'] = 'Invalid priority';
      }
      if (this.formData.dueDate && new Date(this.formData.dueDate) < new Date()) {
        newErrors['dueDate'] = 'Cannot be in the past';
      }
    } else if (this.modalType === 'message') {
      if (!this.formData.recipient) newErrors['recipient'] = 'Required';
      if (!this.formData.content) newErrors['content'] = 'Required';
      if (this.formData.content && this.formData.content.length > 1000) {
        newErrors['content'] = 'Too long';
      }
    }

    if (Object.keys(newErrors).length > 0) {
      this.errors = newErrors;
      return;
    }

    // Submission logic per type...
  }
}
```

**Why violates ENG-3.1:** Component has extremely high cyclomatic complexity with numerous nested conditionals. It handles multiple responsibilities: data fetching, form validation, state management, role-based UI, tab navigation, and modal management. Should be decomposed into smaller components, services, and use reactive patterns.

---

## VIOLATION: Complex Logic in Template

```typescript
// BAD: order-status.component.ts - Excessive logic in template
import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-order-status',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div>
      <!-- Deeply nested ternary operators in template -->
      {{ order.status === 'pending'
        ? (order.paymentStatus === 'awaiting'
          ? (order.customer.type === 'business'
            ? (order.customer.membership === 'premium'
              ? 'Premium business - payment pending, priority processing'
              : 'Business account - awaiting payment verification')
            : (order.customer.membership === 'premium'
              ? 'Premium customer - payment pending'
              : 'Payment pending - please complete checkout'))
          : (order.paymentStatus === 'processing'
            ? 'Payment is being processed...'
            : 'Payment confirmed'))
        : (order.status === 'processing'
          ? (order.shippingStatus === 'preparing'
            ? (hasFragileItems()
              ? (hasOversizedItems()
                ? 'Special handling: fragile oversized items'
                : 'Careful packaging for fragile items')
              : 'Preparing your order')
            : (order.shippingStatus === 'ready'
              ? (order.delivery.type === 'express'
                ? (order.delivery.scheduled
                  ? 'Ready for scheduled express pickup'
                  : 'Ready for next express shipment')
                : 'Ready for standard shipping')
              : 'Processing order'))
          : (order.status === 'shipped'
            ? 'Order shipped'
            : (order.status === 'delivered'
              ? 'Order delivered'
              : 'Unknown status')))
      }}
    </div>
  `
})
export class OrderStatusComponent {
  @Input({ required: true }) order!: any;

  hasFragileItems(): boolean {
    return this.order.items.some((i: any) => i.fragile);
  }

  hasOversizedItems(): boolean {
    return this.order.items.some((i: any) => i.size === 'oversized');
  }
}
```

**Why violates ENG-3.1:** Template contains deeply nested ternary operators that are nearly impossible to read. Business logic is embedded in the template instead of the component class. Should use a method or pipe to compute the status message, or break into separate components.

---

## VIOLATION: Component Doing Everything

```typescript
// BAD: product-card.component.ts - All logic crammed into component
import { Component, Input, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-product-card',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="product-card">
      <h3>{{ product.name }}</h3>

      <!-- Complex price calculation in template -->
      <p class="price">
        ${{ calculateFinalPrice() }}
      </p>

      <!-- Complex availability logic -->
      <p class="availability">{{ getAvailabilityText() }}</p>

      <!-- Complex button state -->
      <button
        [disabled]="isButtonDisabled()"
        (click)="handleAddToCart()">
        {{ getButtonText() }}
      </button>
    </div>
  `
})
export class ProductCardComponent implements OnInit {
  @Input({ required: true }) product!: any;
  @Input() user!: any;
  @Input() cart!: any;
  @Input() promotions!: any[];

  private inventory: any;

  constructor(private http: HttpClient) {}

  ngOnInit() {
    // Direct HTTP call in component
    this.http.get(`/api/inventory/${this.product.id}`).subscribe(inv => {
      this.inventory = inv;
    });
  }

  calculateFinalPrice(): string {
    // 20+ lines of price calculation logic
    const promo = this.promotions.find(p => p.productId === this.product.id);
    let price = this.product.basePrice;
    if (promo) price -= promo.discount;
    if (this.user.membership === 'gold') price -= this.product.basePrice * 0.1;
    else if (this.user.membership === 'silver') price -= this.product.basePrice * 0.05;
    if (this.cart.items.length > 5) price -= this.product.basePrice * 0.02;
    if (this.product.category === 'electronics' && !this.product.warrantyIncluded) {
      price += 29.99;
    }
    // ... more calculation logic
    return price.toFixed(2);
  }

  getAvailabilityText(): string {
    // 30+ lines of availability logic
    if (this.product.inventory > 0) {
      if (this.product.inventory > 10) return 'In Stock';
      if (this.product.inventory > 5) return `Only ${this.product.inventory} left`;
      if (this.product.preorder) return `${this.product.inventory} left - preorder for more`;
      return `Last ${this.product.inventory}!`;
    }
    if (this.product.preorder) {
      if (this.product.preorderDate) {
        return `Preorder - ships ${new Date(this.product.preorderDate).toLocaleDateString()}`;
      }
      return 'Preorder available';
    }
    if (this.product.restockDate) {
      return `Out of stock - expected ${new Date(this.product.restockDate).toLocaleDateString()}`;
    }
    return 'Out of stock';
  }

  isButtonDisabled(): boolean {
    // Complex disabled state logic
    return (
      (this.product.inventory === 0 && !this.product.preorder) ||
      (this.cart.items.some((i: any) => i.productId === this.product.id) && !this.product.allowMultiple) ||
      (this.user.membership === 'none' && this.product.membersOnly) ||
      (this.product.ageRestricted && (!this.user.verified || this.user.age < 21))
    );
  }

  getButtonText(): string {
    // More complex branching
    if (this.cart.items.some((i: any) => i.productId === this.product.id)) {
      return this.product.allowMultiple ? 'Add Another' : 'In Cart';
    }
    if (this.product.inventory === 0) {
      return this.product.preorder ? 'Preorder Now' : 'Notify Me';
    }
    return 'Add to Cart';
  }

  handleAddToCart(): void {
    // Direct HTTP calls, state management, analytics all mixed
    this.http.post('/api/cart', { productId: this.product.id }).subscribe();
    this.http.post('/api/analytics/event', { type: 'add_to_cart' }).subscribe();
    // ... more logic
  }
}
```

**Why violates ENG-3.1:** Component violates single responsibility principle. Contains direct HTTP calls, complex business logic (pricing, availability, button state), and analytics tracking. Should be split into: PriceService, InventoryService, CartService, and smaller presentation components.

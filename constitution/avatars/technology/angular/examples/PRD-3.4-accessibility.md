---
law_id: PRD-3.4
avatar: angular
---

# PRD-3.4: Accessibility Examples for Angular

## COMPLIANT: Properly Labeled Form with Error Handling

```typescript
// contact-form.component.ts
import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';

interface FormData {
  name: string;
  email: string;
  message: string;
}

@Component({
  selector: 'app-contact-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  template: `
    <div *ngIf="submitted" role="status" aria-live="polite">
      <h2>Thank you for your message!</h2>
      <p>We will get back to you soon.</p>
    </div>

    <form
      *ngIf="!submitted"
      [formGroup]="form"
      (ngSubmit)="onSubmit()"
      aria-describedby="form-instructions">

      <p id="form-instructions" class="sr-only">
        All fields are required. Errors will be announced as you fill out the form.
      </p>

      <div class="form-group">
        <label [attr.for]="nameId">
          Name <span aria-hidden="true">*</span>
          <span class="sr-only">(required)</span>
        </label>
        <input
          [id]="nameId"
          type="text"
          formControlName="name"
          [attr.aria-required]="true"
          [attr.aria-invalid]="form.get('name')?.invalid && form.get('name')?.touched"
          [attr.aria-describedby]="form.get('name')?.invalid && form.get('name')?.touched ? nameErrorId : null"
          autocomplete="name"
        />
        <span
          *ngIf="form.get('name')?.invalid && form.get('name')?.touched"
          [id]="nameErrorId"
          role="alert"
          class="error">
          {{ getErrorMessage('name') }}
        </span>
      </div>

      <div class="form-group">
        <label [attr.for]="emailId">
          Email <span aria-hidden="true">*</span>
          <span class="sr-only">(required)</span>
        </label>
        <input
          [id]="emailId"
          type="email"
          formControlName="email"
          [attr.aria-required]="true"
          [attr.aria-invalid]="form.get('email')?.invalid && form.get('email')?.touched"
          [attr.aria-describedby]="form.get('email')?.invalid && form.get('email')?.touched ? emailErrorId : null"
          autocomplete="email"
        />
        <span
          *ngIf="form.get('email')?.invalid && form.get('email')?.touched"
          [id]="emailErrorId"
          role="alert"
          class="error">
          {{ getErrorMessage('email') }}
        </span>
      </div>

      <div class="form-group">
        <label [attr.for]="messageId">
          Message <span aria-hidden="true">*</span>
          <span class="sr-only">(required)</span>
        </label>
        <textarea
          [id]="messageId"
          formControlName="message"
          rows="5"
          [attr.aria-required]="true"
          [attr.aria-invalid]="form.get('message')?.invalid && form.get('message')?.touched"
          [attr.aria-describedby]="form.get('message')?.invalid && form.get('message')?.touched ? messageErrorId : null"
        ></textarea>
        <span
          *ngIf="form.get('message')?.invalid && form.get('message')?.touched"
          [id]="messageErrorId"
          role="alert"
          class="error">
          {{ getErrorMessage('message') }}
        </span>
      </div>

      <button type="submit" [disabled]="form.invalid">Send Message</button>
    </form>
  `,
  styles: [`
    .sr-only {
      position: absolute;
      width: 1px;
      height: 1px;
      padding: 0;
      margin: -1px;
      overflow: hidden;
      clip: rect(0, 0, 0, 0);
      border: 0;
    }
    .error { color: #d32f2f; font-size: 0.875rem; }
  `]
})
export class ContactFormComponent {
  @Output() formSubmit = new EventEmitter<FormData>();

  // Unique IDs for accessibility
  private idCounter = 0;
  nameId = `name-${++this.idCounter}`;
  nameErrorId = `name-error-${this.idCounter}`;
  emailId = `email-${++this.idCounter}`;
  emailErrorId = `email-error-${this.idCounter}`;
  messageId = `message-${++this.idCounter}`;
  messageErrorId = `message-error-${this.idCounter}`;

  form: FormGroup;
  submitted = false;

  private errorMessages: Record<string, Record<string, string>> = {
    name: { required: 'Name is required' },
    email: { required: 'Email is required', email: 'Invalid email format' },
    message: { required: 'Message is required' }
  };

  constructor(private fb: FormBuilder) {
    this.form = this.fb.group({
      name: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      message: ['', Validators.required]
    });
  }

  getErrorMessage(field: string): string {
    const control = this.form.get(field);
    if (!control?.errors) return '';

    const errorKey = Object.keys(control.errors)[0];
    return this.errorMessages[field]?.[errorKey] ?? 'Invalid input';
  }

  onSubmit(): void {
    if (this.form.valid) {
      this.formSubmit.emit(this.form.value as FormData);
      this.submitted = true;
    }
  }
}
```

**Why compliant:** Uses proper label associations via [attr.for] and [id]. Includes aria-required and aria-invalid attributes. Announces errors using role="alert". Provides autocomplete attributes for browser autofill. Uses unique IDs for form elements. Includes screen reader-only text for required field indicators.

---

## COMPLIANT: Accessible Modal Dialog with CDK

```typescript
// modal.component.ts
import { Component, Input, Output, EventEmitter, OnDestroy, AfterViewInit, ViewChild, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { A11yModule, FocusTrap, FocusTrapFactory } from '@angular/cdk/a11y';
import { PortalModule } from '@angular/cdk/portal';

@Component({
  selector: 'app-modal',
  standalone: true,
  imports: [CommonModule, A11yModule, PortalModule],
  template: `
    <div
      *ngIf="isOpen"
      class="modal-overlay"
      (click)="onOverlayClick($event)"
      (keydown)="onKeyDown($event)">

      <div
        #modalContent
        class="modal-content"
        role="dialog"
        aria-modal="true"
        [attr.aria-labelledby]="titleId"
        tabindex="-1">

        <header class="modal-header">
          <h2 [id]="titleId">{{ title }}</h2>
          <button
            type="button"
            (click)="close()"
            aria-label="Close dialog"
            class="modal-close">
            <span aria-hidden="true">&times;</span>
          </button>
        </header>

        <div class="modal-body">
          <ng-content></ng-content>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .modal-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.5);
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .modal-content {
      background: white;
      border-radius: 8px;
      max-width: 500px;
      width: 90%;
      max-height: 90vh;
      overflow-y: auto;
    }
  `]
})
export class ModalComponent implements AfterViewInit, OnDestroy {
  @Input() isOpen = false;
  @Input() title = '';
  @Output() closed = new EventEmitter<void>();

  @ViewChild('modalContent') modalContent!: ElementRef<HTMLElement>;

  titleId = `modal-title-${Math.random().toString(36).substr(2, 9)}`;

  private focusTrap!: FocusTrap;
  private previousActiveElement: HTMLElement | null = null;

  constructor(private focusTrapFactory: FocusTrapFactory) {}

  ngAfterViewInit(): void {
    if (this.isOpen && this.modalContent) {
      this.initializeFocusTrap();
    }
  }

  ngOnDestroy(): void {
    this.destroyFocusTrap();
  }

  private initializeFocusTrap(): void {
    // Store current focus
    this.previousActiveElement = document.activeElement as HTMLElement;

    // Prevent body scroll
    document.body.style.overflow = 'hidden';

    // Create focus trap
    this.focusTrap = this.focusTrapFactory.create(this.modalContent.nativeElement);
    this.focusTrap.focusInitialElement();
  }

  private destroyFocusTrap(): void {
    document.body.style.overflow = '';

    if (this.focusTrap) {
      this.focusTrap.destroy();
    }

    // Restore focus
    if (this.previousActiveElement) {
      this.previousActiveElement.focus();
    }
  }

  onOverlayClick(event: MouseEvent): void {
    if (event.target === event.currentTarget) {
      this.close();
    }
  }

  onKeyDown(event: KeyboardEvent): void {
    if (event.key === 'Escape') {
      this.close();
    }
  }

  close(): void {
    this.destroyFocusTrap();
    this.closed.emit();
  }
}
```

**Why compliant:** Implements proper ARIA dialog pattern with role="dialog" and aria-modal="true". Uses Angular CDK FocusTrap for focus management. Stores and restores focus on close. Supports keyboard navigation: Escape to close. Uses aria-labelledby for accessible name. Prevents body scroll while open.

---

## COMPLIANT: Accessible Data Table with Sorting

```typescript
// data-table.component.ts
import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

interface Column<T> {
  key: keyof T;
  header: string;
  sortable?: boolean;
}

@Component({
  selector: 'app-data-table',
  standalone: true,
  imports: [CommonModule],
  template: `
    <table [attr.aria-describedby]="descriptionId">
      <caption>
        {{ caption }}
        <span [id]="descriptionId" class="sr-only">
          {{ sortColumn ? 'Sorted by ' + sortColumn + ' ' + sortDirection + '. ' : '' }}
          Use column headers to sort.
        </span>
      </caption>
      <thead>
        <tr>
          <th
            *ngFor="let column of columns"
            scope="col"
            [attr.aria-sort]="sortColumn === column.key ? sortDirection : null">
            <button
              *ngIf="column.sortable; else staticHeader"
              (click)="handleSort(column.key)"
              [attr.aria-label]="getSortAriaLabel(column)">
              {{ column.header }}
              <span *ngIf="sortColumn === column.key" aria-hidden="true">
                {{ sortDirection === 'ascending' ? ' ▲' : ' ▼' }}
              </span>
            </button>
            <ng-template #staticHeader>{{ column.header }}</ng-template>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr *ngFor="let row of sortedData">
          <td *ngFor="let column of columns; let i = index" [attr.headers]="column.key">
            <strong *ngIf="i === 0">{{ row[column.key] }}</strong>
            <ng-container *ngIf="i !== 0">{{ row[column.key] }}</ng-container>
          </td>
        </tr>
      </tbody>
    </table>
  `,
  styles: [`
    .sr-only {
      position: absolute;
      width: 1px;
      height: 1px;
      padding: 0;
      margin: -1px;
      overflow: hidden;
      clip: rect(0, 0, 0, 0);
      border: 0;
    }
    th button {
      background: none;
      border: none;
      cursor: pointer;
      font-weight: bold;
    }
  `]
})
export class DataTableComponent<T extends { id: string }> {
  @Input() data: T[] = [];
  @Input() columns: Column<T>[] = [];
  @Input() caption = '';

  sortColumn: keyof T | null = null;
  sortDirection: 'ascending' | 'descending' = 'ascending';
  descriptionId = `table-desc-${Math.random().toString(36).substr(2, 9)}`;

  get sortedData(): T[] {
    if (!this.sortColumn) return this.data;

    return [...this.data].sort((a, b) => {
      const aVal = String(a[this.sortColumn!]);
      const bVal = String(b[this.sortColumn!]);
      const comparison = aVal.localeCompare(bVal);
      return this.sortDirection === 'ascending' ? comparison : -comparison;
    });
  }

  handleSort(column: keyof T): void {
    if (this.sortColumn === column) {
      this.sortDirection = this.sortDirection === 'ascending' ? 'descending' : 'ascending';
    } else {
      this.sortColumn = column;
      this.sortDirection = 'ascending';
    }
  }

  getSortAriaLabel(column: Column<T>): string {
    const base = `Sort by ${column.header}`;
    if (this.sortColumn === column.key) {
      return `${base}, currently ${this.sortDirection}`;
    }
    return base;
  }
}
```

**Why compliant:** Uses semantic table elements with proper structure. Includes caption for table description. Uses scope="col" for header cells and aria-sort for sortable columns. Sort buttons have descriptive aria-labels announcing current state. Visual sort indicators are hidden from screen readers with aria-hidden.

---

## COMPLIANT: Accessible Tab Panel with Keyboard Navigation

```typescript
// tabs.component.ts
import { Component, Input, QueryList, ViewChildren, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';

interface Tab {
  id: string;
  label: string;
  content: string;
}

@Component({
  selector: 'app-tabs',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="tabs">
      <div role="tablist" [attr.aria-label]="ariaLabel" class="tab-list">
        <button
          *ngFor="let tab of tabs; let i = index"
          #tabButton
          role="tab"
          [id]="'tab-' + tab.id"
          [attr.aria-selected]="activeTab === tab.id"
          [attr.aria-controls]="'panel-' + tab.id"
          [tabindex]="activeTab === tab.id ? 0 : -1"
          (click)="selectTab(tab.id)"
          (keydown)="onKeyDown($event, i)"
          [class.active]="activeTab === tab.id">
          {{ tab.label }}
        </button>
      </div>

      <div
        *ngFor="let tab of tabs"
        role="tabpanel"
        [id]="'panel-' + tab.id"
        [attr.aria-labelledby]="'tab-' + tab.id"
        [hidden]="activeTab !== tab.id"
        [tabindex]="0"
        class="tab-panel">
        {{ tab.content }}
      </div>
    </div>
  `,
  styles: [`
    .tab-list { display: flex; gap: 4px; border-bottom: 1px solid #ccc; }
    button[role="tab"] {
      padding: 8px 16px;
      border: none;
      background: #f5f5f5;
      cursor: pointer;
    }
    button[role="tab"].active { background: white; border-bottom: 2px solid #1976d2; }
    .tab-panel { padding: 16px; }
  `]
})
export class TabsComponent {
  @Input() tabs: Tab[] = [];
  @Input() ariaLabel = 'Content tabs';

  @ViewChildren('tabButton') tabButtons!: QueryList<ElementRef<HTMLButtonElement>>;

  activeTab = '';

  ngOnInit(): void {
    if (this.tabs.length > 0) {
      this.activeTab = this.tabs[0].id;
    }
  }

  selectTab(tabId: string): void {
    this.activeTab = tabId;
  }

  onKeyDown(event: KeyboardEvent, index: number): void {
    let newIndex: number;

    switch (event.key) {
      case 'ArrowRight':
        newIndex = (index + 1) % this.tabs.length;
        break;
      case 'ArrowLeft':
        newIndex = (index - 1 + this.tabs.length) % this.tabs.length;
        break;
      case 'Home':
        newIndex = 0;
        break;
      case 'End':
        newIndex = this.tabs.length - 1;
        break;
      default:
        return;
    }

    event.preventDefault();
    const newTab = this.tabs[newIndex];
    this.selectTab(newTab.id);

    // Focus the new tab button
    const buttons = this.tabButtons.toArray();
    buttons[newIndex]?.nativeElement.focus();
  }
}
```

**Why compliant:** Implements WAI-ARIA tabs pattern with proper roles (tablist, tab, tabpanel). Uses aria-selected to indicate active tab. Manages focus with roving tabindex pattern. Supports keyboard navigation: Arrow keys for tabs, Home/End for first/last. Panels are properly associated via aria-controls and aria-labelledby.

---

## VIOLATION: Missing Form Labels and ARIA

```typescript
// BAD: search-form.component.ts - Inaccessible form
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-search-form',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="search-container">
      <!-- No label or aria-label -->
      <input
        type="text"
        placeholder="Search..."
        [(ngModel)]="query"
      />

      <!-- No accessible name for icon button -->
      <button (click)="onSearch()">
        <svg viewBox="0 0 24 24">
          <path d="M15.5 14h-.79l-.28-.27..." />
        </svg>
      </button>

      <!-- Results without live region -->
      <div class="results">
        <div *ngIf="results.length > 0">
          <div *ngFor="let r of results">{{ r }}</div>
        </div>
        <div *ngIf="results.length === 0">No results found</div>
      </div>
    </div>
  `
})
export class SearchFormComponent {
  query = '';
  results: string[] = [];

  onSearch(): void {
    // search implementation
  }
}
```

**Why violates PRD-3.4:** Input has no associated label or aria-label. Placeholder is not a substitute for a label. Button with only an SVG icon has no accessible name. Results are not announced to screen readers because there is no aria-live region.

---

## VIOLATION: Inaccessible Custom Dropdown

```typescript
// BAD: custom-select.component.ts - Broken accessibility
import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';

interface Option {
  value: string;
  label: string;
}

@Component({
  selector: 'app-custom-select',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="custom-select">
      <!-- Using div instead of button, no keyboard support -->
      <div
        class="select-trigger"
        (click)="toggleOpen()">
        {{ getSelectedLabel() }}
        <span class="arrow">▼</span>
      </div>

      <!-- No ARIA roles, no keyboard navigation -->
      <div *ngIf="isOpen" class="options">
        <div
          *ngFor="let option of options"
          class="option"
          [class.selected]="value === option.value"
          (click)="selectOption(option.value)">
          {{ option.label }}
        </div>
      </div>
    </div>
  `
})
export class CustomSelectComponent {
  @Input() options: Option[] = [];
  @Input() value = '';
  @Output() valueChange = new EventEmitter<string>();

  isOpen = false;

  toggleOpen(): void {
    this.isOpen = !this.isOpen;
  }

  selectOption(value: string): void {
    this.valueChange.emit(value);
    this.isOpen = false;
  }

  getSelectedLabel(): string {
    return this.options.find(o => o.value === this.value)?.label ?? 'Select...';
  }
}
```

**Why violates PRD-3.4:** Uses divs with click handlers instead of interactive elements, making it unreachable by keyboard. Missing all ARIA roles (listbox, option). No aria-expanded to indicate open state. No arrow key navigation support. Selected state is only visual, not announced.

---

## VIOLATION: Non-Semantic Interactive Elements

```typescript
// BAD: product-card.component.ts - Click handlers on non-interactive elements
import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-product-card',
  standalone: true,
  imports: [CommonModule],
  template: `
    <!-- Div with click handler - not keyboard accessible -->
    <div
      class="product-card"
      (click)="onSelect.emit(product.id)"
      [style.cursor]="'pointer'">

      <!-- Image without alt text -->
      <img [src]="product.image" />

      <h3>{{ product.name }}</h3>
      <p>{{ product.price | currency }}</p>

      <!-- Span acting as button -->
      <span
        class="add-to-cart-btn"
        (click)="onAddToCart($event)">
        Add to Cart
      </span>
    </div>
  `
})
export class ProductCardComponent {
  @Input() product: any;
  @Output() onSelect = new EventEmitter<string>();
  @Output() addToCart = new EventEmitter<string>();

  onAddToCart(event: Event): void {
    event.stopPropagation();
    this.addToCart.emit(this.product.id);
  }
}
```

**Why violates PRD-3.4:** Uses div with click handler for clickable card, which is not focusable or keyboard accessible. Image has no alt attribute. Uses span styled as button instead of actual button element. No focus indicators. Screen reader users cannot interact with any of these elements.

---

## VIOLATION: Missing Focus Management and Live Regions

```typescript
// BAD: search-results.component.ts - No focus management or announcements
import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-search-results',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div>
      <!-- Loading state not announced -->
      <div *ngIf="loading" class="spinner"></div>

      <!-- Results update not announced -->
      <div class="results-grid">
        <div *ngFor="let r of results" class="result-card">
          {{ r.title }}
        </div>
      </div>

      <!-- Empty state not announced -->
      <div *ngIf="!loading && results.length === 0">
        No results for "{{ query }}"
      </div>
    </div>
  `
})
export class SearchResultsComponent implements OnChanges {
  @Input() query = '';
  @Input() results: any[] = [];
  @Input() loading = false;

  ngOnChanges(changes: SimpleChanges): void {
    // No accessibility considerations when state changes
  }
}
```

**Why violates PRD-3.4:** Loading state is only visual (spinner class) with no accessible text or aria-live announcement. When results change, screen reader users are not informed. Empty state is not announced. Focus is not managed after results load, leaving users disoriented.

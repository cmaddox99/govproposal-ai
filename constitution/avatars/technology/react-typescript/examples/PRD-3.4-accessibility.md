---
law_id: PRD-3.4
avatar: react-typescript
---

# PRD-3.4: Accessibility Examples for React + TypeScript

## COMPLIANT: Properly Labeled Form with Error Handling

```typescript
// ContactForm.tsx
import { useState, useId } from 'react';

interface FormData {
  name: string;
  email: string;
  message: string;
}

interface FormErrors {
  name?: string;
  email?: string;
  message?: string;
}

export function ContactForm({ onSubmit }: { onSubmit: (data: FormData) => void }) {
  const [formData, setFormData] = useState<FormData>({ name: '', email: '', message: '' });
  const [errors, setErrors] = useState<FormErrors>({});
  const [submitted, setSubmitted] = useState(false);

  // Generate unique IDs for accessibility
  const nameId = useId();
  const emailId = useId();
  const messageId = useId();
  const nameErrorId = useId();
  const emailErrorId = useId();
  const messageErrorId = useId();

  const validate = (): boolean => {
    const newErrors: FormErrors = {};
    if (!formData.name.trim()) newErrors.name = 'Name is required';
    if (!formData.email.trim()) newErrors.email = 'Email is required';
    else if (!/\S+@\S+\.\S+/.test(formData.email)) newErrors.email = 'Invalid email format';
    if (!formData.message.trim()) newErrors.message = 'Message is required';
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (validate()) {
      onSubmit(formData);
      setSubmitted(true);
    }
  };

  if (submitted) {
    return (
      <div role="status" aria-live="polite">
        <h2>Thank you for your message!</h2>
        <p>We will get back to you soon.</p>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} noValidate aria-describedby="form-instructions">
      <p id="form-instructions" className="sr-only">
        All fields are required. Errors will be announced as you fill out the form.
      </p>

      <div className="form-group">
        <label htmlFor={nameId}>
          Name <span aria-hidden="true">*</span>
          <span className="sr-only">(required)</span>
        </label>
        <input
          id={nameId}
          type="text"
          value={formData.name}
          onChange={e => setFormData({ ...formData, name: e.target.value })}
          aria-required="true"
          aria-invalid={!!errors.name}
          aria-describedby={errors.name ? nameErrorId : undefined}
          autoComplete="name"
        />
        {errors.name && (
          <span id={nameErrorId} role="alert" className="error">
            {errors.name}
          </span>
        )}
      </div>

      <div className="form-group">
        <label htmlFor={emailId}>
          Email <span aria-hidden="true">*</span>
          <span className="sr-only">(required)</span>
        </label>
        <input
          id={emailId}
          type="email"
          value={formData.email}
          onChange={e => setFormData({ ...formData, email: e.target.value })}
          aria-required="true"
          aria-invalid={!!errors.email}
          aria-describedby={errors.email ? emailErrorId : undefined}
          autoComplete="email"
        />
        {errors.email && (
          <span id={emailErrorId} role="alert" className="error">
            {errors.email}
          </span>
        )}
      </div>

      <div className="form-group">
        <label htmlFor={messageId}>
          Message <span aria-hidden="true">*</span>
          <span className="sr-only">(required)</span>
        </label>
        <textarea
          id={messageId}
          value={formData.message}
          onChange={e => setFormData({ ...formData, message: e.target.value })}
          aria-required="true"
          aria-invalid={!!errors.message}
          aria-describedby={errors.message ? messageErrorId : undefined}
          rows={5}
        />
        {errors.message && (
          <span id={messageErrorId} role="alert" className="error">
            {errors.message}
          </span>
        )}
      </div>

      <button type="submit">Send Message</button>
    </form>
  );
}
```

**Why compliant:** Uses proper label associations via htmlFor/id, includes aria-required and aria-invalid attributes, announces errors using role="alert", provides autocomplete attributes, uses unique IDs via useId(), and includes screen reader-only text for required field indicators.

---

## COMPLIANT: Accessible Modal Dialog

```typescript
// Modal.tsx
import { useEffect, useRef, useCallback } from 'react';
import { createPortal } from 'react-dom';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
}

export function Modal({ isOpen, onClose, title, children }: ModalProps) {
  const modalRef = useRef<HTMLDivElement>(null);
  const previousActiveElement = useRef<HTMLElement | null>(null);

  // Trap focus within modal
  const handleKeyDown = useCallback((e: KeyboardEvent) => {
    if (e.key === 'Escape') {
      onClose();
      return;
    }

    if (e.key !== 'Tab' || !modalRef.current) return;

    const focusableElements = modalRef.current.querySelectorAll<HTMLElement>(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    const firstElement = focusableElements[0];
    const lastElement = focusableElements[focusableElements.length - 1];

    if (e.shiftKey && document.activeElement === firstElement) {
      e.preventDefault();
      lastElement.focus();
    } else if (!e.shiftKey && document.activeElement === lastElement) {
      e.preventDefault();
      firstElement.focus();
    }
  }, [onClose]);

  useEffect(() => {
    if (isOpen) {
      // Store current focus
      previousActiveElement.current = document.activeElement as HTMLElement;

      // Prevent body scroll
      document.body.style.overflow = 'hidden';

      // Focus the modal
      modalRef.current?.focus();

      // Add keyboard listener
      document.addEventListener('keydown', handleKeyDown);
    }

    return () => {
      document.body.style.overflow = '';
      document.removeEventListener('keydown', handleKeyDown);

      // Restore focus when closing
      if (previousActiveElement.current) {
        previousActiveElement.current.focus();
      }
    };
  }, [isOpen, handleKeyDown]);

  if (!isOpen) return null;

  return createPortal(
    <div
      className="modal-overlay"
      onClick={onClose}
      aria-hidden="true"
    >
      <div
        ref={modalRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
        className="modal-content"
        onClick={e => e.stopPropagation()}
        tabIndex={-1}
      >
        <header className="modal-header">
          <h2 id="modal-title">{title}</h2>
          <button
            onClick={onClose}
            aria-label="Close dialog"
            className="modal-close"
          >
            <span aria-hidden="true">&times;</span>
          </button>
        </header>
        <div className="modal-body">
          {children}
        </div>
      </div>
    </div>,
    document.body
  );
}
```

**Why compliant:** Implements proper ARIA dialog pattern with role="dialog" and aria-modal="true". Manages focus: traps focus within modal, stores and restores focus on close. Supports keyboard navigation: Escape to close, Tab trapping. Uses aria-labelledby for accessible name.

---

## COMPLIANT: Accessible Data Table with Sorting

```typescript
// DataTable.tsx
import { useState } from 'react';

interface Column<T> {
  key: keyof T;
  header: string;
  sortable?: boolean;
}

interface DataTableProps<T extends { id: string }> {
  data: T[];
  columns: Column<T>[];
  caption: string;
}

export function DataTable<T extends { id: string }>({
  data,
  columns,
  caption
}: DataTableProps<T>) {
  const [sortColumn, setSortColumn] = useState<keyof T | null>(null);
  const [sortDirection, setSortDirection] = useState<'ascending' | 'descending'>('ascending');

  const handleSort = (column: keyof T) => {
    if (sortColumn === column) {
      setSortDirection(prev => prev === 'ascending' ? 'descending' : 'ascending');
    } else {
      setSortColumn(column);
      setSortDirection('ascending');
    }
  };

  const sortedData = [...data].sort((a, b) => {
    if (!sortColumn) return 0;
    const aVal = String(a[sortColumn]);
    const bVal = String(b[sortColumn]);
    const comparison = aVal.localeCompare(bVal);
    return sortDirection === 'ascending' ? comparison : -comparison;
  });

  return (
    <table aria-describedby="table-description">
      <caption>
        {caption}
        <span id="table-description" className="sr-only">
          {sortColumn
            ? `Sorted by ${String(sortColumn)} ${sortDirection}. `
            : ''}
          Use column headers to sort.
        </span>
      </caption>
      <thead>
        <tr>
          {columns.map(column => (
            <th
              key={String(column.key)}
              scope="col"
              aria-sort={
                sortColumn === column.key
                  ? sortDirection
                  : undefined
              }
            >
              {column.sortable ? (
                <button
                  onClick={() => handleSort(column.key)}
                  aria-label={`Sort by ${column.header}${
                    sortColumn === column.key
                      ? `, currently ${sortDirection}`
                      : ''
                  }`}
                >
                  {column.header}
                  {sortColumn === column.key && (
                    <span aria-hidden="true">
                      {sortDirection === 'ascending' ? ' ▲' : ' ▼'}
                    </span>
                  )}
                </button>
              ) : (
                column.header
              )}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {sortedData.map(row => (
          <tr key={row.id}>
            {columns.map((column, index) => (
              <td
                key={String(column.key)}
                headers={String(column.key)}
              >
                {index === 0 ? (
                  <strong>{String(row[column.key])}</strong>
                ) : (
                  String(row[column.key])
                )}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

**Why compliant:** Uses semantic table elements with proper structure. Includes caption for table description. Uses scope="col" for header cells and aria-sort for sortable columns. Sort buttons have descriptive aria-labels announcing current state. Visual sort indicators are hidden from screen readers with aria-hidden.

---

## COMPLIANT: Accessible Tab Panel

```typescript
// Tabs.tsx
import { useState, useRef, KeyboardEvent } from 'react';

interface Tab {
  id: string;
  label: string;
  content: React.ReactNode;
}

interface TabsProps {
  tabs: Tab[];
  ariaLabel: string;
}

export function Tabs({ tabs, ariaLabel }: TabsProps) {
  const [activeTab, setActiveTab] = useState(tabs[0].id);
  const tabRefs = useRef<Map<string, HTMLButtonElement>>(new Map());

  const handleKeyDown = (e: KeyboardEvent<HTMLButtonElement>, index: number) => {
    let newIndex: number;

    switch (e.key) {
      case 'ArrowRight':
        newIndex = (index + 1) % tabs.length;
        break;
      case 'ArrowLeft':
        newIndex = (index - 1 + tabs.length) % tabs.length;
        break;
      case 'Home':
        newIndex = 0;
        break;
      case 'End':
        newIndex = tabs.length - 1;
        break;
      default:
        return;
    }

    e.preventDefault();
    const newTab = tabs[newIndex];
    setActiveTab(newTab.id);
    tabRefs.current.get(newTab.id)?.focus();
  };

  return (
    <div className="tabs">
      <div
        role="tablist"
        aria-label={ariaLabel}
        className="tab-list"
      >
        {tabs.map((tab, index) => (
          <button
            key={tab.id}
            ref={el => {
              if (el) tabRefs.current.set(tab.id, el);
            }}
            role="tab"
            id={`tab-${tab.id}`}
            aria-selected={activeTab === tab.id}
            aria-controls={`panel-${tab.id}`}
            tabIndex={activeTab === tab.id ? 0 : -1}
            onClick={() => setActiveTab(tab.id)}
            onKeyDown={e => handleKeyDown(e, index)}
            className={activeTab === tab.id ? 'active' : ''}
          >
            {tab.label}
          </button>
        ))}
      </div>
      {tabs.map(tab => (
        <div
          key={tab.id}
          role="tabpanel"
          id={`panel-${tab.id}`}
          aria-labelledby={`tab-${tab.id}`}
          hidden={activeTab !== tab.id}
          tabIndex={0}
          className="tab-panel"
        >
          {tab.content}
        </div>
      ))}
    </div>
  );
}
```

**Why compliant:** Implements WAI-ARIA tabs pattern with proper roles (tablist, tab, tabpanel). Uses aria-selected to indicate active tab. Manages focus with roving tabindex pattern. Supports keyboard navigation: Arrow keys for tabs, Home/End for first/last. Panels are properly associated via aria-controls and aria-labelledby.

---

## VIOLATION: Missing Form Labels and ARIA

```typescript
// BAD: SearchForm.tsx - Inaccessible form
export function SearchForm({ onSearch }: { onSearch: (query: string) => void }) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<string[]>([]);

  return (
    <div className="search-container">
      {/* No label or aria-label */}
      <input
        type="text"
        placeholder="Search..."
        value={query}
        onChange={e => setQuery(e.target.value)}
      />

      {/* No accessible name */}
      <button onClick={() => onSearch(query)}>
        <svg viewBox="0 0 24 24">
          <path d="M15.5 14h-.79l-.28-.27..." />
        </svg>
      </button>

      {/* Results without live region */}
      <div className="results">
        {results.length > 0 ? (
          results.map((r, i) => <div key={i}>{r}</div>)
        ) : (
          <div>No results found</div>
        )}
      </div>
    </div>
  );
}
```

**Why violates PRD-3.4:** Input has no associated label or aria-label, only a placeholder which disappears on focus and is not reliably read by screen readers. Button with only an icon has no accessible name. Results are not announced to screen readers because there is no aria-live region.

---

## VIOLATION: Inaccessible Custom Dropdown

```typescript
// BAD: CustomSelect.tsx - Broken accessibility
export function CustomSelect({
  options,
  value,
  onChange
}: {
  options: { value: string; label: string }[];
  value: string;
  onChange: (value: string) => void;
}) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="custom-select">
      {/* Using div instead of button, no keyboard support */}
      <div
        className="select-trigger"
        onClick={() => setIsOpen(!isOpen)}
      >
        {options.find(o => o.value === value)?.label || 'Select...'}
        <span className="arrow">▼</span>
      </div>

      {/* No ARIA roles, no keyboard navigation */}
      {isOpen && (
        <div className="options">
          {options.map(option => (
            <div
              key={option.value}
              className={`option ${value === option.value ? 'selected' : ''}`}
              onClick={() => {
                onChange(option.value);
                setIsOpen(false);
              }}
            >
              {option.label}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
```

**Why violates PRD-3.4:** Uses divs with onClick instead of interactive elements, making it unreachable by keyboard. Missing all ARIA roles (listbox, option). No aria-expanded to indicate open state. No arrow key navigation support. Selected state is only visual, not announced.

---

## VIOLATION: Non-Semantic Interactive Elements

```typescript
// BAD: Card.tsx - Click handlers on non-interactive elements
export function ProductCard({ product, onSelect }: ProductCardProps) {
  return (
    // Div with click handler - not keyboard accessible
    <div
      className="product-card"
      onClick={() => onSelect(product.id)}
      style={{ cursor: 'pointer' }}
    >
      {/* Image without alt text */}
      <img src={product.image} />

      <h3>{product.name}</h3>
      <p>${product.price}</p>

      {/* Span acting as button */}
      <span
        className="add-to-cart-btn"
        onClick={e => {
          e.stopPropagation();
          // add to cart
        }}
      >
        Add to Cart
      </span>
    </div>
  );
}
```

**Why violates PRD-3.4:** Uses div with onClick for clickable card, which is not focusable or keyboard accessible. Image has no alt attribute. Uses span styled as button instead of actual button element. No focus indicators. Screen reader users cannot interact with any of these elements.

---

## VIOLATION: Missing Focus Management and Loading States

```typescript
// BAD: SearchResults.tsx - No focus management or live regions
export function SearchResults({ query }: { query: string }) {
  const [results, setResults] = useState<Result[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    fetchResults(query).then(r => {
      setResults(r);
      setLoading(false);
    });
  }, [query]);

  return (
    <div>
      {/* Loading state not announced */}
      {loading && <div className="spinner" />}

      {/* Results update not announced */}
      <div className="results-grid">
        {results.map(r => (
          <div key={r.id} className="result-card">
            {r.title}
          </div>
        ))}
      </div>

      {/* Empty state not announced */}
      {!loading && results.length === 0 && (
        <div>No results for "{query}"</div>
      )}
    </div>
  );
}
```

**Why violates PRD-3.4:** Loading state is only visual (spinner) with no accessible text or aria-live announcement. When results change, screen reader users are not informed. Empty state is not announced. Focus is not managed after results load, leaving users disoriented.

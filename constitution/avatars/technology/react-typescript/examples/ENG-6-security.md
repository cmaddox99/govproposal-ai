---
laws: [ENG-6.1, ENG-6.4, ENG-6.7]
avatar: [react-typescript]
title: Security Laws — React / TypeScript
---

# Security Laws: ENG-6.1, ENG-6.4, ENG-6.7 — React / TypeScript

## ENG-6.1: Security by Design

Never store tokens in `localStorage`. Use protected routes. Sanitize DOM output. Enforce CSP.

```typescript
// auth/RequireAuth.tsx
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from './useAuth';

export function RequireAuth({ children }: { children: JSX.Element }) {
  const { isAuthenticated, hasRole } = useAuth();
  const location = useLocation();
  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }
  return children;
}

// App.tsx — every protected route wrapped
<Route path="/booking-management" element={
  <RequireAuth><BookingManagementPage /></RequireAuth>
} />
<Route path="/admin" element={
  <RequireAuth><AdminPage /></RequireAuth>  // role check inside AdminPage
} />
```

Token storage — use httpOnly cookies (set by BFF/SSR) or short-lived `sessionStorage`:

```typescript
// auth/tokenStore.ts
export const tokenStore = {
  set: (token: string) => sessionStorage.setItem('aa_session', token),
  get: () => sessionStorage.getItem('aa_session'),
  clear: () => sessionStorage.removeItem('aa_session'),
  // ❌ NEVER: localStorage.setItem('token', token)
};
```

Avoid `dangerouslySetInnerHTML` with unescaped content:

```typescript
// ❌ XSS vulnerability — userContent from API may contain <script>
<div dangerouslySetInnerHTML={{ __html: userContent }} />

// ✅ Sanitize with DOMPurify first, or use a text-only renderer
import DOMPurify from 'dompurify';
<div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(userContent) }} />
```

Next.js CSP header config:

```typescript
// next.config.ts
const securityHeaders = [
  { key: 'Content-Security-Policy',
    value: "default-src 'self'; script-src 'self'; object-src 'none'" },
  { key: 'X-Frame-Options', value: 'DENY' },
];
export default { async headers() { return [{ source: '/(.*)', headers: securityHeaders }]; } };
```

## ENG-6.4: Data Protection

No PII in Redux state that gets persisted. No PII in URL params. Strip sensitive data before Sentry.

```typescript
// store/bookingSlice.ts
interface BookingState {
  flightId: string;
  seatCode: string;
  correlationId: string;
  // ✅ No passengerName, email, cardNumber in Redux state
}

// TypeScript discriminated union enforces classification at compile time
type DataClassification = 'public' | 'internal' | 'sensitive' | 'pii';

interface ClassifiedValue<T, C extends DataClassification> {
  value: T;
  classification: C;
}

// PII fields must be wrapped — prevents accidental Redux persistence
type PassengerEmail = ClassifiedValue<string, 'pii'>;
```

Strip card data from Sentry error boundary:

```typescript
import * as Sentry from '@sentry/react';

Sentry.init({
  beforeSend(event) {
    // Remove any extras that may contain payment or PII data
    if (event.extra) {
      delete event.extra['cardNumber'];
      delete event.extra['passengerEmail'];
    }
    return event;
  },
});
```

PII must never appear in URL query params:

```typescript
// ❌ PII in URL — appears in server logs, analytics, browser history
navigate(`/rebook?email=john@example.com&pnr=ABC123`);

// ✅ Use POST body or route state
navigate('/rebook', { state: { bookingId } });
```

## ENG-6.7: Audit Trail

Capture correlation ID from backend response headers and attach to every audit log entry.

```typescript
// api/apiClient.ts
export async function apiPost<T>(url: string, body: unknown): Promise<{ data: T; correlationId: string }> {
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  const correlationId = res.headers.get('X-Correlation-ID') ?? '';
  const data: T = await res.json();
  return { data, correlationId };
}

// audit/auditLogger.ts
interface AuditEntry {
  event: string;
  correlationId: string;
  timestamp: string;
  screenName: string;
  // ❌ No passengerName, email, cardNumber
}

export async function logAuditEvent(entry: AuditEntry): Promise<void> {
  await fetch('/api/audit/client-events', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(entry),
  });
  // ❌ NEVER: console.log(JSON.stringify(apiResponse)) in production
}
```

## Anti-Patterns

1. **`localStorage.setItem("token", jwt)`** — localStorage persists across browser sessions and is accessible via XSS; use `sessionStorage` or httpOnly cookies.
2. **PII in Redux DevTools-visible state** — Redux DevTools exposes the full store in the browser; any passenger name, email, or card number in state is visible to any developer running the app.
3. **`dangerouslySetInnerHTML` with unescaped user content** — API-sourced flight descriptions or itinerary notes may contain injected `<script>` tags; always sanitize with DOMPurify.
4. **`console.log(apiResponse)` in production** — booking API responses contain PNR, passenger name, seat assignment, and price breakdown; production builds must have `console.log` removed (via Vite/Webpack `drop_console`).
5. **PII in URL query params** — `?pnr=ABC123&email=john@aa.com` appears in server access logs, CDN logs, browser history, and analytics platforms.

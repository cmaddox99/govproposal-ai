# ENG-6.5 — Input Validation · Node.js/TypeScript

**AA Reference — FLIFO-BFF validation middleware** uses data-driven rules — good OCP pattern. Adding a new field = adding to the `validationRules` object, no code change.

```typescript
// AA FLIFO-BFF pattern — data-driven validation rules
const validationRules: ValidationRule[] = [
  { field: 'flightNumber', required: true, pattern: /^[A-Z]{2}\d{1,4}$/ },
  { field: 'departureDate', required: true, validator: isISODate },
  { field: 'origin', required: false, pattern: /^[A-Z]{3}$/ },
];

// Middleware applies rules uniformly — no per-field if/else
export function validateRequest(rules: ValidationRule[]): RequestHandler {
  return (req, res, next) => {
    const errors = rules
      .filter(r => r.required && !req.query[r.field])
      .map(r => ({ field: r.field, error: 'required' }));
    if (errors.length) return res.status(400).json({ errors });
    next();
  };
}
```

**AA OCP violation to avoid (FLIFO-BFF `getCountryCode`):**

```typescript
// BAD — adding a country requires modifying this function
function getCountryCode(country: string): string {
  if (country === 'US') return '+1';
  if (country === 'ES') return '+34';
  if (country === 'UK') return '+44';
  return '+1'; // silent default
}

// FIX — data-driven lookup
const COUNTRY_CODES: Record<string, string> = { US: '+1', ES: '+34', UK: '+44' };
const getCountryCode = (c: string): string => COUNTRY_CODES[c] ?? '+1';
```

**HARD_BLOCK:** Never use `any` for `validatedQuery` — define a per-endpoint request interface.

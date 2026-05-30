---
laws: [ENG-6.1, ENG-6.4, ENG-6.7]
avatar: [angular]
title: Security Laws — Angular
---

# Security Laws: ENG-6.1, ENG-6.4, ENG-6.7 — Angular

## ENG-6.1: Security by Design

Protect every route and HTTP call from the first commit. Never ship an admin or booking route without an `AuthGuard`.

```typescript
// auth.guard.ts
@Injectable({ providedIn: 'root' })
export class AuthGuard implements CanActivate {
  constructor(private auth: AuthService, private router: Router) {}
  canActivate(route: ActivatedRouteSnapshot): boolean {
    if (!this.auth.isAuthenticated()) {
      this.router.navigate(['/login']);
      return false;
    }
    const required = route.data['roles'] as string[];
    return required ? this.auth.hasAnyRole(required) : true;
  }
}

// app-routing.module.ts
{ path: 'admin/passengers', component: PassengerAdminComponent,
  canActivate: [AuthGuard], data: { roles: ['AGENT', 'SUPERVISOR'] } }
```

Attach JWT via interceptor — never inline in individual services:

```typescript
// jwt.interceptor.ts
@Injectable()
export class JwtInterceptor implements HttpInterceptor {
  constructor(private auth: AuthService) {}
  intercept(req: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    const token = this.auth.getToken(); // reads from sessionStorage, never localStorage
    if (token) {
      req = req.clone({ setHeaders: { Authorization: `Bearer ${token}` } });
    }
    return next.handle(req);
  }
}
```

Add CSP via `index.html` meta tag:

```html
<meta http-equiv="Content-Security-Policy"
  content="default-src 'self'; script-src 'self'; object-src 'none';">
```

## ENG-6.4: Data Protection

| Classification | Example | Rule |
|---|---|---|
| PII | Passenger name, email, PNR | Never store in `localStorage` or `@ngrx/store` slices that persist |
| Sensitive | JWT token, seat upgrade payment | `sessionStorage` only; cleared on window close |
| Internal | Flight numbers, gate info | May appear in component state |
| Public | Airport codes, schedule | No restriction |

```typescript
// ❌ NEVER: exposes token to XSS
localStorage.setItem('aa_jwt', token);

// ✅ CORRECT: sessionStorage with short expiry
sessionStorage.setItem('aa_session', token);
// Or prefer httpOnly cookie set by SSR/BFF layer

// Strip PII before logging errors
@Injectable()
export class ErrorInterceptor implements HttpInterceptor {
  intercept(req: HttpRequest<unknown>, next: HttpHandler) {
    return next.handle(req).pipe(
      catchError((err: HttpErrorResponse) => {
        // Log safe fields only — never log Authorization header or request body
        this.logger.error('HTTP error', { status: err.status, url: err.url });
        return throwError(() => err);
      })
    );
  }
}
```

Never place passenger names, emails, or PNR numbers in URL query params:

```typescript
// ❌ NEVER
this.router.navigate(['/booking'], { queryParams: { pnr: 'ABC123', email: 'j.doe@example.com' } });

// ✅ CORRECT: pass via resolver/state
this.router.navigate(['/booking', bookingId]);
```

## ENG-6.7: Audit Trail

Capture the correlation ID returned by the AA API gateway and propagate it through every subsequent request and log entry:

```typescript
// correlation.interceptor.ts
@Injectable()
export class CorrelationInterceptor implements HttpInterceptor {
  intercept(req: HttpRequest<unknown>, next: HttpHandler) {
    return next.handle(req).pipe(
      tap(event => {
        if (event instanceof HttpResponse) {
          const tid = event.headers.get('X-Correlation-ID');
          if (tid) this.correlationService.setTid(tid);
        }
      })
    );
  }
}
```

Log navigation and booking events with correlation ID — never log form field values:

```typescript
// audit-logger.service.ts
logUserAction(event: string, metadata: Record<string, string>): void {
  this.logger.info({
    event,
    correlationId: this.correlationService.getTid(),
    timestamp: new Date().toISOString(),
    ...metadata
    // ❌ NEVER include: passengerName, email, cardNumber
  });
}

// Usage in booking component
this.auditLogger.logUserAction('SEAT_SELECTED', { flightId, seatCode });
```

## Anti-Patterns

1. **JWT in `localStorage`** — XSS can steal the token. Use `sessionStorage` or httpOnly cookies.
2. **Logging full form payloads** — `console.log(this.bookingForm.value)` leaks card numbers, PNR, and passenger PII into browser DevTools and log aggregators.
3. **Hardcoding API keys in `environment.ts`** — `environment.ts` is committed to Git. Use runtime injection via `APP_INITIALIZER` fetching config from a secure endpoint.
4. **Bypassing Angular XSS protection** — `this.sanitizer.bypassSecurityTrustHtml(userContent)` without explicit sanitization opens stored-XSS on passenger-facing pages. Never trust HTML from API responses.
5. **Unguarded admin routes** — omitting `canActivate: [AuthGuard]` on `/admin` routes allows unauthenticated access; Angular's router does not protect routes by default.

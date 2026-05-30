# ENG-4.1 — Atomic TDD · Node.js/TypeScript

**AA Fleet Reality:** `mobile-platform-bff` 100% statement/branch/function/line coverage — the only repo in the AA BFF fleet at 100%. `Mobile-FLIFO-BFF` at 93% line / 80% branch. `mobile-cache-ms` at 80% line / **59% branch** (below ENG-4.1 threshold).

## AA Pattern — Express route test with Supertest

```typescript
// AA BFF standard: Jest + Supertest, not Vitest
describe('GET /flightStatus/v2.0', () => {
  it('should return 400 when appVersion header missing', async () => {
    const res = await request(app).get('/flightStatus/v2.0').expect(400);
    expect(res.body.errorCode).toBe('MISSING_APP_VERSION');
  });

  it('should return flight status with requestId in response', async () => {
    mockFlightStatusService.mockResolvedValueOnce(buildMockFlight());
    const res = await request(app)
      .get('/flightStatus/v2.0')
      .set('x-app-version', '6.0.0')
      .set('x-request-id', 'test-req-123')
      .expect(200);
    expect(res.body.requestId).toBe('test-req-123');
  });
});
```

## What kills branch coverage in AA TS repos

| Pattern | Repo | Branch miss |
|---|---|---|
| `x !== undefined && x !== null` (20+ locations) | FLIFO-BFF | 2 branches each |
| `if (cloudProvider === 'Azure')` without test for IBM path | cache-ms | Critical miss |
| env-switching `if (env === 'non-prod')` chains | FLIFO-BFF | 4-branch miss |
| `try/catch` with only happy-path test | cache-ms | catch branch uncovered |

**HARD_BLOCK:** Coverage < 90% on any new TypeScript BFF file. Branch coverage is not optional — `mobile-cache-ms` at 59% branch is a BLOCKING debt.

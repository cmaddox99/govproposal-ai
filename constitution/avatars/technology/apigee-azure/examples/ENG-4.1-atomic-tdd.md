---
avatar: avatar-tech-apigee-azure
law: ENG-4.1
title: "Atomic TDD Law"
---

# ENG-4.1 — Atomic TDD Law: Apigee + Azure

**One failing test before one line of implementation. Red → Green → Refactor on every layer.**

---

## Layer 1 — Apigee Proxy (JavaScript + Mocha)

```javascript
// RED — test/biometrics-proxy.test.js
it('should reject requests without OAuth token', async () => {
  const res = await apigeeTest.sendRequest({
    proxy: 'ct-bioentexit-biometrics-apigee',
    verb: 'GET', path: '/v1/biometrics/status',
    headers: {}  // no Authorization header
  });
  assert.equal(res.status, 401);
  assert.equal(res.body.code, 'oauth.v2.InvalidAccessToken');
});

// GREEN — add OAuthV2 VerifyAccessToken to proxy PreFlow
// REFACTOR — extract to shared flow SF-AuthEnforcement once 2+ proxies need it
```

**Rule:** One proxy = one test file. Shared flow changes require tests in all consumer proxies.

---

## Layer 2 — Terraform Module (checkov + tflint)

```hcl
# RED — checkov policy: CKV_AZURE_4 (Key Vault soft-delete enabled)
# Running: checkov -d ./modules/keyvault
# Expected: PASSED check: CKV_AZURE_4

# WRONG (causes test to fail):
resource "azurerm_key_vault" "gate_mgmt" {
  soft_delete_retention_days = 0  # ❌ fails CKV_AZURE_4
}

# GREEN (test passes):
resource "azurerm_key_vault" "gate_mgmt" {
  soft_delete_retention_days = 90
  purge_protection_enabled   = true
}
```

**Rule:** `terraform validate + tflint + checkov` must pass in CI before any `terraform plan` runs.

---

## Layer 3 — Azure Function (TypeScript / Jest)

```typescript
// RED — src/__tests__/process-biometric-event.test.ts
it('processes biometric match event and marks as processed', async () => {
  const store = createMockStore();
  const handler = createBiometricEventHandler(store);
  const event: BiometricMatchEvent = {
    eventId: 'evt-001', flightId: 'AA-123',
    gateId: 'DFW-A15', matchResult: 'MATCH', timestamp: new Date()
  };

  await handler.run(event);

  expect(store.markProcessed).toHaveBeenCalledWith('evt-001');
  expect(store.audit).toHaveBeenCalledWith(expect.objectContaining({
    eventId: 'evt-001', matchResult: 'MATCH'
  }));
});

// GREEN — implement handler; use store.existsAsync for idempotency gate
// REFACTOR — extract event validation to shared validator used across all Function handlers
```

**Rule:** Never test the Azure Functions runtime — test the handler logic with a mock context.

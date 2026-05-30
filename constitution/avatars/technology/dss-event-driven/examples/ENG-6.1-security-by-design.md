---
avatar: avatar-tech-dss-event-driven
law: ENG-6.1
title: "Security by Design Law"
---

# ENG-6.1 — Security by Design Law: DSS Event-Driven

**What this law requires:** Security controls are built into the architecture from day one — not added after the fact. For DSS Event-Driven microservices, this means service-to-service authentication via Azure AD, no shared secrets between services, managed identity for all Azure resource access, and input validation at every event handler boundary.

---

## Service-to-Service Authentication (OAuth 2.0 Client Credentials)

Every microservice authenticates to downstream services using **Azure AD Managed Identity** — no passwords, no shared API keys, no `.env` secrets.

```typescript
// dss-displayhub-flightevent/src/auth/service-auth.ts
import { DefaultAzureCredential } from "@azure/identity";

const credential = new DefaultAzureCredential(); // Uses AKS pod identity — no secrets in code

export async function getServiceBearerToken(scope: string): Promise<string> {
  const tokenResponse = await credential.getToken(scope);
  if (!tokenResponse) {
    throw new Error(`Failed to acquire token for scope: ${scope}`);
  }
  return tokenResponse.token;
}
```

```typescript
// Usage — calling the Gate Assignment Service
const token = await getServiceBearerToken(
  "api://dss-gate-assignment-service/.default"
);
await fetch("https://gate-assignment.dss.aa.internal/api/v1/gates", {
  headers: { Authorization: `Bearer ${token}` },
});
```

---

## No Shared Secrets Between Microservices

**Prohibited patterns (ENG-6.1 violation):**

```typescript
// ❌ NEVER — shared API key in environment variable
const apiKey = process.env.GATE_SERVICE_API_KEY; // violates ENG-6.1

// ❌ NEVER — hardcoded credential
const password = "dssPlatform#2026"; // immediate audit finding
```

**Required pattern — Azure Key Vault via CSI driver:**

```yaml
# k8s/dss-displayhub-flightevent/secretproviderclass.yaml
apiVersion: secrets-store.csi.x-k8s.io/v1
kind: SecretProviderClass
metadata:
  name: dss-flightevent-secrets
  namespace: dss-prod
spec:
  provider: azure
  parameters:
    usePodIdentity: "false"
    clientID: "${MANAGED_IDENTITY_CLIENT_ID}"   # Injected by Helm — not hardcoded
    keyvaultName: "dss-platform-kv-prod"
    objects: |
      array:
        - |
          objectName: dss-servicebus-connection
          objectType: secret
    tenantID: "${AZURE_TENANT_ID}"
```

---

## Input Validation in Event Handlers

All incoming Azure Service Bus messages are validated before processing. Malformed or tampered payloads are rejected with a dead-letter — never processed partially.

```typescript
// dss-displayhub-flightevent/src/handlers/flight-event.handler.ts
import { z } from "zod";

const FlightEventSchema = z.object({
  flightNumber: z.string().regex(/^AA\d{1,4}$/, "Invalid AA flight number format"),
  departureGate: z.string().min(1).max(10),
  eventType: z.enum(["GATE_ASSIGNED", "GATE_CHANGE", "DEPARTURE", "DELAY"]),
  eventTimestamp: z.string().datetime(),
  correlationId: z.string().uuid("Correlation ID must be a valid UUID"),
});

export async function handleFlightEvent(rawMessage: unknown): Promise<void> {
  const parseResult = FlightEventSchema.safeParse(rawMessage);
  if (!parseResult.success) {
    // Dead-letter — do not process malformed event
    throw new Error(`Invalid flight event payload: ${parseResult.error.message}`);
  }
  const event = parseResult.data;
  // Safe to process — schema validated
  await processValidatedEvent(event);
}
```

---

## Managed Identity for Key Vault Access

```typescript
// Never use service principal credentials in application code
// AKS workload identity (Managed Identity) is the only accepted pattern

import { SecretClient } from "@azure/keyvault-secrets";
import { DefaultAzureCredential } from "@azure/identity";

const vaultUrl = process.env.KEY_VAULT_URL; // Injected by Helm/k8s — not hardcoded
const client = new SecretClient(vaultUrl!, new DefaultAzureCredential());

export async function getConnectionString(secretName: string): Promise<string> {
  const secret = await client.getSecret(secretName);
  return secret.value!;
}
```

---

## Security Checklist (ENG-6.1)

| Control | Implementation | Status |
|---------|---------------|--------|
| Service authentication | Azure AD Managed Identity + OAuth 2.0 client credentials | Required |
| No shared secrets | Zero API keys between services; Key Vault CSI driver only | Required |
| Input validation | Zod schema at every event handler entry point | Required |
| No plaintext credentials | No `.env` files committed; no hardcoded passwords | Required |
| Network segmentation | AKS NetworkPolicy — services only accept traffic from named peers | Required |
| TLS everywhere | All inter-service HTTP enforces TLS 1.2+ via AKS ingress | Required |

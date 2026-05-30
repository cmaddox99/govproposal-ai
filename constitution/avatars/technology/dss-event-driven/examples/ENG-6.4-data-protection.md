---
avatar: avatar-tech-dss-event-driven
law: ENG-6.4
title: "Data Protection Law"
---

# ENG-6.4 — Data Protection Law: DSS Event-Driven

**All secrets via Azure Key Vault CSI driver in AKS. No .env files committed. No plaintext credentials.**

---

## AKS — Key Vault CSI Driver (Production Pattern)

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
    useVMManagedIdentity: "true"
    userAssignedIdentityID: ""  # empty = system-assigned
    keyvaultName: kv-gate-mgmt-prod
    objects: |
      array:
        - |
          objectName: dss-postgres-connection-string
          objectType: secret
        - |
          objectName: dss-redis-connection-string
          objectType: secret
        - |
          objectName: dss-servicebus-connection-string
          objectType: secret
    tenantId: ${AZURE_TENANT_ID}
  secretObjects:
    - secretName: dss-flightevent-secrets
      type: Opaque
      data:
        - objectName: dss-postgres-connection-string
          key: POSTGRES_CONNECTION_STRING
```

```yaml
# Deployment uses the secret — mounted as env var from K8s Secret (Key Vault backed)
env:
  - name: POSTGRES_CONNECTION_STRING
    valueFrom:
      secretKeyRef:
        name: dss-flightevent-secrets
        key: POSTGRES_CONNECTION_STRING
```

---

## What Never Gets Committed

```
.env                     ❌ Never committed — add to .gitignore
.env.local               ❌ Never committed
docker-compose.override.yml with real secrets  ❌
k8s/*-secret.yaml with base64 values  ❌  (use SecretProviderClass instead)
```

---

## CI/CD — Pipeline Secrets vs. App Runtime

```yaml
# GitHub Actions: pipeline credentials only (deploy service principal)
env:
  AZURE_CLIENT_ID: ${{ secrets.AZURE_CLIENT_ID }}  # deploy SP — not app runtime

# App runtime: NEVER uses GitHub Actions secrets — always Key Vault via AKS CSI
```

---

## Acceptance Criteria
- [ ] All DSS deployments use `SecretProviderClass` — no raw Kubernetes Secret YAML in repo
- [ ] `git-secrets` pre-commit hook active in all DSS repos — blocks credential patterns
- [ ] CI scan (truffleHog or gitleaks) passes on every PR — no secrets in history
- [ ] Pods use Managed Identity for Key Vault access — no client secret in pod spec

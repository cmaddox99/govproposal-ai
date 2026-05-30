---
avatar: avatar-product-gate-management
law: ENG-6.1
title: "Security by Design Law"
---

# ENG-6.1 — Security by Design Law: Gate Management Application

**What this law requires:** Security is designed in from the start. Every identity, access, and data boundary decision is made before implementation begins.

---

## Identity Architecture

| Actor | Identity Provider | Auth | Authorization |
|---|---|---|---|
| Gate Agent | Azure AD | SSO (OIDC) | Role: `gate-agent` |
| Station Manager | Azure AD | SSO + MFA | Role: `station-manager` |
| Biometrics Supervisor | Azure AD | SSO + MFA (required) | Role: `biometrics-supervisor` |
| IT/Platform Engineer | Azure AD | SSO + MFA + PIM | Role: `platform-engineer` |
| Service-to-Service | Azure AD App Registration | OAuth 2.0 client credentials | Scope per service |
| Connect Me Bot | Azure Bot Framework + AAD | App registration token | Bot scope only |

---

## Role Access Rules — Non-Negotiable

### gate-agent
- ✅ View GIDS/FIDS display data, run carry-on check, initiate biometric boarding session
- ❌ Override carry-on decision (requires `station-manager` token)
- ❌ Change biometric match threshold (requires `biometrics-supervisor` with MFA)
- ❌ Access audit logs (requires `platform-engineer`)

### biometrics-supervisor
- ✅ All gate-agent permissions + biometric match dashboard + threshold change (triggers CBP notification)
- ❌ Access raw biometric templates (CBP restricted — system-only)
- ❌ Suppress opt-out UI (hard-coded — not role-accessible)

**MFA mandatory** for all supervisor/manager operations. Session timeout: 4 hours.

---

## Service-to-Service Security

```
Apigee → biometrics-api         OAuth 2.0 client credentials  scope: biometrics.boarding
Apigee → carryon-api            OAuth 2.0 client credentials  scope: carryon.compliance
DisplayHub → Display APIs       OAuth 2.0 client credentials  scope: dss.read
Connect Me Bot → Teams Graph    Azure AD managed identity      scope: Channel.Message.Send
All services → Key Vault        Managed Identity               role: Key Vault Secrets User
```

No shared secrets between services. Each service has its own app registration.

---

## Acceptance Criteria
- [ ] Agent endpoints return 403 when called with token missing `gate-agent` role
- [ ] Carry-on override blocked at API level without valid supervisor authorization token
- [ ] Threshold change blocked without MFA claim in supervisor token
- [ ] All service-to-service calls authenticated (invalid token returns 401 — integration test)
- [ ] No service using client secrets for Azure resource access (Managed Identity only)

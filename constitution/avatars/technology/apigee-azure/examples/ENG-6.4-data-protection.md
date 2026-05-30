---
avatar: avatar-tech-apigee-azure
law: ENG-6.4
title: "Data Protection Law"
codebase_source: "AAInternal/apigeeDocs"
---

# ENG-6.4 — Data Protection Law: Apigee + Azure

**Developer app credentials in HashiCorp Vault. Runtime secrets in Azure Key Vault. No plaintext anywhere.**

## Two Vault Tiers at AA

| Secret Type | Store | How |
|---|---|---|
| Developer app client ID + secret | **HashiCorp Vault** | Auto-stored by Runway on app creation |
| Runtime secrets (Service Bus, DB) | **Azure Key Vault** | `@Microsoft.KeyVault(SecretUri=...)` reference |
| EDGEMICRO_KEY / EDGEMICRO_SECRET | **HashiCorp Vault** | Requested from DataMovement team, stored in Vault |

---

## HashiCorp Vault — Developer App Credentials (AA Required)

Before creating a developer app, a **HashiCorp Vault namespace** must exist:

```bash
# Create namespace via: https://developer.aa.com/secret-vault/create-namespace
# Runway stores generated client ID + secret automatically at:
# vault/data/<squad>/<app-name>/apigee-credentials
```

**Never hardcode or copy client credentials** — always retrieve from Vault path at runtime.

---

---

## Apigee — KVM for Environment Config

```javascript
// WRONG — hardcoded backend URL
<TargetEndpoint name="BiometricsBackend">
  <HTTPTargetConnection>
    <URL>https://biometrics-api-prod.azurewebsites.net</URL>  <!-- never hardcode -->
  </HTTPTargetConnection>
</TargetEndpoint>

// CORRECT — Target Server (configured per environment)
<TargetEndpoint name="BiometricsBackend">
  <HTTPTargetConnection>
    <LoadBalancer>
      <Server name="biometrics-api"/>  <!-- name resolves via Target Server config -->
    </LoadBalancer>
  </HTTPTargetConnection>
</TargetEndpoint>
```

**KVM entries are not committed to VCS** — provisioned via Apigee Management API in CI/CD only.

---

## Azure Functions — Key Vault Reference Syntax

```hcl
# Terraform — CORRECT: Key Vault reference, not plaintext
resource "azurerm_linux_function_app" "biometrics_processor" {
  app_settings = {
    "ServiceBusConnectionString" = "@Microsoft.KeyVault(SecretUri=${azurerm_key_vault_secret.sb_conn.id})"
    "BiometricsDbPassword"       = "@Microsoft.KeyVault(SecretUri=${azurerm_key_vault_secret.db_pass.id})"
  }
}

# WRONG — never do this
resource "azurerm_linux_function_app" "biometrics_processor" {
  app_settings = {
    "BiometricsDbPassword" = "my-actual-password"  # BLOCKING violation
  }
}
```

---

## Terraform — No Secrets in State or VCS

```hcl
# WRONG — secret as variable in .tfvars (never commit)
variable "db_password" { default = "my-password" }  # ❌

# CORRECT — read from Key Vault at plan time
data "azurerm_key_vault_secret" "db_password" {
  name         = "biometrics-db-password"
  key_vault_id = azurerm_key_vault.gate_mgmt.id
}
```

**Remote state** must use Azure Blob with OIDC authentication — no stored credentials for state access.

---

## Acceptance Criteria
- [ ] `git-secrets` pre-commit hook blocks credential patterns (configured in all gate-mgmt repos)
- [ ] checkov `CKV_AZURE_131` passing — no plaintext secrets in Function app settings
- [ ] KVM provisioning script uses Apigee Management API (not committed to proxy bundle)
- [ ] `terraform output` does not expose sensitive values (marked `sensitive = true`)

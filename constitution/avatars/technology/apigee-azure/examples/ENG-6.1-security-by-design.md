---
avatar: avatar-tech-apigee-azure
law: ENG-6.1
title: "Security by Design Law"
---

# ENG-6.1 — Security by Design Law: Apigee + Azure

**Every inbound request authenticated at Apigee. Every Azure service call authenticated via Managed Identity.**

---

## Apigee — OAuthV2 on Every Proxy PreFlow

```xml
<!-- Required on EVERY proxy — no exceptions -->
<PreFlow name="PreFlow">
  <Request>
    <Step>
      <Name>OAuthV2-VerifyAccessToken</Name>
    </Step>
    <Step>
      <Name>SpikeArrest-Default</Name>
    </Step>
  </Request>
</PreFlow>

<!-- OAuthV2 policy -->
<OAuthV2 name="OAuthV2-VerifyAccessToken">
  <Operation>VerifyAccessToken</Operation>
  <!-- On failure: returns 401 with oauth.v2.InvalidAccessToken -->
</OAuthV2>
```

**Never create a proxy without OAuthV2 in PreFlow.** HTTP trigger Azure Functions behind Apigee are not public APIs — Apigee is the perimeter.

---

## Azure Functions — Managed Identity (No Client Secrets)

```hcl
# Terraform — enable Managed Identity
resource "azurerm_linux_function_app" "biometrics_processor" {
  identity { type = "SystemAssigned" }
}

# Key Vault access for the Function's identity
resource "azurerm_key_vault_access_policy" "biometrics_func" {
  key_vault_id = azurerm_key_vault.gate_mgmt.id
  object_id    = azurerm_linux_function_app.biometrics_processor.identity[0].principal_id
  secret_permissions = ["Get", "List"]  # minimum required — never "Set" unless the function writes secrets
}
```

```csharp
// C# — acquire token via Managed Identity (no credentials in code)
var credential = new DefaultAzureCredential();
var client = new SecretClient(
    new Uri("https://kv-gate-mgmt.vault.azure.net/"),
    credential  // uses Managed Identity automatically in Azure
);
var secret = await client.GetSecretAsync("ServiceBusConnectionString");
```

---

## M2M vs. User Auth — Which to Use

| Pattern | Use when |
|---|---|
| OAuth 2.0 client credentials | Service-to-service (Apigee → backend API) |
| OAuth 2.0 authorization code | User-facing operations (gate agent actions) |
| Managed Identity | Azure service-to-service (Function → Key Vault, Service Bus) |
| Never: BasicAuthentication | Never — blocked by Apigee policy review |
| Never: API key in header | Never for inbound — OAuth client credentials only |

---

## Acceptance Criteria
- [ ] Every proxy has OAuthV2 VerifyAccessToken in PreFlow — verified by proxy scan in CI
- [ ] All Function apps have `identity { type = "SystemAssigned" }` — verified by Terraform checkov
- [ ] No Function app settings contain plaintext credentials — verified by checkov CKV_AZURE_131

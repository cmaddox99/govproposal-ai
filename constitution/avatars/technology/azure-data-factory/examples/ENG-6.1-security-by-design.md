---
law_id: ENG-6.1
avatar: azure-data-factory
---

# ENG-6.1 Security by Design — Azure Data Factory

All ADF Linked Services must authenticate using Azure Managed Identity where possible. When
a connection string is unavoidable, it must be stored in Azure Key Vault and referenced via
a Key Vault reference — never stored inline or as a pipeline parameter default value.

---

## COMPLIANT

### 1. ADF Linked Service — Azure Databricks with Managed Identity (No Credentials Block)

```json
{
  "name": "ls_databricks_prod",
  "type": "Microsoft.DataFactory/factories/linkedservices",
  "properties": {
    "type": "AzureDatabricks",
    "description": "TopML Databricks workspace — MSI authentication, no credentials stored",
    "typeProperties": {
      "domain": {
        "value": "@{linkedService().databricksWorkspaceUrl}",
        "type": "Expression"
      },
      "authentication": "MSI",
      "workspaceResourceId": {
        "value": "@{linkedService().workspaceResourceId}",
        "type": "Expression"
      },
      "newClusterNodeType": "Standard_DS3_v2",
      "newClusterNumOfWorker": "2:8",
      "newClusterVersion": "13.3.x-scala2.12",
      "newClusterSparkConf": {
        "spark.databricks.delta.preview.enabled": "true",
        "spark.sql.adaptive.enabled": "true"
      }
    },
    "parameters": {
      "databricksWorkspaceUrl": { "type": "String" },
      "workspaceResourceId":    { "type": "String" }
    }
  }
}
```

There is **no** `accessToken`, `credential`, or `password` block. The ADF factory's
system-assigned managed identity must be granted the `Contributor` role on the Databricks
workspace resource.

---

### 2. ADF Linked Service — Azure Data Lake Storage Gen2 with Managed Identity

```json
{
  "name": "ls_adls_prod",
  "type": "Microsoft.DataFactory/factories/linkedservices",
  "properties": {
    "type": "AzureBlobFS",
    "description": "TopML ADLS Gen2 — MSI authentication",
    "typeProperties": {
      "url": {
        "value": "@{linkedService().storageAccountUrl}",
        "type": "Expression"
      },
      "accountKey": null,
      "servicePrincipalId": null,
      "tenant": null
    },
    "parameters": {
      "storageAccountUrl": { "type": "String" }
    }
  }
}
```

The `accountKey`, `servicePrincipalId`, and `tenant` fields are explicitly `null`. ADF
uses the managed identity to authenticate — no secret is needed.

---

### 3. Key Vault Reference for Connection Strings That Cannot Use MSI

For legacy SQL Server or third-party JDBC connections where MSI is not supported, use
an Azure Key Vault reference. The secret value never appears in ADF JSON.

```json
{
  "name": "ls_sqlserver_legacy_prod",
  "type": "Microsoft.DataFactory/factories/linkedservices",
  "properties": {
    "type": "SqlServer",
    "description": "Legacy SQL Server — connection string via Key Vault (MSI not supported)",
    "typeProperties": {
      "connectionString": {
        "type": "AzureKeyVaultSecret",
        "store": {
          "referenceName": "ls_keyvault_prod",
          "type": "LinkedServiceReference"
        },
        "secretName": "topml-sqlserver-jdbc-conn",
        "secretVersion": ""
      }
    }
  }
}
```

The Key Vault Linked Service (`ls_keyvault_prod`) itself uses MSI to access Key Vault —
no credentials are stored anywhere in ADF.

```json
{
  "name": "ls_keyvault_prod",
  "properties": {
    "type": "AzureKeyVault",
    "typeProperties": {
      "baseUrl": "https://topml-kv.vault.azure.net/"
    }
  }
}
```

---

### 4. Pipeline Expression Using Key Vault Reference

When a dynamic value (e.g., a JDBC URL with embedded credentials) is needed inside a
pipeline expression:

```
@Microsoft.KeyVault(SecretUri=https://topml-kv.vault.azure.net/secrets/jdbc-conn/)
```

---

## VIOLATION

### Anti-Pattern 1: Linked Service With Inline Password

```json
{
  "name": "ls_databricks_prod",
  "properties": {
    "type": "AzureDatabricks",
    "typeProperties": {
      "domain": "https://adb-9876543210.12.azuredatabricks.net",
      "authentication": "Basic",
      "accessToken": {
        "type": "SecureString",
        "value": "dapi1234abcd5678efgh9012ijklmnopqrstu"
      }
    }
  }
}
```

**Why this violates ENG-6.1:**
- The Databricks personal access token is stored in the ADF ARM template, which is committed
  to the Git repository
- Any developer, CI runner, or tooling with repository read access can extract the token
- Token rotation requires a code change and redeployment
- `SecureString` in ADF JSON is only obscured in the portal UI — it is still readable via
  the ARM template and ADF REST API

---

### Anti-Pattern 2: Connection String With Credentials as Pipeline Parameter Default

```json
{
  "name": "pl_prod_anp_daily",
  "properties": {
    "parameters": {
      "jdbcConnectionString": {
        "type": "string",
        "defaultValue": "Server=EXAMPLE-SQL-SERVER;Database=campaigns;User Id=svc_adf;Password=EXAMPLE-PASSWORD"
      }
    }
  }
}
```

**Why this violates ENG-6.1:**
- The password is stored as the `defaultValue` of a pipeline parameter in plain text
- Pipeline parameter values are visible in the ADF UI to anyone with Data Factory Reader role
- The value is committed to source control in the ARM template
- Pipeline run history records parameter values — the credential is now in audit logs forever

---

### Anti-Pattern 3: Hardcoded Storage Account Key in Dataset

```json
{
  "name": "ds_adls_customer_segments",
  "properties": {
    "type": "Parquet",
    "linkedServiceName": {
      "referenceName": "ls_adls_inline_key",
      "type": "LinkedServiceReference"
    }
  }
},
{
  "name": "ls_adls_inline_key",
  "properties": {
    "type": "AzureBlobStorage",
    "typeProperties": {
      "connectionString": "DefaultEndpointsProtocol=https;AccountName=topmlprodsa;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCD..."
    }
  }
}
```

**Why this violates ENG-6.1:** The storage account key grants full read/write/delete access
to all containers in the storage account. If leaked (e.g., via a public GitHub repository),
all TopML campaign data, model outputs, and customer segments are exposed to exfiltration
or deletion.

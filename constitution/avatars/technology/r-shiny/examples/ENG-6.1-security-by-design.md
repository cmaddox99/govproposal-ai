---
law_id: ENG-6.1
avatar: r-shiny
---

# ENG-6.1 Security by Design — R / Shiny

All credentials and secrets must be injected via environment variables and accessed through
`config::get()`. Shiny must enforce authentication checks with `shiny::req()` before any
data is read or rendered.

---

## COMPLIANT

### 1. config.yml — Secrets From Environment Variables Only

```yaml
# config.yml
default:
  app_title: "TopML Campaign Dashboard"
  cache_ttl_seconds: 300
  azure_tenant_id: "00000000-0000-0000-0000-000000000000"

dev:
  inherits: default
  azure_storage_url: "https://topmldevsa.blob.core.windows.net/campaigns"
  azure_client_id: !expr Sys.getenv("AZURE_CLIENT_ID_DEV")
  azure_client_secret: !expr Sys.getenv("AZURE_CLIENT_SECRET_DEV")

stage:
  inherits: default
  azure_storage_url: "https://topmlstagesa.blob.core.windows.net/campaigns"
  azure_client_id: !expr Sys.getenv("AZURE_CLIENT_ID_STAGE")
  azure_client_secret: !expr Sys.getenv("AZURE_CLIENT_SECRET_STAGE")

prod:
  inherits: default
  azure_storage_url: "https://topmlprodsa.blob.core.windows.net/campaigns"
  azure_client_id: !expr Sys.getenv("AZURE_CLIENT_ID_PROD")
  azure_client_secret: !expr Sys.getenv("AZURE_CLIENT_SECRET_PROD")
```

`!expr Sys.getenv(...)` instructs the `config` package to evaluate the expression at runtime,
reading the value from the process environment. The secret is **never** stored in source code
or `config.yml`.

---

### 2. global.R — Loading Azure Credentials via config::get()

```r
# global.R
library(config)
library(AzureStor)
library(AzureAuth)

cfg <- config::get()   # reads R_CONFIG_ACTIVE to determine environment

# Credentials come exclusively from environment variables via config.yml
storage_container <- AzureStor::blob_container(
  url   = cfg$azure_storage_url,
  token = AzureAuth::get_azure_token(
    resource = "https://storage.azure.com/",
    tenant   = cfg$azure_tenant_id,
    app      = cfg$azure_client_id,
    password = cfg$azure_client_secret
  )
)
```

No secret ever appears as a literal string.

---

### 3. server.R — Authentication Check Before Every Data Operation

```r
# server.R
server <- function(input, output, session) {
  # Retrieve the authenticated user from the Shiny session (set by AAD SSO proxy)
  user <- reactive({
    req(session$user)          # stops execution if session$user is NULL or empty
    session$user
  })

  output$campaign_table <- renderDT({
    req(user())                # re-enforce auth in every output that renders data
    req(input$campaign_id)

    load_campaign_data(storage_container, input$campaign_id)
  })

  output$offer_performance <- renderPlot({
    req(user())                # auth check before every data render
    req(input$campaign_id, input$date_range)

    data <- load_campaign_data(storage_container, input$campaign_id)
    plot_offer_performance(data, input$date_range[1], input$date_range[2])
  })
}
```

`shiny::req()` halts execution silently (returning `NULL` to the output) when any condition
is falsy. This prevents data rendering for unauthenticated sessions.

---

## VIOLATION

### Anti-Pattern 1: Hardcoded Storage Account Key in global.R

```r
# global.R — WRONG
library(AzureStor)

# NEVER do this — connection string with embedded key committed to source control
storage_key <- "DefaultEndpointsProtocol=https;AccountName=topmlprodsa;AccountKey=Eby8vdM02xNOc..."

storage_container <- AzureStor::blob_container(
  url = "https://topmlprodsa.blob.core.windows.net/campaigns",
  key = storage_key
)
```

**Why this violates ENG-6.1:**
- The storage account key is committed to the Git repository, exposing full read/write access
  to production data
- Key rotation requires a code change and redeployment
- Any developer with repository access can exfiltrate all campaign data

---

### Anti-Pattern 2: No Authentication Check Before Rendering Data

```r
# server.R — WRONG
server <- function(input, output, session) {
  output$campaign_table <- renderDT({
    # No req(session$user) — data renders for any unauthenticated request
    load_campaign_data(storage_container, input$campaign_id)
  })

  output$offer_performance <- renderPlot({
    # No auth check — financial offer data exposed without authentication
    data <- load_campaign_data(storage_container, input$campaign_id)
    plot_offer_performance(data, Sys.Date() - 30, Sys.Date())
  })
}
```

**Why this violates ENG-6.1:**
- An unauthenticated HTTP request to the Shiny server triggers `load_campaign_data()`,
  potentially exposing PII and commercial campaign data
- There is no defence-in-depth — if the proxy or SSO layer fails, data is unprotected

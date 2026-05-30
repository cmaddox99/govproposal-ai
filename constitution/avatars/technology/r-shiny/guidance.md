# R / Shiny Avatar Guidance

This guidance specializes the AA Hangar AI Constitution laws for R / Shiny applications on the
topml platform. Follow all conventions defined in `manifest.yaml`.

---

## 1. Business Logic Separation

All business logic **must** be extracted into pure R functions residing in the `R/` directory.
These functions:

- Accept data frames (or vectors / scalars) as inputs
- Return data frames (or scalars) as outputs
- Have **no side effects** — no `input$`, no `reactive()`, no `output$`
- Are independently testable with `testthat`

### Why This Matters

Shiny's reactivity makes server-side code difficult to unit test. By extracting pure functions,
you gain full testability without a running Shiny session.

### Example: Pure KPI Calculation Function

```r
# R/kpi_calculations.R

#' Calculate campaign KPI summary
#'
#' @param campaign_data data.table with columns: impressions, clicks, conversions, revenue
#' @param start_date Date — filter start (inclusive)
#' @param end_date Date — filter end (inclusive)
#' @return data.table with columns: ctr, cvr, roas, total_revenue
calculate_campaign_kpi <- function(campaign_data, start_date, end_date) {
  stopifnot(
    is.data.frame(campaign_data),
    inherits(start_date, "Date"),
    inherits(end_date, "Date"),
    start_date <= end_date
  )

  filtered <- campaign_data[date >= start_date & date <= end_date]

  data.table(
    ctr           = ifelse(sum(filtered$impressions) == 0, 0,
                          sum(filtered$clicks) / sum(filtered$impressions)),
    cvr           = ifelse(sum(filtered$clicks) == 0, 0,
                          sum(filtered$conversions) / sum(filtered$clicks)),
    roas          = ifelse(sum(filtered$revenue) == 0, 0,
                          sum(filtered$revenue) / sum(filtered$ad_spend)),
    total_revenue = sum(filtered$revenue)
  )
}
```

### Anti-Pattern: Logic Inside server.R

```r
# WRONG — untestable, mixed concerns
server <- function(input, output, session) {
  output$kpi_table <- renderTable({
    data <- load_data()                      # side effect
    data <- data[data$date >= input$start_date, ]   # logic mixed with reactive
    data$ctr <- data$clicks / data$impressions      # calculation buried in output
    data
  })
}
```

---

## 2. Azure Blob Storage Integration

Use `AzureStor` for all Azure Blob / ADLS access. Connection tokens come exclusively from
`config::get()` — **never** hardcoded.

### Pattern: `load_campaign_data()` Pure Loader Function

```r
# R/data_loaders.R
library(AzureStor)
library(data.table)
library(config)

#' Load campaign data from Azure Blob Storage
#'
#' @param container AzureStor blob container object
#' @param campaign_id character — validated campaign ID (e.g., "ANP-202501")
#' @return data.table of campaign records
load_campaign_data <- function(container, campaign_id) {
  stopifnot(
    inherits(container, "blob_container"),
    is.character(campaign_id),
    nchar(campaign_id) > 0
  )

  blob_path <- paste0("campaigns/", campaign_id, "/data.parquet")
  tmp_file  <- tempfile(fileext = ".parquet")
  on.exit(unlink(tmp_file))

  AzureStor::download_blob(container, blob_path, tmp_file)
  arrow::read_parquet(tmp_file)
}

#' Initialise Azure Blob container from config
#'
#' Called once in global.R — result passed into modules as a parameter.
#' @return AzureStor blob_container
init_storage_container <- function() {
  cfg <- config::get()
  AzureStor::blob_container(
    url   = cfg$azure_storage_url,
    token = AzureAuth::get_azure_token(
      resource  = "https://storage.azure.com/",
      tenant    = cfg$azure_tenant_id,
      app       = cfg$azure_client_id,
      password  = cfg$azure_client_secret
    )
  )
}
```

### global.R Initialisation

```r
# global.R
library(config)
library(AzureStor)

container <- init_storage_container()   # single shared container handle
```

---

## 3. Config-Based Environment Management

All environment-specific values live in `config.yml`. Switch environments via the
`R_CONFIG_ACTIVE` environment variable.

### config.yml Structure

```yaml
default:
  azure_tenant_id: "00000000-0000-0000-0000-000000000000"
  app_title: "TopML Campaign Dashboard"
  cache_ttl_seconds: 300

dev:
  inherits: default
  azure_storage_url: "https://topmldevsa.blob.core.windows.net/campaigns"
  azure_client_id: !expr Sys.getenv("AZURE_CLIENT_ID_DEV")
  azure_client_secret: !expr Sys.getenv("AZURE_CLIENT_SECRET_DEV")
  log_level: "DEBUG"

stage:
  inherits: default
  azure_storage_url: "https://topmlstagesa.blob.core.windows.net/campaigns"
  azure_client_id: !expr Sys.getenv("AZURE_CLIENT_ID_STAGE")
  azure_client_secret: !expr Sys.getenv("AZURE_CLIENT_SECRET_STAGE")
  log_level: "INFO"

prod:
  inherits: default
  azure_storage_url: "https://topmlprodsa.blob.core.windows.net/campaigns"
  azure_client_id: !expr Sys.getenv("AZURE_CLIENT_ID_PROD")
  azure_client_secret: !expr Sys.getenv("AZURE_CLIENT_SECRET_PROD")
  log_level: "WARN"
```

### Accessing Config Values

```r
# Always use config::get() — never Sys.getenv() directly in app code
cfg <- config::get()
storage_url <- cfg$azure_storage_url

# Or access a specific environment explicitly
prod_url <- config::get("azure_storage_url", config = "prod")
```

### Environment Switching

```bash
# Local dev
R_CONFIG_ACTIVE=dev Rscript app.R

# CI / stage deployment
R_CONFIG_ACTIVE=stage Rscript app.R
```

---

## 4. Shiny Module Pattern

Every discrete UI section **must** be implemented as a Shiny module: a paired
`mod_<name>_ui(id)` + `mod_<name>_server(id, ...)` function.

### Module Skeleton

```r
# modules/mod_campaign_summary.R

#' Campaign Summary Module — UI
#'
#' @param id character namespace id
mod_campaign_summary_ui <- function(id) {
  ns <- NS(id)
  tagList(
    selectInput(ns("campaign_id"), "Campaign", choices = NULL),
    dateRangeInput(ns("date_range"), "Date Range",
                   start = Sys.Date() - 30, end = Sys.Date()),
    DT::DTOutput(ns("kpi_table"))
  )
}

#' Campaign Summary Module — Server
#'
#' @param id character namespace id
#' @param container reactive — AzureStor blob container (passed from parent)
mod_campaign_summary_server <- function(id, container) {
  moduleServer(id, function(input, output, session) {
    # Reactive: fetch data only when campaign_id or date range changes
    campaign_data <- reactive({
      req(input$campaign_id)
      load_campaign_data(container(), input$campaign_id)
    })

    # Reactive: compute KPIs from pure function (testable independently)
    kpi_summary <- reactive({
      req(campaign_data())
      calculate_campaign_kpi(
        campaign_data(),
        start_date = input$date_range[1],
        end_date   = input$date_range[2]
      )
    })

    output$kpi_table <- DT::renderDT({
      kpi_summary()
    }, options = list(pageLength = 25))
  })
}
```

### Wiring Modules in server.R

```r
# server.R — thin orchestration only
server <- function(input, output, session) {
  container_r <- reactive({ container })   # expose shared container as reactive

  mod_campaign_summary_server("summary", container = container_r)
  mod_offer_performance_server("offers",  container = container_r)
  mod_audience_builder_server("audience", container = container_r)
}
```

### Module Communication

Pass shared state between modules via `reactiveValues()` created in server.R:

```r
server <- function(input, output, session) {
  shared <- reactiveValues(
    selected_campaign = NULL,
    date_range        = c(Sys.Date() - 30, Sys.Date())
  )

  mod_campaign_summary_server("summary", container = reactive(container), shared = shared)
  mod_offer_performance_server("offers",  container = reactive(container), shared = shared)
}
```

---

## 5. Reactive Dependency Chain Limits

Keep reactive expressions **focused on a single responsibility**. Complex dependency graphs
cause silent re-execution bugs and make debugging extremely difficult.

### Rules

| Rule | Limit |
|------|-------|
| Max reactive dependencies per `reactive()` | 3 |
| Max lines per `observe()` / `observeEvent()` block | 10 |
| Max nesting depth of reactives | 1 (no nested `reactive({ reactive({ }) })`) |

### Compliant: Single-Responsibility Reactives

```r
# Each reactive does ONE thing
raw_data     <- reactive({ req(input$campaign_id); load_campaign_data(container, input$campaign_id) })
filtered     <- reactive({ req(raw_data()); filter_by_date(raw_data(), input$date_range[1], input$date_range[2]) })
kpi_summary  <- reactive({ req(filtered());  calculate_campaign_kpi(filtered()) })

output$kpi_table <- renderDT({ kpi_summary() })
```

### Violation: Overloaded Reactive

```r
# WRONG — one reactive does everything
output$kpi_table <- renderDT({
  data <- load_campaign_data(container, input$campaign_id)   # dep 1
  data <- data[date >= input$start_date & date <= input$end_date, ]  # dep 2 + 3
  data$ctr <- data$clicks / data$impressions
  if (input$show_roas) data$roas <- data$revenue / data$ad_spend     # dep 4
  data[order(-data$ctr), ]
})
```

---

## 6. Dashboard KPI Data Refresh

For dashboards displaying near-real-time data, use `reactivePoll()` to refresh on a schedule
without blocking the UI.

### Pattern: Scheduled Data Refresh with `reactivePoll()`

```r
# modules/mod_campaign_summary.R
mod_campaign_summary_server <- function(id, container) {
  moduleServer(id, function(input, output, session) {
    # Poll for new data every 5 minutes; checkFunc reads only a lightweight metadata file
    campaign_data <- reactivePoll(
      intervalMillis = 300000,   # 5 minutes
      session        = session,
      checkFunc      = function() {
        # Cheap check: read last-modified timestamp from metadata blob
        meta <- AzureStor::get_blob_properties(container(), "campaigns/last_updated.txt")
        meta$`last-modified`
      },
      valueFunc = function() {
        req(input$campaign_id)
        load_campaign_data(container(), input$campaign_id)
      }
    )

    output$kpi_table <- DT::renderDT({ campaign_data() })
  })
}
```

### Caching Expensive Computations

```r
# Use reactiveValues + timestamp to avoid redundant re-computation
cache <- reactiveValues(data = NULL, loaded_at = NULL)

observe({
  invalidateLater(300000, session)   # re-check every 5 minutes
  now <- Sys.time()
  if (is.null(cache$loaded_at) || difftime(now, cache$loaded_at, units = "secs") > 300) {
    cache$data      <- load_campaign_data(container, input$campaign_id)
    cache$loaded_at <- now
  }
})
```

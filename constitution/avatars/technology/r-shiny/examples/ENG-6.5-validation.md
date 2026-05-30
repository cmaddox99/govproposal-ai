---
law_id: ENG-6.5
avatar: r-shiny
---

# ENG-6.5 Input Validation — R / Shiny

All user-supplied inputs must be validated with `shiny::validate()` + `shiny::need()` before
they are used in data operations. Raw `input$` values must **never** be interpolated directly
into file paths, storage blob paths, SQL queries, or Delta table names.

---

## COMPLIANT

### Campaign ID Validation

```r
output$campaign_table <- renderDT({
  validate(
    need(input$campaign_id, "Please select a campaign"),
    need(
      grepl("^[A-Z]{2,4}-[0-9]{4,6}$", input$campaign_id),
      "Campaign ID format invalid (expected format: ANP-202501)"
    )
  )

  load_campaign_data(container, input$campaign_id)
})
```

`validate()` stops rendering and displays a user-friendly message when any `need()` fails.
The regex `^[A-Z]{2,4}-[0-9]{4,6}$` ensures only valid campaign IDs (e.g., `ANP-202501`,
`TOPML-2025`) reach the storage layer — preventing path traversal attacks.

---

### Date Range Validation

```r
output$offer_performance_chart <- renderPlot({
  validate(
    need(input$date_range,                         "Please select a date range"),
    need(!is.na(input$date_range[1]),              "Start date is invalid"),
    need(!is.na(input$date_range[2]),              "End date is invalid"),
    need(
      input$date_range[1] <= input$date_range[2],
      "Start date must be before end date"
    ),
    need(
      as.numeric(difftime(input$date_range[2], input$date_range[1], units = "days")) <= 366,
      "Date range cannot exceed 366 days"
    )
  )

  data <- load_campaign_data(container, input$campaign_id)
  plot_offer_performance(data, input$date_range[1], input$date_range[2])
})
```

---

### Numeric Range Validation (Budget Threshold Filter)

```r
output$segment_table <- renderDT({
  validate(
    need(is.numeric(input$min_revenue),           "Minimum revenue must be a number"),
    need(input$min_revenue >= 0,                  "Minimum revenue cannot be negative"),
    need(input$min_revenue <= 10000000,           "Minimum revenue exceeds maximum allowed value"),
    need(
      !is.na(input$max_revenue) && input$max_revenue > input$min_revenue,
      "Maximum revenue must be greater than minimum revenue"
    )
  )

  filter_segments_by_revenue(segment_data, input$min_revenue, input$max_revenue)
})
```

---

### Sanitised File Path Construction

```r
# R/data_loaders.R

load_campaign_data <- function(container, campaign_id) {
  # Validate format before constructing any path
  if (!grepl("^[A-Z]{2,4}-[0-9]{4,6}$", campaign_id)) {
    stop(paste("Invalid campaign_id format:", campaign_id))
  }

  # Safe path construction — campaign_id passes regex before use
  blob_path <- paste0("campaigns/", campaign_id, "/data.parquet")
  tmp_file  <- tempfile(fileext = ".parquet")
  on.exit(unlink(tmp_file))

  AzureStor::download_blob(container, blob_path, tmp_file)
  arrow::read_parquet(tmp_file)
}
```

---

## VIOLATION

### Anti-Pattern 1: Raw input$campaign_id Directly in Blob Path (Path Traversal Risk)

```r
# WRONG — no validation before path construction
output$campaign_table <- renderDT({
  # input$campaign_id could be "../../prod-secrets/credentials" or
  # "ANP-202501/../admin-keys/storage.key"
  blob_path <- paste0("campaigns/", input$campaign_id, "/data.parquet")
  tmp <- tempfile()
  AzureStor::download_blob(container, blob_path, tmp)
  arrow::read_parquet(tmp)
})
```

**Why this violates ENG-6.5:** A malicious or malformed `input$campaign_id` value like
`../../prod-secrets/credentials` causes the blob path to traverse outside the intended
`campaigns/` directory, potentially exposing arbitrary blobs in the storage account.

---

### Anti-Pattern 2: Raw input$campaign_id in SQL Query (SQL Injection Risk)

```r
# WRONG — SQL injection via unsanitised Shiny input
output$campaign_metrics <- renderTable({
  conn <- DBI::dbConnect(odbc::odbc(), dsn = "topml_sql")
  on.exit(DBI::dbDisconnect(conn))

  # campaign_id could be: "'; DROP TABLE campaigns; --"
  query <- paste0(
    "SELECT * FROM campaigns WHERE campaign_id = '", input$campaign_id, "'"
  )
  DBI::dbGetQuery(conn, query)
})
```

**Why this violates ENG-6.5:** String interpolation of `input$campaign_id` directly into
SQL allows arbitrary SQL injection. The correct approach is parameterised queries:

```r
# Correct SQL pattern — parameterised query
DBI::dbGetQuery(
  conn,
  "SELECT * FROM campaigns WHERE campaign_id = ?",
  params = list(input$campaign_id)
)
```

---

### Anti-Pattern 3: No Validation in renderDT Leading to R Errors Exposed to Users

```r
# WRONG — no validate() / need() — raw R errors shown to end users
output$campaign_table <- renderDT({
  # If input$campaign_id is NULL or empty, load_campaign_data() throws an
  # unhandled R error that Shiny renders as a red error message containing
  # internal function names and file paths
  load_campaign_data(container, input$campaign_id)
})
```

**Why this violates ENG-6.5:** R stack traces exposed in the UI reveal internal implementation
details (function names, file paths, package versions) that aid attackers in fingerprinting
the application. Use `validate()` to intercept bad input before calling any data function.

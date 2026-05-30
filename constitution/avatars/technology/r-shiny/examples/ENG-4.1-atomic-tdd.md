---
law_id: ENG-4.1
avatar: r-shiny
---

# ENG-4.1 Atomic TDD — R / Shiny

Atomic TDD requires each test to cover exactly **one behaviour** of **one pure function**.
In Shiny apps, this means extracting all business logic into the `R/` directory and testing
those functions with `testthat` — never testing the reactive graph directly.

---

## COMPLIANT — Red → Green → Refactor

### Context

`calculate_campaign_kpi()` is being added to `R/kpi_calculations.R` to compute
click-through rate (CTR) for the TopML Campaign Dashboard.

---

### RED — Write the Failing Test First

```r
# tests/test-kpi_calculations.R
library(testthat)
library(data.table)

# Source the function under test (not yet implemented)
source(here::here("R", "kpi_calculations.R"))

test_that("calculate_campaign_kpi returns zero CTR for empty impressions", {
  empty_data <- data.table(
    date        = as.Date(character(0)),
    impressions = numeric(0),
    clicks      = numeric(0),
    conversions = numeric(0),
    revenue     = numeric(0),
    ad_spend    = numeric(0)
  )

  result <- calculate_campaign_kpi(
    campaign_data = empty_data,
    start_date    = as.Date("2025-01-01"),
    end_date      = as.Date("2025-01-31")
  )

  expect_equal(result$ctr, 0)
})
```

Run the test — it **fails** because `calculate_campaign_kpi` does not exist yet:

```
Error in calculate_campaign_kpi(...) : could not find function "calculate_campaign_kpi"
```

---

### GREEN — Write the Minimal Implementation

```r
# R/kpi_calculations.R

calculate_campaign_kpi <- function(campaign_data, start_date, end_date) {
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

Run test — it **passes**:

```
✔ | 1 passed | test-kpi_calculations.R
```

---

### REFACTOR — Add Type Validation and Additional Tests

```r
# R/kpi_calculations.R (refactored)

#' Calculate campaign KPI summary
#'
#' @param campaign_data data.table with columns: date, impressions, clicks,
#'   conversions, revenue, ad_spend
#' @param start_date Date
#' @param end_date Date
#' @return data.table(ctr, cvr, roas, total_revenue)
calculate_campaign_kpi <- function(campaign_data, start_date, end_date) {
  stopifnot(
    is.data.table(campaign_data),
    all(c("date", "impressions", "clicks", "conversions", "revenue", "ad_spend")
        %in% names(campaign_data)),
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

Additional focused tests (each covers one behaviour):

```r
# tests/test-kpi_calculations.R

test_that("calculate_campaign_kpi computes correct CTR with valid data", {
  campaign_data <- data.table(
    date        = as.Date("2025-01-15"),
    impressions = 1000L,
    clicks      = 50L,
    conversions = 5L,
    revenue     = 500.00,
    ad_spend    = 100.00
  )

  result <- calculate_campaign_kpi(
    campaign_data,
    start_date = as.Date("2025-01-01"),
    end_date   = as.Date("2025-01-31")
  )

  expect_equal(result$ctr, 0.05)
})

test_that("calculate_campaign_kpi errors when start_date is after end_date", {
  campaign_data <- data.table(
    date = as.Date("2025-01-15"), impressions = 100L,
    clicks = 5L, conversions = 1L, revenue = 50.0, ad_spend = 10.0
  )

  expect_error(
    calculate_campaign_kpi(campaign_data,
                           start_date = as.Date("2025-02-01"),
                           end_date   = as.Date("2025-01-01")),
    regexp = "start_date <= end_date"
  )
})

test_that("calculate_campaign_kpi errors when required columns are missing", {
  bad_data <- data.table(date = as.Date("2025-01-15"), impressions = 100L)

  expect_error(
    calculate_campaign_kpi(bad_data,
                           start_date = as.Date("2025-01-01"),
                           end_date   = as.Date("2025-01-31"))
  )
})
```

Run all tests:

```bash
Rscript -e "testthat::test_dir('tests/')"
# ✔ | 4 passed | test-kpi_calculations.R
```

---

## VIOLATION

### Anti-Pattern 1: Testing Entire server.R Behaviour in One shinytest2 Test

```r
# tests/test-app.R — WRONG
test_that("entire dashboard works", {
  app <- AppDriver$new(app_dir = ".")

  # Testing multiple reactive paths in a single test
  app$set_inputs(campaign_id = "ANP-202501")
  app$set_inputs(date_range = c("2025-01-01", "2025-01-31"))
  app$set_inputs(show_roas = TRUE)
  app$set_inputs(audience_segment = "loyalty_gold")
  app$set_inputs(offer_type = "upgrade")

  # One assertion covers 5 different business rules — impossible to isolate failures
  expect_equal(app$get_value(output = "kpi_table")$nrow, 12)
})
```

**Why this violates ENG-4.1:**
- Tests multiple reactive paths simultaneously — a single failure gives no indication of which
  business rule broke
- No unit tests exist for `calculate_campaign_kpi`, `filter_by_segment`, or `load_campaign_data`
- shinytest2 integration tests are slow and require a running Shiny session

### Anti-Pattern 2: No Unit Tests for Business Logic Functions

```r
# server.R — business logic embedded, never tested
server <- function(input, output, session) {
  output$kpi_table <- renderTable({
    data <- readRDS("data/campaigns.rds")
    data <- data[data$campaign_id == input$campaign_id, ]
    data$ctr  <- data$clicks / data$impressions         # untested calculation
    data$roas <- data$revenue / data$ad_spend            # untested calculation
    data
  })
}

# tests/ directory is empty — zero unit tests
```

**Why this violates ENG-4.1:** The business logic for CTR and ROAS calculation exists only
inside a `renderTable()` call. It is never tested. Any regression in the formula is only
caught (if at all) by a developer manually inspecting the dashboard.

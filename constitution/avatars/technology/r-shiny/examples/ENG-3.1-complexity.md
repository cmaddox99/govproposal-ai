---
law_id: ENG-3.1
avatar: r-shiny
---

# ENG-3.1 Complexity Limits — R / Shiny

Shiny reactive graphs grow unmanageable when individual `reactive()` and `observe()` blocks
carry too many responsibilities. Keep each reactive expression focused on a **single concern**,
limit dependencies, and enforce small `observe()` blocks.

| Metric | Limit |
|--------|-------|
| Reactive dependencies per `reactive()` expression | ≤ 3 |
| Lines per `observe()` / `observeEvent()` block | ≤ 10 |
| Nesting depth of reactive expressions | ≤ 1 |
| Lines per module server function | ≤ 60 |

---

## COMPLIANT

### Named Reactives With Single Responsibility

```r
# modules/mod_campaign_summary.R

mod_campaign_summary_server <- function(id, container) {
  moduleServer(id, function(input, output, session) {

    # Step 1 — fetch raw data (depends on: campaign_id only)
    raw_data <- reactive({
      req(input$campaign_id)
      load_campaign_data(container(), input$campaign_id)   # pure function call
    })

    # Step 2 — filter by date (depends on: raw_data, date_range only)
    filtered_data <- reactive({
      req(raw_data(), input$date_range)
      filter_by_date(raw_data(), input$date_range[1], input$date_range[2])
    })

    # Step 3 — compute KPIs (depends on: filtered_data only)
    kpi_summary <- reactive({
      req(filtered_data())
      calculate_campaign_kpi(filtered_data())
    })

    # Output: render from pre-computed reactive (no logic here)
    output$kpi_table <- DT::renderDT({
      kpi_summary()
    }, options = list(pageLength = 25, scrollX = TRUE))

    # observe block: single concern — update campaign selector choices
    observeEvent(input$refresh_campaigns, {
      choices <- list_available_campaigns(container())
      updateSelectInput(session, "campaign_id", choices = choices)
    })

  })
}
```

Each reactive step:
1. Has a descriptive name (`raw_data`, `filtered_data`, `kpi_summary`)
2. Has at most 2–3 upstream dependencies
3. Calls a pure function from `R/` — the logic lives there, not in the reactive

---

### observe() Block Under 10 Lines

```r
# Correct — single-purpose observe block
observeEvent(input$export_csv, {
  req(kpi_summary())
  filename <- paste0("campaign_kpi_", Sys.Date(), ".csv")
  write.csv(kpi_summary(), filename, row.names = FALSE)
  showNotification(paste("Exported:", filename), type = "message")
})
```

---

## VIOLATION

### Anti-Pattern: Single observe() With 25+ Reactive Dependencies

```r
# WRONG — one observe does everything: fetching, filtering, computing, rendering, and logging
observe({
  data <- load_campaign_data(container, input$campaign_id)        # dep 1
  data <- data[data$date >= input$start_date, ]                   # dep 2
  data <- data[data$date <= input$end_date, ]                     # dep 3
  data <- data[data$offer_type %in% input$offer_types, ]          # dep 4
  data <- data[data$segment    %in% input$audience_segments, ]    # dep 5

  if (input$show_roas) {                                          # dep 6
    data$roas <- data$revenue / data$ad_spend
  }
  if (input$show_ctr) {                                           # dep 7
    data$ctr <- data$clicks / data$impressions
  }
  if (input$currency == "GBP") {                                  # dep 8
    data$revenue <- data$revenue * input$fx_rate                  # dep 9
  }

  output$kpi_table   <<- renderDT({ data })
  output$kpi_chart   <<- renderPlot({ plot(data$date, data$ctr) })
  output$revenue_box <<- renderValueBox({ valueBox(sum(data$revenue), "Revenue") })

  log_info(paste("Rendered for user:", session$user,             # dep 10 (side effect)
                 "campaign:", input$campaign_id,
                 "rows:", nrow(data)))
})
```

**Why this violates ENG-3.1:**
- 10+ reactive dependencies mean this block re-executes when *any* input changes — including
  unrelated inputs like `input$currency` triggering a full data reload
- Mixed concerns: data fetching, filtering, KPI computation, output rendering, and logging are
  all collapsed into one block
- Impossible to unit test — logic is inseparable from the reactive context
- A bug in date filtering causes the entire block to fail, masking which rule broke
- Nested `<<-` assignment to `output$` inside `observe()` bypasses Shiny's normal rendering
  lifecycle and causes unpredictable behavior

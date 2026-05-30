---
law_id: ENG-3.1
avatar: data-engineering
---

# ENG-3.1: Complexity Limits Examples for Data Engineering

## COMPLIANT: Small Focused Pipeline Functions

```python
from pyspark.sql import DataFrame
import pyspark.sql.functions as F
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType


def clean_order_timestamps(df: DataFrame) -> DataFrame:
    """Standardize timestamps to UTC.

    Cyclomatic complexity: 1
    """
    return df.withColumn(
        "order_timestamp",
        F.to_utc_timestamp(F.col("order_timestamp"), "America/Chicago")
    )


def filter_valid_orders(df: DataFrame) -> DataFrame:
    """Remove orders with invalid amounts or missing customer IDs.

    Cyclomatic complexity: 1
    """
    return df.filter(
        (F.col("amount") > 0) &
        (F.col("amount") < 1_000_000) &
        F.col("customer_id").isNotNull()
    )


def calculate_order_totals(df: DataFrame) -> DataFrame:
    """Compute line item totals and order-level aggregations.

    Cyclomatic complexity: 1
    """
    return (
        df.withColumn("line_total", F.col("quantity") * F.col("unit_price"))
          .groupBy("order_id", "customer_id", "order_date")
          .agg(
              F.sum("line_total").alias("order_total"),
              F.count("*").alias("item_count"),
              F.max("line_total").alias("max_line_total"),
          )
    )


def enrich_with_customer_segment(
    orders_df: DataFrame,
    customers_df: DataFrame,
) -> DataFrame:
    """Join customer segment information onto orders.

    Cyclomatic complexity: 1
    """
    return orders_df.join(
        customers_df.select("customer_id", "segment", "region"),
        on="customer_id",
        how="left",
    )


def build_daily_order_summary(
    raw_orders: DataFrame,
    customers: DataFrame,
) -> DataFrame:
    """Orchestrate the daily order summary pipeline.

    Each step is a small, testable function.
    Cyclomatic complexity: 1
    """
    return (
        raw_orders
        .transform(clean_order_timestamps)
        .transform(filter_valid_orders)
        .transform(calculate_order_totals)
        .transform(lambda df: enrich_with_customer_segment(df, customers))
    )
```

**Why compliant:** Each function does one thing with cyclomatic complexity of 1. The pipeline is composed of small, independently testable transformations. The orchestrator function reads like a recipe. Adding or removing a step requires changing only one line.

---

## COMPLIANT: dbt Model with Modular CTEs

```sql
-- models/marts/daily_revenue_summary.sql
-- Each CTE is a focused transformation step

WITH valid_orders AS (
    -- Step 1: Filter to valid, completed orders
    SELECT
        order_id,
        customer_id,
        order_date,
        total_amount
    FROM {{ ref('stg_orders') }}
    WHERE status IN ('confirmed', 'shipped', 'delivered')
      AND total_amount > 0
      AND total_amount < 1000000
),

daily_totals AS (
    -- Step 2: Aggregate to daily level
    SELECT
        order_date,
        COUNT(DISTINCT order_id) AS order_count,
        COUNT(DISTINCT customer_id) AS unique_customers,
        SUM(total_amount) AS gross_revenue,
        AVG(total_amount) AS avg_order_value
    FROM valid_orders
    GROUP BY order_date
),

with_moving_averages AS (
    -- Step 3: Add 7-day moving averages
    SELECT
        *,
        AVG(gross_revenue) OVER (
            ORDER BY order_date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS revenue_7d_avg,
        AVG(order_count) OVER (
            ORDER BY order_date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS orders_7d_avg
    FROM daily_totals
)

-- Final output
SELECT
    order_date,
    order_count,
    unique_customers,
    gross_revenue,
    avg_order_value,
    revenue_7d_avg,
    orders_7d_avg
FROM with_moving_averages
ORDER BY order_date
```

**Why compliant:** Each CTE has a single responsibility (filter, aggregate, enrich). The query reads top-to-bottom as a pipeline. Each CTE can be tested independently by selecting from it. No deeply nested subqueries or complex CASE expressions.

---

## COMPLIANT: Focused Validation Functions for Data Quality

```python
from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class ValidationResult:
    is_valid: bool
    errors: tuple[str, ...]

    @staticmethod
    def success() -> "ValidationResult":
        return ValidationResult(is_valid=True, errors=())

    @staticmethod
    def failure(errors: Sequence[str]) -> "ValidationResult":
        return ValidationResult(is_valid=False, errors=tuple(errors))


def validate_schema(df: DataFrame, expected_columns: dict[str, str]) -> ValidationResult:
    """Verify DataFrame has expected columns and types."""
    errors = []
    actual = {field.name: str(field.dataType) for field in df.schema.fields}

    for col_name, col_type in expected_columns.items():
        if col_name not in actual:
            errors.append(f"Missing column: {col_name}")
        elif actual[col_name] != col_type:
            errors.append(f"Column {col_name}: expected {col_type}, got {actual[col_name]}")

    return ValidationResult.failure(errors) if errors else ValidationResult.success()


def validate_no_nulls(df: DataFrame, columns: list[str]) -> ValidationResult:
    """Check that specified columns have no null values."""
    errors = []
    for col in columns:
        null_count = df.filter(F.col(col).isNull()).count()
        if null_count > 0:
            errors.append(f"Column {col} has {null_count} null values")

    return ValidationResult.failure(errors) if errors else ValidationResult.success()


def validate_row_count(df: DataFrame, min_rows: int, max_rows: int) -> ValidationResult:
    """Verify row count is within expected range."""
    count = df.count()
    if count < min_rows:
        return ValidationResult.failure([f"Too few rows: {count} < {min_rows}"])
    if count > max_rows:
        return ValidationResult.failure([f"Too many rows: {count} > {max_rows}"])
    return ValidationResult.success()
```

**Why compliant:** Each validation function checks one thing. Results are returned as immutable value objects. Functions are composable and independently testable. No nested conditionals or complex branching.

---

## VIOLATION: Monolithic ETL Function

```python
def run_daily_etl(spark, config):
    """Monolithic ETL function with cyclomatic complexity > 25.

    This function does EVERYTHING: extraction, validation, transformation,
    aggregation, error handling, and loading in one massive block.
    """
    # Step 1: Read from multiple sources with inline error handling
    try:
        orders_df = spark.read.parquet(config["orders_path"])
    except Exception as e:
        print(f"Failed to read orders: {e}")
        try:
            # Fallback to backup location
            orders_df = spark.read.parquet(config["orders_backup_path"])
        except Exception:
            print("Both order sources failed, using empty DataFrame")
            orders_df = spark.createDataFrame([], orders_schema)

    try:
        customers_df = spark.read.parquet(config["customers_path"])
    except Exception:
        customers_df = spark.createDataFrame([], customers_schema)

    # Step 2: Inline validation with deeply nested conditionals
    if orders_df.count() > 0:
        null_count = orders_df.filter(F.col("customer_id").isNull()).count()
        if null_count > 0:
            if config.get("strict_mode"):
                if null_count > config.get("max_null_threshold", 100):
                    raise ValueError(f"Too many nulls: {null_count}")
                else:
                    print(f"Warning: {null_count} null customer IDs")
                    orders_df = orders_df.filter(F.col("customer_id").isNotNull())
            else:
                orders_df = orders_df.fillna({"customer_id": "UNKNOWN"})

        if orders_df.filter(F.col("amount") <= 0).count() > 0:
            if config.get("remove_invalid_amounts", True):
                orders_df = orders_df.filter(F.col("amount") > 0)
            else:
                if config.get("cap_negative_amounts"):
                    orders_df = orders_df.withColumn(
                        "amount",
                        F.when(F.col("amount") <= 0, F.lit(0)).otherwise(F.col("amount"))
                    )
    else:
        if config.get("fail_on_empty", False):
            raise ValueError("No orders found")
        else:
            print("Warning: Empty orders DataFrame")

    # Step 3: Complex transformations with more branching
    if config.get("timezone_conversion"):
        if config["source_timezone"] == "UTC":
            pass  # Already UTC
        elif config["source_timezone"] in ["CST", "America/Chicago"]:
            orders_df = orders_df.withColumn(
                "order_timestamp",
                F.to_utc_timestamp(F.col("order_timestamp"), "America/Chicago")
            )
        elif config["source_timezone"] in ["EST", "America/New_York"]:
            orders_df = orders_df.withColumn(
                "order_timestamp",
                F.to_utc_timestamp(F.col("order_timestamp"), "America/New_York")
            )
        else:
            orders_df = orders_df.withColumn(
                "order_timestamp",
                F.to_utc_timestamp(F.col("order_timestamp"), config["source_timezone"])
            )

    # Step 4: Aggregation with conditional logic
    if config.get("aggregation_level") == "daily":
        result_df = orders_df.groupBy("order_date").agg(
            F.sum("amount").alias("total_revenue"),
            F.count("*").alias("order_count")
        )
    elif config.get("aggregation_level") == "weekly":
        result_df = orders_df.withColumn(
            "week_start", F.date_trunc("week", F.col("order_date"))
        ).groupBy("week_start").agg(
            F.sum("amount").alias("total_revenue"),
            F.count("*").alias("order_count")
        )
    elif config.get("aggregation_level") == "monthly":
        result_df = orders_df.withColumn(
            "month_start", F.date_trunc("month", F.col("order_date"))
        ).groupBy("month_start").agg(
            F.sum("amount").alias("total_revenue"),
            F.count("*").alias("order_count")
        )
    else:
        result_df = orders_df

    # Step 5: Customer enrichment with yet more branching
    if customers_df.count() > 0:
        if config.get("join_type") == "inner":
            result_df = result_df.join(customers_df, "customer_id", "inner")
        else:
            result_df = result_df.join(customers_df, "customer_id", "left")

    # Step 6: Write with format-specific logic
    output_format = config.get("output_format", "parquet")
    if output_format == "parquet":
        result_df.write.mode("overwrite").parquet(config["output_path"])
    elif output_format == "delta":
        result_df.write.format("delta").mode("overwrite").save(config["output_path"])
    elif output_format == "csv":
        result_df.write.mode("overwrite").option("header", True).csv(config["output_path"])
    else:
        raise ValueError(f"Unsupported format: {output_format}")

    # Step 7: Post-processing notifications
    row_count = result_df.count()
    if config.get("send_notification"):
        if row_count == 0:
            send_alert("ETL produced zero rows", severity="high")
        elif row_count < config.get("min_expected_rows", 0):
            send_alert(f"ETL produced fewer rows than expected: {row_count}", severity="medium")
        else:
            send_notification(f"ETL complete: {row_count} rows")

    return result_df
```

**Why violates ENG-3.1:**
- Single function with cyclomatic complexity exceeding 25
- Seven distinct responsibilities crammed into one function (read, validate, transform, aggregate, enrich, write, notify)
- Deeply nested conditionals (4+ levels in validation section)
- Configuration-driven branching makes every path hard to test
- Adding a new aggregation level or output format increases complexity further
- Impossible to test individual steps in isolation

---

## How to Fix

Decompose into focused functions with a pipeline orchestrator:

```python
# Fixed: Each step is a small, testable function
def run_daily_etl(spark: SparkSession, config: PipelineConfig) -> DataFrame:
    """Orchestrate the daily ETL pipeline."""
    orders = read_with_fallback(spark, config.orders_path, config.orders_backup_path)
    customers = read_source(spark, config.customers_path)

    validated_orders = validate_and_clean(orders, config.validation)
    normalized_orders = normalize_timestamps(validated_orders, config.source_timezone)
    aggregated = aggregate_by_period(normalized_orders, config.aggregation_level)
    enriched = enrich_with_customers(aggregated, customers)

    write_output(enriched, config.output_path, config.output_format)
    notify_completion(enriched.count(), config.notification)

    return enriched
```

Each helper function has cyclomatic complexity under 5, is independently testable, and can be modified without affecting other steps.

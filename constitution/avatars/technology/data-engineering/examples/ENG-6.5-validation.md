---
law_id: ENG-6.5
avatar: data-engineering
---

# ENG-6.5: Input Validation Examples for Data Engineering

## COMPLIANT: Schema Validation with Pydantic and Spark

```python
from pydantic import BaseModel, Field, field_validator
from datetime import date, datetime
from decimal import Decimal
from uuid import UUID
from typing import Literal


# Pydantic models for pipeline configuration validation
class PipelineConfig(BaseModel):
    """Validated configuration for the ETL pipeline."""

    source_path: str = Field(min_length=1, pattern=r"^s3://[a-z0-9][\w\-./]+$")
    output_path: str = Field(min_length=1, pattern=r"^s3://[a-z0-9][\w\-./]+$")
    run_date: date
    aggregation_level: Literal["daily", "weekly", "monthly"]
    max_records: int = Field(ge=1, le=100_000_000, default=10_000_000)

    model_config = {"extra": "forbid"}

    @field_validator("run_date")
    @classmethod
    def validate_run_date_not_future(cls, v: date) -> date:
        if v > date.today():
            raise ValueError("Run date cannot be in the future")
        return v


# Schema validation for incoming DataFrames
from pyspark.sql import DataFrame
from pyspark.sql.types import (
    StructType, StructField, StringType, DoubleType,
    IntegerType, TimestampType
)
import pyspark.sql.functions as F


EXPECTED_ORDER_SCHEMA = StructType([
    StructField("order_id", StringType(), nullable=False),
    StructField("customer_id", StringType(), nullable=False),
    StructField("amount", DoubleType(), nullable=False),
    StructField("quantity", IntegerType(), nullable=False),
    StructField("order_timestamp", TimestampType(), nullable=False),
    StructField("product_category", StringType(), nullable=True),
])


def validate_dataframe_schema(
    df: DataFrame,
    expected_schema: StructType,
    source_name: str,
) -> DataFrame:
    """Validate DataFrame matches expected schema.

    Raises SchemaValidationError if schema does not match.
    """
    actual_fields = {field.name: field for field in df.schema.fields}
    expected_fields = {field.name: field for field in expected_schema.fields}

    missing = set(expected_fields) - set(actual_fields)
    if missing:
        raise SchemaValidationError(
            f"Source '{source_name}' missing columns: {sorted(missing)}"
        )

    for name, expected_field in expected_fields.items():
        actual_field = actual_fields[name]
        if actual_field.dataType != expected_field.dataType:
            raise SchemaValidationError(
                f"Column '{name}': expected {expected_field.dataType}, "
                f"got {actual_field.dataType}"
            )

    return df


def validate_data_quality(df: DataFrame) -> tuple[DataFrame, DataFrame]:
    """Validate data quality rules and separate valid from invalid rows.

    Returns (valid_df, rejected_df) tuple.
    """
    # Tag each row with validation results
    validated = df.withColumn(
        "validation_errors",
        F.array(
            *[
                F.when(condition, F.lit(message))
                for condition, message in [
                    (F.col("order_id").isNull(), "order_id is null"),
                    (F.col("customer_id").isNull(), "customer_id is null"),
                    (F.col("amount") <= 0, "amount must be positive"),
                    (F.col("amount") > 1_000_000, "amount exceeds maximum"),
                    (F.col("quantity") <= 0, "quantity must be positive"),
                    (F.col("quantity") > 10_000, "quantity exceeds maximum"),
                    (F.col("order_timestamp").isNull(), "order_timestamp is null"),
                ]
            ]
        )
    ).withColumn(
        "validation_errors",
        F.expr("filter(validation_errors, x -> x IS NOT NULL)")
    )

    valid_df = (
        validated
        .filter(F.size("validation_errors") == 0)
        .drop("validation_errors")
    )

    rejected_df = (
        validated
        .filter(F.size("validation_errors") > 0)
        .withColumn("rejected_at", F.current_timestamp())
    )

    return valid_df, rejected_df


# Usage in pipeline
def run_validated_pipeline(spark, raw_config: dict) -> DataFrame:
    """Pipeline with validation at every boundary."""
    # 1. Validate configuration
    config = PipelineConfig(**raw_config)

    # 2. Read and validate schema
    raw_df = spark.read.parquet(config.source_path)
    schema_validated_df = validate_dataframe_schema(
        raw_df, EXPECTED_ORDER_SCHEMA, "orders"
    )

    # 3. Validate data quality
    valid_df, rejected_df = validate_data_quality(schema_validated_df)

    # 4. Log rejected records for investigation
    if rejected_df.count() > 0:
        rejected_df.write.mode("append").parquet(
            f"{config.output_path}/rejected/{config.run_date}"
        )

    return valid_df
```

**Why compliant:**
- Pipeline configuration is validated with Pydantic before execution begins
- DataFrame schema is validated against an expected definition
- Data quality rules are applied declaratively with clear error messages
- Invalid rows are separated and logged rather than silently dropped
- Each validation function has a single responsibility

---

## COMPLIANT: dbt Schema Tests for Data Validation

```yaml
# models/staging/schema.yml
version: 2

models:
  - name: stg_orders
    description: "Staged orders with validated schema"
    columns:
      - name: order_id
        description: "Unique order identifier"
        tests:
          - unique
          - not_null
      - name: customer_id
        description: "Customer reference"
        tests:
          - not_null
          - relationships:
              to: ref('stg_customers')
              field: customer_id
      - name: amount
        description: "Order amount in USD"
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0.01
              max_value: 1000000
      - name: quantity
        description: "Item count"
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 1
              max_value: 10000
      - name: order_date
        description: "Date order was placed"
        tests:
          - not_null
          - dbt_utils.not_accepted_values:
              values: ['1970-01-01', '9999-12-31']
      - name: status
        description: "Order status"
        tests:
          - accepted_values:
              values: ['draft', 'submitted', 'confirmed', 'shipped', 'delivered', 'cancelled']
```

```sql
-- tests/generic/test_no_duplicate_orders_per_day.sql
-- Custom singular test for business rule validation
SELECT
    customer_id,
    order_date,
    COUNT(*) AS duplicate_count
FROM {{ ref('stg_orders') }}
GROUP BY customer_id, order_date
HAVING COUNT(*) > 50  -- No customer should have 50+ orders per day
```

**Why compliant:** Schema tests validate column-level constraints declaratively. Referential integrity is checked with `relationships` tests. Range tests catch outlier values. Custom tests enforce business rules. All tests run as part of the dbt pipeline before downstream models.

---

## COMPLIANT: Great Expectations for Runtime Validation

```python
import great_expectations as gx
from great_expectations.core.expectation_suite import ExpectationSuite


def create_order_expectations() -> ExpectationSuite:
    """Define data quality expectations for order data."""
    suite = ExpectationSuite(expectation_suite_name="orders_suite")

    # Column presence
    suite.add_expectation(
        gx.expectations.ExpectTableColumnsToMatchSet(
            column_set=[
                "order_id", "customer_id", "amount",
                "quantity", "order_timestamp", "product_category"
            ],
            exact_match=False,
        )
    )

    # Not null constraints
    for column in ["order_id", "customer_id", "amount", "order_timestamp"]:
        suite.add_expectation(
            gx.expectations.ExpectColumnValuesToNotBeNull(column=column)
        )

    # Uniqueness
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeUnique(column="order_id")
    )

    # Range validation
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="amount",
            min_value=0.01,
            max_value=1_000_000.00,
        )
    )

    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="quantity",
            min_value=1,
            max_value=10_000,
        )
    )

    # Categorical validation
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeInSet(
            column="product_category",
            value_set=[
                "electronics", "clothing", "food",
                "home", "sports", "other"
            ],
        )
    )

    # Row count sanity check
    suite.add_expectation(
        gx.expectations.ExpectTableRowCountToBeBetween(
            min_value=1,
            max_value=50_000_000,
        )
    )

    return suite


def validate_with_great_expectations(
    df: DataFrame,
    suite: ExpectationSuite,
) -> bool:
    """Run Great Expectations validation and return pass/fail."""
    context = gx.get_context()
    datasource = context.sources.add_or_update_spark(name="spark_source")
    data_asset = datasource.add_dataframe_asset(name="orders")
    batch_request = data_asset.build_batch_request(dataframe=df)

    checkpoint = context.add_or_update_checkpoint(
        name="order_validation",
        validations=[{
            "batch_request": batch_request,
            "expectation_suite_name": suite.expectation_suite_name,
        }],
    )

    result = checkpoint.run()
    return result.success
```

**Why compliant:** Expectations are defined declaratively and separate from pipeline logic. Each expectation validates one specific rule. The suite can be version-controlled and shared across pipelines. Failures produce detailed diagnostic reports.

---

## VIOLATION: No Validation on Incoming Data

```python
def run_etl(spark, source_path, output_path):
    """Pipeline with no validation at any boundary."""

    # No config validation - raw string paths used directly
    # source_path could be empty, malformed, or point to wrong data

    # No schema validation - assumes columns exist
    orders_df = spark.read.parquet(source_path)

    # Direct column access without checking existence
    # Will crash at runtime if columns are missing or renamed
    result = (
        orders_df
        .filter(F.col("status") == "completed")  # Column may not exist!
        .withColumn(
            "total",
            F.col("amount") * F.col("quantity")  # Could be null, negative, or wrong type!
        )
        .groupBy("customer_id")  # customer_id could be null!
        .agg(
            F.sum("total").alias("customer_total"),
            F.count("*").alias("order_count"),
        )
    )

    # No data quality checks
    # - Null customer_ids silently create a "null" group
    # - Negative amounts produce wrong totals
    # - Zero quantities are included
    # - Duplicate order_ids inflate counts

    # No row count validation
    # Could write zero rows or millions of corrupt rows
    result.write.mode("overwrite").parquet(output_path)

    # No post-write verification
    print(f"Done! Wrote to {output_path}")
```

**Why violates ENG-6.5:**
- No configuration validation; invalid paths cause runtime failures
- No schema validation; column renames or removals cause silent failures
- No data quality checks; null, negative, and duplicate values produce wrong results
- No row count validation; empty or wildly inflated outputs go undetected
- No rejected record tracking; bad data is silently included or silently dropped
- No post-write verification; corrupt output is published to downstream consumers

---

## VIOLATION: Validation That Silently Hides Problems

```python
def clean_orders(df: DataFrame) -> DataFrame:
    """Bad validation: silently fixes data without tracking."""

    # Silently drops rows with no audit trail!
    df = df.dropna()

    # Silently coerces values with no logging!
    df = df.withColumn(
        "amount",
        F.when(F.col("amount") <= 0, F.lit(0.01)).otherwise(F.col("amount"))
    )

    # Silently replaces nulls with magic values!
    df = df.fillna({
        "customer_id": "UNKNOWN",
        "product_category": "other",
        "quantity": 1,
    })

    # No metrics on how many rows were affected
    # No rejected records table for investigation
    # No alerts when data quality degrades
    return df
```

**Why violates ENG-6.5:**
- `dropna()` silently removes rows with no tracking of what was lost
- Magic value replacements hide data quality issues from downstream consumers
- No metrics or logging to detect degrading data quality over time
- No rejected records table for data stewards to investigate
- Problems in source data go undetected until business reports are wrong

---

## Validation Strategy Summary

| Boundary | What to Validate | Tool |
|----------|-----------------|------|
| **Pipeline Config** | Paths, dates, parameters | Pydantic, dataclasses |
| **Source Schema** | Column names, types, presence | Spark schema comparison |
| **Data Quality** | Nulls, ranges, uniqueness, referential integrity | Great Expectations, dbt tests |
| **Row Counts** | Min/max expected rows, zero-row checks | Custom assertions |
| **Output** | Post-write verification, schema match | Read-back validation |

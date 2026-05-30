---
law_id: ENG-4.1
avatar: data-engineering
---

# ENG-4.1: Atomic TDD Examples for Data Engineering

## COMPLIANT: Unit Testing Spark Transformations with pytest

```python
import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
from chispa import assert_df_equality
from transformations.customer_aggregations import aggregate_customer_orders


@pytest.fixture(scope="session")
def spark():
    """Create a SparkSession for testing."""
    return SparkSession.builder \
        .master("local[2]") \
        .appName("unit-tests") \
        .config("spark.sql.shuffle.partitions", "2") \
        .getOrCreate()


@pytest.fixture
def sample_orders(spark):
    """Create sample order data for testing."""
    schema = StructType([
        StructField("customer_id", StringType(), False),
        StructField("order_id", StringType(), False),
        StructField("amount", DoubleType(), False),
        StructField("order_date", StringType(), False)
    ])
    data = [
        ("C001", "O001", 100.50, "2024-01-15"),
        ("C001", "O002", 250.00, "2024-01-20"),
        ("C002", "O003", 75.25, "2024-01-18"),
    ]
    return spark.createDataFrame(data, schema)


def test_aggregate_customer_orders_calculates_totals(spark, sample_orders):
    """Test that customer order aggregation computes correct totals."""
    # Arrange
    expected_schema = StructType([
        StructField("customer_id", StringType(), False),
        StructField("total_orders", IntegerType(), False),
        StructField("total_amount", DoubleType(), False)
    ])
    expected_data = [
        ("C001", 2, 350.50),
        ("C002", 1, 75.25),
    ]
    expected_df = spark.createDataFrame(expected_data, expected_schema)

    # Act
    result_df = aggregate_customer_orders(sample_orders)

    # Assert
    assert_df_equality(result_df, expected_df, ignore_row_order=True)


def test_aggregate_customer_orders_handles_empty_dataframe(spark):
    """Test aggregation gracefully handles empty input."""
    # Arrange
    schema = StructType([
        StructField("customer_id", StringType(), False),
        StructField("order_id", StringType(), False),
        StructField("amount", DoubleType(), False),
        StructField("order_date", StringType(), False)
    ])
    empty_df = spark.createDataFrame([], schema)

    # Act
    result_df = aggregate_customer_orders(empty_df)

    # Assert
    assert result_df.count() == 0
```

**Why compliant:** Tests are atomic, focused on single behaviors, use fixtures for setup, follow Arrange-Act-Assert pattern, and test both happy path and edge cases. Each test is independent and can run in isolation.

---

## COMPLIANT: Testing dbt Models with pytest-dbt

```python
import pytest
from dbt.tests.util import run_dbt, check_relations_equal


class TestCustomerLifetimeValue:
    """Test suite for customer_lifetime_value dbt model."""

    @pytest.fixture(scope="class")
    def seeds(self):
        """Seed data for testing."""
        return {
            "raw_customers": """
customer_id,first_name,last_name,created_at
1,John,Doe,2024-01-01
2,Jane,Smith,2024-01-02
""",
            "raw_orders": """
order_id,customer_id,amount,order_date
1,1,100.00,2024-01-15
2,1,200.00,2024-02-15
3,2,150.00,2024-01-20
""",
            "expected_clv": """
customer_id,total_orders,total_revenue,avg_order_value
1,2,300.00,150.00
2,1,150.00,150.00
"""
        }

    @pytest.fixture(scope="class")
    def project_config_update(self):
        return {"name": "clv_test_project"}

    def test_customer_lifetime_value_calculation(self, project):
        """Test CLV model produces correct aggregations."""
        # Run seeds and model
        run_dbt(["seed"])
        run_dbt(["run", "--select", "customer_lifetime_value"])

        # Compare result with expected
        check_relations_equal(
            project.adapter,
            ["customer_lifetime_value", "expected_clv"]
        )

    def test_clv_model_handles_null_orders(self, project):
        """Test CLV handles customers with no orders."""
        run_dbt(["seed"])
        run_dbt(["run", "--select", "customer_lifetime_value"])

        # Verify model runs without error and has expected row count
        results = project.run_sql(
            "SELECT COUNT(*) as cnt FROM customer_lifetime_value",
            fetch="one"
        )
        assert results[0] == 2


# dbt schema test in YAML format
"""
# models/staging/schema.yml
version: 2

models:
  - name: customer_lifetime_value
    description: "Customer lifetime value aggregations"
    columns:
      - name: customer_id
        tests:
          - unique
          - not_null
      - name: total_revenue
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
"""
```

**Why compliant:** Uses dbt's testing framework properly, seeds test data, compares results with expected outcomes, and includes both Python tests and dbt schema tests for comprehensive coverage.

---

## VIOLATION: Integration Test Masquerading as Unit Test

```python
from pyspark.sql import SparkSession
from transformations.customer_aggregations import aggregate_customer_orders


def test_full_pipeline():
    """Test entire data pipeline end-to-end."""
    spark = SparkSession.builder \
        .master("local[*]") \
        .appName("test") \
        .getOrCreate()

    # Read from actual S3 bucket
    orders_df = spark.read.parquet("s3://production-data/orders/")
    customers_df = spark.read.parquet("s3://production-data/customers/")

    # Run multiple transformations
    cleaned_orders = clean_orders(orders_df)
    enriched_orders = enrich_with_customers(cleaned_orders, customers_df)
    aggregated = aggregate_customer_orders(enriched_orders)

    # Write to test location
    aggregated.write.mode("overwrite").parquet("s3://test-output/results/")

    # Read back and verify
    result = spark.read.parquet("s3://test-output/results/")
    assert result.count() > 0  # Vague assertion

    spark.stop()
```

**Why violates ENG-4.1:** This test violates atomic TDD principles by: (1) testing multiple transformations at once instead of isolating each function, (2) depending on external production data making tests non-deterministic, (3) having side effects by writing to external storage, (4) using vague assertions that don't verify actual business logic, and (5) not using fixtures for SparkSession management.

---

## VIOLATION: Missing Test Isolation in dbt

```sql
-- models/marts/daily_revenue.sql
-- No tests defined, relies on manual verification

SELECT
    DATE(order_timestamp) as order_date,
    SUM(amount) as total_revenue,
    COUNT(*) as order_count
FROM {{ ref('stg_orders') }}
GROUP BY 1

-- Developer verifies by running:
-- dbt run && dbt docs generate
-- Then manually checks results in the warehouse
```

```yaml
# models/marts/schema.yml
version: 2

models:
  - name: daily_revenue
    # No column tests defined
    # No data quality tests
    # No documentation
```

**Why violates ENG-4.1:** This violates atomic TDD by: (1) having no automated tests for the model, (2) relying on manual verification which is error-prone and non-repeatable, (3) missing schema tests for data quality (not_null, unique, accepted_range), (4) no test for edge cases like empty source data or null values, and (5) no singular tests to verify business logic correctness.

---

## COMPLIANT: Testing Spark Data Quality with Great Expectations

```python
import pytest
import great_expectations as gx
from great_expectations.core.batch import RuntimeBatchRequest
from pyspark.sql import SparkSession


@pytest.fixture(scope="module")
def ge_context():
    """Initialize Great Expectations context."""
    return gx.get_context()


@pytest.fixture(scope="module")
def spark():
    return SparkSession.builder \
        .master("local[2]") \
        .appName("ge-tests") \
        .getOrCreate()


class TestOrderDataQuality:
    """Data quality tests for order data."""

    def test_order_id_is_unique(self, ge_context, spark, sample_orders_df):
        """Verify order_id uniqueness."""
        # Arrange
        validator = ge_context.get_validator(
            batch_request=RuntimeBatchRequest(
                datasource_name="spark_datasource",
                data_connector_name="runtime_data_connector",
                data_asset_name="orders",
                runtime_parameters={"batch_data": sample_orders_df},
                batch_identifiers={"batch_id": "test_batch"},
            ),
            expectation_suite_name="orders_suite"
        )

        # Act & Assert
        result = validator.expect_column_values_to_be_unique("order_id")
        assert result.success, "order_id must be unique"

    def test_amount_within_valid_range(self, ge_context, spark, sample_orders_df):
        """Verify order amounts are within acceptable range."""
        validator = ge_context.get_validator(
            batch_request=RuntimeBatchRequest(
                datasource_name="spark_datasource",
                data_connector_name="runtime_data_connector",
                data_asset_name="orders",
                runtime_parameters={"batch_data": sample_orders_df},
                batch_identifiers={"batch_id": "test_batch"},
            ),
            expectation_suite_name="orders_suite"
        )

        result = validator.expect_column_values_to_be_between(
            "amount", min_value=0.01, max_value=100000.00
        )
        assert result.success, "Order amounts must be between $0.01 and $100,000"

    def test_no_null_customer_ids(self, ge_context, spark, sample_orders_df):
        """Verify customer_id is never null."""
        validator = ge_context.get_validator(
            batch_request=RuntimeBatchRequest(
                datasource_name="spark_datasource",
                data_connector_name="runtime_data_connector",
                data_asset_name="orders",
                runtime_parameters={"batch_data": sample_orders_df},
                batch_identifiers={"batch_id": "test_batch"},
            ),
            expectation_suite_name="orders_suite"
        )

        result = validator.expect_column_values_to_not_be_null("customer_id")
        assert result.success, "customer_id must not be null"
```

**Why compliant:** Each test focuses on a single data quality expectation, uses proper fixtures for context and SparkSession, assertions are specific and meaningful, and tests can run independently with deterministic sample data.

---

## TDD Cycle Commands

```bash
# RED: Run specific test, see it fail
pytest tests/pipelines/test_transformer.py::test_transform_adds_calculated_fields -v

# GREEN: Write code, run test again
pytest tests/pipelines/test_transformer.py::test_transform_adds_calculated_fields -v

# REFACTOR: Run all unit tests
pytest tests/ -m "not integration"

# VERIFY: Check coverage and constitutional compliance
pytest --cov=src --cov-fail-under=80
constitution-lint .

# Commit when green and compliant
git add -A && git commit -m "Add calculated fields to data transformer"
```

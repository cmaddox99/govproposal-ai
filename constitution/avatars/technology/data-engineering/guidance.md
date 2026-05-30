# Data Engineering Guidance

> **Purpose:** Stack-specific agent behaviors for Data Engineering, ETL, and Spark projects.

---

## Overview

This guidance provides patterns for AI agents working with Data Engineering projects including ETL pipelines, Apache Spark, data warehousing, and data quality frameworks.

---

## Testing Framework

**Primary Framework:** pytest + pyspark.testing + great_expectations

### Test Structure

```python
import pytest
from pyspark.sql import SparkSession
from pyspark.testing import assertDataFrameEqual
from myproject.transformations.orders import (
    clean_orders,
    calculate_order_metrics,
    OrderTransformer
)

@pytest.fixture(scope="session")
def spark():
    """Session-scoped Spark fixture."""
    return (SparkSession.builder
            .master("local[2]")
            .appName("unit-tests")
            .config("spark.sql.shuffle.partitions", "2")
            .getOrCreate())

@pytest.fixture
def sample_orders(spark):
    """Sample orders DataFrame."""
    return spark.createDataFrame([
        ("order-1", "cust-1", 100.0, "2024-01-15", "placed"),
        ("order-2", "cust-1", 200.0, "2024-01-16", "placed"),
        ("order-3", "cust-2", 50.0, "2024-01-15", "cancelled"),
    ], ["order_id", "customer_id", "total", "order_date", "status"])


class TestCleanOrders:
    """Tests for order cleaning transformation."""

    def test_removes_cancelled_orders(self, spark, sample_orders):
        """Cancelled orders should be filtered out."""
        # Act
        result = clean_orders(sample_orders)

        # Assert
        assert result.count() == 2
        assert result.filter("status = 'cancelled'").count() == 0

    def test_removes_null_totals(self, spark):
        """Orders with null totals should be removed."""
        # Arrange
        orders = spark.createDataFrame([
            ("order-1", "cust-1", 100.0, "placed"),
            ("order-2", "cust-1", None, "placed"),
        ], ["order_id", "customer_id", "total", "status"])

        # Act
        result = clean_orders(orders)

        # Assert
        assert result.count() == 1
        assert result.filter("total IS NULL").count() == 0


class TestCalculateOrderMetrics:
    """Tests for order metrics calculation."""

    def test_calculates_customer_totals(self, spark, sample_orders):
        """Should calculate total per customer."""
        # Act
        result = calculate_order_metrics(sample_orders)

        # Assert
        cust_1 = result.filter("customer_id = 'cust-1'").collect()[0]
        assert cust_1.total_spent == 300.0
        assert cust_1.order_count == 2

    def test_calculates_average_order_value(self, spark, sample_orders):
        """Should calculate average order value."""
        # Act
        result = calculate_order_metrics(sample_orders)

        # Assert
        cust_1 = result.filter("customer_id = 'cust-1'").collect()[0]
        assert cust_1.avg_order_value == 150.0
```

### Data Quality Tests

```python
import great_expectations as gx
from great_expectations.dataset import SparkDFDataset

class TestDataQuality:
    """Data quality validation tests."""

    def test_orders_schema_valid(self, spark, sample_orders):
        """Orders should have valid schema."""
        expected_schema = ["order_id", "customer_id", "total", "order_date", "status"]
        assert sample_orders.columns == expected_schema

    def test_orders_data_expectations(self, spark, sample_orders):
        """Orders should meet data quality expectations."""
        # Wrap DataFrame with Great Expectations
        ge_df = SparkDFDataset(sample_orders)

        # Define expectations
        ge_df.expect_column_values_to_not_be_null("order_id")
        ge_df.expect_column_values_to_be_unique("order_id")
        ge_df.expect_column_values_to_be_between("total", min_value=0)
        ge_df.expect_column_values_to_be_in_set(
            "status",
            ["placed", "shipped", "delivered", "cancelled"]
        )

        # Validate
        results = ge_df.validate()
        assert results.success, f"Data validation failed: {results}"
```

---

## Common Patterns

### Transformation Functions

```python
from pyspark.sql import DataFrame
from pyspark.sql import functions as F

def clean_orders(orders_df: DataFrame) -> DataFrame:
    """
    Clean orders data by removing invalid records.

    Removes:
    - Cancelled orders
    - Orders with null totals
    - Orders with negative totals
    """
    return (orders_df
            .filter(F.col("status") != "cancelled")
            .filter(F.col("total").isNotNull())
            .filter(F.col("total") >= 0))


def calculate_order_metrics(orders_df: DataFrame) -> DataFrame:
    """
    Calculate customer-level order metrics.

    Returns DataFrame with columns:
    - customer_id
    - total_spent
    - order_count
    - avg_order_value
    - first_order_date
    - last_order_date
    """
    return (orders_df
            .groupBy("customer_id")
            .agg(
                F.sum("total").alias("total_spent"),
                F.count("order_id").alias("order_count"),
                F.avg("total").alias("avg_order_value"),
                F.min("order_date").alias("first_order_date"),
                F.max("order_date").alias("last_order_date")
            ))
```

### Schema Definitions

```python
from pyspark.sql.types import (
    StructType, StructField, StringType, DoubleType,
    DateType, TimestampType, IntegerType
)

# Explicit schema for raw data
RAW_ORDERS_SCHEMA = StructType([
    StructField("order_id", StringType(), nullable=False),
    StructField("customer_id", StringType(), nullable=False),
    StructField("total", DoubleType(), nullable=True),
    StructField("order_date", DateType(), nullable=True),
    StructField("status", StringType(), nullable=True),
    StructField("created_at", TimestampType(), nullable=True),
])

# Read with explicit schema
def read_orders(spark, path: str) -> DataFrame:
    """Read orders with enforced schema."""
    return (spark.read
            .schema(RAW_ORDERS_SCHEMA)
            .parquet(path))
```

### ETL Job Structure

```python
from abc import ABC, abstractmethod
from pyspark.sql import SparkSession, DataFrame
from dataclasses import dataclass

@dataclass
class JobConfig:
    """Configuration for ETL job."""
    input_path: str
    output_path: str
    partition_date: str
    write_mode: str = "overwrite"


class ETLJob(ABC):
    """Base class for ETL jobs."""

    def __init__(self, spark: SparkSession, config: JobConfig):
        self.spark = spark
        self.config = config

    @abstractmethod
    def extract(self) -> DataFrame:
        """Extract data from source."""
        pass

    @abstractmethod
    def transform(self, df: DataFrame) -> DataFrame:
        """Apply transformations."""
        pass

    @abstractmethod
    def load(self, df: DataFrame) -> None:
        """Load data to destination."""
        pass

    def run(self) -> None:
        """Execute the ETL job."""
        raw_df = self.extract()
        transformed_df = self.transform(raw_df)
        self.load(transformed_df)


class OrdersETLJob(ETLJob):
    """ETL job for orders data."""

    def extract(self) -> DataFrame:
        return read_orders(self.spark, self.config.input_path)

    def transform(self, df: DataFrame) -> DataFrame:
        return (df
                .transform(clean_orders)
                .transform(calculate_order_metrics))

    def load(self, df: DataFrame) -> None:
        (df.write
         .mode(self.config.write_mode)
         .partitionBy("order_date")
         .parquet(self.config.output_path))
```

### Airflow DAG

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='orders_daily_pipeline',
    default_args=default_args,
    description='Daily orders ETL pipeline',
    schedule_interval='0 6 * * *',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['orders', 'etl'],
) as dag:

    extract_task = SparkSubmitOperator(
        task_id='extract_orders',
        application='jobs/orders/extract.py',
        conf={'spark.executor.memory': '4g'},
    )

    transform_task = SparkSubmitOperator(
        task_id='transform_orders',
        application='jobs/orders/transform.py',
    )

    quality_check = PythonOperator(
        task_id='quality_check',
        python_callable=run_data_quality_checks,
    )

    load_task = SparkSubmitOperator(
        task_id='load_orders',
        application='jobs/orders/load.py',
    )

    extract_task >> transform_task >> quality_check >> load_task
```

---

## Anti-Patterns to Avoid

### No Schema Enforcement

```python
# BAD - Infer schema (slow, unreliable)
df = spark.read.parquet(path)  # Schema inferred

# GOOD - Explicit schema
df = spark.read.schema(ORDERS_SCHEMA).parquet(path)
```

### Collect in Production

```python
# BAD - Collecting large datasets to driver
all_data = df.collect()  # Out of memory!
for row in all_data:
    process(row)

# GOOD - Use distributed operations
result = (df
          .groupBy("customer_id")
          .agg(F.sum("total"))
          .write.parquet(output_path))
```

### Hardcoded Paths

```python
# BAD - Hardcoded paths
df = spark.read.parquet("s3://my-bucket/orders/2024-01-15")

# GOOD - Configuration-driven
config = load_config(env)
df = spark.read.parquet(f"{config.base_path}/orders/{partition_date}")
```

---

## Data Quality Framework

```python
from great_expectations.core.expectation_suite import ExpectationSuite

def create_orders_expectations() -> ExpectationSuite:
    """Create expectations for orders data."""
    suite = ExpectationSuite(expectation_suite_name="orders_suite")

    # Schema expectations
    suite.add_expectation({
        "expectation_type": "expect_table_columns_to_match_ordered_list",
        "kwargs": {
            "column_list": ["order_id", "customer_id", "total", "order_date", "status"]
        }
    })

    # Value expectations
    suite.add_expectation({
        "expectation_type": "expect_column_values_to_not_be_null",
        "kwargs": {"column": "order_id"}
    })

    suite.add_expectation({
        "expectation_type": "expect_column_values_to_be_unique",
        "kwargs": {"column": "order_id"}
    })

    suite.add_expectation({
        "expectation_type": "expect_column_values_to_be_between",
        "kwargs": {"column": "total", "min_value": 0}
    })

    return suite
```

---

## Tools and Commands

### Development

```bash
# Start Spark shell
pyspark --master local[4]

# Run Spark job locally
spark-submit --master local[4] jobs/orders/transform.py

# Start Airflow locally
airflow standalone

# Run specific DAG
airflow dags trigger orders_daily_pipeline
```

### Testing

```bash
# Run all tests
pytest

# Run with Spark tests (slower)
pytest tests/transformations/

# Run data quality tests
pytest tests/quality/

# Run Great Expectations checkpoint
great_expectations checkpoint run orders_checkpoint
```

### Data Quality

```bash
# Initialize Great Expectations
great_expectations init

# Create new expectation suite
great_expectations suite new

# Run checkpoint
great_expectations checkpoint run orders_checkpoint

# Build data docs
great_expectations docs build
```

---

## Testing Strategy

1. **Unit Tests** - Pure transformation functions
   - Input/output verification
   - Edge case handling
   - Schema validation

2. **Integration Tests** - Full pipeline execution
   - End-to-end data flow
   - Cross-system integration
   - Performance benchmarks

3. **Data Quality Tests** - Data expectations
   - Schema conformance
   - Value ranges
   - Referential integrity
   - Freshness checks

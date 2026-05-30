---
law_id: BUS-3.1
avatar: data-engineering
---

# BUS-3.1: Data Governance Examples for Data Engineering

## COMPLIANT: Comprehensive Data Lineage with OpenLineage

```python
from openlineage.client import OpenLineageClient
from openlineage.client.run import RunEvent, RunState, Run, Job, Dataset
from openlineage.client.facet import (
    SchemaDatasetFacet,
    SchemaField,
    DataQualityMetricsInputDatasetFacet,
    ColumnLineageDatasetFacet,
    ColumnLineageDatasetFacetFieldsAdditional,
    InputField
)
import uuid
from datetime import datetime


class LineageTrackedTransformation:
    """Base class for transformations with automatic lineage tracking."""

    def __init__(self, namespace: str, job_name: str):
        self.client = OpenLineageClient.from_environment()
        self.namespace = namespace
        self.job_name = job_name
        self.run_id = str(uuid.uuid4())

    def emit_start(self, inputs: list[Dataset], outputs: list[Dataset]):
        """Emit lineage event when job starts."""
        self.client.emit(
            RunEvent(
                eventType=RunState.START,
                eventTime=datetime.utcnow().isoformat() + "Z",
                run=Run(runId=self.run_id),
                job=Job(namespace=self.namespace, name=self.job_name),
                inputs=inputs,
                outputs=outputs
            )
        )

    def emit_complete(self, inputs: list[Dataset], outputs: list[Dataset]):
        """Emit lineage event when job completes successfully."""
        self.client.emit(
            RunEvent(
                eventType=RunState.COMPLETE,
                eventTime=datetime.utcnow().isoformat() + "Z",
                run=Run(runId=self.run_id),
                job=Job(namespace=self.namespace, name=self.job_name),
                inputs=inputs,
                outputs=outputs
            )
        )


class CustomerAggregationJob(LineageTrackedTransformation):
    """Customer aggregation with full lineage tracking."""

    def __init__(self):
        super().__init__(
            namespace="production.data-platform",
            job_name="customer_aggregation"
        )

    def run(self, spark, input_path: str, output_path: str):
        """Execute transformation with lineage events."""
        # Define input dataset with schema facet
        input_dataset = Dataset(
            namespace="s3://data-lake",
            name="raw_orders",
            facets={
                "schema": SchemaDatasetFacet(
                    fields=[
                        SchemaField(name="customer_id", type="STRING"),
                        SchemaField(name="order_id", type="STRING"),
                        SchemaField(name="amount", type="DOUBLE"),
                        SchemaField(name="order_date", type="DATE")
                    ]
                )
            }
        )

        # Define output dataset with column lineage
        output_dataset = Dataset(
            namespace="s3://data-lake",
            name="customer_aggregates",
            facets={
                "schema": SchemaDatasetFacet(
                    fields=[
                        SchemaField(name="customer_id", type="STRING"),
                        SchemaField(name="total_orders", type="INTEGER"),
                        SchemaField(name="total_amount", type="DOUBLE"),
                        SchemaField(name="avg_order_value", type="DOUBLE")
                    ]
                ),
                "columnLineage": ColumnLineageDatasetFacet(
                    fields={
                        "total_amount": ColumnLineageDatasetFacetFieldsAdditional(
                            inputFields=[
                                InputField(
                                    namespace="s3://data-lake",
                                    name="raw_orders",
                                    field="amount"
                                )
                            ],
                            transformationDescription="SUM(amount)",
                            transformationType="AGGREGATION"
                        )
                    }
                )
            }
        )

        # Emit start event
        self.emit_start([input_dataset], [output_dataset])

        try:
            # Execute transformation
            orders_df = spark.read.parquet(input_path)
            result_df = orders_df.groupBy("customer_id").agg(
                F.count("order_id").alias("total_orders"),
                F.sum("amount").alias("total_amount"),
                F.avg("amount").alias("avg_order_value")
            )
            result_df.write.mode("overwrite").parquet(output_path)

            # Emit completion event
            self.emit_complete([input_dataset], [output_dataset])

        except Exception as e:
            self.emit_fail([input_dataset], [output_dataset], str(e))
            raise
```

**Why compliant:** Implements comprehensive data lineage tracking with OpenLineage, captures schema information, tracks column-level lineage with transformation types, and emits events for job lifecycle (start, complete, fail) enabling full auditability.

---

## COMPLIANT: Data Quality Framework with Automated Monitoring

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import great_expectations as gx
from great_expectations.core import ExpectationSuite
from pyspark.sql import DataFrame
import json


@dataclass
class DataQualityResult:
    """Immutable data quality check result."""
    dataset_name: str
    check_timestamp: datetime
    passed: bool
    total_expectations: int
    successful_expectations: int
    failed_expectations: int
    details: dict

    def to_audit_record(self) -> dict:
        """Convert to audit record for storage."""
        return {
            "dataset_name": self.dataset_name,
            "check_timestamp": self.check_timestamp.isoformat(),
            "passed": self.passed,
            "success_rate": self.successful_expectations / self.total_expectations,
            "details": json.dumps(self.details)
        }


class DataQualityGate:
    """Enforces data quality standards before data promotion."""

    def __init__(self, context: gx.DataContext):
        self.context = context
        self.audit_log = []

    def validate_dataset(
        self,
        df: DataFrame,
        suite_name: str,
        dataset_name: str,
        fail_on_error: bool = True
    ) -> DataQualityResult:
        """Validate DataFrame against expectation suite."""

        validator = self.context.get_validator(
            batch_request=self._create_batch_request(df, dataset_name),
            expectation_suite_name=suite_name
        )

        results = validator.validate()

        quality_result = DataQualityResult(
            dataset_name=dataset_name,
            check_timestamp=datetime.utcnow(),
            passed=results.success,
            total_expectations=results.statistics["evaluated_expectations"],
            successful_expectations=results.statistics["successful_expectations"],
            failed_expectations=results.statistics["unsuccessful_expectations"],
            details=self._extract_failure_details(results)
        )

        # Always log for audit trail
        self._log_audit_record(quality_result)

        if not quality_result.passed and fail_on_error:
            raise DataQualityException(
                f"Data quality validation failed for {dataset_name}. "
                f"Passed {quality_result.successful_expectations}/{quality_result.total_expectations} checks."
            )

        return quality_result

    def _log_audit_record(self, result: DataQualityResult):
        """Persist audit record for compliance."""
        audit_record = result.to_audit_record()
        audit_record["logged_at"] = datetime.utcnow().isoformat()

        # Write to audit table
        self.audit_log.append(audit_record)

        # Also emit to monitoring system
        self._emit_metrics(result)

    def _emit_metrics(self, result: DataQualityResult):
        """Emit metrics for monitoring dashboards."""
        metrics = {
            "dq.validation.success": 1 if result.passed else 0,
            "dq.expectations.total": result.total_expectations,
            "dq.expectations.passed": result.successful_expectations,
            "dq.expectations.failed": result.failed_expectations,
        }
        # Emit to Prometheus/DataDog/CloudWatch
        for metric_name, value in metrics.items():
            statsd.gauge(metric_name, value, tags=[f"dataset:{result.dataset_name}"])


# Expectation Suite Definition
def create_customer_suite() -> ExpectationSuite:
    """Define data quality expectations for customer data."""
    suite = ExpectationSuite(expectation_suite_name="customer_data_quality")

    # Structural expectations
    suite.add_expectation(
        gx.expectations.ExpectColumnToExist(column="customer_id")
    )
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToNotBeNull(column="customer_id")
    )
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeUnique(column="customer_id")
    )

    # Business rule expectations
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToMatchRegex(
            column="email",
            regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        )
    )
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="age",
            min_value=0,
            max_value=150
        )
    )

    return suite
```

**Why compliant:** Implements a data quality gate pattern that blocks bad data from propagating, maintains immutable audit records with timestamps, emits metrics for monitoring, and defines explicit business rule expectations in code.

---

## VIOLATION: No Data Lineage Tracking

```python
from pyspark.sql import SparkSession
import pyspark.sql.functions as F


def run_aggregation_job():
    """Run aggregation with no lineage tracking."""
    spark = SparkSession.builder.appName("aggregation").getOrCreate()

    # Read from multiple sources - no tracking of what was read
    orders = spark.read.parquet("s3://bucket/orders/")
    customers = spark.read.parquet("s3://bucket/customers/")
    products = spark.read.parquet("s3://bucket/products/")

    # Complex transformations - no documentation of logic
    result = orders \
        .join(customers, "customer_id") \
        .join(products, "product_id") \
        .groupBy("region", "category") \
        .agg(F.sum("amount").alias("total"))

    # Write to output - no tracking of what was written
    result.write.mode("overwrite").parquet("s3://bucket/aggregates/")

    print("Job completed")


if __name__ == "__main__":
    run_aggregation_job()
```

**Why violates BUS-3.1:** This code violates data governance by: (1) having no data lineage tracking making it impossible to trace data flow, (2) no documentation of which sources contributed to outputs, (3) no column-level lineage for aggregations, (4) no audit trail of when data was processed, and (5) making regulatory compliance (GDPR, CCPA) impossible to demonstrate.

---

## VIOLATION: Missing Data Quality Checks

```python
from pyspark.sql import SparkSession


def load_customer_data(spark, path):
    """Load customer data without any quality checks."""
    # Just read and return - no validation
    return spark.read.parquet(path)


def process_orders(spark, orders_path, output_path):
    """Process orders without data quality gates."""
    orders_df = spark.read.parquet(orders_path)

    # Assume data is clean - dangerous!
    # No null checks
    # No duplicate detection
    # No schema validation
    # No business rule validation

    # Calculate metrics that could be wrong due to bad data
    aggregated = orders_df.groupBy("customer_id").agg(
        {"amount": "sum", "order_id": "count"}
    )

    # Write potentially corrupted results
    aggregated.write.mode("overwrite").parquet(output_path)


def main():
    spark = SparkSession.builder.getOrCreate()

    # Load data with no quality checks
    customers = load_customer_data(spark, "s3://raw/customers/")

    # Process with no validation
    process_orders(spark, "s3://raw/orders/", "s3://curated/metrics/")

    print("Pipeline completed successfully")  # Lies!
```

**Why violates BUS-3.1:** This violates data governance by: (1) having no data quality checks before processing, (2) no validation of schema or data types, (3) no null/duplicate detection that could skew results, (4) no audit trail of data quality, (5) assuming data is clean without verification, and (6) potentially propagating bad data downstream.

---

## COMPLIANT: Data Catalog Integration with Apache Atlas

```python
from atlasclient.client import Atlas
from atlasclient.entity import Entity
from datetime import datetime
from typing import List, Dict, Any


class DataCatalogManager:
    """Manages data catalog entries for governance compliance."""

    def __init__(self, atlas_url: str, username: str, password: str):
        self.client = Atlas(atlas_url, username, password)

    def register_dataset(
        self,
        name: str,
        location: str,
        schema: List[Dict[str, Any]],
        owner: str,
        classification: str,
        description: str
    ) -> str:
        """Register a dataset in the catalog with full metadata."""

        # Create table entity
        table_entity = Entity(
            typeName="spark_table",
            attributes={
                "name": name,
                "qualifiedName": f"spark://{location}",
                "location": location,
                "owner": owner,
                "description": description,
                "createTime": datetime.utcnow().isoformat(),
                "lastModifiedTime": datetime.utcnow().isoformat(),
            },
            classifications=[
                {"typeName": classification}  # e.g., "PII", "CONFIDENTIAL", "PUBLIC"
            ]
        )

        # Create column entities with lineage
        columns = []
        for col_def in schema:
            column_entity = Entity(
                typeName="spark_column",
                attributes={
                    "name": col_def["name"],
                    "qualifiedName": f"spark://{location}/{col_def['name']}",
                    "type": col_def["type"],
                    "description": col_def.get("description", ""),
                    "isPrimaryKey": col_def.get("is_primary_key", False),
                    "isNullable": col_def.get("nullable", True),
                },
                classifications=[
                    {"typeName": col_def["classification"]}
                ] if "classification" in col_def else []
            )
            columns.append(column_entity)

        # Register in catalog
        result = self.client.entity_post(table_entity)
        for col in columns:
            col.attributes["table"] = {"guid": result.guid}
            self.client.entity_post(col)

        return result.guid

    def add_lineage(
        self,
        source_guid: str,
        target_guid: str,
        process_name: str,
        transformation_logic: str
    ):
        """Record lineage relationship between datasets."""

        process_entity = Entity(
            typeName="spark_process",
            attributes={
                "name": process_name,
                "qualifiedName": f"spark_process://{process_name}",
                "description": transformation_logic,
                "inputs": [{"guid": source_guid}],
                "outputs": [{"guid": target_guid}],
                "startTime": datetime.utcnow().isoformat(),
            }
        )

        self.client.entity_post(process_entity)


# Usage Example
catalog = DataCatalogManager(
    atlas_url="http://atlas:21000",
    username="admin",
    password=os.environ["ATLAS_PASSWORD"]
)

# Register dataset with PII classification
customer_guid = catalog.register_dataset(
    name="customer_master",
    location="s3://data-lake/curated/customers/",
    schema=[
        {"name": "customer_id", "type": "STRING", "is_primary_key": True},
        {"name": "email", "type": "STRING", "classification": "PII"},
        {"name": "name", "type": "STRING", "classification": "PII"},
        {"name": "created_at", "type": "TIMESTAMP"},
    ],
    owner="data-platform-team",
    classification="CONFIDENTIAL",
    description="Master customer data with PII fields"
)
```

**Why compliant:** Integrates with enterprise data catalog (Apache Atlas), registers datasets with full metadata including schema and classifications, tracks data ownership, marks PII columns for compliance, and enables lineage tracking between datasets.

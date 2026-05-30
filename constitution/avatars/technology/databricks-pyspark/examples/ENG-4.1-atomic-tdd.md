---
law_id: ENG-4.1
avatar: databricks-pyspark
---

# ENG-4.1: Atomic TDD Examples for Databricks / PySpark

---

## COMPLIANT

One test. One transformation function. RED → GREEN → REFACTOR.

### Step 1 — RED: Write the failing test first

```python
# tests/test_offer_filter.py
import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType

from topml.transformations.offer_filter import apply_customer_offer_filter


@pytest.fixture(scope="session")
def spark() -> SparkSession:
    from delta import configure_spark_with_delta_pip
    builder = (
        SparkSession.builder
        .master("local[2]")
        .appName("topml-tests")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config(
            "spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        )
        .config("spark.sql.shuffle.partitions", "4")
    )
    return configure_spark_with_delta_pip(builder).getOrCreate()


@pytest.fixture()
def customers_delta(spark: SparkSession, tmp_path):
    """Ephemeral Delta table fixture with representative customer rows."""
    schema = StructType([
        StructField("customer_id_hash", StringType(), False),
        StructField("loyalty_tier", StringType(), False),
        StructField("marketing_opt_out", StringType(), False),
        StructField("account_status", StringType(), False),
    ])
    rows = [
        ("hash_001", "PLATINUM", "N", "ACTIVE"),   # eligible
        ("hash_002", "GOLD",     "N", "ACTIVE"),   # wrong tier
        ("hash_003", "PLATINUM", "Y", "ACTIVE"),   # opted out
        ("hash_004", "PLATINUM", "N", "SUSPENDED"),# wrong status
    ]
    path = str(tmp_path / "customer_segments")
    (
        spark.createDataFrame(rows, schema)
        .write.format("delta").save(path)
    )
    return spark.read.format("delta").load(path)


def test_apply_customer_offer_filter_returns_only_eligible_platinum(
    spark: SparkSession,
    customers_delta,
):
    # Arrange — fixture provides 4 rows; only hash_001 should survive
    customers = customers_delta

    # Act
    result = apply_customer_offer_filter(customers, offer_tier="PLATINUM")

    # Assert
    rows = result.collect()
    assert len(rows) == 1
    assert rows[0]["customer_id_hash"] == "hash_001"
```

Run it — **test fails** because `apply_customer_offer_filter` does not exist yet:

```bash
pytest tests/test_offer_filter.py::test_apply_customer_offer_filter_returns_only_eligible_platinum -v
# FAILED — ImportError: cannot import name 'apply_customer_offer_filter'
```

---

### Step 2 — GREEN: Write the minimum implementation to pass

```python
# src/topml/transformations/offer_filter.py
from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def apply_customer_offer_filter(
    customers: DataFrame,
    offer_tier: str,
    opt_out_flag: str = "Y",
) -> DataFrame:
    """Return customers eligible for an offer: correct tier, not opted out, account active."""
    return (
        customers
        .filter(F.col("loyalty_tier") == offer_tier)
        .filter(F.col("marketing_opt_out") != opt_out_flag)
        .filter(F.col("account_status") == "ACTIVE")
    )
```

Run it — **test passes**:

```bash
pytest tests/test_offer_filter.py::test_apply_customer_offer_filter_returns_only_eligible_platinum -v
# PASSED
```

---

### Step 3 — REFACTOR: Improve readability without changing behaviour

```python
# src/topml/transformations/offer_filter.py
from pyspark.sql import DataFrame
from pyspark.sql import functions as F

_OPT_OUT_VALUE = "Y"
_ACTIVE_STATUS = "ACTIVE"


def apply_customer_offer_filter(
    customers: DataFrame,
    offer_tier: str,
) -> DataFrame:
    """Return customers eligible for an offer: correct tier, not opted out, account active."""
    return (
        customers
        .filter(F.col("loyalty_tier") == offer_tier)
        .filter(F.col("marketing_opt_out") != _OPT_OUT_VALUE)
        .filter(F.col("account_status") == _ACTIVE_STATUS)
    )
```

Run the test again — still **passes**. Constants extracted; signature simplified. One test proves the refactor is safe.

---

## VIOLATION

### Multiple tests written before any implementation

```python
# tests/test_offer_pipeline.py  ← VIOLATION: entire test suite written upfront
def test_filter_returns_only_platinum(): ...
def test_filter_excludes_opted_out(): ...
def test_filter_excludes_suspended_accounts(): ...
def test_propensity_score_applied(): ...
def test_ranked_offers_are_top_n(): ...
def test_audit_log_written(): ...
# 6 failing tests; no implementation exists; violates RED-GREEN-REFACTOR cycle
```

### Test-after development

```python
# src/topml/pipelines/scoring_pipeline.py  ← written first, 200 lines
def run_offer_scoring_pipeline(spark, dbutils, target_date): ...

# tests/test_scoring_pipeline.py  ← written after, retrofitted
def test_run_offer_scoring_pipeline():
    # Arrange: enormous fixture to match the already-written function
    ...
```

Both patterns break ENG-4.1. Tests written after implementation do not drive design — they only confirm existing behaviour.

---

## TDD Cycle Commands

```bash
# RED: run the single new test, confirm it fails
pytest tests/test_offer_filter.py::test_apply_customer_offer_filter_returns_only_eligible_platinum -v

# GREEN: implement minimum code, run the same test
pytest tests/test_offer_filter.py::test_apply_customer_offer_filter_returns_only_eligible_platinum -v

# REFACTOR: clean up, run full suite to confirm nothing regressed
pytest tests/ -v

# Coverage check before opening a PR
pytest tests/ --cov=src --cov-report=term-missing
```

---
law_id: ENG-3.1
avatar: databricks-pyspark
---

# ENG-3.1: Complexity Limits Examples for Databricks / PySpark

---

## COMPLIANT

Each transformation function does exactly **one thing**, has cyclomatic complexity ≤ 10, and is independently testable. Complex pipelines are built by composing named pure functions.

### Chain of three single-purpose pure functions

```python
# src/topml/transformations/offer_filter.py
from pyspark.sql import DataFrame
from pyspark.sql import functions as F

_OPT_OUT_VALUE = "Y"
_ACTIVE_STATUS = "ACTIVE"


def filter_eligible_customers(
    customers: DataFrame,
    offer_tier: str,
) -> DataFrame:
    """Return only customers who are eligible for an offer: correct tier, active, not opted out.

    Cyclomatic complexity: 1 (no branches — declarative filter chain).
    """
    return (
        customers
        .filter(F.col("loyalty_tier") == offer_tier)
        .filter(F.col("marketing_opt_out") != _OPT_OUT_VALUE)
        .filter(F.col("account_status") == _ACTIVE_STATUS)
    )
```

```python
# src/topml/transformations/scoring.py
from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def apply_propensity_score(
    customers: DataFrame,
    scores: DataFrame,
) -> DataFrame:
    """Join pre-computed propensity scores onto the eligible customer set.

    Cyclomatic complexity: 1 (single join, no conditional branches).
    """
    return (
        customers
        .join(scores.select("customer_id_hash", "propensity_score"), on="customer_id_hash", how="left")
        .withColumn(
            "propensity_score",
            F.coalesce(F.col("propensity_score"), F.lit(0.0)),
        )
    )
```

```python
# src/topml/transformations/ranking.py
from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def rank_offers(customers_scored: DataFrame, top_n: int = 3) -> DataFrame:
    """Rank each customer's eligible offers by propensity score, returning the top N.

    Cyclomatic complexity: 1 (window function, no branches).
    """
    window = Window.partitionBy("customer_id_hash").orderBy(F.col("propensity_score").desc())
    return (
        customers_scored
        .withColumn("offer_rank", F.rank().over(window))
        .filter(F.col("offer_rank") <= top_n)
    )
```

### Pipeline composes named functions — readable and testable at each step

```python
# src/topml/pipelines/scoring_pipeline.py
from pyspark.sql import SparkSession

from topml.transformations.offer_filter import filter_eligible_customers
from topml.transformations.scoring import apply_propensity_score
from topml.transformations.ranking import rank_offers


def build_offer_candidates(
    spark: SparkSession,
    offer_tier: str,
    top_n: int = 3,
) -> None:
    customers = spark.table("main.marketing.customer_segments")
    scores    = spark.table("main.feature_store.customer_propensity_scores")

    eligible  = filter_eligible_customers(customers, offer_tier=offer_tier)
    scored    = apply_propensity_score(eligible, scores)
    ranked    = rank_offers(scored, top_n=top_n)

    ranked.write.format("delta").mode("append").saveAsTable("main.marketing.offer_candidates")
```

Each function can be unit-tested independently with a small DataFrame fixture. The pipeline is readable as English.

---

## VIOLATION

### Single `run_campaign()` function with 15+ conditional branches and mixed I/O

```python
# VIOLATION — src/topml/pipelines/campaign.py
def run_campaign(spark, dbutils, target_date, campaign_type, dry_run=False):
    # reads Delta
    customers = spark.table("main.marketing.customer_segments")

    # conditional on campaign_type — branch 1
    if campaign_type == "platinum_upgrade":
        customers = customers.filter(customers.loyalty_tier == "GOLD")
    elif campaign_type == "status_match":
        customers = customers.filter(customers.loyalty_tier == "SILVER")
    elif campaign_type == "win_back":
        customers = customers.filter(customers.account_status == "CHURNED")
    elif campaign_type == "birthday":
        customers = customers.filter(customers.birth_month == target_date[:7])
    else:
        raise ValueError(f"Unknown campaign_type: {campaign_type}")

    # calls model — branch 2, 3
    if campaign_type in ("platinum_upgrade", "status_match"):
        scores = _call_propensity_model(customers, dbutils)
    else:
        scores = customers.withColumn("score", F.lit(1.0))

    # ranking — branch 4, 5
    if campaign_type == "birthday":
        ranked = scores  # birthday campaigns: everyone gets one offer
    else:
        ranked = scores.orderBy(F.col("score").desc()).limit(50000)

    # writes output — side effect inside the function
    if not dry_run:
        ranked.write.format("delta").mode("append").saveAsTable("main.marketing.offer_candidates")

    # sends to email platform — another side effect
    if not dry_run and campaign_type != "win_back":
        api_key = dbutils.secrets.get("topml-kv-prod", "sendgrid-api-key")
        _send_to_sendgrid(ranked.toPandas(), api_key)

    # logs to stdout — not a durable audit record
    print(f"Campaign {campaign_type} sent {ranked.count()} offers on {target_date}")

    # more branches for reporting...
    if campaign_type == "platinum_upgrade":
        _write_campaign_report(spark, ranked, "upgrade_report")
    elif campaign_type == "birthday":
        _write_campaign_report(spark, ranked, "birthday_report")
```

This function has:
- Cyclomatic complexity > 15 (each `if/elif/else` adds a branch)
- Mixed I/O: reads Delta, calls a model API, writes Delta, calls SendGrid, prints to stdout
- Untestable without mocking all external systems simultaneously
- No way to test the ranking logic without triggering the email send

Violations of ENG-3.1: function does not do one thing, complexity exceeds limit, side effects prevent isolated testing.

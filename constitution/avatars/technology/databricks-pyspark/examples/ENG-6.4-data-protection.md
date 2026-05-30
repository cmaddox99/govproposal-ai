---
law_id: ENG-6.4
avatar: databricks-pyspark
---

# ENG-6.4: Data Protection Examples for Databricks / PySpark

---

## COMPLIANT

### 1. Unity Catalog column masking on PII fields

Column masks are defined as SQL functions and attached to table columns. Non-privileged users see masked values; members of `topml_pii_viewers` see the real value.

```sql
-- Create mask functions for each PII field
CREATE FUNCTION main.marketing.mask_customer_id(customer_id STRING)
  RETURNS STRING
  RETURN CASE
    WHEN is_account_group_member('topml_pii_viewers') THEN customer_id
    ELSE sha2(customer_id, 256)
  END;

CREATE FUNCTION main.marketing.mask_email_address(email_address STRING)
  RETURNS STRING
  RETURN CASE
    WHEN is_account_group_member('topml_pii_viewers') THEN email_address
    ELSE CONCAT(LEFT(email_address, 2), '***@***.***')
  END;

CREATE FUNCTION main.marketing.mask_loyalty_id(loyalty_id STRING)
  RETURNS STRING
  RETURN CASE
    WHEN is_account_group_member('topml_pii_viewers') THEN loyalty_id
    ELSE sha2(loyalty_id, 256)
  END;

-- Attach masks to the customer profile table
ALTER TABLE main.marketing.customer_profile
  ALTER COLUMN customer_id   SET MASK main.marketing.mask_customer_id;

ALTER TABLE main.marketing.customer_profile
  ALTER COLUMN email_address SET MASK main.marketing.mask_email_address;

ALTER TABLE main.marketing.customer_profile
  ALTER COLUMN loyalty_id    SET MASK main.marketing.mask_loyalty_id;
```

---

### 2. Row-level security via Unity Catalog row filter

Restrict which rows a user can see based on the data region they are authorised for:

```sql
-- Row filter: users see only rows for their authorised data region
CREATE FUNCTION main.marketing.filter_customer_region(data_region STRING)
  RETURNS BOOLEAN
  RETURN is_account_group_member('topml_global_access')
      OR array_contains(
           split(current_user_attribute('data_regions'), ','),
           data_region
         );

ALTER TABLE main.marketing.customer_profile
  SET ROW FILTER main.marketing.filter_customer_region ON (data_region);
```

---

### 3. Python Fernet encryption for external tokens before writing to Delta

When storing tokens that must be transmitted to external systems (e.g., a third-party email platform token), encrypt before writing to Delta:

```python
# src/topml/audit/offer_audit.py
import base64
import os
from cryptography.fernet import Fernet
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StringType


def encrypt_external_token(token: str, encryption_key: bytes) -> str:
    """Encrypt an external platform token with Fernet symmetric encryption."""
    f = Fernet(encryption_key)
    return f.encrypt(token.encode()).decode()


def write_offer_decisions_with_encrypted_tokens(
    spark: SparkSession,
    decisions_df: DataFrame,
    dbutils,
) -> None:
    encryption_key = dbutils.secrets.get(
        scope="topml-kv-prod",
        key="offer-token-encryption-key",
    ).encode()

    encrypt_udf = F.udf(
        lambda token: encrypt_external_token(token, encryption_key),
        StringType(),
    )

    encrypted_df = decisions_df.withColumn(
        "external_platform_token",
        encrypt_udf(F.col("external_platform_token")),
    )

    (
        encrypted_df.write
        .format("delta")
        .mode("append")
        .saveAsTable("main.marketing.offer_decisions")
    )
```

---

### 4. PII fields hashed with SHA-256 before writing to reporting tables

Reporting tables never contain raw PII. Hash all customer identifiers at the transformation layer:

```python
# src/topml/transformations/pii_hashing.py
from pyspark.sql import DataFrame
from pyspark.sql import functions as F

_PII_COLUMNS = ("customer_id", "email_address", "loyalty_id", "phone_number")


def hash_pii_columns(df: DataFrame) -> DataFrame:
    """Replace PII columns with SHA-256 hashes for reporting tables."""
    result = df
    for col_name in _PII_COLUMNS:
        if col_name in df.columns:
            result = result.withColumn(
                f"{col_name}_hash",
                F.sha2(F.col(col_name).cast("string"), 256),
            ).drop(col_name)
    return result
```

```python
# Usage in pipeline
from topml.transformations.pii_hashing import hash_pii_columns

reporting_df = hash_pii_columns(scored_customers)
reporting_df.write.format("delta").mode("append").saveAsTable("main.reporting.offer_scores")
```

---

## VIOLATION

### Writing raw PII to a Delta table without masking

```python
# VIOLATION — raw PII written directly to Delta, no masking, no hashing
(
    customers_df  # contains customer_id, email_address, loyalty_id in plaintext
    .write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("main.reporting.offer_candidates")
)
# Any user with SELECT on this table reads full PII
```

### No encryption on external tokens stored in Delta

```python
# VIOLATION — external platform token stored in plaintext
decisions_df = decisions_df.withColumn(
    "external_platform_token",
    F.lit(platform_token),  # plaintext token visible in Delta table scan
)
decisions_df.write.format("delta").mode("append").saveAsTable("main.marketing.offer_decisions")
# Token can be extracted by anyone with table access and replayed against the external platform
```

Both patterns violate ENG-6.4. Column masks, row filters, and field-level hashing are not optional for tables containing customer identity data — they are mandatory controls.

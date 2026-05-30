# PostgreSQL / SQLAlchemy (Async) Guidance

> **Purpose:** Stack-specific patterns for Python services using async PostgreSQL with SQLAlchemy 2.x and asyncpg. Covers session lifecycle, PII-encrypted columns, audit immutability, raw SQL migration governance, and testing strategy.

---

## Overview

Services using PostgreSQL via SQLAlchemy + asyncpg face patterns not covered by generic FastAPI guidance:

- **Async session lifecycle:** `AsyncSession` scoping across FastAPI request boundaries
- **asyncpg pool management:** Connection pool sizing, timeout configuration, health checks
- **PII-encrypted columns:** Encrypt at write, hash for lookup, key rotation governance
- **Audit immutability:** Trace tables must be append-only — UPDATE/DELETE forbidden by law (`BUS-7.1`)
- **Raw SQL migrations:** When Alembic is not used, raw `.sql` scripts need governance (versioning, idempotency, rollback)

---

## DBConnector Pattern

> **Per `ENG-6.1` (Security):** DB credentials must come from environment variables. Connection strings must never be serialized to logs.

### Recommended Structure

```python
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import logging

class DBConnector:
    """Single-responsibility DB connection manager. Per ENG-3.4 (SRP)."""

    def __init__(self):
        self._conn_string = (
            f"postgresql://{settings.db_user}:{settings.db_password}"
            f"@{settings.db_host}:{settings.db_port}/{settings.db_name}"
        )
        self._engine = None

    def connect(self):
        """Acquire engine; log status — NOT the connection string."""
        try:
            self._engine = create_engine(self._conn_string, pool_pre_ping=True)
            # Per ENG-6.1: log host + db only, never full DSN
            logging.info(f"DB connected: host={settings.db_host}, db={settings.db_name}")
        except SQLAlchemyError as e:
            logging.error(f"DB connection failed: host={settings.db_host}")
            raise

    def health_check(self) -> bool:
        """Return True if DB is reachable."""
        try:
            with self._engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception:
            return False
```

### Anti-Patterns

```python
# BAD — logs full connection string (contains password)
logging.info(f"Connecting: {self._conn_string}")

# BAD — credentials hardcoded
engine = create_engine("postgresql://admin:password123@prod-db:5432/mydb")

# BAD — no pool_pre_ping (silent stale connections in production)
engine = create_engine(conn_string)
```

---

## Async Session Lifecycle

> **Per `ENG-4.1` (Atomic TDD):** Async sessions must be injected as dependencies, not instantiated inside business logic, to enable unit testing.

### FastAPI Dependency Pattern

```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

# In config/database.py
async_engine = create_async_engine(
    f"postgresql+asyncpg://{settings.db_user}:{settings.db_password}"
    f"@{settings.db_host}:{settings.db_port}/{settings.db_name}",
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_pre_ping=True,   # detect stale connections
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# FastAPI dependency
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

# In router
@router.post("/response")
async def generate_response(session: AsyncSession = Depends(get_db_session)):
    ...
```

---

## PII-Encrypted Column Governance

> **Per `ENG-6.5` (Input Validation) and `BUS-7.1` (Audit Trail):** PII fields must be encrypted before write and hashed for audit lookups. The encryption key must never be logged.

### Encrypt-Before-Write Pattern

```python
from cryptography.fernet import Fernet
import hashlib, base64

def get_fernet() -> Fernet:
    """Load key from env — never hardcode. Per ENG-6.1."""
    key = os.getenv("PII_ENCRYPTION_KEY")
    if not key:
        raise RuntimeError("PII_ENCRYPTION_KEY not set")
    return Fernet(key.encode())

def encrypt_pii_field(value: str) -> str:
    """Encrypt a PII field value for storage."""
    return get_fernet().encrypt(value.encode()).decode()

def hash_pii_for_lookup(value: str) -> str:
    """Non-reversible SHA-256 hash for audit lookups (cannot recover original)."""
    salt = os.getenv("PII_ENCRYPTION_SALT", "")
    return hashlib.sha256(f"{salt}{value}".encode()).hexdigest()
```

### Column Naming Convention

| Column Type | Naming Pattern | Storage |
|-------------|---------------|---------|
| Encrypted PII value | `customer_name_encrypted` | Fernet ciphertext |
| PII lookup hash | `customer_name_hash` | SHA-256 hex digest |
| Non-PII audit field | `complaint_category` | Plaintext |

---

## Audit Immutability Pattern

> **Per `BUS-7.1` (Audit Trail):** Trace tables must be append-only. This is non-negotiable.

### Schema Design

```sql
-- scripts/create_traces_table.sql
CREATE TABLE IF NOT EXISTS traces (
    id              SERIAL PRIMARY KEY,
    tid             VARCHAR(255) NOT NULL,
    created_at      TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    model_deployment VARCHAR(100) NOT NULL,
    complaint_category VARCHAR(200),
    compensation_amount NUMERIC(10,2),
    pii_hash        VARCHAR(64),   -- SHA-256 hash, not cleartext PII
    outcome         VARCHAR(50),   -- 'accepted', 'edited', 'rejected'
    prompt_tokens   INT,
    completion_tokens INT,
    payload_hash    VARCHAR(64)    -- hash of system prompt for version tracking
    -- NO updated_at column — this table is append-only by design
);

-- Enforce immutability at DB level
CREATE RULE no_update_traces AS ON UPDATE TO traces DO INSTEAD NOTHING;
CREATE RULE no_delete_traces AS ON DELETE TO traces DO INSTEAD NOTHING;
```

### Insert-Only Pattern in Python

```python
async def write_trace(session: AsyncSession, event: dict) -> None:
    """Per BUS-7.1: INSERT only. Never UPDATE or DELETE trace records."""
    await session.execute(
        text("""
            INSERT INTO traces (tid, model_deployment, complaint_category,
                               compensation_amount, pii_hash, outcome,
                               prompt_tokens, completion_tokens)
            VALUES (:tid, :model, :category, :compensation,
                    :pii_hash, :outcome, :prompt_tokens, :completion_tokens)
        """),
        event,
    )
    # DO NOT call session.execute("UPDATE traces ...") — ever
```

---

## Raw SQL Migration Governance

When Alembic is not used, raw SQL migration scripts require governance:

### Required Properties per Migration Script

| Property | Requirement |
|----------|-------------|
| **Idempotent** | Must be safe to run twice (`IF NOT EXISTS`, `IF EXISTS`) |
| **Forward-only** | No DROP TABLE or destructive changes without explicit rollback companion |
| **Named with version prefix** | e.g., `001_create_traces_table.sql`, `002_add_hash_metadata.sql` |
| **Tested in CI** | Applied to a fresh PostgreSQL container in the integration test pipeline |

```sql
-- CORRECT: idempotent migration
ALTER TABLE traces ADD COLUMN IF NOT EXISTS payload_hash VARCHAR(64);

-- INCORRECT: destructive, not idempotent
ALTER TABLE traces ADD COLUMN payload_hash VARCHAR(64);  -- fails if column exists
```

---

## Test Pyramid for DB Code (ENG-4.2)

| Test Layer | What to Test | How |
|------------|-------------|-----|
| **Unit** | DBConnector init, health_check logic, PII encryption/decryption, hash generation | Mock `requests`, `SQLAlchemy` engine, `os.getenv` |
| **Integration** | Actual INSERT/SELECT against real schema; migration scripts | Docker Compose PostgreSQL; `pytest-asyncio` |
| **E2E** | Full request → DB write → audit trace present | Full app stack via `httpx.AsyncClient` |

```python
# Unit test — mock the session, test business logic only
async def test_write_trace_inserts_correct_fields(mock_session):
    event = {"tid": "t-001", "model": "gpt-4o", "outcome": "accepted", ...}
    await write_trace(mock_session, event)
    mock_session.execute.assert_called_once()
    call_args = mock_session.execute.call_args
    assert ":tid" in str(call_args)

# Integration test — use real PostgreSQL declared in conftest via Docker Compose
@pytest.mark.integration
async def test_trace_record_is_immutable(pg_session):
    await write_trace(pg_session, {"tid": "t-002", ...})
    await pg_session.commit()
    # Attempt UPDATE — should silently do nothing (DB rule applied)
    await pg_session.execute(text("UPDATE traces SET outcome='tampered' WHERE tid='t-002'"))
    row = (await pg_session.execute(text("SELECT outcome FROM traces WHERE tid='t-002'"))).fetchone()
    assert row.outcome == "accepted"  # unchanged
```

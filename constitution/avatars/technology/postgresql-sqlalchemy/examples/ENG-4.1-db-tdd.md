---
law_id: ENG-4.1
avatar: postgresql-sqlalchemy
---

# ENG-4.1: Atomic TDD Examples for PostgreSQL / SQLAlchemy (Async)

## COMPLIANT: Full TDD Cycle for DBConnector

```python
# tests/unit/test_db_connector.py
import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.exc import SQLAlchemyError
from app.status.database.db_connector import DBConnector


# ─────────────────────────────────────────────────────────────
# Step 1: RED — Write failing test for health_check behavior
# ─────────────────────────────────────────────────────────────

def test_health_check_returns_true_when_db_reachable():
    """DBConnector.health_check() returns True when SELECT 1 succeeds."""
    # GIVEN
    connector = DBConnector()
    mock_engine = MagicMock()
    mock_conn = MagicMock()
    mock_engine.connect.return_value.__enter__ = lambda s: mock_conn
    mock_engine.connect.return_value.__exit__ = MagicMock(return_value=False)
    connector._engine = mock_engine

    # WHEN
    result = connector.health_check()

    # THEN
    assert result is True
    mock_conn.execute.assert_called_once()


# Step 2: GREEN — Implement health_check() in DBConnector
# def health_check(self) -> bool:
#     try:
#         with self._engine.connect() as conn:
#             conn.execute(text("SELECT 1"))
#         return True
#     except Exception:
#         return False


# ─────────────────────────────────────────────────────────────
# Step 3: Next RED — health_check returns False on exception
# ─────────────────────────────────────────────────────────────

def test_health_check_returns_false_when_db_unreachable():
    """DBConnector.health_check() returns False (not raises) when DB is down."""
    # GIVEN
    connector = DBConnector()
    mock_engine = MagicMock()
    mock_engine.connect.side_effect = SQLAlchemyError("connection refused")
    connector._engine = mock_engine

    # WHEN
    result = connector.health_check()

    # THEN — must return False, not raise
    assert result is False


# Step 4: GREEN — ensure except clause returns False


# ─────────────────────────────────────────────────────────────
# Step 5: Security RED — connection string must never be logged
# ─────────────────────────────────────────────────────────────

def test_connect_does_not_log_connection_string(caplog):
    """Per ENG-6.1: DB connection string (with password) must never appear in logs."""
    import logging
    with patch.dict("os.environ", {
        "DB_HOST": "prod-db.internal",
        "DB_PORT": "5432",
        "DB_NAME": "cr_ops",
        "DB_USER": "appuser",
        "DB_PASSWORD": "super-secret-pw",
        "DB_SCHEMA": "public",
    }):
        with patch("app.status.database.db_connector.create_engine"):
            connector = DBConnector()
            with caplog.at_level(logging.DEBUG):
                try:
                    connector.connect()
                except Exception:
                    pass

    # THEN — password must not appear in any log record
    assert "super-secret-pw" not in caplog.text
    # Per ENG-6.1: full connection string must not be serialized to logs
    assert "postgresql://appuser:super-secret-pw" not in caplog.text


# Step 6: GREEN — ensure logging.info only references host and db name


# ─────────────────────────────────────────────────────────────
# Step 7: Audit immutability RED — PII hash written correctly
# ─────────────────────────────────────────────────────────────

def test_hash_pii_for_lookup_is_deterministic_and_non_reversible():
    """Per BUS-7.1: PII hash must be deterministic and non-reversible."""
    from app.status.utilities.pii_hasher import hash_pii_for_lookup

    # GIVEN
    with patch.dict("os.environ", {"PII_ENCRYPTION_SALT": "test-salt"}):
        # WHEN
        hash1 = hash_pii_for_lookup("Maria Torres")
        hash2 = hash_pii_for_lookup("Maria Torres")
        hash_different = hash_pii_for_lookup("John Smith")

        # THEN — deterministic
        assert hash1 == hash2
        # Different inputs → different hashes
        assert hash1 != hash_different
        # Non-reversible — original value cannot be recovered from hash
        assert "Maria Torres" not in hash1
        assert len(hash1) == 64  # SHA-256 hex digest length


# Step 8: GREEN — implement hash_pii_for_lookup with HMAC-SHA256
```

## VIOLATION: Session Leaked Outside Request Boundary

```python
# BAD — session created inside business logic (untestable, scope leaked)
async def write_trace(event: dict):
    engine = create_async_engine(conn_string)   # new engine per call — resource leak
    async with AsyncSession(engine) as session:
        await session.execute(...)
        await session.commit()

# BAD — UPDATE on audit trace (violates BUS-7.1)
async def correct_trace(tid: str, new_outcome: str, session: AsyncSession):
    await session.execute(
        text("UPDATE traces SET outcome=:outcome WHERE tid=:tid"),
        {"outcome": new_outcome, "tid": tid}
    )
```

**Why non-compliant:** Creating an engine per call leaks resources and bypasses pool management. Injecting the session as a dependency is required for testability (`ENG-4.1`). UPDATE on trace records violates `BUS-7.1` audit immutability law.

---
laws: [ENG-6.1, ENG-6.4, ENG-6.7]
avatar: [postgresql-sqlalchemy]
title: Security Laws — PostgreSQL / SQLAlchemy
---

# Security Laws: ENG-6.1, ENG-6.4, ENG-6.7 — PostgreSQL / SQLAlchemy

## ENG-6.1: Security by Design

Load DB credentials from environment. Use a least-privilege application role. Enforce TLS for all connections.

```python
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# ✅ Credentials from env vars — never hardcoded, never in alembic.ini
DATABASE_URL = os.environ["DATABASE_URL"]
# e.g. postgresql+asyncpg://app_role:${DB_PASSWORD}@db.internal:5432/aa_bookings?ssl=require

engine = create_async_engine(
    DATABASE_URL,
    connect_args={"ssl": "require"},   # TLS enforced
    pool_pre_ping=True,
)

# ❌ NEVER
# engine = create_async_engine("postgresql+asyncpg://admin:SuperSecret@localhost/aa_bookings")
```

DB role grants — least privilege (application role has no DDL):

```sql
-- Run once during provisioning (not in application code)
CREATE ROLE app_role LOGIN PASSWORD '...'; -- password from Vault
GRANT SELECT, INSERT, UPDATE ON bookings, passengers, flights TO app_role;
-- No GRANT CREATE TABLE, DROP TABLE, or DELETE ON audit_log

CREATE ROLE migration_role LOGIN PASSWORD '...';
GRANT ALL PRIVILEGES ON DATABASE aa_bookings TO migration_role;
```

SQLAlchemy ORM prevents injection by default — never concatenate user input into raw SQL:

```python
# ✅ Safe: ORM / parameterized
result = await session.execute(
    select(Booking).where(Booking.pnr == pnr_input)
)

# ❌ SQL injection vulnerability
result = await session.execute(
    text(f"SELECT * FROM bookings WHERE pnr = '{pnr_input}'")
)
```

## ENG-6.4: Data Protection

Encrypt PII columns using a custom `TypeDecorator` with AES-GCM. Key from environment.

```python
import os, base64
from sqlalchemy import TypeDecorator, String
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import secrets

class EncryptedString(TypeDecorator):
    impl = String
    cache_ok = True

    def __init__(self):
        super().__init__()
        key_b64 = os.environ["PII_ENCRYPTION_KEY"]   # 32-byte key, base64-encoded
        self._gcm = AESGCM(base64.b64decode(key_b64))

    def process_bind_param(self, value, dialect):
        if value is None: return None
        nonce = secrets.token_bytes(12)
        ct = self._gcm.encrypt(nonce, value.encode(), None)
        return base64.b64encode(nonce + ct).decode()

    def process_result_value(self, value, dialect):
        if value is None: return None
        raw = base64.b64decode(value)
        return self._gcm.decrypt(raw[:12], raw[12:], None).decode()

class Passenger(Base):
    __tablename__ = "passengers"
    id    = Column(Integer, primary_key=True)
    email = Column(EncryptedString(), nullable=False)   # PII — encrypted at rest
    name  = Column(EncryptedString(), nullable=False)   # PII — encrypted at rest
    pnr   = Column(String(6), nullable=False)           # booking key
```

Never log PII column values:

```python
# ✅ Log only safe identifiers
logger.info("passenger_created", passenger_id=passenger.id, pnr=passenger.pnr)
# ❌ NEVER: logger.info("created %s", passenger.email)
```

Run Alembic migrations under the `migration_role` (separate from `app_role`):

```ini
# alembic.ini — no password; injected at runtime
sqlalchemy.url = %(DATABASE_MIGRATION_URL)s
```

## ENG-6.7: Audit Trail

Append-only audit table enforced at the PostgreSQL level. Correlation ID propagated through SQLAlchemy session.

```sql
-- Prevent UPDATE and DELETE at the DB level
CREATE TABLE booking_audit (
    id             BIGSERIAL PRIMARY KEY,
    recorded_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    actor_id       TEXT NOT NULL,
    action         TEXT NOT NULL,          -- REBOOK, CANCEL, UPGRADE
    entity_id      TEXT NOT NULL,          -- PNR or booking UUID
    payload_hash   TEXT NOT NULL,          -- SHA-256 of the change payload
    correlation_id TEXT NOT NULL
);

CREATE RULE no_update_audit AS ON UPDATE TO booking_audit DO INSTEAD NOTHING;
CREATE RULE no_delete_audit AS ON DELETE TO booking_audit DO INSTEAD NOTHING;
REVOKE UPDATE, DELETE ON booking_audit FROM app_role;
```

```python
import hashlib, json

async def write_audit(session: AsyncSession, actor_id: str, action: str,
                       entity_id: str, payload: dict, correlation_id: str) -> None:
    payload_hash = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
    entry = BookingAudit(
        actor_id=actor_id, action=action,
        entity_id=entity_id, payload_hash=payload_hash,
        correlation_id=correlation_id,
    )
    session.add(entry)   # INSERT only — no session.merge() or session.execute(update(...))
    await session.flush()
```

## Anti-Patterns

1. **`DATABASE_URL` containing password in application code** — a hardcoded connection string is committed to Git and visible in process listings (`ps aux`); use env vars or Vault.
2. **Raw SQL with f-strings** — `text(f"SELECT * FROM flights WHERE id = '{flight_id}'")` enables SQL injection even with async SQLAlchemy; always use bound parameters.
3. **Logging `result.scalars().all()` when results contain PII** — logging the full ORM result set prints decrypted email and name fields; log counts or IDs only.
4. **`UPDATE` rows in audit table** — any application-layer update (even via ORM) on `booking_audit` destroys the evidentiary chain; the PostgreSQL RULE and REVOKE provide defence-in-depth.
5. **No TLS for DB connection** — omitting `sslmode=require` on internal networks exposes queries containing PNR and passenger data to network sniffing on the same VLAN.

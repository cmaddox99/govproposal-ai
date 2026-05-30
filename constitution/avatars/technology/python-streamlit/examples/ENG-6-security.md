---
laws: [ENG-6.1, ENG-6.4, ENG-6.7]
avatar: [python-streamlit]
title: Security Laws — Python Streamlit
---

# Security Laws: ENG-6.1, ENG-6.4, ENG-6.7 — Python Streamlit

## ENG-6.1: Security by Design

Load secrets via Streamlit's secrets management or environment variables. Authenticate users via SSO before any data is rendered. Validate all widget inputs.

```toml
# .streamlit/secrets.toml  (gitignored — never committed)
[database]
url = "postgresql://..."

[api]
aa_internal_api_key = "..."
```

```python
# app.py
import streamlit as st
import os

# ✅ Read from Streamlit secrets (backed by env vars in production)
DB_URL      = st.secrets["database"]["url"]
API_KEY     = st.secrets["api"]["aa_internal_api_key"]

# ❌ NEVER
# API_KEY = "sk-abc123..."
```

Enforce SSO before rendering any data:

```python
from streamlit_oauth import OAuth2Component    # example SSO integration

def require_auth() -> dict:
    if "user" not in st.session_state:
        oauth = OAuth2Component(...)
        result = oauth.authorize_button("Sign in with AA SSO", ...)
        if result and "token" in result:
            st.session_state["user"] = decode_token(result["token"])
        else:
            st.stop()    # ✅ halt rendering until authenticated
    return st.session_state["user"]

user = require_auth()
```

Validate widget inputs before passing to business logic:

```python
pnr_input = st.text_input("Enter PNR")
if pnr_input:
    import re
    if not re.match(r'^[A-Z]{6}$', pnr_input.strip()):
        st.error("Invalid PNR format — must be 6 uppercase letters")
        st.stop()
    results = fetch_booking(pnr_input.strip())
```

## ENG-6.4: Data Protection

Never display raw PII in Streamlit tables. Never cache DataFrames containing PII. Filter before rendering.

```python
import pandas as pd

def mask_passenger_df(df: pd.DataFrame) -> pd.DataFrame:
    """Return display-safe version — mask PII columns."""
    safe = df.copy()
    if "email" in safe.columns:
        safe["email"] = safe["email"].str.replace(r'(.{2}).*(@.*)', r'\1***\2', regex=True)
    if "name" in safe.columns:
        safe["name"] = safe["name"].apply(lambda n: n.split()[0][0] + ". " + n.split()[-1])
    return safe

# ✅ Display masked view only
st.dataframe(mask_passenger_df(passenger_df))

# ❌ NEVER: st.write(raw_passenger_df)
# ❌ NEVER: st.dataframe(df_with_emails_and_names)
```

Do not cache PII DataFrames with `@st.cache_data`:

```python
# ❌ Cached to disk — PII persists across sessions
@st.cache_data
def load_passenger_data(pnr: str) -> pd.DataFrame: ...

# ✅ Short-lived session state only — no disk cache for PII
def load_passenger_data(pnr: str) -> pd.DataFrame:
    return api_client.get_booking(pnr)    # fetched fresh, not cached
```

## ENG-6.7: Audit Trail

Log every user session with filters applied and export actions. Use structlog for structured output. Never log data values.

```python
import structlog, datetime

log = structlog.get_logger()

def log_session_action(action: str, user: dict, metadata: dict) -> None:
    log.info(
        action,
        user_id       = user["employee_id"],
        timestamp     = datetime.datetime.utcnow().isoformat(),
        correlation_id= st.session_state.get("correlation_id", ""),
        **metadata,
        # ❌ NEVER include actual data values: passenger_names, pnr_list, etc.
    )

# Log filter application
log_session_action("filter_applied", user,
    {"filter_type": "departure_date", "flight_count_returned": len(results)})

# Log export action (append-only audit)
if st.button("Export to CSV"):
    log_session_action("data_export", user,
        {"row_count": len(display_df), "export_format": "csv"})
    st.download_button("Download", data=csv_bytes, file_name="report.csv")
```

Append-only audit store for export events:

```python
async def record_export_audit(user_id: str, row_count: int,
                               correlation_id: str) -> None:
    await db.execute(
        "INSERT INTO streamlit_audit (user_id, action, row_count, correlation_id, recorded_at) "
        "VALUES (:uid, 'EXPORT', :rc, :cid, now())",
        {"uid": user_id, "rc": row_count, "cid": correlation_id},
    )
    # INSERT only — no UPDATE on streamlit_audit rows
```

## Anti-Patterns

1. **`st.write(df)` with PII columns visible** — Streamlit renders DataFrames as interactive HTML tables; passenger names and emails are exposed to anyone with app access.
2. **Hardcoded API keys in `app.py`** — keys in source code are committed to Git and visible in any container image layer; use `.streamlit/secrets.toml` (gitignored) or env vars.
3. **`@st.cache_data` on PII DataFrames** — Streamlit's disk-backed cache persists data across sessions and users; a PII DataFrame cached this way is readable by subsequent users.
4. **No authentication on internal tools with sensitive data** — Streamlit apps default to public access; any tool that queries flight ops or passenger data must be behind SSO before the first `st.dataframe()` call.
5. **Logging full query results** — `logger.info("results: %s", df.to_dict())` prints every row including PII fields to the log aggregator.

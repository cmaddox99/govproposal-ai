> Examples for: skill-10-security-review  
> Parent skill: 10-security-review.md  
> These are optional pedagogical supplements — not in governance scope.

---

## OWASP Top 10 (2021)

### A01: Broken Access Control

**Risk:** Users act outside intended permissions.

**Vulnerabilities:**
- Missing access control checks
- Insecure direct object references (IDOR)
- CORS misconfiguration
- Force browsing to authenticated pages

**Mitigations:**
```python
# BAD - No authorization check
@app.get("/users/{user_id}/profile")
def get_profile(user_id: int):
    return db.get_user(user_id)

# GOOD - Authorization verified
@app.get("/users/{user_id}/profile")
def get_profile(user_id: int, current_user: User = Depends(get_current_user)):
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Access denied")
    return db.get_user(user_id)
```

**Test:**
```python
def test_user_cannot_access_other_users_profile():
    # Given user A is authenticated
    # When user A requests user B's profile
    # Then access should be denied with 403
```

---

### A02: Cryptographic Failures

**Risk:** Sensitive data exposed due to weak or missing encryption.

**Vulnerabilities:**
- Transmitting data in cleartext
- Using weak algorithms (MD5, SHA1 for passwords)
- Hard-coded keys or secrets
- Missing encryption at rest

**Mitigations:**
```python
# BAD - Weak password hashing
password_hash = hashlib.md5(password.encode()).hexdigest()

# GOOD - Strong password hashing
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
password_hash = pwd_context.hash(password)
```

**Checklist:**
- [ ] TLS 1.2+ for all transmissions
- [ ] Strong algorithms (AES-256, bcrypt, Argon2)
- [ ] Secrets in environment variables or vault
- [ ] Encryption at rest for sensitive data

---

### A03: Injection

**Risk:** Untrusted data sent to interpreter as command/query.

**Vulnerabilities:**
- SQL injection
- NoSQL injection
- Command injection
- LDAP injection

**Mitigations:**
```python
# BAD - SQL injection vulnerability
query = f"SELECT * FROM users WHERE email = '{email}'"
cursor.execute(query)

# GOOD - Parameterized query
query = "SELECT * FROM users WHERE email = %s"
cursor.execute(query, (email,))

# BETTER - ORM
user = db.query(User).filter(User.email == email).first()
```

**Test:**
```python
def test_sql_injection_prevented():
    malicious_email = "'; DROP TABLE users; --"
    response = client.get(f"/users?email={malicious_email}")
    # Should not execute injection, should return empty or error
    assert User.query.count() > 0  # Table still exists
```

---

### A04: Insecure Design

**Risk:** Missing or ineffective security controls in design.

**Vulnerabilities:**
- No rate limiting
- Missing fraud detection
- Insecure password recovery
- Trust boundaries not defined

**Mitigations:**
```python
# Rate limiting
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.post("/login")
@limiter.limit("5/minute")
def login(credentials: LoginRequest):
    ...

# Account lockout
if failed_attempts >= 5:
    lock_account_temporarily(user)
    notify_user_of_suspicious_activity(user)
```

**Threat Model Questions:**
1. What are we building?
2. What can go wrong?
3. What are we doing about it?
4. Did we do a good job?

---

### A05: Security Misconfiguration

**Risk:** Insecure default configurations or missing hardening.

**Vulnerabilities:**
- Default credentials
- Unnecessary features enabled
- Overly verbose error messages
- Missing security headers

**Mitigations:**
```python
# Security headers middleware
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response

# Production error handling
@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    # Don't expose internal details
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal error occurred"}
    )
```

---

### A06: Vulnerable and Outdated Components

**Risk:** Using components with known vulnerabilities.

**Mitigations:**
```bash
# Python - check for vulnerabilities
pip-audit

# JavaScript - check for vulnerabilities
npm audit

# Automated dependency updates
# Use Dependabot, Renovate, or Snyk
```

**Process:**
- [ ] Regular dependency audits (weekly)
- [ ] Automated security scanning in CI/CD
- [ ] Subscribe to security advisories
- [ ] Defined process for critical updates

---

### A07: Identification and Authentication Failures

**Risk:** Weak authentication allows attackers to assume identities.

**Vulnerabilities:**
- Weak password policies
- Missing multi-factor authentication
- Session fixation
- Credential stuffing susceptibility

**Mitigations:**
```python
# Password policy
def validate_password(password: str) -> bool:
    if len(password) < 12:
        raise ValueError("Password must be at least 12 characters")
    if not re.search(r"[A-Z]", password):
        raise ValueError("Password must contain uppercase letter")
    if not re.search(r"[a-z]", password):
        raise ValueError("Password must contain lowercase letter")
    if not re.search(r"\d", password):
        raise ValueError("Password must contain number")
    if password in common_passwords:
        raise ValueError("Password is too common")
    return True

# Session management
@app.post("/login")
def login(credentials: LoginRequest, response: Response):
    user = authenticate(credentials)
    # Regenerate session on login
    session_id = generate_secure_session_id()
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=3600
    )
```

---

### A08: Software and Data Integrity Failures

**Risk:** Code or data modified without integrity verification.

**Vulnerabilities:**
- Unsigned updates
- Insecure deserialization
- CI/CD pipeline compromise
- Missing integrity checks

**Mitigations:**
```python
# Verify signatures on external data
def verify_webhook(payload: bytes, signature: str, secret: str) -> bool:
    expected = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)

# Avoid insecure deserialization
# BAD
data = pickle.loads(untrusted_input)

# GOOD
data = json.loads(untrusted_input)
validated_data = MySchema.parse_obj(data)
```

---

### A09: Security Logging and Monitoring Failures

**Risk:** Attacks go undetected due to insufficient logging.

**Mitigations:**
```python
# Security event logging
import structlog
logger = structlog.get_logger()

def login(credentials: LoginRequest):
    user = db.get_user_by_email(credentials.email)

    if not user:
        logger.warning("login_failed",
            reason="user_not_found",
            email=credentials.email,
            ip=request.client.host)
        raise HTTPException(401)

    if not verify_password(credentials.password, user.password_hash):
        logger.warning("login_failed",
            reason="invalid_password",
            user_id=user.id,
            ip=request.client.host)
        increment_failed_attempts(user)
        raise HTTPException(401)

    logger.info("login_success",
        user_id=user.id,
        ip=request.client.host)
    return create_session(user)
```

**What to log:**
- Authentication events (success/failure)
- Authorization failures
- Input validation failures
- Security-relevant errors
- Admin actions

---

### A10: Server-Side Request Forgery (SSRF)

**Risk:** Server makes requests to unintended locations.

**Mitigations:**
```python
# Validate URLs before fetching
from urllib.parse import urlparse
import ipaddress

ALLOWED_HOSTS = ["api.trusted-service.com"]
BLOCKED_NETWORKS = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
]

def validate_url(url: str) -> bool:
    parsed = urlparse(url)

    # Check allowed hosts
    if parsed.hostname not in ALLOWED_HOSTS:
        raise ValueError(f"Host not allowed: {parsed.hostname}")

    # Resolve and check IP
    ip = ipaddress.ip_address(socket.gethostbyname(parsed.hostname))
    for network in BLOCKED_NETWORKS:
        if ip in network:
            raise ValueError(f"IP in blocked network: {ip}")

    return True
```

---

## Good Examples

### Example 1: Secure Feature Design

```markdown
# Feature: Password Reset

## Threat Model

### Spoofing
- Risk: Attacker requests reset for victim's account
- Mitigation: Token sent only to verified email

### Information Disclosure
- Risk: Timing attack reveals valid emails
- Mitigation: Constant-time response regardless of email existence

### Denial of Service
- Risk: Flood reset requests
- Mitigation: Rate limit to 3 requests per email per hour

## Security Controls
- [ ] Cryptographically random token (32 bytes)
- [ ] Token expires in 1 hour
- [ ] Token invalidated after use
- [ ] Old tokens invalidated on new request
- [ ] Rate limiting enforced
- [ ] Constant-time email lookup
```

---

## Bad Examples (Anti-Patterns)

### Anti-Pattern 1: Security Through Obscurity

```python
# BAD - Hidden admin endpoint
@app.get("/super-secret-admin-panel-2024")
def admin_panel():
    return admin_data  # No authentication!
```

**Correct approach:** Proper authentication and authorization.

---

### Anti-Pattern 2: Client-Side Security Only

```javascript
// BAD - Validation only on client
if (user.role === 'admin') {
    showAdminPanel();
}
// Attacker can modify JavaScript to bypass
```

**Correct approach:** Server-side authorization always.

---


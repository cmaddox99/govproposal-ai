---
skill:
  id: skill-10-security-review
  name: Security Review
  category: security
  version: "2.0.0"

laws:
  implements:
    - id: ENG-6.1
      title: Security by Design Law (NON-NEGOTIABLE)
    - id: ENG-6.2
      title: Authentication Law
    - id: ENG-6.3
      title: Authorization Law
    - id: ENG-6.4
      title: Data Protection Law (NON-NEGOTIABLE)
    - id: ENG-6.5
      title: Input Validation Law
    - id: ENG-6.7
      title: Audit Trail Law (NON-NEGOTIABLE)
  references:
    - id: BUS-2.2
      title: TSA Security Compliance Law

triggers:
  phrases:
    - "Security review"
    - "Check for vulnerabilities"
    - "OWASP compliance"
    - "Threat modeling"

followed_by:
  - skill-08-code-review
  - skill-27-constitution-compliance
---

# Skill: Security Review

> **Purpose:** Identify and mitigate security vulnerabilities through systematic threat modeling and secure coding practices.

---

## Purpose

Security Review is the disciplined practice of identifying, assessing, and mitigating security risks in software. This skill ensures:

1. **Proactive threat identification** - Find vulnerabilities before attackers do
2. **OWASP compliance** - Address the most critical web application security risks
3. **Defense in depth** - Multiple layers of security controls
4. **Secure by design** - Security built in, not bolted on
5. **Compliance readiness** - Meet regulatory and industry requirements

**Key principle:** Security is everyone's responsibility. Every feature, every change, every review.

---

## When to Invoke

Invoke this skill when:

- Designing new features that handle user data
- Implementing authentication or authorization
- Processing payments or sensitive information
- Integrating with external services or APIs
- Reviewing code that touches security boundaries
- Preparing for security audits or penetration tests

**Trigger phrases:**
- "Is this secure?"
- "What are the security implications?"
- "Let's do a threat model"
- "Review this for vulnerabilities"
- "Check for OWASP issues"

---

## Constitutional Foundation

### Engineering Constitution
- **Article V, Section 5.1** - Security: No known vulnerabilities shipped
- **Article V, Section 5.2** - Defense in Depth: Multiple security layers
- **Article IV, Section 4.1** - Test-First: Security tests before implementation

### Product Constitution
- **Article VI, Section 6.1** - User Trust: Protect user data and privacy

### Business Constitution
- **Article III, Section 3.1** - Compliance: Meet regulatory requirements
- **Article III, Section 3.2** - Data Protection: Handle data responsibly

---

## Method: Security Review Process

### Step 1: Threat Modeling (STRIDE)

| Threat | Question | Example |
|--------|----------|---------|
| **S**poofing | Can attacker pretend to be someone else? | Fake authentication |
| **T**ampering | Can attacker modify data? | Man-in-the-middle |
| **R**epudiation | Can attacker deny actions? | Missing audit logs |
| **I**nformation Disclosure | Can attacker access private data? | Data leaks |
| **D**enial of Service | Can attacker disrupt service? | Resource exhaustion |
| **E**levation of Privilege | Can attacker gain more access? | Privilege escalation |

### Step 2: Code Review for Security

**Checklist:**
- [ ] Input validation on all external data
- [ ] Output encoding to prevent XSS
- [ ] Parameterized queries for database access
- [ ] Authorization checks on all protected resources
- [ ] Secrets not hardcoded
- [ ] Error handling doesn't leak information
- [ ] Logging of security events
- [ ] Rate limiting on sensitive endpoints

### Step 3: Security Testing

```python
# Security test examples
class TestSecurityControls:

    def test_authentication_required(self):
        response = client.get("/api/protected")
        assert response.status_code == 401

    def test_authorization_enforced(self):
        # User A can't access User B's data
        token_a = login_as("user_a")
        response = client.get("/api/users/user_b/data",
                             headers={"Authorization": f"Bearer {token_a}"})
        assert response.status_code == 403

    def test_rate_limiting(self):
        for _ in range(10):
            response = client.post("/api/login", json={"email": "x", "password": "y"})
        assert response.status_code == 429  # Too Many Requests

    def test_xss_prevention(self):
        malicious = "<script>alert('xss')</script>"
        response = client.post("/api/comments", json={"text": malicious})
        # Response should be escaped
        assert "<script>" not in response.json()["text"]
```

---

## Quality Checklist

Before considering security review complete:

### OWASP Top 10
- [ ] A01: Access control verified
- [ ] A02: Cryptography reviewed
- [ ] A03: Injection prevented
- [ ] A04: Secure design patterns used
- [ ] A05: Configuration hardened
- [ ] A06: Dependencies scanned
- [ ] A07: Authentication robust
- [ ] A08: Integrity verified
- [ ] A09: Logging adequate
- [ ] A10: SSRF prevented

### Process
- [ ] Threat model documented
- [ ] Security tests written
- [ ] Secrets properly managed
- [ ] Security headers configured

---

## Skill Interactions

### Preceded By
- **08-Code Review** - Initial review may identify security concerns

### Followed By
- **06-Atomic TDD** - Security tests implemented via TDD

### Related Skills
- **11-Incident Response** - When security issues are exploited
- **12-API Design** - API security patterns

> 📎 Examples: See 10-security-review-examples.md

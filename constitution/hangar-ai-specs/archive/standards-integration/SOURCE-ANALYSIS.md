# Source Document Analysis: Standards Integration

This document analyzes the Security and Compliance Adoption and Technology Standards Adoption documents to identify:
- **Universal Laws**: Rules that apply to ALL projects without exception
- **Law Enrichments**: Additional requirements for existing laws
- **Exception-Prone Rules**: Context-dependent rules documented here (not as laws)
- **Avatar Examples**: Technology-specific implementations

---

## Classification Criteria

### What Qualifies as a Universal Law?

| Criteria | Must Pass |
|----------|-----------|
| Applies to ALL projects | ✅ |
| No valid business exception | ✅ |
| Violation is always a defect | ✅ |
| Security/quality non-negotiable | ✅ |

### What Belongs in Exception Documentation?

| Criteria | Any Match |
|----------|-----------|
| Technology/vendor specific | ⚠️ |
| Valid business exceptions exist | ⚠️ |
| Legacy integration scenarios | ⚠️ |
| Context-dependent application | ⚠️ |

---

## Exception-Prone Rules

The following rules from source documents are **NOT universal laws** and should be handled via the Architecture Review Board (ARB) exception process.

### 1. Technology Stack Choices

These are **organizational standards**, not universal engineering laws. Valid exceptions may exist.

#### 1.1 Database Technology Restrictions

| Rule | Source | Valid Exception Scenarios |
|------|--------|---------------------------|
| PostgreSQL as only SQL DB | Tech Standards #3 | Legacy Oracle/SQL Server migrations, vendor-mandated databases, specialized use cases (TimescaleDB for time-series) |
| MongoDB as only NoSQL DB | Tech Standards #4 | Redis for caching, DynamoDB for serverless, Elasticsearch for search, Cassandra for specific workloads |

**Exception Request Requirements:**
- Technical justification with alternatives analysis
- Security assessment of alternative technology
- Migration path to standard technology (if applicable)
- Support and maintenance plan

#### 1.2 Frontend Framework Restrictions

| Rule | Source | Valid Exception Scenarios |
|------|--------|---------------------------|
| React or Angular only | Tech Standards #2 | Embedded systems (smaller frameworks), internal tools (simpler solutions), acquired products, mobile apps (React Native/Flutter) |
| TypeScript required | Tech Standards #2 | Legacy JavaScript codebases (migration timeline), third-party library constraints |

**Exception Request Requirements:**
- Business case for alternative
- Security and accessibility compliance plan
- Component reusability strategy

#### 1.3 CI/CD Platform Restrictions

| Rule | Source | Valid Exception Scenarios |
|------|--------|---------------------------|
| GitHub Actions only | Tech Standards #6 | Multi-cloud deployments requiring cloud-native CI/CD, legacy Jenkins pipelines (migration timeline), air-gapped environments |
| GitHub Enterprise Cloud only | Tech Standards #7 | Air-gapped/offline environments, acquisition integration |

**Exception Request Requirements:**
- Security scanning equivalent implementation
- Audit logging compliance
- Migration timeline to standard platform

#### 1.4 Operating System Restrictions

| Rule | Source | Valid Exception Scenarios |
|------|--------|---------------------------|
| Ubuntu as only server OS | Tech Standards #10 | Windows-only vendor software, specialized appliances, mainframe integration, RHEL vendor requirements |

**Exception Request Requirements:**
- Security hardening equivalent
- Patch management plan
- Configuration management approach

### 2. Network/Infrastructure Rules

These rules have valid technical exceptions based on architecture context.

#### 2.1 CDN/WAF Specific Rules

| Rule | Source | Valid Exception Scenarios |
|------|--------|---------------------------|
| Traffic must use port 80/443 only | Akamai Policy #4 | Internal services not using Akamai, legacy integrations requiring custom ports, WebSocket connections |
| Origin must use approved port ranges | Akamai Policy #5 | Backend services with non-standard ports, legacy application integration |

**When This Applies:** Only for applications using Akamai CDN/WAF
**Not Applicable To:** Internal services, non-web applications, services behind other WAF solutions

#### 2.2 Network Connectivity Rules

| Rule | Source | Valid Exception Scenarios |
|------|--------|---------------------------|
| No direct internet connection without firewall | Network Policy #8 | Air-gapped test environments, isolated development networks |

**Exception Request Requirements:**
- Network architecture diagram
- Compensating security controls
- Risk assessment approval

### 3. Process and Operational Rules

These rules may have context-dependent application timing.

#### 3.1 Training and Access Rules

| Rule | Source | Valid Exception Scenarios |
|------|--------|---------------------------|
| Training before code contribution | Security #10 | New hire onboarding grace period (30 days max), emergency contractor access (with supervision) |
| Annual training completion | Security #10 | Medical leave, extended absence (completion within 30 days of return) |

**Note:** Training requirement is still mandatory; timing may have grace periods.

#### 3.2 Production Access Rules

| Rule | Source | Valid Exception Scenarios |
|------|--------|---------------------------|
| Ad-hoc queries prohibited on production | Database Policy #13 | Emergency incident response (with approval and audit), compliance investigations (legal requirement) |
| No dev/test access to production | Database Policy #12 | Break-glass emergency scenarios (time-boxed, fully audited) |

**Exception Process:**
- Pre-approved emergency procedures with documented approval chain
- Full audit logging of all actions
- Post-incident review required

### 4. Protocol and Encryption Rules

These have transitional exceptions for legacy integration.

| Rule | Source | Valid Exception Scenarios |
|------|--------|---------------------------|
| TLS 1.2+ required | Multiple | Legacy system integration (time-boxed remediation plan required), hardware that cannot be upgraded |
| Certificate validity | CDN Policy #6 | Internal development environments (not production) |

**Exception Requirements:**
- Documented remediation timeline (maximum 12 months)
- Compensating controls during transition
- Risk acceptance sign-off

---

## Rules That ARE Universal Laws

The following rules from source documents have been classified as universal laws because they have NO valid exceptions.

### Security Laws (Always Apply)

| Rule | Source | Why Universal |
|------|--------|---------------|
| Security training required | Security #10 | Basic competency, no exception justifies untrained developers |
| Third-party security assessment | Security #4 | Vendor risk always exists, cannot be waived |
| Network segmentation | Network #4 | Defense in depth is fundamental |
| Production database isolation | Database #1, #12 | Data protection cannot be compromised |

### Operational Laws (Always Apply)

| Rule | Source | Why Universal |
|------|--------|---------------|
| Component registration | Tech Standards #11 | Discoverability required for operations |
| Semantic versioning | Tech Standards #14 | Communication clarity, no downside |
| GitOps for production | Tech Standards K8s #6 | Auditability, no manual changes ever acceptable |

---

## ARB Exception Request Process

For rules documented in this file, teams may request exceptions through:

### 1. Submission Requirements

- [ ] Technical justification document
- [ ] Risk assessment
- [ ] Security review
- [ ] Mitigation/compensating controls plan
- [ ] Timeline (if transitional)

### 2. Review Process

1. Submit to Architecture Review Board (ARB)
2. Security team review (mandatory for security-related)
3. ARB discussion and decision
4. Document approval with conditions
5. Annual renewal for ongoing exceptions

### 3. Exception Tracking

All approved exceptions tracked in:
- ARB decision register
- Component catalog metadata
- Security compliance dashboard

---

## Summary Statistics

| Category | Count | Disposition |
|----------|-------|-------------|
| Universal Laws (new) | 7 | Add to constitution |
| Law Enrichments | 5 | Enhance existing laws |
| Exception-Prone Rules | 15 | This document |
| Avatar Examples | 12+ | Technology-specific guidance |
| New Avatars | 6 | Create avatar packages |

---

## References

- Source: Security and Compliance Adoption (2026-01-29)
- Source: Technology Standards Adoption (2026-01-29)
- Related: [OpenSpec Proposal](../openspec/changes/standards-integration/SPEC.md)
- Related: AA Architecture Review Board Process

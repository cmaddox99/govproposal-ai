# OpenSpec: Technology Standards & Security Integration

## Metadata

| Field | Value |
|-------|-------|
| **Proposal ID** | aa-engineering-laws-standards-integration |
| **Status** | draft |
| **Author** | AA Engineering Team |
| **Created** | 2026-02-04 |
| **Target Repository** | aa-engineering-laws |
| **Source Documents** | Security and Compliance Adoption, Technology Standards Adoption |

---

## Problem Statement

Two organizational documents contain valuable standards and requirements:

1. **Security and Compliance Adoption** - Security policies for software, network, database, and CDN/WAF
2. **Technology Standards Adoption** - Approved technology stack and engineering standards

These documents contain:
- **Universal laws** that should be added to the engineering constitution
- **Enrichments** for existing laws (additional requirements/details)
- **Technology-specific examples** for existing avatars
- **New avatar candidates** (PostgreSQL, MongoDB, Kubernetes, GitHub Actions, OpenTelemetry)
- **Exception-prone rules** that should be documented separately (not as laws)

### Goal

Analyze, classify, and integrate content from these documents to:
1. Strengthen the engineering constitution with universal security and standards laws
2. Enrich existing laws with additional requirements
3. Add technology-specific examples to avatars
4. Create new technology avatars where appropriate
5. Document exception-prone rules separately in `docs/standards-exceptions.md`

---

## Analysis Summary

### Document 1: Security and Compliance Adoption

| Policy | Laws Found | Universal | Has Exceptions | Action |
|--------|------------|-----------|----------------|--------|
| Software Security | 10 | 7 | 3 | Add/Enrich laws, document exceptions |
| Network Security | 9 | 6 | 3 | Add/Enrich laws, document exceptions |
| Database Security | 15 | 10 | 5 | Add/Enrich laws, avatar examples |
| Akamai CDN/WAF | 6 | 2 | 4 | Avatar examples, document exceptions |

### Document 2: Technology Standards Adoption

| Standard | Laws Found | Universal | Has Exceptions | Action |
|----------|------------|-----------|----------------|--------|
| Back-End Languages | 5 | 3 | 2 | Enrich existing laws |
| Front-End Frameworks | 6 | 4 | 2 | Enrich avatars |
| PostgreSQL | 7 | 5 | 2 | **New avatar** |
| MongoDB | 6 | 4 | 2 | **New avatar** |
| Kubernetes | 6 | 4 | 2 | **New avatar** |
| CI/CD (GitHub Actions) | 6 | 5 | 1 | **New avatar** |
| Source Code Management | 7 | 6 | 1 | Enrich ENG-5.4 |
| Integration Protocols | 7 | 5 | 2 | Add laws, **Kafka avatar** |
| OpenTelemetry | 7 | 6 | 1 | Enrich ENG-5.5, **new avatar** |
| Operating System | 6 | 4 | 2 | Document as standard |
| Component Catalog | 6 | 5 | 1 | Add law |
| Technical Documentation | 6 | 5 | 1 | Enrich ENG-3.6 |
| Structured Logging | 7 | 6 | 1 | Enrich ENG-5.5 |
| Semantic Versioning | 6 | 6 | 0 | Add law |

---

## Proposed Changes

### Phase 1: New Laws

#### 1.1 New Security Laws (Article VI)

| ID | Title | Source | Rationale |
|----|-------|--------|-----------|
| ENG-6.9 | Security Training Law | Software Security #10 | **Universal**: All developers must have security awareness |
| ENG-6.10 | Third-Party Security Law | Software Security #4 | **Universal**: Vendor solutions must meet security requirements |
| ENG-6.11 | Network Segmentation Law | Network Security #4 | **Universal**: Systems must be segmented by risk |
| ENG-6.12 | Database Isolation Law | Database Security #1, #12 | **Universal**: Production DBs isolated from dev/test |

**Proposed ENG-6.9: Security Training Law**
```
All developers SHALL complete security training:
- Annual security awareness training required
- Training completion before code contribution privileges
- Role-specific training for security-sensitive roles
```

**Proposed ENG-6.10: Third-Party Security Law**
```
All vendor solutions SHALL meet security requirements:
- Security assessment before acquisition
- Contract requirements for security compliance
- Ongoing vendor security monitoring
```

**Proposed ENG-6.11: Network Segmentation Law**
```
Systems SHALL be segmented by risk and sensitivity:
- Controlled traffic flow between segments
- Firewalls at trust zone boundaries
- Development/Test/Production isolation
```

**Proposed ENG-6.12: Database Isolation Law**
```
Production databases SHALL be isolated:
- No development/testing access to production data
- No direct queries on production without approval
- Database links between prod/dev prohibited
```

#### 1.2 New Platform Laws (Article VIII)

| ID | Title | Source | Rationale |
|----|-------|--------|-----------|
| ENG-8.6 | Component Catalog Law | Tech Standards #11 | **Universal**: All services must be discoverable |
| ENG-8.7 | Semantic Versioning Law | Tech Standards #14 | **Universal**: Predictable version communication |
| ENG-8.8 | GitOps Deployment Law | Tech Standards K8s #6 | **Universal**: No manual production deployments |

**Proposed ENG-8.6: Component Catalog Law**
```
All applications and services SHALL be registered in Component Catalog:
- Metadata: squad, product, portfolio mappings
- Dependencies and integrations documented
- Ownership clearly defined
```

**Proposed ENG-8.7: Semantic Versioning Law**
```
All software releases SHALL follow Semantic Versioning (SemVer):
- Format: MAJOR.MINOR.PATCH
- MAJOR: Incompatible API changes
- MINOR: Backward-compatible functionality
- PATCH: Backward-compatible bug fixes
```

**Proposed ENG-8.8: GitOps Deployment Law**
```
All production deployments SHALL use GitOps principles:
- Declarative configuration in version control
- No manual kubectl apply in production
- Automated reconciliation of desired state
```

### Phase 2: Enrich Existing Laws

#### 2.1 ENG-5.2 (CI/CD Pipeline Law) - Enrich

**Current:** Pipeline structure and quality gates
**Add from Tech Standards:**
```
Additional Requirements:
- Reusable workflows required for consistency
- Separation of build and deploy stages
- Pipeline runs must be logged and auditable
- Security scans must pass before deployment (fail-build on critical)
```

#### 2.2 ENG-5.4 (Git Workflow Law) - Enrich

**Current:** Branching strategy and commits
**Add from Tech Standards:**
```
Additional Requirements:
- All commits signed and auditable
- Secrets scanning enabled on all repositories
- Third-party dependencies scanned continuously
- Policy-as-code, docs-as-code approaches enforced
```

#### 2.3 ENG-5.5 (Observability Law) - Enrich

**Current:** Logs, metrics, traces
**Add from Tech Standards (OpenTelemetry, Structured Logging):**
```
Additional Requirements:
- OpenTelemetry SDK integration required for all new services
- Correlation IDs required in all log messages
- Structured logs (JSON format) required
- Required fields: timestamp, log level, correlation ID, service name
- No sensitive data (PII, credentials) in logs
- Real-user monitoring (RUM) for customer-facing applications
```

#### 2.4 ENG-6.4 (Data Protection Law) - Enrich

**Current:** Encryption at rest/in transit, data classification
**Add from Tech Standards (Database section):**
```
Additional Requirements:
- All database connections must use TLS with appropriate ciphers
- Credentials never stored/transported in clear text
- Secrets stored in enterprise vault infrastructure only
- Data masking applied where appropriate
```

#### 2.5 ENG-3.6 (Documentation Law) - Enrich

**Current:** API docs, comments, ADRs
**Add from Tech Standards (TechDocs):**
```
Additional Requirements:
- All documentation in Markdown format
- Docs versioned in repository alongside code
- Docs-as-code approach (reviewed with code changes)
- Content organized by audience (guides, API refs, architecture)
```

### Phase 3: New Technology Avatars

#### 3.1 PostgreSQL Avatar

**Source:** Technology Standards - Database SQL section

```yaml
avatar:
  id: postgresql
  type: technology
  name: PostgreSQL
  category: database

stack:
  type: SQL Database
  version: PostgreSQL 15+
  
specializes_laws:
  - id: ENG-6.4   # Data Protection
  - id: ENG-6.12  # Database Isolation
  - id: ENG-7.8   # Disaster Recovery
```

**Guidance Topics:**
- TLS connection configuration
- Asynchronous replication setup
- Zone-redundant HA patterns
- Automated backup/restore procedures
- Data at rest encryption
- Data masking implementation

#### 3.2 MongoDB Avatar

**Source:** Technology Standards - Database NoSQL section

```yaml
avatar:
  id: mongodb
  type: technology
  name: MongoDB
  category: database

stack:
  type: NoSQL Database
  version: MongoDB 7+
  
specializes_laws:
  - id: ENG-6.4   # Data Protection
  - id: ENG-6.12  # Database Isolation
  - id: ENG-7.8   # Disaster Recovery
```

**Guidance Topics:**
- TLS connection configuration
- Replica set configuration
- Sharding patterns
- Automated backup strategies
- Encryption at rest

#### 3.3 Kubernetes Avatar

**Source:** Technology Standards - Container Runtime section

```yaml
avatar:
  id: kubernetes
  type: technology
  name: Kubernetes
  category: platform

stack:
  type: Container Orchestration
  version: Kubernetes 1.28+
  
specializes_laws:
  - id: ENG-5.1   # Infrastructure as Code
  - id: ENG-5.3   # Environment Parity
  - id: ENG-6.11  # Network Segmentation
  - id: ENG-8.8   # GitOps Deployment
```

**Guidance Topics:**
- Namespace isolation patterns
- Admission controller configuration
- Security policy enforcement
- GitOps with ArgoCD/Flux
- Resource limits and requests

#### 3.4 GitHub Actions Avatar

**Source:** Technology Standards - CI/CD section

```yaml
avatar:
  id: github-actions
  type: technology
  name: GitHub Actions
  category: devops

stack:
  type: CI/CD Platform
  version: GitHub Actions
  
specializes_laws:
  - id: ENG-5.2   # CI/CD Pipeline
  - id: ENG-5.4   # Git Workflow
  - id: ENG-6.6   # Vulnerability Management
```

**Guidance Topics:**
- Reusable workflow patterns
- Security scanning integration
- Self-hosted runner configuration
- Build/deploy separation
- Audit logging

#### 3.5 OpenTelemetry Avatar

**Source:** Technology Standards - Observability section

```yaml
avatar:
  id: opentelemetry
  type: technology
  name: OpenTelemetry
  category: observability

stack:
  type: Observability Framework
  version: OTel SDK
  
specializes_laws:
  - id: ENG-5.5   # Observability
  - id: ENG-8.5   # Telemetry Platform
```

**Guidance Topics:**
- SDK integration patterns
- Correlation ID propagation
- Distributed tracing setup
- Metrics collection
- Log format standards

#### 3.6 Kafka Avatar

**Source:** Technology Standards - Integration Protocols section

```yaml
avatar:
  id: kafka
  type: technology
  name: Apache Kafka
  category: messaging

stack:
  type: Event Streaming
  version: Apache Kafka 3.x
  
specializes_laws:
  - id: ENG-6.4   # Data Protection
  - id: ENG-7.1   # Failure Handling
  - id: ENG-7.6   # Idempotency
  - id: ENG-8.3   # Integration Platform
```

**Guidance Topics:**
- TLS configuration
- Consumer group patterns
- Idempotent producers
- Dead letter queues
- Schema registry usage

### Phase 4: Avatar Examples (Existing Avatars)

#### 4.1 Java-Spring Examples

| Law | Example | Source |
|-----|---------|--------|
| ENG-6.4 | Database TLS Configuration | Tech Standards |
| ENG-6.9 | Security Headers Config | Security Policy |
| ENG-5.5 | OpenTelemetry Integration | Tech Standards |

#### 4.2 React-Frontend Examples

| Law | Example | Source |
|-----|---------|--------|
| ENG-6.5 | Form Validation with TypeScript | Tech Standards |
| ENG-3.1 | Atomic Design Components | Tech Standards |

#### 4.3 Angular-Frontend Examples

| Law | Example | Source |
|-----|---------|--------|
| ENG-6.5 | Reactive Form Validation | Tech Standards |
| ENG-3.1 | Component Architecture | Tech Standards |

### Phase 5: Exception-Prone Rules Document

Create `docs/standards-exceptions.md` for rules that may have valid exceptions:

#### Network/Infrastructure Rules (Not Universal Laws)

| Rule | Source | Exception Scenarios |
|------|--------|---------------------|
| Akamai port restriction (80/443 only) | CDN Policy #4 | Internal services, legacy integrations |
| Ubuntu OS requirement | OS Standard | Windows-only vendor software, specialized appliances |
| PostgreSQL as only SQL DB | DB Standard | Legacy Oracle/SQL Server, vendor requirements |
| MongoDB as only NoSQL DB | DB Standard | Redis for caching, DynamoDB for serverless |
| React/Angular only | Frontend Standard | Internal tools, embedded systems |

#### Process Rules (Context-Dependent)

| Rule | Source | Exception Scenarios |
|------|--------|---------------------|
| TLS 1.2+ only | Multiple | Legacy system integration (time-boxed) |
| Ad-hoc queries prohibited | DB Policy #13 | Emergency incident response |
| Annual training before contribution | Security #10 | Onboarding grace period |

#### Technology-Specific (Vendor Lock-in Risk)

| Rule | Source | Exception Scenarios |
|------|--------|---------------------|
| GitHub Enterprise Cloud only | SCM Standard | Air-gapped environments |
| GitHub Actions only | CI/CD Standard | Multi-cloud deployments, Jenkins legacy |
| DevPlatform/Backstage only | Catalog Standard | Acquisition integration |

---

## Tasks

### Phase 1: New Laws
- [ ] **1.1**: Add ENG-6.9 Security Training Law to security.md
- [ ] **1.2**: Add ENG-6.10 Third-Party Security Law to security.md
- [ ] **1.3**: Add ENG-6.11 Network Segmentation Law to security.md
- [ ] **1.4**: Add ENG-6.12 Database Isolation Law to security.md
- [ ] **1.5**: Add ENG-8.6 Component Catalog Law to platform.md
- [ ] **1.6**: Add ENG-8.7 Semantic Versioning Law to platform.md
- [ ] **1.7**: Add ENG-8.8 GitOps Deployment Law to platform.md
- [ ] **1.8**: Update laws/index.yaml with new law IDs

### Phase 2: Enrich Existing Laws
- [ ] **2.1**: Enrich ENG-5.2 CI/CD Pipeline Law
- [ ] **2.2**: Enrich ENG-5.4 Git Workflow Law
- [ ] **2.3**: Enrich ENG-5.5 Observability Law
- [ ] **2.4**: Enrich ENG-6.4 Data Protection Law
- [ ] **2.5**: Enrich ENG-3.6 Documentation Law

### Phase 3: New Avatars
- [ ] **3.1**: Create avatars/postgresql/ (manifest.yaml, guidance.md)
- [ ] **3.2**: Create avatars/mongodb/ (manifest.yaml, guidance.md)
- [ ] **3.3**: Create avatars/kubernetes/ (manifest.yaml, guidance.md)
- [ ] **3.4**: Create avatars/github-actions/ (manifest.yaml, guidance.md)
- [ ] **3.5**: Create avatars/opentelemetry/ (manifest.yaml, guidance.md)
- [ ] **3.6**: Create avatars/kafka/ (manifest.yaml, guidance.md)
- [ ] **3.7**: Update avatars/index.yaml with new avatars

### Phase 4: Avatar Examples
- [ ] **4.1**: Add java-spring examples (ENG-6.4 TLS, ENG-5.5 OTel)
- [ ] **4.2**: Add react-frontend examples (TypeScript validation)
- [ ] **4.3**: Add angular-frontend examples (Reactive forms)
- [ ] **4.4**: Add postgresql examples (HA, encryption)
- [ ] **4.5**: Add kubernetes examples (GitOps, security policies)

### Phase 5: Exception Documentation
- [ ] **5.1**: Create docs/standards-exceptions.md
- [ ] **5.2**: Document network/infrastructure exceptions
- [ ] **5.3**: Document process exceptions
- [ ] **5.4**: Document technology-specific exceptions

### Phase 6: Validation
- [ ] **6.1**: Run constitution-lint on repository
- [ ] **6.2**: Verify all law cross-references
- [ ] **6.3**: Review new laws for universality (no exceptions)
- [ ] **6.4**: Final documentation review

### Phase 7: Repository Alignment
- [ ] **7.1**: Update README.md with new laws and avatars
- [ ] **7.2**: Update AGENTS.md with new loading instructions
- [ ] **7.3**: Update docs/token-optimization-analysis.md with new structure
- [ ] **7.4**: Update practice-guides/README.md index
- [ ] **7.5**: Create/update practice guides for new laws (security training, GitOps, etc.)
- [ ] **7.6**: Update avatar manifests with new law references
- [ ] **7.7**: Verify all cross-references and internal links
- [ ] **7.8**: Run full token optimization validation
- [ ] **7.9**: Archive OpenSpec proposal to openspec/archive/

---

## Acceptance Criteria

1. **New Laws**: 7 new laws added (ENG-6.9 through ENG-6.12, ENG-8.6 through ENG-8.8)
2. **Enriched Laws**: 5 existing laws enhanced with additional requirements
3. **New Avatars**: 6 new technology avatars created (PostgreSQL, MongoDB, Kubernetes, GitHub Actions, OpenTelemetry, Kafka)
4. **Examples**: At least 2 new examples per existing avatar
5. **Exception Document**: docs/standards-exceptions.md with all non-universal rules
6. **Index Updates**: All registries (laws, avatars) updated
7. **Validation**: constitution-lint passes on repository
8. **Repository Alignment**: All supporting docs updated (README, AGENTS.md, practice guides, token optimization analysis)
9. **Token Optimization**: New content follows decomposed structure for efficient AI agent loading
10. **Proposal Archived**: OpenSpec moved to archive/ upon completion

---

## Classification Criteria

### What Makes a Universal Law?

A rule qualifies as a **universal law** if:
- ✅ Applies to ALL projects without exception
- ✅ Violation would always be a defect
- ✅ No valid business reason to deviate
- ✅ Security/quality cannot be compromised

### What Requires Exception Documentation?

A rule requires **exception documentation** if:
- ⚠️ Technology-specific (vendor lock-in)
- ⚠️ May have valid business exceptions
- ⚠️ Legacy integration scenarios exist
- ⚠️ Depends on project context

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Over-constraining with laws | Medium | High | Exception document + ARB review process |
| Missing critical security rules | Low | High | Security team review |
| Avatar maintenance burden | Medium | Medium | Clear ownership, automated testing |
| Law ID conflicts | Low | Medium | Verify index before assignment |

---

## Estimated Effort

| Phase | Tasks | Estimated Time |
|-------|-------|----------------|
| Phase 1: New Laws | 8 | 2-3 hours |
| Phase 2: Enrich Laws | 5 | 1-2 hours |
| Phase 3: New Avatars | 7 | 3-4 hours |
| Phase 4: Avatar Examples | 5 | 2-3 hours |
| Phase 5: Exception Docs | 4 | 1-2 hours |
| Phase 6: Validation | 4 | 1 hour |
| Phase 7: Repository Alignment | 9 | 2-3 hours |
| **Total** | **42** | **12-18 hours** |

---

## Notes

- Source documents should be archived after integration
- Laws must be universal - if exceptions exist, document separately
- New avatars focus on AA-approved technology stack
- Exception document serves as ARB reference for deviation requests
- Security laws take precedence per priority hierarchy

# GovProposalAI Constitution

**Established:** January 2026
**Authority:** Project Technical Governance
**Jurisdiction:** All code, specifications, and development within the GovProposalAI system
**Co-Founders:** Adeel Ali & Charles

---

## Preamble

We, the developers and maintainers of GovProposalAI, in order to provide a robust, scalable, and compliant government proposal management platform for small-to-medium businesses (SMBs), establish this Constitution to govern the development, testing, and deployment of our system.

**Mission:** To build an AI-powered, multi-tenant SaaS platform that enables SMBs in government contracting to discover aligned solicitations, manage proposal workflows, and maintain compliance with federal, state, and local procurement regulations.

**Client:** SMBs performing government contracting (federal, state, local)
**Core Capability:** Agentic monitoring of government portals + human-in-the-loop proposal management

---

## Article I: Foundational Principles

### Section 1.1: Primary Objectives
The system SHALL pursue these objectives in order of priority:
1. **Compliance:** Meet all applicable government contracting regulations (FAR, DFARS, CMMC, FedRAMP)
2. **Data Privacy:** Protect sensitive proposal data and controlled unclassified information (CUI)
3. **Accuracy:** Ensure solicitation matching and proposal content integrity
4. **Scalability:** Support multi-tenant SaaS with organization isolation
5. **User Experience:** Empower proposal managers with AI-assisted workflows

### Section 1.2: Bounded Context
The system SHALL:
1. Focus on government solicitation discovery, proposal management, and compliance tracking
2. Maintain strict separation of concerns across microservices
3. NEVER expose internal service details through the API gateway
4. Follow Domain-Driven Design with clearly defined bounded contexts

### Section 1.3: Multi-Tenancy Law
The system SHALL enforce strict organization isolation:
1. No cross-organization data leakage permitted
2. Each organization maintains independent:
   - NAICS code configurations
   - Solicitation preferences
   - Proposal pipelines
   - Team member access
   - Compliance documentation
3. Tenant filtering MUST be applied at the database partition level
4. API requests MUST include organization context

**Test Organizations (UAT Environment):**

| Organization | ID | Slug | Purpose |
|--------------|-----|------|---------|
| Acme Contractors Inc. | `11111111-1111-1111-1111-111111111111` | `acme-contractors` | Primary test org |
| Beta Defense Solutions | `22222222-2222-2222-2222-222222222222` | `beta-defense` | Secondary test org |

**Seed Data Requirement:**
Each microservice implementation SHALL include seed data for BOTH test organizations:
- Realistic data that reflects actual government contracting operations
- Sufficient volume for meaningful testing (10-50 records per entity type)
- Data that exercises edge cases and business rules

### Section 1.4: API-First Development Law
**ALL development SHALL follow API-First principles:**

1. **Contract First:** OpenAPI specifications defined BEFORE implementation
2. **Microservices API:** Backend services expose gRPC internally, REST externally
3. **Versioning:** APIs SHALL use semantic versioning (v1, v2, etc.)
4. **Documentation:** Every endpoint MUST have complete OpenAPI documentation

### Section 1.5: Frontend Prototype as Source of Truth Law
**The product-owner-approved frontend prototype defines the data model requirements:**

1. **Frontend Defines Requirements:** The frontend prototype shows what data the system needs
2. **Never Simplify Frontend to Match Backend:** EXTEND the backend to support all frontend fields
3. **Properly Designed Backend:** Models should be properly designed while supporting all frontend requirements
4. **Product Owner Approval:** Changes to frontend data requirements require product owner sign-off

### Section 1.6: AI-Engineer Pairing and Teaching Law

**Claude SHALL act as a teaching partner, not just a code generator:**

**The Learning Feedback Loop:**
1. **Claude follows the constitution strictly** - no shortcuts, no "just this once" exceptions
2. **Claude explains the WHY** - every decision references the constitutional principle behind it
3. **Engineers observe and learn** - watching Claude apply principles builds mental models
4. **Engineers develop judgment** - like citizens with laws, engineers internalize principles

---

## Article II: Architecture Laws

### Section 2.1: Microservices Architecture
The backend SHALL be decomposed into the following bounded contexts:

**Core Domain Services:**
1. **Solicitation Discovery Service** - Portal monitoring, NAICS matching, opportunity alerts
2. **Proposal Management Service** - Proposals, sections, versions, deadlines, pipeline status
3. **Compliance Service** - FAR/DFARS tracking, certifications, representations
4. **Document Service** - Templates, attachments, PDF generation, exports
5. **Analytics Service** - Win/loss tracking, pipeline metrics, performance dashboards

**Supporting Services:**
6. **Identity Service** - Authentication, authorization, user management, RBAC
7. **Organization Service** - Tenant management, NAICS profiles, team configuration
8. **Notification Service** - Email alerts, deadline reminders, opportunity notifications
9. **Audit Service** - Audit trail, compliance logging, activity tracking
10. **AI Agent Service** - LLM orchestration, prompt management, agentic workflows

### Section 2.2: Government Portal Integration Law
**The system SHALL integrate with government procurement portals:**

**Federal Portals:**
1. **SAM.gov** - Primary federal opportunities source
2. **beta.SAM.gov** - Contract opportunities API
3. **FPDS** - Federal Procurement Data System
4. **USASpending.gov** - Award data for competitive intelligence

**State & Local:**
5. **State procurement portals** - Configurable per state
6. **Municipal bid boards** - Configurable per locality

**Integration Requirements:**
- **Rate Limiting:** Respect all portal API rate limits
- **Caching:** Cache portal responses to minimize API calls
- **Fallback:** Graceful degradation when portals are unavailable
- **Audit Trail:** Log all portal interactions for compliance

### Section 2.3: BASE Architecture Law
The system SHALL implement BASE (Basically Available, Soft state, Eventual consistency):

1. **Basically Available:** System remains available during partial failures
2. **Soft State:** State may change over time due to eventual consistency
3. **Eventual Consistency:** Updates propagate to all nodes eventually

**Implementation:**
- Use PostgreSQL for transactional data, Elasticsearch for search
- Implement saga pattern for distributed transactions
- Use event sourcing for audit trail and state reconstruction
- Apply CQRS where beneficial (solicitation search vs proposal editing)

### Section 2.4: Event-Driven Architecture Law
**Services SHALL communicate via events:**

1. **Event Bus:** Apache Kafka (or Redis Streams for simpler deployments)
2. **Event Schema:** All events defined in JSON Schema or Avro
3. **Event Sourcing:** Critical domains (Proposals, Compliance) maintain event logs
4. **Idempotency:** All event handlers MUST be idempotent
5. **Dead Letter Queues:** Failed events routed to DLQ for manual review

### Section 2.5: API Gateway Law
**All external traffic SHALL route through API Gateway:**

1. **Authentication:** JWT validation at gateway level
2. **Rate Limiting:** Per-tenant and per-user limits
3. **Request Routing:** Route to appropriate microservice
4. **Response Caching:** Cache GET requests where appropriate
5. **Circuit Breaker:** Protect services from cascade failures

---

## Article III: Government Contracting Compliance Laws

### Section 3.1: Federal Acquisition Regulation (FAR) Compliance
**The system SHALL support FAR compliance:**

1. **FAR Part 4** - Administrative matters, contractor registration (SAM.gov integration)
2. **FAR Part 9** - Contractor qualifications, responsibility determinations
3. **FAR Part 12** - Commercial items acquisitions
4. **FAR Part 15** - Contracting by negotiation (competitive proposals)
5. **FAR Part 19** - Small business programs (set-asides tracking)
6. **FAR Part 52** - Solicitation provisions and contract clauses tracking

**Implementation:**
- Track applicable FAR clauses per solicitation
- Generate compliance checklists based on FAR requirements
- Alert users to missing certifications or representations

### Section 3.2: DFARS Compliance (Defense Contracts)
**For defense-related proposals, the system SHALL support:**

1. **DFARS 252.204-7012** - Safeguarding Covered Defense Information (CDI)
2. **DFARS 252.204-7019/7020/7021** - NIST SP 800-171 and CMMC requirements
3. **DFARS 252.225** - Foreign acquisition requirements (Buy American, ITAR)
4. **Cost Accounting Standards (CAS)** - For cost-reimbursement contracts

### Section 3.3: DCAA Compliance
**For contracts subject to DCAA audit, the system SHALL:**

1. **Cost Accounting:** Support DCAA-compliant cost tracking methodologies
2. **Timekeeping:** Integrate with timekeeping systems for labor costing
3. **Indirect Rates:** Support provisional and final indirect rate structures
4. **Audit Trail:** Maintain comprehensive records for DCAA audits

### Section 3.4: Cybersecurity Maturity Model Certification (CMMC)
**The system SHALL support CMMC 2.0 compliance:**

**Level 1 (Foundational):** 17 practices from FAR 52.204-21
- Basic safeguarding of Federal Contract Information (FCI)

**Level 2 (Advanced):** 110 practices from NIST SP 800-171
- Protection of Controlled Unclassified Information (CUI)
- Required for most DoD contracts

**Level 3 (Expert):** NIST SP 800-172 practices
- Protection against Advanced Persistent Threats (APT)
- Required for highest-priority programs

**Implementation:**
- Track customer's CMMC certification level
- Filter opportunities based on CMMC requirements
- Alert users to opportunities exceeding their certification level
- Provide CMMC compliance self-assessment checklists

### Section 3.5: Data Privacy Laws
**The system SHALL comply with applicable data privacy regulations:**

1. **FISMA** - Federal Information Security Management Act
2. **NIST 800-171** - Protecting CUI in non-federal systems
3. **State Privacy Laws** - CCPA, VCDPA, CPA, etc. based on customer location
4. **FedRAMP** - Required for cloud services used by federal agencies

**Data Classification:**
| Classification | Description | Handling |
|---------------|-------------|----------|
| Public | Non-sensitive business info | Standard protection |
| Internal | Business-sensitive | Encrypted at rest |
| Confidential | Proprietary/bid pricing | Encrypted + access controls |
| CUI | Controlled Unclassified Info | NIST 800-171 controls |
| Restricted | Classified references | Prohibited in system |

### Section 3.6: Small Business Compliance
**The system SHALL support small business program tracking:**

1. **Small Business (SB)** - Revenue/employee thresholds by NAICS
2. **Small Disadvantaged Business (SDB)** - 8(a) program eligibility
3. **Women-Owned Small Business (WOSB/EDWOSB)** - Certification tracking
4. **Service-Disabled Veteran-Owned (SDVOSB)** - VA verification
5. **HUBZone** - Geographic eligibility tracking
6. **Mentor-Protege** - Relationships and joint ventures

**Implementation:**
- Track customer's certifications and set-aside eligibility
- Filter opportunities by set-aside type
- Alert users to expiring certifications
- Calculate size standard compliance by NAICS

---

## Article IV: Technology Stack Laws

### Section 4.1: Backend Technology Laws
The backend SHALL use:

**Microservices Runtime:**
1. **Python 3.12+** for business logic services
2. **FastAPI** for REST API endpoints
3. **gRPC** for inter-service communication
4. **Pydantic** for data validation
5. **SQLAlchemy** (async) for ORM

**Data Layer:**
1. **PostgreSQL 16** - Primary transactional database
2. **Elasticsearch 8.x** - Solicitation search and analytics
3. **Redis 7.x** - Caching, sessions, rate limiting
4. **Apache Kafka** - Event streaming (or Redis Streams for simpler deployments)

**AI/ML Layer:**
1. **LangChain/LangGraph** - LLM orchestration for agentic workflows
2. **Anthropic Claude** - Primary LLM for proposal assistance
3. **pgvector** - Vector embeddings for semantic search
4. **Celery** - Background task processing for portal monitoring

**Testing:**
1. **pytest, pytest-asyncio, pytest-cov** for unit/integration tests
2. **hypothesis** for property-based testing
3. **locust** for load testing
4. **ruff** (linting), **mypy** (type checking), **bandit** (security)

### Section 4.2: Frontend Technology Laws
The frontend SHALL use:

1. **Next.js 15+** with App Router and TypeScript
2. **React 19+** with Server Components
3. **Radix UI + Tailwind CSS** for components
4. **React Hook Form + Zod** for form validation
5. **Zustand** for client state management
6. **TanStack Query** for server state
7. **Playwright** for E2E testing

### Section 4.3: Infrastructure Laws
**Phased Infrastructure Strategy:**

---

**PHASE 1: Development & UAT**

| Component | Service | Notes |
|-----------|---------|-------|
| **Frontend** | Vercel or Fly.io | Next.js app |
| **Microservices** | Fly.io | Python/FastAPI containers |
| **Database** | Neon or Supabase | Managed PostgreSQL |
| **Search** | Elastic Cloud | Managed Elasticsearch |
| **Cache** | Upstash Redis | Serverless Redis |
| **Events** | Upstash Kafka or Redis Streams | Event streaming |
| **CI/CD** | GitHub Actions | Automated deployment |
| **Auth** | Clerk or Auth0 | Managed identity |

---

**PHASE 2: Production (FedRAMP-Ready)**

| Component | Service | Notes |
|-----------|---------|-------|
| **Compute** | AWS GovCloud or Azure Government | FedRAMP authorized |
| **Container Orchestration** | EKS/AKS | Kubernetes |
| **Database** | RDS PostgreSQL (FedRAMP) | Managed, encrypted |
| **Search** | Amazon OpenSearch | FedRAMP authorized |
| **Secrets** | AWS Secrets Manager / Azure Key Vault | FedRAMP authorized |
| **Identity** | AWS Cognito or Azure AD B2C | Federal-ready |

---

**Migration Trigger: Phase 1 -> Phase 2**
Move to GovCloud when:
- First federal customer requires FedRAMP
- CMMC Level 2+ compliance needed
- CUI handling required

### Section 4.4: AI-Age UI Design Law
**The frontend SHALL embody modern AI-age aesthetics:**

**Core Principles:**
1. **Dark-First Design:** Default dark theme with full light mode support
2. **Gradient Accents:** Emerald-500 to Blue-500 gradient for AI elements
3. **Glass Morphism:** Subtle blur and transparency effects
4. **Smooth Animations:** Micro-interactions with tailwindcss-animate
5. **Responsive Design:** Mobile-first with tablet and desktop breakpoints

**Design System Standards:**

| Element | Dark Mode | Light Mode |
|---------|-----------|------------|
| Background | `#0a0a0f` (near-black) | `#ffffff` (white) |
| Card Background | `white/[0.03]` with blur | `gray-50` with shadow |
| Primary Accent | Emerald-500 to Blue-500 gradient | Same gradient |
| Text Primary | `white` | `gray-900` |
| Text Secondary | `white/60` | `gray-500` |
| Borders | `white/[0.08]` | `gray-200` |
| AI Elements | Pulsing gradient border | Same |

**AI-Specific UI Patterns:**
- **Agent Status Indicators:** Pulsing dots for active agents
- **Streaming Responses:** Character-by-character reveal
- **Confidence Scores:** Visual indicators for AI suggestions
- **Human-in-the-Loop:** Clear approval/reject UI for AI actions

---

## Article V: Code Quality Laws

### Section 5.1: Style and Formatting Laws

**Python Code SHALL:**
1. Follow PEP 8 conventions
2. Use `snake_case` for functions and variables
3. Use `PascalCase` for classes
4. Be formatted via `ruff format` (no exceptions)
5. Include type hints for all functions (strict mypy mode)

**TypeScript Code SHALL:**
1. Use `camelCase` for functions and variables
2. Use `PascalCase` for components and classes
3. Be formatted via `Prettier` (no exceptions)
4. Enable strict mode (no `any` types without explicit justification)

### Section 5.2: Architecture Patterns

**The system SHALL adhere to:**
1. **Domain-Driven Design:** Organize by bounded context
2. **Hexagonal Architecture:** Ports and adapters for each service
3. **Repository Pattern:** Data access layer separated from business logic
4. **CQRS:** Separate read and write models where complexity warrants
5. **Event Sourcing:** For critical domains (proposals, compliance)
6. **Saga Pattern:** For distributed transactions

### Section 5.3: Complexity Limits
- **Cyclomatic Complexity:** <= 10 per function
- **Cognitive Complexity:** <= 7 per function
- **Function Length:** <= 50 lines
- **Class Length:** <= 300 lines
- **Maximum Parameters:** <= 4 (use dataclasses for more)

### Section 5.4: Git Branching Strategy Law
**Feature branches SHALL be used for proposal work:**

**Branch Naming Convention:**
```
proposal/<change-id>
```
Examples:
- `proposal/setup-infrastructure`
- `proposal/implement-solicitation-service`
- `proposal/add-sam-gov-integration`

**Workflow Rules:**
1. **Create branch from main** when starting a proposal
2. **Rebase frequently** (daily minimum) to avoid drift
3. **Pull request per proposal** (or per vertical slice for large proposals)
4. **Require 1 reviewer** before merge to main
5. **Squash merge** to keep main history clean
6. **Delete branch** immediately after merge

### Section 5.5: CI/CD Deployment Law

**ALL deployments to UAT and Production SHALL go through CI/CD pipelines.**

**Enforcement:**
- CI/CD workflows are the ONLY authorized deployment mechanism
- Manual deploys are for local development testing only
- Any production or UAT deployment must have a corresponding PR and CI run

---

## Article VI: Testing Laws

### Section 6.1: Atomic Test-Driven Development Law
**TDD SHALL be practiced in atomic cycles - ONE test at a time:**

1. **Write ONE failing test** that defines expected behavior
2. **Write the MINIMUM production code** to make that ONE test pass
3. **Refactor WHILE GREEN** - improve code quality with passing tests as safety net
4. **Commit frequently** - each green state is a valid commit point
5. **Repeat** - never write multiple tests before making them pass

### Section 6.2: Test Pyramid Law
The test suite SHALL maintain:
1. **70-80% Unit Tests:** Fast (<10ms), test behavior not structure
2. **15-25% Integration Tests:** Test service contracts, mock external services
3. **5-10% E2E Tests:** Complete user workflows, critical paths only

### Section 6.3: Coverage Laws
1. **Overall Coverage:** Minimum 80% line coverage
2. **New Code:** Minimum 90% line coverage
3. **Critical Paths:** 100% line coverage (compliance checks, proposal submission)
4. **Mutation Score:** Minimum 70% for changed code

### Section 6.4: Contract Testing Law
**All service interfaces SHALL have contract tests:**

1. **Consumer-Driven Contracts:** Consumers define expected behavior
2. **Pact/Contract Testing:** Automated contract verification
3. **Schema Validation:** All events validated against schemas
4. **Backward Compatibility:** Breaking changes require version bump

### Section 6.5: Vertical Slice Development Law
**ALL feature development SHALL be delivered as vertical slices:**

1. **Slice Definition:** Includes all layers (API, service, repository, UI, tests)
2. **Horizontal Development PROHIBITED:** No layer-by-layer implementation
3. **Independent Testability:** Each slice independently testable
4. **Complete Before Moving On:** Finish slice before starting next

**Example Slices:**
- "As a user, I can view SAM.gov opportunities matching my NAICS codes" (API + Service + UI + Tests)
- "As a user, I can approve an opportunity and create a proposal" (API + Service + UI + Tests)
- NOT: "Build the database layer" then "Build the API layer" then "Build the UI layer"

---

## Article VII: Business Domain Laws

### Section 7.1: Solicitation Discovery Domain
**Solicitation monitoring SHALL:**
1. Support configurable NAICS code profiles per organization
2. Monitor SAM.gov and configurable state/local portals
3. Deduplicate opportunities across sources
4. Score opportunities based on alignment criteria
5. Provide AI-powered opportunity summaries

### Section 7.2: Proposal Management Domain
**Proposal workflow SHALL:**
1. Support multi-stage pipeline (Discovery -> Qualification -> Capture -> Proposal -> Submitted -> Awarded/Lost)
2. Track proposal sections with version history
3. Enforce deadline management with alerts
4. Support team collaboration with role-based access
5. Generate compliance matrices

### Section 7.3: Compliance Tracking Domain
**Compliance management SHALL:**
1. Track FAR/DFARS clause applicability
2. Maintain certification and representation status
3. Generate compliance checklists per solicitation
4. Alert on expiring certifications
5. Support CMMC self-assessment

### Section 7.4: AI Agent Domain
**AI-assisted workflows SHALL:**
1. Maintain human-in-the-loop for all critical actions
2. Provide confidence scores for AI suggestions
3. Log all AI interactions for audit
4. Support user feedback for improvement
5. Never auto-submit without explicit approval

---

## Article VIII: Security Laws

### Section 8.1: Data Protection Law
1. **Encryption at Rest:** AES-256 for all data stores
2. **Encryption in Transit:** TLS 1.3 for all communications
3. **Key Management:** Rotate keys annually, store in KMS
4. **PII Handling:** Encrypt all personally identifiable information
5. **Backup Encryption:** All backups encrypted with separate keys

### Section 8.2: Access Control Law
1. **RBAC:** Role-based access control for all resources
2. **Least Privilege:** Users receive minimum necessary permissions
3. **MFA Required:** Multi-factor authentication for all accounts
4. **Session Management:** 30-minute idle timeout, 8-hour absolute timeout
5. **API Keys:** Rotate quarterly, scope to specific services

### Section 8.3: Audit Trail Law
**ALL data modifications SHALL be audited:**

1. **Immutable Audit Log:** Write-once, append-only audit records
2. **Required Fields:** timestamp, user_id, organization_id, action, resource_type, resource_id, old_value, new_value, ip_address
3. **Retention:** Minimum 7 years for compliance records
4. **Tamper Evidence:** Cryptographic chaining of audit entries
5. **Searchable:** Indexed for compliance investigations

### Section 8.4: CUI Handling Law (When Applicable)
**If handling Controlled Unclassified Information:**

1. **Marking:** All CUI must be clearly marked
2. **Access:** Only authorized personnel with need-to-know
3. **Transmission:** Encrypted channels only
4. **Storage:** NIST 800-171 compliant storage
5. **Disposal:** Secure deletion procedures

---

## Article IX: Amendment Process

### Section 9.1: Constitution Amendment Law
This Constitution MAY be amended by:
1. Proposal via OpenSpec change process
2. Review and approval by project maintainers (Asad & Charles)
3. Documentation in `openspec/changes/` directory
4. Update to this document with changelog entry

### Section 9.2: Law Precedence
In case of conflict:
1. **Government compliance** takes precedence over features
2. **Data privacy** takes precedence over performance
3. **Security laws** are non-negotiable
4. **Testing laws** cannot be waived

---

## Changelog

**January 12, 2026:** Initial Constitution Established
- Established foundational principles for GovProposalAI
- Defined microservices architecture with 10 bounded contexts
- Mandated compliance with FAR, DFARS, DCAA, CMMC, FedRAMP
- Adopted API-First development approach
- Established Vertical Slice Development Law (no waterfall)
- Adopted Atomic TDD and Test Pyramid from GMS Constitution
- Adopted AI-Age UI Design Law from GMS Constitution
- Defined government portal integration requirements
- Established security and audit trail laws

---

**Signed and Ratified:** January 12, 2026
**Co-Founders:** Adeel Ali & Charles
**Witness:** Claude Opus 4.5 (AI Assistant)

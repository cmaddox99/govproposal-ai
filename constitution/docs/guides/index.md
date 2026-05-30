# American Airlines Hangar's AI Constitution Guides

**📚 Complete Learning Resource for AI-Assisted Development with Constitutional Governance**

These guides support organizational transformation toward **100% AI-Assisted Coding** using the Hangar SDD framework and American Airlines Hangar's Constitutional governance.

---

## 🎯 Purpose

This documentation helps teams:
- **Understand** the Constitution and its laws
- **Implement** Spec-Driven Development (SDD) with Hangar SDD
- **Adopt** AI-assisted coding practices
- **Transform** development workflows for brownfield and greenfield projects

---

## 📖 Guide Categories

### 🏛️ Constitution & Laws (Start Here)
Understanding the foundational governance that enables AI-assisted development.

| Guide | Description | Time | Audience |
|-------|-------------|------|----------|
| [Constitution Overview](./constitution/constitution-overview.md) | Introduction to constitutional governance | 20 min | Everyone |
| [Atomic TDD Law](./constitution/atomic-tdd-law.md) | The 8-step TDD cycle for AI-human pairing | 30 min | Engineers |
| [Vertical Slice Development Law](./constitution/vertical-slice-law.md) | Slicing work for Hangar SDD proposals | 25 min | Engineers, PMs |
| [Code Quality Laws](./constitution/code-quality-laws.md) | Complexity, immutability, Law of Demeter | 25 min | Engineers |
| [Test Pyramid Law](./constitution/test-pyramid-law.md) | Testing strategy and coverage requirements | 20 min | Engineers |
| [AI-Engineer Pairing Law](./constitution/ai-engineer-pairing-law.md) | How AI agents follow the Constitution | 20 min | Everyone |
| [Domain-Driven Design Law](./constitution/ddd-law.md) | Entities, value objects, aggregates | 25 min | Engineers |
| [Continuous Refactoring Law](./constitution/continuous-refactoring-law.md) | Boy Scout Rule and technical debt | 15 min | Engineers |

### 🚀 Adoption Guides
How to adopt the Constitution for different project contexts.

| Guide | Description | Time | Audience |
|-------|-------------|------|----------|
| [Brownfield Adoption](./adoption/brownfield-adoption.md) | Adopting Constitution in existing projects | 30 min | Tech Leads |
| [Greenfield MVP](./adoption/greenfield-mvp.md) | Starting new projects with Constitution | 25 min | Tech Leads, PMs |
| [Organizational Transformation](./adoption/organizational-transformation.md) | Scaling AI-assisted development | 35 min | Leadership |

### 🔧 Testing Guides
Comprehensive testing practices aligned with Constitutional laws.

| Guide | Description | Time | Audience |
|-------|-------------|------|----------|
| [Testing Architecture](./testing/testing-architecture.md) | Where tests go and what to mock | 15 min | Engineers |
| [Characterization Testing](./testing/characterization-testing.md) | Testing legacy code for safe refactoring | 25 min | Engineers |
| [Atomic TDD Workflow](./testing/atomic-tdd-workflow.md) | Step-by-step TDD with examples | 30 min | Engineers |
| [WireMock Contract Testing](./testing/wiremock-contract-testing.md) | Testing external SOAP/REST APIs | 20 min | Engineers |

### 🧩 Avatar Architecture
How technology avatars structure their reference content for optimal RAG retrieval.

| Guide | Description | Time | Audience |
|-------|-------------|------|----------|
| [Avatar Model Schema](./avatar-model-schema.md) | Token budgets, required fields, file structure | 20 min | Avatar maintainers |
| [Split-Reference Architecture](./avatars/split-reference-architecture.md) | Pseudo-RAG pattern for large reference content | 15 min | Avatar maintainers |

### 💬 Prompt Engineering
Effective prompts for AI-assisted development with Constitutional compliance.

| Guide | Description | Time | Audience |
|-------|-------------|------|----------|
| [Prompt Patterns](./prompts/prompt-patterns.md) | Effective prompts for spec-driven development | 20 min | Engineers |
| [Agent Response Patterns](./prompts/agent-response-patterns.md) | How AI responds to Constitutional laws | 15 min | Engineers |

---

## 🎓 Learning Paths

### Path 1: New Team Member (2-3 hours)
1. [Constitution Overview](./constitution/constitution-overview.md)
2. [AI-Engineer Pairing Law](./constitution/ai-engineer-pairing-law.md)
3. [Testing Architecture](./testing/testing-architecture.md)
4. [Atomic TDD Workflow](./testing/atomic-tdd-workflow.md)
5. [Prompt Patterns](./prompts/prompt-patterns.md)

### Path 2: Tech Lead Adopting Constitution (3-4 hours)
1. [Constitution Overview](./constitution/constitution-overview.md)
2. [Brownfield Adoption](./adoption/brownfield-adoption.md) OR [Greenfield MVP](./adoption/greenfield-mvp.md)
3. [Vertical Slice Development Law](./constitution/vertical-slice-law.md)
4. [Code Quality Laws](./constitution/code-quality-laws.md)
5. [Organizational Transformation](./adoption/organizational-transformation.md)

### Path 3: Engineer Working on Legacy Code (2 hours)
1. [Characterization Testing](./testing/characterization-testing.md)
2. [Atomic TDD Law](./constitution/atomic-tdd-law.md)
3. [Continuous Refactoring Law](./constitution/continuous-refactoring-law.md)
4. [Test Pyramid Law](./constitution/test-pyramid-law.md)

### Path 4: Leadership Understanding AI Transformation (1 hour)
1. [Constitution Overview](./constitution/constitution-overview.md)
2. [AI-Engineer Pairing Law](./constitution/ai-engineer-pairing-law.md)
3. [Organizational Transformation](./adoption/organizational-transformation.md)

---

## 📁 Directory Structure

```
hangar-ai-specs/
├── index.md                              ← You are here
├── constitution/                         ← Constitutional law guides
│   ├── constitution-overview.md
│   ├── atomic-tdd-law.md
│   ├── vertical-slice-law.md
│   ├── code-quality-laws.md
│   ├── test-pyramid-law.md
│   ├── ai-engineer-pairing-law.md
│   ├── ddd-law.md
│   └── continuous-refactoring-law.md
├── adoption/                             ← Adoption strategies
│   ├── brownfield-adoption.md
│   ├── greenfield-mvp.md
│   └── organizational-transformation.md
├── testing/                              ← Testing practices
│   ├── testing-architecture.md
│   ├── characterization-testing.md
│   ├── atomic-tdd-workflow.md
│   └── wiremock-contract-testing.md
└── prompts/                              ← Prompt engineering
    ├── prompt-patterns.md
    └── agent-response-patterns.md
```

---

## 🔗 Related Resources

- **[AGENTS.md](../../AGENTS.md)** - Hangar SDD workflow instructions for AI agents
- **[Laws](../../laws/)** - The authoritative source of all laws
- **[Hangar AI Specs](../../hangar-ai-specs/)** - Project-specific proposals and specs

---

## ✅ Constitutional Alignment

These guides support compliance with:
- **Article I** - Foundational Principles (AI-Engineer Pairing Law)
- **Article II** - Architecture Laws (DDD, Layered Architecture)
- **Article III** - Code Quality Laws (Complexity, Immutability, Law of Demeter)
- **Article IV** - Testing Laws (Atomic TDD, Test Pyramid, Coverage)
- **Article V** - Security and Compliance Laws
- **Article VI** - Performance and Reliability Laws

---

---

**Maintained by:** The Hangar, American Airlines IT
**Last Updated:** January 2026
**Version:** 1.0.0

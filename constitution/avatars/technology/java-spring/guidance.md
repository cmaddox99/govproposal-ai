# Java/Spring Boot — AA BFF Fleet Guidance

> **Stack reality (2026):** AA mobile BFF fleet is 19 Java repos. Primary framework is Spring Boot 2.x (migration to 3.x underway). Mobile-Manage-Minilith is Spring MVC + Axis2 (pre-Boot legacy — not Spring Boot). Fleet DI: `@Autowired` field injection is the norm; constructor injection is the goal. ServiceLocator anti-pattern (`ServiceLocator.getXxxManager()`) is pervasive in the Minilith — treat as a HARD_BLOCK pattern in any new code.

## Core Laws

| Law | Requirement |
|-----|-------------|
| **ENG-4.1** Atomic TDD | Every unit of behavior covered by a failing test before implementation. `./mvnw test` must pass. |
| **ENG-3.1** Complexity | No class > 300 LOC. No method > 30 LOC. God classes are the fleet's #1 defect driver. |
| **ENG-2.1** DDD | Domain objects carry behavior. POJOs with zero behavior are an anemic domain model violation. |
| **ENG-2.2** Layers | Controller → Service → Repository. ServiceLocator bypasses all layer boundaries — banned. |
| **ENG-3.3** Demeter | No method chains through unrelated objects. BFF builder classes are the primary offender. |
| **ENG-3.5** Naming | Classes: PascalCase. Methods: camelCase. Getter names must not hide I/O operations. |
| **ENG-11.1** SDD | Create `hangar-ai-specs/PROPOSAL.md` before any new BFF feature implementation. |

## AA BFF Fleet Patterns to Avoid

- **Mutable `@Service` singletons** — thread-safety critical defect in TravelHubResponseBuilderV2/V3/V4
- **`BigDecimal(double)` for currency** — precision loss; use `BigDecimal(String)` or `.valueOf()`
- **Copy-paste versioning** — V2/V3/V4 full-class clones; use abstract base class + strategy
- **Getter-named methods with HTTP calls** — violates principle of least surprise

> Full examples in `guidance-detail.md`. Use cases in `use-cases/`.

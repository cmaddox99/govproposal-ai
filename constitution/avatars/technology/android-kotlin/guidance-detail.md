# Android Kotlin Guidance

> **Purpose:** Stack-specific agent behaviors for Android applications built with Kotlin, Jetpack Compose, and Hilt. Grounded in the Jeroen Mols TDD philosophy, Philipp Hauer Kotlin testing idioms, Fernando Cejas Clean Architecture, and Google's Now in Android living reference.

---

## Authoritative Sources

| Authority | Source | Domain |
|-----------|--------|--------|
| **Jeroen Mols** | [jeroenmols.com](https://jeroenmols.com) · GDE · *"Testing Made Sweet with a Mockito"* | Android TDD philosophy and isolation |
| **Philipp Hauer** | [phauer.com](https://phauer.com) · [KotlinConf 2018](https://www.youtube.com/watch?v=RX_g65J14H0) | Kotlin-idiomatic unit testing patterns |
| **Fernando Cejas** | [fernandocejas.com](https://fernandocejas.com) · [android-kotlin repo](https://github.com/android10/Android-CleanArchitecture-Kotlin) | Clean Architecture layers in Kotlin |
| **Google Now in Android** | [github.com/android/nowinandroid](https://github.com/android/nowinandroid) | Official 2024–2025 Compose + Hilt + modular reference |
| **MockK** | [mockk.io](https://mockk.io) | Kotlin-native mocking |
| **Turbine** | [github.com/cashapp/turbine](https://github.com/cashapp/turbine) | Kotlin Flow stream testing |

---

## The Jeroen Mols TDD Manifesto for Android

> *"Everything can be tested."*  — Jeroen Mols, jeroenmols.com

The common excuse for untested Android code is that the framework makes testing hard. Mols' answer: that's a **design problem**, not a testing problem. Android's tight coupling to the framework is dissolved by **Dependency Injection** — once dependencies are injected rather than constructed internally, every class becomes testable on the JVM without an emulator.

**Key principles:**

1. **Isolate Android from business logic** — domain and use-case code must have zero Android framework imports. `ViewModel` accesses repositories via interfaces; the implementation lives in the data layer.
2. **Push coverage down to fast JVM unit tests** — Espresso and UI tests are slow and fragile. Every behaviour that can be tested via MockK + JUnit 5 should be. UI tests exist only to verify the wiring.
3. **Test doubles over real dependencies** — hand-written `interface` fakes for domain protocols; MockK for Android seams (Context, Resources, system services).
4. **RED-GREEN-REFACTOR, one test at a time** — same cycle as Jon Reid for iOS; same discipline.

---

## Philipp Hauer: Kotlin-Idiomatic Test Structure

> *"Write tests that feel like Kotlin, not Java."*  — Philipp Hauer, KotlinConf 2018

### Backtick Test Names

```kotlin
@Test
fun `adding item to empty order updates total`() { ... }

@Test
fun `adding item when order is placed throws exception`() { ... }
```

Failure messages read as English sentences. Never use `_` separators or camelCase.

### `@TestInstance(Lifecycle.PER_CLASS)` + `val` Mocks

```kotlin
@TestInstance(TestInstance.Lifecycle.PER_CLASS)
class OrderServiceTest {
    // val — not lateinit var — because PER_CLASS creates one instance
    private val repository = mockk<OrderRepository>()
    private val auditLogger = mockk<AuditLogger>(relaxed = true)
    private val sut = OrderService(repository, auditLogger)

    @BeforeEach
    fun setUp() {
        clearMocks(repository)
    }
}
```

Benefits: `val` for mocks; non-static `@BeforeAll`/`@AfterAll`; cleaner setup.

### `@Nested` Inner Classes for Context Grouping

```kotlin
@TestInstance(TestInstance.Lifecycle.PER_CLASS)
class OrderTest {

    inner class `when order is empty` {
        @Test
        fun `total is zero`() { ... }

        @Test
        fun `status is draft`() { ... }
    }

    inner class `when order has items` {
        @BeforeEach
        fun setUp() { order.addItem(product, 1) }

        @Test
        fun `total reflects added items`() { ... }

        @Test
        fun `can place order`() { ... }
    }
}
```

---

## MockK Patterns

MockK is Kotlin-native — it mocks `final` classes, `object`s, and `suspend` functions without configuration.

### Basic Mocking

```kotlin
// Simple stub
val repository = mockk<OrderRepository>()
every { repository.findById(any()) } returns Order.stub()

// Suspend function stub
coEvery { repository.save(any()) } returns Unit

// Relaxed mock — returns defaults for un-stubbed calls (useful for loggers, sinks)
val auditLogger = mockk<AuditLogger>(relaxed = true)
```

### Verification

```kotlin
// Verify a suspend call happened exactly once
coVerify(exactly = 1) { repository.save(match { it.status == OrderStatus.PLACED }) }

// Verify nothing was called on a mock
verify { auditLogger wasNot Called }
```

### Slot Capturing

```kotlin
val slot = slot<AuditEvent>()
coEvery { auditLogger.log(capture(slot)) } just runs

sut.placeOrder(orderId)

val event = slot.captured
assertEquals("order.place", event.operation)
assertEquals(AuditResult.SUCCESS, event.result)
```

### Spy (partial mock)

```kotlin
// Spy wraps a real instance — override only specific methods
val realRepository = InMemoryOrderRepository()
val spy = spyk(realRepository)
every { spy.save(any()) } throws RuntimeException("DB failure")
```

---

## Turbine: Testing Kotlin Flow

Turbine (Cash App) gives structured assertions for Flow streams — no `advanceUntilIdle` busy-waits.

```kotlin
import app.cash.turbine.test

@Test
fun `loading orders emits loading then success`() = runTest {
    val orders = listOf(Order.stub())
    coEvery { repository.getOrders() } returns orders

    viewModel.uiState.test {
        assertEquals(OrderListUiState.Loading, awaitItem())
        assertEquals(OrderListUiState.Success(orders), awaitItem())
        cancelAndConsumeRemainingEvents()
    }
}

@Test
fun `loading orders emits error on failure`() = runTest {
    coEvery { repository.getOrders() } throws IOException("Network error")

    viewModel.uiState.test {
        skipItems(1)  // Loading
        val error = awaitItem()
        assertIs<OrderListUiState.Error>(error)
        cancelAndConsumeRemainingEvents()
    }
}
```

---

## Fernando Cejas: Clean Architecture Layers

> *"The domain layer must have zero Android imports."*  — Fernando Cejas

```
┌─────────────────────────────────────────────────────────┐
│  Presentation (Jetpack Compose + HiltViewModel)          │
│  Depends on Domain interfaces only                       │
├─────────────────────────────────────────────────────────┤
│  Domain (pure Kotlin — zero Android framework imports)   │
│  Entities, use cases, repository interfaces              │
├─────────────────────────────────────────────────────────┤
│  Data (Room, Retrofit, Datastore, Android Keystore)      │
│  Implements repository interfaces from Domain            │
└─────────────────────────────────────────────────────────┘
```

Dependency rule: each layer imports only the layer directly below via interfaces. Data is **never** imported by Domain. Presentation depends on Domain interfaces, not Data implementations.

### Domain Layer — Zero Android Imports

```kotlin
// core/domain/model/Order.kt — no Android imports
data class Order(
    val id: OrderId,
    val customerId: CustomerId,
    val lines: List<OrderLine> = emptyList(),
    val status: OrderStatus = OrderStatus.DRAFT
) {
    val total: Money get() = lines.fold(Money.ZERO) { acc, line -> acc + line.total }

    fun addItem(product: Product, quantity: Int): Order {
        check(status == OrderStatus.DRAFT) { "Cannot modify a placed order" }
        val existing = lines.find { it.productId == product.id }
        return if (existing != null) {
            copy(lines = lines.map {
                if (it.productId == product.id) it.copy(quantity = it.quantity + quantity) else it
            })
        } else {
            copy(lines = lines + OrderLine(product.id, product.price, quantity))
        }
    }
}

// Repository interface lives in domain — implementation lives in data
interface OrderRepository {
    suspend fun getOrder(id: OrderId): Order?
    suspend fun save(order: Order)
    fun observeOrders(): Flow<List<Order>>
}
```

### Use Case Pattern (Interactor)

```kotlin
// core/domain/usecase/PlaceOrderUseCase.kt
class PlaceOrderUseCase @Inject constructor(
    private val orderRepository: OrderRepository,
    private val auditLogger: AuditLogger
) {
    suspend operator fun invoke(orderId: OrderId): Result<Order> = runCatching {
        val order = orderRepository.getOrder(orderId)
            ?: throw OrderNotFoundException(orderId)
        val placed = order.place()
        orderRepository.save(placed)
        auditLogger.log(AuditEvent("order.place", orderId.value, AuditResult.SUCCESS))
        placed
    }.onFailure { error ->
        auditLogger.log(AuditEvent("order.place", orderId.value, AuditResult.FAILURE, error.message))
    }
}
```

---

## MVVM + Hilt ViewModel + StateFlow + Compose

### ViewModel (Google NiA pattern)

```kotlin
// Sealed interface for UI state — exhaustive, immutable
sealed interface OrderDetailUiState {
    data object Loading : OrderDetailUiState
    data class Success(val order: Order) : OrderDetailUiState
    data class Error(val message: String) : OrderDetailUiState
}

@HiltViewModel
class OrderDetailViewModel @Inject constructor(
    private val placeOrder: PlaceOrderUseCase,
    private val observeOrder: ObserveOrderUseCase,
    savedStateHandle: SavedStateHandle
) : ViewModel() {

    private val orderId = OrderId(savedStateHandle.get<String>("orderId")!!)

    private val _uiState = MutableStateFlow<OrderDetailUiState>(OrderDetailUiState.Loading)
    val uiState: StateFlow<OrderDetailUiState> = _uiState.asStateFlow()

    init {
        observeOrder(orderId)
            .map { order -> OrderDetailUiState.Success(order) }
            .catch { emit(OrderDetailUiState.Error(it.message ?: "Unknown error")) }
            .onEach { _uiState.value = it }
            .launchIn(viewModelScope)
    }

    fun placeOrder() {
        viewModelScope.launch {
            placeOrder(orderId)
                .onFailure { _uiState.value = OrderDetailUiState.Error(it.message ?: "Failed") }
        }
    }
}
```

### Compose Screen

```kotlin
@Composable
fun OrderDetailScreen(
    viewModel: OrderDetailViewModel = hiltViewModel(),
    onNavigateBack: () -> Unit = {}
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    when (val state = uiState) {
        is OrderDetailUiState.Loading -> CircularProgressIndicator()
        is OrderDetailUiState.Success -> OrderDetailContent(
            order = state.order,
            onPlaceOrder = viewModel::placeOrder
        )
        is OrderDetailUiState.Error -> ErrorCard(
            message = state.message,
            onRetry = viewModel::placeOrder
        )
    }
}
```

---

## Hilt Dependency Injection

### Module Setup

```kotlin
@Module
@InstallIn(SingletonComponent::class)
object RepositoryModule {
    @Provides
    @Singleton
    fun provideOrderRepository(
        orderDao: OrderDao,
        orderApi: OrderApi
    ): OrderRepository = OrderRepositoryImpl(orderDao, orderApi)
}
```

### Test Injection with `@HiltAndroidTest`

```kotlin
@HiltAndroidTest
@RunWith(AndroidJUnit4::class)
class OrderRepositoryImplTest {

    @get:Rule
    val hiltRule = HiltAndroidRule(this)

    @Inject
    lateinit var repository: OrderRepository

    // Replace production module with test double
    @UninstallModules(RepositoryModule::class)
    @Module
    @InstallIn(SingletonComponent::class)
    object FakeRepositoryModule {
        @Provides
        fun provideRepository(): OrderRepository = FakeOrderRepository()
    }

    @Before
    fun setUp() { hiltRule.inject() }

    @Test
    fun `repository returns saved order`() = runTest { ... }
}
```

---

## Security by Design (ENG-6.1)

See `examples/ENG-6.1-security.md` for full COMPLIANT/VIOLATION examples. Key principles:

- **ProGuard/R8 always enabled in release** — `minifyEnabled = true` in release build type
- **Network Security Config** — `res/xml/network_security_config.xml` restricts cleartext and declares pin sets
- **No API keys in code** — use `BuildConfig` fields injected from CI environment variables via `local.properties` (gitignored)
- **Play Integrity API** — verify app authenticity before sensitive operations
- **No PII in Logcat** — use `if (BuildConfig.DEBUG)` guards and redacting wrapper types

---

## Data Protection (ENG-6.4)

See `examples/ENG-6.4-data-protection.md` for full COMPLIANT/VIOLATION examples. Key principles:

- **Android Keystore** — hardware-backed key storage for auth tokens and Restricted data (AES-256-GCM)
- **EncryptedSharedPreferences** — Jetpack Security wrapper over SharedPreferences for Confidential data
- **Certificate pinning** — OkHttp `CertificatePinner` or Network Security Config pin set
- **No PII in Logcat** — custom `SensitiveString` wrapper type with redacted `toString()`

---

## Audit Trail (ENG-6.7)

See `examples/ENG-6.7-audit-trail.md` for full examples. Key principles:

- `fastlane increment_version_code` → monotonic `versionCode` per CI run
- `fastlane supply` release notes contain commit SHA → Play Store build traceable to commit
- Runtime: `AuditEvent` data class emitted to server-side observability sink (not Logcat)

---

## Android Test Pyramid

```
                    ┌───────────┐
                    │  UI Tests │  ≤10%  Compose Testing / Espresso
                   ┌┴───────────┴┐
                   │ Integration │  ~20%  Robolectric / @HiltAndroidTest
                  ┌┴─────────────┴┐
                  │   Unit Tests  │  ≥70%  JUnit 5 + MockK + Turbine (JVM only)
                  └───────────────┘
```

- **Unit (≥70%):** Pure Kotlin, no Android dependencies, run on JVM — fast, precise, MockK for doubles
- **Integration (~20%):** Robolectric runs Android framework on JVM; Hilt test injection; Room in-memory DB
- **UI (≤10%):** Compose `composeTestRule.onNodeWithText(...)`; Espresso for legacy Views; Gradle Managed Devices for CI

### Gradle Managed Devices (CI)

```kotlin
// app/build.gradle.kts
android {
    testOptions {
        managedDevices {
            localDevices {
                create("pixel6api34") {
                    device = "Pixel 6"
                    apiLevel = 34
                    systemImageSource = "aosp"
                }
            }
        }
    }
}
```

```bash
./gradlew pixel6api34DebugAndroidTest  # CI device test — no physical device needed
```

---

## fastlane Pipeline

```ruby
# fastlane/Fastfile
default_platform(:android)

platform :android do

  lane :test do
    gradle(task: "test")          # JVM unit tests
    gradle(task: "lint")          # Android Lint
  end

  lane :beta do
    # AUDIT: monotonic versionCode = unique build identifier per CI run
    increment_version_code(
      gradle_file_path: "app/build.gradle.kts",
      version_code: ENV["BUILD_NUMBER"].to_i
    )
    gradle(
      task: "bundle",
      build_type: "Release",
      print_command: false  # never log signing args (ENG-6.1)
    )
    # AUDIT: version_name contains commit SHA — Play Store build traceable to commit
    supply(
      track: "internal",
      aab: lane_context[SharedValues::GRADLE_AAB_OUTPUT_PATH],
      version_name: "#{ENV['BUILD_NUMBER']}.0 (#{ENV['GITHUB_SHA'][0,8]})",
      skip_upload_apk: true
    )
  end

  lane :deploy do
    gradle(task: "bundle", build_type: "Release")
    supply(track: "production", rollout: "0.10")
  end

end
```

---

## Commands Reference

```bash
# Run unit tests (JVM — no emulator)
./gradlew test

# Run a single test class
./gradlew :app:testDebugUnitTest --tests '*.OrderViewModelTest'

# Run instrumented tests (requires device/emulator)
./gradlew connectedAndroidTest

# Run with Gradle Managed Devices (CI)
./gradlew pixel6api34DebugAndroidTest

# Build release AAB
./gradlew bundleRelease

# Lint
./gradlew lint

# Full CI pipeline via fastlane
bundle exec fastlane test
bundle exec fastlane beta
```

---

## Governance Laws — Android Implementation Notes

> The following notes capture codebase-specific findings from the 2026-04-30 Mode 3 Validate audit
> of the `androidapps` repository. Moved from `manifest.yaml` to here per schema §2.

### ENG-10.1 — Constitution Metrics Collection

- Static analysis: **ktlint 12.1.0** + **Android Lint custom rules** (`lintchecks/` module)
- SonarQube quality gate surfaced in CI
- **Detekt is NOT configured** in the live codebase — do not reference it in agent guidance
- Target: zero ENG-3.1 violations (cyclomatic complexity >10) per release
- Run: `./gradlew lint` + `./gradlew sonarqube -Papp.isJenkins=true`

### ENG-11.1 — Spec-Driven Development (Hangar SDD)

- `hangar-ai-specs/` directory was created 2026-05-05 (Mode 2 correction cycle)
- Before creation: 80 files >500 LOC; composite score flat at 4.7/10 despite 3,191 commits in 90 days
- Spec-first discipline directly addresses god-class growth pattern
- See `examples/ENG-11.1-spec-driven-development.md` for scaffold and usage

### ENG-12.1 — Quality Gate Law

- `sonarqube.gradle` exists in `androidapps` — constitutional gate must be provisioned before any workflow phase advance
- Human reviews SonarQube dashboard before each phase advance
- Run: `./gradlew sonarqube -Papp.isJenkins=true`

### ENG-13.1 — Artifact Governance

- All governance artifacts must be rendered via `aa-artifact-render` before review
- Applies to: `PROPOSAL.md` (once `hangar-ai-specs/` created), ADRs for god-class decompositions, phase gate evidence artifacts

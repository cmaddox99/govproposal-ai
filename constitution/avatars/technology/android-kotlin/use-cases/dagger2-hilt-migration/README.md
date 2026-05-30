# Use Case: Dagger 2 → Hilt Migration

**Avatar:** android-kotlin  
**Laws:** ENG-2.2 (Layered Architecture), ENG-4.1 (Atomic TDD)  
**AA Context:** androidapps uses Dagger 2 (56 @Module, 316 @Provides, 486 @Inject). Zero Hilt annotations. Migration is the target architectural direction.

---

## Problem

Dagger 2 requires hand-written `@Component` and `@Subcomponent` interfaces, verbose `@Module` boilerplate, and manual injection entry points for Activities and Fragments. This creates friction and discourages proper DI adoption. The AA `DataModule.kt` (1,737 LOC, 316 `@Provides`) is a direct consequence — all DI wired in one monolithic module because splitting Dagger components is expensive.

Hilt removes this friction: it generates the component hierarchy automatically, scopes injection to Android lifecycle owners, and enables `@HiltViewModel` constructor injection without factory boilerplate.

---

## Migration Pattern (incremental — module by module)

### Step 1 — Add Hilt to the feature module

```kotlin
// app/build.gradle.kts — add Hilt plugin
plugins {
    id("com.google.dagger.hilt.android")
    kotlin("kapt")
}
dependencies {
    implementation("com.google.dagger:hilt-android:2.51")
    kapt("com.google.dagger:hilt-compiler:2.51")
}
```

### Step 2 — Annotate Application (once, whole-app)

```kotlin
// ✅ Hilt entry point — replaces DaggerAppComponent.create()
@HiltAndroidApp
class AAmobileApplication : Application()
```

### Step 3 — Replace Dagger2 @Module with Hilt @Module

```kotlin
// BEFORE (Dagger 2) — requires @Component to wire
@Module
class BookingModule {
    @Provides @Singleton
    fun provideBookingRepository(api: BookingApi, dao: BookingDao): BookingRepository =
        BookingRepositoryImpl(api, dao)
}

// AFTER (Hilt) — installed automatically into SingletonComponent
@Module
@InstallIn(SingletonComponent::class)
object BookingModule {
    @Provides @Singleton
    fun provideBookingRepository(api: BookingApi, dao: BookingDao): BookingRepository =
        BookingRepositoryImpl(api, dao)
}
```

### Step 4 — Replace manual ViewModel factory with @HiltViewModel

```kotlin
// BEFORE (Dagger 2) — manual factory boilerplate
class BookingViewModelFactory @Inject constructor(
    private val searchUseCase: SearchFlightsUseCase
) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T =
        BookingViewModel(searchUseCase) as T
}

// AFTER (Hilt) — zero factory code
@HiltViewModel
class BookingViewModel @Inject constructor(
    private val searchUseCase: SearchFlightsUseCase
) : ViewModel()
```

### Step 5 — Update test injection

```kotlin
// Hilt test — replaces DaggerTestComponent
@HiltAndroidTest
@RunWith(AndroidJUnit4::class)
class BookingRepositoryTest {
    @get:Rule val hiltRule = HiltAndroidRule(this)
    @Inject lateinit var repository: BookingRepository

    @Before fun setUp() = hiltRule.inject()

    @Test
    fun `repository returns booked flight`() = runTest {
        // no manual DI wiring needed
    }
}
```

---

## AA Migration Strategy

Given DataModule.kt at 1,737 LOC, do **not** migrate the whole app at once. Strategy:

1. Add `@HiltAndroidApp` to Application — this doesn't break existing Dagger components
2. Migrate one feature module at a time, starting with new features (greenfield Hilt, legacy Dagger)
3. Each migrated `@Module` gets `@InstallIn(...)` — Hilt and Dagger components can coexist during migration
4. Remove the old `@Component` only after all modules feeding it are migrated
5. Split `DataModule.kt` into feature-scoped modules as part of migration (BookingModule, CheckinModule, ReservationModule)

> Full Hilt documentation: developer.android.com/training/dependency-injection/hilt-android

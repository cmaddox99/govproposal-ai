---
law_id: ENG-4.1
avatar: ios-swift
non_negotiable: true
authority: Jon Reid / Quality Coding (qualitycoding.org)
---

# ENG-4.1: Atomic TDD Examples for iOS (Swift)

> **Law:** Every code change MUST follow RED → GREEN → REFACTOR. One test at a time. No production code without a failing test first.

---

## Jon Reid's "Test Zero" Pattern

Every new test file starts with a deliberately failing test to verify infrastructure before any real tests are written. This is a small step that gives fast feedback — if Test Zero doesn't fail, something is wrong with your test setup.

```swift
// Step 0: Test Zero — deliberately failing, delete once you confirm it fails
import XCTest
@testable import MyApp

final class BoardingPassTests: XCTestCase {
    func test_zero() {
        XCTFail("Tests not yet implemented in BoardingPassTests")
    }
}
```

Once you see the red `test_zero` failure in Xcode's test navigator, delete it and proceed with the first real test.

---

## COMPLIANT: Full RED → GREEN → REFACTOR Cycle (XCTest)

### Step 1 — RED: Write ONE failing test

```swift
// BoardingPassTests.swift
func test_validBarcode_isAccepted() {
    // Arrange
    let validator = BoardingPassValidator()

    // Act
    let result = validator.validate(barcode: "AA1234567890")

    // Assert
    XCTAssertTrue(result.isValid)
}
// Run: xcodebuild test -scheme MyApp -only-testing:MyAppTests/BoardingPassTests/test_validBarcode_isAccepted
// Required output: TEST FAILED ✗
```

### Step 2 — GREEN: Write minimum code to pass

```swift
// BoardingPassValidator.swift
struct ValidationResult {
    let isValid: Bool
}

struct BoardingPassValidator {
    func validate(barcode: String) -> ValidationResult {
        return ValidationResult(isValid: true) // minimum to pass
    }
}
// Run tests again → Required output: TEST PASSED ✓
```

### Step 3 — REFACTOR: Add real behaviour, keep tests green

```swift
// Write the NEXT test first to drive real validation logic
func test_emptyBarcode_isRejected() {
    let validator = BoardingPassValidator()
    let result = validator.validate(barcode: "")
    XCTAssertFalse(result.isValid)
    XCTAssertEqual(result.failureReason, .emptyBarcode)
}

// Now refactor validator to support both tests:
enum ValidationFailure: Equatable {
    case emptyBarcode
    case invalidFormat
}

struct ValidationResult: Equatable {
    let isValid: Bool
    let failureReason: ValidationFailure?

    static let valid = ValidationResult(isValid: true, failureReason: nil)
}

struct BoardingPassValidator {
    private static let barcodePattern = /^[A-Z]{2}\d{10}$/

    func validate(barcode: String) -> ValidationResult {
        guard !barcode.isEmpty else {
            return ValidationResult(isValid: false, failureReason: .emptyBarcode)
        }
        guard barcode.wholeMatch(of: Self.barcodePattern) != nil else {
            return ValidationResult(isValid: false, failureReason: .invalidFormat)
        }
        return .valid
    }
}
// Run full suite → All tests PASSED ✓
```

---

## COMPLIANT: Same Cycle in Swift Testing (Xcode 16+)

```swift
@testable import MyApp
import Testing

// Use final class (not struct) — allows mutable spy properties, deinit teardown
final class BoardingPassTests: @unchecked Sendable {

    // Test Zero — delete after confirming it fails
    @Test
    func zero() async throws {
        Issue.record("Tests not yet implemented in BoardingPassTests")
    }

    // Step 1 — RED
    @Test
    func validBarcode_isAccepted() async throws {
        let validator = BoardingPassValidator()
        let result = validator.validate(barcode: "AA1234567890")
        #expect(result.isValid == true)
    }

    // Step 2 — after GREEN, drive next behaviour
    @Test
    func emptyBarcode_isRejected() async throws {
        let validator = BoardingPassValidator()
        let result = validator.validate(barcode: "")
        #expect(result.isValid == false)
        #expect(result.failureReason == .emptyBarcode)
    }
}
```

---

## COMPLIANT: Dependency Injection for ViewController Testing

Per Jon Reid: unit tests call code from the **inside** using DI — no XCUITest required for business logic.

```swift
// Protocol isolates the dependency
protocol FlightStatusService {
    func fetchStatus(for flightNumber: String) async throws -> FlightStatus
}

// RED: write test with mock
final class FlightStatusViewModelTests: XCTestCase {
    func test_fetchStatus_updatesState() async {
        // Arrange
        let mockService = MockFlightStatusService()
        mockService.stubbedStatus = FlightStatus(code: "ON_TIME", delay: 0)
        let sut = FlightStatusViewModel(service: mockService)

        // Act
        await sut.loadStatus(for: "AA100")

        // Assert
        XCTAssertEqual(sut.statusCode, "ON_TIME")
        XCTAssertFalse(sut.isLoading)
    }
}

// Mock (hand-written — no mock framework needed)
final class MockFlightStatusService: FlightStatusService {
    var stubbedStatus: FlightStatus?
    func fetchStatus(for flightNumber: String) async throws -> FlightStatus {
        return stubbedStatus!
    }
}
```

---

## VIOLATION: Multiple Behaviours in One Test

```swift
// BAD — tests multiple things, hides which behaviour is failing
func test_boardingPassFlow() {
    let validator = BoardingPassValidator()
    let scanner = BarcodeScanner()

    // VIOLATION: three separate concerns in one test
    XCTAssertTrue(validator.validate(barcode: "AA1234567890").isValid)
    XCTAssertFalse(validator.validate(barcode: "").isValid)
    let scanned = scanner.scan(image: UIImage())
    XCTAssertNotNil(scanned)  // VIOLATION: also tests scanner
}

// BAD — production code written before any test
struct BoardingPassValidator {
    func validate(barcode: String) -> ValidationResult {
        // VIOLATION: full implementation with no test driving it
        guard !barcode.isEmpty,
              barcode.count == 12,
              barcode.prefix(2).allSatisfy({ $0.isLetter }),
              barcode.dropFirst(2).allSatisfy({ $0.isNumber })
        else {
            return ValidationResult(isValid: false, failureReason: .invalidFormat)
        }
        return .valid
    }
}
```

**Why ENG-4.1 violated:** Multiple assertions per test obscure the failure cause. Production code written before a failing test skips the RED step — no evidence the test ever failed.

---

## TDD Commands for iOS

```bash
# RED: run specific test, confirm it fails
xcodebuild test \
  -scheme MyApp \
  -destination 'platform=iOS Simulator,name=iPhone 17' \
  -only-testing:MyAppTests/BoardingPassTests/test_validBarcode_isAccepted

# GREEN: write minimum code, run same test
xcodebuild test \
  -scheme MyApp \
  -destination 'platform=iOS Simulator,name=iPhone 17' \
  -only-testing:MyAppTests/BoardingPassTests/test_validBarcode_isAccepted

# REFACTOR: run all domain tests to verify nothing broken
xcodebuild test \
  -scheme MyApp \
  -destination 'platform=iOS Simulator,name=iPhone 17' \
  -only-testing:MyAppTests/Domain

# VERIFY: full suite + coverage + lint
xcodebuild test -scheme MyApp -destination 'platform=iOS Simulator,name=iPhone 17' -enableCodeCoverage YES
aa-constitution-lint .

bundle exec fastlane run_unit_tests
```

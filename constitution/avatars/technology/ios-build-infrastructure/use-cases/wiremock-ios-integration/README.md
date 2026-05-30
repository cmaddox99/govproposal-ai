# Use Case: WireMock iOS Integration

**Avatar:** ios-build-infrastructure v1.0.0
**Law:** ENG-4.1 (Atomic TDD Law)
**Context:** Adding network-dependent tests to `americanmobileapp-ios` using WireMock stubs.

---

## Scenario

A developer needs to test a view model that calls the flight-status API. The test should stub the network call and assert on the response — without hitting the real AA backend.

## Constraints

- `Foundation.Process` is unavailable in iOS SDK test targets — WireMock JAR must be started externally
- Production `RequestRewriteProtocol` is not importable into the test target — use a self-contained `URLProtocol` subclass

## Pattern

**1. Start WireMock externally before `xcodebuild test`**
```bash
java -jar ~/projects/mobile-wiremock-stubs/wiremock/wiremock.jar \
  --port 8080 --root-dir ~/projects/mobile-wiremock-stubs/wiremock &
curl -s http://localhost:8080/__admin/health | grep healthy
```

**2. Register `AAWireMockURLProtocol` in test setUp**
```swift
override class func setUp() {
    super.setUp()
    URLProtocol.registerClass(AAWireMockURLProtocol.self)
}
override class func tearDown() {
    URLProtocol.unregisterClass(AAWireMockURLProtocol.self)
    super.tearDown()
}
```

**3. Use `XCTUnwrap` — never force-unwrap**
```swift
// ✅ Fails gracefully; other tests continue
let data = try XCTUnwrap(receivedData, "Is WireMock running on :8080?")
```

**4. Add stub mapping in `wiremock/mappings/`**
```json
{
  "request": { "method": "GET", "urlPattern": "/v2/flightstatus/.*" },
  "response": { "status": 200, "bodyFileName": "flight-status-200.json" }
}
```

## Expected Outcome

Tests using `AAWireMockURLProtocol` intercept AA API hosts and resolve against WireMock stubs at `localhost:8080`. If WireMock is down, `XCTUnwrap` fails the test gracefully — the rest of the suite continues running.

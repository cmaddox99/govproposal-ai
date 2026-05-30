# Use Case: Build a Feature Module with Atomic TDD
# Avatar: avatar-ios-swift | Laws: ENG-4.1, ENG-3.2, ENG-3.1
# Grounded in: booking-ios structural patterns — MVVM + Coordinator, XCTest GIVEN-WHEN-THEN

use_case:
  id: uc-ios-feature-module-tdd
  name: Build a New Feature Module with Atomic TDD
  jtbd: "When I start a new iOS feature, I need a tested, coherent module structure I can grow without regressions."
  actor: iOS Engineer
  laws: [ENG-4.1, ENG-3.2, ENG-3.1]

---

## Pre-conditions

- Feature is defined by a vertical slice (single JTBD, single navigator)
- A target test file exists before any production code is written (Test Zero law)

## Main Flow

1. Create the module directory with the standard layout:
   ```
   FeatureName/
     Sources/
       ViewModel/     (business logic, Combine bindings)
       View/          (SwiftUI or UIKit — no business logic)
       Coordinator/   (navigation only)
     Tests/
       FeatureTests.swift
   ```
2. Write `Test Zero` — an `XCTFail("not yet implemented")` that verifies the test harness runs
3. Write the first failing test (RED) against the ViewModel — no production code yet
4. Write the minimum code to make it pass (GREEN)
5. Refactor to remove duplication (REFACTOR) — test still green
6. Repeat cycle for each new behaviour
7. Coordinator tests validate navigation actions — mock the router protocol
8. View does not contain `if` statements or business logic — verify at code review

## Single Responsibility Check (ENG-3.1)

A file over 200 lines is a warning. Over 300 lines is a review flag. The booking-ios `BookingSearchCoordinator` at 461 lines is a documented violation — do not replicate this pattern.

## What Not to Do

- Do not write a `// TODO: add tests later` comment — this is a BLOCK under ENG-4.1
- Do not use `!` (force unwrap) in production code — the booking-ios codebase has ~4 force unwraps; keep this count flat or reduce it
- Do not put routing logic in the ViewModel

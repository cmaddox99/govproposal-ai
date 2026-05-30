# ENG-3.3 — Law of Demeter (Java/Spring, AA BFF Context)

> **AA fleet finding:** Builder classes routinely chain through 4-5 object layers to extract data. This is information expert violation + Demeter violation combined.

## The Rule

A method may call methods on:
1. `this`
2. Objects passed as parameters
3. Objects it creates
4. Direct fields of `this`

**Not on:** objects returned by calling methods on other objects.

## Pattern

```java
// ❌ Train wreck — 4-layer chain in AA BFF builders
String carrier = reservation.getFlights().get(0).getSegments().get(0).getOperatingCarrier().getCode();

// ✅ Ask the object that knows
String carrier = reservation.firstOperatingCarrierCode();
// Reservation knows how to navigate its own structure
```

## AA BFF Builder Violation Pattern

```java
// ❌ SeatsBuilder.java (aa-ct-mobile-manage-bff) — reaches into nested graphs
for (Cabin cabin : flight.getAircraftDetails().getCabins()) {
    for (Row row : cabin.getRows()) {
        for (Seat seat : row.getSeats()) {
            // O(n³) — all three loops reach into objects they don't own
            float price = seat.getPricingDetails().getUsdAmount(); // 4 levels deep
        }
    }
}

// ✅ Push the query to the object that owns the data
List<Seat> availableSeats = flight.findAvailableSeatsWithPrice(cabinType);
```

## The Test

If your code has `a.getB().getC().getD()` you have a Demeter violation. Refactor: move the behavior to the object that owns `b`.

> Full Demeter patterns in `ENG-3.3-demeter-detail.md`.

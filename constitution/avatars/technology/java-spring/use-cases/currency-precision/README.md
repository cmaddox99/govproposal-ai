# Use Case: Currency Precision — BigDecimal(String) Not BigDecimal(double)

**Avatar:** avatar-java-spring  
**Laws:** ENG-3.1 (Complexity / Bug Prevention), ENG-4.1 (Atomic TDD)  
**AA Evidence:** mobile-change-bff — `ReshopBuilder.java` (CRITICAL bug)  
**Risk level:** CRITICAL — customers see incorrect fare difference prices

## The Bug

```java
// ❌ CRITICAL BUG — mobile-change-bff ReshopBuilder.java
BigDecimal fareDifference = new BigDecimal(299.99); // double constructor
// IEEE 754: 299.99 is actually 299.9899999999999948840923...
// Result: customer shown $299.98 instead of $299.99
```

`BigDecimal(double)` inherits the floating-point imprecision of the `double` argument. For financial calculations this means wrong prices can reach customers.

## The Fix

```java
// ✅ String constructor — exact representation
BigDecimal fareDifference = new BigDecimal("299.99");   // always exact
BigDecimal fareDifference = BigDecimal.valueOf(299.99); // also safe — uses canonical string form

// ✅ Arithmetic with scale
BigDecimal newFare = baseFare.add(fareDifference)
    .setScale(2, RoundingMode.HALF_UP); // always specify scale for money
```

## The Test That Would Have Caught It

```java
@Test
void calculateFareDifference_preservesCentsAccurately() {
    // Arrange — values chosen to expose double precision loss
    Fare base     = Fare.of("199.99");
    Fare upgraded = Fare.of("299.99");

    // Act
    Money diff = fareCalculator.difference(base, upgraded);

    // Assert — isEqualByComparingTo ignores scale; assertEquals("100.00") would work too
    assertThat(diff.amount()).isEqualByComparingTo("100.00");
    assertThat(diff.amount().scale()).isEqualTo(2);
}
```

## Canonical AA BFF Pattern for Currency

```java
public record Fare(BigDecimal amount, Currency currency) {

    public static Fare of(String amountString) {
        return new Fare(new BigDecimal(amountString), Currency.USD);
    }

    public Fare add(Fare other) {
        requireSameCurrency(other);
        return new Fare(this.amount.add(other.amount).setScale(2, HALF_UP), currency);
    }

    public Fare subtract(Fare other) {
        requireSameCurrency(other);
        return new Fare(this.amount.subtract(other.amount).setScale(2, HALF_UP), currency);
    }
}
```

## Scope in AA BFF Fleet

Search all Java repos for `new BigDecimal(` patterns where the argument is a double/float literal or a double variable. Any fare, price, tax, or fee calculation is at risk. mobile-change-bff ReshopBuilder was the confirmed instance; airfare-search-bff has similar fare manipulation code.

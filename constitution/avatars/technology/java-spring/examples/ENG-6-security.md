---
laws: [ENG-6.1, ENG-6.4, ENG-6.7]
avatar: [java-spring]
title: Security Laws — Java Spring
---

# Security Laws: ENG-6.1, ENG-6.4, ENG-6.7 — Java Spring

## ENG-6.1: Security by Design

Configure Spring Security with explicit CORS, CSP headers, and JWT decoder. Never use `anyRequest().permitAll()`.

```java
@Configuration
@EnableWebSecurity
@EnableMethodSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        return http
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/public/**").permitAll()
                .requestMatchers("/api/admin/**").hasRole("SUPERVISOR")
                .anyRequest().authenticated())          // deny by default
            .oauth2ResourceServer(oauth2 -> oauth2.jwt(Customizer.withDefaults()))
            .cors(cors -> cors.configurationSource(corsConfig()))  // explicit — not permitAll
            .headers(h -> h
                .contentSecurityPolicy(csp -> csp.policyDirectives(
                    "default-src 'self'; object-src 'none'")))
            .build();
    }

    @Bean
    public JwtDecoder jwtDecoder() {
        return JwtDecoders.fromIssuerLocation(env.getProperty("spring.security.oauth2.resourceserver.jwt.issuer-uri"));
    }
}
```

Apply least-privilege method-level checks on service layer:

```java
@Service
public class BookingService {
    @PreAuthorize("hasRole('AGENT') or hasRole('SUPERVISOR')")
    public Booking rebook(String pnr, String newFlightId) { ... }

    @PreAuthorize("hasRole('SUPERVISOR')")
    public void cancelWithRefund(String pnr) { ... }
}
```

## ENG-6.4: Data Protection

Mark PII with a custom annotation; use Jasypt for encrypted properties; never log passenger data.

```java
// @PiiField marks fields for compile-time / static-analysis checks
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.FIELD)
public @interface PiiField {}

public class Passenger {
    @PiiField private String email;
    @PiiField private String name;
    private String pnr;        // booking reference — treat as sensitive but not PII
}
```

```yaml
# application.yml — use Jasypt encrypted values, never plain text
datasource:
  password: ENC(xT9kL2mN8pQ...)
```

Log order/booking IDs — never passenger names or emails:

```java
@Slf4j
@Service
public class RebookingService {
    public void rebook(String pnr, String flightId, String correlationId) {
        // ✅ Safe: only business keys
        log.info("Rebooking initiated pnr={} flightId={} correlationId={}",
                 pnr, flightId, correlationId);
        // ❌ NEVER: log.info("Passenger {} rebooked", passenger.getName());
    }
}
```

## ENG-6.7: Audit Trail

Use Spring Data Auditing plus an INSERT-only repository. Propagate `correlationId` via MDC.

```java
// CorrelationFilter.java
@Component
public class CorrelationFilter extends OncePerRequestFilter {
    @Override
    protected void doFilterInternal(HttpServletRequest req,
                                    HttpServletResponse res,
                                    FilterChain chain) throws IOException, ServletException {
        String tid = Optional.ofNullable(req.getHeader("X-Correlation-ID"))
                             .orElse(UUID.randomUUID().toString());
        MDC.put("correlationId", tid);
        res.setHeader("X-Correlation-ID", tid);
        try { chain.doFilter(req, res); } finally { MDC.clear(); }
    }
}
```

```java
// AuditLog.java
@Entity
@Table(name = "booking_audit")
@EntityListeners(AuditingEntityListener.class)
public class AuditLog {
    @Id @GeneratedValue private Long id;
    @CreatedDate private Instant recordedAt;
    @CreatedBy  private String actorId;
    private String action;         // REBOOK, CANCEL, UPGRADE
    private String entityId;       // PNR or bookingId
    private String correlationId;
    // ❌ No mutable fields — no @LastModifiedDate, no UPDATE path
}

// AuditRepository.java — expose save only
public interface AuditRepository extends Repository<AuditLog, Long> {
    AuditLog save(AuditLog entry);   // INSERT only; no delete/update methods
}
```

Emit Micrometer counter for security events:

```java
meterRegistry.counter("security.events", "type", "unauthorized_access",
    "correlationId", correlationId).increment();
```

## Anti-Patterns

1. **`anyRequest().permitAll()`** — opens every endpoint to unauthenticated callers; every route must be explicitly permitted or protected.
2. **Logging sensitive request parameters** — Spring's `CommonsRequestLoggingFilter` by default logs query strings containing PNR, email, and seat selections; disable or filter before enabling.
3. **JDBC URL with password visible in logs** — Spring Boot autoconfiguration may log the `DataSource` URL at DEBUG level; use `spring.datasource.url` with Jasypt encryption and ensure DEBUG is disabled in production.
4. **`@PreAuthorize("isAuthenticated()")` everywhere** — authentication without role checks means any valid token (including customer self-service tokens) can call agent-only endpoints.
5. **API keys in `application.properties`** — any secret in a properties file is one Git commit away from exposure; use Spring Cloud Config with Vault or Azure Key Vault binding.

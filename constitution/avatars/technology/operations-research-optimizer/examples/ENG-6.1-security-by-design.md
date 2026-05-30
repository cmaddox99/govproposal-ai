---
law_id: ENG-6.1
avatar: operations-research-optimizer
---

# ENG-6.1: Security by Design Examples for Operations Research / MIP Optimizer

---

## COMPLIANT: OAuth Token Fetched Once, Never Logged

```java
// ✅ Token obtained from secure source, never written to logs
@Component
public class FsaClientImpl {

    private final AppProperties appProperties;
    private final WebClient webClient;

    public String fetchOAuthToken() {
        return webClient.post()
                .uri(appProperties.getAuthTokenUrl())
                .bodyValue(buildTokenRequest())  // credentials come from injected config
                .retrieve()
                .bodyToMono(TokenResponse.class)
                .map(TokenResponse::getAccessToken)
                .block();
        // ✅ Token is returned to caller — never logged here
    }

    public List<StudentScheduleDto> getStudentScheduleDtos(String contractMonth) {
        String token = fetchOAuthToken();
        // ✅ token used in Authorization header only
        return webClient.get()
                .uri(...)
                .header(HttpHeaders.AUTHORIZATION, "Bearer " + token)
                .retrieve()
                .bodyToFlux(StudentScheduleDto.class)
                .collectList()
                .block();
    }
}
```

**Why compliant:** Credentials come from injected `AppProperties` (not hardcoded). The token is never passed to `log.*()`. It lives only in memory for the duration of the API call.

---

## COMPLIANT: Client Certificates Loaded from Secure Store

```java
// ✅ Certificate loaded from keystore path in application properties — not bundled in code
@Configuration
public class CcsWebClientConfig {

    @Bean
    public WebClient ccsWebClient(AppProperties appProperties) throws Exception {
        SslContext sslContext = SslContextBuilder
                .forClient()
                .keyManager(
                        loadCertificate(appProperties.getCcsCertPath()),
                        loadPrivateKey(appProperties.getCcsCertKeyPath()))
                .build();

        return WebClient.builder()
                .clientConnector(new ReactorClientHttpConnector(
                        HttpClient.create().secure(spec -> spec.sslContext(sslContext))))
                .build();
    }
}
```

**Why compliant:** Certificate paths are externalised to `AppProperties` (bound from environment-specific `application-{profile}.properties`, which are not in version control). No certificate material is hardcoded.

---

## VIOLATION: Credentials Hardcoded in Source

```java
// ❌ VIOLATES ENG-6.1 — credentials committed to version control
public class FsaClientImpl {

    private static final String CLIENT_ID = "jose-prod-client";       // ← in repo
    private static final String CLIENT_SECRET = "s3cr3tP@ssw0rd!";   // ← in repo

    public String fetchOAuthToken() {
        return webClient.post()
                .bodyValue(Map.of(
                        "client_id", CLIENT_ID,
                        "client_secret", CLIENT_SECRET))
                .retrieve()
                ...
    }
}
```

**Why violates ENG-6.1:** Secrets committed to source control are permanently exposed — even after deletion, git history retains them. This is a critical security failure regardless of repo visibility.

---

## VIOLATION: Bearer Token Written to Log

```java
// ❌ VIOLATES ENG-6.1 — token appears in log output and log files
public List<StudentScheduleDto> getStudentScheduleDtos(String contractMonth) {
    String token = fetchOAuthToken();
    log.debug("Using token: {}", token);  // ← token in logs = credential exposure
    ...
}
```

**Why violates ENG-6.1:** Log files are often shipped to centralised log aggregators (Splunk, Azure Monitor). A bearer token in logs means it's readable by anyone with log access — and may be replayed until expiry.


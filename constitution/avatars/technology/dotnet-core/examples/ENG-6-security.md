---
laws: [ENG-6.1, ENG-6.4, ENG-6.7]
avatar: [dotnet-core]
title: Security Laws — .NET Core
---

# Security Laws: ENG-6.1, ENG-6.4, ENG-6.7 — .NET Core

## ENG-6.1: Security by Design

Use `[Authorize]` with named policies and load secrets from Azure Key Vault — never from `appsettings.json`.

```csharp
// Program.cs
builder.Configuration.AddAzureKeyVault(
    new Uri(builder.Configuration["KeyVault:Uri"]!),
    new DefaultAzureCredential());

builder.Services.AddAuthorization(opts =>
{
    opts.AddPolicy("AgentOnly", p => p.RequireRole("Agent", "Supervisor"));
    opts.AddPolicy("SupervisorOnly", p => p.RequireRole("Supervisor"));
});

// BookingController.cs
[ApiController, Route("api/bookings")]
[Authorize(Policy = "AgentOnly")]
public class BookingController : ControllerBase
{
    [HttpDelete("{id}")]
    [Authorize(Policy = "SupervisorOnly")]   // least-privilege escalation
    public async Task<IActionResult> CancelBooking(string id) { ... }
}
```

Validate every inbound model with FluentValidation:

```csharp
public class RebookRequestValidator : AbstractValidator<RebookRequest>
{
    public RebookRequestValidator()
    {
        RuleFor(x => x.Pnr).Matches(@"^[A-Z]{6}$").WithMessage("Invalid PNR format");
        RuleFor(x => x.NewFlightId).NotEmpty().MaximumLength(10);
    }
}
```

Use ASP.NET Core Data Protection for token generation — never `new Random()`:

```csharp
var protector = _dataProtectionProvider.CreateProtector("BookingTokens");
string token = protector.Protect(userId + ":" + bookingId);
```

## ENG-6.4: Data Protection

Mark PII fields with `[PersonalData]` and encrypt sensitive columns at the EF Core layer:

```csharp
// Passenger.cs
public class Passenger
{
    public int Id { get; set; }
    [PersonalData] public string Email { get; set; } = default!;
    [PersonalData] public string Name { get; set; } = default!;
    public string Pnr { get; set; } = default!;        // booking key, not PII per se
}

// EncryptedStringConverter.cs (EF Core ValueConverter + AES-GCM)
public class EncryptedStringConverter : ValueConverter<string, string>
{
    public EncryptedStringConverter(byte[] key) : base(
        v => AesGcmEncrypt(v, key),
        v => AesGcmDecrypt(v, key)) { }
}

// DbContext
modelBuilder.Entity<Passenger>()
    .Property(p => p.Email)
    .HasConversion(new EncryptedStringConverter(_encryptionKey));
```

Never log request bodies containing PII:

```csharp
// ❌ NEVER
_logger.LogInformation("Request: {Body}", await new StreamReader(Request.Body).ReadToEndAsync());

// ✅ Log safe correlation metadata only
_logger.LogInformation("RebookRequest received {@Meta}",
    new { CorrelationId = HttpContext.TraceIdentifier, FlightId = request.NewFlightId });
```

## ENG-6.7: Audit Trail

Propagate correlation ID via middleware and enrich Serilog with it. Audit rows are INSERT-only:

```csharp
// CorrelationIdMiddleware.cs
public async Task InvokeAsync(HttpContext context)
{
    var tid = context.Request.Headers["X-Correlation-ID"].FirstOrDefault()
              ?? Activity.Current?.TraceId.ToString()
              ?? Guid.NewGuid().ToString();
    context.Items["CorrelationId"] = tid;
    using (LogContext.PushProperty("CorrelationId", tid))
    {
        context.Response.Headers["X-Correlation-ID"] = tid;
        await _next(context);
    }
}

// AuditRepository.cs — INSERT only, no Update method exposed
public async Task RecordAsync(AuditEntry entry)
{
    // EF Core: Add + SaveChanges — no _context.Update(entry) ever
    _context.AuditLogs.Add(entry);
    await _context.SaveChangesAsync();
}
```

Use Serilog enrichers in `Program.cs`:

```csharp
Log.Logger = new LoggerConfiguration()
    .Enrich.WithMachineName()
    .Enrich.WithEnvironmentName()
    .Enrich.FromLogContext()          // picks up CorrelationId pushed above
    .WriteTo.Console(new JsonFormatter())
    .CreateLogger();
```

## Anti-Patterns

1. **Connection strings in `appsettings.json`** — committed to Git, readable by anyone with repo access. Use Azure Key Vault or user-secrets for local dev.
2. **Logging `Request.Body` verbatim** — contains passenger PII (name, email, payment data). Log only safe identifiers.
3. **`UPDATE` on audit log rows** — audit records must be immutable; any update destroys the evidentiary chain. Use append-only tables with a PostgreSQL `RULE` or EF Core convention that prevents `DbContext.Update` on audit entities.
4. **Disabling HTTPS in production** — `app.UseHttpsRedirection()` must not be gated behind an `IsDevelopment()` check in production deployments.
5. **Returning stack traces in 500 responses** — `UseDeveloperExceptionPage()` exposes internal paths and class names; use `UseExceptionHandler` with a safe problem-details response in production.

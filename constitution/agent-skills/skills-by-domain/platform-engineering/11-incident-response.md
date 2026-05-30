---
skill:
  id: skill-11-incident-response
  name: Incident Response
  category: operations
  version: "2.0.0"

laws:
  implements:
    - id: BUS-9.1
      title: Incident Classification Law
    - id: BUS-9.2
      title: Incident Response Law
    - id: BUS-9.3
      title: Breach Notification Law (NON-NEGOTIABLE)
    - id: BUS-9.4
      title: Root Cause Analysis Law
  references:
    - id: ENG-5.5
      title: Observability Law

triggers:
  phrases:
    - "Production incident"
    - "System down"
    - "Postmortem needed"
    - "Root cause analysis"

followed_by:
  - skill-13-observability
  - skill-16-documentation
---

# Skill: Incident Response

> **Purpose:** Systematically detect, respond to, and learn from production incidents to minimize impact and prevent recurrence.

---

## Purpose

Incident Response is the disciplined practice of handling production issues effectively. This skill ensures:

1. **Rapid detection** - Know when things break before users tell you
2. **Structured response** - Clear process reduces chaos during incidents
3. **Effective communication** - Stakeholders informed appropriately
4. **Root cause analysis** - Understand why, not just what
5. **Continuous improvement** - Incidents make the system stronger

**Key principle:** Incidents are learning opportunities. Blame the system, not the people.

---

## When to Invoke

Invoke this skill when:

- Alerts fire indicating production issues
- Users report problems with the system
- Monitoring shows anomalies
- Deployments cause unexpected behavior
- Security incidents are detected
- After resolution, for postmortem analysis

**Trigger phrases:**
- "Production is down"
- "Users are reporting errors"
- "We're seeing elevated error rates"
- "Something's wrong in prod"
- "Let's do a postmortem"

---

## Constitutional Foundation

### Engineering Constitution
- **Article VI, Section 6.1** - Observability: Systems must be observable
- **Article VI, Section 6.2** - Reliability: Defined SLOs and error budgets
- **Article IV, Section 4.1** - Test-First: Tests prevent regressions

### Product Constitution
- **Article VI, Section 6.1** - User Trust: Minimize user impact
- **Article VI, Section 6.2** - Communication: Keep users informed

### Business Constitution
- **Article IV, Section 4.1** - Continuity: Business operations maintained
- **Article III, Section 3.3** - Audit Trail: Incidents documented

---

## Incident Severity Levels

| Severity | Impact | Response Time | Examples |
|----------|--------|---------------|----------|
| **SEV-1** | Complete outage, all users affected | Immediate (15 min) | Site down, data loss, security breach |
| **SEV-2** | Major feature broken, many users affected | 30 minutes | Payment processing down, login broken |
| **SEV-3** | Minor feature broken, some users affected | 2 hours | Search slow, minor UI bugs |
| **SEV-4** | Minimal impact, workaround exists | Next business day | Cosmetic issues, edge cases |

---

## Method: Incident Response Process

### Phase 1: Detection & Alert

**Signals:**
- Automated alerts (error rates, latency, availability)
- User reports
- Synthetic monitoring failures
- Log anomalies

**Initial Assessment:**
```markdown
## Incident Detected

**Time:** [timestamp]
**Source:** [how detected]
**Initial Symptoms:** [what's happening]
**Affected Systems:** [which services]
**User Impact:** [who's affected, how many]
**Severity:** SEV-[1-4]
```

---

### Phase 2: Triage & Escalation

**Assign Roles:**

| Role | Responsibility |
|------|----------------|
| **Incident Commander (IC)** | Coordinates response, makes decisions |
| **Technical Lead** | Investigates and implements fixes |
| **Communications Lead** | Updates stakeholders and users |
| **Scribe** | Documents timeline and actions |

**Escalation Matrix:**

```
SEV-1: IC + On-call engineer + Engineering lead + VP Engineering
SEV-2: IC + On-call engineer + Team lead
SEV-3: On-call engineer + Team lead
SEV-4: On-call engineer
```

---

### Phase 3: Investigation

**Gather Information:**

```bash
# Check recent deployments
git log --oneline -10

# Check error rates
# [monitoring dashboard link]

# Check logs
kubectl logs -f deployment/api --since=30m | grep ERROR

# Check metrics
# CPU, memory, request latency, error rates
```

**Investigation Questions:**
1. What changed recently? (deploys, config, traffic)
2. When did it start?
3. What's the blast radius?
4. What are the error messages?
5. Is it getting worse or stable?

**Document Timeline:**
```markdown
## Timeline

| Time | Event |
|------|-------|
| 14:32 | Alert fired: error rate > 5% |
| 14:35 | IC assigned: @engineer |
| 14:38 | Identified: deployment at 14:30 |
| 14:42 | Rollback initiated |
| 14:45 | Service recovering |
| 14:50 | All clear, error rate normal |
```

---

### Phase 4: Mitigation

**Mitigation Strategies (in order of preference):**

1. **Rollback** - Fastest, safest if recent deploy caused issue
2. **Feature flag disable** - Isolate problematic feature
3. **Scale up** - If capacity related
4. **Failover** - Switch to backup systems
5. **Hotfix** - Last resort, only if others won't work

**Rollback Procedure:**
```bash
# Kubernetes rollback
kubectl rollout undo deployment/api

# Verify rollback
kubectl rollout status deployment/api

# Check error rates dropping
```

**DO NOT during incident:**
- Deploy new code (unless hotfix approved by IC)
- Make config changes unrelated to incident
- Panic

---

### Phase 5: Communication

**Internal Updates (every 15-30 min for SEV-1/2):**
```markdown
## Incident Update - [Time]

**Status:** Investigating | Mitigating | Monitoring | Resolved
**Impact:** [current user impact]
**Actions:** [what we're doing]
**ETA:** [when we expect resolution]
**Next Update:** [when]
```

**External Communication (if user-facing):**
```markdown
## Status Page Update

**Title:** [Service] Degraded Performance

We are currently experiencing issues with [service].
Some users may experience [symptoms].

Our team is actively investigating and working on a fix.
We will provide updates as we have more information.

Last updated: [time]
```

---

### Phase 6: Resolution

**Verify Resolution:**
- [ ] Error rates returned to normal
- [ ] Latency returned to normal
- [ ] Affected features working
- [ ] No new alerts firing
- [ ] User reports stopped

**Close Incident:**
```markdown
## Incident Resolved

**Duration:** [start] to [end] ([X] minutes)
**Root Cause:** [brief description]
**Resolution:** [what fixed it]
**Follow-up:** [postmortem scheduled]
```

---

### Phase 7: Postmortem

**Blameless Postmortem Template:**

```markdown
# Postmortem: [Incident Title]

## Summary
**Date:** [date]
**Duration:** [X] minutes
**Severity:** SEV-[N]
**Author:** [name]

## Impact
- [X] users affected
- [Y] revenue impact (if applicable)
- [Description of user experience]

## Timeline
| Time | Event |
|------|-------|
| ... | ... |

## Root Cause
[Detailed technical explanation of what went wrong]

## Contributing Factors
1. [Factor 1]
2. [Factor 2]

## What Went Well
- [Thing 1]
- [Thing 2]

## What Went Poorly
- [Thing 1]
- [Thing 2]

## Action Items
| Action | Owner | Due Date |
|--------|-------|----------|
| [Action 1] | @person | [date] |
| [Action 2] | @person | [date] |

## Lessons Learned
[Key takeaways for the team]
```

---

## Runbook Templates

### High Error Rate

```markdown
## Runbook: High Error Rate

### Symptoms
- Error rate alert firing (> 5%)
- 5xx responses increasing

### Investigation Steps
1. Check recent deployments
   ```bash
   git log --oneline -10
   ```

2. Check error logs
   ```bash
   kubectl logs deployment/api --since=10m | grep -i error
   ```

3. Check dependent services
   - Database connectivity
   - External API status
   - Cache availability

### Mitigation Steps
1. If recent deploy: rollback
2. If dependency issue: enable circuit breaker
3. If capacity issue: scale up

### Escalation
If not resolved in 15 minutes, escalate to team lead.
```

### Database Connection Issues

```markdown
## Runbook: Database Connection Issues

### Symptoms
- Connection timeout errors
- "Too many connections" errors
- Queries timing out

### Investigation Steps
1. Check connection pool status
2. Check database CPU/memory
3. Check for long-running queries
4. Check for connection leaks

### Mitigation Steps
1. Kill long-running queries
2. Restart affected pods (one at a time)
3. Scale database if capacity issue

### Prevention
- Connection pool limits
- Query timeouts
- Regular connection pool health checks
```

---

## Good Examples

### Example 1: Well-Handled SEV-2

```markdown
## Incident: Payment Processing Failure

**Timeline:**
- 10:15 - Alert: payment_errors > 10%
- 10:17 - IC assigned, investigation started
- 10:22 - Root cause: payment provider API returning 503
- 10:25 - Enabled fallback payment provider
- 10:28 - Payments recovering
- 10:35 - All clear, monitoring

**What went well:**
- Alert fired quickly
- Runbook was up to date
- Fallback provider worked as designed
- Communication was timely

**Action items:**
- Add synthetic transaction monitoring
- Automate failover for payment providers
```

---

## Bad Examples (Anti-Patterns)

### Anti-Pattern 1: Hero Culture

```markdown
# BAD - Single person "fixes" everything

"I'll just SSH into production and fix it"
- No communication
- No documentation
- No review
- Creates knowledge silos
```

**Correct approach:** Follow process, document actions, involve team.

---

### Anti-Pattern 2: Blame Game

```markdown
# BAD - Postmortem focuses on who

"This happened because John deployed without testing"

# Result: People hide mistakes, culture of fear
```

**Correct approach:** Focus on systems and processes, not individuals.

---

### Anti-Pattern 3: No Follow-Through

```markdown
# BAD - Postmortem action items never done

Postmortem from 3 months ago:
- [ ] Add monitoring for X (never done)
- [ ] Fix race condition (never done)
- [ ] Update runbook (never done)

# Same incident happens again
```

**Correct approach:** Track action items, assign owners, set deadlines.

---

## Quality Checklist

Before considering incident resolved:

### During Incident
- [ ] Severity correctly assessed
- [ ] Roles assigned
- [ ] Timeline documented
- [ ] Stakeholders informed
- [ ] Mitigation verified

### After Incident
- [ ] Postmortem scheduled (within 48h for SEV-1/2)
- [ ] Timeline complete
- [ ] Root cause identified
- [ ] Action items assigned
- [ ] Runbooks updated

### Prevention
- [ ] Similar incidents prevented
- [ ] Monitoring improved
- [ ] Documentation updated
- [ ] Team retrospective held

---

## Skill Interactions

### Preceded By
- **10-Security Review** - Security incidents may trigger response

### Followed By
- **06-Atomic TDD** - Fixes implemented via TDD
- **09-Refactoring** - Systemic improvements

### Related Skills
- **08-Code Review** - Review of hotfixes

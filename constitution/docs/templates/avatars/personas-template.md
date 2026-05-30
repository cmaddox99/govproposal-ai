# Persona Template

Use this template to define user personas for your product avatar.  
**Location:** `avatars/product-type/{{ product }}/examples/personas.md`

---

## Personas: {{ Product }}

### Persona 1: {{ Name }}

**Role:** {{ Job Title }}  
**Organization:** {{ Organization Type }}  
**Experience Level:** {{ Beginner | Intermediate | Advanced }}

**Goals:**
- Goal 1 related to {{ product }}
- Goal 2 related to {{ product }}
- Goal 3 related to {{ product }}

**Pain Points:**
- Pain point 1
- Pain point 2
- Pain point 3

**Key Behaviors:**
- Behavior 1 (how they interact with {{ product }})
- Behavior 2 (decisions they make)
- Behavior 3 (frequency of engagement)

**Example Quote:**
> "{{ Authentic quote reflecting their perspective on {{ product }}}}"

**Relevant Laws:**
- PRD-{{ Law Number }}: {{ Why this law matters to this persona }}
- PRD-{{ Law Number }}: {{ Why this law matters to this persona }}

---

### Persona 2: {{ Name }}

**Role:** {{ Job Title }}  
**Organization:** {{ Organization Type }}  
**Experience Level:** {{ Beginner | Intermediate | Advanced }}

**Goals:**
- Goal 1
- Goal 2
- Goal 3

**Pain Points:**
- Pain point 1
- Pain point 2
- Pain point 3

**Key Behaviors:**
- Behavior 1
- Behavior 2
- Behavior 3

**Example Quote:**
> "{{ Authentic quote }}"

**Relevant Laws:**
- PRD-{{ Law Number }}: {{ Why this law matters }}
- PRD-{{ Law Number }}: {{ Why this law matters }}

---

### Persona 3: {{ Name }}

**Role:** {{ Job Title }}  
**Organization:** {{ Organization Type }}  
**Experience Level:** {{ Beginner | Intermediate | Advanced }}

**Goals:**
- Goal 1
- Goal 2
- Goal 3

**Pain Points:**
- Pain point 1
- Pain point 2
- Pain point 3

**Key Behaviors:**
- Behavior 1
- Behavior 2
- Behavior 3

**Example Quote:**
> "{{ Authentic quote }}"

**Relevant Laws:**
- PRD-{{ Law Number }}: {{ Why this law matters }}
- PRD-{{ Law Number }}: {{ Why this law matters }}

---

## Persona Journeys

### {{ Persona 1 }}: {{ Journey Name }}

```
Step 1: {{ Step description }}
  └─ Need: {{ What they need }}
  └─ Law: PRD-{{ Number }} ({{ Why }})

Step 2: {{ Step description }}
  └─ Need: {{ What they need }}
  └─ Law: PRD-{{ Number }} ({{ Why }})

Step 3: {{ Step description }}
  └─ Need: {{ What they need }}
  └─ Law: PRD-{{ Number }} ({{ Why }})

Outcome: {{ Success metric }}
```

---

### {{ Persona 2 }}: {{ Journey Name }}

```
Step 1: {{ Step description }}
  └─ Need: {{ What they need }}
  └─ Law: PRD-{{ Number }} ({{ Why }})

Step 2: {{ Step description }}
  └─ Need: {{ What they need }}
  └─ Law: PRD-{{ Number }} ({{ Why }})

Outcome: {{ Success metric }}
```

---

## Persona-Law Mapping

| Persona | PRD-1.1 | PRD-2.1 | PRD-3.1 | PRD-4.1 | PRD-5.1 |
|---------|---------|---------|---------|---------|---------|
| {{ Name 1 }} | ✅ Critical | ✅ Important | ⚠️ Nice to Have | ✅ Critical | ✅ Important |
| {{ Name 2 }} | ⚠️ Nice to Have | ✅ Critical | ✅ Important | ⚠️ Nice to Have | ✅ Critical |
| {{ Name 3 }} | ✅ Important | ⚠️ Nice to Have | ✅ Critical | ✅ Important | ⚠️ Nice to Have |

**Legend:**
- ✅ Critical: This persona can't do their job without this law
- ✅ Important: This law significantly improves their effectiveness
- ⚠️ Nice to Have: This law is helpful but not essential

---

**Last Updated:** {{ YYYY-MM-DD }}  
**Product:** {{ Product Name }}  
**Research Date:** {{ When personas were validated }}

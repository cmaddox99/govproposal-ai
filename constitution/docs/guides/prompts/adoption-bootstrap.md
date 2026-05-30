# Adoption Bootstrap Prompt

> A simple, one-paragraph prompt that agentically adopts the hangar-ai-constitution to any project.

---

## The Prompt

Copy and paste this prompt into your AI assistant. Replace `{{TARGET_REPO_PATH}}` with the absolute path to your project.

```
Clone the hangar-ai-constitution from https://github.com/AAInternal/hangar-ai-constitution.git to {{TARGET_REPO_PATH}}/../ (the parent directory of my project), then read the adoption guide at hangar-ai-constitution/docs/guides/adoption/brownfield-adoption.md and fully adopt the constitution to my project at {{TARGET_REPO_PATH}}, creating all required files (AGENTS.md, hangar-ai-specs/ structure) and writing characterization tests for existing code.
```

---

## Usage

### Step 1: Determine Your Project Path

Get the absolute path to your project:
```bash
cd /path/to/your/project
pwd
# Example output: /Users/john/repos/my-service
```

### Step 2: Fill in the Placeholder

Replace `{{TARGET_REPO_PATH}}` with your project path:

**Before:**
```
{{TARGET_REPO_PATH}}
```

**After:**
```
/Users/john/repos/my-service
```

### Step 3: Paste and Run

Paste the filled-in prompt into your AI assistant (GitHub Copilot, Claude, etc.).

---

## What the Agent Will Do

The agent will autonomously:

1. **Clone the Constitution** to the parent directory of your project
2. **Read the adoption guide** to understand the process
3. **Analyze your codebase** to determine technology and domain
4. **Create AGENTS.md** at your project root with proper authority hierarchy
5. **Create hangar-ai-specs/ structure** with project-rules.md
6. **Write characterization tests** for existing code
7. **Generate a compliance report** summarizing the adoption

---

## Expected Directory Structure After Adoption

```
your-projects-directory/
├── hangar-ai-constitution/     # Cloned constitution
│   ├── laws/
│   ├── avatars/
│   ├── agent-skills/
│   └── docs/guides/adoption/      # Where the agent reads the guide
│
└── your-project/                  # Your adopted project
    ├── AGENTS.md                  # NEW - Links to constitution
    ├── hangar-ai-specs/
    │   ├── changes/
    │   ├── project-rules.md       # NEW - Project-specific extensions
    │   └── AGENTS.md              # NEW - Project workflow instructions
    ├── src/
    │   └── test/                  # NEW/UPDATED - Characterization tests
    └── ...
```

---

## Example: Loyalty Service Legacy

For the workshop, the filled-in prompt would be:

```
Clone the hangar-ai-constitution from https://github.com/AAInternal/hangar-ai-constitution.git to /Users/aali/repos/american-airlines/../ (the parent directory of my project), then read the adoption guide at hangar-ai-constitution/docs/guides/adoption/brownfield-adoption.md and fully adopt the constitution to my project at /Users/aali/repos/american-airlines/loyalty-service-legacy, creating all required files (AGENTS.md, hangar-ai-specs/ structure) and writing characterization tests for existing code.
```

---

## Why This Works

This prompt is optimized for token efficiency through:

| Technique | How It's Applied |
|-----------|------------------|
| **Agentic Delegation** | Agent reads the guide itself instead of embedding instructions |
| **Reference vs Copy** | Points to brownfield-adoption.md rather than duplicating content |
| **Single Responsibility** | One clear task: adopt the constitution |
| **Implicit Context** | Agent discovers technology/domain from codebase analysis |
| **Index-First Navigation** | Agent uses constitution's index files to find relevant content |

The agent only reads what it needs from the ~500K token constitution, typically <30% for any single adoption.

---

## Troubleshooting

### Clone fails (authentication)

If git clone fails due to authentication:
1. Ensure you have access to the AAInternal organization
2. Or clone manually first, then use a modified prompt:
   ```
   The hangar-ai-constitution is already cloned at {{TARGET_REPO_PATH}}/../hangar-ai-constitution. 
   Read the adoption guide at hangar-ai-constitution/docs/guides/adoption/brownfield-adoption.md 
   and fully adopt the constitution to my project at {{TARGET_REPO_PATH}}.
   ```

### Agent reads too much

If the agent is reading the entire constitution:
- Remind it to use index files first: `laws/index.yaml`, `avatars/index.yaml`
- Ask it to read only the relevant avatar for your technology

### Adoption incomplete

If the agent stops early:
- Ask it to continue: "Continue the adoption, focusing on characterization tests"
- Or run specific phases: "Now create the hangar-ai-specs/ directory structure"

---
laws: [ENG-3.3]
avatar: [dotnet-core]
title: Function Length — C#/.NET
---

# ENG-3.3: Function Length — dotnet-core

Functions must do one thing. Maximum 20 lines. If a function needs a comment to explain what a block does, extract that block.

## Example (C#/.NET)

Break large orchestration methods into named private methods each ≤ 20 lines.
Name the method after the **what**, not the **how**.

**Rule**: Cyclomatic complexity ≤ 5 per function. SonarQube gate enforces this.

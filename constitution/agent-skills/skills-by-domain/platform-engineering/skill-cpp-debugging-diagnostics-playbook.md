---
skill:
  id: skill-cpp-debugging-diagnostics-playbook
  name: "C++ Debugging & Diagnostics Playbook"
  category: platform-engineering
  version: "1.0.0"
  avatar: cpp

laws:
  implements:
    - id: ENG-5.5
      title: Observability Law
    - id: ENG-6.7
      title: Audit Trail Law
  references:
    - id: ENG-4.1
      title: Atomic TDD Law (NON-NEGOTIABLE)
    - id: ENG-7.1
      title: Reliability Law

triggers:
  phrases:
    - "C++ debugging"
    - "C++ core dump"
    - "C++ GDB"
    - "C++ segfault"
    - "C++ memory leak"
    - "C++ profiling"
    - "C++ crash analysis"

followed_by:
  - skill-cpp-sanitizer-hardening
  - skill-cpp-logging-diagnostics-standards
---

# Skill: C++ Debugging & Diagnostics Playbook

## Purpose

Provide a standardized playbook for diagnosing C++ production issues and development-time defects. Per [ENG-5.5](laws/engineering/eng-5-devops.md), systems must be observable; per [ENG-6.7](laws/engineering/eng-6-security.md), diagnostic actions must be auditable.

## Procedure

1. **Configure core dumps** — set `ulimit -c unlimited` in service entrypoints; configure `kernel.core_pattern` to write cores to a persistent, access-controlled volume
2. **GDB/LLDB quick-start** — load the core with `gdb <binary> <core>`; run `bt full` for backtrace, `info threads` for thread state, `frame N` to inspect locals; use conditional breakpoints (`break file:line if expr`) for targeted debugging
3. **Detect memory leaks with Valgrind** — run `valgrind --tool=memcheck --leak-check=full` on integration test binaries outside CI (too slow for per-commit); track leak counts in a dashboard
4. **Profile CPU hotspots** — use `perf record -g` + `perf script | flamegraph.pl` to generate flamegraphs; attach `perf` to running processes with `-p <pid>` for production profiling
5. **Symbolize crashes** — store split debug info (built with `-gsplit-dwarf`) alongside release artifacts; use `addr2line -e <binary> <address>` or `llvm-symbolizer` to map addresses to source lines
6. **Enable AddressSanitizer in dev** — compile with `-fsanitize=address -fno-omit-frame-pointer` during development; ASan catches use-after-free, buffer overflow, and stack-use-after-return

## Governance Gate

Per [ENG-6.7](laws/engineering/eng-6-security.md), every production diagnostic session (core dump access, `perf` attach) must be logged with operator identity, timestamp, and justification. Per [ENG-5.5](laws/engineering/eng-5-devops.md), services without core dump collection configured fail the observability gate.

## Post-Mortem Analysis Checklist

- [ ] Core dump collected and preserved with incident ID
- [ ] Stack trace symbolized and attached to incident ticket
- [ ] Root cause identified and linked to failing test (per [ENG-4.1](laws/engineering/eng-4-testing.md))
- [ ] Fix verified by reproducing the crash scenario in a test

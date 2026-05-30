# KI-004 — DerivedData Accumulation

**Law:** ENG-4.2 (Test Pyramid Law)

## Symptom

Coverage silently reports 0% or `llvm-profdata` finds no input files, despite tests passing.

## Root Cause

Xcode creates a new `AmericanAirlines-XXXXXXXX` DerivedData directory per workspace path variation. After Xcode upgrades or workspace path changes, multiple stale directories accumulate. Each contains profraw files from a different Xcode version — all written at v8.

## Fix

```bash
# Wildcard is intentional — delete ALL matching directories
rm -rf ~/Library/Developer/Xcode/DerivedData/AmericanAirlines-*

# Verify clean state
ls ~/Library/Developer/Xcode/DerivedData/ | grep AmericanAirlines
# Should return nothing
```

Run this as part of bootstrap (once per machine) and after any Xcode upgrade.

## Detection

```bash
# Show raw profraw files and their LLVM versions
xcrun llvm-profdata show <path-to-file.profraw>
# Note: there is NO --summary flag. Use the plain show subcommand.
# The first line of output reports the profraw format version.
```

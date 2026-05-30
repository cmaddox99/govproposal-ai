#!/bin/bash
# ══════════════════════════════════════════════════════
#  HANGAR AI CONSTITUTION — TECH TALK DEMO SETUP
#  Run this script once before the talk
# ══════════════════════════════════════════════════════

DEMO_BASE="$(cd "$(dirname "$0")" && pwd)"
SLIDES="$DEMO_BASE/tech-talk-constitution-demo.html"

echo ""
echo "🔵  Verifying SonarQube is running..."
if curl -s -u admin:HangarConstitution2026 http://localhost:9000/api/system/status | grep -q '"status":"UP"'; then
  echo "    ✅ SonarQube UP at localhost:9000"
else
  echo "    ❌ SonarQube is NOT running! Start it before proceeding."
  echo "    Tip: Check Docker — docker start sonarqube"
  exit 1
fi

echo ""
echo "🔵  Opening slides..."
open "$SLIDES"
sleep 1

echo "🔵  Opening SonarQube dashboard..."
open "http://localhost:9000/dashboard?id=aa-loyalty-legacy"
sleep 1

echo "🔵  Opening phase artifacts (demo order)..."
open "$DEMO_BASE/phase-1-assess.html"
sleep 0.5
open "$DEMO_BASE/phase-2-govern.html"
sleep 0.5
open "$DEMO_BASE/phase-3-isolate.html"
sleep 0.5
open "$DEMO_BASE/phase-4-refactor.html"
sleep 0.5
open "$DEMO_BASE/phase-5-validate.html"
sleep 0.5
open "$DEMO_BASE/phase-6-certify.html"

echo ""
echo "═══════════════════════════════════════════════"
echo "  ✅  ALL TABS OPEN — DEMO READY"
echo "═══════════════════════════════════════════════"
echo ""
echo "  BROWSER TAB ORDER:"
echo "  1. Slides     → tech-talk-constitution-demo.html"
echo "  2. SonarQube  → localhost:9000/dashboard?id=aa-loyalty-legacy"
echo "  3-8. Phases   → phase-1 through phase-6"
echo ""
echo "  DEMO FLOW:"
echo "  Slides 1–3  → Constitutional AI concept + Hangar model"
echo "  Slide 4     → Intro the demo (say: AI-generated, WIP)"
echo "  Terminal    → Ask Copilot CLI to run Legacy Rescue on aa-loyalty-legacy"
echo "  Phase tabs  → Show artifacts as Copilot CLI walks through phases"
echo "  SonarQube   → Show dashboard during Phase 1 and Phase 5"
echo "  Slides 5+   → Wrap up, discussion"
echo ""
echo "  COPILOT CLI PROMPT TO USE AT START OF DEMO:"
echo '  "Run the Legacy Rescue workflow on the aa-loyalty-legacy codebase'
echo '   at hangar-ai-specs/changes/loyalty-legacy-rescue-demo/aa-loyalty-legacy'
echo '   following the Hangar AI Constitution. Start with Phase 1 — Assess."'
echo ""

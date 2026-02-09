#!/usr/bin/env bash
set -euo pipefail

# ─── Inflight API — Dev Server ─────────────────────────────
#
# Activates the Python venv and starts FastAPI on port 8000.
#
# Usage:
#   ./scripts/run.sh              # normal start
#   ./scripts/run.sh --install    # pip install first
# ────────────────────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_DIR"

# ─── 1. Activate virtual environment ───────────────────────

if [[ -d venv ]]; then
  source venv/bin/activate
  echo "✅ Python venv activated ($(python --version))"
else
  echo "❌ No venv/ found. Create it first:"
  echo "   python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
  exit 1
fi

# ─── 2. Install dependencies if requested ──────────────────

if [[ "${1:-}" == "--install" ]]; then
  echo "📦 Installing Python dependencies..."
  pip install -r requirements.txt
  echo ""
fi

# ─── 3. Read prewarm config (if demo-config.json exists nearby) ──

UI_CONFIG="../inflight-ui-poc/scripts/demo-config.json"
if [[ -f "$UI_CONFIG" ]] && command -v python3 &> /dev/null; then
  export PREWARM_AIRPORTS=$(python3 -c "import json; print(json.load(open('$UI_CONFIG')).get('prewarm_airports','FCO'))")
  export PREWARM_LANGUAGES=$(python3 -c "import json; print(json.load(open('$UI_CONFIG')).get('prewarm_languages','en,es,it'))")
  echo "📋 Pre-warm config from demo-config.json:"
  echo "   Airports:  $PREWARM_AIRPORTS"
  echo "   Languages: $PREWARM_LANGUAGES"
fi

# ─── 4. Start FastAPI ──────────────────────────────────────

echo ""
echo "🚀 Starting API on http://localhost:8000"
echo "   Docs at http://localhost:8000/docs"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

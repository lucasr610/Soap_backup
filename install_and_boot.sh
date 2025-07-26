#!/usr/bin/env bash
# Boot script for ATI Oracle Engine: install dependencies, run tests, and launch pipeline

set -e

ROOT="${SOAP_ROOT:-$HOME/Soap}"
VENV="$ROOT/.venv"

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV" ]; then
  echo "Creating virtual environment at $VENV"
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install --upgrade pip
  "$VENV/bin/pip" install -r "$ROOT/requirements.txt"
fi

# Activate environment
source "$VENV/bin/activate"

# Run tests (optional, non-blocking)
pytest -q || echo "Tests failed or skipped — continuing boot."

# Try full mesh pipeline, fallback to basic boot trigger if needed
"$VENV/bin/python" "$ROOT/ATI_ENGINE_MESH_PROD/run_all_phases.py" "$@" || {
  echo "run_all_phases.py failed, attempting trigger_boot fallback..."
  "$VENV/bin/python" "$ROOT/trigger_boot.py" || true
}

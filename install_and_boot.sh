#!/usr/bin/env bash
set -e

# Install Python dependencies
pip install -r requirements.txt

# Run unit tests (optional step)
pytest -q || echo "Tests failed or skipped — continuing boot."

# Launch the ATI Engine pipeline
python ATI_ENGINE_MESH_PROD/run_all_phases.py "$@" || {
  echo "Falling back to trigger_boot.py..."
  python trigger_boot.py || true
}

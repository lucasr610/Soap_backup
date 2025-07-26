#!/usr/bin/env bash
# Install dependencies and start Codex engine
# If .venv already exists, reuse it

set -e

ROOT="${SOAP_ROOT:-$HOME/Soap}"
VENV="$ROOT/.venv"

if [ ! -d "$VENV" ]; then
    echo "Creating virtual environment at $VENV"
    python3 -m venv "$VENV"
    "$VENV/bin/pip" install --upgrade pip
    "$VENV/bin/pip" install -r "$ROOT/requirements.txt"
fi

source "$VENV/bin/activate"

exec "$VENV/bin/python" "$ROOT/codex_controller.py" --loop --warm-start

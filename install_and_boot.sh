#!/usr/bin/env bash
set -e

# install dependencies
pip install -r requirements.txt

# run unit tests
pytest -q

# placeholder for boot logic
python trigger_boot.py || true

#!/usr/bin/env bash
# Install dependencies and run the ATI Engine pipeline
set -e
pip install -r requirements.txt
python ATI_ENGINE_MESH_PROD/run_all_phases.py "$@"


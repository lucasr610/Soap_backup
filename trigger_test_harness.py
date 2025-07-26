#!/usr/bin/env python3
"""Run all triggers and execute the agent pipeline for testing."""
import subprocess
from pathlib import Path

from ATI_ENGINE_MESH_PROD.agents.watson_phase import run_watson
from ATI_ENGINE_MESH_PROD.agents.father_phase import run_father
from ATI_ENGINE_MESH_PROD.agents.safety_officer_phase import run_safety_officer
from ATI_ENGINE_MESH_PROD.agents.arbiter_phase import run_arbiter
from ATI_ENGINE_MESH_PROD.agents.soap_phase import run_soap

TRIGGERS = [
    "+ATTENTION+",
    "+CODE-RED+",
    "+FULL_SAVE_NOW+",
    "+SPIN-DOWN+",
    "+SPIN-UP+",
]


def main() -> None:
    root = Path.home() / "Soap/triggers"
    for trig in TRIGGERS:
        path = root / trig
        print(f"⚡ Running {trig} ...")
        subprocess.run(["bash", str(path)], check=False)

    # After running shell triggers, execute the agent pipeline
    run_watson()
    run_father()
    run_safety_officer()
    run_arbiter()
    run_soap()


if __name__ == "__main__":
    main()

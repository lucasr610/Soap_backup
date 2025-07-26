#!/usr/bin/env python3
"""Run all triggers in sequence for testing and import pipeline agents."""
import subprocess
from pathlib import Path

from ATI_ENGINE_MESH_PROD.agents.watson_phase import run_watson
from ATI_ENGINE_MESH_PROD.agents.father_phase import run_father
from ATI_ENGINE_MESH_PROD.agents.safety_officer_phase import run_mother
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


if __name__ == "__main__":
    main()

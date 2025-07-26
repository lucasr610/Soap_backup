#!/usr/bin/env python3
"""Run ATI Engine pipeline phases sequentially or individually."""
import argparse

import sys
from pathlib import Path
CURRENT_DIR = Path(__file__).resolve().parents[1]
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from agents.watson_phase import run_watson
from agents.father_phase import run_father
from agents.mother_phase import run_mother
from agents.arbiter_phase import run_arbiter
from agents.soap_phase import run_soap

PHASES = {
    "watson": run_watson,
    "father": run_father,
    "mother": run_mother,
    "arbiter": run_arbiter,
    "soap": run_soap,
}


def run_all() -> None:
    """Run the full SOP generation pipeline."""
    for func in PHASES.values():
        func()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run agent phases individually or the full pipeline",
    )
    parser.add_argument(
        "--phase",
        choices=list(PHASES.keys()) + ["all"],
        default="all",
        help="Phase to run (default: all phases)",
    )
    args = parser.parse_args()

    if args.phase == "all":
        run_all()
    else:
        PHASES[args.phase]()


if __name__ == "__main__":
    main()

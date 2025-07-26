#!/usr/bin/env python3
"""Watson phase for ATI Engine Mesh.

Parses raw SOP text into a structured dictionary."""
import json
from copy import deepcopy


def structure_sop(raw_text: str) -> dict:
    """Parse raw SOP text into structured sections."""
    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
    return {
        "title": lines[0] if lines else "Untitled SOP",
        "purpose": "Describe the purpose.",
        "scope": "Define the scope here.",
        "tools": [],
        "materials": [],
        "safety": [],
        "procedure": lines[1:],
    }


def run_watson(raw_text: str) -> dict:
    """Return initial SOP structure from raw text."""
    sop = structure_sop(raw_text)
    sop["watson_backup"] = deepcopy(sop)
    sop["status"] = "watson_complete"
    return sop


if __name__ == "__main__":
    import sys
    text = sys.stdin.read()
    print(json.dumps(run_watson(text), indent=2))

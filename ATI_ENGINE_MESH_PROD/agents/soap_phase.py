#!/usr/bin/env python3
"""Soap phase for ATI Engine Mesh.

Generates final explanation and technical notes."""
import json
from copy import deepcopy
from typing import Dict, List, Tuple


def explain_sop(sop: Dict) -> Tuple[List[str], List[str]]:
    breakdown: List[str] = []
    tech_notes: List[str] = []

    breakdown.append(f"📌 Purpose: {sop.get('purpose', '').strip()}")
    breakdown.append(f"📍 Scope: {sop.get('scope', '').strip()}")

    breakdown.append("🧰 Tools needed:")
    for tool in sop.get('tools', []):
        breakdown.append(f"  - {tool}")
    breakdown.append("📦 Materials needed:")
    for mat in sop.get('materials', []):
        breakdown.append(f"  - {mat}")

    if sop.get('safety'):
        breakdown.append("🛡️ Safety Notes:")
        for note in sop['safety']:
            breakdown.append(f"  ⚠️ {note}")

    breakdown.append("🛠️ Procedure Steps:")
    for i, step in enumerate(sop.get('procedure', []), 1):
        breakdown.append(f"  Step {i}: {step}")
        text = step.lower()
        if any(k in text for k in ['remove', 'disassemble']):
            tech_notes.append(
                f"Step {i}: Disassembly step - ensure parts are organized and secure."
            )
        if any(k in text for k in ['torque', 'tighten']):
            tech_notes.append(
                f"Step {i}: Fastening step - use torque wrench to manufacturer spec."
            )
        if 'grease' in text:
            tech_notes.append(
                f"Step {i}: Lubrication - apply correct grease sparingly."
            )

    return breakdown, tech_notes


def run_soap(data: Dict) -> Dict:
    sop = deepcopy(data)
    sop["soap_backup"] = deepcopy(sop)
    breakdown, notes = explain_sop(sop)
    sop["explanation"] = breakdown
    sop["tech_notes"] = notes
    sop["status"] = "soap_complete"
    return sop


if __name__ == "__main__":
    import sys
    sop = json.load(sys.stdin)
    print(json.dumps(run_soap(sop), indent=2))

#!/usr/bin/env python3
"""Intelligence Officer phase.

Validates logic of structured SOPs."""
import json
from copy import deepcopy
from typing import List, Dict


def validate_logic(sop: Dict) -> List[str]:
    """Return list of logic issues in the SOP."""
    issues = []
    if not sop.get("tools"):
        issues.append("Missing tool list.")
    proc = sop.get("procedure", [])
    if not isinstance(proc, list) or not proc:
        issues.append("Procedure steps are missing or invalid.")
    else:
        actions = ["install", "remove", "check", "clean", "torque", "grease"]
        for idx, step in enumerate(proc, 1):
            if not any(verb in step.lower() for verb in actions):
                issues.append(f"Step {idx} may lack a clear action: '{step}'")
    return issues


def run_intelligence_officer(data: Dict) -> Dict:
    """Validate SOP logic and update status."""
    sop = deepcopy(data)
    sop["intelligence_backup"] = deepcopy(sop)
    issues = validate_logic(sop)
    if issues:
        sop["logic_issues"] = issues
        sop["status"] = "needs_human_review"
    else:
        sop["status"] = "intelligence_complete"
    return sop


if __name__ == "__main__":
    import sys
    sop = json.load(sys.stdin)
    print(json.dumps(run_intelligence_officer(sop), indent=2))

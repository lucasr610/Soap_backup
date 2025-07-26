#!/usr/bin/env python3
"""Arbiter phase for ATI Engine Mesh.

Resolves conflicts and finalizes SOP status."""
import json
from copy import deepcopy
from typing import Dict, List


def resolve_conflicts(sop: Dict) -> bool:
    """Return True if no conflicts found."""
    conflicts: List[str] = []
    if sop.get("logic_issues"):
        conflicts.extend(sop["logic_issues"])
    if not sop.get("safety"):
        conflicts.append("Missing safety procedures.")
    if conflicts:
        sop["conflict_fields"] = conflicts
        return False
    return True


def run_arbiter(data: Dict) -> Dict:
    sop = deepcopy(data)
    sop["arbiter_backup"] = deepcopy(sop)
    if resolve_conflicts(sop):
        sop["status"] = "arbiter_complete"
    else:
        sop["status"] = "arbiter_conflict"
    return sop


if __name__ == "__main__":
    import sys
    sop = json.load(sys.stdin)
    print(json.dumps(run_arbiter(sop), indent=2))

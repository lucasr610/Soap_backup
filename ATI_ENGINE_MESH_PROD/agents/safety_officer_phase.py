#!/usr/bin/env python3
"""Safety Officer phase.

Adds PPE defaults and regulatory references."""
import json
from copy import deepcopy
from pathlib import Path
from typing import Dict, List

PPE_DEFAULTS = [
    "Wear safety glasses.",
    "Use mechanic gloves.",
    "Ensure work area is clean and dry.",
]

HAZARD_FLAGS = [
    ("brake", "⚠️ Brake dust may contain asbestos. Avoid blowing or dry brushing."),
    ("jack", "⚠️ Always use jack stands. Never rely solely on a jack."),
    ("grease", "⚠️ Use nitrile gloves to avoid chemical exposure."),
    ("cotter pin", "⚠️ Watch for sharp edges when removing retaining hardware."),
]

DEFAULT_REG_RULES = {
    "General": [
        {"body": "OSHA", "rule": "29 CFR 1910"},
        {"body": "EPA", "rule": "RCRA"},
    ],
    "Aviation": [{"body": "FAA", "rule": "14 CFR Part 43"}],
    "Medical": [
        {"body": "FDA", "rule": "21 CFR Part 820"},
        {"body": "CDC", "rule": "Disinfection Guidelines"},
    ],
}

RULES_FILE = Path.home() / "Soap" / "overlay" / "regulatory_rules.json"


def load_rules() -> Dict:
    if RULES_FILE.is_file():
        try:
            return json.loads(RULES_FILE.read_text())
        except Exception:
            pass
    return DEFAULT_REG_RULES


def apply_safety(sop: Dict) -> List[str]:
    added = []
    sop.setdefault("safety", [])
    for rule in PPE_DEFAULTS:
        if rule not in sop["safety"]:
            sop["safety"].append(rule)
            added.append(rule)
    for step in sop.get("procedure", []):
        for keyword, warning in HAZARD_FLAGS:
            if keyword in step.lower() and warning not in sop["safety"]:
                sop["safety"].append(warning)
                added.append(warning)
    return added


def apply_regulatory_rules(sop: Dict, rules: Dict) -> List[str]:
    added = []
    industry = sop.get("industry", "General")
    targets = rules.get(industry, rules.get("General", []))
    sop.setdefault("regulatory_refs", [])
    for item in targets:
        ref = f"{item['body']}: {item['rule']}"
        if ref not in sop["regulatory_refs"]:
            sop["regulatory_refs"].append(ref)
            added.append(ref)
        if ref not in sop.get("safety", []):
            sop["safety"].append(ref)
            added.append(ref)
    return added


def run_safety_officer(data: Dict) -> Dict:
    sop = deepcopy(data)
    sop["safety_officer_backup"] = deepcopy(sop)
    rules = load_rules()
    apply_safety(sop)
    apply_regulatory_rules(sop, rules)
    sop["status"] = "safety_officer_complete"
    return sop


if __name__ == "__main__":
    import sys
    sop = json.load(sys.stdin)
    print(json.dumps(run_safety_officer(sop), indent=2))

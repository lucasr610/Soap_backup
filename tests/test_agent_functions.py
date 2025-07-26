import json
import types
from importlib import reload
from pathlib import Path

import agents.watson_phase as watson_phase
import agents.father_phase as father_phase
import agents.mother_phase as mother_phase
import agents.arbiter_phase as arbiter_phase
import agents.soap_phase as soap_phase


def reload_modules():
    reload(watson_phase)
    reload(father_phase)
    reload(mother_phase)
    reload(arbiter_phase)
    reload(soap_phase)


def test_structure_sop_keys():
    reload_modules()
    result = watson_phase.structure_sop("Title\nStep1")
    expected = {
        "title",
        "purpose",
        "scope",
        "tools",
        "materials",
        "safety",
        "procedure",
        "watson_backup",
    }
    assert set(result.keys()) == expected
    assert result["procedure"] == ["Step1"]


def test_apply_safety_and_rules():
    reload_modules()
    sop = {
        "procedure": ["install brake", "torque bolts"],
        "industry": "General",
    }
    added = mother_phase.apply_safety(sop)
    regs = mother_phase.apply_regulatory_rules(sop, mother_phase.DEFAULT_REG_RULES)
    assert isinstance(added, list)
    assert isinstance(regs, list)
    assert "safety" in sop and isinstance(sop["safety"], list)
    assert "regulatory_refs" in sop and isinstance(sop["regulatory_refs"], list)


def test_resolve_conflicts():
    reload_modules()
    sop = {"logic_issues": ["bad"], "safety": []}
    ok = arbiter_phase.resolve_conflicts(sop)
    assert not ok
    assert "conflict_fields" in sop


def test_explain_sop_structure():
    reload_modules()
    sop = {
        "purpose": "demo",
        "scope": "demo",
        "tools": ["hammer"],
        "materials": [],
        "safety": ["Wear glasses."],
        "procedure": ["Remove wheel"],
    }
    breakdown, notes = soap_phase.explain_sop(sop)
    assert isinstance(breakdown, list)
    assert isinstance(notes, list)
    assert any("Purpose" in line for line in breakdown)


def test_orchestrator_cycle(tmp_path, monkeypatch):
    import sys
    from pathlib import Path

    soap_pkg = Path(__file__).resolve().parents[1] / "Soap"
    sys.path.insert(0, str(soap_pkg))
    sys.modules.pop("core", None)
    sys.modules.pop("core.codex_folder_creator", None)
    sys.modules.pop("core.snapshot_rotator", None)
    from Soap.system_agents import motherboard_orchestrator as orchestrator

    reload_modules()
    monkeypatch.setattr(orchestrator, "run_watson", lambda: None)
    monkeypatch.setattr(orchestrator, "run_father", lambda: None)
    monkeypatch.setattr(orchestrator, "run_arbiter", lambda: None)
    monkeypatch.setattr(orchestrator, "run_soap", lambda: None)
    monkeypatch.setattr(orchestrator, "rotate_agent_snapshots", lambda: None)
    monkeypatch.setattr(orchestrator.time, "sleep", lambda x: None)
    hb = tmp_path / "hb.log"
    monkeypatch.setattr(orchestrator, "HEARTBEAT_PATH", hb)
    monkeypatch.setattr(orchestrator, "log_event", lambda msg: None)
    orchestrator.orchestrate_cycle()
    assert hb.exists()

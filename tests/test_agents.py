import json
import sys
from pathlib import Path
from types import ModuleType

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from importlib import reload
import agents.watson_phase as watson_phase
import agents.father_phase as father_phase
import agents.mother_phase as mother_phase
import agents.arbiter_phase as arbiter_phase
import agents.soap_phase as soap_phase


def reload_agents() -> None:
    reload(watson_phase)
    reload(father_phase)
    reload(mother_phase)
    reload(arbiter_phase)
    reload(soap_phase)


def test_agent_pipeline(tmp_path, monkeypatch):
    home = tmp_path
    monkeypatch.setattr(Path, "home", lambda: home)

    reload_agents()

    soap_dir = home / "Soap"
    queue_dir = soap_dir / "agent_queue"
    logs_dir = soap_dir / "data" / "logs"
    queue_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)

    task = {
        "raw_text": "Remove wheel\nTorque bolts\nGrease bearing",
        "status": "queued",
    }
    task_path = queue_dir / "task.json"
    task_path.write_text(json.dumps(task))

    watson_phase.run_watson()

    data = json.loads(task_path.read_text())
    data["tools"] = ["socket", "wrench"]
    data["materials"] = ["grease"]
    data["procedure"] = ["Remove wheel", "Grease bearing", "Torque bolts"]
    data["industry"] = "General"
    task_path.write_text(json.dumps(data))

    father_phase.run_father()
    mother_phase.run_mother()
    arbiter_phase.run_arbiter()
    soap_phase.run_soap()

    result = json.loads(task_path.read_text())
    assert result["status"] == "soap_complete"
    assert "explanation" in result
    assert "tech_notes" in result


def test_controller_process_queue(tmp_path, monkeypatch):
    home = tmp_path
    monkeypatch.setattr(Path, "home", lambda: home)

    reload_agents()

    # provide stub modules to avoid heavy deps
    stub_vec = ModuleType("rag_vectorizer")
    stub_vec.vectorize = lambda: None
    stub_warm = ModuleType("warm_start_engine")
    stub_warm.load_vectors = lambda: None
    stub_warm.search_similar = lambda text: []
    monkeypatch.setitem(sys.modules, "rag_vectorizer", stub_vec)
    monkeypatch.setitem(sys.modules, "warm_start_engine", stub_warm)

    from importlib import import_module

    codex = reload(import_module("codex_controller"))

    queue_dir = home / "Soap" / "agent_queue"
    queue_dir.mkdir(parents=True, exist_ok=True)

    task = {"raw_text": "Check pump", "status": "queued"}
    task_path = queue_dir / "pump.json"
    task_path.write_text(json.dumps(task))

    codex.process_queue(home / "Soap")

    data = json.loads(task_path.read_text())
    assert data["status"] == "arbiter_conflict"


def test_controller_multiple_runs(tmp_path, monkeypatch):
    """Ensure pipeline succeeds on three successive tasks."""
    home = tmp_path
    monkeypatch.setattr(Path, "home", lambda: home)

    reload_agents()

    stub_vec = ModuleType("rag_vectorizer")
    stub_vec.vectorize = lambda: None
    stub_warm = ModuleType("warm_start_engine")
    stub_warm.load_vectors = lambda: None
    stub_warm.search_similar = lambda text: []
    monkeypatch.setitem(sys.modules, "rag_vectorizer", stub_vec)
    monkeypatch.setitem(sys.modules, "warm_start_engine", stub_warm)

    from importlib import import_module

    codex = reload(import_module("codex_controller"))

    queue_dir = home / "Soap" / "agent_queue"
    queue_dir.mkdir(parents=True, exist_ok=True)

    for i in range(3):
        task = {"raw_text": f"Task {i}", "status": "queued"}
        path = queue_dir / f"task_{i}.json"
        path.write_text(json.dumps(task))
        codex.process_queue(home / "Soap")
        data = json.loads(path.read_text())
        assert data["status"] == "arbiter_conflict"

import json
from pathlib import Path
from importlib import reload

from fastapi.testclient import TestClient


def setup_app(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from backend.app import main as backend_main
    reload(backend_main)
    return TestClient(backend_main.app)


def test_health(tmp_path, monkeypatch):
    client = setup_app(tmp_path, monkeypatch)
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_submit_and_process(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    # stub heavy modules for controller
    import sys
    from types import ModuleType
    stub_vec = ModuleType("rag_vectorizer")
    stub_vec.vectorize = lambda: None
    stub_warm = ModuleType("warm_start_engine")
    stub_warm.load_vectors = lambda: None
    stub_warm.search_similar = lambda text: []
    monkeypatch.setitem(sys.modules, "rag_vectorizer", stub_vec)
    monkeypatch.setitem(sys.modules, "warm_start_engine", stub_warm)

    from backend.app import main as backend_main
    reload(backend_main)
    client = TestClient(backend_main.app)

    resp = client.post("/submit", json={"raw_text": "Check pump"})
    assert resp.status_code == 200
    name = resp.json()["queued"]

    # task file should exist
    path = tmp_path / "Soap" / "agent_queue" / name
    assert path.exists()

    resp = client.get("/tasks")
    assert resp.status_code == 200
    assert resp.json()["tasks"][0]["name"] == name

    resp = client.post("/process")
    assert resp.status_code == 200

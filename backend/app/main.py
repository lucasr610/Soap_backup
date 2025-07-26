from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pathlib import Path
import json
import time

from codex_controller import process_queue
from Soap.utils import get_soap_root

app = FastAPI(title="ATI Oracle Backend")


@app.get("/", response_class=HTMLResponse)
def index():
    path = Path(__file__).resolve().parents[2] / "frontend" / "index.html"
    return path.read_text()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/submit")
def submit(task: dict):
    if "raw_text" not in task:
        raise HTTPException(status_code=400, detail="raw_text required")

    root = get_soap_root()
    queue_dir = root / "agent_queue"
    queue_dir.mkdir(parents=True, exist_ok=True)
    name = f"task_{int(time.time()*1000)}.json"
    path = queue_dir / name
    task["status"] = "queued"
    path.write_text(json.dumps(task, indent=2))
    return {"queued": name}

@app.post("/process")
def process_once():
    root = get_soap_root()
    process_queue(root)
    return {"processed": True}

@app.get("/tasks")
def list_tasks():
    root = get_soap_root()
    queue_dir = root / "agent_queue"
    tasks = []
    for path in queue_dir.glob("*.json"):
        try:
            data = json.loads(path.read_text())
            tasks.append({"name": path.name, "status": data.get("status")})
        except Exception:
            continue
    return {"tasks": tasks}


# ATI Oracle Engine

The **ATI Oracle Engine** is the AI-driven backend of the ATI Nexus platform powering **Maintenance Docs**. It transforms raw, unstructured maintenance instructions into structured, verified, and human-readable **Standard Operating Procedures (SOPs)** using a secure, modular AI rotor framework.

---

## 🧠 System Overview

This platform uses a chain of **five protected agents** to handle SOP synthesis:

- **Watson** – parses raw task text into structured SOP format  
- **Father** – validates logic and consistency  
- **Mother** – performs safety, compliance, and regulation checks  
- **Arbiter** – detects unresolved issues and flags conflicts  
- **Soap** – generates the final human-readable SOP breakdown and notes  

🌀 The processing pipeline:
- Input tasks: `~/Soap/agent_queue/*.json`
- Output SOPs: `~/Soap/overlay/sops/*.json`

Other components include:
- Snapshot rotator
- Logging and state backup
- Vectorized search indexing

## Installation

Create and activate a Python virtual environment, then install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 🖥️ Frontend

The web dashboard is built with **React** and **Tailwind CSS**. It provides tabs to submit new tasks and view the current queue. The frontend is served directly by the FastAPI backend at the root URL.

---

## 🔁 Backup & Restore Utilities

- `backup_now.py`  
  Triggers `+FULL_SAVE_NOW+` to archive the current state.  
  Optional:
  - `SOAP_ROOT` — override Soap directory (default: `~/Soap`)
  - `BACKUP_LOG_PATH` — default is `~/Soap/logs/backup_now.log`

- `restore_now.py`  
  Triggers `+SPIN-UP+` to restore system state from a local snapshot.  
  Optional:
  - `RESTORE_LOG_PATH` — default is `~/Soap/logs/restore_now.log`

- `codex_controller.py`  
  Main pipeline runner. Processes SOP tasks through all agents.  
  Flags:
  - `--loop`: monitors the queue continuously (default interval: 5 sec)  
  - `--warm-start`: loads existing vector store before running

- `warm_start_engine.py`  
  Loads TF-IDF vectors from `~/Soap/vector_store/` if present.

- `rag_vectorizer.py`  
  Updates the vector store from SOPs in `~/Soap/overlay/sops/`.

- `system_snapshot.py`  
  Creates zip snapshots of the entire Soap directory and keeps the last five archives.

- `upload_to_gcs.py`  
  Stub script for uploading a file to Google Cloud Storage. Not used in local development.

---

## ✅ Running `codex_controller.py`

1. Place a JSON file in `~/Soap/agent_queue/` with at least a `raw_text` field and set `status` to `"queued"`:

```json
{
  "raw_text": "Replace coolant filter as per maintenance schedule.",
  "status": "queued"
}

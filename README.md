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
- GCS cloud sync
- Logging and state backup
- Vectorized search indexing

---

## 🔁 Backup & Restore Utilities

- `backup_now.py`  
  Triggers `+FULL_SAVE_NOW+` to archive the current state.  
  Optional:
  - `SOAP_ROOT` — override Soap directory (default: `~/Soap`)
  - `BACKUP_LOG_PATH` — default is `~/Soap/logs/backup_now.log`

- `restore_now.py`  
  Triggers `+SPIN-UP+` to restore system state from GCS archive.  
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
  Uploads a snapshot or other file to a specified Google Cloud Storage bucket.

---

## ✅ Running codex_controller.py

1. Place a JSON file in `~/Soap/agent_queue/` with at least a `raw_text` field and set `status` to `"queued"`:

```json
{
  "raw_text": "Replace coolant filter as per maintenance schedule.",
  "status": "queued"
}

## 📦 Installation

1. Install Python 3.11 or later.
2. Install required packages:

   ```bash
   pip install -r requirements.txt
   ```

Set the `SOAP_ROOT` environment variable if your Soap directory is not `~/Soap`.

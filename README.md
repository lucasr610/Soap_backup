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

---

## 🧩 Vector Store & RAG Components

- `warm_start_engine.py`  
  Loads TF-IDF vector store from `~/Soap/vector_store/` (if available).

- `rag_vectorizer.py`  
  Indexes all SOPs under `~/Soap/overlay/sops/` to update the vector store for hybrid search and retrieval.

---

## 🌀 SOP Processing Pipeline

Run SOP tasks through all agents via

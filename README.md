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

---

## 📦 Installation

1. Install Python 3.11 or later.
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate


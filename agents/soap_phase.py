# ~/ATI_ORACLE_ENGINE/agents/soap_phase.py
#!/usr/bin/env python3
"""
soap_phase.py: Final explanation agent for ATI SOP system.
Generates human-readable breakdown and technical notes for fully verified SOPs.
"""

import json
import logging
from pathlib import Path

HOME_DIR = Path.home()
QUEUE_DIR = HOME_DIR / "Soap" / "agent_queue"
LOG_DIR = HOME_DIR / "Soap" / "data" / "logs"
LOG_FILE = LOG_DIR / "soap_phase.log"

def setup_logging():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=str(LOG_FILE),
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s'
    )

logger = logging.getLogger()

def log(message, level=logging.INFO):
    print(message)
    logger.log(level, message)

def explain_sop(sop: dict):
    breakdown = []
    tech_notes = []
    breakdown.append(f"📌 Purpose: {sop.get('purpose', '').strip()}")
    breakdown.append(f"📍 Scope: {sop.get('scope', '').strip()}")
    breakdown.append("🧰 Tools needed:")
    for tool in sop.get('tools', []):
        breakdown.append(f"  - {tool}")
    breakdown.append("📦 Materials needed:")
    for mat in sop.get('materials', []):
        breakdown.append(f"  - {mat}")
    if sop.get('safety'):
        breakdown.append("🛡️ Safety Notes:")
        for note in sop['safety']:
            breakdown.append(f"  ⚠️ {note}")
    breakdown.append("🛠️ Procedure Steps:")
    for i, step in enumerate(sop.get('procedure', []), 1):
        breakdown.append(f"  Step {i}: {step}")
        text = step.lower()
        if any(k in text for k in ["remove", "disassemble"]):
            tech_notes.append(f"Step {i}: Disassembly step - ensure parts are organized and secure.")
        if any(k in text for k in ["torque", "tighten"]):
            tech_notes.append(f"Step {i}: Fastening step - use torque wrench to manufacturer spec.")
        if 'grease' in text:
            tech_notes.append(f"Step {i}: Lubrication - apply correct grease sparingly.")
    return breakdown, tech_notes

def run_soap():
    setup_logging()
    tasks = sorted(QUEUE_DIR.glob('*.json'))
    for task in tasks:
        try:
            data = json.loads(task.read_text())
            if data.get('status') != 'arbiter_complete':
                continue
            log(f"🧽 Soap processing: {task.name}")
            breakdown, tech_notes = explain_sop(data)
            data['soap_backup'] = json.loads(json.dumps(data))
            data['explanation'] = breakdown
            data['tech_notes'] = tech_notes
            data['status'] = 'soap_complete'
            task.write_text(json.dumps(data, indent=2))
            log(f"✅ Soap complete: {task.name}")
        except Exception as e:
            log(f"❌ Soap error on {task.name}: {e}", level=logging.ERROR)

if __name__ == '__main__':
    run_soap()

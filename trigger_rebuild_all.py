#!/usr/bin/env python3
"""Rebuild-all trigger wrapper."""
import subprocess
from pathlib import Path
import time

from Soap.utils import get_soap_root

ROOT = get_soap_root()
LOG_PATH = ROOT / "logs/trigger_rebuild_all.log"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


def log(msg: str) -> None:
    with open(LOG_PATH, "a") as fh:
        fh.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")


def main() -> None:
    print("🔨 [+REBUILD-ALL+] Restoring protected files from registry...")
    log("Rebuild-all trigger fired")
    subprocess.run(f"python3 {ROOT}/rebuild_all.py", shell=True)
    log("Rebuild-all complete")


if __name__ == "__main__":
    main()

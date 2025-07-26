#!/usr/bin/env python3
"""Full save trigger wrapper."""
import subprocess
from pathlib import Path
import time

from Soap.utils import get_soap_root

ROOT = get_soap_root()
LOG_PATH = ROOT / "logs/trigger_full_save.log"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


def log(msg: str) -> None:
    with open(LOG_PATH, "a") as fh:
        fh.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")


def main() -> None:
    print("💾 [+FULL-SAVE+] Zipping and uploading Soap...")
    log("Full save trigger fired")
    subprocess.run(f"python3 {ROOT}/full_save.py", shell=True)
    log("Full save complete")


if __name__ == "__main__":
    main()

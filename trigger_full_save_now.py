#!/usr/bin/env python3
"""Immediate full save trigger wrapper."""
import subprocess
from pathlib import Path
import time

from Soap.utils import get_soap_root

ROOT = get_soap_root()
LOG_PATH = ROOT / "logs/trigger_full_save_now.log"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


def log(msg: str) -> None:
    with open(LOG_PATH, "a") as fh:
        fh.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")


def main() -> None:
    print("💾 [+FULL_SAVE_NOW+] Saving system state now...")
    log("Full save now trigger fired")
    subprocess.run(f"python3 {ROOT}/full_save_now.py", shell=True)
    log("Full save now complete")


if __name__ == "__main__":
    main()

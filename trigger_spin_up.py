#!/usr/bin/env python3
"""Spin-Up trigger wrapper."""
import subprocess
from pathlib import Path
import time

from Soap.utils import get_soap_root

ROOT = get_soap_root()
LOG_PATH = ROOT / "logs/trigger_spin_up.log"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


def log(msg: str) -> None:
    with open(LOG_PATH, "a") as fh:
        fh.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")


def main() -> None:
    print("🔄 [+SPIN-UP+] Restoring from cloud and relaunching rotors...")
    log("Spin-Up trigger fired")

    boot_script = Path.home() / "Soap/install_and_boot.sh"

    if boot_script.exists():
        subprocess.run(["bash", str(boot_script)], check=False)
    else:
        fallback = ROOT / "spin_up.py"
        subprocess.run(f"python3 {fallback}", shell=True)

    log("Spin-Up complete")


if __name__ == "__main__":
    main()

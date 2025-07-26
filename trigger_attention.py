# ~/Soap/trigger_attention.py

import subprocess
from pathlib import Path
import time

from Soap.utils import get_soap_root

ROOT = get_soap_root()
LOG_PATH = ROOT / "logs/trigger_attention.log"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


def log(msg):
    with open(LOG_PATH, "a") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")


def main():
    print("🧠 [+ATTENTION+] SYSTEM IS WAKING UP...")
    log("Attention trigger fired.")
    subprocess.run(f"python3 {ROOT}/attention.py", shell=True)
    print("🔁 Handing off to ROTOR_FUSION...")
    subprocess.run(f"python3 {ROOT}/rotor_fusion.py +CODE-RED+", shell=True)


if __name__ == "__main__":
    main()

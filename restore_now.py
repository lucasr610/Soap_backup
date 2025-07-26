#!/usr/bin/env python3
"""Restore Now Trigger."""
import logging
import os
import subprocess
import sys
from pathlib import Path

from Soap.utils import get_soap_root


def setup_logger() -> logging.Logger:
    default_log = get_soap_root() / "logs/restore_now.log"
    env_log = os.getenv("RESTORE_LOG_PATH")
    log_file = Path(env_log if env_log else default_log).expanduser()

    log_file.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("restore_now")
    logger.setLevel(logging.INFO)

    fmt = logging.Formatter("%(asctime)s %(message)s")
    fh = logging.FileHandler(log_file)
    fh.setFormatter(fmt)
    logger.addHandler(fh)
    logger.addHandler(logging.StreamHandler(sys.stdout))

    return logger


def main() -> None:
    logger = setup_logger()
    trigger = get_soap_root() / "triggers/+SPIN-UP+"
    logger.info("Restore Now triggered. Using trigger %s", trigger)
    print("🗃️ [RESTORE-NOW] Calling +SPIN-UP+ trigger...")
    if not trigger.is_file():
        logger.error("Trigger not found: %s", trigger)
        sys.exit(f"Trigger not found: {trigger}")

    try:
        subprocess.run(["bash", str(trigger)], check=True)
    except subprocess.CalledProcessError as exc:
        logger.error("Restore failed with code %s", exc.returncode)
        print("❌ [RESTORE-NOW] Restore failed.")
        sys.exit(exc.returncode)
    else:
        logger.info("Restore completed successfully.")
        print("✅ [RESTORE-NOW] Restore finished.")


if __name__ == "__main__":
    main()

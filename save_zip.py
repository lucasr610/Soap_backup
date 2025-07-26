#!/usr/bin/env python3
"""Archive the Soap directory into a single zip file."""
import os
from pathlib import Path
from core.snapshot_rotator import rotate_snapshots


def main() -> None:
    root = Path(os.getenv("SOAP_ROOT", Path.home() / "Soap"))
    dest = root / "snapshots"
    dest.mkdir(parents=True, exist_ok=True)
    snap = rotate_snapshots(str(root), str(dest), max_versions=1)
    print(f"[SAVE-ZIP] Archive written to {snap}")


if __name__ == "__main__":
    main()

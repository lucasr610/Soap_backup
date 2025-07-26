#!/usr/bin/env python3
"""Create a full snapshot of the Soap directory."""
from system_snapshot import create_snapshot


def main() -> None:
    snap = create_snapshot()
    print(f"[FULL-SAVE] Snapshot created at {snap}")


if __name__ == "__main__":
    main()

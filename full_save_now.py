#!/usr/bin/env python3
"""Immediately create a snapshot of the Soap directory."""
from system_snapshot import create_snapshot


def main() -> None:
    snap = create_snapshot()
    print(f"[FULL_SAVE_NOW] Snapshot created at {snap}")


if __name__ == "__main__":
    main()

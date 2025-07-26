from pathlib import Path

from core.snapshot_rotator import rotate_snapshots
from Soap.utils import get_soap_root


def create_snapshot(dst: Path | None = None) -> Path:
    root = get_soap_root()
    dest = dst or root / "snapshots"
    dest.mkdir(parents=True, exist_ok=True)
    snap = rotate_snapshots(str(root), str(dest), max_versions=5)
    return Path(snap)


if __name__ == "__main__":
    snapshot = create_snapshot()
    print(f"Snapshot saved to {snapshot}")

import shutil
import time
import os

def rotate_snapshots(src_dir, dst_dir, max_versions=3):
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    new_snapshot = os.path.join(dst_dir, f"snapshot_{timestamp}.zip")
    shutil.make_archive(new_snapshot.replace('.zip', ''), 'zip', src_dir)
    versions = sorted([f for f in os.listdir(dst_dir) if f.startswith("snapshot_") and f.endswith(".zip")])
    while len(versions) > max_versions:
        os.remove(os.path.join(dst_dir, versions.pop(0)))
    return new_snapshot

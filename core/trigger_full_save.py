from core.snapshot_rotator import rotate_snapshots

def trigger_full_save(src_dir, dst_dir):
    return rotate_snapshots(src_dir, dst_dir)

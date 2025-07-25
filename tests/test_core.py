import os
import tempfile
import zipfile
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from core.codex_folder_creator import create_codex_structure
from core.snapshot_rotator import rotate_snapshots


def test_create_codex_structure(tmp_path):
    base = tmp_path / 'codex'
    create_codex_structure(base)
    for folder in ['agents', 'core', 'triggers', 'configs', 'secrets', 'outputs']:
        assert (base / folder).exists()


def test_rotate_snapshots(tmp_path):
    src = tmp_path / 'src'
    dst = tmp_path / 'dst'
    src.mkdir()
    dst.mkdir()
    # create a file in src
    file_path = src / 'file.txt'
    file_path.write_text('data')

    snap1 = rotate_snapshots(src, dst, max_versions=2)
    assert os.path.isfile(snap1)
    # create another file to change snapshot content
    file_path.write_text('new')
    import time
    time.sleep(1)
    snap2 = rotate_snapshots(src, dst, max_versions=2)
    assert os.path.isfile(snap2)
    # create third snapshot to trigger rotation
    file_path.write_text('more')
    time.sleep(1)
    snap3 = rotate_snapshots(src, dst, max_versions=2)
    assert os.path.isfile(snap3)
    snaps = sorted(p for p in os.listdir(dst) if p.startswith('snapshot_'))
    assert len(snaps) == 2

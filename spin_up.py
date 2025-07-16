import os
import zipfile

def spin_up(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"[SPIN-UP] Restored from {zip_path}")

import os
import zipfile
import time

def spin_down(folder, out_zip):
    ts = time.strftime("%Y%m%d_%H%M%S")
    zip_name = f"{out_zip}_{ts}.zip"
    with zipfile.ZipFile(zip_name, 'w') as z:
        for root, dirs, files in os.walk(folder):
            for f in files:
                path = os.path.join(root, f)
                z.write(path, os.path.relpath(path, folder))
    print(f"[SPIN-DOWN] Saved snapshot to {zip_name}")

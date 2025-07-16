import os

def create_codex_structure(base_path):
    folders = [
        "agents",
        "core",
        "triggers",
        "configs",
        "secrets",
        "outputs"
    ]
    for folder in folders:
        path = os.path.join(base_path, folder)
        os.makedirs(path, exist_ok=True)
    return True

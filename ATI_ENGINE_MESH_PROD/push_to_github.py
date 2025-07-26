#!/usr/bin/env python3
"""Push local repo to GitHub with configurable remote and branch."""

import json
import os
import subprocess
from pathlib import Path

CONFIG_FILE = Path(__file__).with_name("config.json")


def load_config():
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except Exception:
            pass
    return {}


def get_setting(key: str, prompt: str) -> str:
    val = os.getenv(key)
    if not val:
        cfg = load_config()
        val = cfg.get(key.lower())
    if not val:
        val = input(prompt).strip()
    return val


def find_remote(url: str):
    try:
        output = subprocess.check_output(["git", "remote", "-v"], text=True)
    except subprocess.CalledProcessError as exc:
        print(f"Error reading git remotes: {exc}")
        return None
    for line in output.splitlines():
        parts = line.split()
        if len(parts) >= 2 and parts[1] == url:
            return parts[0]
    return None


def ensure_remote(url: str):
    remote = find_remote(url)
    if remote:
        return remote
    remote = input(f"Remote for {url} not found. Enter name to add (or leave blank to abort): ").strip()
    if not remote:
        print("Aborting push.")
        return None
    try:
        subprocess.check_call(["git", "remote", "add", remote, url])
        return remote
    except subprocess.CalledProcessError as exc:
        print(f"Failed to add remote: {exc}")
        return None


def push(remote: str, branch: str):
    try:
        subprocess.check_call(["git", "push", remote, branch])
        return True
    except subprocess.CalledProcessError as exc:
        print(f"Push failed: {exc}")
        return False


def main():
    repo_url = get_setting("REPO_URL", "Repository URL: ")
    branch = get_setting("BRANCH_NAME", "Branch to push: ")
    if not repo_url or not branch:
        print("Repository URL and branch are required.")
        return
    remote = ensure_remote(repo_url)
    if not remote:
        return
    print(f"Pushing to {remote}/{branch}...")
    if push(remote, branch):
        print("Push complete.")


if __name__ == "__main__":
    main()

import os
import argparse
import subprocess
from pathlib import Path


def push_to_github(repo_path: Path, repo_url: str | None, commit_msg: str) -> None:
    """Commit and push changes in repo_path to repo_url."""
    try:
        subprocess.run(["git", "-C", str(repo_path), "add", "-A"], check=True)
        subprocess.run(["git", "-C", str(repo_path), "commit", "-m", commit_msg], check=True)
    except subprocess.CalledProcessError:
        # Nothing to commit or add failed
        return

    cmd = ["git", "-C", str(repo_path), "push"]
    if repo_url:
        cmd.append(repo_url)
        cmd.append("HEAD")
    subprocess.run(cmd, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Commit and push local changes to GitHub")
    parser.add_argument("--repo-url", default=os.getenv("REPO_URL"), help="Remote repository URL")
    parser.add_argument("--commit-message", default=os.getenv("COMMIT_MSG", "Auto commit"), help="Commit message")
    parser.add_argument("--path", default=os.getenv("REPO_PATH", str(Path.cwd())), help="Path to git repository")
    args = parser.parse_args()

    push_to_github(Path(args.path), args.repo_url, args.commit_message)


if __name__ == "__main__":
    main()

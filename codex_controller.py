#!/usr/bin/env python3
"""Master controller for the SOP pipeline.

Scans ``$SOAP_ROOT``/agent_queue (or ``~/Soap`` by default) for tasks and runs
them through all five agents in sequence. Completed SOPs are exported to
``$SOAP_ROOT``/overlay/sops/.
"""
import argparse
import json
import time
from pathlib import Path

from agents.watson_phase import run_watson
from agents.father_phase import run_father
from agents.mother_phase import run_mother
from agents.arbiter_phase import run_arbiter
from agents.soap_phase import run_soap
from warm_start_engine import load_vectors, search_similar
from rag_vectorizer import vectorize

from Soap.utils import get_soap_root


def attach_related_sops(queue_dir: Path) -> None:
    """Attach related SOP paths to queued tasks using vector search."""
    for task in queue_dir.glob("*.json"):
        try:
            data = json.loads(task.read_text())
            if data.get("status") != "queued":
                continue
            raw_text = data.get("raw_text")
            if not raw_text:
                continue
            related = search_similar(raw_text)
            if related:
                data["related_sops"] = related
                task.write_text(json.dumps(data, indent=2))
        except Exception:
            continue


def process_queue(root: Path) -> None:
    """Run all agents once and export completed SOPs."""
    queue_dir = root / "agent_queue"
    output_dir = root / "overlay" / "sops"
    output_dir.mkdir(parents=True, exist_ok=True)

    if not any(queue_dir.glob("*.json")):
        return

    attach_related_sops(queue_dir)

    for path in sorted(queue_dir.glob("*.json")):
        try:
            data = json.loads(path.read_text())
        except Exception as exc:
            logging.error("Invalid JSON %s: %s", path.name, exc)
            continue

        if data.get("status") == "queued":
            data = run_watson(data)
        if data.get("status") == "watson_complete":
            data = run_father(data)
        if data.get("status") == "father_complete":
            data = run_mother(data)
        if data.get("status") in {"father_complete", "mother_complete", "needs_human_review"}:
            data = run_arbiter(data)
        if data.get("status") == "arbiter_complete":
            data = run_soap(data)

        path.write_text(json.dumps(data, indent=2))
        if data.get("status") == "soap_complete":
            out = output_dir / path.name
            out.write_text(json.dumps(data, indent=2))

    vectorize()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run SOP pipeline")
    parser.add_argument(
        "--loop",
        action="store_true",
        help="Continuously watch queue",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=5,
        help="Loop sleep seconds",
    )
    parser.add_argument(
        "--warm-start",
        action="store_true",
        help="Load vector store before running",
    )
    args = parser.parse_args()

    root = get_soap_root()
    if args.warm_start:
        load_vectors()
    while True:
        process_queue(root)
        if not args.loop:
            break
        time.sleep(args.interval)


if __name__ == "__main__":
    main()

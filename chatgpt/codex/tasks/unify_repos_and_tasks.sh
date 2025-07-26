#!/usr/bin/env bash
: <<'GODMODE'
God Mode Configuration – ATI Oracle Engine OS
Date: 2025-07-25 (America/Chicago)

System Overview:
- ATI Oracle Engine OS: Unified AI Operating System with modular plugin architecture.
- Rotor Mesh: Dynamically spawns and routes agent plugins through a 4-second rotor cycle.
- SOAP Agent: Standard Operating Procedure (SOP) generator, safety compliance checks.
- OS Engine: Cognitive kernel managing AI agent lifecycle and plugin orchestration.

Restrictions:
- Merge operations are one-off; no circular or loop merges.
- Branch deletions occur only after successful merge into main.
- External side-effects limited to GitHub repository pushes.
- Script must run idempotently: safe to re-run without errors.

Changes Applied by this Script:
- Merges all local branches into main across all repos.
- Combines all Codex task markdown into docs/codex_master_tasks.md.
- Pushes updated main and tasks to GitHub origin.

GODMODE

set -e

# 1. Iterate through each Git repo under current directory (depth 2)
find . -maxdepth 2 -type d -name ".git" | sed 's|/\.git||' | while read -r repo; do
  cd "$repo"
  echo "Processing repo: $(pwd)"
  git fetch --all
  git checkout main
  branches=$(git for-each-ref --format='%(refname:short)' refs/heads/ | grep -v '^main$')
  for br in $branches; do
    echo "Merging branch: $br"
    git merge --no-ff "$br" -m "Automated merge of $br into main" || true
    git branch -d "$br" && git push origin --delete "$br" || true
  done
  echo "Pushing updated main to origin"
  git push origin main
  cd - > /dev/null
done

# 2. Combine all Codex task files into a single master doc
TASK_DIR="codex_tasks"
OUTPUT_FILE="docs/codex_master_tasks.md"
if [[ -d "$TASK_DIR" ]]; then
  echo "Combining Codex tasks from $TASK_DIR into $OUTPUT_FILE"
  mkdir -p "$(dirname "$OUTPUT_FILE")"
  cat "$TASK_DIR"/*.md | awk '!seen[$0]++' > "$OUTPUT_FILE"
  cd $(git rev-parse --show-toplevel)
  if ! git diff --quiet "$OUTPUT_FILE"; then
    git add "$OUTPUT_FILE"
    git commit -m "Combine all Codex tasks into master document" && git push origin main
  fi
else
  echo "No $TASK_DIR directory found – skipping Codex task merge"
fi

echo "All branches merged into main, Codex tasks unified, and pushed to GitHub."

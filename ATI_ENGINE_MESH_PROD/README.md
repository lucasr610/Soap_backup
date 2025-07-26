# ATI Engine Mesh Prod Utilities

This directory contains helper scripts for working with the production mesh.

## `push_to_github.py`

Pushes the current repository to a GitHub remote. The script determines the
repository URL and target branch from the following sources, in order:

1. Environment variables `REPO_URL` and `BRANCH_NAME`.
2. A local `config.json` file located next to the script with keys
   `"repo_url"` and `"branch"`.
3. Interactive user input.

If the specified remote is not found in the current git configuration, the
script prompts for a remote name and adds it before pushing. Errors are
reported instead of raising uncaught exceptions.

### Example

```bash
export REPO_URL=https://github.com/myorg/myrepo.git
export BRANCH_NAME=main
python push_to_github.py
```

Alternatively create a `config.json` file:

```json
{
  "repo_url": "https://github.com/myorg/myrepo.git",
  "branch": "main"
}
```

Running the script without environment variables will then use these values.

